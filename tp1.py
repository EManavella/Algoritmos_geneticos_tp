import random
import math

# ─────────────────────────────────────────
#  PARÁMETROS DEL PROBLEMA
# ─────────────────────────────────────────
NUM_BITS       = 30                  # Longitud del cromosoma
COEF           = 2**NUM_BITS - 1     # 2^30 - 1
DOMINIO_MAX    = 2**NUM_BITS - 1     # [0, 2^30 - 1]
TAM_POBLACION  = 10
CICLOS         = 200
PROB_CROSSOVER = 0.75
PROB_MUTACION  = 0.05

# ─────────────────────────────────────────
#  FUNCIÓN OBJETIVO
# ─────────────────────────────────────────
def funcion_objetivo(cromosoma: list[int]) -> float:
    """f(x) = (x / coef)^2   con x = valor decimal del cromosoma."""
    x = decodificar(cromosoma)
    return (x / COEF) ** 2

def fitness(poblacion: list) -> float:
    fobj = [funcion_objetivo(ind) for ind in poblacion]
    total = sum(fobj)
    return [f/total for f in fobj]

def decodificar(cromosoma: list[int]) -> int:
    """Convierte lista de bits ["0", "1", ..., "1"] a entero."""
    return int("".join(str(b) for b in cromosoma), 2)

def individuo_aleatorio() -> list[int]:
    return [random.randint(0, 1) for _ in range(NUM_BITS)]

def ruleta (poblacion: list, lista_fitness: list[float]) -> list[int]:
    sum_fitness = sum(lista_fitness) #Calcular el total del fitness

    casillas = []
    for f in lista_fitness:
        cantidad = round(f * 100)
        if cantidad == 0: # fitness muy bajo, pero queremos que tenga al menos 1 casilla
            cantidad = 1
        casillas.append(cantidad)

    ruleta = []
    for indice, cantidad in enumerate(casillas):
        for _ in range(cantidad):
            ruleta.append(indice)   # repetimos el índice 'cantidad' veces


    posicion1 = random.randint(0, len(ruleta) - 1)      # número al azar entre 0 y 99
    padre1 = poblacion[ruleta[posicion1]]      # el cromosoma en sí 
    
    posicion2 = random.randint(0, len(ruleta) - 1)
    padre2 = poblacion[ruleta[posicion2] ]   # el cromosoma en sí

    return padre1, padre2


def crossover1punto(padre1: list[int], padre2: list[int]) -> tuple[list[int], list[int]]:
    if random.random() <= PROB_CROSSOVER:
        
        punto = random.randint(0, NUM_BITS - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2, punto
    else:
        return padre1[:], padre2[:], None
    
def mutacion(cromosoma: list[int]) -> list[int]:
    cromosoma = cromosoma[:]
    for i in range(len(cromosoma)):
        if random.random() <= PROB_MUTACION:
            cromosoma[i] = 1 - cromosoma[i]
    return cromosoma

def estadisticas(poblacion):
    valores = [funcion_objetivo(ind) for ind in poblacion]
    maximo   = max(valores)
    minimo   = min(valores)
    promedio = sum(valores) / len(valores)
    
    # Desviación estándar: σ = sqrt(Σ(fi - f̄)² / N)
    varianza = sum((f - promedio) ** 2 for f in valores) / len(valores)
    desv_std = varianza ** 0.5

    idx_max = valores.index(maximo)
    return {
        "maximo":    maximo,
        "minimo":    minimo,
        "promedio":  promedio,
        "desv_std":  desv_std,
        "cromosoma": poblacion[idx_max]
    }

poblacion = [individuo_aleatorio() for _ in range(TAM_POBLACION)]
historial = [] 


print("POBLACIÓN INICIAL")
print("")

for ciclo in range(1, CICLOS + 1):
    lista_fitness = fitness(poblacion)
    nueva_poblacion = []

    while len(nueva_poblacion) < TAM_POBLACION:
        padre1, padre2 = ruleta(poblacion, lista_fitness)
        hijo1, hijo2, punto = crossover1punto(padre1, padre2)
        hijo1 = mutacion(hijo1)
        hijo2 = mutacion(hijo2)

        nueva_poblacion.append(hijo1)
        if len(nueva_poblacion) < TAM_POBLACION:
            nueva_poblacion.append(hijo2)
    
    poblacion = nueva_poblacion[:]
    historial.append(estadisticas(poblacion))

print(f"{'Ciclo':>6} | {'Máximo':>10} | {'Mínimo':>10} | {'Promedio':>10} | {'Desv.Std':>10} | Cromosoma del máximo")
print("─" * 105)

for i, stats in enumerate(historial, 1):
    print(f"{i:>6} | {stats['maximo']:>10.6f} | {stats['minimo']:>10.6f} | {stats['promedio']:>10.6f} | {stats['desv_std']:>10.6f} | {stats['cromosoma']}")


# Mejor solución global
mejor = max(historial, key=lambda s: s["maximo"])
print(f"\n{'═' * 90}")
print(f"MEJOR SOLUCIÓN GLOBAL")
print(f"  Cromosoma : {mejor['cromosoma']}")
print(f"  X         : {decodificar(mejor['cromosoma'])}")
print(f"  F.Obj     : {mejor['maximo']:.6f}")