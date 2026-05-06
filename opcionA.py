import random
import time
import matplotlib.pyplot as plt


NUM_BITS       = 30
COEF           = 2**NUM_BITS - 1
TAM_POBLACION  = 10
PROB_CROSSOVER = 0.75
PROB_MUTACION  = 0.05

GENERACIONES = [20, 100, 200]   


def bits_a_dec(cromosoma):
    return int("".join(str(b) for b in cromosoma), 2)

def cromosoma_aleatorio():
    return [random.randint(0, 1) for _ in range(NUM_BITS)]

def funcion_objetivo(cromosoma):
    x = bits_a_dec(cromosoma)
    return (x / COEF) ** 2

def fitness(poblacion):
    fobj  = [funcion_objetivo(ind) for ind in poblacion]
    total = sum(fobj)
    return [f / total for f in fobj]


def ruleta(poblacion, lista_fitness):
    casillas = []
    for f in lista_fitness:
        cantidad = round(f * 100)
        if cantidad == 0:
            cantidad = 1
        casillas.append(cantidad)

    array_ruleta = []
    for indice, cantidad in enumerate(casillas):
        for _ in range(cantidad):
            array_ruleta.append(indice)

    padre1 = poblacion[array_ruleta[random.randint(0, len(array_ruleta) - 1)]]
    padre2 = poblacion[array_ruleta[random.randint(0, len(array_ruleta) - 1)]]
    return padre1, padre2

def crossover1punto(padre1, padre2):
    if random.random() <= PROB_CROSSOVER:
        punto = random.randint(1, NUM_BITS - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2
    return padre1[:], padre2[:]

def mutacion(cromosoma):
    cromosoma = cromosoma[:]
    for i in range(len(cromosoma)):
        if random.random() <= PROB_MUTACION:
            cromosoma[i] = 1 - cromosoma[i]
    return cromosoma


def estadisticas(poblacion, lista_fitness):
    valores    = [funcion_objetivo(ind) for ind in poblacion]
    maximo     = max(valores)
    minimo     = min(valores)
    promedio   = sum(valores) / len(valores)
    promedio_f = sum(lista_fitness) / len(lista_fitness)
    varianza   = sum((f - promedio_f) ** 2 for f in lista_fitness) / len(lista_fitness)
    desv_std   = varianza ** 0.5
    idx_max    = valores.index(maximo)
    return {
        "maximo":    maximo,
        "minimo":    minimo,
        "promedio":  promedio,
        "desv_std":  desv_std,
        "cromosoma": poblacion[idx_max]
    }


def correr_ag(n_ciclos):
    poblacion     = [cromosoma_aleatorio() for _ in range(TAM_POBLACION)]
    lista_fitness = fitness(poblacion)
    historial     = [estadisticas(poblacion, lista_fitness)]   

    t0 = time.perf_counter()                  

    for _ in range(n_ciclos):
        nueva_poblacion = []
        while len(nueva_poblacion) < TAM_POBLACION:
            padre1, padre2 = ruleta(poblacion, lista_fitness)
            hijo1, hijo2   = crossover1punto(padre1, padre2)
            hijo1          = mutacion(hijo1)
            hijo2          = mutacion(hijo2)
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < TAM_POBLACION:
                nueva_poblacion.append(hijo2)

        poblacion     = nueva_poblacion[:]
        lista_fitness = fitness(poblacion)
        historial.append(estadisticas(poblacion, lista_fitness))

    tiempo = time.perf_counter() - t0

    return historial, tiempo


def imprimir_tabla(historial, n_ciclos):
    ancho = 64
    print(f"\n{'═' * ancho}")
    print(f"  TABLA — {n_ciclos} generaciones  |  Método: Ruleta")
    print(f"{'═' * ancho}")
    print(f"  {'Gen':>5} | {'Máximo':>10} | {'Mínimo':>10} | {'Promedio':>10} | {'Desv.Std':>10}")
    print(f"  {'─' * 58}")
    for i, stats in enumerate(historial):
        print(f"  {i:>5} | {stats['maximo']:>10.6f} | {stats['minimo']:>10.6f} | "
              f"{stats['promedio']:>10.6f} | {stats['desv_std']:>10.6f}")
    print(f"{'═' * ancho}")
    mejor = max(historial, key=lambda s: s["maximo"])
    print(f"  Mejor F.Obj : {mejor['maximo']:.6f}")
    print(f"  Cromosoma   : {mejor['cromosoma']}")
    print(f"  X           : {bits_a_dec(mejor['cromosoma'])}")


def graficar(historial, n_ciclos):
    ciclos    = list(range(len(historial)))
    maximos   = [h["maximo"]   for h in historial]
    minimos   = [h["minimo"]   for h in historial]
    promedios = [h["promedio"] for h in historial]

    plt.figure(figsize=(10, 5))
    plt.plot(ciclos, maximos,   label="Máximo",   color="steelblue", linewidth=2)
    plt.plot(ciclos, promedios, label="Promedio", color="seagreen",  linewidth=2)
    plt.plot(ciclos, minimos,   label="Mínimo",   color="tomato",    linewidth=2, linestyle="--")
    plt.title(f"AG Ruleta — {n_ciclos} generaciones")
    plt.xlabel("Generación")
    plt.ylabel("F. objetivo")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    nombre = f"ag_ruleta_{n_ciclos}_generaciones.png"
    plt.savefig(nombre, dpi=150)
    plt.show()
    print(f"  → Gráfica guardada: {nombre}")


tiempos = {}

for n in GENERACIONES:
    print(f"\n{'#'*64}")
    print(f"  AG con {n} generaciones — Método: Ruleta")
    print(f"{'#'*64}")

    historial, tiempo = correr_ag(n)
    tiempos[n] = tiempo

    imprimir_tabla(historial, n)
    graficar(historial, n)
    print(f"  Tiempo de ejecución: {tiempo:.6f} s")

# tabla final
print(f"\n{'═' * 42}")
print(f"  TABLA RESUMEN DE TIEMPOS")
print(f"{'═' * 42}")
print(f"  {'Generaciones':>12} | {'Método':>10} | {'Tiempo':>10}")
print(f"  {'─' * 38}")
for n in GENERACIONES:
    print(f"  {n:>12} | {'Ruleta':>10} | {tiempos[n]:>8.6f} s")
print(f"{'═' * 42}")
print("\n  Fin de la opción A")