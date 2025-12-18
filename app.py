import streamlit as st
import psycopg2
from datetime import date

# Função para conectar ao banco apenas uma vez
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="db.XXXX.supabase.co",
        dbname="postgres",
        user="seu_usuario",
        password="sua_senha",
        port="5432"
    )

# Título
st.title("Registro de Estatísticas da Pelada")

# Formulário
with st.form("estatisticas_form"):
    data_pelada = st.date_input("Data da pelada", value=date.today())
    nome_jogador = st.text_input("Nome do jogador")
    time = st.text_input("Time")
    gols_feitos = st.number_input("Gols feitos", min_value=0, step=1)
    eh_goleiro = st.checkbox("Jogador é goleiro?")
    gols_sofridos = st.number_input("Gols sofridos", min_value=0, step=1) if eh_goleiro else 0

    submitted = st.form_submit_button("Enviar")

    if submitted:
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO estatisticas (data_pelada, nome_jogador, time, gols_feitos, gols_sofridos)
                VALUES (%s, %s, %s, %s, %s)
            """, (data_pelada, nome_jogador, time, gols_feitos, gols_sofridos))

            conn.commit()
            cur.close()
            st.success("Estatísticas registradas com sucesso!")

        except Exception as e:
            st.error(f"Erro ao inserir no banco: {e}")