import streamlit as st
import psycopg2
from psycopg2.pool import SimpleConnectionPool

# ----------- POOL DE CONEXÕES ----------- #
@st.cache_resource
def get_pool():
    return SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        host="aws-1-us-east-2.pooler.supabase.com",
        database="postgres",
        user="postgres.xcogxppribxdhehmcdlb",
        password=st.secrets["db_password"],
        port=5432,
        sslmode="require"
    )

def run_query(query, params=None, fetch=True):
    pool = get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            result = cur.fetchall() if fetch else None
            conn.commit()
            return result
    finally:
        pool.putconn(conn)


# ----------- INTERFACE STREAMLIT ----------- #
st.title("📊 Registro de Estatísticas da Pelada")

# Partidas
partidas = run_query("SELECT id, data_partida FROM partidas ORDER BY data_partida DESC")
partida_escolhida = st.selectbox("Selecione a partida:", partidas, format_func=lambda x: x[1].strftime("%d/%m/%Y"))

# Jogadores
jogadores = run_query("SELECT id, nome FROM jogadores ORDER BY nome")
jogador_escolhido = st.selectbox("Selecione o jogador:", jogadores, format_func=lambda x: x[1])

# Times
times = run_query("SELECT id, time FROM times ORDER BY time")
time_escolhido = st.selectbox("Selecione o time:", times, format_func=lambda x: x[1])

# Estatísticas
gols_marcados = st.number_input("Gols marcados:", min_value=0)
gols_sofridos = st.number_input("Gols sofridos (somente goleiro):", min_value=0)

# Botão
if st.button("Registrar Estatística"):
    existe = run_query(
        "SELECT 1 FROM estatisticas WHERE partida_id = %s AND jogador_id = %s",
        (partida_escolhida[0], jogador_escolhido[0])
    )

    if existe:
        st.error("❌ Já existe uma estatística para esse jogador nesta partida!")
    else:
        run_query(
            """
            INSERT INTO estatisticas (partida_id, jogador_id, time_id, gols_marcados, gols_sofridos)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (partida_escolhida[0], jogador_escolhido[0], time_escolhido[0], gols_marcados, gols_sofridos),
            fetch=False
        )
        st.success("✅ Estatística registrada com sucesso!")
