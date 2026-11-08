import sys
from pathlib import Path

from transcriptor.motores.tesseract import MotorTesseract


def elegir_imagen():
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return Path("datos/ja-p1.jpg")

def mostrar_resultado(resultado):
    print("Texto reconocido:")
    print(resultado.texto)
    print()
    print("Posicion de cada linea:")
    for linea in resultado.lineas:
        print(f"x={linea.x:<4} y={linea.y:<4} {linea.texto}")
    print()
    print(f"Tiempo: {resultado.segundos:.2f} segundos")


def main():
    ruta = elegir_imagen()
    if not ruta.exists():
        print(f"No existe la imagen: {ruta}")
        return
    motor = MotorTesseract()
    resultado = motor.reconocer(ruta)
    mostrar_resultado(resultado)


if __name__ == "__main__":
    main()