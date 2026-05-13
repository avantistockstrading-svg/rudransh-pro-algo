import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="RUDRANSH PRO-ALGO", layout="wide")

st.title("📈 RUDRANSH PRO-ALGO")
st.markdown("### Live Trading Signals")

# Symbols
SYMBOLS = {
    "NIFTY": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "CRUDEOIL": "CL=F",
    "NATURALGAS": "NG=F"
}

# Sidebar
with st.sidebar:
    st.markdown("## 🚀 CONTROL")
    
    if st.button("▶️ START"):
        st.session_state.running = True
        st.success("Started!")
    
    if st.button("🛑 STOP"):
        st.session_state.running = False
        st.warning("Stopped!")
    
    st.markdown("---")
    market = st.selectbox("Select Asset", list(SYMBOLS.keys()))

# Get data
df = yf.download(SYMBOLS[market], period="2d", interval="5m", progress=False)

if not df.empty:
    # Calculate indicators manually (without pandas_ta)
    close = df['Close']
    
    # EMA 9 and EMA 20
    df['EMA9'] = close.ewm(span=9, adjust=False).mean()
    df['EMA20'] = close.ewm(span=20, adjust=False).mean()
    
    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    current = close.iloc[-1]
    ema20 = df['EMA20'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    
    # Signal logic
    if current > ema20 and rsi < 70:
        signal = "🔵 BUY"
        sl = current - 15
    elif current < ema20 and rsi > 30:
        signal = "🔴 SELL"
        sl = current + 15
    else:
        signal = "⚪ WAIT"
        sl = 0
    
    # Display
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Price", f"₹{current:.2f}")
    col2.metric("Signal", signal)
    col3.metric("RSI", f"{rsi:.1f}")
    col4.metric("Stop Loss", f"₹{sl:.2f}" if sl else "N/A")
    
    # Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=market, line=dict(color='#00ff88', width=2)))
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Status
    if st.session_state.get('running', False):
        st.success("🟢 ALGO IS RUNNING")
    else:
        st.warning("🔴 ALGO IS STOPPED")

st.caption("🔄 Auto Refresh Every 10 Seconds")
st_autorefresh(interval=10000, key="refresh")
