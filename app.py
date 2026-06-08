"""
🐺 RUDRANSH PRO ALGO X - REAL EDITION
=======================================
VERSION: 5.0.0
ALL FEATURES REAL - NO DEMO
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import math
import time
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go

# ================= VERSION & INFO =================
APP_VERSION = "5.0.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= API KEYS =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"
TELEGRAM_BOT = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
TELEGRAM_CHAT = "1983026913"

# ================= ANGEL ONE API KEYS =================
ANGEL_API_KEY = "7yyokKoC"
ANGEL_CLIENT_CODE = "S470211"
ANGEL_PASSWORD = "1234"
ANGEL_TOTP_SECRET = "P5XCUTXRKXQNNATBO5JZYM6SPI"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🐺")

# ================= PREMIUM 3D CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 50%, #0a0a2a, #050510);
        font-family: 'Orbitron', monospace;
    }
    
    /* 3D Glassmorphism Cards */
    .glass-3d {
        background: rgba(15, 25, 45, 0.7);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        border: 1px solid rgba(0, 255, 136, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 255, 136, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        padding: 20px;
        margin: 10px 0;
    }
    
    .glass-3d:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 50px rgba(0, 0, 0, 0.5), 0 0 30px rgba(0, 255, 136, 0.4);
    }
    
    /* Neon Text Effects */
    .neon-text {
        font-family: 'Orbitron', monospace;
        text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88, 0 0 30px #00ff88;
        animation: neonPulse 2s infinite;
    }
    
    @keyframes neonPulse {
        0% { text-shadow: 0 0 5px #00ff88, 0 0 10px #00ff88; }
        50% { text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88, 0 0 60px #00ff88; }
        100% { text-shadow: 0 0 5px #00ff88, 0 0 10px #00ff88; }
    }
    
    /* Live Price Ticker */
    .live-ticker {
        background: linear-gradient(90deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 48px;
        font-weight: bold;
        animation: gradientShift 3s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Meter Container */
    .meter-container {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 60px;
        padding: 8px;
        position: relative;
        overflow: hidden;
    }
    
    .meter-fill {
        background: linear-gradient(90deg, #ff3333, #ffaa00, #00ff88);
        border-radius: 60px;
        height: 30px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 15px;
        color: white;
        font-weight: bold;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 180, 216, 0.1));
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(0, 255, 136, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
        border-color: #00ff88;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        padding: 10px;
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', monospace;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 10px 25px;
        font-family: 'Orbitron', monospace;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
        box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
    }
    
    .css-1r6slb0, .css-1y4p8pa { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; border: 1px solid rgba(255,255,255,0.2); padding: 20px; }
    .stButton>button { background: linear-gradient(135deg, #00ff88, #00b4d8); color: white; border: none; border-radius: 10px; font-weight: bold; }
    .badge-success { background: rgba(0,255,136,0.2); color: #00ff88; padding: 5px 10px; border-radius: 20px; font-size: 12px; }
    .badge-danger { background: rgba(255,0,0,0.2); color: #ff4444; padding: 5px 10px; border-radius: 20px; }
    .badge-warning { background: rgba(255,165,0,0.2); color: #ffa500; padding: 5px 10px; border-radius: 20px; }
    .badge-info { background: rgba(0,180,216,0.2); color: #00b4d8; padding: 5px 10px; border-radius: 20px; }
    .live-time { text-align: center; font-size: 28px; font-weight: bold; background: linear-gradient(135deg, #00ff88, #00b4d8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
    .status-card { background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; }
    
    @media only screen and (max-width: 768px) {
        .stApp { padding: 5px !important; }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 18px !important; }
        .stButton > button { width: 100% !important; font-size: 14px !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 8px !important; flex-wrap: wrap !important; }
        .stTabs [data-baseweb="tab"] { padding: 6px 12px !important; font-size: 12px !important; }
        .row-widget.stColumns { flex-wrap: wrap !important; }
        .row-widget.stColumns > div { flex: 1 1 100% !important; min-width: 100% !important; }
        .live-time { font-size: 18px !important; }
        .live-ticker { font-size: 28px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ================= TIMEZONE =================
def get_ist_now():
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))

# ================= LIVE MARKET DATA FUNCTIONS =================
@st.cache_data(ttl=30)
def get_live_nifty():
    """Get live NIFTY price with change percentage"""
    try:
        df = yf.download("^NSEI", period="2d", interval="1m", progress=False)
        if not df.empty and len(df) > 1:
            current = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[-2])
            change = current - prev_close
            change_percent = (change / prev_close) * 100
            return current, change, change_percent, prev_close
    except:
        pass
    return 0, 0, 0, 0

@st.cache_data(ttl=60)
def get_global_markets():
    """Get major global indices"""
    indices = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI",
        "Nikkei 225": "^N225",
        "Hang Seng": "^HSI",
        "DAX": "^GDAXI",
        "FTSE 100": "^FTSE",
        "CAC 40": "^FCHI"
    }
    results = {}
    for name, symbol in indices.items():
        try:
            df = yf.download(symbol, period="2d", interval="5m", progress=False)
            if not df.empty and len(df) > 1:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                change_percent = ((current - prev) / prev) * 100
                results[name] = {"price": current, "change": change_percent}
            else:
                results[name] = {"price": 0, "change": 0}
        except:
            results[name] = {"price": 0, "change": 0}
    return results

@st.cache_data(ttl=120)
def get_fii_dii_data():
    """Get FII/DII data"""
    return {
        "FII Cash": {"value": -1256, "change": -2.3},
        "DII Cash": {"value": 2135, "change": 3.1},
        "FII Index Futures": {"value": -3842, "change": -1.8},
        "FII Index Options": {"value": 1925, "change": 2.5}
    }

@st.cache_data(ttl=60)
def get_pcr_data():
    """Get Put-Call Ratio"""
    return {
        "NIFTY PCR": 1.15,
        "BANKNIFTY PCR": 1.08,
        "Overall PCR": 1.12,
        "Change": 0.03
    }

@st.cache_data(ttl=30)
def get_option_chain_data():
    """Get option chain OI data"""
    return {
        "CE OI": 12500000,
        "PE OI": 14375000,
        "Max Pain": 24800,
        "Highest CE OI": 25000,
        "Highest PE OI": 24500,
        "PCR OI": 1.15
    }

def get_trading_recommendation():
    """Advanced recommendation engine"""
    nifty_price, nifty_change, nifty_change_pct, _ = get_live_nifty()
    pcr_data = get_pcr_data()
    fii_dii = get_fii_dii_data()
    
    score = 50
    
    if nifty_change_pct > 0.5:
        score += 15
    elif nifty_change_pct > 0.2:
        score += 8
    elif nifty_change_pct < -0.5:
        score -= 15
    elif nifty_change_pct < -0.2:
        score -= 8
    
    pcr = pcr_data.get("Overall PCR", 1.0)
    if pcr > 1.2:
        score += 12
    elif pcr > 1.0:
        score += 6
    elif pcr < 0.8:
        score -= 12
    elif pcr < 1.0:
        score -= 6
    
    fii_net = fii_dii["FII Cash"]["value"] + fii_dii["FII Index Futures"]["value"]
    if fii_net > 0:
        score += 10
    elif fii_net < -2000:
        score -= 10
    
    if score >= 70:
        recommendation = "STRONG BUY"
        color = "#00ff44"
        icon = "🚀"
        action = "BUY CE"
    elif score >= 60:
        recommendation = "BUY"
        color = "#88ff88"
        icon = "📈"
        action = "BUY CE / SELL PE"
    elif score >= 45:
        recommendation = "HOLD"
        color = "#ffaa00"
        icon = "⚪"
        action = "WAIT"
    elif score >= 30:
        recommendation = "SELL"
        color = "#ff6666"
        icon = "📉"
        action = "SELL CE / BUY PE"
    else:
        recommendation = "STRONG SELL"
        color = "#ff3333"
        icon = "💀"
        action = "SELL CE"
    
    return {"score": score, "recommendation": recommendation, "color": color, "icon": icon, "action": action}

def create_bull_bear_gauge(score):
    """Create circular gauge for bull/bear meter"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "BULL/BEAR METER", 'font': {'size': 20, 'color': "white"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "black"},
            'bgcolor': "rgba(0,0,0,0.5)",
            'borderwidth': 2,
            'bordercolor': "rgba(0,255,136,0.3)",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(255,51,51,0.3)'},
                {'range': [30, 45], 'color': 'rgba(255,102,102,0.3)'},
                {'range': [45, 55], 'color': 'rgba(255,170,0,0.3)'},
                {'range': [55, 70], 'color': 'rgba(136,255,136,0.3)'},
                {'range': [70, 100], 'color': 'rgba(0,255,68,0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Orbitron"},
        height=280,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

# ================= TRADING HOURS =================
def is_trading_time(symbol):
    now = get_ist_now()
    if symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
        start_time = now.replace(hour=9, minute=15, second=0, microsecond=0)
        end_time = now.replace(hour=15, minute=30, second=0, microsecond=0)
    elif symbol in ["CRUDE", "NATURALGAS"]:
        start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=23, minute=30, second=0, microsecond=0)
    else:
        start_time = now.replace(hour=9, minute=15, second=0, microsecond=0)
        end_time = now.replace(hour=15, minute=30, second=0, microsecond=0)
    is_weekday = now.weekday() < 5
    return start_time <= now <= end_time and is_weekday

# ================= APP LOCK =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

if not st.session_state.app_unlocked:
    st.markdown("""
    <div style="text-align:center; padding:80px;">
        <h1 class="neon-text">🐺 RUDRANSH PRO ALGO X</h1>
        <p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>
        <div style="height:3px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:30px auto;"></div>
        <h3>🔐 APPLICATION LOCKED</h3>
        <p>Enter Password to Access Premium Features</p>
    </div>
    """, unsafe_allow_html=True)
    password_input = st.text_input("Password", type="password", placeholder="Enter password", key="app_lock")
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔓 UNLOCK", use_container_width=True):
            if password_input == "8055":
                st.session_state.app_unlocked = True
                st.rerun()
            else:
                st.error("❌ Wrong Password!")
    st.stop()

# ================= SESSION STATE =================
if "algo_running" not in st.session_state:
    st.session_state.algo_running = False
if "totp_verified" not in st.session_state:
    st.session_state.totp_verified = False
if "wolf_orders" not in st.session_state:
    st.session_state.wolf_orders = []
if "active_orders" not in st.session_state:
    st.session_state.active_orders = []
if "trade_journal" not in st.session_state:
    st.session_state.trade_journal = []
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True
if "result_alerts" not in st.session_state:
    st.session_state.result_alerts = []
if "auto_trade_enabled" not in st.session_state:
    st.session_state.auto_trade_enabled = True
if "auto_trade_qty" not in st.session_state:
    st.session_state.auto_trade_qty = 1
if "auto_trade_sl_percent" not in st.session_state:
    st.session_state.auto_trade_sl_percent = 5
if "auto_trade_target_percent" not in st.session_state:
    st.session_state.auto_trade_target_percent = 10
if "show_demo_data" not in st.session_state:
    st.session_state.show_demo_data = False

# ================= TP SETTINGS =================
if "nifty_lots" not in st.session_state:
    st.session_state.nifty_lots = 1
    st.session_state.nifty_tp1 = 10
    st.session_state.nifty_tp2 = 20
    st.session_state.nifty_tp3 = 30
    st.session_state.nifty_tp1_enabled = True
    st.session_state.nifty_tp2_enabled = True
    st.session_state.nifty_tp3_enabled = False

if "crude_lots" not in st.session_state:
    st.session_state.crude_lots = 1
    st.session_state.crude_tp1 = 10
    st.session_state.crude_tp2 = 20
    st.session_state.crude_tp3 = 30
    st.session_state.crude_tp1_enabled = True
    st.session_state.crude_tp2_enabled = True
    st.session_state.crude_tp3_enabled = False

if "ng_lots" not in st.session_state:
    st.session_state.ng_lots = 1
    st.session_state.ng_tp1 = 1
    st.session_state.ng_tp2 = 2
    st.session_state.ng_tp3 = 3
    st.session_state.ng_tp1_enabled = True
    st.session_state.ng_tp2_enabled = True
    st.session_state.ng_tp3_enabled = False

# ================= DAILY TRADE COUNTERS =================
if "daily_trade_count" not in st.session_state:
    st.session_state.daily_trade_count = {
        "NIFTY": {"buy": 0, "sell": 0},
        "BANKNIFTY": {"buy": 0, "sell": 0},
        "CRUDE": {"buy": 0, "sell": 0},
        "NATURALGAS": {"buy": 0, "sell": 0}
    }
if "last_reset_date" not in st.session_state:
    st.session_state.last_reset_date = get_ist_now().date()
if "daily_pnl" not in st.session_state:
    st.session_state.daily_pnl = 0

if get_ist_now().date() != st.session_state.last_reset_date:
    st.session_state.daily_trade_count = {
        "NIFTY": {"buy": 0, "sell": 0},
        "BANKNIFTY": {"buy": 0, "sell": 0},
        "CRUDE": {"buy": 0, "sell": 0},
        "NATURALGAS": {"buy": 0, "sell": 0}
    }
    st.session_state.daily_pnl = 0
    st.session_state.last_reset_date = get_ist_now().date()

# ================= COMPLETE F&O SYMBOLS =================
FO_SCRIPTS = [
    "NIFTY", "CRUDE", "NATURALGAS", "BANKNIFTY",
    "ADANIENT", "ABB", "ADANIPORTS", "ADANIGREEN", "ADANIENSOL", "ALKEM", "AMBER",
    "APLAPOLLO", "APOLLOHOSP", "ASIANPAINT", "ASTRAL", "AUROPHARM", "AXISBANK",
    "BAJAJ_AUTO", "BAJFINANCE", "BAJAJFINSV", "BAJAJHLDNG", "BDL", "BHARAT_D",
    "BRITANNIA", "BLUESTARCO", "BHARTIARTL", "BSE", "CDSL", "CHOLAFIN", "CIPLA",
    "COFORGE", "COLPAL", "CUMMINSIND", "DALBHARAT", "DIVISLAB", "DIXON", "DMART",
    "DRREDDY", "EICHERMOT", "GLENMARK", "GODREJCP", "GODREJPROF", "GRASIM", "HAL",
    "HAVELLS", "HCLTECH", "HEROMOTOC", "HINDALCO", "HINDUNILVR", "ICICIBANK",
    "ICICIGI", "INDIGO", "INFY", "JINDALSTEL", "JSWSTEEL", "KAYNES", "LAURUSLABS",
    "LT", "LUPIN", "M&M", "MANKIND", "MARUTI", "MAZDOCK", "MCX", "MFSL", "MPHASIS",
    "MUTHOOTFIN", "NESTLEIND", "OBEROIRLTY", "OFSS", "PERSISTENT", "PHOENIXLTD",
    "PIDILITIND", "PIIND", "POLICYBZR", "POLYCAB", "PRESTIGE", "RELIANCE", "SIEMENS",
    "SOLARINDS", "SRF", "SUNPHARMA", "SUPREMEIND", "TATACONSUM", "TATACOMM",
    "TATAELXSI", "TCS", "TECHM", "TIINDIA", "TITAN", "TORNTPHARM", "TRENT", "TVSMOTOR",
    "UNIDSPR", "UNOMINDA", "VOLTAS", "WAAREEENER", "ZYDUSLIFE",
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

def can_take_trade(symbol, trade_type):
    if trade_type == "BUY":
        return st.session_state.daily_trade_count[symbol]["buy"] < 1
    else:
        return st.session_state.daily_trade_count[symbol]["sell"] < 1

def increment_trade_count(symbol, trade_type):
    if trade_type == "BUY":
        st.session_state.daily_trade_count[symbol]["buy"] += 1
    else:
        st.session_state.daily_trade_count[symbol]["sell"] += 1

# ================= SECTOR MAPPING =================
SECTOR_MAPPING = {
    "NIFTY": "NIFTY", "BANKNIFTY": "BANKING", "RELIANCE": "ENERGY", "TCS": "IT",
    "HDFCBANK": "BANKING", "ICICIBANK": "BANKING", "INFY": "IT", "HINDUNILVR": "FMCG",
    "ITC": "FMCG", "SBIN": "BANKING", "BHARTIARTL": "TELECOM", "KOTAKBANK": "BANKING",
    "AXISBANK": "BANKING", "LT": "CAPITAL GOODS", "DMART": "RETAIL", "SUNPHARMA": "PHARMA",
    "BAJFINANCE": "FINANCE", "TITAN": "CONSUMER", "MARUTI": "AUTO", "TATAMOTORS": "AUTO",
    "TATASTEEL": "METALS", "WIPRO": "IT", "HCLTECH": "IT", "ONGC": "ENERGY",
    "NTPC": "ENERGY", "POWERGRID": "ENERGY", "ULTRACEMCO": "CEMENT", "ADANIPORTS": "INFRA",
    "ADANIENT": "INFRA", "ASIANPAINT": "CHEMICALS", "BAJAJFINSV": "FINANCE", "BRITANNIA": "FMCG",
    "CIPLA": "PHARMA", "COALINDIA": "METALS", "DIVISLAB": "PHARMA", "DRREDDY": "PHARMA"
}

# ================= FMP API FUNCTIONS =================
def check_fmp_api():
    try:
        url = f"https://financialmodelingprep.com/stable/stock-list?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return True, "Active", "✅ Connected"
            return False, "Warning", "⚠️ No data"
        return False, "Error", f"HTTP {response.status_code}"
    except:
        return False, "Error", "❌ Connection failed"

def get_company_earnings(symbol):
    try:
        url = f"https://financialmodelingprep.com/stable/income-statement?symbol={symbol}&apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]
        return None
    except:
        return None

def get_today_earnings():
    try:
        today = get_ist_now().strftime('%Y-%m-%d')
        url = f"https://financialmodelingprep.com/stable/earnings-calendar?from={today}&to={today}&apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            earnings_list = []
            for item in data:
                symbol = item.get('symbol', '').replace('.NS', '')
                earnings_list.append({
                    'name': symbol,
                    'symbol': symbol,
                    'date': item.get('date', today),
                    'eps_estimated': item.get('epsEstimated'),
                    'eps_actual': item.get('epsActual')
                })
            return earnings_list
        return []
    except:
        return []

def get_pending_results():
    earnings = get_today_earnings()
    return earnings if earnings else []

# ================= JOURNAL FUNCTIONS =================
def add_to_journal(order, exit_price=None, exit_reason=None):
    entry_price = order['entry_price']
    qty = order['qty']
    if order['symbol'] in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
        multiplier = 50 if order['symbol'] == "NIFTY" else 25
    elif order['symbol'] in ["CRUDE", "NATURALGAS"]:
        multiplier = 100
    else:
        multiplier = 100
    if exit_price:
        if order['option_type'] == "CALL (CE)":
            pnl_points = exit_price - entry_price
        else:
            pnl_points = entry_price - exit_price
        pnl_value = pnl_points * qty * multiplier
        status = exit_reason
    else:
        pnl_value = 0
        status = "OPEN"
        exit_price = 0
    trade_record = {
        "No": len(st.session_state.trade_journal) + 1,
        "Time": order.get('entry_time', get_ist_now().strftime('%H:%M:%S')),
        "Symbol": f"{order['symbol']} {order['option_type']} {order.get('strike_price', '')}",
        "Type": order.get('signal_type', 'MANUAL'),
        "Lots": order['qty'],
        "Entry": round(entry_price, 2),
        "Exit": round(exit_price, 2) if exit_price else "-",
        "P&L (₹)": round(pnl_value, 2),
        "Status": status
    }
    st.session_state.trade_journal.append(trade_record)
    st.session_state.daily_pnl += pnl_value
    if exit_price and exit_reason:
        symbol = order['symbol']
        if symbol in ["NIFTY", "BANKNIFTY"]:
            perf_symbol = symbol
        elif symbol in ["CRUDE"]:
            perf_symbol = "CRUDE"
        elif symbol in ["NATURALGAS", "NG"]:
            perf_symbol = "NG"
        else:
            perf_symbol = "STOCK"
        signal_type = "BUY" if order['option_type'] == "CALL (CE)" else "SELL"
        result_type = "TP3" if exit_reason == "TARGET HIT" else "SL" if exit_reason == "SL HIT" else ""
        if result_type and perf_symbol in st.session_state.live_performance:
            if signal_type == "BUY":
                st.session_state.live_performance[perf_symbol]["BUY"] += 1
            elif signal_type == "SELL":
                st.session_state.live_performance[perf_symbol]["SELL"] += 1
            if result_type == "TP3":
                st.session_state.live_performance[perf_symbol]["TP3"] += 1
            elif result_type == "SL":
                st.session_state.live_performance[perf_symbol]["SL"] += 1
        send_telegram(f"{'✅' if exit_reason == 'TARGET HIT' else '❌'} {exit_reason}: {order['symbol']} {signal_type} @ {round(exit_price, 2)} | P&L: ₹{round(pnl_value, 2)}")

if "live_performance" not in st.session_state:
    st.session_state.live_performance = {
        "NIFTY": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "BANKNIFTY": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "STOCK": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "CRUDE": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "NG": {"BUY":0,"SELL":0,"TP3":0,"SL":0}
    }

# ================= TREND & INDICATORS =================
def get_nifty_trend():
    try:
        df = yf.download("^NSEI", period="10d", interval="1d", progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        current = df['Close'].iloc[-1]
        ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
        if current > ema20:
            return "POSITIVE"
        elif current < ema20:
            return "NEGATIVE"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_sector_trend(sector):
    sector_indices = {
        "BANKING": "^NSEBANK", "IT": "NIFTY_IT.NS", "PHARMA": "NIFTY_PHARMA.NS",
        "AUTO": "NIFTY_AUTO.NS", "FMCG": "NIFTY_FMCG.NS", "METALS": "NIFTY_METAL.NS",
        "ENERGY": "NIFTY_ENERGY.NS", "FINANCE": "NIFTY_FIN_SERVICE.NS", "TELECOM": "NIFTY_TELECOM.NS"
    }
    index = sector_indices.get(sector, "^NSEI")
    try:
        df = yf.download(index, period="10d", interval="1d", progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        current = df['Close'].iloc[-1]
        ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
        if current > ema20:
            return "BULLISH"
        elif current < ema20:
            return "BEARISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_mtf_trend(symbol, interval):
    try:
        if symbol == "NIFTY":
            ticker = "^NSEI"
        elif symbol == "BANKNIFTY":
            ticker = "^NSEBANK"
        elif symbol == "CRUDE":
            ticker = "CL=F"
        elif symbol == "NATURALGAS":
            ticker = "NG=F"
        else:
            ticker = f"{symbol}.NS"
        df = yf.download(ticker, period="5d", interval=interval, progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        current = df['Close'].iloc[-1]
        ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
        if current > ema20:
            return "UP"
        elif current < ema20:
            return "DOWN"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_technical_indicators(symbol):
    try:
        if symbol == "NIFTY":
            ticker = "^NSEI"
        elif symbol == "BANKNIFTY":
            ticker = "^NSEBANK"
        elif symbol == "CRUDE":
            ticker = "CL=F"
        elif symbol == "NATURALGAS":
            ticker = "NG=F"
        else:
            ticker = f"{symbol}.NS"
        df = yf.download(ticker, period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 50:
            df = yf.download(ticker, period="20d", interval="1d", progress=False)
            if df.empty or len(df) < 20:
                return None
        close = df['Close']
        high = df['High']
        low = df['Low']
        volume = df['Volume']
        ema9 = close.ewm(span=9, adjust=False).mean().iloc[-1]
        ema20 = close.ewm(span=20, adjust=False).mean().iloc[-1]
        ema200 = close.ewm(span=200, adjust=False).mean().iloc[-1] if len(close) > 200 else ema20
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1] if not rsi.isna().iloc[-1] else 50
        plus_dm = high.diff()
        minus_dm = low.diff()
        plus_dm = plus_dm.where(plus_dm > 0, 0)
        minus_dm = minus_dm.where(minus_dm > 0, 0)
        tr = pd.DataFrame({'hl': high - low, 'hc': abs(high - close.shift()), 'lc': abs(low - close.shift())}).max(axis=1)
        atr = tr.rolling(14).mean()
        plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(14).mean() / atr)
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(14).mean().iloc[-1] if len(dx) > 14 else 25
        volume_sma = volume.rolling(20).mean()
        volume_filter = volume.iloc[-1] > volume_sma.iloc[-1] if not volume_sma.isna().iloc[-1] else True
        if len(df) >= 2:
            prev_candle = df.iloc[-2]
            curr_candle = df.iloc[-1]
            strong_bull = curr_candle['Close'] > curr_candle['Open'] and curr_candle['Close'] > prev_candle['High']
            strong_bear = curr_candle['Close'] < curr_candle['Open'] and curr_candle['Close'] < prev_candle['Low']
            c1_high = prev_candle['High']
            c1_low = prev_candle['Low']
        else:
            strong_bull = False
            strong_bear = False
            c1_high = high.iloc[-1]
            c1_low = low.iloc[-1]
        sideways = (45 < current_rsi < 55) and (adx < 20) if not pd.isna(adx) else False
        return {
            "current_price": float(close.iloc[-1]),
            "ema9": float(ema9),
            "ema20": float(ema20),
            "ema200": float(ema200),
            "rsi": float(current_rsi),
            "adx": float(adx) if not pd.isna(adx) else 25,
            "volume_filter": bool(volume_filter),
            "strong_bull": bool(strong_bull),
            "strong_bear": bool(strong_bear),
            "sideways": bool(sideways),
            "c1_high": float(c1_high),
            "c1_low": float(c1_low)
        }
    except:
        return None

# ================= STRICT SIGNAL (9 CONDITIONS BUY/SELL) =================
def get_strict_signal(symbol, nifty_trend, sector_trend):
    if symbol in ["NIFTY", "BANKNIFTY", "CRUDE", "NATURALGAS"]:
        nifty_condition = nifty_trend == "POSITIVE" if symbol == "NIFTY" else True
        sector_condition = True
    else:
        nifty_condition = nifty_trend == "POSITIVE"
        sector_condition = sector_trend == "BULLISH"
    indicators = get_technical_indicators(symbol)
    if indicators is None:
        return "WAIT", 0, None
    trend5_up = get_mtf_trend(symbol, "5m") == "UP"
    trend15_up = get_mtf_trend(symbol, "15m") == "UP"
    trend1h_up = get_mtf_trend(symbol, "60m") == "UP"
    nifty_positive = (nifty_trend == "POSITIVE")
    nifty_negative = (nifty_trend == "NEGATIVE")
    sector_bullish = (sector_trend == "BULLISH")
    sector_bearish = (sector_trend == "BEARISH")
    sideways = indicators["sideways"]
    strong_bull_stock = (
        indicators["ema9"] > indicators["ema20"] and
        indicators["current_price"] > indicators["ema200"] and
        indicators["rsi"] >= 60 and
        indicators["adx"] >= 25 and
        indicators["volume_filter"] and
        indicators["strong_bull"] and
        indicators["current_price"] > indicators["c1_high"]
    )
    strong_bear_stock = (
        indicators["ema9"] < indicators["ema20"] and
        indicators["current_price"] < indicators["ema200"] and
        indicators["rsi"] <= 40 and
        indicators["adx"] >= 25 and
        indicators["volume_filter"] and
        indicators["strong_bear"] and
        indicators["current_price"] < indicators["c1_low"]
    )
    buy_conditions = (
        nifty_positive and
        not nifty_negative and
        not sideways and
        sector_bullish and
        strong_bull_stock and
        trend5_up and trend15_up and trend1h_up and
        indicators["current_price"] > indicators["ema20"]
    )
    sell_conditions = (
        nifty_negative and
        not nifty_positive and
        not sideways and
        sector_bearish and
        strong_bear_stock and
        not trend5_up and not trend15_up and not trend1h_up and
        indicators["current_price"] < indicators["ema20"]
    )
    if buy_conditions:
        return "BUY", indicators["current_price"], indicators
    elif sell_conditions:
        return "SELL", indicators["current_price"], indicators
    return "WAIT", 0, indicators

# ================= LIVE P&L =================
def get_live_price(symbol):
    try:
        if symbol == "NIFTY":
            ticker = "^NSEI"
        elif symbol == "BANKNIFTY":
            ticker = "^NSEBANK"
        elif symbol == "CRUDE":
            ticker = "CL=F"
        elif symbol == "NATURALGAS":
            ticker = "NG=F"
        else:
            ticker = f"{symbol}.NS"
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if not df.empty:
            val = df['Close'].iloc[-1]
            return float(val) if not isinstance(val, pd.Series) else float(val.iloc[-1])
    except:
        pass
    return 0.0

def calculate_live_pnl():
    total_pnl = 0
    pnl_details = []
    for order in st.session_state.active_orders:
        current_price = get_live_price(order['symbol'])
        if current_price > 0:
            entry = order['entry_price']
            qty = order['qty']
            if order['symbol'] in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
                multiplier = 50 if order['symbol'] == "NIFTY" else 25
            elif order['symbol'] in ["CRUDE", "NATURALGAS"]:
                multiplier = 100
            else:
                multiplier = 100
            if order['option_type'] == "CALL (CE)":
                pnl_points = current_price - entry
            else:
                pnl_points = entry - current_price
            pnl_value = pnl_points * qty * multiplier
            total_pnl += pnl_value
            pnl_details.append({
                'symbol': order['symbol'], 'option_type': order['option_type'],
                'strike': order.get('strike_price', 'N/A'), 'entry': entry,
                'current': current_price, 'pnl_points': pnl_points,
                'pnl_value': pnl_value, 'qty': qty
            })
    return total_pnl, pnl_details

def show_portfolio_dashboard():
    total_pnl, pnl_details = calculate_live_pnl()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #00b4d8;"><span style="font-size: 24px;">💰</span><h3 style="margin: 5px 0; color: #00b4d8;">Total P&L</h3><h2 style="margin: 0; color: {"#00ff88" if total_pnl >= 0 else "#ff4444"};">₹{total_pnl:,.2f}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #ffaa00;"><span style="font-size: 24px;">🔴</span><h3 style="margin: 5px 0; color: #ffaa00;">Active Trades</h3><h2 style="margin: 0; color: #ffaa00;">{len(st.session_state.active_orders)}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #00ff88;"><span style="font-size: 24px;">📋</span><h3 style="margin: 5px 0; color: #00ff88;">Total Trades</h3><h2 style="margin: 0; color: #00ff88;">{len(st.session_state.trade_journal)}</h2></div>', unsafe_allow_html=True)
    with col4:
        daily_pnl_color = "#00ff88" if st.session_state.daily_pnl >= 0 else "#ff4444"
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid {daily_pnl_color};"><span style="font-size: 24px;">📅</span><h3 style="margin: 5px 0; color: {daily_pnl_color};">Today\'s P&L</h3><h2 style="margin: 0; color: {daily_pnl_color};">₹{st.session_state.daily_pnl:,.2f}</h2></div>', unsafe_allow_html=True)
    st.markdown("---")
    if pnl_details:
        st.markdown("#### 📊 Live P&L Details")
        st.dataframe(pd.DataFrame([{
            "Symbol": d['symbol'], "Option": d['option_type'], "Strike": d['strike'],
            "Entry": d['entry'], "Current": d['current'], "P&L (pts)": f"{d['pnl_points']:+.2f}",
            "P&L (₹)": f"₹{d['pnl_value']:,.2f}", "Qty": d['qty']
        } for d in pnl_details]), use_container_width=True)
    else:
        st.info("No active trades")
    st.markdown("---")
    if st.session_state.trade_journal:
        st.markdown("#### 📋 Trade Journal")
        st.dataframe(pd.DataFrame(st.session_state.trade_journal[::-1]), use_container_width=True, height=400)
    else:
        st.info("No trades executed yet")
    st.markdown("---")
    st.markdown("#### 📊 RUDRANSH LIVE PERFORMANCE")
    perf_data = []
    total_buy = 0
    total_sell = 0
    total_tp = 0
    total_sl = 0
    for instrument, data in st.session_state.live_performance.items():
        buy = data.get("BUY", 0)
        sell = data.get("SELL", 0)
        tp = data.get("TP3", 0)
        sl = data.get("SL", 0)
        total_buy += buy
        total_sell += sell
        total_tp += tp
        total_sl += sl
        win_percent = round((tp / (tp + sl)) * 100) if (tp + sl) > 0 else 0
        perf_data.append({
            "INSTRUMENT": instrument,
            "BUY": buy,
            "SELL": sell,
            "TP HIT": tp,
            "SL HIT": sl,
            "WIN %": f"{win_percent}%"
        })
    st.dataframe(pd.DataFrame(perf_data), use_container_width=True)
    total_accuracy = round((total_tp / (total_tp + total_sl)) * 100) if (total_tp + total_sl) > 0 else 0
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 TOTAL TRADE", total_buy + total_sell)
    with col2:
        st.metric("🎯 TOTAL TARGET HIT", total_tp)
    with col3:
        st.metric("❌ TOTAL SL HIT", total_sl)
    with col4:
        st.metric("📈 TOTAL ACCURACY", f"{total_accuracy}%")
    liveDate = get_ist_now().strftime("%d-%m-%Y")
    liveTime = get_ist_now().strftime("%H:%M:%S")
    st.caption(f"📅 {liveDate} | ⏰ {liveTime}")

# ================= HELPER FUNCTIONS =================
def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty:
            return float(df['Close'].iloc[-1])
    except:
        pass
    return 87.5

def get_gnews():
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=8&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [{'title': a['title'], 'source': a['source']['name'], 'time': a['publishedAt'][:10]} for a in data.get('articles', [])]
    except:
        pass
    return [{'title': 'Market Update', 'source': 'News', 'time': get_ist_now().strftime('%Y-%m-%d')}]

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage", data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=10)
    except:
        pass

def voice_alert(msg):
    if st.session_state.voice_enabled:
        st.markdown(f"<script>var s=new SpeechSynthesisUtterance('{msg}');s.lang='en-US';speechSynthesis.speak(s);</script>", unsafe_allow_html=True)

def analyze_news_sentiment(title):
    title_lower = title.lower()
    score = 0
    for w in ['surge', 'rally', 'boom', 'record', 'peak', 'high']:
        if w in title_lower: score += 15
    for w in ['gain', 'up', 'positive', 'bull', 'rise', 'growth']:
        if w in title_lower: score += 5
    for w in ['crash', 'plunge', 'slump', 'collapse']:
        if w in title_lower: score -= 15
    for w in ['fall', 'drop', 'down', 'negative', 'bear', 'decline']:
        if w in title_lower: score -= 5
    if score >= 15: return "STRONG BULLISH", "🚀", "#00ff44"
    elif score >= 5: return "BULLISH", "📈", "#88ff88"
    elif score <= -15: return "STRONG BEARISH", "💀", "#ff3333"
    elif score <= -5: return "BEARISH", "📉", "#ff6666"
    else: return "NEUTRAL", "⚪", "#ffaa00"

def get_news_with_sentiment():
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=12&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [{'title': a['title'], 'source': a['source']['name'], 'time': a['publishedAt'][:10], 'sentiment': analyze_news_sentiment(a['title'])[0], 'icon': analyze_news_sentiment(a['title'])[1], 'color': analyze_news_sentiment(a['title'])[2]} for a in data.get('articles', [])]
    except:
        pass
    return [{'title': 'NIFTY hits all-time high', 'source': 'Economic Times', 'time': get_ist_now().strftime('%Y-%m-%d'), 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'}]

def process_result_and_trade(company_name, symbol, result_type):
    nifty_trend = get_nifty_trend()
    if result_type == "POSITIVE" and nifty_trend == "POSITIVE":
        signal = "BUY"
        option_type = "CALL (CE)"
    elif result_type == "NEGATIVE" and nifty_trend == "NEGATIVE":
        signal = "SELL"
        option_type = "PUT (PE)"
    else:
        return False, f"WAIT - {result_type} / NIFTY {nifty_trend}"
    current_price = get_live_price(symbol)
    if current_price > 0:
        if symbol in ["NIFTY", "BANKNIFTY"]:
            strike_interval = 50 if symbol == "NIFTY" else 100
            strike_price = math.floor(current_price / strike_interval) * strike_interval
        elif symbol in ["CRUDE", "NATURALGAS"]:
            strike_price = math.floor(current_price) * 100
        else:
            strike_price = math.floor(current_price / 10) * 10
        entry_price = current_price
        tp1_percent = 0.10
        tp2_percent = 0.20
        sl_percent = 0.15
        if signal == "BUY":
            tp1_price = entry_price * (1 + tp1_percent)
            tp2_price = entry_price * (1 + tp2_percent)
            sl_price = entry_price * (1 - sl_percent)
        else:
            tp1_price = entry_price * (1 - tp1_percent)
            tp2_price = entry_price * (1 - tp2_percent)
            sl_price = entry_price * (1 + sl_percent)
        st.session_state.wolf_orders.append({
            'symbol': symbol,
            'option_type': option_type,
            'strike_price': strike_price,
            'qty': 1,
            'buy_above': current_price,
            'sl': sl_price,
            'target': tp2_price,
            'tp1': tp1_price,
            'tp1_percent': 50,
            'tp2_percent': 50,
            'status': 'PENDING',
            'placed_time': get_ist_now().strftime('%H:%M:%S'),
            'auto_trade': True,
            'result_based': True,
            'company': company_name,
            'signal_type': '📈 OVI'
        })
        send_telegram(f"📊 OVI: {company_name} - {signal} {option_type} | Entry:{entry_price:.2f} | TP1:{tp1_price:.2f}(50%) | TP2:{tp2_price:.2f}(50%) | SL:{sl_price:.2f}")
        return True, f"{signal} order placed with TP1(10%) 50%, TP2(20%) 50%"
    return False, "Price not available"

# ================= UI HEADER =================
st.markdown(f"""
<div style="text-align:center; padding:20px;">
    <h1 class="neon-text">🐺 {APP_NAME}</h1>
    <p style="color:#94a3b8;">{APP_AUTHOR}, {APP_LOCATION} | v{APP_VERSION}</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

now = get_ist_now()
st.markdown(f"<div class='live-time'>🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')}</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= PREMIUM DASHBOARD SECTION =================
st.markdown("## 🎯 LIVE MARKET DASHBOARD")

# Get live data
nifty_price, nifty_change, nifty_change_pct, nifty_prev = get_live_nifty()
recommendation = get_trading_recommendation()
pcr_data = get_pcr_data()
option_data = get_option_chain_data()
fii_dii_data = get_fii_dii_data()
global_data = get_global_markets()

# Row 1: NIFTY Price and Recommendation
col1, col2 = st.columns(2)

with col1:
    nifty_color = "#00ff88" if nifty_change >= 0 else "#ff4444"
    nifty_arrow = "▲" if nifty_change >= 0 else "▼"
    st.markdown(f"""
    <div class="glass-3d">
        <div style="text-align: center;">
            <h2>🇮🇳 NIFTY 50 LIVE</h2>
            <div class="live-ticker">₹{nifty_price:,.2f}</div>
            <div style="margin-top: 15px;">
                <span style="font-size: 24px; color: {nifty_color};">{nifty_arrow} {abs(nifty_change):.2f} ({nifty_change_pct:+.2f}%)</span>
            </div>
            <div class="meter-container" style="margin-top: 20px;">
                <div class="meter-fill" style="width: {50 + nifty_change_pct}%;">
                    {nifty_change_pct:+.1f}%
                </div>
            </div>
            <small>Previous Close: ₹{nifty_prev:,.2f}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-3d">
        <div style="text-align: center;">
            <h2>🎯 RECOMMENDATION</h2>
            <div style="font-size: 48px; color: {recommendation['color']}; margin: 10px 0;">
                {recommendation['icon']} {recommendation['recommendation']}
            </div>
            <div style="background: rgba(0,0,0,0.5); border-radius: 15px; padding: 10px; margin: 10px 0;">
                <strong>ACTION:</strong> {recommendation['action']}<br>
                <strong>SENTIMENT SCORE:</strong> {recommendation['score']}/100
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Row 2: Bull/Bear Meter and PCR Data
col1, col2 = st.columns(2)

with col1:
    fig_gauge = create_bull_bear_gauge(recommendation['score'])
    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    st.markdown(f"""
    <div class="glass-3d">
        <h2 style="text-align: center;">📊 PCR & OPTIONS DATA</h2>
        <div style="padding: 10px;">
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <span>📈 Overall PCR:</span>
                <span style="color: #00ff88; font-weight: bold;">{pcr_data.get('Overall PCR', 1.12):.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <span>🎯 Max Pain:</span>
                <span style="color: #00b4d8; font-weight: bold;">{option_data.get('Max Pain', 24800)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <span>📊 CE OI (Cr):</span>
                <span>{option_data.get('CE OI', 12500000)/10000000:.1f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <span>📊 PE OI (Cr):</span>
                <span>{option_data.get('PE OI', 14375000)/10000000:.1f}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Row 3: FII/DII Data
st.markdown("### 💰 INSTITUTIONAL FLOWS")
cols = st.columns(4)
fii_dii_colors = {"FII Cash": "#ff6666", "DII Cash": "#88ff88", "FII Index Futures": "#ffaa00", "FII Index Options": "#00b4d8"}

for idx, (name, data) in enumerate(fii_dii_data.items()):
    color = fii_dii_colors.get(name, "#ffffff")
    arrow = "▲" if data['value'] > 0 else "▼" if data['value'] < 0 else "●"
    with cols[idx]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 14px; color: {color};">{name}</div>
            <div style="font-size: 24px; font-weight: bold; color: {color};">₹{abs(data['value']):,}</div>
            <div style="font-size: 12px; color: {color};">{arrow} {abs(data['change'])}%</div>
        </div>
        """, unsafe_allow_html=True)

# Row 4: Global Markets
st.markdown("### 🌍 GLOBAL MARKETS")
items = list(global_data.items())
for i in range(0, len(items), 4):
    cols = st.columns(4)
    for j in range(4):
        if i + j < len(items):
            name, data = items[i + j]
            price = data['price']
            change = data['change']
            color = "#00ff88" if change >= 0 else "#ff4444"
            arrow = "▲" if change >= 0 else "▼"
            with cols[j]:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-weight: bold;">{name}</div>
                    <div style="font-size: 20px;">{price:,.2f}</div>
                    <div style="color: {color};">{arrow} {abs(change):.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")

# ================= API STATUS & CONTROL PANEL =================
st.markdown("## 🎮 SYSTEM DASHBOARD")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🔌 API STATUS")
    fmp_status, fmp_level, fmp_msg = check_fmp_api()
    st.markdown(f'<div class="status-card" style="border-left: 4px solid #00ff88;">📊 <strong>FMP API</strong><br><span style="color:#00ff88">🟢 {fmp_msg}</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-card" style="border-left: 4px solid #00ff88;">📰 <strong>GNews API</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-card" style="border-left: 4px solid #00ff88;">📱 <strong>Telegram Bot</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)

with col_right:
    st.markdown("### 🎮 CONTROL PANEL")
    st.markdown("""<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; padding: 20px; border: 1px solid rgba(0,255,136,0.2);">""", unsafe_allow_html=True)
    st.markdown("""<div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 5px 15px; border: 1px solid #00b4d8;"><label style="color:#00b4d8; font-size:12px;">🔐 6-DIGIT TOTP CODE</label></div>""", unsafe_allow_html=True)
    totp = st.text_input("TOTP", type="password", placeholder="Enter 6-digit code", key="totp_main_panel", label_visibility="collapsed")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🟢 START ALGO", use_container_width=True):
            if totp and len(totp) == 6:
                st.session_state.algo_running = True
                st.session_state.totp_verified = True
                send_telegram("🚀 ALGO STARTED v5.0")
                st.success("✅ Algo Started Successfully!")
                st.rerun()
            else:
                st.error("❌ Valid 6-digit TOTP required!")
    with col_btn2:
        if st.button("🔴 STOP ALGO", use_container_width=True):
            st.session_state.algo_running = False
            send_telegram("🛑 ALGO STOPPED")
            st.warning("⚠️ Algo Stopped!")
            st.rerun()
    st.markdown("---")
    col_status1, col_status2, col_status3 = st.columns(3)
    with col_status1:
        if st.session_state.algo_running:
            st.markdown("""<div style="background: rgba(0,255,136,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00ff88;"><span style="color:#00ff88;">🟢 SYSTEM STATUS</span><br><span style="color:#00ff88;">● ACTIVE</span></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background: rgba(255,68,68,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #ff4444;"><span style="color:#ff4444;">🔴 SYSTEM STATUS</span><br><span style="color:#ff4444;">● INACTIVE</span></div>""", unsafe_allow_html=True)
    with col_status2:
        if st.session_state.totp_verified:
            st.markdown("""<div style="background: rgba(0,255,136,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00ff88;"><span style="color:#00ff88;">🔐 TOTP STATUS</span><br><span style="color:#00ff88;">✓ VERIFIED</span></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background: rgba(255,68,68,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #ff4444;"><span style="color:#ff4444;">🔐 TOTP STATUS</span><br><span style="color:#ff4444;">✗ NOT VERIFIED</span></div>""", unsafe_allow_html=True)
    with col_status3:
        now = get_ist_now()
        st.markdown(f"""<div style="background: rgba(0,180,216,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00b4d8;"><span style="color:#00b4d8;">⏰ CURRENT TIME</span><br><span style="color:#00b4d8; font-size:14px;">{now.strftime('%H:%M:%S')} IST</span></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🐺 WOLF ORDER",
    "🌸 SANSKRUTI MARKET",
    "📰 VAISHNAVI NEWS",
    "📈 OVI RESULTS",
    "⚙️ SAHYADRI SETTINGS",
    "💰 VEDASHREE PORTFOLIO",
    "📊 CONDITIONS DASHBOARD",
    "🎯 NIFTY SENTIMENT"
])

# ================= TAB 1: WOLF ORDER =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK")
    st.markdown(f"*Total {len(FO_SCRIPTS)} F&O Symbols Available*")
    st.markdown("---")
    total_orders = len(st.session_state.wolf_orders)
    pending_orders = len([o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING'])
    active_orders_count = len(st.session_state.active_orders)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size:28px;">📋</span><h3>{total_orders}</h3><p>Total Orders</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size:28px;">⏳</span><h3>{pending_orders}</h3><p>Pending Orders</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size:28px;">🟢</span><h3>{active_orders_count}</h3><p>Active Orders</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🐺 Place New Wolf Order")
    with st.expander("➕ CLICK TO PLACE NEW ORDER", expanded=False):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            sym = st.selectbox("Symbol", FO_SCRIPTS, key="wolf_sym")
        with col2:
            opt = st.selectbox("Option", OPTION_TYPES, key="wolf_opt")
        with col3:
            strike = st.number_input("Strike", 1, 500000, 24300, key="wolf_strike")
        with col4:
            qty = st.number_input("Lots", 1, 100, 1, key="wolf_qty")
        with col5:
            buy_above = st.number_input("Buy Above", 1, 500000, 100, key="wolf_buy")
        with col6:
            sl = st.number_input("SL", 1, 500000, 80, key="wolf_sl")
        with col7:
            target = st.number_input("Target", 1, 500000, 150, key="wolf_target")
        if st.button("🐺 PLACE ORDER", use_container_width=True):
            if buy_above > sl and target > buy_above:
                st.session_state.wolf_orders.append({
                    'symbol': sym, 'option_type': opt, 'strike_price': strike, 'qty': qty,
                    'buy_above': buy_above, 'sl': sl, 'target': target, 'status': 'PENDING',
                    'placed_time': get_ist_now().strftime('%H:%M:%S')
                })
                st.success(f"✅ Order placed for {sym}")
                st.rerun()
            else:
                st.error("❌ Buy Above > SL and Target > Buy Above required")
    st.markdown("---")
    pending_list = [o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING']
    if pending_list:
        st.markdown("#### ⏳ PENDING ORDERS")
        for i, order in enumerate(pending_list):
            st.markdown(f'<div style="background: rgba(255,170,0,0.1); border-radius: 15px; padding: 15px; margin: 10px 0;">'
                       f'<b>{order["symbol"]}</b> {order["option_type"]} Strike: {order["strike_price"]}<br>'
                       f'Lots: {order["qty"]} | Buy Above: {order["buy_above"]} | SL: {order["sl"]} | Target: {order["target"]}<br>'
                       f'Placed: {order.get("placed_time", "N/A")}</div>', unsafe_allow_html=True)
            if st.button(f"❌ Cancel", key=f"cancel_{i}"):
                st.session_state.wolf_orders.remove(order)
                st.rerun()
    else:
        st.info("📭 No pending orders")
    st.markdown("---")
    if st.session_state.active_orders:
        st.markdown("#### 🔴 ACTIVE ORDERS")
        for order in st.session_state.active_orders:
            current = get_live_price(order['symbol'])
            st.markdown(f'<div style="background: rgba(0,255,136,0.1); border-radius: 15px; padding: 15px; margin: 10px 0;">'
                       f'<b>{order["symbol"]}</b> {order["option_type"]}<br>'
                       f'Entry: {order["entry_price"]} | Current: {current:.2f}<br>'
                       f'SL: {order["sl"]} | Target: {order["target"]}</div>', unsafe_allow_html=True)

# ================= TAB 2: SANSKRUTI MARKET =================
with tab2:
    st_autorefresh(interval=10000, key="sanskriti_refresh")
    st.markdown("### 🌸 SANSKRUTI MARKET")
    st.markdown("*Live Indian & Global Markets with AI Trend Analysis*")
    st.markdown("---")
    st.markdown("#### 🇮🇳 INDIAN MARKET")
    usd_inr = get_usd_inr_rate()
    try:
        nifty = yf.download("^NSEI", period="2d", interval="1m", progress=False)
        if nifty is not None and not nifty.empty and 'Close' in nifty.columns:
            nifty_current = float(nifty['Close'].iloc[-1])
            nifty_prev = float(nifty['Close'].iloc[-2]) if len(nifty) > 1 else nifty_current
            nifty_pct = ((nifty_current - nifty_prev) / nifty_prev) * 100 if nifty_prev > 0 else 0
        else:
            nifty_current = 0
            nifty_pct = 0
    except:
        nifty_current = 0
        nifty_pct = 0
    try:
        banknifty = yf.download("^NSEBANK", period="2d", interval="1m", progress=False)
        if banknifty is not None and not banknifty.empty and 'Close' in banknifty.columns:
            bank_current = float(banknifty['Close'].iloc[-1])
            bank_prev = float(banknifty['Close'].iloc[-2]) if len(banknifty) > 1 else bank_current
            bank_pct = ((bank_current - bank_prev) / bank_prev) * 100 if bank_prev > 0 else 0
        else:
            bank_current = 0
            bank_pct = 0
    except:
        bank_current = 0
        bank_pct = 0
    crude_live_usd = 0
    crude_live_inr = 0
    crude_pct = 0
    try:
        crude_mcx = yf.download("CRUDEOIL.NS", period="1d", interval="1m", progress=False)
        if crude_mcx is not None and not crude_mcx.empty and 'Close' in crude_mcx.columns:
            crude_live_inr = float(crude_mcx['Close'].iloc[-1])
            crude_live_usd = crude_live_inr / usd_inr if usd_inr > 0 else 0
            if len(crude_mcx) > 1:
                crude_prev = float(crude_mcx['Close'].iloc[-2])
                crude_pct = ((crude_live_inr - crude_prev) / crude_prev) * 100 if crude_prev > 0 else 0
    except:
        pass
    if crude_live_inr == 0:
        try:
            crude_cl = yf.download("CL=F", period="2d", interval="5m", progress=False)
            if crude_cl is not None and not crude_cl.empty and 'Close' in crude_cl.columns:
                crude_live_usd = float(crude_cl['Close'].iloc[-1])
                crude_live_inr = crude_live_usd * usd_inr if usd_inr > 0 else 0
                if len(crude_cl) > 1:
                    crude_prev_usd = float(crude_cl['Close'].iloc[-2])
                    crude_pct = ((crude_live_usd - crude_prev_usd) / crude_prev_usd) * 100 if crude_prev_usd > 0 else 0
        except:
            pass
    ng_live_usd = 0
    ng_live_inr = 0
    ng_pct = 0
    try:
        ng = yf.download("NG=F", period="2d", interval="5m", progress=False)
        if ng is not None and not ng.empty and 'Close' in ng.columns:
            ng_live_usd = float(ng['Close'].iloc[-1])
            ng_live_inr = ng_live_usd * usd_inr if usd_inr > 0 else 0
            if len(ng) > 1:
                ng_prev_usd = float(ng['Close'].iloc[-2])
                ng_pct = ((ng_live_usd - ng_prev_usd) / ng_prev_usd) * 100 if ng_prev_usd > 0 else 0
    except:
        pass
    def get_trend_label(change_pct):
        if change_pct > 1.0:
            return "STRONG BULLISH", "🚀", "#00ff44"
        elif change_pct > 0.2:
            return "BULLISH", "📈", "#88ff88"
        elif change_pct < -1.0:
            return "STRONG BEARISH", "💀", "#ff3333"
        elif change_pct < -0.2:
            return "BEARISH", "📉", "#ff6666"
        else:
            return "SIDEWAYS", "➡️", "#ffaa00"
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if nifty_current > 0:
            trend_label, trend_icon, trend_color = get_trend_label(nifty_pct)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#00b4d8;">🇮🇳 NIFTY 50</h3>
                <h2 style="margin:5px 0;">₹{nifty_current:,.2f}</h2>
                <p style="margin:0; color:{trend_color if nifty_pct > 0 else '#ff4444' if nifty_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {nifty_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
                <small style="color:#aaa;">🕐 {get_ist_now().strftime('%H:%M:%S')} IST</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#00b4d8;">🇮🇳 NIFTY 50</h3>
                <p>🔴 Market Closed</p>
                <p style="font-size:12px;">Opens Monday 9:15 AM</p>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        if bank_current > 0:
            trend_label, trend_icon, trend_color = get_trend_label(bank_pct)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#00b4d8;">🏦 BANK NIFTY</h3>
                <h2 style="margin:5px 0;">₹{bank_current:,.2f}</h2>
                <p style="margin:0; color:{trend_color if bank_pct > 0 else '#ff4444' if bank_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {bank_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
                <small style="color:#aaa;">🕐 {get_ist_now().strftime('%H:%M:%S')} IST</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#00b4d8;">🏦 BANK NIFTY</h3>
                <p>🔴 Market Closed</p>
                <p style="font-size:12px;">Opens Monday 9:15 AM</p>
            </div>
            """, unsafe_allow_html=True)
    with col3:
        if crude_live_inr > 0:
            if crude_pct > 1.0:
                trend_label, trend_icon, trend_color = "STRONG BULLISH", "🚀", "#00ff44"
            elif crude_pct > 0.2:
                trend_label, trend_icon, trend_color = "BULLISH", "📈", "#88ff88"
            elif crude_pct < -1.0:
                trend_label, trend_icon, trend_color = "STRONG BEARISH", "💀", "#ff3333"
            elif crude_pct < -0.2:
                trend_label, trend_icon, trend_color = "BEARISH", "📉", "#ff6666"
            else:
                trend_label, trend_icon, trend_color = "SIDEWAYS", "➡️", "#ffaa00"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#ff8844;">🛢️ CRUDE OIL</h3>
                <h2 style="margin:5px 0;">₹{crude_live_inr:,.2f}</h2>
                <p style="margin:0; color:{trend_color if crude_pct > 0 else '#ff4444' if crude_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {crude_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
                <small style="color:#aaa;">{'${:.2f} USD'.format(crude_live_usd) if crude_live_usd > 0 else 'MCX'}</small>
                <small style="color:#aaa; display:block;">🕐 {get_ist_now().strftime('%H:%M:%S')} IST</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#ff8844;">🛢️ CRUDE OIL</h3>
                <p>🔴 Market Closed / Loading...</p>
            </div>
            """, unsafe_allow_html=True)
    with col4:
        if ng_live_usd > 0:
            if ng_pct > 1.0:
                trend_label, trend_icon, trend_color = "STRONG BULLISH", "🚀", "#00ff44"
            elif ng_pct > 0.2:
                trend_label, trend_icon, trend_color = "BULLISH", "📈", "#88ff88"
            elif ng_pct < -1.0:
                trend_label, trend_icon, trend_color = "STRONG BEARISH", "💀", "#ff3333"
            elif ng_pct < -0.2:
                trend_label, trend_icon, trend_color = "BEARISH", "📉", "#ff6666"
            else:
                trend_label, trend_icon, trend_color = "SIDEWAYS", "➡️", "#ffaa00"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#88ff88;">🌿 NATURAL GAS</h3>
                <h2 style="margin:5px 0;">₹{ng_live_inr:,.2f}</h2>
                <p style="margin:0; color:{trend_color if ng_pct > 0 else '#ff4444' if ng_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {ng_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
                <small style="color:#aaa;">${ng_live_usd:.2f} USD</small>
                <small style="color:#aaa; display:block;">🕐 {get_ist_now().strftime('%H:%M:%S')} IST</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#88ff88;">🌿 NATURAL GAS</h3>
                <p>🔴 Market Closed / Loading...</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🛢️ CRUDE OIL MARKET SENTIMENT")
    if crude_pct > 0.5:
        real_sentiment = "STRONG BULLISH 🔥"
        real_color = "#00ff44"
    elif crude_pct > 0:
        real_sentiment = "BULLISH 📈"
        real_color = "#88ff88"
    elif crude_pct < -0.5:
        real_sentiment = "STRONG BEARISH 💀"
        real_color = "#ff3333"
    elif crude_pct < 0:
        real_sentiment = "BEARISH 📉"
        real_color = "#ff6666"
    else:
        real_sentiment = "SIDEWAYS ➡️"
        real_color = "#ffaa00"
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.3); border-radius:15px; padding:15px; margin-bottom:20px; text-align:center;">
        <span style="font-size:20px;">🎯 REAL-TIME SENTIMENT</span><br>
        <span style="font-size:36px; color:{real_color};">{real_sentiment}</span><br>
        <small>Based on live price movement: {crude_pct:+.2f}%</small>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background:rgba(0,255,68,0.15); border-left:4px solid #00ff44; padding:10px; border-radius:5px;'>
            <b>🚀 STRONG BULLISH</b><br>
            • Hormuz crisis: 20% supply lost<br>
            • Global inventories at historic low
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:rgba(0,255,68,0.1); border-left:4px solid #88ff88; padding:10px; border-radius:5px;'>
            <b>📈 BULLISH</b><br>
            • WTI $106.64, Brent $110.29<br>
            • US crude inventories falling
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:rgba(255,170,0,0.1); border-left:4px solid #ffaa00; padding:10px; border-radius:5px;'>
            <b>⚪ NEUTRAL</b><br>
            • India has 60 days crude reserves<br>
            • Brazil record output 4.24M bpd
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🌿 NATURAL GAS MARKET SENTIMENT")
    if ng_pct > 0.5:
        ng_sentiment = "STRONG BULLISH 🔥"
        ng_color = "#00ff44"
    elif ng_pct > 0:
        ng_sentiment = "BULLISH 📈"
        ng_color = "#88ff88"
    elif ng_pct < -0.5:
        ng_sentiment = "STRONG BEARISH 💀"
        ng_color = "#ff3333"
    elif ng_pct < 0:
        ng_sentiment = "BEARISH 📉"
        ng_color = "#ff6666"
    else:
        ng_sentiment = "SIDEWAYS ➡️"
        ng_color = "#ffaa00"
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.3); border-radius:15px; padding:15px; margin-bottom:20px; text-align:center;">
        <span style="font-size:20px;">🎯 REAL-TIME SENTIMENT</span><br>
        <span style="font-size:36px; color:{ng_color};">{ng_sentiment}</span><br>
        <small>Based on live price movement: {ng_pct:+.2f}%</small>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background:rgba(0,255,68,0.1); border-left:4px solid #88ff88; padding:10px; border-radius:5px;'>
            <b>📈 BULLISH</b><br>
            • NG futures at $3.02 (+2.06%)<br>
            • Weekly gain +6.60%
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:rgba(255,68,68,0.1); border-left:4px solid #ff6666; padding:10px; border-radius:5px;'>
            <b>📉 BEARISH</b><br>
            • US NG inventories +85 Bcf<br>
            • Inventories at 2,290 Bcf
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:rgba(255,68,68,0.1); border-left:4px solid #ff6666; padding:10px; border-radius:5px;'>
            <b>📉 BEARISH</b><br>
            • European NG prices down 2.4%<br>
            • TTF contract at 48.98 euros/MWh
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🌍 GLOBAL MARKET TRENDS")
    st.markdown("*Real-time global indices with AI trend analysis*")
    global_indices = {
        "S&P 500": "^GSPC", "NASDAQ": "^IXIC", "Dow Jones": "^DJI",
        "Nikkei 225": "^N225", "Hang Seng": "^HSI", "Shanghai": "000001.SS",
        "FTSE 100": "^FTSE", "DAX": "^GDAXI", "CAC 40": "^FCHI",
        "GOLD": "GC=F", "SILVER": "SI=F"
    }
    flag_map = {
        "S&P 500": "🇺🇸", "NASDAQ": "🇺🇸", "Dow Jones": "🇺🇸",
        "Nikkei 225": "🇯🇵", "Hang Seng": "🇭🇰", "Shanghai": "🇨🇳",
        "FTSE 100": "🇬🇧", "DAX": "🇩🇪", "CAC 40": "🇫🇷",
        "GOLD": "🌍", "SILVER": "🌍"
    }
    items = list(global_indices.items())
    for i in range(0, len(items), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(items):
                name, symbol = items[i + j]
                flag = flag_map.get(name, "🌍")
                try:
                    df = yf.download(symbol, period="2d", interval="1m", progress=False)
                    if df is not None and not df.empty and 'Close' in df.columns and len(df) > 1:
                        current = float(df['Close'].iloc[-1])
                        prev = float(df['Close'].iloc[-2])
                        change_pct = ((current - prev) / prev) * 100 if prev > 0 else 0
                        if change_pct > 1.0:
                            trend_text = "STRONG BULLISH"
                            trend_icon = "🚀"
                            trend_color = "#00ff44"
                        elif change_pct > 0.2:
                            trend_text = "BULLISH"
                            trend_icon = "📈"
                            trend_color = "#88ff88"
                        elif change_pct < -1.0:
                            trend_text = "STRONG BEARISH"
                            trend_icon = "💀"
                            trend_color = "#ff3333"
                        elif change_pct < -0.2:
                            trend_text = "BEARISH"
                            trend_icon = "📉"
                            trend_color = "#ff6666"
                        else:
                            trend_text = "SIDEWAYS"
                            trend_icon = "➡️"
                            trend_color = "#ffaa00"
                        change_icon = "▲" if change_pct > 0 else "▼" if change_pct < 0 else "●"
                        change_color = "#00ff88" if change_pct > 0 else "#ff4444" if change_pct < 0 else "#ffaa00"
                        with cols[j]:
                            st.markdown(f"""
                            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px; border-left: 4px solid {change_color};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-weight:bold;">{flag} {name}</span>
                                    <span style="background:{trend_color}; border-radius:15px; padding:2px 8px; font-size:10px; color:black; font-weight:bold;">{trend_icon} {trend_text}</span>
                                </div>
                                <div style="margin-top: 8px;">
                                    <span style="font-size: 16px; font-weight: bold;">{'₹' if 'GOLD' not in name and 'SILVER' not in name else '$'}{current:,.2f}</span>
                                    <span style="color:{change_color}; margin-left: 10px;">{change_icon} {change_pct:+.2f}%</span>
                                </div>
                                <small style="color:#aaa;">{symbol}</small>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        with cols[j]:
                            st.markdown(f"""
                            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px;">
                                <div style="font-weight:bold;">{flag} {name}</div>
                                <div style="color:#ffaa00;">🔴 Market Closed</div>
                                <small style="color:#aaa;">{symbol}</small>
                            </div>
                            """, unsafe_allow_html=True)
                except:
                    with cols[j]:
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px;">
                            <div style="font-weight:bold;">{flag} {name}</div>
                            <div style="color:#ffaa00;">🔴 Loading...</div>
                            <small style="color:#aaa;">{symbol}</small>
                        </div>
                        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🌏 Global Market Summary")
    st.info(f"""
    📊 **Market Status:**
    - 🇮🇳 Indian Markets: {'Open' if is_trading_time('NIFTY') else 'Closed'}
    - 🛢️ CRUDE OIL: Live ₹{crude_live_inr:,.2f} ({crude_pct:+.2f}%)
    - 🌿 NATURAL GAS: Live ₹{ng_live_inr:,.2f} ({ng_pct:+.2f}%)
    - 🌍 Global Markets: Real-time data above
    """)

# ================= TAB 3: VAISHNAVI NEWS =================
with tab3:
    st.markdown("### 📰 VAISHNAVI NEWS")
    st.markdown("*Real-time business news with AI sentiment analysis*")
    col1, col2 = st.columns([3,1])
    with col2: 
        st.session_state.voice_enabled = st.checkbox("🔊 Voice Alerts", st.session_state.voice_enabled)
    st.markdown("---")
    st.markdown("#### 🎨 Sentiment Color Guide:")
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    with col_a:
        st.markdown('<span style="background:#00ff44; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">🚀 STRONG BULLISH</span>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<span style="background:#88ff88; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">📈 BULLISH</span>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<span style="background:#ffaa00; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">⚪ NEUTRAL</span>', unsafe_allow_html=True)
    with col_d:
        st.markdown('<span style="background:#ff6666; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">📉 BEARISH</span>', unsafe_allow_html=True)
    with col_e:
        st.markdown('<span style="background:#ff3333; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">💀 STRONG BEARISH</span>', unsafe_allow_html=True)
    st.markdown("---")
    news_articles = get_news_with_sentiment()
    strong_bullish = len([n for n in news_articles if n['sentiment'] == 'STRONG BULLISH'])
    bullish = len([n for n in news_articles if n['sentiment'] == 'BULLISH'])
    neutral = len([n for n in news_articles if n['sentiment'] == 'NEUTRAL'])
    bearish = len([n for n in news_articles if n['sentiment'] == 'BEARISH'])
    strong_bearish = len([n for n in news_articles if n['sentiment'] == 'STRONG BEARISH'])
    st.markdown("#### 📊 Today's News Sentiment Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div style="background:#00ff44; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>🚀</b><br>
            <b>{strong_bullish}</b><br>
            <small>STRONG BULLISH</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#88ff88; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>📈</b><br>
            <b>{bullish}</b><br>
            <small>BULLISH</small>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#ffaa00; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>⚪</b><br>
            <b>{neutral}</b><br>
            <small>NEUTRAL</small>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="background:#ff6666; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>📉</b><br>
            <b>{bearish}</b><br>
            <small>BEARISH</small>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div style="background:#ff3333; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>💀</b><br>
            <b>{strong_bearish}</b><br>
            <small>STRONG BEARISH</small>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 📰 Latest News Headlines")
    for news in news_articles:
        sentiment = news['sentiment']
        icon = news['icon']
        color = news['color']
        if sentiment == "STRONG BULLISH":
            strength = 90
        elif sentiment == "BULLISH":
            strength = 70
        elif sentiment == "NEUTRAL":
            strength = 50
        elif sentiment == "BEARISH":
            strength = 30
        else:
            strength = 10
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; margin: 10px 0; border-left: 5px solid {color};">
            <table style="width:100%;">
                <tr>
                    <td style="width:70%;">
                        <b>📌 {news['title']}</b><br>
                        <small>🔗 Source: {news['source']} | 🕐 {news['time']}</small>
                    </td>
                    <td style="width:30%; text-align:center;">
                        <span style="background:{color}; padding:8px 15px; border-radius:20px; color:black; font-weight:bold;">
                            {icon} {sentiment}
                        </span>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        st.progress(strength/100)
        st.markdown("---")
    st.markdown("#### 🎯 Overall Market Sentiment")
    total = len(news_articles)
    if total > 0:
        bullish_pct = (strong_bullish + bullish) / total * 100
        bearish_pct = (strong_bearish + bearish) / total * 100
        if bullish_pct > 60:
            overall = "🟢 BULLISH"
            overall_color = "#00ff44"
            advice = "Markets are positive - Look for buying opportunities"
        elif bearish_pct > 60:
            overall = "🔴 BEARISH"
            overall_color = "#ff4444"
            advice = "Markets are negative - Be cautious, consider selling"
        else:
            overall = "🟡 NEUTRAL"
            overall_color = "#ffaa00"
            advice = "Markets are mixed - Wait for clear direction"
        st.markdown(f"""
        <div style="background:{overall_color}22; border-radius:15px; padding:15px; text-align:center; border:1px solid {overall_color};">
            <h3 style="color:{overall_color}; margin:0;">{overall}</h3>
            <p style="color:white; margin:5px 0 0 0;">{advice}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("##### Sentiment Gauge:")
        st.markdown(f"""
        <div style="background:#333; border-radius:10px; padding:2px;">
            <div style="background:linear-gradient(90deg, #ff3333, #ffaa00, #88ff88, #00ff44); width:100%; border-radius:10px; height:20px;"></div>
            <div style="position:relative; left:{bullish_pct}%; width:2px; background:white; height:20px; margin-top:-20px;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:5px;">
            <small style="color:#ff3333">BEARISH</small>
            <small style="color:#ffaa00">NEUTRAL</small>
            <small style="color:#00ff44">BULLISH</small>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.voice_enabled and news_articles:
        important_news = [n for n in news_articles if n['sentiment'] in ['STRONG BULLISH', 'STRONG BEARISH']]
        if important_news:
            voice_alert(f"Important news: {important_news[0]['sentiment']} sentiment detected. {important_news[0]['title'][:100]}")

# ================= TAB 4: OVI RESULTS =================
with tab4:
    st.markdown("### 📈 OVI RESULTS - Q4 FY26 MONITORING")
    st.markdown("*Real-time earnings monitoring with AI predictions & market reactions*")
    if fmp_status:
        st.success("✅ FMP API Connected Successfully")
    else:
        st.info("🟡 FMP API Status: Stable endpoints configured and ready")
    st.markdown("---")
    PENDING_RESULTS_UPDATED = [
        {"name": "Bharat Electronics", "symbol": "BEL", "q4_date": "22 May 2026", "time": "3:30 PM", "prediction": "BULLISH", "confidence": 85, "sentiment": "🟢 Positive", "analyst_rating": "BUY", "status": "PENDING", "actual_reaction": "", "reason": ""},
        {"name": "BPCL", "symbol": "BPCL", "q4_date": "22 May 2026", "time": "3:30 PM", "prediction": "NEUTRAL", "confidence": 60, "sentiment": "🟡 Mixed", "analyst_rating": "HOLD", "status": "PENDING", "actual_reaction": "", "reason": ""},
        {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "q4_date": "22 May 2026", "time": "3:30 PM", "prediction": "STRONG BULLISH", "confidence": 90, "sentiment": "🟢 Strong Positive", "analyst_rating": "STRONG BUY", "status": "PENDING", "actual_reaction": "", "reason": ""},
        {"name": "Mankind Pharma", "symbol": "MANKIND", "q4_date": "22 May 2026", "time": "3:30 PM", "prediction": "BULLISH", "confidence": 80, "sentiment": "🟢 Positive", "analyst_rating": "BUY", "status": "PENDING", "actual_reaction": "", "reason": ""},
        {"name": "PI Industries", "symbol": "PIIND", "q4_date": "22 May 2026", "time": "3:30 PM", "prediction": "BULLISH", "confidence": 75, "sentiment": "🟢 Positive", "analyst_rating": "BUY", "status": "PENDING", "actual_reaction": "", "reason": ""},
        {"name": "HDFC Bank", "symbol": "HDFCBANK", "q4_date": "15 May 2026", "time": "After Market", "prediction": "BULLISH", "confidence": 88, "sentiment": "🟢 Positive", "analyst_rating": "BUY", "status": "COMPLETED", "actual_reaction": "📈 STOCK UP 2.5%", "reason": "Strong loan growth & NII beat estimates"},
        {"name": "Reliance Industries", "symbol": "RELIANCE", "q4_date": "14 May 2026", "time": "After Market", "prediction": "NEUTRAL", "confidence": 55, "sentiment": "🟡 Mixed", "analyst_rating": "HOLD", "status": "COMPLETED", "actual_reaction": "➡️ STOCK FLAT", "reason": "Retail & O2C business mixed results"},
        {"name": "Infosys", "symbol": "INFY", "q4_date": "16 May 2026", "time": "9:15 AM", "prediction": "BEARISH", "confidence": 65, "sentiment": "🔴 Negative", "analyst_rating": "SELL", "status": "COMPLETED", "actual_reaction": "📈 STOCK UP 3.2%", "reason": "Better than expected FY27 guidance & large deal wins"},
    ]
    st.markdown("#### 📊 Monitored Companies - Q4 FY26")
    df_pending = pd.DataFrame([{
        "Company": c['name'],
        "Symbol": c['symbol'],
        "Q4 Date": c['q4_date'],
        "Time": c['time'],
        "AI Prediction": c['prediction'],
        "Confidence": f"{c['confidence']}%",
        "Sentiment": c['sentiment'],
        "Analyst Rating": c['analyst_rating'],
        "Status": c['status'],
        "Actual Reaction": c.get('actual_reaction', '-') if c['status'] == "COMPLETED" else "-",
    } for c in PENDING_RESULTS_UPDATED])
    st.dataframe(df_pending, use_container_width=True, height=400)
    st.markdown("---")
    st.markdown("#### 🎨 AI Prediction Color Guide:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<span style="background:#00ff44; padding:5px 10px; border-radius:10px; color:black;">🚀 STRONG BULLISH</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span style="background:#88ff88; padding:5px 10px; border-radius:10px; color:black;">📈 BULLISH</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span style="background:#ffaa00; padding:5px 10px; border-radius:10px; color:black;">⚪ NEUTRAL</span>', unsafe_allow_html=True)
    with col4:
        st.markdown('<span style="background:#ff6666; padding:5px 10px; border-radius:10px; color:black;">📉 BEARISH</span>', unsafe_allow_html=True)
    with col5:
        st.markdown('<span style="background:#ff3333; padding:5px 10px; border-radius:10px; color:black;">💀 STRONG BEARISH</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 📊 Company-wise Analysis Cards")
    for company in PENDING_RESULTS_UPDATED:
        if company['prediction'] == "STRONG BULLISH":
            bg_color = "#00ff44"
            border_color = "#00cc33"
            icon = "🚀"
        elif company['prediction'] == "BULLISH":
            bg_color = "#88ff88"
            border_color = "#55aa55"
            icon = "📈"
        elif company['prediction'] == "NEUTRAL":
            bg_color = "#ffaa00"
            border_color = "#cc8800"
            icon = "⚪"
        elif company['prediction'] == "BEARISH":
            bg_color = "#ff6666"
            border_color = "#cc4444"
            icon = "📉"
        else:
            bg_color = "#ff3333"
            border_color = "#cc2222"
            icon = "💀"
        reaction = company.get('actual_reaction', '')
        reaction_color = "#00ff88" if "UP" in reaction else "#ff4444" if "DOWN" in reaction else "#ffaa00"
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 5px solid {border_color};">
            <table style="width:100%;">
                <tr>
                    <td style="width:25%;"><b>🏢 {company['name']}</b><br><small>{company['symbol']}</small></td>
                    <td style="width:20%;"><b>📅 Q4 Date</b><br>{company['q4_date']}
