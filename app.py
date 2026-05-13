import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Configura tu llave directamente aquí para la prueba
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

st.title("🤖 Mi Chatbot con Gemini")

# 1. Inicializar la memoria y el modelo SOLO UNA VEZ
if "chatbot" not in st.session_state:
    st.session_state.memoria = ConversationBufferMemory()
    
    # IMPORTANTE: Usa el nombre del modelo que te funcionó en el paso anterior
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    st.session_state.chatbot = ConversationChain(
        llm=llm, 
        memory=st.session_state.memoria,
        verbose=False
    )
    # Historial visual para Streamlit
    st.session_state.mensajes_ui = []

# 2. Mostrar el historial en la pantalla
for mensaje in st.session_state.mensajes_ui:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

# 3. Caja de texto para el usuario
pregunta = st.chat_input("Escribe tu mensaje aquí...")

if pregunta:
    # Guardar y mostrar lo que escribió el usuario
    st.session_state.mensajes_ui.append({"rol": "user", "contenido": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Obtener respuesta de Gemini usando la memoria de LangChain
    respuesta = st.session_state.chatbot.predict(input=pregunta)

    # Guardar y mostrar la respuesta de la IA
    st.session_state.mensajes_ui.append({"rol": "assistant", "contenido": respuesta})
    with st.chat_message("assistant"):
        st.markdown(respuesta)
