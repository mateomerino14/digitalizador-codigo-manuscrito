# Bitácora de desarrollo

Registro del avance del prototipo, relacionado con las actividades del cronograma del perfil (Tabla 1).

## 07/11/2026: Estructura inicial del proyecto

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026), como preparación de la estructura común para comparar las herramientas.
- **Qué se hizo:** Se creó el repositorio y se organizó el proyecto en carpetas según los componentes transcriptor, corrector y evaluador, más la interfaz.
- **Decisiones:** Las credenciales de los servicios en la nube y las imágenes de los estudiantes se excluyen del repositorio por seguridad y privacidad.
- **Commits:** `chore: estructura inicial del proyecto`, `docs: agrega bitacora de desarrollo`
- **Pendiente:** Modelos de datos y contrato base de los motores HTR.

## 07/11/2026: Revisión de la documentación de las herramientas HTR

- **Actividad del cronograma:** Objetivo 2, actividad 1, "Revisión de la documentación de las herramientas HTR candidatas" (planificada del 25/10/2026 al 31/10/2026).
- **Qué se hizo:** Se revisó la documentación oficial de Tesseract, PaddleOCR, TrOCR, Google Cloud Vision y Azure AI Vision, y se elaboró la tabla de características de cada herramienta (sección 3.1.1 del Capítulo 3).
- **Decisiones:** Tesseract se mantiene como línea base, aunque no cuenta con un modelo para escritura a mano. TrOCR requiere segmentar las líneas antes de reconocerlas, ya que no las detecta por sí mismo. Los servicios en la nube se usarán dentro de su cantidad gratuita de solicitudes.
- **Commits:** Ninguno, actividad documental.
- **Pendiente:** Preparar la estructura del proyecto para la prueba piloto.


## 07/11/2026: Modelos de datos y contrato de los motores

- **Actividad del cronograma:** Objetivo 2, actividad 2, "Prueba piloto con imágenes de código manuscrito" (planificada del 25/10/2026 al 31/10/2026), como preparación de la estructura común para comparar las herramientas.
- **Qué se hizo:** Se definieron las clases Linea y Resultado, que representan la salida de cualquier herramienta HTR, y la clase abstracta MotorHTR, que todos los motores deben cumplir.
- **Decisiones:** Se guarda la posición horizontal de cada línea para poder reconstruir la indentación más adelante. Se aplicó el patrón Estrategia para que todas las herramientas sean intercambiables y se puedan comparar en igualdad de condiciones.
- **Commits:** `feat: agrega modelos de linea y resultado`, `feat: agrega contrato base de los motores HTR`, `test: agrega pruebas de los modelos y del contrato base`
- **Pendiente:** Motor Tesseract como línea base.

