# Quality Control CEP (Control Estadístico de Procesos)

Este repositorio contiene un conjunto de herramientas desarrolladas en Python para el análisis y la aplicación de técnicas de Control Estadístico de Procesos (CEP). El objetivo es proporcionar soluciones interactivas para facilitar la creación, análisis y evaluación de sistemas de control de calidad.

---

## Subproyectos

Este proyecto se divide en los siguientes componentes:

1.  **Análisis Univariado:** Una interfaz gráfica para la generación y análisis de cartas de control de Shewhart para una sola variable.
2.  **Muestreo de Aceptación:** Una herramienta de consola para calcular la probabilidad de aceptación de un lote.

---

### 1. Análisis Univariado (`analisis-univariado`)

Una aplicación de escritorio para la generación de cartas de control univariadas de Shewhart (promedio y rango). La herramienta permite visualizar datos históricos, identificar causas especiales, depurar el proceso (Fase I) y establecer límites de control para el monitoreo futuro (Fase II).

#### Características Principales

* **Generación de Cartas de Control (Fase I):** Crea las cartas de control de promedio ($\bar{X}$) y rango (R) a partir de un conjunto de datos históricos. Señala visualmente los puntos que exceden los límites de control.
* **Depuración de Cartas:** Ofrece la opción de eliminar subgrupos afectados por causas asignables y recalcular los límites de control para establecer un estado de control estadístico.
* **Cálculo de Índices de Capacidad:** Calcula los índices **Cp** (capacidad del proceso a largo plazo) y **Cpk** (desplazamiento del proceso respecto al centro de las especificaciones) utilizando los límites de diseño proporcionados.
* **Monitoreo del Proceso (Fase II):** Utiliza los parámetros depurados (media y desviación estándar) para generar cartas de control y monitorear nuevos datos del proceso en tiempo real.

#### Tecnologías Utilizadas

* **Python**
* **Tkinter:** para la interfaz gráfica de usuario (GUI).
* **Matplotlib:** para la generación de los gráficos de control.
* **Numpy:** para los cálculos numéricos y estadísticos.

#### Instalación y Uso

Para utilizar esta herramienta, sigue estos pasos:

1.  Asegúrate de tener Python y las librerías requeridas (`matplotlib`, `numpy`) instaladas en tu entorno.
2.  Clona o descarga el repositorio en tu máquina local.
3.  Navega a la carpeta `analisis-univariado`.
4.  Configura el archivo `data.py` con tus propios datos. Debes modificar las siguientes variables:
    * `datos_univariado`: Una lista de listas que contiene los subgrupos de datos históricos para la Fase I.
        ```python
        # Ejemplo: 5 subgrupos de 4 muestras cada uno
        datos_univariado = [
            [25, 26, 24, 25],
            [28, 27, 26, 27],
            [22, 23, 24, 23],
            [29, 30, 28, 29],
            [25, 25, 26, 26]
        ]
        ```
    * `datos_linea`: Una lista de listas que contiene los nuevos datos del proceso para la Fase II.
        ```python
        # Ejemplo: Nuevos datos para monitorear
        datos_linea = [
            [26, 27, 25, 26],
            [24, 25, 25, 24]
        ]
        ```
    * `diseño_univariado`: Un diccionario con los límites de especificación del diseño.
        ```python
        # Ejemplo: Límites de especificación
        diseño_univariado = {
            "lse": 30,  # Límite Superior de Especificación
            "lie": 20   # Límite Inferior de Especificación
        }
        ```
5.  Ejecuta el archivo `main.py` para lanzar la aplicación.

---

### 2. Muestreo de Aceptación (`muestreo-aceptacion`)

Una herramienta de consola que calcula la probabilidad de aceptación ($P_a$) de un lote de productos. Utiliza los parámetros de un plan de muestreo (tamaño del lote, tamaño de la muestra y número de aceptación) para determinar la probabilidad de que un lote con una determinada proporción de defectos sea aceptado.

#### Características Principales

* Calcula la probabilidad de encontrar un número específico de ítems defectuosos en la muestra.
* Suma estas probabilidades para obtener la probabilidad acumulada de aceptación ($P_a$) del lote completo.

#### Tecnologías Utilizadas

* **Python**

#### Instalación y Uso

La herramienta funciona directamente desde la consola:

1.  Navega a la carpeta `muestreo-aceptacion`.
2.  Ejecuta el archivo `main.py` desde tu terminal:
    ```bash
    python main.py
    ```
3.  El programa te solicitará que ingreses los siguientes datos uno por uno:
    * **N:** Tamaño total del lote.
    * **n:** Tamaño de la muestra a inspeccionar.
    * **c:** Número de aceptación (la cantidad máxima de defectos permitida en la muestra para que el lote sea aceptado).
    * **p:** Proporción de ítems defectuosos en el lote (ej. 0.05 para un 5%).
4.  Tras ingresar los datos, la herramienta imprimirá las probabilidades individuales de encontrar 0, 1, ..., hasta `c` defectos, y finalmente mostrará la **probabilidad de aceptación ($P_a$)** total.
