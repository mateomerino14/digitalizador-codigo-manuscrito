from PIL import Image, ImageDraw

from transcriptor.segmentacion import segmentar_lineas


def hoja():
    return Image.new("L", (200, 200), 255)


def test_dos_lineas():
    imagen = hoja()
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle([20, 20, 150, 40], fill=0)
    dibujo.rectangle([60, 100, 180, 120], fill=0)
    assert segmentar_lineas(imagen) == [(20, 20, 151, 41), (60, 100, 181, 121)]


def test_une_punto():
    imagen = hoja()
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle([20, 10, 25, 14], fill=0)
    dibujo.rectangle([20, 20, 150, 40], fill=0)
    assert segmentar_lineas(imagen) == [(20, 10, 151, 41)]


def test_ignora_ruido():
    imagen = hoja()
    ImageDraw.Draw(imagen).rectangle([20, 100, 150, 103], fill=0)
    assert segmentar_lineas(imagen) == []


def test_separa_trazo():
    imagen = hoja()
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle([20, 20, 150, 40], fill=0)
    dibujo.rectangle([20, 60, 150, 80], fill=0)
    dibujo.rectangle([100, 40, 101, 60], fill=0)
    assert segmentar_lineas(imagen) == [(20, 20, 151, 41), (20, 60, 151, 81)]


def test_llave_sola():
    imagen = hoja()
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle([20, 20, 150, 40], fill=0)
    dibujo.rectangle([30, 80, 32, 110], fill=0)
    assert segmentar_lineas(imagen) == [(20, 20, 151, 41), (30, 80, 33, 111)]
