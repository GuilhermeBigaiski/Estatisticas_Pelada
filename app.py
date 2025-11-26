import streamlit as st
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from datetime import datetime

# 1. POOL DE CONEXÃO COM CACHE
@st.cache_resource
def get_connection_pool():
    return SimpleConnectionPool(
        minconn=1,
        maxconn=4,  # reduzido para aliviar Supabase
        host="aws-1-us-east-2.pooler.supabase.com",
        database="postgres",
        user="postgres.xcogxppribxdhehmcdlb",
        password=st.secrets["db_password"],
        port=5432,
        sslmode="require"
    )

def run_query(query, params=None, fetch=True):
    pool = get_connection_pool()
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            if fetch:
                result = cur.fetchall()
            else:
                result = None
            conn.commit()
    finally:
        pool.putconn(conn)
    return result

# 2. UI
st.set_page_config(page_title="📊 Estatísticas da Pelada")
st.title("📊 Registro de Estatísticas da Pelada")

# 3. CACHES DE DADOS ESTÁTICOS
@st.cache_data
def carregar_dados():
    partidas = run_query("SELECT id, data_partida FROM partidas ORDER BY data_partida DESC")
    jogadores = run_query("SELECT id, nome, posicao FROM jogadores ORDER BY nome")
    times = run_query("SELECT id, time FROM times ORDER BY time")
    return partidas, jogadores, times

partidas, jogadores, times = carregar_dados()

# 4. FORMULÁRIO
with st.form("form_estatisticas"):

    partida_escolhida = st.selectbox(
        "Selecione a data da pelada:",
        partidas,
        format_func=lambda x: x[1].strftime("%d/%m/%Y")
    )

    jogador_escolhido = st.selectbox(
        "Selecione o jogador:",
        jogadores,
        format_func=lambda x: x[1]
    )

    time_escolhido = st.selectbox(
        "Selecione o time:",
        times,
        format_func=lambda x: x[1]
    )

    gols_marcados = st.number_input("Gols marcados:", min_value=0)

    is_goleiro = jogador_escolhido[2].strip().lower() == "goleiro"
    if is_goleiro:
        gols_sofridos = st.number_input("Gols sofridos:", min_value=0)
    else:
        gols_sofridos = 0  # não preenche nada no campo se não for goleiro

    submitted = st.form_submit_button("✅ Registrar Estatística")

# 5. PROCESSAMENTO
if submitted:
    partida_id = partida_escolhida[0]
    jogador_id = jogador_escolhido[0]
    time_id = time_escolhido[0]

    # Checa duplicidade
    existe = run_query(
        "SELECT 1 FROM estatisticas WHERE partida_id = %s AND jogador_id = %s",
        (partida_id, jogador_id)
    )

    if existe:
        st.warning("⚠️ Já existe estatística registrada para esse jogador nesta pelada.")
    else:
        run_query("""
            INSERT INTO estatisticas (partida_id, jogador_id, time_id, gols_marcados, gols_sofridos)
            VALUES (%s, %s, %s, %s, %s)
        """, (partida_id, jogador_id, time_id, gols_marcados, gols_sofridos), fetch=False)

        st.success("✅ Estatística registrada com sucesso!")
