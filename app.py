
import streamlit as st
from groq import Groq

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Carro Ideal",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# ESTILO VISUAL
# =====================================================

st.markdown("""
<style>
/* Fundo e texto geral */
.stApp {
    background-color: #0b0b0d;
    color: #f5f5f5;
}

[data-testid="stHeader"] {
    background-color: #0b0b0d;
}

[data-testid="stSidebar"] {
    background-color: #121214;
    border-right: 1px solid #292929;
}

[data-testid="stSidebar"] * {
    color: #eeeeee;
}

/* Cabeçalho */
.hero {
    padding: 30px 10px 24px;
    text-align: center;
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
    color: #d9ad55;
    margin-bottom: 5px;
}

.hero p {
    color: #b9b9b9;
    font-size: 17px;
}

.tag {
    display: inline-block;
    color: #e2bd70;
    border: 1px solid #80652e;
    border-radius: 30px;
    padding: 6px 14px;
    font-size: 12px;
    letter-spacing: 2px;
    margin-bottom: 14px;
}

/* Cartões */
.info-card {
    background: #151517;
    border: 1px solid #292929;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
    min-height: 105px;
}

.info-card h4 {
    color: #d9ad55;
    margin-bottom: 8px;
}

.info-card p {
    color: #c8c8c8;
    font-size: 14px;
}

/* Mensagens */
[data-testid="stChatMessage"] {
    background-color: #151517;
    border: 1px solid #282828;
    border-radius: 14px;
    padding: 12px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #f1f1f1;
}

/* BARRA DE PERGUNTAS */
[data-testid="stChatInput"] {
    background-color: #151517 !important;
    border: 1px solid #80652e !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

/* Área onde o usuário digita */
[data-testid="stChatInput"] textarea,
.stChatInput textarea {
    background-color: #151517 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #d9ad55 !important;
    border: none !important;
    box-shadow: none !important;
}

/* Texto de exemplo */
[data-testid="stChatInput"] textarea::placeholder,
.stChatInput textarea::placeholder {
    color: #a7a7a7 !important;
    -webkit-text-fill-color: #a7a7a7 !important;
    opacity: 1 !important;
}

/* Evita fundo claro ao focar */
[data-testid="stChatInput"]:focus-within {
    border-color: #d9ad55 !important;
    box-shadow: 0 0 0 1px #d9ad55 !important;
}

/* Botões */
.stButton button {
    background-color: #c9a04b;
    color: #111111;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

.stButton button:hover {
    background-color: #e0bb69;
    color: #111111;
}

/* Campos adicionais */
[data-testid="stTextInput"] input {
    background-color: #202024 !important;
    color: #ffffff !important;
    border-color: #454545 !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #a7a7a7 !important;
}

/* Divisórias */
hr {
    border-color: #292929;
}

/* Rodapé */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# INSTRUÇÕES DO CONSULTOR
# =====================================================

SYSTEM_PROMPT = """
Você é o Carro Ideal, um consultor automotivo experiente,
educado, criterioso e especialista em ajudar pessoas a escolher
o veículo mais adequado às suas necessidades.

MISSÃO:
"O melhor carro a você diante de suas necessidades."

COMO VOCÊ DEVE ATENDER:

1. Entenda a rotina, as necessidades e as condições financeiras
do cliente antes de recomendar um veículo.

2. Faça perguntas naturais e objetivas, uma ou duas por vez.
Não transforme a conversa em um interrogatório.

3. Descubra, quando relevante:
- Orçamento disponível.
- Compra à vista ou financiamento.
- Uso urbano, rodoviário ou misto.
- Quilometragem diária aproximada.
- Número de passageiros.
- Necessidade de porta-malas.
- Tipo de carro preferido.
- Câmbio manual ou automático.
- Prioridades como economia, conforto, segurança e desempenho.
- Preferência por usado ou zero-quilômetro.
- Região onde pretende comprar.

4. Adapte as perguntas às respostas anteriores. Não pergunte
novamente algo que o cliente já informou.

5. Quando tiver informações suficientes, apresente até três
opções e explique:
- Por que cada veículo combina com o cliente.
- Vantagens e desvantagens.
- Consumo e manutenção, quando houver dados confiáveis.
- Custos que merecem atenção.
- Qual opção você escolheria e por quê.

6. Considere o custo total de propriedade: compra, combustível,
seguro, impostos, manutenção e possíveis reparos.

7. Nunca invente preços atuais, estoque, anúncios, quilometragem,
dados técnicos ou especificações. Você não tem acesso automático
a anúncios em tempo real. Avise quando uma informação precisar
ser confirmada.

8. Os valores e custos variam por ano, versão, região, conservação
e condições de uso. Diferencie fatos de estimativas.

9. Se faltar informação importante, faça perguntas. Se não souber,
admita com honestidade e indique como confirmar.

10. Fale em português brasileiro, com educação, clareza e detalhes
suficientes para ajudar na decisão.

11. Não pressione o cliente a comprar. Sua prioridade é encontrar
uma opção adequada à realidade dele.

12. Mantenha o contexto da conversa.

Comece se apresentando brevemente e perguntando qual é a principal
necessidade do cliente ao procurar um carro.
"""

# =====================================================
# HISTÓRICO INICIAL
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Olá! Seja bem-vindo ao **Carro Ideal**. 🚘\n\n"
                "Vou ajudar você a encontrar um carro que combine "
                "com sua rotina, seu orçamento e suas prioridades.\n\n"
                "**Para começarmos: o que você mais precisa em um "
                "carro e quanto pretende investir?**"
            ),
        }
    ]

# =====================================================
# BARRA LATERAL
# =====================================================

with st.sidebar:
    st.markdown("## 🚘 Carro Ideal")
    st.caption("Seu consultor automotivo pessoal")

    st.divider()

    st.markdown("### Configuração")
    st.caption("Insira sua chave da Groq para ativar o consultor.")

    api_key = st.text_input(
        "Chave da API Groq",
        type="password",
        placeholder="Cole sua chave aqui",
        help="A chave é usada para conectar o aplicativo à Groq.",
    )

    if api_key.strip():
        st.success("Chave inserida nesta sessão.")
    else:
        st.info("Insira sua chave para começar.")

    st.divider()

    st.markdown("### O que posso fazer?")
    st.markdown("""
    - Encontrar um carro para sua rotina.
    - Comparar modelos.
    - Avaliar custos de manutenção.
    - Ajudar a escolher entre usado e zero-quilômetro.
    - Explicar vantagens e desvantagens.
    """)

    st.divider()

    if st.button("🗑️ Nova conversa", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Olá! Seja bem-vindo ao **Carro Ideal**. 🚘\n\n"
                    "Para começarmos: o que você mais precisa em um "
                    "carro e quanto pretende investir?"
                ),
            }
        ]
        st.rerun()

    st.caption("Carro Ideal • Consultoria automotiva")

# =====================================================
# CABEÇALHO
# =====================================================

st.markdown("""
<div class="hero">
    <div class="tag">CONSULTORIA AUTOMOTIVA</div>
    <h1>Carro Ideal</h1>
    <p>O melhor carro a você diante de suas necessidades.</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# CARTÕES
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>🎯 Escolha inteligente</h4>
        <p>Recomendações orientadas pela sua rotina e prioridades.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>💰 Seu orçamento</h4>
        <p>Considere o preço, o combustível e a manutenção.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>🤝 Transparência</h4>
        <p>Compare opções e conheça as limitações antes de decidir.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================================
# EXIBIÇÃO DAS MENSAGENS
# =====================================================

for message in st.session_state.messages:
    avatar = "🚘" if message["role"] == "assistant" else "👤"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# =====================================================
# ENTRADA E RESPOSTA DA GROQ
# =====================================================

pergunta = st.chat_input(
    "Conte o que você precisa em um carro..."
)

if pergunta:
    if not api_key.strip():
        st.warning(
            "Insira sua chave da Groq na barra lateral antes de enviar."
        )
        st.stop()

    # Registra e exibe a pergunta
    st.session_state.messages.append({
        "role": "user",
        "content": pergunta,
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(pergunta)

    with st.chat_message("assistant", avatar="🚘"):
        try:
            client = Groq(api_key=api_key.strip())

            with st.spinner("Analisando suas necessidades..."):
                resposta = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT,
                        },
                        *st.session_state.messages,
                    ],
                    temperature=0.5,
                    max_tokens=1500,
                )

                texto = resposta.choices[0].message.content

                if not texto:
                    texto = (
                        "Não consegui formular uma resposta agora. "
                        "Pode tentar enviar sua pergunta novamente?"
                    )

            st.markdown(texto)

            st.session_state.messages.append({
                "role": "assistant",
                "content": texto,
            })

        except Exception as erro:
            # Retira a última pergunta para não duplicar
            # a mensagem quando o usuário tentar novamente.
            if (
                st.session_state.messages
                and st.session_state.messages[-1]["role"] == "user"
                and st.session_state.messages[-1]["content"] == pergunta
            ):
                st.session_state.messages.pop()

            st.error(
                "Não foi possível conectar à Groq. Verifique sua chave, "
                "a conexão com a internet e a disponibilidade do modelo."
            )

            with st.expander("Detalhes técnicos do erro"):
                st.code(str(erro))
