import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Backtest Inteligente", layout="wide")
st.title("📊 Backtester de Estratégias Personalizadas")

# Upload do CSV
data_file = st.file_uploader("📁 Faça o upload do seu arquivo CSV com os dados históricos:", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)
    st.success("✅ Arquivo carregado com sucesso!")

    st.subheader("🔍 Pré-visualização dos Dados")
    st.dataframe(df.head())

    # Seleção de estratégia
    st.subheader("⚙️ Escolha o Setup para Backtest")
    setup = st.selectbox("Selecione o setup:", ["INVERT 50", "9-50-20", "PC"])

    if st.button("🚀 Executar Backtest"):
        st.info(f"Executando backtest com o setup: {setup}")

        if "setup" in df.columns:
            df_filtrado = df[df["setup"] == setup]

            total_trades = len(df_filtrado)
            wins = len(df_filtrado[df_filtrado["resultado"] == "win"]) if "resultado" in df_filtrado.columns else 0
            losses = len(df_filtrado[df_filtrado["resultado"] == "loss"]) if "resultado" in df_filtrado.columns else 0
            breakeven = len(df_filtrado[df_filtrado["resultado"] == "be"]) if "resultado" in df_filtrado.columns else 0
            taxa_acerto = (wins / total_trades * 100) if total_trades > 0 else 0
            rr = df_filtrado["rr"].mean() if "rr" in df_filtrado.columns else 0
            lucro_total = df_filtrado["lucro"].sum() if "lucro" in df_filtrado.columns else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("🎯 Total de Operações", f"{total_trades}", f"Win: {wins} | Loss: {losses} | BE: {breakeven}")
            col2.metric("📈 Taxa de Acerto", f"{taxa_acerto:.2f}%")
            col3.metric("💰 Resultado Total", f"R$ {lucro_total:,.2f}")

            col4, col5 = st.columns(2)
            col4.metric("📊 R/R Médio", f"{rr:.2f}")
            col5.metric("📅 Período Analisado", f"{df_filtrado['data'].min()} até {df_filtrado['data'].max()}")

            st.markdown("---")
            st.subheader("📋 Detalhes das Operações")
            st.dataframe(df_filtrado.reset_index(drop=True))

            if "lucro" in df_filtrado.columns and "data" in df_filtrado.columns:
                st.subheader("📈 Gráfico de Resultados Diários")
                df_lucro_diario = df_filtrado.groupby("data")["lucro"].sum().reset_index()
                fig = px.bar(df_lucro_diario, x="data", y="lucro", title="Resultado Diário")
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🗓️ Diário de Trade")

    selected_date = st.date_input("Selecione uma data para registrar observações:", date.today())
    note_key = f"note_{selected_date}"
    note = st.text_area("Observações para o dia selecionado:", value=st.session_state.get(note_key, ""))

    if st.button("💾 Salvar Observação"):
        st.session_state[note_key] = note
        st.success("Anotação salva com sucesso!")

    if st.session_state.get(note_key):
        st.info(f"📌 Observação salva para {selected_date}: {st.session_state[note_key]}")
else:
    st.warning("⚠️ Faça o upload de um arquivo CSV para começar.")
