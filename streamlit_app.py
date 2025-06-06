import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime

st.set_page_config(page_title="Backtest Inteligente", layout="wide")
st.markdown("""
    <style>
        body { background-color: #f0f2f6; }
        .main { background-color: #ffffff; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h1, h2, h3 { color: #333333; }
        .stButton>button {
            background-color: #0e76a8;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
        .stTextArea textarea, .stSelectbox, .stMultiselect, .stDateInput, .stFileUploader {
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Backtester de Estratégias Personalizadas")
