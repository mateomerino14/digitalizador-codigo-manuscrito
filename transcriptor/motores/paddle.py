import time

from comun.modelos import Linea, Resultado
from transcriptor.motores.base import MotorHTR


# Choque entre torch y paddle
def _cargar_torch_primero():
    try:
        import torch  # noqa: F401
    except ImportError:
        pass


class MotorPaddle(MotorHTR):
    nombre = "paddleocr"
    _ocr = None

    def disponible(self):
        _cargar_torch_primero()
        try:
            import paddle  # noqa: F401
            import paddleocr  # noqa: F401
        except ImportError:
            return False, "falta instalar paddlepaddle o paddleocr"
        return True, ""

    def reconocer(self, ruta):
        modelo = self._cargar_modelo()
        inicio = time.perf_counter()
        datos = modelo.predict(str(ruta))[0]
        textos = datos["rec_texts"]
        rectangulos = datos["rec_boxes"]
        confianzas = datos["rec_scores"]
        cajas = []
        for k in range(len(textos)):
            rectangulo = rectangulos[k]
            caja = {
                "texto": textos[k],
                "x": int(rectangulo[0]),
                "arriba": int(rectangulo[1]),
                "abajo": int(rectangulo[3]),
                "confianza": float(confianzas[k]) * 100,
            }
            cajas.append(caja)
        lineas = self._agrupar_lineas(cajas)
        textos_lineas = []
        for linea in lineas:
            textos_lineas.append(linea.texto)
        texto = "\n".join(textos_lineas)
        segundos = time.perf_counter() - inicio
        return Resultado(self.nombre, texto, lineas, segundos)

    @classmethod
    def _cargar_modelo(cls):
        if cls._ocr is None:
            _cargar_torch_primero()
            from paddleocr import PaddleOCR

            """cls._ocr = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                enable_mkldnn=False,
            )"""
            # Probando con el modelo small
            cls._ocr = PaddleOCR(
                text_detection_model_name="PP-OCRv6_small_det",
                text_recognition_model_name="PP-OCRv6_small_rec",
                text_det_limit_type="max",
                text_det_limit_side_len=960,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                enable_mkldnn=False,
            )
        return cls._ocr

    def _agrupar_lineas(self, cajas):
        cajas = sorted(cajas, key=self._centro)
        filas = []
        for caja in cajas:
            if len(filas) > 0 and self._es_misma_fila(filas[-1][0], caja):
                filas[-1].append(caja)
            else:
                filas.append([caja])
        lineas = []
        for fila in filas:
            lineas.append(self._unir_fila(fila))
        return lineas

    def _centro(self, caja):
        return (caja["arriba"] + caja["abajo"]) / 2

    def _es_misma_fila(self, primera, caja):
        centro = self._centro(caja)
        return primera["arriba"] <= centro <= primera["abajo"]

    def _unir_fila(self, fila):
        fila = sorted(fila, key=self._posicion_x)
        textos = []
        suma_confianza = 0
        arriba = fila[0]["arriba"]
        for caja in fila:
            textos.append(caja["texto"])
            suma_confianza = suma_confianza + caja["confianza"]
            arriba = min(arriba, caja["arriba"])
        texto = " ".join(textos)
        confianza = suma_confianza / len(fila)
        return Linea(texto, fila[0]["x"], arriba, confianza)

    def _posicion_x(self, caja):
        return caja["x"]
