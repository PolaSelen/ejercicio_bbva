# ejercicio_bbva

Sistema de chat inteligente (RAG) diseñado para consultar información de productos financieros de BBVA.

## Stack Tecnológico
- Python, Streamlit, LangChain, ChromaDB, Ollama (Llama 3.2), Playwright.

## Pipeline de Datos
1. **Scraping**: `scraper.py` extrae datos actualizados de BBVA.
2. **Vectorización**: `vectorizar.py` procesa el texto para búsquedas semánticas.
3. **Interfaz**: `app.py` gestiona el chatbot con historial y memoria.

## Instrucciones de uso
1. Instalar Ollama y descargar modelos: `nomic-embed-text` y `llama3.2`.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Ejecutar: `streamlit run app.py`.
