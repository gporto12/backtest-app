import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Backtest Dashboard", layout="wide")

# Custom CSS for dashboard style
st.markdown("""
    <style>
        body {
            background-color: #0d1117;
            color: white;
        }
        .stApp {
            background-color: #0d1117;
        }
        .css-1v0mbdj, .css-18ni7ap, .css-1cpxqw2 {
            background-color: #161b22 !important;
            border-radius: 10px;
            padding: 1rem;
            color: white;
        }
        .stButton>button {
            background-color: #238636;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Backtest Dashboard")

uploaded_file = st.file_uploader("📁 Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Arquivo carregado com sucesso!")

    st.subheader("📈 Gráfico de Preço")
    if "datetime" in df.columns and "close" in df.columns:
        fig = px.line(df, x="datetime", y="close", title="Preço de Fechamento", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Métricas de Performance")
    col1, col2, col3 = st.columns(3)
    lucro_total = df["lucro"].sum() if "lucro" in df.columns else 0
    win_rate = (len(df[df["resultado"] == "win"]) / len(df) * 100) if "resultado" in df.columns else 0
    rr = df["rr"].mean() if "rr" in df.columns else 0

    col1.metric("💰 Lucro Total", f"R$ {lucro_total:,.2f}")
    col2.metric("🎯 Win Rate", f"{win_rate:.2f}%")
    col3.metric("⚖️ R/R Médio", f"{rr:.2f}")

    st.subheader("📋 Histórico de Operações")
    st.dataframe(df, use_container_width=True)
else:
    st.info("👆 Faça upload de um arquivo CSV para começar.")