# PS3 HFW Proxy - XMB Edition

Este proyecto es una interfaz gráfica estilo **XMB de PS3** diseñada
para ejecutar un servidor proxy que permite a una PS3 descargar un
archivo **PUP modificado** (HFW, CFW, parches, etc.) haciéndole creer
que es una actualización oficial.

La herramienta está pensada para simplificar el proceso de instalación
de **HFW + HEN** o pruebas de actualización en consolas PS3.

![Descripci贸n de la imagen](https://github.com/Azzlaer/PS3_ProxyUP/blob/main/01.png)

------------------------------------------------------------------------

## 🎮 Características

-   Interfaz visual inspirada en el **XMB de PlayStation 3**\
-   Indicadores de estado (🟢 activo / 🔴 inactivo)\
-   Logs en tiempo real\
-   Opción para seleccionar archivo PUP\
-   Configuración de:
    -   Host
    -   Puerto
    -   Versión reportada\
-   Botón de **Inicio** y **Detención** del proxy\
-   Sin botón de maximizar para evitar deformaciones\
-   Compatible con **Windows, Linux y macOS**

------------------------------------------------------------------------

## 🧩 Requisitos

-   Python 3.8+
-   Librerías estándar (tkinter, http.server)
-   No requiere instalación de módulos externos --- todo está incluido
    en Python

------------------------------------------------------------------------

## 🚀 Cómo usar

1.  Ejecuta el script:

    ``` bash
    python ps3_proxy_xmb.py
    ```

2.  Selecciona tu archivo `PS3UPDAT.PUP`.

3.  Ajusta:

    -   Host (recomendado: 0.0.0.0)
    -   Puerto (ejemplo: 8080)
    -   Versión reportada (ej: 4.90)

4.  Presiona **▶️ Iniciar Proxy**.

5.  En la PS3, configura la conexión a Internet con:

    -   **Proxy habilitado**
    -   IP de tu PC
    -   Puerto configurado en el programa

6.  En la PS3 ve a: **Ajustes → Actualización del Sistema → Actualizar
    mediante Internet**

La consola descargará tu PUP desde tu PC.

------------------------------------------------------------------------

## 📁 Estructura de archivos

    PS3-HFW-Proxy/
    │── ps3_proxy_xmb.py
    │── README.md

------------------------------------------------------------------------

## 📝 Notas importantes

-   Este software **no modifica la consola**, solo actúa como servidor.\
-   No distribuye archivos PUP.\
-   Úsalo únicamente con archivos PUP legítimos o con fines educativos.

------------------------------------------------------------------------

## 🧑‍💻 Autor

Generado con ayuda de ChatGPT --- XMB Edition UI.

------------------------------------------------------------------------

## 📜 Licencia

Este proyecto es de uso libre para investigación y modificación
personal.
