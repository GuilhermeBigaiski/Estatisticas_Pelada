import streamlit as st
from supabase import create_client, Client

# Conexão segura com Supabase via Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

st.title("Pelada")

# Buscar dados
datas = supabase.table("partidas").select("id, data_partida").execute().data
jogadores = supabase.table("jogadores").select("id, nome").execute().data
times = supabase.table("times").select("id, time").execute().data

# Dropdowns
partida = st.selectbox(
    "Data da pelada",
    datas,
    format_func=lambda x: x["data_partida"]
)

jogador = st.selectbox(
    "Nome do jogador",
    jogadores,
    format_func=lambda x: x["nome"]
)

time = st.selectbox(
    "Time",
    times,
    format_func=lambda x: x["time"]
)

tipo = st.radio("Tipo de jogador", ["Linha", "Goleiro"])

if tipo == "Linha":
    gols_marcados = st.number_input("Gols marcados", min_value=0)
    gols_sofridos = 0
else:
    gols_sofridos = st.number_input("Gols sofridos", min_value=0)
    gols_marcados = 0

if st.button("Salvar"):
    supabase.table("estatisticas").insert({
        "partida_id": partida["id"],
        "jogador_id": jogador["id"],
        "time_id": time["id"],
        "gols_marcados": gols_marcados,
        "gols_sofridos": gols_sofridos
    }).execute()

    st.success("Registro salvo com sucesso!")
