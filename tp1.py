import random
import math
import time
import matplotlib.pyplot as plt


NUM_BITS       = 30                  # Longitud del cromosoma
COEF           = 2**NUM_BITS - 1     # 2^30 - 1
DOMINIO_MAX    = 2**NUM_BITS - 1     # [0, 2^30 - 1]
TAM_POBLACION  = 10
CICLOS         = 20
PROB_CROSSOVER = 0.75
PROB_MUTACION  = 0.05


def funcion_objetivo(cromosoma: list[int]) -> float:
    x = bits_a_dec(cromosoma)
    return (x / COEF) ** 2

def fitness(poblacion: list) -> float:
    fobj = [funcion_objetivo(ind) for ind in poblacion]
    total = sum(fobj)
    return [f/total for f in fobj]

def bits_a_dec(cromosoma: list[int]) -> int: # Convertir la lista de bits a un número decimal
    return int("".join(str(b) for b in cromosoma), 2)

def cromosoma_aleatorio() -> list[int]:
    return [random.randint(0, 1) for _ in range(NUM_BITS)]

def ruleta (poblacion: list, lista_fitness: list[float]) -> list[int]:

    casillas = []
    for f in lista_fitness:
        cantidad = round(f * 100)
        if cantidad == 0: # fitness muy bajo, pero obligamos a que tenga al menos 1 casilla
            cantidad = 1
        casillas.append(cantidad)

    ruleta = []
    for indice, cantidad in enumerate(casillas):
        for _ in range(cantidad):
            ruleta.append(indice)   # repetimos el índice 'cantidad' veces

    posicion1 = random.randint(0, len(ruleta) - 1)      # número al azar entre 0 y el tamaño de la ruleta - 1
    padre1 = poblacion[ruleta[posicion1]]      

    posicion2 = random.randint(0, len(ruleta) - 1)
    padre2 = poblacion[ruleta[posicion2] ]   

    return padre1, padre2


def crossover1punto(padre1: list[int], padre2: list[int]) -> tuple[list[int], list[int]]:
    if random.random() <= PROB_CROSSOVER:
        
        punto = random.randint(1, NUM_BITS - 1)
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

def estadisticas(poblacion, lista_fitness):
    valores = [funcion_objetivo(ind) for ind in poblacion]
    maximo   = max(valores)
    minimo   = min(valores)
    promedio_f = sum(lista_fitness) / len(lista_fitness)
    promedio   = sum(valores) / len(valores)
    
    # Desviación estándar: σ = sqrt(Σ(fi - f̄)² / N)
    varianza = sum((f - promedio_f) ** 2 for f in lista_fitness) / len(poblacion)
    desv_std = varianza ** 0.5

    idx_max = valores.index(maximo)

    return {
        "maximo":    maximo,
        "minimo":    minimo,
        "promedio":  promedio,
        "desv_std":  desv_std,
        "cromosoma": poblacion[idx_max]
    }

def graficar_historial(historial):
    ciclos = list(range(0, len(historial)))
    maximos = [h["maximo"] for h in historial]
    minimos = [h["minimo"] for h in historial]
    promedios = [h["promedio"] for h in historial]

    plt.figure(figsize=(10, 5))
    plt.plot(  ciclos, maximos,   label="Máximo",   color="steelblue",  linewidth=2)
    plt.plot(  ciclos, promedios, label="Promedio", color="seagreen",   linewidth=2)
    plt.plot(  ciclos, minimos,   label="Mínimo",   color="tomato",     linewidth=2, linestyle="--")

    plt.title(f"Evolución del AG — {CICLOS} generaciones")
    plt.xlabel("Generación")
    plt.ylabel("F. objetivo")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"ag_{CICLOS}_generaciones.png", dpi=150)
    plt.show()

poblacion = [cromosoma_aleatorio() for _ in range(TAM_POBLACION)]
historial = []
t0 = time.perf_counter()
lista_fitness = fitness(poblacion)
historial.append(estadisticas(poblacion, lista_fitness))


for ciclo in range(CICLOS):
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
    lista_fitness = fitness(poblacion)
    historial.append(estadisticas(poblacion, lista_fitness))

tiempo_total = time.perf_counter() - t0

print(f"{'Ciclo':>6} | {'Máximo':>10} | {'Mínimo':>10} | {'Promedio':>10} | {'Desv.Std':>10} | Cromosoma del máximo")
print("─" * 105)

for i, stats in enumerate(historial, 0):
    print(f"{i:>6} | {stats['maximo']:>10.6f} | {stats['minimo']:>10.6f} | {stats['promedio']:>10.6f} | {stats['desv_std']:>10.6f} | {stats['cromosoma']}")

print(f"\nTiempo total de ejecución: {tiempo_total:.6f} segundos")
# Mejor solución global
mejor = max(historial, key=lambda s: s["maximo"])
print(f"\n{'═' * 90}")
print(f"MEJOR SOLUCIÓN GLOBAL")
print(f"  Cromosoma : {mejor['cromosoma']}")
print(f"  X         : {bits_a_dec(mejor['cromosoma'])}")
print(f"  F.Obj     : {mejor['maximo']:.6f}")

graficar_historial(historial)