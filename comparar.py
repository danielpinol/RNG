# Compara dos corridas del generador para demostrar que no dan lo mismo.


def leer(ruta):
    numeros = []
    with open(ruta) as archivo:
        for linea in archivo:
            numeros.append(int(linea))
    return numeros

def comparar():
    corrida1 = leer("salida/corrida1.txt")
    corrida2 = leer("salida/corrida2.txt")

    # Contamos en cuántas posiciones las dos corridas tienen el mismo número
    iguales = 0
    for i in range(len(corrida1)):
        if corrida1[i] == corrida2[i]:
            iguales = iguales + 1

    # Por puro azar deberían coincidir alrededor de 1/256 = 0.4%.
    # Si fueran la misma secuencia, coincidirían el 100%.
    porcentaje = round(iguales / len(corrida1) * 100, 2)
    print("  Números iguales en la misma posición:", iguales, "de", len(corrida1), "(" + str(porcentaje) + "%)")
    print("  Lo normal por casualidad:             cerca de 0.4%")
    print("  Si salieran los mismos números:       sería 100%")
    if porcentaje < 1:
        print("  Resultado:                            las dos veces salieron números DIFERENTES")
    else:
        print("  Resultado:                            las dos veces salieron números muy parecidos")
    return porcentaje
