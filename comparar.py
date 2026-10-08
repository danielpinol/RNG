# Compara dos corridas del generador para demostrar que no dan lo mismo.


def leer(ruta):
    numeros = []
    with open(ruta) as archivo:
        for linea in archivo:
            numeros.append(int(linea))
    return numeros