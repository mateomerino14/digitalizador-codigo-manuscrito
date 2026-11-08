from transcriptor.motores.tesseract import MotorTesseract


def test_agrupa_lineas():
    datos = {
        "text": ["print(x)", "", "x", "=", "1"],
        "block_num": [1, 1, 1, 1, 1],
        "par_num": [1, 1, 1, 1, 1],
        "line_num": [2, 2, 1, 1, 1],
        "left": [40, 0, 0, 20, 40],
        "top": [60, 0, 10, 10, 10],
        "conf": [90, -1, 80, 70, 60],
    }
    lineas = MotorTesseract()._agrupar_lineas(datos)
    assert [linea.texto for linea in lineas] == ["x = 1", "print(x)"]
    assert lineas[1].x == 40
    assert lineas[0].confianza == 70