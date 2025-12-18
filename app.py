import streamlit as st
from supabase import create_client
from datetime import datetime

# Conexão com Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_API_KEY"]
supabase = create_client(url, key)

st.title("📋 Registro de Estatísticas da Pelada")

# Carrega os dados dos dropdowns
jogadores_data = supabase.table("jogadores").select("id, nome").execute().data
times_data = supabase.table("times").select("id, time").execute().data
partidas_data = supabase.table("partidas").select("id, data_partida").order("data_partida", desc=True).execute().data

# Dropdowns
jogador_nome_para_id = {j["nome"]: j["id"] for j in jogadores_data}
time_nome_para_id = {t["time"]: t["id"] for t in times_data}
data_str_para_id = {p["data_partida"][:10]: p["id"] for p in partidas_data}

jogadores = list(jogador_nome_para_id.keys())
times = list(time_nome_para_id.keys())
datas = list(data_str_para_id.keys())

# Formulário
with st.form("form_estatisticas"):
    jogador_nome = st.selectbox("👤 Jogador", jogadores)
    time_nome = st.selectbox("🏳️ Time", times)
    data_str = st.selectbox("📅 Data da Partida", datas)
    gols_marcados = st.number_input("⚽ Gols Marcados", min_value=0, step=1)
    gols_sofridos = st.number_input("🥅 Gols Sofridos", min_value=0, step=1)

    submitted = st.form_submit_button("Registrar")

    if submitted:
        jogador_id = jogador_nome_para_id[jogador_nome]
        time_id = time_nome_para_id[time_nome]
        partida_id = data_str_para_id[data_str]

        try:
            response = supabase.table("estatisticas").insert({
                "jogador_id": jogador_id,
                "time_id": time_id,
                "partida_id": partida_id,
                "gols_marcados": gols_marcados,
                "gols_sofridos": gols_sofridos
            }).execute()
            st.success("✅ Estatísticas registradas com sucesso!")

        except Exception as e:
            st.error("❌ Erro ao registrar estatísticas. Verifique se o jogador já foi registrado para esta partida.")
            st.exception(e)
