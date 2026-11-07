# Digitalizador de código manuscrito

Prototipo para la digitalización de código fuente manuscrito mediante reconocimiento de escritura y corrección léxica, desarrollado como Proyecto de Grado en la Carrera de Ingeniería Informática de la FCyT-UMSS.

## Componentes

- `transcriptor`: convierte imágenes de código manuscrito en texto mediante herramientas HTR.
- `corrector`: corrige errores léxicos comparando el texto con las palabras reservadas de Java y Python.
- `evaluador`: mide el desempeño del prototipo y guarda el historial de evaluaciones.
- `app`: interfaz en Streamlit.

## Instalación

1. Instalar Python 3.10 o superior y Tesseract OCR.
2. Crear y activar un entorno virtual.
3. Instalar las dependencias con `pip install -r requirements.txt`.
4. Copiar `.env.example` como `.env` y completar las claves de los servicios en la nube.

## Pruebas

python -m pytest