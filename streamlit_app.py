import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Backtest Inteligente", layout="wide")

st.markdown("""
    <style>
        body { background-color: #f7f9fb; }
        .main { background-color: #ffffff; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        h1, h2, h3, h4 { color: #1a1a1a; }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 6px;
            padding: 0.4em 1.2em;
            border: none;
            font-weight: bold;
        }
        .stSelectbox, .stTextArea textarea, .stDateInput, .stFileUploader {
            border-radius: 8px;
            font-size: 1rem;
        }
        .stMetric-value { font-size: 1.8rem; color: #007bff; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Backtest Inteligente de Estratégias")
...
