import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import time

st.set_page_config(page_title="Rudransh Pro-Algo", layout="wide")

st.markdown("""
<style>
.main { padding: 0rem 0.5rem; }
.stButton button { background: linear-gradient(90deg, #00ff88, #00cc66); color: black; font-weight: bold; border-radius: 30px; padding: 12px; width: 100%; border: none; }
div[data-testid="column"]:nth-child(2) button { background: linear-gradient(90deg, #ff4b4b, #cc0000); color: white; }
.status-running { background: #00ff88; color: black; padding: 8px; border-radius: 30px; text-align: center; font-weight: bold; }
.status-stopped { background: #ff4b4b; color: white; padding: 8px; border-radius: 30px; text-align: center; font-weight: bold; }
.pnl-positive { color: #00ff88; font-size: 24px; font-weight: bold; text-align: center; }
.pnl-negative { color: #ff4b4b; font-size: 24px; font-weight: bold; text-align: center; }
.price { font-size: 32px; font-weight: bold; text-align: center; background: linear-gradient(90deg, #00ff88, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
""", unsafe_allow_html=True)

# Session State
if "running" not in st.session_state:
    st.session_state.running = False
if "pnl" not in st.session_state:
    st.session_state.pnl = 0
if "quantity" not in st.session_state:
    st.session_state.quantity = 65
if "asset" not in st.session_state:
    st.session_state.asset = "NIFTY"
if "signal" not in st.session_state:
    st.session_state.signal = "WAIT"

st.markdown("<h1>📱 RUDRANSH PRO-ALGO</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## 🎮 CONTROLS")
    
    if st.button("▶️ START", use_container_width=True):
        st.session_state.running = True
    if st.button("⏹️ STOP", use_container_width=True):
        st.session_state.running = False
    
    st.markdown("---")
    
    asset = st.selectbox("Asset", ["NIFTY", "CRUDEOIL", "NATURALGAS"])
    st.session_state.asset = asset
    
    lot_sizes = {"NIFTY": 65, "CRUDEOIL": 100, "NATURALGAS": 1250}
    lots = st.number_input("Lots", min_value=1, max_value=10, value=1)
    st.session_state.quantity = lots * lot_sizes[asset]

# Status Row
col1, col2 = st.columns(2)
with col1:
    if st.session_state.running:
        st.markdown("<div class='status-running'>🟢 RUNNING</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-stopped'>🔴 STOPPED</div>", unsafe_allow_html=True)
with col2:
    color = "pnl-positive" if st.session_state.pnl >= 0 else "pnl-negative"
    st.markdown(f"<div style='text-align:center;'>P&L<br><span class='{color}'>₹{st.session_state.pnl:,.0f}</span></div>", unsafe_allow_html=True)

st.markdown("---")

# Try to get live price
price = 23500
try:
    symbols = {"NIFTY": "^NSEI", "CRUDEOIL": "CL=F", "NATURALGAS": "NG=F"}
    df = yf.download(symbols[asset], period="1d", progress=False)
    if not df.empty and 'Close' in df.columns:
        price = df['Close'].iloc[-1]
except:
    pass

st.markdown(f"<div class='price'>₹{price:,.2f}</div>", unsafe_allow_html=True)

st.markdown("---")

# Signal Logic (Simple)
if st.session_state.running:
    # Demo signal - in real market, signal will come from calculations
    if datetime.now().second % 30 < 15:
        signal = "BUY"
    else:
        signal = "WAIT"
    st.session_state.signal = signal
else:
    st.session_state.signal = "WAIT"

# Display Signal
col1, col2, col3, col4 = st.columns(4)
col1.metric("Price", f"₹{price:,.2f}")
col2.metric("Signal", st.session_state.signal)
col3.metric("Quantity", st.session_state.quantity)
col4.metric("Asset", asset)

st.markdown("---")

# Control Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 BUY", use_container_width=True):
        st.success(f"BUY {st.session_state.quantity} qty")
        st.session_state.pnl += 500
with col2:
    if st.button("🔴 SELL", use_container_width=True):
        st.error(f"SELL {st.session_state.quantity} qty")
        st.session_state.pnl -= 500
with col3:
    if st.button("🔲 SQ OFF", use_container_width=True):
        st.session_state.pnl = 0
        st.warning("Squared off!")

st.markdown("---")

# Auto Trade (Demo)
if st.session_state.running and st.session_state.signal == "BUY":
    st.success("🚀 AUTO BUY EXECUTED")
    st.balloons()

# Market Hours
now = datetime.now()
if asset == "NIFTY":
    if 9 <= now.hour <= 15:
        st.info("🟢 Market OPEN | 9:30 AM - 3:30 PM")
    else:
        st.info("⏸️ Market CLOSED")
else:
    if 18 <= now.hour <= 23:
        st.info("🟢 Market OPEN | 6:00 PM - 11:00 PM")
    else:
        st.info("⏸️ Market CLOSED")

st.caption(f"🕐 {now.strftime('%H:%M:%S')} | Auto Refresh")
time.sleep(1)
st.rerun()
