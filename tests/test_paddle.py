from transcriptor.motores.paddle import MotorPaddle


def caja(texto, x, arriba, abajo, confianza=90):
    return {"texto": texto, "x": x, "arriba": arriba, "abajo": abajo, "confianza": confianza}

def test_agrupa_lineas():
    cajas = [caja("range(5):", 200, 12, 48), caja("print(i)", 90, 70, 105), caja("for i in", 40, 10, 50, confianza=70)]
    lineas = MotorPaddle()._agrupar_lineas(cajas)
    assert [linea.texto for linea in lineas] == ["for i in range(5):", "print(i)"]
    assert lineas[0].x == 40
    assert lineas[0].confianza == 80
    assert lineas[1].x == 90