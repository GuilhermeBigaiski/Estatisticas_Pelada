import streamlit as st
from supabase import create_client
from datetime import datetime

# Conexão com Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_API_KEY"]
supabase = create_client(url, key)

st.title("📋 Registro de Estatísticas da Pelada")

# Carrega os dados dos dropdowns com ID
jogadores_data = supabase.table("jogadores").select("id, nome").execute().data
times_data = supabase.table("times").select("id, time").execute().data
partidas_data = supabase.table("partidas").select("id, data_partida").order("data_partida", desc=True).execute().data

# Cria dicionários {nome: id}
jogadores_dict = {j["nome"]: j["id"] for j in jogadores_data}
times_dict = {t["time"]: t["id"] for t in times_data}
datas_dict = {p["data_partida"][:10]: p["id"] for p in partidas_data}

# Converte os dados em listas para os dropdowns
jogadores = list(jogadores_dict.keys())
times = list(times_dict.keys())
datas = list(datas_dict.keys())

# Formulário
with st.form("form_estatisticas"):
    jogador_nome = st.selectbox("👤 Jogador", jogadores)
    time_nome = st.selectbox("🏳️ Time", times)
    data_partida = st.selectbox("📅 Data da Partida", datas)
    gols_marcados = st.number_input("⚽ Gols Marcados", min_value=0, step=1)
    gols_sofridos = st.number_input("🥅 Gols Sofridos", min_value=0, step=1)

    submitted = st.form_submit_button("Registrar")

    if submitted:
        # Recupera os IDs
        jogador_id = jogadores_dict[jogador_nome]
        time_id = times_dict[time_nome]
        partida_id = datas_dict[data_partida]

        # Tenta inserir os dados na tabela estatisticas
        try:
            response = supabase.table("estatisticas").insert({
                "jogador_id": jogador_id,
                "time_id": time_id,
                "partida_id": partida_id,
                "gols_marcados": gols_marcados,
                "gols_sofridos": gols_sofridos
            }).execute()

            if response.data:
    st.success("✅ Estatísticas registradas com sucesso!")
else:
    st.error("❌ Erro ao registrar estatísticas.")
    st.write("Detalhes do erro:")
    st.json(response.error)

        except Exception as e:
            st.error("❌ Erro na inserção:")
            st.exception(e)

