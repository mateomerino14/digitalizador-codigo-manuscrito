# Bitácora de desarrollo

Registro del avance del prototipo, relacionado con las actividades del cronograma del perfil (Tabla 1).

## 07/11/2026: Revisión de la documentación de las herramientas HTR

- **Actividad del cronograma:** Objetivo 2, actividad 1, "Revisión de la documentación de las herramientas HTR candidatas" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se revisó la documentación oficial de Tesseract, PaddleOCR, TrOCR, Google Cloud Vision y Azure AI Vision, y se elaboró la tabla de características de cada herramienta del Capítulo 3.
- **Decisiones:** Tesseract se mantiene como línea base, aunque no cuenta con un modelo para escritura a mano. TrOCR requiere segmentar las líneas antes de reconocerlas, ya que no las detecta por sí mismo. Los servicios en la nube se usarían dentro de su cantidad gratuita de solicitudes.
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
- **Decisiones:** Tesseract se usa como línea base de la prueba piloto. Se guarda la posición horizontal de cada línea, ya que el texto reconocido pierde la indentación del código.
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
- **Observaciones:** Con las imágenes limpias, Tesseract obtiene el mismo número de líneas que el código escrito, pero confunde caracteres parecidos, como el 0 con la O y el 1 con una barra vertical, y palabras reservadas, como range reconocida como mange y print como priot. La posición horizontal de la línea indentada es claramente mayor, 145 frente a valores entre 45 y 54 en Python, y 294 frente a valores entre 91 y 125 en Java, lo que permitirá reconstruir la indentación. En Java se pierden más símbolos, como los punto y coma y la llave de cierre.
- **Commits:** Ninguno, prueba manual.
- **Pendiente:** Registro de motores, servicio del transcriptor y preprocesamiento de las imágenes.

## 07/11/2026: Análisis de requerimientos

- **Actividad del cronograma:** Etapa de análisis del ciclo en cascada, previa al diseño de la arquitectura del Objetivo 3.
- **Qué se hizo:** Se identificaron 12 requerimientos funcionales y 7 no funcionales del prototipo, documentados en el Capítulo 3.
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
- **Decisiones:** Un píxel se considera tinta si su nivel de gris es menor a 110, o si su componente azul supera al rojo en más de 35 con un gris menor a 160. El preprocesamiento puede desactivarse para comparar los resultados con y sin limpieza en la prueba piloto.
- **Observaciones:** Con las fotos originales en papel cuadriculado, la limpieza automática produjo el mismo resultado que la limpieza manual, con las mismas posiciones de línea. En Python, la palabra range fue reconocida correctamente, aunque el cero se reconoció como © y la i como ji.
- **Commits:** `feat: agrega libreria para preprocesamiento para eliminar la cuadricula`, `test: agrega pruebas del preprocesamiento`, `feat: aplica el preprocesamiento en el servicio del transcriptor`, `feat: permite elegir el motor y guardar la imagen limpia en el script`
- **Pendiente:** Métricas CER y WER para la prueba piloto.

## 08/11/2026: Métricas CER y WER

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026), como preparación para comparar las herramientas.
- **Qué se hizo:** Se implementó la distancia de Levenshtein y, a partir de ella, la tasa de error de caracteres (CER) y la tasa de error de palabras (WER), según las fórmulas del Capítulo 2.
- **Decisiones:** La distancia recibe secuencias, por lo que la misma función compara caracteres para el CER y palabras para el WER. Se ubicó en el componente evaluador para reutilizarla en el Objetivo 5. Si la referencia está vacía se lanza un error, para no dividir entre cero.
- **Observaciones:** Con la imagen de Python sin cuadrícula se obtuvo un CER de 0.26 y un WER de 0.91. El WER es mucho mayor porque una palabra cuenta como error aunque tenga un solo carácter distinto.
- **Commits:** `feat: agrega calculo de distancia de Levenshtein, CER y WER`, `test: agrega pruebas de las metricas`, `fix: Ajuste de metrica en evaluador`
- **Pendiente:** Motor PaddleOCR.

## 08/11/2026: Motor PaddleOCR

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se integró PaddleOCR como segundo motor, registrándolo sin modificar el servicio. Como PaddleOCR detecta fragmentos de texto, se agrupan los que están a la misma altura para formar líneas completas de código.
- **Decisiones:** El modelo se carga una sola vez y se reutiliza, y el tiempo de reconocimiento se mide sin incluir esa carga. La confianza se convierte a la escala de 0 a 100 para compararla con Tesseract.
- **Problemas:** PaddlePaddle 3.3.1 falla en Windows sin tarjeta gráfica con el error `ConvertPirAttribute2RuntimeAttribute not support`, causado por la librería de aceleración oneDNN. Se resolvió desactivándola con `enable_mkldnn=False`.
- **Observaciones:** Se usó el modelo PP-OCRv6 medium, la versión por defecto de PaddleOCR 3.7.0. Reconoció mucho mejor que Tesseract, sobre todo en Java. Los errores más frecuentes fueron suma como soma, el 5 como s, el 0 como O y println como printin, y la llave de cierre se detectó sin texto. La indentación se conservó en ambas imágenes. Sin oneDNN, el reconocimiento tardó entre 17 y 35 segundos por imagen.
- **Commits:** `feat: agrega motor PaddleOCR`, `feat: registra el motor PaddleOCR`, `test: agrega prueba de agrupacion de lineas de PaddleOCR`, `fix: excluye la carga del modelo del tiempo de Paddle`
- **Pendiente:** Motor TrOCR con segmentación de líneas.

## 11/11/2026: Exclusión de Google Cloud Vision

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se intentó activar la prueba gratuita de Google Cloud para usar Cloud Vision.
- **Problemas:** Para cuentas registradas en Bolivia, Google Cloud exige un prepago de 30 USD antes de activar la prueba gratuita y sus créditos.
- **Decisiones:** Google Cloud Vision no se incluye en la prueba piloto por no cumplir el criterio de disponibilidad. Se conserva una captura del aviso como evidencia.
- **Commits:** Ninguno, actividad de configuración.
- **Pendiente:** Cuenta de Azure AI Vision.

## 11/11/2026: Exclusión de Azure AI Vision

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se intentó activar Azure AI Vision mediante Azure for Students y mediante una cuenta gratuita.
- **Problemas:** Azure for Students no reconoció el dominio del correo institucional de la UMSS. La verificación académica manual tampoco fue posible, porque la Universidad Mayor de San Simón no figura en la lista de instituciones de Microsoft y el formulario no permite ingresarla. Al intentar crear una cuenta gratuita, Microsoft bloqueó el acceso por no poder validar la cuenta.
- **Decisiones:** Azure AI Vision no se incluye en la prueba piloto por no cumplir el criterio de disponibilidad. Con la exclusión de ambos servicios en la nube, la piloto se realiza con Tesseract como línea base, PaddleOCR y TrOCR, todas de código abierto. Gracias al registro de motores, un servicio en la nube puede integrarse más adelante si se obtiene acceso. Se conservan capturas de los mensajes como evidencia.
- **Commits:** `docs: registra la exclusion de Google Cloud Vision y Azure AI Vision`
- **Pendiente:** Motor TrOCR con segmentación de líneas.

## 11/11/2026 - 12/11/2026: Motor TrOCR y segmentación de líneas

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se integró TrOCR con el modelo microsoft/trocr-base-handwritten, ajustado con IAM. Como TrOCR solo reconoce una línea por imagen, se implementó una segmentación de líneas por proyección horizontal, que cuenta la tinta de cada fila de píxeles.
- **Problemas:**
  - La primera descarga del modelo, de 1.33 GB, falló por falta de espacio en el disco y se liberó espacio.
  - En Python, las dos primeras líneas quedaron unidas. Al imprimir la tinta por fila se observó que entre ellas no había una fila vacía, sino un valle de alrededor de 11 píxeles por fila, debido a un trazo que cruzaba de una línea a otra.
  - Un primer umbral relativo a toda la imagen separó esas líneas, pero eliminó en Java la línea con la llave de cierre, por tener muy poca tinta.
  - En Java, los pedazos de la llave de apertura, las colas de los punto y coma y los puntos de la i aparecían como líneas sueltas. Al ser muchos, la mediana de alturas quedaba en el tamaño de un pedazo y no de una línea.
- **Decisiones:**
  - Los bloques de tinta se buscan con un umbral mínimo de 2 píxeles por fila, para no perder ningún trazo, y cada bloque se divide donde su tinta baja del 10% de su propia fila más llena.
  - La altura típica de una línea se calcula con la mediana de las partes que miden al menos el 30% de la más alta.
  - Las partes menores al 30% de esa altura se consideran pedazos y se unen con la línea más cercana, arriba o abajo, si están a menos de media altura típica.
  - Todas las reglas son relativas, para adaptarse al tamaño de la letra de cada imagen. Cada caso quedó cubierto con una prueba unitaria.
- **Observaciones:** Con la segmentación final se obtuvieron 4 líneas en Python y 5 en Java, con la indentación conservada. Al recibir una sola línea por imagen, TrOCR mejoró, por ejemplo range pasó de reconocerse como France a reconocerse correctamente. Aun así, TrOCR tiende a convertir el código en palabras inglesas y confunde los símbolos, como la llave de cierre reconocida como 3 y println como print in. El tiempo fue de 10 segundos en Python y 15 en Java.
- **Commits:** `feat: agrega segmentacion de lineas por proyeccion horizontal`, `test: agrega pruebas de la segmentacion de lineas`, `feat: agrega motor TrOCR`, `feat: registra el motor TrOCR`, `refactor: segmentacion final, pruebas y ajustes de estilo con ruff`
- **Pendiente:** Documentar la implementación del transcriptor en el Capítulo 3.

## 11/11/2026 - 15/11/2026: Estilo y legibilidad del código

- **Actividad del cronograma:** Objetivo 3, actividad 2, "Programación de la lógica de transcripción" (planificada del 01/11/2026 al 14/11/2026).
- **Qué se hizo:** Se reescribió el motor PaddleOCR con estructuras básicas y funciones pequeñas con nombre, y se aplicó la guía de estilo PEP 8 a todo el proyecto con la herramienta Ruff, tanto en el formato como en el orden de los imports.
- **Decisiones:** Se prioriza la legibilidad sobre la brevedad, para que cada función pueda explicarse línea por línea. Se quitaron las anotaciones de tipo en los valores de retorno. Los imports que solo comprueban si una librería está instalada se marcan con `# noqa: F401`, porque son intencionales.
- **Commits:** `fix: ajuste de codigo`, `style: corrige comentarios y formato segun PEP 8`, `style: aplica formato PEP 8 con ruff`, `refactor: segmentacion final, pruebas y ajustes de estilo con ruff`
- **Pendiente:** Configuración de Ruff y script de las figuras del Capítulo 3.

## 12/11/2026: Documentación de la implementación del transcriptor

- **Actividad del cronograma:** Objetivo 3, actividad 2, "Programación de la lógica de transcripción" (planificada del 01/11/2026 al 14/11/2026).
- **Qué se hizo:** Se documentó en el Capítulo 3 la implementación del componente transcriptor, con el preprocesamiento, la integración de las herramientas y la segmentación de líneas, y se agregó la exclusión de los servicios en la nube a la prueba piloto.
- **Decisiones:** Se definieron las condiciones de captura de las imágenes, de frente, con iluminación uniforme, tinta negra o azul y una sola hoja por imagen, ya que el proyecto trata sobre el reconocimiento del código y no sobre el tratamiento de imágenes. Por ello no se implementa la corrección de inclinación, y estas mismas condiciones se aplicarán en la captura de la muestra.
- **Commits:** Ninguno, actividad documental.
- **Pendiente:** Imágenes y referencias de la prueba piloto.

## 15/11/2026: Conflicto entre PaddlePaddle y PyTorch

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Al volver a ejecutar PaddleOCR después de instalar PyTorch para TrOCR, el motor dejó de funcionar.
- **Problemas:** PaddleOCR carga la librería modelscope, que a su vez carga PyTorch. En Windows, cuando PaddlePaddle se carga primero, PyTorch falla al cargar sus librerías con el error `WinError 127` en `shm.dll`.
- **Decisiones:** Pendiente de diagnóstico.
- **Commits:** Ninguno.
- **Pendiente:** Resolver el conflicto antes de ejecutar la prueba piloto.

## 15/11/2026: Script de figuras y uniformidad del código

- **Actividad del cronograma:** Objetivo 3, actividad 2, "Programación de la lógica de transcripción" (planificada del 01/11/2026 al 14/11/2026).
- **Qué se hizo:** Se creó el script figuras.py, que genera las Figuras 3 y 4 del Capítulo 3 a partir de las imágenes de prueba, usando las mismas funciones de preprocesamiento y segmentación del prototipo. Se agregó la configuración de Ruff al repositorio y se unificó el estilo del código.
- **Decisiones:** Las figuras se generan con código para que puedan reproducirse y verificarse. Las funciones que realizan una acción se nombran con verbos y las que calculan un valor se nombran según el valor que devuelven, por lo que se renombraron cinco funciones. Se quitaron todas las anotaciones de tipo para mantener un mismo criterio en todo el proyecto. Se aceptan las comas finales que agrega Ruff al dividir una expresión en varias líneas.
- **Commits:** `chore: agrega configuracion de ruff`, `feat: agrega script que genera las figuras de la segmentacion`, `refactor: nombra funciones segun su accion y quita anotaciones de tipo`
- **Pendiente:** Resolver el conflicto entre PaddlePaddle y PyTorch.