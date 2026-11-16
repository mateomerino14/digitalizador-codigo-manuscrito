import csv
from pathlib import Path

from evaluador.metricas import cer, wer
from transcriptor import servicio

PILOTO = Path("datos/piloto")
RESULTADOS = PILOTO / "resultados.csv"
MOTORES = ["tesseract", "paddleocr", "trocr"]
COLUMNAS = ["imagen", "lenguaje", "motor", "limpieza", "cer", "wer", "segundos"]


def normalizar(texto):
    lineas = []
    for linea in texto.splitlines():
        linea = linea.strip()
        if linea:
            lineas.append(linea)
    return "\n".join(lineas)


def imagenes_piloto():
    imagenes = []
    for lenguaje in ["python", "java"]:
        for ruta in sorted((PILOTO / lenguaje).glob("*.jpg")):
            if ruta.with_suffix(".txt").exists():
                imagenes.append((ruta, lenguaje))
    return imagenes


def referencia_de(ruta):
    texto = ruta.with_suffix(".txt").read_text(encoding="utf-8")
    return normalizar(texto)


def evaluar_motores(imagenes):
    filas = []
    for ruta, lenguaje in imagenes:
        referencia = referencia_de(ruta)
        for motor in MOTORES:
            for limpieza in [False, True]:
                print(f"{ruta.name} {motor} limpieza={limpieza}")
                try:
                    resultado = servicio.reconocer(ruta, motor, limpieza)
                except Exception as error:
                    print(f"  error: {error}")
                    continue
                texto = normalizar(resultado.texto)
                filas.append(
                    {
                        "imagen": ruta.stem,
                        "lenguaje": lenguaje,
                        "motor": motor,
                        "limpieza": "si" if limpieza else "no",
                        "cer": round(cer(referencia, texto), 4),
                        "wer": round(wer(referencia, texto), 4),
                        "segundos": round(resultado.segundos, 2),
                    }
                )
    return filas


def evaluar_nube():
    filas = []
    archivo_nube = PILOTO / "python" / "nube.csv"
    if not archivo_nube.exists():
        return filas
    with open(archivo_nube, encoding="utf-8") as archivo:
        for dato in csv.DictReader(archivo):
            referencia = referencia_de(PILOTO / "python" / (dato["imagen"] + ".jpg"))
            for motor in ["google", "azure"]:
                texto = normalizar(dato[motor])
                filas.append(
                    {
                        "imagen": dato["imagen"],
                        "lenguaje": "python",
                        "motor": motor,
                        "limpieza": "dataset",
                        "cer": round(cer(referencia, texto), 4),
                        "wer": round(wer(referencia, texto), 4),
                        "segundos": 0,
                    }
                )
    return filas


def guardar(filas):
    with open(RESULTADOS, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"Resultados guardados en: {RESULTADOS}")


def promedio(filas, columna):
    suma = 0
    for fila in filas:
        suma += fila[columna]
    return suma / len(filas)


def mostrar_resumen(filas):
    grupos = {}
    for fila in filas:
        grupo = f"{fila['lenguaje']:<8} {fila['motor']:<10} {fila['limpieza']:<8}"
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append(fila)
    print()
    print("lenguaje motor      limpieza    cer    wer    seg")
    for grupo in sorted(grupos):
        cer_medio = promedio(grupos[grupo], "cer")
        wer_medio = promedio(grupos[grupo], "wer")
        seg_medio = promedio(grupos[grupo], "segundos")
        print(f"{grupo} {cer_medio:>6.3f} {wer_medio:>6.3f} {seg_medio:>6.1f}")


def main():
    imagenes = imagenes_piloto()
    print(f"Imagenes encontradas: {len(imagenes)}")
    filas = evaluar_motores(imagenes) + evaluar_nube()
    guardar(filas)
    mostrar_resumen(filas)


if __name__ == "__main__":
    main()
