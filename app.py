import streamlit as st
import psycopg2
from psycopg2.pool import SimpleConnectionPool

# ---------------------------
#  POOL DE CONEXÕES OTIMIZADO
# ---------------------------
@st.cache_resource
def get_pool():
    try:
        return SimpleConnectionPool(
            minconn=1,
            maxconn=5,  # limite ideal para Supabase Free + Streamlit
            host="aws-1-us-east-2.pooler.supabase.com",
            database="postgres",
            user="postgres.xcogxppribxdhehmcdlb",
            password=st.secrets["db_password"],
            port=5432,
            sslmode='require'
        )
    except Exception as e:
        st.error(f"Erro ao criar pool de conexões: {e}")
        st.stop()


# ---------------------------
#  EXECUTAR CONSULTAS SQL
# ---------------------------
def run_query(query, params=None, fetch=True):
    try:
        pool = get_pool()
        conn = pool.getconn()
        cur = conn.cursor()

        cur.execute(query, params or ())

        data = cur.fetchall() if fetch else None
        conn.commit()

        cur.close()
        pool.putconn(conn)

        return data

    except Exception as e:
        st.error(f"Erro ao executar consulta: {e}")
        return None


# ---------------------------
#  INTERFACE STREAMLIT
# ---------------------------
st.title("📊 Registro de Estatísticas da Pelada")


# Buscar dados apenas 1 vez — economia de conexões ✅
partidas = run_query("SELECT id, data_partida FROM partidas ORDER BY data_partida DESC")
jogadores = run_query("SELECT id, nome FROM jogadores ORDER BY nome")
times = run_query("SELECT id, time FROM times ORDER BY time")

# Se algo falhar, interrompe app
if not partidas or not jogadores or not times:
    st.error("Erro ao carregar dados do banco. Tente novamente mais tarde.")
    st.stop()


# ---------------------------
#  FORMULÁRIO OTIMIZADO ✅
# ---------------------------
with st.form("estatisticas_form"):
    partida_escolhida = st.selectbox(
        "Selecione a partida:",
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
    gols_sofridos = st.number_input("Gols sofridos (somente goleiro):", min_value=0)

    enviar = st.form_submit_button("Registrar Estatística ✅")


# ---------------------------
#  PROCESSAR ENVIO
# ---------------------------
if enviar:

    # Verificar duplicidade — evita erro e economiza conexão ✅
    existe = run_query(
        "SELECT 1 FROM estatisticas WHERE partida_id=%s AND jogador_id=%s",
        (partida_escolhida[0], jogador_escolhido[0])
    )

    if existe:
        st.warning("⚠️ Já existe uma estatística para esse jogador nesta partida!")
        st.stop()

    # Inserir dado
    run_query(
        """
        INSERT INTO estatisticas (partida_id, jogador_id, time_id, gols_marcados, gols_sofridos)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (partida_escolhida[0], jogador_escolhido[0], time_escolhido[0], gols_marcados, gols_sofridos),
        fetch=False
    )

    st.success("✅ Estatística registrada com sucesso!")
    st.balloons()