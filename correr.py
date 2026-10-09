# Corre todo el proyecto con un solo comando: python correr.py
import os         # para movernos a la carpeta del proyecto (viene con Python)

# Nos movemos a la carpeta donde está este archivo. Así "salida/" siempre se crea
# aquí, aunque corras el programa desde otra carpeta o con el botón de VS Code.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import comparar   # nuestro archivo comparar.py
import generador  # nuestro archivo generador.py

linea = "=" * 60

print(linea)
print("   NÚMEROS AL AZAR USANDO LA CÁMARA")
print(linea)

print("\n[1/3] PRIMERA VEZ: la cámara toma fotos y saca 160,000 números")
segundos1 = generador.generar("corrida1.txt")

print("\n[2/3] SEGUNDA VEZ: se repite todo con fotos nuevas")
segundos2 = generador.generar("corrida2.txt")

print("\n[3/3] ¿Salieron los mismos números las dos veces?")
porcentaje = comparar.comparar()

print("\n" + linea)
print("   RESUMEN")
print(linea)
print("  Tiempo primera vez:    ", segundos1, "segundos")
print("  Tiempo segunda vez:    ", segundos2, "segundos")
print("  Números iguales:        " + str(porcentaje) + "%   (lo normal: cerca de 0.4%)")

print(linea)