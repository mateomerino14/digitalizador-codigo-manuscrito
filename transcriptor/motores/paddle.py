import time
from pathlib import Path
from comun.modelos import Linea, Resultado
from transcriptor.motores.base import MotorHTR


class MotorPaddle(MotorHTR):
    nombre = "paddleocr"
    _ocr = None

    def disponible(self):
        try:
            import paddle
            import paddleocr
        except ImportError:
            return False, "falta instalar paddlepaddle o paddleocr"
        return True, ""

    def reconocer(self, ruta: Path) -> Resultado:
        modelo = self._modelo()
        inicio = time.perf_counter()
        datos = modelo.predict(str(ruta))[0]
        cajas = []
        for texto, caja, confianza in zip(datos["rec_texts"], datos["rec_boxes"], datos["rec_scores"]):
            cajas.append({"texto": texto, "x": int(caja[0]), "arriba": int(caja[1]), "abajo": int(caja[3]), "confianza": float(confianza) * 100})
        lineas = self._agrupar_lineas(cajas)
        texto = "\n".join(linea.texto for linea in lineas)
        return Resultado(self.nombre, texto, lineas, time.perf_counter() - inicio)

    @classmethod
    def _modelo(cls):
        if cls._ocr is None:
            from paddleocr import PaddleOCR
            cls._ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False, enable_mkldnn=False,)
        return cls._ocr

    def _agrupar_lineas(self, cajas):
        filas = []
        for caja in sorted(cajas, key=lambda c: (c["arriba"] + c["abajo"]) / 2):
            centro = (caja["arriba"] + caja["abajo"]) / 2
            if filas and filas[-1][0]["arriba"] <= centro <= filas[-1][0]["abajo"]:
                filas[-1].append(caja)
            else:
                filas.append([caja])
        lineas = []
        for fila in filas:
            fila.sort(key=lambda c: c["x"])
            texto = " ".join(c["texto"] for c in fila)
            confianza = sum(c["confianza"] for c in fila) / len(fila)
            lineas.append(Linea(texto, fila[0]["x"], min(c["arriba"] for c in fila), confianza))
        return lineas