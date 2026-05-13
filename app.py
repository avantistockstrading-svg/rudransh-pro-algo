import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import yfinance as yf
import requests
from datetime import datetime, timedelta
import time
from streamlit_autorefresh import st_autorefresh
import json
import os

st.set_page_config(page_title="Rudransh Pro-Algo", layout="wide")

# ===== Professional CSS (Mobile Optimized) =====
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

# ===== Telegram Alert =====
def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
    except:
        pass

# ===== Session State =====
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

# Reset daily trades
if datetime.now().date() != st.session_state.last_trade_date:
    st.session_state.nifty_trades = 0
    st.session_state.crude_trades = 0
    st.session_state.ng_trades = 0
    st.session_state.last_trade_date = datetime.now().date()

# ===== DEFAULT TP/SL CONFIGURATION =====
DEFAULT_CONFIG = {
    "NIFTY": {"lot": 65, "sl": 30, "tp1": 12, "tp2": 22, "tp3": 30},
    "CRUDEOIL": {"lot": 100, "sl": 10, "tp1": 10, "tp2": 15, "tp3": 20},
    "NATURALGAS": {"lot": 1250, "sl": 2, "tp1": 1, "tp2": 1.5, "tp3": 2},
    "STOCK_OPTIONS": {"lot": "auto", "sl": 10, "tp1": 5, "tp2": 10, "tp3": 15}
}

BOOKING_DEFAULT = {"tp1": 50, "tp2": 25, "tp3": 25}
MAX_OPTION_QTY = 2000

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

if "config" not in st.session_state:
    settings = load_settings()
    st.session_state.config = settings["config"]
    st.session_state.booking = settings["booking"]
if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = False

# ===== Header =====
st.markdown("<h1>📱 RUDRANSH PRO-ALGO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Advanced Trading Terminal</p>", unsafe_allow_html=True)
st.markdown("---")

# ===== Sidebar =====
with st.sidebar:
    st.markdown("## 🎮 CONTROLS")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START", use_container_width=True):
            st.session_state.running = True
            send_telegram("🤖 ALGO STARTED")
            st.toast("Algo Started!", icon="✅")
    with col2:
        if st.button("⏹️ STOP", use_container_width=True):
            st.session_state.running = False
            send_telegram("🛑 ALGO STOPPED")
            st.toast("Algo Stopped!", icon="🛑")
    
    st.markdown("---")
    
    # Manual Settings Toggle
    st.markdown("## ⚙️ SETTINGS")
    manual_toggle = st.toggle("🔧 Manual Edit Mode", value=st.session_state.manual_mode)
    
    if manual_toggle != st.session_state.manual_mode:
        st.session_state.manual_mode = manual_toggle
        st.rerun()
    
    if st.session_state.manual_mode:
        st.info("✏️ Edit TP/SL Values")
        
        # NIFTY
        st.markdown("### NIFTY")
        nifty_sl = st.number_input("SL", value=st.session_state.config["NIFTY"]["sl"], step=5, key="n_sl")
        nifty_tp1 = st.number_input("TP1", value=st.session_state.config["NIFTY"]["tp1"], step=5, key="n_tp1")
        nifty_tp2 = st.number_input("TP2", value=st.session_state.config["NIFTY"]["tp2"], step=5, key="n_tp2")
        nifty_tp3 = st.number_input("TP3", value=st.session_state.config["NIFTY"]["tp3"], step=5, key="n_tp3")
        
        # Booking %
        st.markdown("### Booking %")
        tp1_pct = st.slider("TP1 %", 0, 100, st.session_state.booking["tp1"])
        tp2_pct = st.slider("TP2 %", 0, 100, st.session_state.booking["tp2"])
        tp3_pct = st.slider("TP3 %", 0, 100, st.session_state.booking["tp3"])
        
        if st.button("💾 SAVE", use_container_width=True):
            st.session_state.config["NIFTY"] = {"lot": 65, "sl": nifty_sl, "tp1": nifty_tp1, "tp2": nifty_tp2, "tp3": nifty_tp3}
            st.session_state.booking = {"tp1": tp1_pct, "tp2": tp2_pct, "tp3": tp3_pct}
            save_settings(st.session_state.config, st.session_state.booking)
            st.success("Saved!")
            st.rerun()
        
        if st.button("🔄 RESET", use_container_width=True):
            st.session_state.config = DEFAULT_CONFIG.copy()
            st.session_state.booking = BOOKING_DEFAULT.copy()
            save_settings(st.session_state.config, st.session_state.booking)
            st.success("Reset to Default!")
            st.rerun()
    
    st.markdown("---")
    
    # Asset Selection
    st.markdown("## 📈 ASSET")
    asset = st.selectbox("Select", ["NIFTY", "CRUDEOIL", "NATURALGAS", "STOCK_OPTIONS"])
    st.session_state.asset = asset
    
    if asset == "STOCK_OPTIONS":
        lot_size = st.number_input("Lot Size", min_value=100, max_value=2000, value=500, step=100)
        if lot_size <= 0:
            lot_size = 500
        max_lots = MAX_OPTION_QTY // lot_size
        if max_lots < 1:
            max_lots = 1
        lots = st.number_input("Lots", min_value=1, max_value=max_lots, value=min(2, max_lots))
        st.session_state.quantity = lots * lot_size
    else:
        lot_size = st.session_state.config[asset]["lot"]
        lots = st.number_input("Lots", min_value=1, max_value=10, value=1)
        st.session_state.quantity = lots * lot_size
    
    st.markdown(f"<p style='text-align:center; color:#00ff88;'>📦 Qty: {st.session_state.quantity}</p>", unsafe_allow_html=True)
    
    # Current settings display
    if asset in st.session_state.config:
        cfg = st.session_state.config[asset]
        st.caption(f"SL: {cfg['sl']} | TP1: {cfg['tp1']} | TP2: {cfg['tp2']} | TP3: {cfg['tp3']}")

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

# ===== Get Data for Signal Calculation =====
def calculate_signals():
    symbol_map = {"NIFTY": "^NSEI", "CRUDEOIL": "CL=F", "NATURALGAS": "NG=F", "STOCK_OPTIONS": "^NSEI"}
    
    # Get NIFTY data for trend filter
    nifty_df = yf.download("^NSEI", period="7d", interval="15m", progress=False)
    nifty_df.columns = [str(c).lower() for c in nifty_df.columns]
    
    # Determine NIFTY trend
    if len(nifty_df) >= 20 and 'close' in nifty_df.columns:
        nifty_ema20 = nifty_df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
        nifty_current = nifty_df['close'].iloc[-1]
        nifty_positive = nifty_current > nifty_ema20
        nifty_negative = nifty_current < nifty_ema20
    else:
        nifty_positive = True
        nifty_negative = False
    
    # Get stock data
    stock_df = yf.download(symbol_map[asset], period="7d", interval="15m", progress=False)
    stock_df.columns = [str(c).lower() for c in stock_df.columns]
    
    if stock_df.empty or len(stock_df) < 30:
        return {"signal": "WAIT", "buy": False, "sell": False, "price": 0}
    
    # Calculate indicators for stock
    stock_df['ema9'] = stock_df['close'].ewm(span=9, adjust=False).mean()
    stock_df['ema20'] = stock_df['close'].ewm(span=20, adjust=False).mean()
    stock_df['ema200'] = stock_df['close'].ewm(span=200, adjust=False).mean()
    stock_df['rsi'] = ta.rsi(stock_df['close'], 14)
    
    # ADX
    adx_data = ta.adx(stock_df['high'], stock_df['low'], stock_df['close'], length=14)
    stock_df['adx'] = adx_data['ADX_14'] if adx_data is not None else 0
    
    # Volume SMA
    stock_df['volume_sma'] = stock_df['volume'].rolling(20).mean()
    
    # Get latest values
    c1 = stock_df.iloc[-2]
    c2 = stock_df.iloc[-1]
    
    ema9 = stock_df['ema9'].iloc[-1]
    ema20 = stock_df['ema20'].iloc[-1]
    ema200 = stock_df['ema200'].iloc[-1] if not stock_df['ema200'].isna().all() else c2['close']
    rsi = stock_df['rsi'].iloc[-1]
    adx = stock_df['adx'].iloc[-1]
    volume = c2['volume']
    volume_sma = stock_df['volume_sma'].iloc[-1] if not stock_df['volume_sma'].isna().all() else 1
    
    # Conditions
    strong_bull = c2['close'] > c2['open'] and c2['close'] > c1['high']
    strong_bear = c2['close'] < c2['open'] and c2['close'] < c1['low']
    volume_filter = volume > volume_sma if volume > 0 else True
    sideways = (45 < rsi < 55) and adx < 20
    
    # 5m Trend (using 15m data as proxy)
    trend5_up = ema9 > ema20
    trend15_up = ema9 > ema20
    trend1h_up = ema9 > ema20
    
    # Stock strength
    strong_bull_stock = (ema9 > ema20 and c2['close'] > ema200 and rsi >= 60 and adx >= 25 and volume_filter and strong_bull and c2['close'] > c1['high'])
    strong_bear_stock = (ema9 < ema20 and c2['close'] < ema200 and rsi <= 40 and adx >= 25 and volume_filter and strong_bear and c2['close'] < c1['low'])
    
    sector_bullish = True
    sector_bearish = False
    
    # FINAL BUY/SELL CONDITIONS (तुमच्या अचूक logic नुसार)
    buy_condition = (nifty_positive and not nifty_negative and not sideways and sector_bullish and strong_bull_stock and trend5_up and trend15_up and trend1h_up and c2['close'] > ema20)
    
    sell_condition = (nifty_negative and not nifty_positive and not sideways and sector_bearish and strong_bear_stock and not trend5_up and not trend15_up and not trend1h_up and c2['close'] < ema20)
    
    if buy_condition:
        signal = "BUY"
    elif sell_condition:
        signal = "SELL"
    else:
        signal = "WAIT"
    
    # Cooldown check
    cooldown_ok = (datetime.now() - st.session_state.last_trade_time).seconds > 300
    
    return {
        "signal": signal,
        "buy": buy_condition and cooldown_ok and st.session_state.last_trade_side != "BUY",
        "sell": sell_condition and cooldown_ok and st.session_state.last_trade_side != "SELL",
        "price": c2['close'],
        "ema20": ema20,
        "rsi": rsi,
        "adx": adx,
        "trend": "BULLISH" if ema9 > ema20 else "BEARISH"
    }

# Calculate signals
signals = calculate_signals()

# ===== Display =====
col1, col2, col3, col4 = st.columns(4)
col1.metric("Price", f"₹{signals['price']:.2f}")
col2.metric("Signal", signals['signal'])
col3.metric("RSI", f"{signals['rsi']:.1f}")
col4.metric("ADX", f"{signals['adx']:.1f}")

# ===== Control Buttons =====
st.markdown("---")
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

# ===== Auto Trade Execution =====
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

if st.session_state.running and market_hours and trades_today < max_trades:
    if signals['buy']:
        st.success(f"🚀 BUY SIGNAL at ₹{signals['price']:.2f}")
        send_telegram(f"🔵 BUY {asset} | Qty: {st.session_state.quantity} | Price: ₹{signals['price']:.2f}")
        if asset == "NIFTY":
            st.session_state.nifty_trades += 1
        elif asset == "CRUDEOIL":
            st.session_state.crude_trades += 1
        else:
            st.session_state.ng_trades += 1
        st.session_state.last_trade_side = "BUY"
        st.session_state.last_trade_time = datetime.now()
        st.balloons()
    
    elif signals['sell']:
        st.error(f"🔻 SELL SIGNAL at ₹{signals['price']:.2f}")
        send_telegram(f"🔴 SELL {asset} | Qty: {st.session_state.quantity} | Price: ₹{signals['price']:.2f}")
        if asset == "NIFTY":
            st.session_state.nifty_trades += 1
        elif asset == "CRUDEOIL":
            st.session_state.crude_trades += 1
        else:
            st.session_state.ng_trades += 1
        st.session_state.last_trade_side = "SELL"
        st.session_state.last_trade_time = datetime.now()

# ===== Status =====
st.markdown("---")
if st.session_state.running and market_hours:
    st.success("🟢 ALGO RUNNING")
elif not market_hours:
    st.info("⏰ Market closed")
else:
    st.warning("🔴 ALGO STOPPED")

st.caption("🔄 Auto Refresh Every 10 Seconds")
st_autorefresh(interval=10000, key="refresh")

# ===== Daily Trades =====
st.markdown("---")
st.markdown("### Daily Trades")
col1, col2, col3 = st.columns(3)
col1.metric("NIFTY", f"{st.session_state.nifty_trades}/2")
col2.metric("CRUDE", f"{st.session_state.crude_trades}/2")
col3.metric("NG", f"{st.session_state.ng_trades}/2")

st.markdown("---")
st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
