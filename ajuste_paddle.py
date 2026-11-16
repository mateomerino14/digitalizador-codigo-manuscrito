import statistics

from evaluador.metricas import cer
from piloto import PILOTO, normalizar, referencia_de
from transcriptor import servicio
from transcriptor.motores.paddle import MotorPaddle, _cargar_torch_primero

IMAGENES = ["py-03", "py-06", "py-09", "py-12", "py-18"]
BASE = {
    "use_doc_orientation_classify": False,
    "use_doc_unwarping": False,
    "use_textline_orientation": False,
    "enable_mkldnn": False,
}
CONFIGURACIONES = {
    "medium": {},
    "medium y limite 960": {
        "text_det_limit_type": "max",
        "text_det_limit_side_len": 960,
    },
    "small y limite 960": {
        "text_detection_model_name": "PP-OCRv6_small_det",
        "text_recognition_model_name": "PP-OCRv6_small_rec",
        "text_det_limit_type": "max",
        "text_det_limit_side_len": 960,
    },
}


def preparar_motor(extra):
    _cargar_torch_primero()
    from paddleocr import PaddleOCR

    parametros = dict(BASE)
    parametros.update(extra)
    MotorPaddle._ocr = PaddleOCR(**parametros)


# Medir CER y tiempo con conf cargada
def medir():
    errores = []
    tiempos = []
    for imagen in IMAGENES:
        ruta = PILOTO / "python" / (imagen + ".jpg")
        resultado = servicio.reconocer(ruta, "paddleocr", False)
        error = cer(referencia_de(ruta), normalizar(resultado.texto))
        print(f"  {imagen}  cer={error:.3f}  seg={resultado.segundos:.1f}")
        errores.append(error)
        tiempos.append(resultado.segundos)
    return statistics.mean(errores), statistics.mean(tiempos)


# Probando modelo small
def main():
    resumen = []
    for nombre, extra in CONFIGURACIONES.items():
        print(nombre)
        try:
            preparar_motor(extra)
            cer_medio, seg_medio = medir()
        except Exception as error:
            print(f"  error: {error}")
            continue
        resumen.append((nombre, cer_medio, seg_medio))
    print()
    print("configuracion            cer     seg")
    for nombre, cer_medio, seg_medio in resumen:
        print(f"{nombre:<22} {cer_medio:>6.3f} {seg_medio:>6.1f}")


if __name__ == "__main__":
    main()
