import streamlit as st
import psycopg2
import os

# Configurações iniciais
st.set_page_config(page_title="Registro de Estatísticas", layout="centered")

# Conexão com o Supabase (PostgreSQL)
@st.cache_resource
def connect_db():
    return psycopg2.connect(
        host=os.getenv("SUPABASE_HOST"),
        dbname=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        port="5432"
    )

conn = connect_db()
cur = conn.cursor()

# Título
st.title("📊 Registro de Estatísticas da Pelada")

# Formulário
with st.form("form_estatisticas"):
    data_partida = st.date_input("Data da pelada")
    jogador = st.text_input("Nome do jogador")
    time = st.selectbox("Time", ["Time 1", "Time 2"])
    gols_feitos = st.number_input("Gols feitos", min_value=0, step=1)
    eh_goleiro = st.checkbox("É goleiro?")
    
    gols_sofridos = 0
    if eh_goleiro:
        gols_sofridos = st.number_input("Gols sofridos", min_value=0, step=1)
    
    submitted = st.form_submit_button("Registrar")

# Envio ao banco
if submitted:
    try:
        cur.execute("""
            INSERT INTO estatisticas (data_partida, jogador, time, gols_feitos, gols_sofridos)
            VALUES (%s, %s, %s, %s, %s)
        """, (data_partida, jogador, time, gols_feitos, gols_sofridos))
        conn.commit()
        st.success("Estatística registrada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao registrar: {e}")
