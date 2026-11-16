import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from transcriptor.preprocesamiento import limpiar
from transcriptor.segmentacion import segmentar_lineas

FIGURAS = Path("datos/figuras")

ETIQUETAS = {
    "es": {
        "x": "Fila de píxeles",
        "y": "Píxeles de tinta en la fila",
        "umbral": "10% de la fila más llena",
        "valle": "valle",
        "archivo": "tinta-por-fila.png",
    },
    "en": {
        "x": "Pixel row",
        "y": "Ink pixels in the row",
        "umbral": "10% of the fullest row",
        "valle": "valley",
        "archivo": "ink-per-row.png",
    },
}


def tinta_por_fila(ruta):
    imagen = limpiar(Image.open(ruta))
    tinta = np.asarray(imagen.convert("L")) < 128
    return tinta.sum(axis=1)


def primer_bloque(por_fila):
    arriba = None
    for y in range(len(por_fila)):
        if por_fila[y] >= 2 and arriba is None:
            arriba = y
        elif por_fila[y] < 2 and arriba is not None:
            return arriba, y
    return arriba, len(por_fila)


def guardar_grafico_tinta(ruta, idioma):
    etiquetas = ETIQUETAS[idioma]
    por_fila = tinta_por_fila(ruta)
    arriba, abajo = primer_bloque(por_fila)
    filas = list(range(arriba, abajo))
    valores = por_fila[arriba:abajo]
    umbral = valores.max() * 0.10
    con_texto = np.where(valores >= umbral)[0]
    primera = con_texto[0]
    ultima = con_texto[-1]
    colores = []
    for k in range(len(valores)):
        if primera < k < ultima and valores[k] < umbral:
            colores.append("#9a9a9a")
        else:
            colores.append("#3d5a80")
    figura, eje = plt.subplots(figsize=(8, 3.6), dpi=200)
    eje.bar(filas, valores, width=1.0, color=colores, linewidth=0)
    linea = eje.axhline(umbral, color="#c44e2b", linewidth=1.2, linestyle="--")
    eje.legend([linea], [etiquetas["umbral"]], loc="upper left", frameon=False)
    valle = []
    for k in range(len(valores)):
        if colores[k] == "#9a9a9a":
            valle.append(filas[k])
    if len(valle) > 0:
        centro = (valle[0] + valle[-1]) / 2
        eje.annotate(
            etiquetas["valle"],
            xy=(centro, umbral * 0.8),
            xytext=(centro, valores.max() * 0.35),
            ha="center",
            arrowprops={"arrowstyle": "->"},
        )
    eje.set_xlabel(etiquetas["x"])
    eje.set_ylabel(etiquetas["y"])
    eje.spines["top"].set_visible(False)
    eje.spines["right"].set_visible(False)
    eje.grid(axis="y", color="#e5e5e5")
    eje.set_axisbelow(True)
    figura.tight_layout()
    figura.savefig(FIGURAS / etiquetas["archivo"], facecolor="white")
    plt.close(figura)


# Remarca liena reconocida por segmentacion
def guardar_grafico_segmentacion(ruta):
    imagen = limpiar(Image.open(ruta)).convert("RGB")
    dibujo = ImageDraw.Draw(imagen)
    for caja in segmentar_lineas(imagen):
        dibujo.rectangle(caja, outline=(196, 78, 43), width=4)
    imagen.save(FIGURAS / "segmentacion-java.png")


def main():
    if len(sys.argv) < 3:
        print("Uso: python figuras.py <imagen_python> <imagen_java>")
        return
    FIGURAS.mkdir(parents=True, exist_ok=True)
    guardar_grafico_tinta(sys.argv[1], "es")
    guardar_grafico_tinta(sys.argv[1], "en")
    guardar_grafico_segmentacion(sys.argv[2])
    print(f"Figuras guardadas en: {FIGURAS}")


if __name__ == "__main__":
    main()
