from transcriptor.motores.tesseract import MotorTesseract
from transcriptor.motores.paddle import MotorPaddle
from transcriptor.motores.trocr import MotorTrOCR

MOTORES = {
    MotorTesseract.nombre: MotorTesseract,
    MotorPaddle.nombre: MotorPaddle,
    MotorTrOCR.nombre: MotorTrOCR,
}
