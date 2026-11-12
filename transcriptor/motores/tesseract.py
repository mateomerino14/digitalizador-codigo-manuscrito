import shutil
import time
from pathlib import Path
from comun.modelos import Linea, Resultado
from transcriptor.motores.base import MotorHTR


class MotorTesseract(MotorHTR):
    nombre = "tesseract"

    def disponible(self):
        if shutil.which("tesseract") is None:
            return False, "tesseract no esta instalado o no esta en el PATH"
        try:
            import pytesseract
        except ImportError:
            return False, "falta instalar pytesseract"
        return True, ""

    def reconocer(self, ruta: Path):
        import pytesseract
        from PIL import Image

        inicio = time.perf_counter()
        datos = pytesseract.image_to_data(
            Image.open(ruta), output_type=pytesseract.Output.DICT
        )
        # print(datos)
        lineas = self._agrupar_lineas(datos)
        texto = "\n".join(linea.texto for linea in lineas)
        return Resultado(self.nombre, texto, lineas, time.perf_counter() - inicio)

    def _agrupar_lineas(self, datos):
        grupos = {}
        for i, palabra in enumerate(datos["text"]):
            if not palabra.strip():
                continue
            clave = (datos["block_num"][i], datos["par_num"][i], datos["line_num"][i])
            grupos.setdefault(clave, []).append(i)
        lineas = []
        for indices in grupos.values():
            texto = " ".join(datos["text"][i] for i in indices)
            x = min(datos["left"][i] for i in indices)
            y = min(datos["top"][i] for i in indices)
            confianza = sum(float(datos["conf"][i]) for i in indices) / len(indices)
            lineas.append(Linea(texto, x, y, confianza))
        return sorted(lineas, key=lambda linea: linea.y)
