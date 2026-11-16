import numpy as np
from PIL import Image, ImageFilter


def reducir(imagen):
    lado_mayor = max(imagen.size)
    if lado_mayor <= 2000:
        return imagen
    escala = 2000 / lado_mayor
    ancho = round(imagen.width * escala)
    alto = round(imagen.height * escala)
    return imagen.resize((ancho, alto), Image.Resampling.LANCZOS)


def limpiar(imagen):
    rgb = np.asarray(imagen.convert("RGB")).astype(int)
    gris = np.asarray(imagen.convert("L")).astype(int)
    rojo = rgb[:, :, 0]
    azul = rgb[:, :, 2]
    oscuro = gris < 110
    tinta_azul = (azul - rojo > 35) & (gris < 160)
    tinta = oscuro | tinta_azul
    limpia = np.where(tinta, 0, 255).astype(np.uint8)
    return Image.fromarray(limpia).filter(ImageFilter.MedianFilter(3))
