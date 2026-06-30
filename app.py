import os
import streamlit as st
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM

st.set_page_config(page_title="Asistente BBVA", layout="centered")
st.title("Asistente Conversacional BBVA")

# 1. Configurar conexión a la BD y LLM
embeddings = OllamaEmbeddings(model="nomic-embed-text")
base_datos = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
llm = OllamaLLM(model="llama3.2")

# Historial
if "historial" not in st.session_state:
    st.session_state.historial = []

for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Lógica de Respuesta Real
if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    with st.chat_message("user"):
        st.write(pregunta)
    st.session_state.historial.append({"role": "user", "content": pregunta})
    
    with st.chat_message("assistant"):
        with st.spinner("Consultando base de datos..."):
            # Búsqueda de similitud en tu chroma_db
            docs = base_datos.similarity_search(pregunta, k=3)
            contexto = "\n".join([d.page_content for d in docs])
            
            # Prompt para el LLM
            prompt = f"""
            Eres un asistente especializado en productos de BBVA Colombia.
            Utiliza EXCLUSIVAMENTE el siguiente contexto para responder. Si la información no está en el contexto, di: 'Lo siento, no encontré información sobre eso en los productos de BBVA'.
            
            CONTEXTO:
            {contexto}
            
            PREGUNTA DEL CLIENTE:
            {pregunta}
            """
            
            respuesta = llm.invoke(prompt)
            st.write(respuesta)
            
    st.session_state.historial.append({"role": "assistant", "content": respuesta})
