from PIL import Image, ImageDraw
from transcriptor.preprocesamiento import limpiar


def hoja(color, ancho=1):
    imagen = Image.new("RGB", (40, 40), "white")
    ImageDraw.Draw(imagen).line([(0, 20), (39, 20)], fill=color, width=ancho)
    return imagen


def test_quita_cuadricula():
    limpia = limpiar(hoja((150, 180, 220)))
    assert limpia.getpixel((20, 20)) == 255


def test_tinta_negra():
    limpia = limpiar(hoja((30, 30, 30), ancho=5))
    assert limpia.getpixel((20, 20)) == 0


def test_tinta_azul():
    limpia = limpiar(hoja((90, 110, 180), ancho=5))
    assert limpia.getpixel((20, 20)) == 0


def test_quita_puntos():
    imagen = Image.new("RGB", (40, 40), "white")
    imagen.putpixel((20, 20), (0, 0, 0))
    assert limpiar(imagen).getpixel((20, 20)) == 255
