import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import requests
from datetime import datetime, timedelta
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Rudransh Pro-Algo", layout="wide")

st.markdown("""
<style>
.main { padding: 0rem 0.5rem; }
.stMetric { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 20px; padding: 15px; margin: 5px 0; border: 1px solid rgba(255,255,255,0.05); }
.stButton button { background: linear-gradient(90deg, #00ff88, #00cc66); color: black; font-weight: bold; border-radius: 30px; padding: 12px; width: 100%; border: none; }
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

def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
    except:
        pass

# Session State
if "running" not in st.session_state:
    st.session_state.running = False
if "pnl" not in st.session_state:
    st.session_state.pnl = 0
if "quantity" not in st.session_state:
    st.session_state.quantity = 65
if "asset" not in st.session_state:
    st.session_state.asset = "NIFTY"
if "last_trade_side" not in st.session_state:
    st.session_state.last_trade_side = ""
if "last_trade_time" not in st.session_state:
    st.session_state.last_trade_time = datetime.now() - timedelta(minutes=10)
if "nifty_trades" not in st.session_state:
    st.session_state.nifty_trades = 0
if "crude_trades" not in st.session_state:
    st.session_state.crude_trades = 0
if "ng_trades" not in st.session_state:
    st.session_state.ng_trades = 0
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = datetime.now().date()

if datetime.now().date() != st.session_state.last_trade_date:
    st.session_state.nifty_trades = 0
    st.session_state.crude_trades = 0
    st.session_state.ng_trades = 0
    st.session_state.last_trade_date = datetime.now().date()

st.markdown("<h1>📱 RUDRANSH PRO-ALGO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Advanced Trading Terminal</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## 🎮 CONTROLS")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START", use_container_width=True):
            st.session_state.running = True
            send_telegram("🤖 ALGO STARTED")
    with col2:
        if st.button("⏹️ STOP", use_container_width=True):
            st.session_state.running = False
            send_telegram("🛑 ALGO STOPPED")
    
    st.markdown("---")
    st.markdown("## 📈 ASSET")
    asset = st.selectbox("Select", ["NIFTY", "CRUDEOIL", "NATURALGAS"])
    st.session_state.asset = asset
    
    lots = st.number_input("Lots", min_value=1, max_value=10, value=1)
    lot_sizes = {"NIFTY": 65, "CRUDEOIL": 100, "NATURALGAS": 1250}
    st.session_state.quantity = lots * lot_sizes[asset]
    
    st.markdown(f"<p style='text-align:center; color:#00ff88;'>📦 Qty: {st.session_state.quantity}</p>", unsafe_allow_html=True)

# Status
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

# Live Price
symbols = {"NIFTY": "^NSEI", "CRUDEOIL": "CL=F", "NATURALGAS": "NG=F"}
try:
    ticker = yf.Ticker(symbols[asset])
    data = ticker.history(period="1d")
    if not data.empty:
        price = data['Close'].iloc[-1]
        st.markdown(f"<div class='price'>₹{price:,.2f}</div>", unsafe_allow_html=True)
except:
    st.markdown(f"<div class='price'>₹23,500</div>", unsafe_allow_html=True)

st.markdown("---")

# Get Data for Signals
def get_signals():
    symbol = symbols[asset]
    df = yf.download(symbol, period="7d", interval="15m", progress=False)
    
    if df.empty or len(df) < 30:
        return {"signal": "WAIT", "price": 0, "trend": "NEUTRAL", "rsi": 50, "ema20": 0}
    
    # Clean column names (convert to lowercase)
    df.columns = [str(c).lower() for c in df.columns]
    close = df['close']
    
    # Calculate EMA
    ema9 = close.ewm(span=9, adjust=False).mean()
    ema20 = close.ewm(span=20, adjust=False).mean()
    
    # Calculate RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    current = close.iloc[-1]
    current_ema20 = ema20.iloc[-1]
    current_rsi = rsi.iloc[-1]
    
    # Signal Logic
    if current > current_ema20 and current_rsi < 70:
        signal = "BUY"
    elif current < current_ema20 and current_rsi > 30:
        signal = "SELL"
    else:
        signal = "WAIT"
    
    return {"signal": signal, "price": current, "rsi": current_rsi, "ema20": current_ema20, "trend": "BULLISH" if current > current_ema20 else "BEARISH"}

signals = get_signals()

# Display
col1, col2, col3, col4 = st.columns(4)
col1.metric("Price", f"₹{signals['price']:.2f}" if signals['price'] else "N/A")
col2.metric("Signal", signals['signal'])
col3.metric("RSI", f"{signals['rsi']:.1f}" if signals['rsi'] else "N/A")
col4.metric("Trend", signals['trend'])

st.markdown("---")

# Control Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 BUY", use_container_width=True):
        st.success(f"BUY {st.session_state.quantity} qty")
with col2:
    if st.button("🔴 SELL", use_container_width=True):
        st.error(f"SELL {st.session_state.quantity} qty")
with col3:
    if st.button("🔲 SQ OFF", use_container_width=True):
        st.session_state.pnl = 0
        st.warning("Squared off!")

st.markdown("---")

# Auto Trade
market_hours = False
now = datetime.now()
if asset == "NIFTY":
    if 9 <= now.hour <= 15:
        market_hours = True
    max_trades = 2
    trades_today = st.session_state.nifty_trades
else:
    if 18 <= now.hour <= 23:
        market_hours = True
    max_trades = 2
    trades_today = st.session_state.crude_trades if asset == "CRUDEOIL" else st.session_state.ng_trades

cooldown_ok = (datetime.now() - st.session_state.last_trade_time).seconds > 300

if st.session_state.running and market_hours and trades_today < max_trades and cooldown_ok:
    if signals['signal'] == "BUY" and st.session_state.last_trade_side != "BUY":
        st.success(f"🚀 BUY SIGNAL at ₹{signals['price']:.2f}")
        send_telegram(f"🔵 BUY {asset} | Qty: {st.session_state.quantity}")
        if asset == "NIFTY":
            st.session_state.nifty_trades += 1
        elif asset == "CRUDEOIL":
            st.session_state.crude_trades += 1
        else:
            st.session_state.ng_trades += 1
        st.session_state.last_trade_side = "BUY"
        st.session_state.last_trade_time = datetime.now()
        st.balloons()
    
    elif signals['signal'] == "SELL" and st.session_state.last_trade_side != "SELL":
        st.error(f"🔻 SELL SIGNAL at ₹{signals['price']:.2f}")
        send_telegram(f"🔴 SELL {asset} | Qty: {st.session_state.quantity}")
        if asset == "NIFTY":
            st.session_state.nifty_trades += 1
        elif asset == "CRUDEOIL":
            st.session_state.crude_trades += 1
        else:
            st.session_state.ng_trades += 1
        st.session_state.last_trade_side = "SELL"
        st.session_state.last_trade_time = datetime.now()

# Status
st.markdown("---")
if st.session_state.running and market_hours:
    st.success("🟢 ALGO RUNNING")
elif not market_hours:
    st.info("⏰ Market closed")
else:
    st.warning("🔴 ALGO STOPPED")

st.caption("🔄 Auto Refresh Every 10 Seconds")
st_autorefresh(interval=10000, key="refresh")

# Daily Trades
st.markdown("---")
st.markdown("### Daily Trades")
col1, col2, col3 = st.columns(3)
col1.metric("NIFTY", f"{st.session_state.nifty_trades}/2")
col2.metric("CRUDE", f"{st.session_state.crude_trades}/2")
col3.metric("NG", f"{st.session_state.ng_trades}/2")
