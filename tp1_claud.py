import random
import math

# ─────────────────────────────────────────
#  PARÁMETROS DEL PROBLEMA
# ─────────────────────────────────────────
NUM_BITS       = 30                  # Longitud del cromosoma
COEF           = 2**NUM_BITS - 1     # 2^30 - 1
DOMINIO_MAX    = 2**NUM_BITS - 1     # [0, 2^30 - 1]

# ─────────────────────────────────────────
#  PARÁMETROS DEL ALGORITMO GENÉTICO
# ─────────────────────────────────────────
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


# ─────────────────────────────────────────
#  CODIFICACIÓN / DECODIFICACIÓN
# ─────────────────────────────────────────
def decodificar(cromosoma: list[int]) -> int:
    """Convierte lista de bits [b29, b28, ..., b0] a entero."""
    return int("".join(str(b) for b in cromosoma), 2)


def individuo_aleatorio() -> list[int]:
    """Genera un cromosoma binario aleatorio de NUM_BITS bits."""
    return [random.randint(0, 1) for _ in range(NUM_BITS)]


# ─────────────────────────────────────────
#  SELECCIÓN: RULETA
# ─────────────────────────────────────────
def seleccion_ruleta(poblacion: list, aptitudes: list[float]) -> list[int]:
    """
    Selecciona un individuo mediante el método de la ruleta.
    La probabilidad de selección es proporcional al fitness.
    """
    total = sum(aptitudes)
    if total == 0:
        return random.choice(poblacion)

    r = random.uniform(0, total)
    acumulado = 0
    for individuo, apt in zip(poblacion, aptitudes):
        acumulado += apt
        if acumulado >= r:
            return individuo[:]
    return poblacion[-1][:]  # fallback


# ─────────────────────────────────────────
#  CROSSOVER: 1 PUNTO
# ─────────────────────────────────────────
def crossover_1punto(padre1: list[int], padre2: list[int]) -> tuple[list[int], list[int]]:
    """
    Cruza dos padres en un punto aleatorio.
    Solo se aplica con probabilidad PROB_CROSSOVER.
    """
    if random.random() <= PROB_CROSSOVER:
        punto = random.randint(1, NUM_BITS - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2
    else:
        return padre1[:], padre2[:]


# ─────────────────────────────────────────
#  MUTACIÓN: INVERSIÓN DE BIT
# ─────────────────────────────────────────
def mutacion_invertida(cromosoma: list[int]) -> list[int]:
    """
    Recorre cada bit y lo invierte con probabilidad PROB_MUTACION.
    """
    return [1 - bit if random.random() <= PROB_MUTACION else bit
            for bit in cromosoma]


# ─────────────────────────────────────────
#  ALGORITMO GENÉTICO CANÓNICO
# ─────────────────────────────────────────
def algoritmo_genetico():
    # --- Población inicial aleatoria ---
    poblacion = [individuo_aleatorio() for _ in range(TAM_POBLACION)]

    print("=" * 60)
    print("  ALGORITMO GENÉTICO CANÓNICO")
    print(f"  f(x) = (x / {COEF})^2   dominio [0, {DOMINIO_MAX}]")
    print("=" * 60)

    mejor_global = None
    mejor_fitness_global = -1

    for ciclo in range(1, CICLOS + 1):
        # --- Evaluación ---
        aptitudes = [fitness(ind) for ind in poblacion]

        # --- Mejor de esta generación ---
        idx_mejor = aptitudes.index(max(aptitudes))
        mejor_gen  = poblacion[idx_mejor]
        fit_mejor  = aptitudes[idx_mejor]
        x_mejor    = decodificar(mejor_gen)

        if fit_mejor > mejor_fitness_global:
            mejor_fitness_global = fit_mejor
            mejor_global = mejor_gen[:]

        print(f"Ciclo {ciclo:02d} | Mejor x = {x_mejor:>10} | "
              f"f(x) = {fit_mejor:.6f} | "
              f"Cromosoma: {''.join(str(b) for b in mejor_gen)}")

        # --- Nueva generación ---
        nueva_poblacion = []

        while len(nueva_poblacion) < TAM_POBLACION:
            # Selección por ruleta
            padre1 = seleccion_ruleta(poblacion, aptitudes)
            padre2 = seleccion_ruleta(poblacion, aptitudes)

            # Crossover de 1 punto
            hijo1, hijo2 = crossover_1punto(padre1, padre2)

            # Mutación invertida
            hijo1 = mutacion_invertida(hijo1)
            hijo2 = mutacion_invertida(hijo2)

            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < TAM_POBLACION:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

    # --- Resultado final ---
    print("=" * 60)
    x_final = decodificar(mejor_global)
    print(f"  MEJOR SOLUCIÓN ENCONTRADA")
    print(f"  x           = {x_final}")
    print(f"  f(x)        = {mejor_fitness_global:.8f}")
    print(f"  Cromosoma   = {''.join(str(b) for b in mejor_global)}")
    print(f"  Óptimo real = x = {DOMINIO_MAX}  →  f(x) = 1.0")
    print("=" * 60)

    return mejor_global, mejor_fitness_global


# ─────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────
if __name__ == "__main__":
    random.seed(42)   # Semilla para reproducibilidad (podés quitarla)
    algoritmo_genetico()