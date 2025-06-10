
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Backtest Estratégias", layout="wide")
st.title("📊 Backtest – INVERT 50, 9-50-20 e PC")

symbol = st.text_input("Ativo", "GER40")
interval = st.selectbox("Tempo gráfico", ["5m", "15m", "1h", "1d"], index=0)
period = st.selectbox("Período", ["1mo", "3mo", "6mo"], index=0)

if st.button("🚀 Rodar Backtest"):
    with st.spinner("Carregando dados e executando estratégias..."):
        data = yf.download(tickers=symbol, interval=interval, period=period)
        df = data.reset_index()
        df.rename(columns={'Datetime': 'datetime'}, inplace=True)
        df['close'] = df['Close']
        df['open'] = df['Open']
        df['high'] = df['High']
        df['low'] = df['Low']

        # Calcular MMEs
        df['mme9'] = df['close'].rolling(9).mean()
        df['mme20'] = df['close'].rolling(20).mean()
        df['mme50'] = df['close'].rolling(50).mean()
        df['mme200'] = df['close'].rolling(200).mean()

        trades = []
        pc_enabled = False  # só habilita PC após um setup válido

        for i in range(200, len(df)):
            row = df.iloc[i]
            prev = df.iloc[i - 1]
            c = df.iloc[i]
            d = c['datetime']

            m9, m20, m50, m200 = c['mme9'], c['mme20'], c['mme50'], c['mme200']
            if not pd.notnull([m9, m20, m50, m200]).all():
                continue

            # INVERT 50
            if m50 > m20 > m9 and c['high'] >= m50 and c['close'] < m20:
                trades.append({'datetime': d, 'setup': 'INVERT 50 SELL', 'entry': c['close'], 'direction': 'sell'})
                pc_enabled = True
                continue
            if m50 < m20 < m9 and c['low'] <= m50 and c['close'] > m20:
                trades.append({'datetime': d, 'setup': 'INVERT 50 BUY', 'entry': c['close'], 'direction': 'buy'})
                pc_enabled = True
                continue

            # 9-50-20
            if (m9 > m50 > m20 or m20 > m50 > m9) and c['low'] <= m50 and c['close'] < m9:
                trades.append({'datetime': d, 'setup': '9-50-20 SELL', 'entry': c['close'], 'direction': 'sell'})
                pc_enabled = True
                continue
            if (m9 < m50 < m20 or m20 < m50 < m9) and c['high'] >= m50 and c['close'] > m9:
                trades.append({'datetime': d, 'setup': '9-50-20 BUY', 'entry': c['close'], 'direction': 'buy'})
                pc_enabled = True
                continue

            # PC
            if pc_enabled:
                if c['close'] < m9 and prev['close'] > prev['mme9']:
                    trades.append({'datetime': d, 'setup': 'PC SELL', 'entry': c['close'], 'direction': 'sell'})
                    pc_enabled = True
                elif c['close'] > m9 and prev['close'] < prev['mme9']:
                    trades.append({'datetime': d, 'setup': 'PC BUY', 'entry': c['close'], 'direction': 'buy'})
                    pc_enabled = True

        trades_df = pd.DataFrame(trades)

        st.success(f"Total de entradas: {len(trades_df)}")
        st.dataframe(trades_df)

        # Gráfico
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df['datetime'], open=df['open'], high=df['high'],
            low=df['low'], close=df['close'], name='Candles'
        ))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['mme9'], mode='lines', name='MME9'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['mme20'], mode='lines', name='MME20'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['mme50'], mode='lines', name='MME50'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['mme200'], mode='lines', name='MME200'))

        for _, row in trades_df.iterrows():
            cor = 'green' if row['direction'] == 'buy' else 'red'
            fig.add_trace(go.Scatter(
                x=[row['datetime']], y=[row['entry']],
                mode='markers+text', marker=dict(color=cor, size=10),
                text=[row['setup']], textposition="top center", name=row['setup']
            ))

        st.plotly_chart(fig, use_container_width=True)
