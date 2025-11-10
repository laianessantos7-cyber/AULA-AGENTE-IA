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
         # menor ou igual a 0.3 mais deterministico
         # entre 0.4 e 0.7 equilibrado para explicação
         # maior que 0.7 mais criativo e menos previsivel.
    )


# Agentes 
agente_resumo= Agent(
    role='Redator de resumo didático.'
    # O que deve fazer.
    goal=(
        'Escrever RESUMO claro e didático sobre {tema} alinhado com o {objetivo}.'
        'A linguagem deve ser didática, direta com contexto prático e sem jargões.'
    ), 
    backtory=' Você transforma temas técnicos/acadêmicos em explicações curtas e precisas.'
    llm= llm, verbose=False
)

agente_exemplos= Agent(
    role= 'Criador de exemplos contextualizados.'
    goal=(
        'Gerar 5 EXEMPLOS CURTOS sobre {tema}, cada um com contexto realista.'
        'Cada exemplo com titulo (em negrito), cénario, dados (se houver), aplicação e resultado.'
    ), 
    backtory=' Você mostra o conceito em ação com exemplos breves e concretos.'
    llm= llm, verbose=False
)
agente_exercicios= Agent(
    role= 'Criador de exercícios práicos.'
    goal=(
        'Criar 4 EXERCÍCIOS SIMPLES sobre {tema}'
        'Variar formato (múltipla escolha, V/F, completar, resolução curta)'
        'Enunciados claros. NÃO incluir respostas'
        
    ), 
    backtory= 'Você cria atividades rápidas que fixam os conceitos essencias',
    llm= llm, verbose=False
)
agente_gabarito
    role= 'Revisor e gabaritador'
    goal=(
        'Ler os EXERCÍCIOS sobre {tema} e produzir o GABARITO oficial, 
        'com respostas corretas e justificativa breve (1-3 frases) por item'
        
    ), 
    backtory= 'Você confere consistência e explica rapidamente o porquê da resposta',
    llm= llm, verbose=False
)
# Tarefas
t_resumo=Task(
    description=(
        'RESUMO: escreva em português do Brasil um resumo didático sobre {tema} e objetivo {objetivo}.'
        'Inclua: definição (3-4 frases), por que importa (2-3), onde se aplica (2-3), e 4-6 ideias-chave,'
        'com marcadores. Formate em Markdown com titulo.'
    ),
    agente=
    expected_output= 'Resumo em Markdown com titulo, paragrafor curtos e 4-6 marcadores (bullets.)'
)

t_exemplos= Task(
    description=(
        'EXEMPLOS: produza 4 exemplos curtos e contextualizados sobre {tema}.'
        'Padrão (até 5 linhas cada): Titulo, cenario, dados/entrada, como aplicar (1-2 frases),resultado'
    ), 
    agent=agente_exemplos,
    expected_output= 'Lista numerada (1-4) em Markdown com exemplos curtos e completos.'
)

t_exercicios= Task(
    description(
        'EXERCICIOS: Crie 4 exercicios simples sobre {tema}em PT-BR.'
        'Varie formatos e não inclua respostas.'
        'Entregue lista numerada (1-4) em Markdown'
    ),
    agent=agente_exercicios,
    expected_output='Lista numerada (1-4) com exercicios simples, sem respostas'

)
t_gabarito= Task(
    description=(
        'GABARITO: Com base nos EXERCICIOS fornecidos no contexto, produza as respostas corretas '
        'Para cada item, dê: \n'
        '- Resposta: (letra, valor, solução) \n'
        '-Comentarios: justificativa breve e direta (1-2 frases), citando o conceito-chave \n'
        'Formato: lista numerada (1 a 3) em Markdown'
    ),
    agent=agente_gabarito,
    expected_output=' Lista numerada (1-3) com resposta e comentario por exercicio.'
    context=[t_exercicios]
)
# Definindo Equipe:
agents= [agente_resumo, agente_exemplos, agente_exercicios, agente_gabarito]
tasks=[t_resumo, t_exemplos, t_exercicios, t_gabarito]
crew= Crew=(
    agents= agents,
    tasks=tasks,
    process= Process.sequential,
)
crew.kickoff(inputs={  
    'tema:'tema,
    'objetivo:'objetivo or 'não informado'
})

# Exibir resultado.
    resumo_out= getattr(t_resumo, "output", None) or  getattr (t_resumo, "result", "") or ""
    exemplo_out= getattr(t_exemplos, "output", None) or  getattr (t_exemplos, "result", "") or ""
    exercicio_out= getattr(t_exercicios, "output", None) or  getattr (t_exercicios, "result", "") or ""
    gabarito_out= getattr(t_gabarito, "output", None) or  getattr (t_gabarito, "result", "") or ""

    # Abas para mostrar os resultados.
    aba_resumo, aba_exemplos, aba_exercicios, aba_gabarito= st.tabs(
        ['Resumo', 'Exemplos', ' Exercicios', ' Gabarito']
    )

    with aba_resumo:
        st.markdown(resumo_out)
    with aba_exemplos:
        st.markdown(exemplo_out)    
    with aba_exercicios:
        st.markdown(exercicio_out)    
    with aba_gabarito:
        st.markdown(gabarito_out)    

