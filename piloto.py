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


def filas_guardadas():
    filas = []
    if not RESULTADOS.exists():
        return filas
    with open(RESULTADOS, encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            fila["cer"] = float(fila["cer"])
            fila["wer"] = float(fila["wer"])
            fila["segundos"] = float(fila["segundos"])
            filas.append(fila)
    return filas


def clave(imagen, motor, limpieza):
    return f"{imagen} {motor} {limpieza}"


def guardar(fila):
    nuevo = not RESULTADOS.exists()
    with open(RESULTADOS, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        if nuevo:
            escritor.writeheader()
        escritor.writerow(fila)


def evaluar_motores(imagenes, hechas):
    for ruta, lenguaje in imagenes:
        referencia = referencia_de(ruta)
        for motor in MOTORES:
            for limpieza in [False, True]:
                texto_limpieza = "si" if limpieza else "no"
                if clave(ruta.stem, motor, texto_limpieza) in hechas:
                    continue
                print(f"{ruta.name} {motor} limpieza={limpieza}")
                try:
                    resultado = servicio.reconocer(ruta, motor, limpieza)
                except Exception as error:
                    print(f"  error: {error}")
                    continue
                texto = normalizar(resultado.texto)
                guardar(
                    {
                        "imagen": ruta.stem,
                        "lenguaje": lenguaje,
                        "motor": motor,
                        "limpieza": texto_limpieza,
                        "cer": round(cer(referencia, texto), 4),
                        "wer": round(wer(referencia, texto), 4),
                        "segundos": round(resultado.segundos, 2),
                    }
                )


def evaluar_nube(hechas):
    archivo_nube = PILOTO / "python" / "nube.csv"
    if not archivo_nube.exists():
        return
    with open(archivo_nube, encoding="utf-8") as archivo:
        for dato in csv.DictReader(archivo):
            referencia = referencia_de(PILOTO / "python" / (dato["imagen"] + ".jpg"))
            for motor in ["google", "azure"]:
                if clave(dato["imagen"], motor, "dataset") in hechas:
                    continue
                texto = normalizar(dato[motor])
                guardar(
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
    hechas = set()
    for fila in filas_guardadas():
        hechas.add(clave(fila["imagen"], fila["motor"], fila["limpieza"]))
    evaluar_motores(imagenes, hechas)
    evaluar_nube(hechas)
    print(f"Resultados guardados en: {RESULTADOS}")
    mostrar_resumen(filas_guardadas())


if __name__ == "__main__":
    main()
