import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# Conexão com Supabase
SUPABASE_URL = "https://SEU_PROJECT_ID.supabase.co"
SUPABASE_API_KEY = "SUA_API_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

st.title("Pelada")

# 1. Buscar dados para os dropdowns
datas_response = supabase.table("partidas").select("data_partida").execute()
jogadores_response = supabase.table("jogadores").select("nome").execute()
times_response = supabase.table("times").select("time").execute()

datas = sorted(set([d["data_partida"] for d in datas_response.data]))
jogadores = [j["nome"] for j in jogadores_response.data]
times = [t["time"] for t in times_response.data]

# Formulário
with st.form("registro_pelada"):
    data_pelada = st.selectbox("Data da pelada", datas)
    nome_jogador = st.selectbox("Nome do jogador", jogadores)
    time = st.selectbox("Time", times)
    
    tipo_jogador = st.selectbox("Tipo de jogador", ["Jogador de linha", "Goleiro"])
    
    if tipo_jogador == "Jogador de linha":
        gols = st.number_input("Gols marcados", min_value=0, step=1)
        gols_sofridos = None
    else:
        gols_sofridos = st.number_input("Gols sofridos", min_value=0, step=1)
        gols = None

    submit = st.form_submit_button("Enviar")

    if submit:
        registro = {
            "data": data_pelada,
            "nome": nome_jogador,
            "time": time,
            "gols": gols,
            "gols_sofridos": gols_sofridos,
            "tipo_jogador": tipo_jogador
        }

        # Insere na tabela do Supabase (ajuste o nome da tabela)
        supabase.table("estatisticas").insert(registro).execute()

        st.success("Registro enviado com sucesso!")

