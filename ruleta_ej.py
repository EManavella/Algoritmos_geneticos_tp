import random


def seleccion_ruletamanual(poblacion, fitnesses):



    # ── PASO 1: calcular el total del fitness ──────────────────────
    total = sum(fitnesses)

    # ── PASO 2: calcular cuántas casillas le toca a cada cromosoma ─
    # Si el cromosoma i tiene fitness 0.5 y el total es 1.0,
    # le tocan round(0.5/1.0 * 100) = 50 casillas
    casillas = []
    for f in fitnesses:
        cantidad = round((f / total) * 100)
        casillas.append(cantidad)

    # ── PASO 3: construir el array de 100 posiciones ───────────────
    # Cada posición guarda el ÍNDICE del cromosoma (0 al 9)
    # Ejemplo: [0,0,0,...,1,1,...,9,9,9]
    ruleta = []
    for indice, cantidad in enumerate(casillas):
        for _ in range(cantidad):
            ruleta.append(indice)   # repetimos el índice 'cantidad' veces

    # ajuste por redondeo (para que queden exactamente 100)
    while len(ruleta) < 100:
        ruleta.append(0)
    while len(ruleta) > 100:
        ruleta.pop()

    # ── PASO 4: elegir padre 1 ─────────────────────────────────────
    posicion1 = random.randint(0, 99)      # número al azar entre 0 y 99
    indice_padre1 = ruleta[posicion1]      # qué cromosoma hay en esa posición
    padre1 = poblacion[indice_padre1]      # el cromosoma en sí

    # ── PASO 5: elegir padre 2 (igual que el padre 1) ─────────────
    posicion2 = random.randint(0, 99)
    indice_padre2 = ruleta[posicion2]
    padre2 = poblacion[indice_padre2]

    return padre1, padre2


def seleccion_ruleta_manual(poblacion, fitnesses):

    # PASO 1: normalizar los fitness para que sumen exactamente 1
    total = sum(fitnesses)
    fitnesses_norm = [f / total for f in fitnesses]
    # fitnesses_norm = [0.155, 0.048, 0.122, ...]  → suman 1.0

    # PASO 2: calcular cuántas casillas le toca a cada cromosoma
    # multiplicamos por 100 y redondeamos
    # por redondeo el array puede quedar en 99, 100 o 101 — está bien
    casillas = []
    for f in fitnesses_norm:
        cantidad = round(f * 100)
        casillas.append(cantidad)

    # PASO 3: construir el array con los índices repetidos
    ruleta = []
    for indice, cantidad in enumerate(casillas):
        for _ in range(cantidad):
            ruleta.append(indice)
    # el array puede tener 99, 100 o 101 posiciones — no importa

    # PASO 4: elegir padre 1
    posicion1 = random.randint(0, len(ruleta) - 1)  # al azar dentro del tamaño real
    padre1 = poblacion[ruleta[posicion1]]

    # PASO 5: elegir padre 2
    posicion2 = random.randint(0, len(ruleta) - 1)
    padre2 = poblacion[ruleta[posicion2]]

    return padre1, padre2