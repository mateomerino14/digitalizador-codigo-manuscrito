import numpy as np
from PIL import Image, ImageFilter


def limpiar(imagen: Image.Image):
    rgb = np.asarray(imagen.convert("RGB")).astype(int)
    gris = np.asarray(imagen.convert("L")).astype(int)
    rojo = rgb[:, :, 0]
    azul = rgb[:, :, 2]
    oscuro = gris < 110
    tinta_azul = (azul - rojo > 35) & (gris < 160)
    tinta = oscuro | tinta_azul
    limpia = np.where(tinta, 0, 255).astype(np.uint8)
    return Image.fromarray(limpia).filter(ImageFilter.MedianFilter(3))