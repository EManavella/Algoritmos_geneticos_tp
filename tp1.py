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
def fitness(cromosoma: list[int]) -> float:
    """f(x) = (x / coef)^2   con x = valor decimal del cromosoma."""
    x = decodificar(cromosoma)
    return (x / COEF) ** 2

def decodificar(cromosoma: list[int]) -> int:
    """Convierte lista de bits ["0", "1", ..., "1"] a entero."""
    return int("".join(str(b) for b in cromosoma), 2)

def individuo_aleatorio() -> list[int]:
    return [random.randint(0, 1) for _ in range(NUM_BITS)]

def ruleta (poblacion: list, lista_fitness: list[float]) -> list[int]:
    sum_fitness = sum(lista_fitness)
    probabilidades = [fit / sum_fitness for fit in lista_fitness]
    return random.choices(poblacion, weights=probabilidades, k=2)

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
lista_fitness = [fitness(ind) for ind in poblacion]
 

#print ("Población inicial:" )
#for i, (ind, fit) in enumerate(zip(poblacion, lista_fitness)):
    # print(f"{i}: {ind} - Fitness: {fit}")

padre1, padre2 = ruleta(poblacion, lista_fitness)
hijo1, hijo2, punto = crossover1punto(padre1, padre2)

hijo1mutado = mutacion(hijo1)
hijo2mutado = mutacion(hijo2)



print (f"Padre 1: {padre1} - Fitness: {fitness(padre1)}")
print (f"Padre 2: {padre2} - Fitness: {fitness(padre2)}")
print (f"Hijo 1: {hijo1} - Fitness: {fitness(hijo1)}")
print (f"Hijo 2: {hijo2} - Fitness: {fitness(hijo2)}")
print (f"Punto de cruce: {punto}")
print (f"Hijo 1 mutado: {hijo1mutado} - Fitness: {fitness(hijo1mutado)}")
print (f"Hijo 2 mutado: {hijo2mutado} - Fitness: {fitness(hijo2mutado)}")
if hijo1mutado != hijo1:
    print (f"El hijo 1 ha sido mutado. Fitness original: {fitness(hijo1)}, Fitness mutado: {fitness(hijo1mutado)}")
if hijo2mutado != hijo2:
    print (f"El hijo 2 ha sido mutado. Fitness original: {fitness(hijo2)}, Fitness mutado: {fitness(hijo2mutado)}")

