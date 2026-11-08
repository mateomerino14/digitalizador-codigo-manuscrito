from transcriptor.motores.tesseract import MotorTesseract
from transcriptor.motores.paddle import MotorPaddle

MOTORES = {
    MotorTesseract.nombre: MotorTesseract,
    MotorPaddle.nombre: MotorPaddle,
}