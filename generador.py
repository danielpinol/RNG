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