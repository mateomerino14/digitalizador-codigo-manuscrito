import pytest
from PIL import Image
from comun.modelos import Resultado
from transcriptor import servicio
from transcriptor.motores.base import MotorHTR

class MotorFalso(MotorHTR):
    nombre = "falso"

    def disponible(self):
        return True, ""

    def reconocer(self, ruta):
        return Resultado(self.nombre, "x = 1")

class MotorApagado(MotorHTR):
    nombre = "apagado"

    def disponible(self):
        return False, "sin conexion"

    def reconocer(self, ruta):
        return Resultado(self.nombre, "")

# Motores falsos
@pytest.fixture
def motores(monkeypatch):
    falsos = {"falso": MotorFalso, "apagado": MotorApagado}
    monkeypatch.setattr(servicio, "MOTORES", falsos)

@pytest.fixture
def imagen(tmp_path):
    ruta = tmp_path / "prueba.png"
    Image.new("RGB", (10, 10), "white").save(ruta)
    return ruta

def test_estado(motores):
    estado = servicio.motores_disponibles()
    assert estado == {"falso": "listo", "apagado": "sin conexion"}

def test_reconoce(motores, imagen):
    resultado = servicio.reconocer(imagen, "falso")
    assert resultado.texto == "x = 1"

def test_motor_desconocido(motores, imagen):
    with pytest.raises(ValueError):
        servicio.reconocer(imagen, "otro")

def test_imagen_inexistente(motores, tmp_path):
    with pytest.raises(FileNotFoundError):
        servicio.reconocer(tmp_path / "no_hay.png", "falso")

def test_motor_apagado(motores, imagen):
    with pytest.raises(RuntimeError):
        servicio.reconocer(imagen, "apagado")