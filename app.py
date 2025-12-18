import streamlit as st
from supabase import create_client
from datetime import datetime

# Conexão com Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_API_KEY"]
supabase = create_client(url, key)

st.title("📋 Registro de Estatísticas da Pelada")

# Carrega os dados dos dropdowns
jogadores_data = supabase.table("jogadores").select("nome").execute().data
times_data = supabase.table("times").select("time").execute().data
partidas_data = supabase.table("partidas").select("data_partida").order("data_partida", desc=True).execute().data

# Converte os dados em listas para os dropdowns
jogadores = [j["nome"] for j in jogadores_data]
times = [t["time"] for t in times_data]
datas = [p["data_partida"][:10] for p in partidas_data]  # Pega só a parte da data

# Formulário
with st.form("form_estatisticas"):
    jogador = st.selectbox("👤 Jogador", jogadores)
    time = st.selectbox("🏳️ Time", times)
    data_partida = st.selectbox("📅 Data da Partida", datas)
    gols_marcados = st.number_input("⚽ Gols Marcados", min_value=0, step=1)
    gols_sofridos = st.number_input("🥅 Gols Sofridos", min_value=0, step=1)

    submitted = st.form_submit_button("Registrar")

    if submitted:
        response = supabase.table("estatisticas").insert({
            "jogador": jogador_id,
            "time": time_id,
            "data": partida_id,
            "gols_marcados": gols_marcados,
            "gols_sofridos": gols_sofridos
        }).execute()

        if response.status_code == 201:
            st.success("✅ Estatísticas registradas com sucesso!")
        else:
            st.error("❌ Erro ao registrar estatísticas.")
            st.json(response)

