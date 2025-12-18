import streamlit as st
from datetime import date
import requests
import os

# URL da Supabase (substitua pela sua)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]

def inserir_dados(data, nome, time, gols, sofreu_gols):
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "data": data.isoformat(),
        "jogador": nome,
        "time": time,
        "gols": gols,
        "gols_sofridos": sofreu_gols if sofreu_gols else None
    }

    response = requests.post(f"{SUPABASE_URL}/rest/v1/estatisticas", json=payload, headers=headers)
    return response.status_code == 201

st.set_page_config(page_title="Registro de Estatísticas", page_icon="⚽", layout="centered")

st.title("📊 Formulário - Estatísticas da Pelada")

with st.form("formulario_estatisticas"):
    data = st.date_input("Data da pelada", value=date.today())
    nome = st.text_input("Nome do jogador")
    time = st.selectbox("Time", ["Time 1", "Time 2"])
    gols = st.number_input("Gols marcados", min_value=0, step=1)

    eh_goleiro = st.checkbox("É goleiro?")
    sofreu_gols = None
    if eh_goleiro:
        sofreu_gols = st.number_input("Gols sofridos", min_value=0, step=1)

    submit = st.form_submit_button("Enviar")

    if submit:
        sucesso = inserir_dados(data, nome, time, gols, sofreu_gols)
        if sucesso:
            st.success("✅ Dados enviados com sucesso!")
        else:
            st.error("❌ Erro ao enviar os dados. Verifique os campos e tente novamente.")