import tempfile
from pathlib import Path

from PIL import Image

from transcriptor.motores import MOTORES
from transcriptor.preprocesamiento import limpiar


def motores_disponibles():
    estado = {}
    for nombre, clase in MOTORES.items():
        listo, motivo = clase().disponible()
        estado[nombre] = "listo" if listo else motivo
    return estado


def reconocer(ruta, nombre_motor, limpiar_imagen=True):
    if nombre_motor not in MOTORES:
        raise ValueError(f"motor desconocido: {nombre_motor}")
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"no existe la imagen: {ruta}")
    motor = MOTORES[nombre_motor]()
    listo, motivo = motor.disponible()
    if not listo:
        raise RuntimeError(f"{nombre_motor} no disponible: {motivo}")
    if not limpiar_imagen:
        return motor.reconocer(ruta)
    # imagen limpia
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as carpeta:
        limpia = Path(carpeta) / "limpia.png"
        limpiar(Image.open(ruta)).save(limpia)
        return motor.reconocer(limpia)
