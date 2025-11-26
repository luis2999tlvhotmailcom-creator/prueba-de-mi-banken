# AS241S4_PII_T09-be-

# 🚀 Backend: Guía de Configuración en Codespaces

Esta guía explica cómo ejecutar el servidor de la API de Flask en un entorno de GitHub Codespaces.

1.  **Activar el entorno virtual:**
    ```bash
    source venv/bin/activate
    ```

2.  **Instalar las dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar el servidor:**
    ```bash
    python run.py
    ```

4.  **Obtener la URL del Backend (¡Importante!):**
    * Una vez que el servidor esté corriendo, ve a la pestaña **"PUERTOS" (PORTS)** en la parte inferior de VS Code.
    * Busca el puerto **5000** (el que dice `python run.py`).
    * Copia la **"Dirección Reenviada" (Forwarded Address)**. La necesitarás para el frontend.
    * *Ejemplo: `https://nombre-aleatorio-5000.app.github.dev`*
