import pytest
from comun.modelos import Linea, Resultado
from transcriptor.motores.base import MotorHTR


def test_guarda_lineas():
    linea = Linea("x = 1", 40, 10)
    resultado = Resultado("prueba", "x = 1", [linea])
    assert resultado.lineas[0].x == 40
    assert resultado.lineas[0].confianza is None


def test_lista_propia():
    primero = Resultado("prueba", "")
    segundo = Resultado("prueba", "")
    primero.lineas.append(Linea("a", 0, 0))
    assert segundo.lineas == []


def test_motor_incompleto():
    with pytest.raises(TypeError):
        MotorHTR()