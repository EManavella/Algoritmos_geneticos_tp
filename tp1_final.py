import random
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def generar_cromosoma(bits):
    # Generacion aleatoria de un cromosoma
    cromosoma = [random.randint(0, 1) for _ in range(bits)]
    cromosoma = ''.join(map(str, cromosoma))
    return cromosoma


def genera_poblacion_inicial(cant_cromo, bits):
    # Generacion de una poblacion inicial de cant_cromo individuos
    return [generar_cromosoma(bits) for i in range(cant_cromo)]


def calcula_obj(poblacion, coef):
    # Calcula el valor de la funcion objetivo para toda la poblacion
    return [((int(cromosoma, 2) / coef) ** 2) for cromosoma in poblacion]


def calcula_fitness(valores_objs, sumatoria):
    # Calcula el fitness para toda la poblacion
    return [i / sumatoria for i in valores_objs]


def busca_maximo(poblacion, coef):
    # Busca el valor maximo de la poblacion y el cromosoma correspondiente a dicho valor
    max = 0
    ganador = 0
    for cromo in poblacion:
        val = int(cromo, 2)
        if (((val / coef) ** 2) > max):
            ganador = cromo
            max = ((val / coef) ** 2)
    return ganador


def torneo(cromosomas, fit):
    # Realiza el metodo de seleccion por Torneo
    seleccionados = []
    tam = len(fit)
    for _ in range(tam):
        idA = random.randint(0, tam - 1)
        idB = random.randint(0, tam - 1)
        if (fit[idA] > fit[idB]):
            seleccionados.append(cromosomas[idA])  # Si el Fitness de A es mayor se elige A
        else:
            seleccionados.append(cromosomas[idB])  # Si el fitness de B es mayor o igual se elige B
    return seleccionados  # Se devuelven los cromosomas seleccionados para la cruza


def ruleta(cromosomas, fit, cant):
    # Realiza el metodo de seleccion por Ruleta
    seleccionados = []
    ruleta = []
    for i in range(len(fit)):
        # Se genera una ruleta donde la cantidad de espacios asignada a cada cromosoma es proporcional a su fitness
        val = max(int(fit[i] * 100), 1)  # A cada cromosoma le corresponde minimo 1 espacio
        for _ in range(val):
            ruleta.append(i)
        while (len(ruleta) < 100):
            ruleta.append(len(fit) - 1)  # Si quedaron espacios sin asignar se asignan a mano
    for _ in range(cant):
        salida = random.randint(0, 99)
        seleccionados.append(cromosomas[ruleta[salida]])  # Se eligen los cromosomas
    return seleccionados  # Se devuelven los cromosomas seleccionados para la cruza


def ruleta_elite(cromosomas, fit):
    # Realiza el metodo de seleccion por Elitismo y luego se llama al metodo de seleccion por Ruleta
    seleccionados = []
    tam = len(fit)
    elite = []
    for i in range(tam):
        elite.append([fit[i], i])
    elite.sort()  # Se ordenan los cromosomas de acuerdo a su fitness
    idA = elite[tam - 1][1]  # Se elige el cromosoma con el mayor valor de fitness
    idB = elite[tam - 2][1]  # Se elige el cromosoma con el segundo mayor valor de fitness
    seleccionados.append(cromosomas[idA])
    seleccionados.append(cromosomas[idB])
    seleccion_ruleta = ruleta(cromosomas, fit, tam - 2)  # Se realiza el metodo de Ruleta descontando los 2 individuos elegidos por elitismo
    return seleccionados + seleccion_ruleta  # Se devuelven los cromosomas seleccionados para la cruza


def cruza(seleccionados, prob_cross):
    # Se realiza la cruza de los cromosomas seleccionados
    descendencia = []
    for i in range(0, len(seleccionados) - 1, 2):
        prob = random.random()
        if (prob <= prob_cross):  # Si el numero generado es menor o igual a la probabilidad de cruza la misma se realiza
            corte = random.randint(0, 29)  # Se genera de forma aleatoria el punto de corte
            padre1 = seleccionados[i]
            padre2 = seleccionados[i + 1]
            hijo1 = padre1[:corte] + padre2[corte:]  # Se genera el primer hijo
            hijo2 = padre2[:corte] + padre1[corte:]  # Se genera el segundo hijo
            descendencia.append(hijo1)
            descendencia.append(hijo2)
        else:
            descendencia.append(seleccionados[i])      # Sin cruza, se guarda el padre 1
            descendencia.append(seleccionados[i + 1])  # Sin cruza, se guarda el padre 2
    return descendencia  # Se devuelve la descendencia generada


def mutacion(hijos, prob_mut):
    # Se realiza la mutacion de los cromosomas
    hijos_nuevos = []
    for hijo in hijos:
        hijo_nuevo = ""
        prob = random.random()
        if (prob <= prob_mut):  # Si el numero generado es menor o igual a la probabilidad de mutacion la misma se realiza
            lim_inf = random.randint(0, 29)  # Se genera el limite inferior
            lim_sup = random.randint(0, 29)  # Se genera el limite superior
            if (lim_inf > lim_sup):
                lim_inf, lim_sup = lim_sup, lim_inf  # Se intercambian los valores si el limite inferior es mayor al superior
            segmento_inv = hijo[lim_inf:lim_sup + 1][::-1]  # Se invierte el segmento generado
            hijo_nuevo = hijo[:lim_inf] + segmento_inv + hijo[lim_sup + 1:]  # Se genera el individuo mutado
            hijos_nuevos.append(hijo_nuevo)
        else:
            hijos_nuevos.append(hijo)  # Sin mutacion, se guarda el individuo sin cambios
    return hijos_nuevos  # Se devuelve la poblacion mutada


def hacer_grafica(maximos, minimos, promedios, cant_individuos, cant_corridas):
    # Se generan las graficas de valor maximo, valor minimo y valor promedio
    numero_corrida = [i + 1 for i in range(cant_corridas)]
    for i in range(cant_corridas):
        promedios[i] = promedios[i] / cant_individuos  # Se calculan los promedios

    plt.figure(figsize=(25, 10))
    plt.plot(numero_corrida, maximos, linestyle='-', label='Valor Maximo')
    plt.title('Maximo por corrida')
    plt.xlabel('Numero Corrida')
    plt.ylabel('Valor Maximo')
    plt.legend()
    plt.show()

    plt.plot(numero_corrida, minimos, linestyle='-', label='Valor Minimo')
    plt.title('Minimo por corrida')
    plt.xlabel('Numero Corrida')
    plt.ylabel('Valor Minimo')
    plt.legend()
    plt.show()

    plt.plot(numero_corrida, promedios, linestyle='-', label='Valor Promedio')
    plt.title('Promedio por corrida')
    plt.xlabel('Numero Corrida')
    plt.ylabel('Valor Promedio')
    plt.legend()
    plt.show()


def hacer_tabla(cromMax, maximos, minimos, promedios, cant_individuos, cant_corridas):
    # Se genera un archivo excel con los datos generados
    for i in range(cant_corridas):
        promedios[i] = promedios[i] / cant_individuos  # Se calculan los promedios
    df = pd.DataFrame(
        list(zip(cromMax, maximos, minimos, promedios)),
        columns=['Cromosoma Maximo', 'Valor Maximo', 'Valor Minimo', 'Promedio']
    )
    wb = Workbook()
    ws = wb.active
    cont = 0
    for r in dataframe_to_rows(df, index=True, header=True):
        if (cont == 0):
            r[0] = "Generacion"  # Se indica el nombre de la primer columna
        if (cont >= 2):
            r[0] = r[0] + 1  # Se actualiza el indice para que el mismo sea 1-index
        ws.append(r)
        cont += 1
    for cell in ws['A'] + ws[1]:
        cell.style = 'Pandas'
    wb.save("pandas_openpyxl.xlsx")  # Se guarda el archivo excel


def main():
    # Variables fijas
    prob_cross = 0.75
    prob_mut = 0.08
    cant_individuos = 10
    op = 0
    generaciones = 20
    coef = (2 ** 30) - 1
    cant_bits = 30
    max_por_ciclo = []
    valormin_por_ciclo = []
    valormax_por_ciclo = []
    sumas_obj_por_ciclo = []

    poblacion = genera_poblacion_inicial(cant_individuos, cant_bits)  # Se genera la poblacion inicial

    for i in range(generaciones):
        valores_func_obj = calcula_obj(poblacion, coef)
        valormin_por_ciclo.append(min(valores_func_obj))
        valormax_por_ciclo.append(max(valores_func_obj))
        sumas_obj_por_ciclo.append(sum(valores_func_obj))
        max_por_ciclo.append(busca_maximo(poblacion, coef))

        sumatoria = sum(valores_func_obj)
        fitness = calcula_fitness(valores_func_obj, sumatoria)

        if (op == 0):
            seleccionados = ruleta(poblacion, fitness, 10)
        elif (op == 1):
            seleccionados = torneo(poblacion, fitness)
        elif (op == 2):
            seleccionados = ruleta_elite(poblacion, fitness)
        else:
            print("El metodo de seleccion elegido no es valido")
            print("Opciones:")
            print("-0: Ruleta")
            print("-1: Torneo")
            print("-2: Ruleta + Elitismo")
            sys.exit()

        hijos = cruza(seleccionados, prob_cross)
        poblacion = mutacion(hijos, prob_mut)

    for i in range(generaciones):
        print("=" * 70)
        print(f"Valor maximo en poblacion {i}: {valormax_por_ciclo[i]} con el cromosoma {max_por_ciclo[i]}")
        print(f"Valor minimo en poblacion {i}: {valormin_por_ciclo[i]}")
        print(f"Promedio de poblacion {i}: {sumas_obj_por_ciclo[i] / cant_individuos}")
        print("=" * 70)

    hacer_tabla(max_por_ciclo, valormax_por_ciclo, valormin_por_ciclo, sumas_obj_por_ciclo, cant_individuos, generaciones)
    hacer_grafica(valormax_por_ciclo, valormin_por_ciclo, sumas_obj_por_ciclo, cant_individuos, generaciones)


main()