import sys
from pathlib import Path
from PIL import Image
from transcriptor import servicio
from transcriptor.preprocesamiento import limpiar


def elegir_imagen():
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return Path("datos/ja-p1.jpg")


def elegir_motor():
    if len(sys.argv) > 2:
        return sys.argv[2]
    return "paddleocr"


def guardar_limpia(ruta):
    destino = ruta.with_name(ruta.stem + "-limpia.png")
    limpiar(Image.open(ruta)).save(destino)
    print(f"Imagen limpia guardada en: {destino}")
    print()


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
    guardar_limpia(ruta)
    resultado = servicio.reconocer(ruta, elegir_motor())
    mostrar_resultado(resultado)


if __name__ == "__main__":
    main()
