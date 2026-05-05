import random
import math

# ─────────────────────────────────────────
#  PARÁMETROS DEL PROBLEMA
# ─────────────────────────────────────────
NUM_BITS       = 30                  # Longitud del cromosoma
COEF           = 2**NUM_BITS - 1     # 2^30 - 1
DOMINIO_MAX    = 2**NUM_BITS - 1     # [0, 2^30 - 1]
TAM_POBLACION  = 10
CICLOS         = 20
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
            print (f"Mutación en bit {i} del cromosoma {cromosoma}")
            print (f"Bit original: {cromosoma[i]}")
            print (f"Bit mutado: {1 - cromosoma[i]}")
            cromosoma[i] = 1 - cromosoma[i]
    return cromosoma


poblacion = [individuo_aleatorio() for _ in range(TAM_POBLACION)]
lista_fitness = fitness(poblacion)
 

print ("Población inicial:" )
for i, (ind, fit) in enumerate(zip(poblacion, lista_fitness)):
    print(f"{i}: {ind} - Fitness: {fit}")

padre1, padre2 = ruleta(poblacion, lista_fitness)
hijo1, hijo2, punto = crossover1punto(padre1, padre2)

hijo1mutado = mutacion(hijo1)
hijo2mutado = mutacion(hijo2)



print(f"Padre 1: {padre1} - F.Obj: {funcion_objetivo(padre1):.4f}")
print(f"Padre 2: {padre2} - F.Obj: {funcion_objetivo(padre2):.4f}")
print(f"Hijo 1: {hijo1} - F.Obj: {funcion_objetivo(hijo1):.4f}")
print(f"Hijo 2: {hijo2} - F.Obj: {funcion_objetivo(hijo2):.4f}")
print(f"Punto de cruce: {punto}")
print(f"Hijo 1 mutado: {hijo1mutado} - F.Obj: {funcion_objetivo(hijo1mutado):.4f}")
print(f"Hijo 2 mutado: {hijo2mutado} - F.Obj: {funcion_objetivo(hijo2mutado):.4f}")

if hijo1mutado != hijo1:
    print(f"Hijo 1 mutado. F.Obj original: {funcion_objetivo(hijo1):.4f} → mutado: {funcion_objetivo(hijo1mutado):.4f}")
if hijo2mutado != hijo2:
    print(f"Hijo 2 mutado. F.Obj original: {funcion_objetivo(hijo2):.4f} → mutado: {funcion_objetivo(hijo2mutado):.4f}")

