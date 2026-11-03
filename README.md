# Ejecutar y presentar el proyecto

Usar Python 3.12 o 3.13. Desde la carpeta de este proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-modelos.txt
$env:PYTHONHASHSEED = '0'
.\.venv\Scripts\python.exe extraer_abstracts.py
.\.venv\Scripts\python.exe matrices.py
.\.venv\Scripts\python.exe demos.py
.\.venv\Scripts\python.exe experimento_r3.py
.\.venv\Scripts\python.exe dendrogramas.py
.\.venv\Scripts\python.exe graficar_r3.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

La primera generación de Sentence-BERT necesita Internet para descargar el modelo. La aplicación consulta las matrices guardadas; no requiere cargar los modelos de IA para mostrar resultados. Ejecutar desde la raíz. `extraer_metadatos.py` usa el manifiesto revisado para conservar coautores.

- [Documento técnico](docs/DOCUMENTO_TECNICO.md): arquitectura, fórmulas, variables, complejidad y limitaciones.
- [Casos reales](docs/CASOS_REALES.md): resultados completos y ejemplos pequeños paso a paso.
- [Guía de sustentación](docs/SUSTENTACION.md).
- [Verificación](docs/VERIFICACION.md).
- [Declaración de IA para revisar](docs/APOYO_IA.md).

## Despliegue reproducible

1. Revisar los cambios y subir el repositorio con corpus, matrices, `resultados/procedencia.json` y vectores. No subir `.venv`, `.deps` ni cachés.
2. En un servicio compatible con Streamlit, conectar el repositorio y seleccionar `app.py`, con Python compatible. Instalar `requirements.txt`; los modelos no son necesarios para servir resultados precalculados.
3. En un servidor propio: `python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501`. Configurar el proxy y acceso público del servidor.
4. Abrir la URL desde otro equipo: comprobar Corpus (artículos 7 y 9), selección de varios artículos en R1, los tres enlaces en R2 y búsqueda en R3. Registrar URL, fecha y pruebas en `docs/VERIFICACION.md`.

Estado de despliegue: pendiente de verificar URL pública. No se afirma que esté desplegada.
