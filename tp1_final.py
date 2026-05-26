import random
import time
import matplotlib.pyplot as plt
from openpyxl import Workbook

NUM_BITS       = 30
COEF           = 2**NUM_BITS - 1
TAM_POBLACION  = 10
PROB_CROSSOVER = 0.75
PROB_MUTACION  = 0.05
T              = 4
ELITE_SIZE     = 2

<<<<<<< HEAD
METODO = "ruleta"
GENERACIONES = [20, 100, 200]
GENERACIONES_ELITISMO = [100]
=======
METODO = "elitismo" 
GENERACIONES = [20, 100, 200]  
GENERACIONES_ELITISMO = [100]  

COLOR_HEADER   = "1F4E79"
COLOR_GEN0     = "D6E4F0"
COLOR_RESUMEN  = "1F4E79"
COLOR_FILA_PAR = "EBF5FB"
FUENTE         = "Arial"

borde_fino = Border(
    left   = Side(style="thin", color="BFBFBF"),
    right  = Side(style="thin", color="BFBFBF"),
    top    = Side(style="thin", color="BFBFBF"),
    bottom = Side(style="thin", color="BFBFBF"),
)

def estilo_header(cell, color_fondo=COLOR_HEADER):
    cell.font      = Font(name=FUENTE, bold=True, color="FFFFFF", size=11)
    cell.fill      = PatternFill("solid", fgColor=color_fondo)
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border    = borde_fino

def estilo_dato(cell, fila_par=False, negrita=False, color_fondo=None):
    fondo          = color_fondo if color_fondo else (COLOR_FILA_PAR if fila_par else "FFFFFF")
    cell.font      = Font(name=FUENTE, bold=negrita, size=10)
    cell.fill      = PatternFill("solid", fgColor=fondo)
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border    = borde_fino
    cell.number_format = "0.0000000000"

def ancho_columnas(ws, anchos):
    for col, ancho in anchos.items():
        ws.column_dimensions[col].width = ancho
>>>>>>> 41fab48df4abd5b3778cec98122b3e550b0f2388


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

def torneo(poblacion, lista_fitness):
    def un_torneo():
        indices = random.sample(range(len(poblacion)), T)
        ganador = max(indices, key=lambda i: lista_fitness[i])
        return poblacion[ganador]
    return un_torneo(), un_torneo()

def seleccionar(poblacion, lista_fitness):
    if METODO == "ruleta":
        return ruleta(poblacion, lista_fitness)
    elif METODO == "torneo":
        return torneo(poblacion, lista_fitness)


def crossover1punto(padre1, padre2):
    if random.random() <= PROB_CROSSOVER:
        punto = random.randint(1, NUM_BITS - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2
    return padre1[:], padre2[:]

def mutacion(cromosoma):
    #copia la lista para no modificar el original
    cromosoma_mutado = cromosoma[:]

    if random.random() <= PROB_MUTACION:
        print(f"  → Cromosoma sin mutar: {cromosoma_mutado}")
        #el limite inferior no puede ser el ultimo bit porque sino no hay mutación
        limite_inferior = random.randint(0, NUM_BITS - 2)
        limite_superior = random.randint(limite_inferior + 1, NUM_BITS - 1)
        print("limite superor:", limite_superior)
        print("limite inferior:", limite_inferior)
        #el slincing no toma en cuenta el último indice, por eso se le suma 1
        # pisa lo que hay de i:j con lo mismo pero recorrido al revés 
        cromosoma_mutado[limite_inferior:limite_superior+1] = cromosoma_mutado[limite_inferior:limite_superior+1][::-1]
        print(f"  → Cromosoma  mutado: {cromosoma_mutado}")
    return cromosoma_mutado


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
            padre1, padre2 = seleccionar(poblacion, lista_fitness)
            hijo1, hijo2   = crossover1punto(padre1, padre2)
            hijo1          = mutacion(hijo1)
            hijo2          = mutacion(hijo2)
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < TAM_POBLACION:
                nueva_poblacion.append(hijo2)
        poblacion     = nueva_poblacion[:]
        lista_fitness = fitness(poblacion)
        historial.append(estadisticas(poblacion, lista_fitness))
    return historial, time.perf_counter() - t0

def correr_ag_elitismo(n_ciclos):
    poblacion     = [cromosoma_aleatorio() for _ in range(TAM_POBLACION)]
    lista_fitness = fitness(poblacion)
    historial     = [estadisticas(poblacion, lista_fitness)]
    t0 = time.perf_counter()
    for _ in range(n_ciclos):
        pares_ordenados = sorted(zip(lista_fitness, poblacion), reverse=True)
        elite = [ind[:] for _, ind in pares_ordenados[:ELITE_SIZE]]
        nueva_poblacion = elite[:]
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
    return historial, time.perf_counter() - t0


def graficar(historial, n_ciclos, metodo):
    ciclos    = list(range(len(historial)))
    maximos   = [h["maximo"]   for h in historial]
    minimos   = [h["minimo"]   for h in historial]
    promedios = [h["promedio"] for h in historial]

    plt.figure(figsize=(10, 5))
    plt.plot(ciclos, maximos,   label="Máximo",   color="steelblue", linewidth=2)
    plt.plot(ciclos, promedios, label="Promedio", color="seagreen",  linewidth=2)
    plt.plot(ciclos, minimos,   label="Mínimo",   color="tomato",    linewidth=2, linestyle="--")
    plt.title(f"AG {metodo.capitalize()} — {n_ciclos} generaciones")
    plt.xlabel("Generación")
    plt.ylabel("F. objetivo")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    nombre = f"ag_{metodo}_{n_ciclos}_generaciones.png"
    plt.savefig(nombre, dpi=150)
    plt.show()
    print(f"  → Gráfica guardada: {nombre}")


def exportar_excel(todos_resultados, tiempos, metodo):
    wb = Workbook()
    wb.remove(wb.active)

    encabezados = ["Generacion", "Maximo", "Minimo", "Promedio", "Desv. Std", "Cromosoma del maximo"]

    for n_ciclos, historial in todos_resultados.items():
        ws = wb.create_sheet(title=f"{n_ciclos} generaciones")
        ws.append(encabezados)
        for i, stats in enumerate(historial):
            ws.append([
                i,
                round(stats["maximo"], 10),
                round(stats["minimo"], 10),
                round(stats["promedio"], 10),
                round(stats["desv_std"], 10),
                str(stats["cromosoma"]),
            ])

    ws_res = wb.create_sheet(title="Resumen tiempos")
    ws_res.append(["Generaciones", "Metodo", "Tiempo (s)"])
    for n, t in tiempos.items():
        ws_res.append([int(n), metodo.capitalize(), round(t, 6)])

    wb.move_sheet("Resumen tiempos", offset=-len(wb.sheetnames) + 1)

    nombre = f"resultados_{metodo}.xlsx"
    wb.save(nombre)
    print(f"\n  → Excel guardado: {nombre}")


tiempos          = {}
todos_resultados = {}

gens = GENERACIONES_ELITISMO if METODO == "elitismo" else GENERACIONES

for n in gens:
    print(f"\n  Ejecutando {n} generaciones — Método: {METODO.capitalize()}...")
    if METODO == "elitismo":
        historial, tiempo = correr_ag_elitismo(n)
    else:
        historial, tiempo = correr_ag(n)
    tiempos[n]          = tiempo
    todos_resultados[n] = historial
    graficar(historial, n, METODO)
    print(f"  Tiempo de ejecución: {tiempo:.6f} s")

exportar_excel(todos_resultados, tiempos, METODO)
print(f"\n  ✓ Fin — Método: {METODO.capitalize()}")