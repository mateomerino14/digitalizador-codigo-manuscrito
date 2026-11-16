import tempfile
from pathlib import Path

import streamlit as st
from PIL import UnidentifiedImageError

from transcriptor import servicio

MOTORES = {"tesseract": "Tesseract", "paddleocr": "PaddleOCR", "trocr": "TrOCR"}
LENGUAJES = {"Python": "py", "Java": "java"}
ESTILO = (
    "<style>[data-testid='stFileUploaderDropzoneInstructions'] {display: none}</style>"
)


def motores_listos():
    listos = []
    for nombre, estado in servicio.motores_disponibles().items():
        if estado == "listo":
            listos.append(nombre)
        else:
            st.caption(f"{MOTORES[nombre]} no disponible: {estado}")
    return listos


def reconocer_imagen(archivo, motor, limpiar):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as carpeta:
        ruta = Path(carpeta) / archivo.name
        ruta.write_bytes(archivo.getvalue())
        return servicio.reconocer(ruta, motor, limpiar)


def posiciones(resultado):
    filas = []
    for linea in resultado.lineas:
        filas.append({"x": linea.x, "y": linea.y, "texto": linea.texto})
    return filas


def mostrar_opciones():
    archivo = st.file_uploader("Imagen del código", type=["jpg", "jpeg", "png"])
    st.caption("Formatos permitidos (JPG, PNG), hasta 20 MB")
    listos = motores_listos()
    motor = st.selectbox("Herramienta", listos, format_func=MOTORES.get)
    lenguaje = st.selectbox("Lenguaje", ["Python", "Java"])
    limpiar = st.checkbox("Limpiar la imagen", value=True)
    if not st.button("Reconocer", type="primary"):
        return
    if archivo is None:
        st.warning("Primero carga una imagen.")
        return
    if motor is None:
        st.error("No hay ninguna herramienta disponible.")
        return
    try:
        with st.spinner("Reconociendo la imagen..."):
            resultado = reconocer_imagen(archivo, motor, limpiar)
    except UnidentifiedImageError:
        st.error("El archivo no es una imagen válida.")
        return
    except (ValueError, RuntimeError) as error:
        st.error(str(error))
        return
    st.session_state["imagen"] = archivo.getvalue()
    st.session_state["resultado"] = resultado
    st.session_state["lenguaje"] = lenguaje


def mostrar_resultado():
    if "resultado" not in st.session_state:
        st.write("Carga una imagen y presiona Reconocer.")
        return
    resultado = st.session_state["resultado"]
    lenguaje = st.session_state["lenguaje"]
    imagen, texto = st.columns(2)
    with imagen:
        st.write("Imagen cargada")
        st.image(st.session_state["imagen"])
    with texto:
        st.write("Texto reconocido")
        st.code(resultado.texto, language=lenguaje.lower())
        st.download_button(
            "Descargar el código",
            resultado.texto,
            file_name=f"codigo.{LENGUAJES[lenguaje]}",
        )
    lineas, tiempo, herramienta = st.columns(3)
    lineas.metric("Líneas", len(resultado.lineas))
    tiempo.metric("Tiempo", f"{resultado.segundos:.1f} s")
    herramienta.metric("Herramienta", MOTORES[resultado.motor])
    st.write("Posición de cada línea")
    st.dataframe(posiciones(resultado), hide_index=True)


def mostrar_pendiente(componente):
    st.write(f"Esta sección se habilitará con el componente {componente}.")


def main():
    st.set_page_config(page_title="Digitalizador de código manuscrito", layout="wide")
    st.markdown(ESTILO, unsafe_allow_html=True)
    st.title("Digitalizador de código manuscrito")
    reconocer, corregir, evaluar, historial = st.tabs(
        ["Reconocer", "Corregir", "Evaluar", "Historial"]
    )
    with reconocer:
        opciones, resultado = st.columns([1, 2])
        with opciones:
            mostrar_opciones()
        with resultado:
            mostrar_resultado()
    with corregir:
        mostrar_pendiente("corrector")
    with evaluar:
        mostrar_pendiente("evaluador")
    with historial:
        mostrar_pendiente("evaluador")


main()
