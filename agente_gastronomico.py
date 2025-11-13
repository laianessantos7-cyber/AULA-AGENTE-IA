import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM



st.set_page_config(page_title="ChefAI 🍳", page_icon="👨‍🍳")
st.header("👨‍🍳 ChefAI — Seu Assistente Culinário Inteligente")
st.write("Descubra, aprenda e prepare receitas incríveis criadas por agentes de IA!")

prato = st.text_input("Nome da receita ou ingrediente principal", placeholder="Ex.: Lasanha de frango, Risoto de cogumelos, Brownie")
cozinha = st.selectbox("Tipo de culinária (opcional)", ["Não especificar", "Italiana", "Brasileira", "Japonesa", "Mexicana", "Francesa", "Vegana"])
nivel = st.selectbox("Nível de dificuldade", ["Fácil", "Médio", "Avançado"])
porcoes = st.number_input("Número de porções", min_value=1, max_value=20, value=4)
mostrar_harmonizacao = st.toggle("Gerar harmonizações (bebidas, acompanhamentos, etc.)", value=True)

executar = st.button("🍴 Gerar Receita")
api_key = "SUA_CHAVE_API"

if executar:
    if not api_key or not prato:
        st.error("Por favor, informe o nome da receita e configure sua API key.")
        st.stop()

    
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.4
    )

    

    agente_contexto = Agent(
        role="Historiador(a) Gastronômico(a)",
        goal=(
            "Apresentar o prato {prato}, sua origem ou contexto cultural, "
            "e o motivo de ser uma boa escolha para {nivel}. "
            "Estilo leve, curioso e inspirador."
        ),
        backstory="Você é um amante da gastronomia que adora contar histórias sobre os pratos e ingredientes.",
        llm=llm, verbose=False
    )

    agente_receita = Agent(
        role="Chef Profissional",
        goal=(
            "Escrever uma receita detalhada de {prato}, com ingredientes, quantidades e modo de preparo "
            "passo a passo, adequada a {porcoes} porções e nível {nivel}."
        ),
        backstory="Você é um chef renomado que explica receitas com precisão e clareza.",
        llm=llm, verbose=False
    )

    agente_dicas = Agent(
        role="Consultor(a) Culinário(a)",
        goal=(
            "Gerar 3–5 dicas extras e variações criativas para a receita {prato}, "
            "considerando possíveis substituições de ingredientes, adaptações para dietas e truques de sabor."
        ),
        backstory="Você é um consultor de cozinha criativo que sempre tem boas ideias para aprimorar receitas.",
        llm=llm, verbose=False
    )

    if mostrar_harmonizacao:
        agente_harmonizacao = Agent(
            role="Sommelier e Harmonizador(a)",
            goal=(
                "Gerar sugestões de bebidas, acompanhamentos e sobremesas que harmonizam bem com {prato}. "
                "Inclua 1–2 bebidas, 1 acompanhamento e 1 sobremesa compatível."
            ),
            backstory="Você é um sommelier experiente com paladar apurado, que entende combinações de sabores.",
            llm=llm, verbose=False
        )

    

    t_contexto = Task(
        description=(
            "INTRODUÇÃO CULINÁRIA\n"
            "Explique a origem ou contexto do prato {prato}. "
            "Conte curiosidades e o porquê de ser interessante para o público de nível {nivel}. "
            "Tom envolvente e convidativo, em até 150 palavras."
        ),
        agent=agente_contexto,
        expected_output="Texto introdutório com curiosidades e contexto cultural."
    )

    t_receita = Task(
        description=(
            "RECEITA DETALHADA\n"
            "Liste os ingredientes com quantidades para {porcoes} porções, "
            "seguido do modo de preparo numerado, com passos curtos e claros. "
            "Formato Markdown."
        ),
        agent=agente_receita,
        expected_output="Receita completa com ingredientes e modo de preparo formatados."
    )

    t_dicas = Task(
        description=(
            "DICAS E VARIAÇÕES\n"
            "Forneça de 3 a 5 dicas curtas sobre como melhorar, variar ou adaptar a receita {prato}. "
            "Inclua ideias para versões vegetarianas, rápidas ou gourmet."
        ),
        agent=agente_dicas,
        expected_output="Lista de dicas em Markdown, numerada (1–5)."
    )

    if mostrar_harmonizacao:
        t_harmonizacao = Task(
            description=(
                "HARMONIZAÇÕES\n"
                "Sugira 1–2 bebidas, 1 acompanhamento e 1 sobremesa que combinem com {prato}. "
                "Inclua breve justificativa de cada sugestão."
            ),
            agent=agente_harmonizacao,
            expected_output="Lista organizada por categoria (bebidas, acompanhamento, sobremesa)."
        )


    

    agentes = [agente_contexto, agente_receita, agente_dicas]
    tarefas = [t_contexto, t_receita, t_dicas]
    if mostrar_harmonizacao:
        agentes.append(agente_harmonizacao)
        tarefas.append(t_harmonizacao)

    crew = Crew(agents=agentes, tasks=tarefas, process=Process.sequential)

    crew.kickoff(inputs={
        "prato": prato,
        "cozinha": cozinha,
        "nivel": nivel,
        "porcoes": porcoes
    })

    
    contexto_out = getattr(t_contexto, "output", "")
    receita_out = getattr(t_receita, "output", "")
    dicas_out = getattr(t_dicas, "output", "")
    harmonizacao_out = getattr(t_harmonizacao, "output", "") if mostrar_harmonizacao else ""

    if mostrar_harmonizacao:
        aba_intro, aba_receita, aba_dicas, aba_harmonizacao = st.tabs(
            ["🍽️ Introdução", "📋 Receita", "💡 Dicas", "🍷 Harmonizações"]
        )
    else:
        aba_intro, aba_receita, aba_dicas = st.tabs(["🍽️ Introdução", "📋 Receita", "💡 Dicas"])

    with aba_intro:
        st.markdown(contexto_out)
    with aba_receita:
        st.markdown(receita_out)
    with aba_dicas:
        st.markdown(dicas_out)
    if mostrar_harmonizacao:
        with aba_harmonizacao:
            st.markdown(harmonizacao_out)
