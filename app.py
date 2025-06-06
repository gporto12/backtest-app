
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# CONFIG
st.set_page_config(page_title="Backtest Dashboard", layout="wide")

# ESTILO MODERNO COM CSS
st.markdown("""
    <style>
        .main {
            background-color: #0f1117;
            color: #FFFFFF;
        }
        h1, h2, h3, h4, h5 {
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #1E88E5;
            color: white;
            padding: 0.5em 1em;
            border-radius: 8px;
        }
        .stFileUploader, .stDataFrame {
            border-radius: 10px;
        }
        .metric-box {
            background-color: #1c1f26;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .metric-box h3 {
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

# TÍTULO
st.title("📊 Backtest Dashboard")

# UPLOAD
data_file = st.file_uploader("📁 Upload do arquivo CSV", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)

    st.markdown("### 📈 Gráfico de Fechamento")
    if "datetime" in df.columns and "close" in df.columns:
        fig = px.line(df, x="datetime", y="close", title="", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Métricas do Backtest")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Lucro Total", f"${df['lucro'].sum():,.2f}" if "lucro" in df.columns else "N/A")
    col2.metric("✅ Win Rate", f"{(len(df[df['resultado']=='win']) / len(df) * 100):.2f}%" if "resultado" in df.columns else "N/A")
    col3.metric("📈 R/R Médio", f"{df['rr'].mean():.2f}" if "rr" in df.columns else "N/A")

    st.markdown("### 🗓️ Calendário de Trades (datas únicas)")
    if "data" in df.columns:
        unique_dates = sorted(df["data"].dropna().unique())
        st.write(", ".join(map(str, unique_dates)))

    st.markdown("### 🧾 Tabela de Operações")
    st.dataframe(df, use_container_width=True)

else:
    st.info("⚠️ Faça o upload de um CSV com colunas como 'datetime', 'close', 'lucro', 'resultado', 'rr', etc.")
