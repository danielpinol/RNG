import hashlib  # SHA-256, para mezclar el ruido (viene con Python)
import os       # os.urandom y crear la carpeta salida (viene con Python)
import sys      # saber si es Mac o Windows y cerrar el programa (viene con Python)
import time     # medir cuánto tarda (viene con Python)

import cv2      # abrir la cámara y tomar fotos (se instala: opencv-python)

CANTIDAD = 160000


def abrir_camara():
    # Mac y Windows abren la cámara de forma distinta
    if sys.platform == "darwin":
        modo = cv2.CAP_AVFOUNDATION
    else:
        modo = cv2.CAP_DSHOW

    camara = cv2.VideoCapture(0, modo)
    if not camara.isOpened():
        print("  No se pudo abrir la cámara 0. Revisando las cámaras 0 a 4:")
        for numero in range(5):
            prueba = cv2.VideoCapture(numero, modo)
            print("    Cámara", numero, "funciona:", prueba.isOpened())
            prueba.release()
        print("  Cerrá Zoom/Teams y cambiá el 0 de VideoCapture por una que funcione.")
        sys.exit()
    return camara

def generar(nombre_archivo):
    inicio = time.time()  # medimos desde que se abre la cámara
    camara = abrir_camara()

    # Las primeras fotos salen mal mientras la cámara ajusta la luz
    for i in range(30):
        camara.read()

    # Dos fotos seguidas nunca son iguales, aunque la cámara esté tapada: eso es el ruido
    ok, foto1 = camara.read()
    ok, foto2 = camara.read()
    cambiaron = (foto1 != foto2).sum()  # cuenta cuántos valores son distintos
    ruido = round(cambiaron / foto1.size * 100, 1)

    numeros = []
    fotos_usadas = 0
    while len(numeros) < CANTIDAD:  # se toman fotos hasta que alcancen los números
        ok, foto = camara.read()
        if not ok:  # la cámara dejó de mandar fotos (se desconectó u otra app la agarró)
            print("  ERROR: la cámara dejó de mandar fotos. Revisá que esté conectada.")
            sys.exit()
        fotos_usadas = fotos_usadas + 1
        # El último bit de cada pixel (0 o 1) es el que más cambia por el ruido del sensor
        bits = (foto & 1).tobytes()
        for i in range(0, len(bits), 1024):  # pedazos de 1024 bits de ruido
            pedazo = bits[i:i + 1024]
            # os.urandom es la fuente aleatoria interna del sistema operativo.
            # Al pegarla a cada pedazo, dos pedazos iguales nunca dan el mismo resultado.
            mezcla = hashlib.sha256(pedazo + os.urandom(16)).digest()
            for numero in mezcla:  # SHA-256 da 32 bytes y cada byte es un número de 0 a 255
                numeros.append(numero)
    camara.release()
    numeros = numeros[:CANTIDAD]  # nos quedamos con 160,000 exactos
    segundos = round(time.time() - inicio, 2)

    os.makedirs("salida", exist_ok=True)
    with open("salida/" + nombre_archivo, "w") as archivo:
        for numero in numeros:
            archivo.write(str(numero) + "\n")

    total_fotos = 30 + 2 + fotos_usadas
    print("  La cámara tomó", total_fotos, "fotos:")
    print("     30 no se usaron (la cámara se estaba ajustando a la luz)")
    print("      2 se compararon: el " + str(ruido) + "% de los puntos cambió solo (eso es el ruido)")
    print("     ", fotos_usadas, "se usaron para sacar los números")
    if cambiaron == 0:  # si la cámara se traba, manda la misma foto repetida
        print("  OJO: las 2 fotos salieron idénticas, la cámara se trabó. Corré el programa otra vez.")
    print("  Resultado:            ", len(numeros), "números al azar")
    print("  Tardó:                ", segundos, "segundos")
    print("  Se guardaron en:       salida/" + nombre_archivo)
    return segundos