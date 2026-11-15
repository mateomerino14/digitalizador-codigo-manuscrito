from abc import ABC, abstractmethod
from pathlib import Path


class MotorHTR(ABC):
    nombre = "base"

    # Determina si un reconocedor se puede usar
    @abstractmethod
    def disponible(self): ...

    @abstractmethod
    def reconocer(self, ruta: Path): ...
