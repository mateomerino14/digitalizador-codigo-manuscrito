from dataclasses import dataclass, field

# Moldes de datos para normalizar los resultados de cada reconocedor


@dataclass
class Linea:
    texto: str
    x: int
    y: int
    confianza: float | None = None


@dataclass
class Resultado:
    motor: str
    texto: str
    lineas: list[Linea] = field(default_factory=list)
    segundos: float = 0.0
