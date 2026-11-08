# Bitácora de desarrollo

Registro del avance del prototipo, relacionado con las actividades del cronograma del perfil (Tabla 1).

## 07/11/2026: Revisión de la documentación de las herramientas HTR

- **Actividad del cronograma:** Objetivo 2, actividad 1, "Revisión de la documentación de las herramientas HTR candidatas" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se revisó la documentación oficial de Tesseract, PaddleOCR, TrOCR, Google Cloud Vision y Azure AI Vision, y se elaboró la tabla de características de cada herramienta (sección 3.1.1 del Capítulo 3).
- **Decisiones:** Tesseract se mantiene como línea base, aunque no cuenta con un modelo para escritura a mano. TrOCR requiere segmentar las líneas antes de reconocerlas, ya que no las detecta por sí mismo. Los servicios en la nube se usarán dentro de su cantidad gratuita de solicitudes.
- **Commits:** Ninguno, actividad documental.
- **Pendiente:** Preparar la estructura del proyecto para la prueba piloto.

## 07/11/2026: Estructura inicial del proyecto

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026), como preparación de la estructura común para comparar las herramientas.
- **Qué se hizo:** Se creó el repositorio y se organizó el proyecto en carpetas según los componentes transcriptor, corrector y evaluador, más la interfaz.
- **Decisiones:** Las credenciales de los servicios en la nube y las imágenes de los estudiantes se excluyen del repositorio por seguridad y privacidad.
- **Commits:** `chore: estructura inicial del proyecto`, `docs: agrega bitacora de desarrollo`, `docs: completa readme, variables de desarrollo necesarias y bitacora`
- **Pendiente:** Modelos de datos y contrato base de los motores HTR.

## 07/11/2026: Modelos de datos y contrato de los motores

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026), como preparación de la estructura común para comparar las herramientas.
- **Qué se hizo:** Se definieron las clases Linea y Resultado, que representan la salida de cualquier herramienta HTR, y la clase abstracta MotorHTR, que todos los motores deben cumplir.
- **Decisiones:** Se guarda la posición horizontal de cada línea para poder reconstruir la indentación más adelante. Se aplicó el patrón Estrategia para que todas las herramientas sean intercambiables y se puedan comparar en igualdad de condiciones.
- **Commits:** `feat: agrega modelos de linea y resultado`, `feat: agrega contrato base de los motores HTR`, `test: agrega pruebas de los modelos y del contrato base`
- **Pendiente:** Motor Tesseract como línea base.

## 07/11/2026: Motor Tesseract

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se integró Tesseract como primer motor, que reconoce una imagen y agrupa las palabras en líneas con su posición y su confianza.
- **Decisiones:** Tesseract se usa como línea base de la prueba piloto. Se guarda la posición horizontal de cada línea, ya que en las primeras pruebas el texto reconocido pierde la indentación del código.
- **Commits:** `feat: agrega motor Tesseract como linea base`, `test: agrega prueba de agrupacion de lineas de Tesseract`, `fix: quitar impresion de depuracion del motor tesseract`
- **Pendiente:** Script para probar el reconocimiento de una imagen.

## 07/11/2026: Script de prueba

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se creó el script ejecucion_prueba.py, que reconoce una imagen y muestra el texto obtenido, la posición de cada línea y el tiempo empleado.
- **Decisiones:** El script recibe la ruta de la imagen desde la terminal y avisa si la imagen no existe, para facilitar las pruebas manuales.
- **Commits:** `feat: agrega script para probar el reconocimiento de una imagen`
- **Pendiente:** Probar el motor con imágenes reales.

## 07/11/2026: Primera prueba con imágenes reales

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se probó el motor Tesseract con dos imágenes de código manuscrito escritas sobre papel cuadriculado, una en Python y otra en Java, primero en su versión original y luego sin la cuadrícula.
- **Decisiones:** Tesseract confunde las líneas de la cuadrícula con caracteres y no logra separar las líneas de código. Al conservar solo la tinta y eliminar la cuadrícula, el reconocimiento mejora notablemente, por lo que se incorporará una etapa de preprocesamiento antes del reconocimiento.
- **Observaciones:** Con las imágenes limpias, Tesseract conserva la estructura del código pero confunde caracteres parecidos (0 y O, i e I) y palabras reservadas (range como mange, print como priot). La posición horizontal de las líneas indentadas es claramente mayor (145 frente a 50 en Python, 294 frente a 100 en Java), lo que permitirá reconstruir la indentación. En Java se pierden más símbolos, como los punto y coma y la llave de cierre.
- **Commits:** Ninguno, prueba manual.
- **Pendiente:** Registro de motores, servicio del transcriptor y preprocesamiento de las imágenes.

## 07/11/2026: Análisis de requerimientos

- **Actividad del cronograma:** Etapa de análisis del ciclo en cascada, previa al diseño de la arquitectura del Objetivo 3.
- **Qué se hizo:** Se identificaron 12 requerimientos funcionales y 7 no funcionales del prototipo (sección 3.2 del Capítulo 3).
- **Decisiones:** Los requerimientos se redactaron según la norma ISO/IEC/IEEE 29148 y los no funcionales se clasificaron según las características de calidad de la norma ISO/IEC 25010.
- **Commits:** Ninguno, actividad documental.
- **Pendiente:** Registro de motores y servicio del transcriptor.

## 07/11/2026: Registro de motores y servicio del transcriptor

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026), como preparación para ejecutar todas las herramientas desde un mismo punto.
- **Qué se hizo:** Se creó un registro con los motores HTR disponibles y un servicio que recibe una imagen y el nombre del motor, revisa que ambos sean válidos y devuelve el resultado del reconocimiento.
- **Decisiones:** Se aplicó el patrón Fachada para que la interfaz y el script de la prueba piloto usen un solo punto de entrada, sin depender de cada motor. Para agregar una herramienta nueva solo se registra su clase. Las pruebas usan motores simulados para no depender de las herramientas instaladas.
- **Commits:** `feat: agrega registro de motores HTR`, `feat: agrega servicio del transcriptor`, `test: agrega pruebas del servicio del transcriptor`
- **Pendiente:** Preprocesamiento de las imágenes para eliminar la cuadrícula.

## 08/11/2026: Preprocesamiento de las imágenes

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026), y Objetivo 3, actividad 2, "Programación de la lógica de transcripción" (planificada del 01/11/2026 al 14/11/2026).
- **Qué se hizo:** Se implementó la etapa de preprocesamiento, que binariza la imagen conservando la tinta negra y azul, elimina la cuadrícula del papel y reduce el ruido con un filtro de mediana. El servicio del transcriptor aplica esta etapa antes de entregar la imagen a cualquier motor.
- **Decisiones:** Un píxel se considera tinta si su nivel de gris es menor a 110, o si su componente azul supera al rojo en más de 35 con un gris menor a 160. Estos valores se definieron como constantes para poder ajustarlos. El preprocesamiento puede desactivarse para comparar los resultados con y sin limpieza en la prueba piloto.
- **Observaciones:** Con las fotos originales en papel cuadriculado, la limpieza automática produjo el mismo resultado que la limpieza manual, con las mismas posiciones de línea. En Python, la palabra range fue reconocida correctamente, aunque el cero se reconoció como © y la i como ji.
- **Commits:** `feat: agrega preprocesamiento para eliminar la cuadricula`, `test: agrega pruebas del preprocesamiento`, `feat: aplica el preprocesamiento en el servicio del transcriptor`, `feat: permite elegir el motor y guardar la imagen limpia en el script de prueba`
- **Pendiente:** Métricas CER y WER para la prueba piloto.