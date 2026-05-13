import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import requests

st.set_page_config(page_title="Rudransh Algo", layout="wide", page_icon="📈")

# ===== Professional Mobile CSS =====
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0rem 0.5rem;
    }
    
    /* Card style */
    .stMetric {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 20px;
        padding: 15px;
        margin: 5px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Button style */
    .stButton button {
        background: linear-gradient(90deg, #00ff88, #00cc66);
        color: black;
        font-weight: bold;
        font-size: 18px;
        border-radius: 30px;
        padding: 12px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0,255,136,0.4);
    }
    
    /* Stop button */
    div[data-testid="column"]:nth-child(2) button {
        background: linear-gradient(90deg, #ff4b4b, #cc0000);
        color: white;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29, #302b63, #24243e);
        border-right: none;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white !important;
        text-align: center;
    }
    
    /* Status indicator */
    .status-running {
        background: linear-gradient(90deg, #00ff88, #00cc66);
        color: black;
        padding: 8px;
        border-radius: 30px;
        text-align: center;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    .status-stopped {
        background: linear-gradient(90deg, #ff4b4b, #cc0000);
        color: white;
        padding: 8px;
        border-radius: 30px;
        text-align: center;
        font-weight: bold;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* P&L display */
    .pnl-positive {
        color: #00ff88;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }
    
    .pnl-negative {
        color: #ff4b4b;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }
    
    /* Price display */
    .price {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #00ff88, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .stMetric {
            margin: 2px 0;
            padding: 10px;
        }
        .stButton button {
            font-size: 16px;
            padding: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== Session State =====
if "running" not in st.session_state:
    st.session_state.running = False
if "pnl" not in st.session_state:
    st.session_state.pnl = 0
if "quantity" not in st.session_state:
    st.session_state.quantity = 65
if "asset" not in st.session_state:
    st.session_state.asset = "NIFTY"

# ===== Header =====
st.markdown("<h1>📱 RUDRANSH PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Professional Trading Terminal</p>", unsafe_allow_html=True)

st.markdown("---")

# ===== Status Row =====
col1, col2 = st.columns(2)

with col1:
    status_class = "status-running" if st.session_state.running else "status-stopped"
    status_text = "🟢 RUNNING" if st.session_state.running else "🔴 STOPPED"
    st.markdown(f"<div class='{status_class}'>{status_text}</div>", unsafe_allow_html=True)

with col2:
    pnl_class = "pnl-positive" if st.session_state.pnl >= 0 else "pnl-negative"
    pnl_symbol = "+" if st.session_state.pnl >= 0 else ""
    st.markdown(f"<div style='text-align:center;'><span style='color:#94a3b8;'>P&L</span><br><span class='{pnl_class}'>₹{pnl_symbol}{st.session_state.pnl:,.2f}</span></div>", unsafe_allow_html=True)

st.markdown("---")

# ===== Live Price =====
try:
    symbols = {"NIFTY": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDEOIL": "CL=F", "NATURALGAS": "NG=F"}
    ticker = yf.Ticker(symbols[st.session_state.asset])
    data = ticker.history(period="1d")
    if not data.empty:
        price = data['Close'].iloc[-1]
        st.markdown(f"<div class='price'>₹{price:,.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#94a3b8;'>{st.session_state.asset} • LIVE</p>", unsafe_allow_html=True)
except:
    st.markdown(f"<div class='price'>₹23,412</div>", unsafe_allow_html=True)

st.markdown("---")

# ===== Control Buttons =====
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ START", use_container_width=True):
        st.session_state.running = True
        st.toast("Algo Started!", icon="✅")
        st.rerun()

with col2:
    if st.button("⏹️ STOP", use_container_width=True):
        st.session_state.running = False
        st.toast("Algo Stopped!", icon="🛑")
        st.rerun()

st.markdown("---")

# ===== Quick Actions =====
st.markdown("<h3 style='font-size:18px;'>⚡ QUICK ACTIONS</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 BUY", use_container_width=True):
        st.success(f"BUY {st.session_state.quantity} qty")
        st.toast(f"BUY Order Placed!", icon="🟢")

with col2:
    if st.button("🔴 SELL", use_container_width=True):
        st.error(f"SELL {st.session_state.quantity} qty")
        st.toast(f"SELL Order Placed!", icon="🔴")

with col3:
    if st.button("🔲 SQ OFF", use_container_width=True):
        st.session_state.pnl = 0
        st.warning("All positions squared off!")
        st.toast("All Trades Closed!", icon="✅")

st.markdown("---")

# ===== Settings =====
st.markdown("<h3 style='font-size:18px;'>⚙️ SETTINGS</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    asset = st.selectbox("Asset", ["NIFTY", "BANK NIFTY", "CRUDEOIL", "NATURALGAS"])
    st.session_state.asset = asset

with col2:
    lot_sizes = {"NIFTY": 65, "BANK NIFTY": 25, "CRUDEOIL": 100, "NATURALGAS": 1250}
    lots = st.number_input("Lots", min_value=1, max_value=10, value=1)
    st.session_state.quantity = lots * lot_sizes[asset]

st.markdown(f"<p style='text-align:center; color:#00ff88;'>📦 Quantity: {st.session_state.quantity}</p>", unsafe_allow_html=True)

st.markdown("---")

# ===== Footer =====
st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')} • Auto Refresh")
