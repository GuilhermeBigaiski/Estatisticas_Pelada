import streamlit as st
from sqlalchemy import create_engine, text
from datetime import date

# ---------------------------
#  POOL DE CONEXÕES / ENGINE
# ---------------------------
@st.cache_resource
def get_engine():
    """
    Cria e retorna uma engine SQLAlchemy com pg8000
    """
    return create_engine(
        f"postgresql+pg8000://postgres.xcogxppribxdhehmcdlb:{st.secrets['db_password']}@aws-1-us-east-2.pooler.supabase.com:5432/postgres"
    )

def run_query(query, params=None, fetch=True):
    """
    Executa query SQL com parâmetros opcionais.
    Retorna resultado se fetch=True, senão apenas executa.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        if fetch:
            return result.fetchall()
        return None


# ---------------------------
#        INTERFACE
# ---------------------------
st.title("💰 Registro Financeiro")

# ---- TIPOS (mensalidade, receita, despesa) ----
tipos = run_query("SELECT id, tipo FROM fin_tipo ORDER BY tipo")
tipo_escolhido = st.selectbox(
    "Selecione o tipo:",
    tipos,
    format_func=lambda x: x[1]
)
tipo_nome = tipo_escolhido[1].lower()  # Para lógica abaixo

# ---- Inicializa variáveis de insert ----
descricao_id = None
jogador_id = None

# ---- Se for DESPESA ou RECEITA → mostrar descrição ----
if tipo_nome in ["despesa", "receita"]:
    descricoes = run_query("SELECT id, descricao FROM fin_descricao ORDER BY descricao")
    desc_escolhida = st.selectbox(
        "Selecione a descrição:",
        descricoes,
        format_func=lambda x: x[1]
    )
    descricao_id = desc_escolhida[0]

# ---- Se for MENSALIDADE → mostrar dropdown de jogador ----
if tipo_nome == "mensalidade":
    jogadores = run_query("SELECT id, nome FROM jogadores ORDER BY nome")
    jogador_escolhido = st.selectbox(
        "Selecione o jogador:",
        jogadores,
        format_func=lambda x: x[1]
    )
    jogador_id = jogador_escolhido[0]

# ---- Data ----
data_registro = st.date_input("Data:", value=date.today())

# ---- Valor ----
valor = st.number_input("Valor (R$):", min_value=0.0, step=0.01, format="%.2f")

# ---- Botão ENVIAR ----
if st.button("Registrar"):

    if valor <= 0:
        st.error("⚠ Valor inválido.")
        st.stop()

    # Inserir no financeiro
    run_query(
        """
        INSERT INTO financeiro (tipo_id, descricao_id, jogador_id, data, valor)
        VALUES (:tipo_id, :descricao_id, :jogador_id, :data, :valor)
        """,
        {
            "tipo_id": tipo_escolhido[0],
            "descricao_id": descricao_id,
            "jogador_id": jogador_id,
            "data": data_registro,
            "valor": valor
        },
        fetch=False
    )

    st.success("✅ Registro inserido com sucesso!")
