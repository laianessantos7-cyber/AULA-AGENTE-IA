import os 
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

# AGENTES PARA ESTUDO.
st.header('🤖 Agentes para estudo. 📚')
st.write('Informe o tema e gere material para estudar:')


tema = st.text_input('Tema de estudo: ', placeholder=' Ex: Algoritmos')
objetivo= st.text_input('Objetivo:', placeholder='Ex: Entender conceitos. ')

executar= st.button('Gerar material')
api_key= 'CHAVE_API'

if executar:
    llm= LLM(
        model='groq/llma-3.3-70b-versatile',
        api_key=api_key,
        temperature=0.3 
         # Temperature: define o nivel de criatividade 
         # menor ou igual a 00.3 mais deterministico
         # entre 0.4 e 0.7 equilibrado para explicação
         # maior que 0.7 mais criativo e menos previsivel.
    )