import pytest
from evaluador.metricas import cer, distancia, wer


def test_distancia():
    assert distancia("range", "mange") == 1
    assert distancia("print", "") == 5
    assert distancia("suma", "suma") == 0


def test_cer():
    assert cer("print", "priot") == 0.2


def test_wer():
    assert wer("for i in range(5):", "for ji in range(5):") == 0.25


def test_referencia_vacia():
    with pytest.raises(ValueError):
        cer("", "x = 1")