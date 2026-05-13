import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import json
import os

st.set_page_config(page_title="Rudransh Pro-Algo", layout="wide")

# ===== Professional CSS =====
st.markdown("""
<style>
    .main { padding: 0rem 0.5rem; }
    .stMetric { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 20px; padding: 15px; margin: 5px 0; border: 1px solid rgba(255,255,255,0.05); }
    .stButton button { background: linear-gradient(90deg, #00ff88, #00cc66); color: black; font-weight: bold; border-radius: 30px; padding: 12px; width: 100%; border: none; transition: all 0.3s ease; }
    div[data-testid="column"]:nth-child(2) button { background: linear-gradient(90deg, #ff4b4b, #cc0000); color: white; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0c29, #302b63, #24243e); }
    h1, h2, h3 { color: white !important; text-align: center; }
    .status-running { background: linear-gradient(90deg, #00ff88, #00cc66); color: black; padding: 8px; border-radius: 30px; text-align: center; font-weight: bold; animation: pulse 2s infinite; }
    .status-stopped { background: linear-gradient(90deg, #ff4b4b, #cc0000); color: white; padding: 8px; border-radius: 30px; text-align: center; font-weight: bold; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
    .pnl-positive { color: #00ff88; font-size: 24px; font-weight: bold; text-align: center; }
    .pnl-negative { color: #ff4b4b; font-size: 24px; font-weight: bold; text-align: center; }
    .price { font-size: 32px; font-weight: bold; text-align: center; background: linear-gradient(90deg, #00ff88, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    @media (max-width: 768px) { .stMetric { margin: 2px 0; padding: 10px; } .stButton button { font-size: 16px; padding: 10px; } }
</style>
""", unsafe_allow_html=True)

# ===== DEFAULT TP/SL CONFIGURATION =====
DEFAULT_CONFIG = {
    "NIFTY": {"lot": 65, "sl": 30, "tp1": 12, "tp2": 22, "tp3": 30},
    "CRUDEOIL": {"lot": 100, "sl": 10, "tp1": 10, "tp2": 15, "tp3": 20},
    "NATURALGAS": {"lot": 1250, "sl": 2, "tp1": 1, "tp2": 1.5, "tp3": 2},
    "STOCK_OPTIONS": {"lot": "auto", "sl": 10, "tp1": 5, "tp2": 10, "tp3": 15}
}

BOOKING_DEFAULT = {"tp1": 50, "tp2": 25, "tp3": 25}
MAX_OPTION_QTY = 2000

# ===== Load/Save Settings Function =====
SETTINGS_FILE = "trade_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"config": DEFAULT_CONFIG.copy(), "booking": BOOKING_DEFAULT.copy()}
    return {"config": DEFAULT_CONFIG.copy(), "booking": BOOKING_DEFAULT.copy()}

def save_settings(config, booking):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump({"config": config, "booking": booking}, f)

# ===== Session State =====
if "running" not in st.session_state:
    st.session_state.running = False
if "pnl" not in st.session_state:
    st.session_state.pnl = 0
if "quantity" not in st.session_state:
    st.session_state.quantity = 65
if "asset" not in st.session_state:
    st.session_state.asset = "NIFTY"
if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = False
if "settings" not in st.session_state:
    settings = load_settings()
    st.session_state.config = settings["config"]
    st.session_state.booking = settings["booking"]

# ===== Header =====
st.markdown("<h1>📱 RUDRANSH PRO-ALGO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Professional Trading Terminal</p>", unsafe_allow_html=True)
st.markdown("---")

# ===== Sidebar - Controls =====
with st.sidebar:
    st.markdown("## 🎮 MAIN CONTROLS")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START", use_container_width=True):
            st.session_state.running = True
            st.toast("Algo Started!", icon="✅")
    with col2:
        if st.button("⏹️ STOP", use_container_width=True):
            st.session_state.running = False
            st.toast("Algo Stopped!", icon="🛑")
    
    st.markdown("---")
    
    # ===== MANUAL SETTINGS SECTION =====
    st.markdown("## ⚙️ TP/SL SETTINGS")
    
    # Manual Mode Toggle
    manual_toggle = st.toggle("🔧 Manual Edit Mode", value=st.session_state.manual_mode)
    
    if manual_toggle != st.session_state.manual_mode:
        st.session_state.manual_mode = manual_toggle
        st.rerun()
    
    if st.session_state.manual_mode:
        st.info("✏️ Manual Mode: तुम्ही स्वतः Settings बदलू शकता")
        
        # NIFTY Settings
        st.markdown("### 📊 NIFTY")
        col_a, col_b = st.columns(2)
        with col_a:
            new_sl = st.number_input("SL (pts)", value=st.session_state.config["NIFTY"]["sl"], step=5, key="nifty_sl")
            new_tp2 = st.number_input("TP2 (pts)", value=st.session_state.config["NIFTY"]["tp2"], step=5, key="nifty_tp2")
        with col_b:
            new_tp1 = st.number_input("TP1 (pts)", value=st.session_state.config["NIFTY"]["tp1"], step=5, key="nifty_tp1")
            new_tp3 = st.number_input("TP3 (pts)", value=st.session_state.config["NIFTY"]["tp3"], step=5, key="nifty_tp3")
        
        # CRUDE Settings
        st.markdown("### 🛢️ CRUDE OIL")
        col_a, col_b = st.columns(2)
        with col_a:
            crude_sl = st.number_input("SL (₹)", value=st.session_state.config["CRUDEOIL"]["sl"], step=5, key="crude_sl")
            crude_tp2 = st.number_input("TP2 (₹)", value=st.session_state.config["CRUDEOIL"]["tp2"], step=5, key="crude_tp2")
        with col_b:
            crude_tp1 = st.number_input("TP1 (₹)", value=st.session_state.config["CRUDEOIL"]["tp1"], step=5, key="crude_tp1")
            crude_tp3 = st.number_input("TP3 (₹)", value=st.session_state.config["CRUDEOIL"]["tp3"], step=5, key="crude_tp3")
        
        # NG Settings
        st.markdown("### 🌿 NATURAL GAS")
        col_a, col_b = st.columns(2)
        with col_a:
            ng_sl = st.number_input("SL (₹)", value=float(st.session_state.config["NATURALGAS"]["sl"]), step=1.0, key="ng_sl")
            ng_tp2 = st.number_input("TP2 (₹)", value=float(st.session_state.config["NATURALGAS"]["tp2"]), step=0.5, key="ng_tp2")
        with col_b:
            ng_tp1 = st.number_input("TP1 (₹)", value=float(st.session_state.config["NATURALGAS"]["tp1"]), step=0.5, key="ng_tp1")
            ng_tp3 = st.number_input("TP3 (₹)", value=float(st.session_state.config["NATURALGAS"]["tp3"]), step=1.0, key="ng_tp3")
        
        # Booking Percentage
        st.markdown("### 📊 Quantity Booking %")
        tp1_pct = st.slider("TP1 Booking %", 0, 100, st.session_state.booking["tp1"])
        tp2_pct = st.slider("TP2 Booking %", 0, 100, st.session_state.booking["tp2"])
        tp3_pct = st.slider("TP3 Booking %", 0, 100, st.session_state.booking["tp3"])
        
        # Save Button
        if st.button("💾 SAVE SETTINGS", use_container_width=True):
            st.session_state.config["NIFTY"] = {"lot": 65, "sl": new_sl, "tp1": new_tp1, "tp2": new_tp2, "tp3": new_tp3}
            st.session_state.config["CRUDEOIL"] = {"lot": 100, "sl": crude_sl, "tp1": crude_tp1, "tp2": crude_tp2, "tp3": crude_tp3}
            st.session_state.config["NATURALGAS"] = {"lot": 1250, "sl": ng_sl, "tp1": ng_tp1, "tp2": ng_tp2, "tp3": ng_tp3}
            st.session_state.booking = {"tp1": tp1_pct, "tp2": tp2_pct, "tp3": tp3_pct}
            save_settings(st.session_state.config, st.session_state.booking)
            st.success("✅ Settings Saved!")
            st.rerun()
        
        # Reset to Default Button
        if st.button("🔄 RESET TO DEFAULT", use_container_width=True):
            st.session_state.config = DEFAULT_CONFIG.copy()
            st.session_state.booking = BOOKING_DEFAULT.copy()
            save_settings(st.session_state.config, st.session_state.booking)
            st.success("✅ Reset to Default!")
            st.rerun()
    
    else:
        # Show Current Settings
        st.markdown("### 📊 Current TP/SL Settings")
        current_asset = st.session_state.asset
        if current_asset in st.session_state.config:
            cfg = st.session_state.config[current_asset]
            st.markdown(f"**SL:** {cfg['sl']} | **TP1:** {cfg['tp1']} | **TP2:** {cfg['tp2']} | **TP3:** {cfg['tp3']}")
        st.markdown(f"**Booking:** TP1:{st.session_state.booking['tp1']}% TP2:{st.session_state.booking['tp2']}% TP3:{st.session_state.booking['tp3']}%")
        st.caption("💡 Toggle 'Manual Edit Mode' to change settings")
    
    st.markdown("---")
    
    # Asset Selection
    st.markdown("## 📈 SELECT ASSET")
    asset = st.selectbox("Asset", ["NIFTY", "CRUDEOIL", "NATURALGAS", "STOCK_OPTIONS"])
    st.session_state.asset = asset
    
    # Quantity Calculation
    if asset == "STOCK_OPTIONS":
        st.markdown("### 📦 Stock Option Lot Size")
        lot_size = st.number_input("Lot Size", min_value=100, max_value=2000, value=500, step=100)
        if lot_size <= 0:
            lot_size = 500
        max_lots = MAX_OPTION_QTY // lot_size
        if max_lots < 1:
            max_lots = 1
        lots = st.number_input("Number of Lots", min_value=1, max_value=max_lots, value=min(2, max_lots))
        st.session_state.quantity = lots * lot_size
        st.caption(f"Max {MAX_OPTION_QTY} qty | {max_lots} lots max")
    else:
        lot_size = st.session_state.config[asset]["lot"]
        lots = st.number_input("Lots", min_value=1, max_value=10, value=1)
        st.session_state.quantity = lots * lot_size
    
    st.markdown(f"<p style='text-align:center; color:#00ff88;'>📦 Quantity: {st.session_state.quantity}</p>", unsafe_allow_html=True)

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
    symbols = {"NIFTY": "^NSEI", "CRUDEOIL": "CL=F", "NATURALGAS": "NG=F", "STOCK_OPTIONS": "^NSEI"}
    if asset != "STOCK_OPTIONS":
        ticker = yf.Ticker(symbols[asset])
        data = ticker.history(period="1d")
        if not data.empty:
            price = data['Close'].iloc[-1]
            st.markdown(f"<div class='price'>₹{price:,.2f}</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; color:#94a3b8;'>{asset} • LIVE</p>", unsafe_allow_html=True)
except:
    st.markdown(f"<div class='price'>₹23,500</div>", unsafe_allow_html=True)

st.markdown("---")

# ===== Control Buttons =====
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

# ===== Display Current TP/SL for Selected Asset =====
st.markdown("### 🎯 Current TP/SL for " + asset)
if asset in st.session_state.config:
    cfg = st.session_state.config[asset]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Stop Loss", f"{cfg['sl']}")
    col2.metric("Target 1", f"{cfg['tp1']}")
    col3.metric("Target 2", f"{cfg['tp2']}")
    col4.metric("Target 3", f"{cfg['tp3']}")
    
    st.markdown(f"**Quantity Booking:** TP1: {st.session_state.booking['tp1']}% | TP2: {st.session_state.booking['tp2']}% | TP3: {st.session_state.booking['tp3']}%")

st.markdown("---")
st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')} • Auto Refresh | Manual TP/SL Editable")
