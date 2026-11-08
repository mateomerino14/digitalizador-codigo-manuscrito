from pathlib import Path
from comun.modelos import Resultado
from transcriptor.motores import MOTORES


def motores_disponibles():
    estado = {}
    for nombre, clase in MOTORES.items():
        listo, motivo = clase().disponible()
        estado[nombre] = "listo" if listo else motivo
    return estado


def reconocer(ruta: Path, nombre_motor: str) -> Resultado:
    if nombre_motor not in MOTORES:
        raise ValueError(f"motor desconocido: {nombre_motor}")
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"no existe la imagen: {ruta}")
    motor = MOTORES[nombre_motor]()
    listo, motivo = motor.disponible()
    if not listo:
        raise RuntimeError(f"{nombre_motor} no disponible: {motivo}")
    return motor.reconocer(ruta)