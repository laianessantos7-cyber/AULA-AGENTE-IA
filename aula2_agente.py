import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM




st.set_page_config(page_title="LinguAI 🌍", page_icon="🗣️")
st.header("🗣️ LinguAI — Assistente Inteligente de Idiomas")
st.write("Aprenda e pratique idiomas com ajuda de agentes de IA especializados!")

idioma = st.selectbox("Escolha o idioma para estudar:", ["Inglês", "Espanhol", "Francês", "Alemão", "Italiano"])
tema = st.text_input("Tema do estudo", placeholder="Ex.: Verb to be, Present Perfect, False Friends, Saudações")
nivel = st.selectbox("Nível do aluno", ["Iniciante", "Intermediário", "Avançado"])
objetivo = st.text_area("Objetivo (opcional)", placeholder="Ex.: aprender a usar o tempo verbal corretamente em frases do dia a dia.")
mostrar_gabarito = st.toggle("Gerar gabarito e dicas de pronúncia", value=True)

executar = st.button("🎯 Gerar conteúdo")
api_key = 'CHAVE_API'

if executar:
    if not api_key or not tema:
        st.error("Por favor, informe o tema e configure sua API key.")
        st.stop()

   
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.3
    )

    

    agente_teoria = Agent(
        role="Professor(a) de Idiomas",
        goal=(
            "Ensinar o tema {tema} do idioma {idioma} para um aluno de nível {nivel}. "
            "Deve explicar regras, exemplos e variações. Linguagem acessível, "
            "sem jargão técnico e com traduções simples."
        ),
        backstory="Você é um professor de idiomas experiente que transforma tópicos difíceis em explicações simples e envolventes.",
        llm=llm, verbose=False
    )

    agente_exemplos = Agent(
        role="Criador(a) de Exemplos de Conversação",
        goal=(
            "Gerar 4 exemplos curtos e contextualizados sobre {tema} no idioma {idioma}. "
            "Inclua frases originais, tradução e breve explicação de uso."
        ),
        backstory="Você cria exemplos práticos e naturais, simulando situações reais de conversação.",
        llm=llm, verbose=False
    )

    agente_exercicios = Agent(
        role="Autor(a) de Exercícios de Idiomas",
        goal=(
            "Criar 3 exercícios curtos sobre {tema} no idioma {idioma}. "
            "Varie formatos (completar, múltipla escolha, tradução, correção). "
            "Não inclua respostas."
        ),
        backstory="Você cria atividades divertidas e educativas para praticar vocabulário e gramática.",
        llm=llm, verbose=False
    )

    if mostrar_gabarito:
        agente_gabarito = Agent(
            role="Revisor(a) e Instrutor(a) de Pronúncia",
            goal=(
                "Gerar o gabarito dos exercícios e incluir uma dica de pronúncia relacionada ao tema {tema} "
                "no idioma {idioma}. Resposta + breve justificativa + dica de pronúncia."
            ),
            backstory="Você é um professor nativo com excelente didática, que revisa respostas e dá dicas úteis de fala e sotaque.",
            llm=llm, verbose=False
        )

    

    t_teoria = Task(
        description=(
            "EXPLICAÇÃO TEÓRICA\n"
            "Explique o tema {tema} no idioma {idioma} para o nível {nivel}. "
            "Inclua definição, quando usar, exemplos e 3–5 dicas rápidas. "
            "Formate em Markdown, misturando idioma e tradução."
        ),
        agent=agente_teoria,
        expected_output="Texto didático e bem formatado em Markdown."
    )

    t_exemplos = Task(
        description=(
            "EXEMPLOS PRÁTICOS\n"
            "Crie 4 exemplos reais sobre {tema} no idioma {idioma}. "
            "Cada um com: frase original, tradução e nota explicativa (em 1 linha)."
        ),
        agent=agente_exemplos,
        expected_output="Lista numerada (1–4) com exemplos e traduções."
    )

    t_exercicios = Task(
        description=(
            "EXERCÍCIOS\n"
            "Crie 3 exercícios curtos para praticar {tema} no idioma {idioma}. "
            "Não inclua respostas. Formato variado e divertido."
        ),
        agent=agente_exercicios,
        expected_output="Lista numerada (1–3) com enunciados curtos."
    )

    if mostrar_gabarito:
        t_gabarito = Task(
            description=(
                "GABARITO E DICAS\n"
                "Responda aos exercícios 1–3 corretamente. "
                "Para cada um: resposta + justificativa curta + dica de pronúncia."
            ),
            agent=agente_gabarito,
            expected_output="Lista numerada (1–3) com respostas, explicações e dicas de fala.",
            context=[t_exercicios]
        )

    
    agents = [agente_teoria, agente_exemplos, agente_exercicios]
    tasks = [t_teoria, t_exemplos, t_exercicios]
    if mostrar_gabarito:
        agents.append(agente_gabarito)
        tasks.append(t_gabarito)

    crew = Crew(agents=agents, tasks=tasks, process=Process.sequential)

    crew.kickoff(inputs={
        "idioma": idioma,
        "tema": tema,
        "nivel": nivel,
        "objetivo": objetivo or "não informado"
    })

   

    teoria_out = getattr(t_teoria, "output", "")
    exemplos_out = getattr(t_exemplos, "output", "")
    exercicios_out = getattr(t_exercicios, "output", "")
    gabarito_out = getattr(t_gabarito, "output", "") if mostrar_gabarito else ""

    if mostrar_gabarito:
        aba_teoria, aba_exemplos, aba_exercicios, aba_gabarito = st.tabs(
            ["📘 Teoria", "💬 Exemplos", "🧩 Exercícios", "✅ Gabarito e Pronúncia"]
        )
    else:
        aba_teoria, aba_exemplos, aba_exercicios = st.tabs(["📘 Teoria", "💬 Exemplos", "🧩 Exercícios"])

    with aba_teoria:
        st.markdown(teoria_out)
    with aba_exemplos:
        st.markdown(exemplos_out)
    with aba_exercicios:
        st.markdown(exercicios_out)
    if mostrar_gabarito:
        with aba_gabarito:
            st.markdown(gabarito_out)
