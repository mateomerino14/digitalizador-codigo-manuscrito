import time
from pathlib import Path
from PIL import Image
from comun.modelos import Linea, Resultado
from transcriptor.motores.base import MotorHTR
from transcriptor.preprocesamiento import limpiar
from transcriptor.segmentacion import segmentar_lineas

class MotorTrOCR(MotorHTR):
    nombre = "trocr"
    modelo_hf = "microsoft/trocr-base-handwritten"
    _procesador = None
    _red = None

    def disponible(self):
        try:
            import torch
            import transformers
        except ImportError:
            return False, "falta instalar torch o transformers"
        return True, ""

    def reconocer(self, ruta: Path):
        procesador, red = self._cargar()
        inicio = time.perf_counter()
        imagen = Image.open(ruta).convert("RGB")
        lineas = []
        #Se corta la imagen en lineas
        for izquierda, arriba, derecha, abajo in segmentar_lineas(limpiar(imagen)):
            caja = (max(izquierda - 10, 0), max(arriba - 10, 0), min(derecha + 10, imagen.width), min(abajo + 10, imagen.height))
            texto = self._leer(procesador, red, imagen.crop(caja))
            lineas.append(Linea(texto, izquierda, arriba))
        texto = "\n".join(linea.texto for linea in lineas)
        return Resultado(self.nombre, texto, lineas, time.perf_counter() - inicio)

    def _leer(self, procesador, red, recorte):
        pixeles = procesador(images=recorte, return_tensors="pt").pixel_values
        ids = red.generate(pixeles, max_new_tokens=64)
        return procesador.batch_decode(ids, skip_special_tokens=True)[0]

    @classmethod
    def _cargar(cls):
        if cls._red is None:
            from transformers import TrOCRProcessor, VisionEncoderDecoderModel
            cls._procesador = TrOCRProcessor.from_pretrained(cls.modelo_hf)
            cls._red = VisionEncoderDecoderModel.from_pretrained(cls.modelo_hf)
        return cls._procesador, cls._red