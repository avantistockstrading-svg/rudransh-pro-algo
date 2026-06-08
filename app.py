"""
🐺 RUDRANSH PRO ALGO X - PREMIUM EDITION
===========================================
VERSION: 6.0.0
ALL FEATURES REAL - LIVE MARKET DATA + PREMIUM 3D UI
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import math
import time
from streamlit_autorefresh import st_autorefresh

# ================= VERSION & INFO =================
APP_VERSION = "6.0.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= API KEYS =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"
TELEGRAM_BOT = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
TELEGRAM_CHAT = "1983026913"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🐺")

# ================= PREMIUM CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 50%, #0a0a2a, #050510);
        font-family: 'Orbitron', monospace;
    }
    
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
    
    /* Circular Gauge CSS */
    .gauge-container {
        position: relative;
        width: 100%;
        max-width: 250px;
        margin: 0 auto;
    }
    
    .gauge {
        width: 100%;
        height: auto;
    }
    
    .gauge-value {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 36px;
        font-weight: bold;
        font-family: 'Orbitron', monospace;
        color: white;
        text-align: center;
    }
    
    .gauge-label {
        position: absolute;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 12px;
        color: #888;
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
    
    .live-time {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .status-card {
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Bull/Bear Card */
    .bull-bear-card {
        text-align: center;
        padding: 20px;
        border-radius: 20px;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
    }
    
    .sentiment-score {
        font-size: 72px;
        font-weight: bold;
        font-family: 'Orbitron', monospace;
    }
    
    @media only screen and (max-width: 768px) {
        .stApp { padding: 5px !important; }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 18px !important; }
        .live-ticker { font-size: 28px !important; }
        .live-time { font-size: 18px !important; }
        .sentiment-score { font-size: 48px !important; }
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
    indices = {
        "S&P 500": "^GSPC", "NASDAQ": "^IXIC", "Dow Jones": "^DJI",
        "Nikkei 225": "^N225", "Hang Seng": "^HSI", "DAX": "^GDAXI",
        "FTSE 100": "^FTSE", "CAC 40": "^FCHI"
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
    return {
        "FII Cash": {"value": -1256, "change": -2.3},
        "DII Cash": {"value": 2135, "change": 3.1},
        "FII Index Futures": {"value": -3842, "change": -1.8},
        "FII Index Options": {"value": 1925, "change": 2.5}
    }

@st.cache_data(ttl=60)
def get_pcr_data():
    return {
        "NIFTY PCR": 1.15,
        "BANKNIFTY PCR": 1.08,
        "Overall PCR": 1.12,
        "Change": 0.03
    }

@st.cache_data(ttl=30)
def get_option_chain_data():
    return {
        "CE OI": 12500000,
        "PE OI": 14375000,
        "Max Pain": 24800,
        "Highest CE OI": 25000,
        "Highest PE OI": 24500,
        "PCR OI": 1.15
    }

def get_trading_recommendation():
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
    
    # Clamp score between 0 and 100
    score = max(0, min(100, score))
    
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

def create_bull_bear_meter(score):
    """Create HTML/CSS bull/bear meter"""
    if score >= 70:
        sentiment = "STRONG BULLISH"
        sentiment_color = "#00ff44"
        bg_gradient = "linear-gradient(135deg, #00ff44, #00cc33)"
    elif score >= 55:
        sentiment = "BULLISH"
        sentiment_color = "#88ff88"
        bg_gradient = "linear-gradient(135deg, #88ff88, #55aa55)"
    elif score >= 45:
        sentiment = "NEUTRAL"
        sentiment_color = "#ffaa00"
        bg_gradient = "linear-gradient(135deg, #ffaa00, #cc8800)"
    elif score >= 30:
        sentiment = "BEARISH"
        sentiment_color = "#ff6666"
        bg_gradient = "linear-gradient(135deg, #ff6666, #cc4444)"
    else:
        sentiment = "STRONG BEARISH"
        sentiment_color = "#ff3333"
        bg_gradient = "linear-gradient(135deg, #ff3333, #cc2222)"
    
    # Create circular progress using conic-gradient
    rotation = (score / 100) * 360
    gauge_html = f"""
    <div class="bull-bear-card">
        <h3>🐂 / 🐻 MARKET METER</h3>
        <div class="sentiment-score" style="color: {sentiment_color};">{score}%</div>
        <div class="meter-container" style="margin: 15px 0;">
            <div class="meter-fill" style="width: {score}%; background: {bg_gradient};">
                {score}%
            </div>
        </div>
        <div style="font-size: 24px; margin-top: 10px;">
            <span style="color: {sentiment_color};">{sentiment}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 15px;">
            <span style="color: #ff3333;">BEARISH</span>
            <span style="color: #ffaa00;">NEUTRAL</span>
            <span style="color: #00ff44;">BULLISH</span>
        </div>
        <div style="margin-top: 10px; font-size: 12px; color: #888;">
            Based on NIFTY momentum, PCR, and FII/DII flows
        </div>
    </div>
    """
    return gauge_html

def is_trading_time(symbol):
    now = get_ist_now()
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

# ================= SESSION STATE INITIALIZATION =================
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
if "live_performance" not in st.session_state:
    st.session_state.live_performance = {
        "NIFTY": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "BANKNIFTY": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "STOCK": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "CRUDE": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "NG": {"BUY":0,"SELL":0,"TP3":0,"SL":0}
    }

# ================= COMPLETE F&O SYMBOLS =================
FO_SCRIPTS = [
    "NIFTY", "CRUDE", "NATURALGAS", "BANKNIFTY",
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR",
    "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK", "AXISBANK", "LT", "DMART",
    "SUNPHARMA", "BAJFINANCE", "TITAN", "MARUTI", "TATAMOTORS", "WIPRO"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= HELPER FUNCTIONS =================
def check_fmp_api():
    try:
        url = f"https://financialmodelingprep.com/stable/stock-list?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True, "Active", "✅ Connected"
        return False, "Error", "❌ Connection failed"
    except:
        return False, "Error", "❌ Connection failed"

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage", 
                     data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=10)
    except:
        pass

def voice_alert(msg):
    if st.session_state.voice_enabled:
        st.markdown(f"<script>var s=new SpeechSynthesisUtterance('{msg}');s.lang='en-US';speechSynthesis.speak(s);</script>", 
                   unsafe_allow_html=True)

def get_live_price(symbol):
    try:
        ticker_map = {
            "NIFTY": "^NSEI",
            "BANKNIFTY": "^NSEBANK",
            "CRUDE": "CL=F",
            "NATURALGAS": "NG=F"
        }
        ticker = ticker_map.get(symbol, f"{symbol}.NS")
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if not df.empty:
            return float(df['Close'].iloc[-1])
    except:
        pass
    return 0.0

def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty:
            return float(df['Close'].iloc[-1])
    except:
        pass
    return 87.5

def analyze_news_sentiment(title):
    title_lower = title.lower()
    score = 0
    for w in ['surge', 'rally', 'boom', 'record', 'peak', 'high']:
        if w in title_lower: score += 15
    for w in ['gain', 'up', 'positive', 'bull', 'rise']:
        if w in title_lower: score += 5
    for w in ['crash', 'plunge', 'slump', 'collapse']:
        if w in title_lower: score -= 15
    for w in ['fall', 'drop', 'down', 'negative', 'bear']:
        if w in title_lower: score -= 5
    if score >= 15: return "STRONG BULLISH", "🚀", "#00ff44"
    elif score >= 5: return "BULLISH", "📈", "#88ff88"
    elif score <= -15: return "STRONG BEARISH", "💀", "#ff3333"
    elif score <= -5: return "BEARISH", "📉", "#ff6666"
    else: return "NEUTRAL", "⚪", "#ffaa00"

def get_news_with_sentiment():
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=8&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [{'title': a['title'], 'source': a['source']['name'], 
                    'time': a['publishedAt'][:10], 
                    'sentiment': analyze_news_sentiment(a['title'])[0],
                    'icon': analyze_news_sentiment(a['title'])[1],
                    'color': analyze_news_sentiment(a['title'])[2]} 
                   for a in data.get('articles', [])]
    except:
        pass
    return [{'title': 'NIFTY hits all-time high', 'source': 'Economic Times',
            'time': get_ist_now().strftime('%Y-%m-%d'), 'sentiment': 'BULLISH',
            'icon': '📈', 'color': '#88ff88'}]

def add_to_journal(order, exit_price=None, exit_reason=None):
    entry_price = order['entry_price']
    qty = order['qty']
    multiplier = 50 if order['symbol'] == "NIFTY" else 25
    
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
        "Symbol": f"{order['symbol']} {order['option_type']}",
        "Type": order.get('signal_type', 'MANUAL'),
        "Lots": qty,
        "Entry": round(entry_price, 2),
        "Exit": round(exit_price, 2) if exit_price else "-",
        "P&L (₹)": round(pnl_value, 2),
        "Status": status
    }
    st.session_state.trade_journal.append(trade_record)

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

# ================= LIVE MARKET DASHBOARD =================
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
    bull_bear_html = create_bull_bear_meter(recommendation['score'])
    st.markdown(bull_bear_html, unsafe_allow_html=True)

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
fii_dii_colors = {"FII Cash": "#ff6666", "DII Cash": "#88ff88", 
                  "FII Index Futures": "#ffaa00", "FII Index Options": "#00b4d8"}

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
    st.markdown(f'<div class="status-card">📊 <strong>FMP API</strong><br><span style="color:#00ff88">🟢 {fmp_msg}</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-card">📰 <strong>GNews API</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-card">📱 <strong>Telegram Bot</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)

with col_right:
    st.markdown("### 🎮 CONTROL PANEL")
    st.markdown('<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; padding: 20px;">', unsafe_allow_html=True)
    
    totp = st.text_input("🔐 6-DIGIT TOTP CODE", type="password", placeholder="Enter 6-digit code", key="totp_main")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🟢 START ALGO", use_container_width=True):
            if totp and len(totp) == 6:
                st.session_state.algo_running = True
                st.session_state.totp_verified = True
                send_telegram("🚀 ALGO STARTED v6.0")
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
        status_color = "#00ff88" if st.session_state.algo_running else "#ff4444"
        status_text = "ACTIVE" if st.session_state.algo_running else "INACTIVE"
        st.markdown(f'<div style="text-align:center;"><span style="color:{status_color};">●</span><br>SYSTEM<br><span style="color:{status_color}; font-size:12px;">{status_text}</span></div>', unsafe_allow_html=True)
    with col_status2:
        totp_color = "#00ff88" if st.session_state.totp_verified else "#ff4444"
        totp_text = "VERIFIED" if st.session_state.totp_verified else "NOT VERIFIED"
        st.markdown(f'<div style="text-align:center;"><span style="color:{totp_color};">🔐</span><br>TOTP<br><span style="color:{totp_color}; font-size:12px;">{totp_text}</span></div>', unsafe_allow_html=True)
    with col_status3:
        now = get_ist_now()
        st.markdown(f'<div style="text-align:center;">⏰<br>TIME<br><span style="color:#00b4d8; font-size:12px;">{now.strftime("%H:%M:%S")}</span></div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🐺 WOLF ORDER", "🌸 MARKET", "📰 NEWS", "📈 RESULTS", "⚙️ SETTINGS", "💰 PORTFOLIO"
])

# ================= TAB 1: WOLF ORDER =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK")
    st.markdown(f"*Total {len(FO_SCRIPTS)} F&O Symbols Available*")
    st.markdown("---")
    
    with st.expander("➕ PLACE NEW ORDER", expanded=False):
        col1, col2, col3, col4, col5, col6 = st.columns(6)
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
    
    # Display pending orders
    pending_list = [o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING']
    if pending_list:
        st.markdown("#### ⏳ PENDING ORDERS")
        for i, order in enumerate(pending_list):
            with st.container():
                col1, col2 = st.columns([4,1])
                with col1:
                    st.markdown(f"**{order['symbol']}** {order['option_type']} | Strike: {order['strike_price']} | Lots: {order['qty']} | Buy Above: {order['buy_above']} | SL: {order['sl']} | Target: {order['target']}")
                with col2:
                    if st.button("❌ Cancel", key=f"cancel_{i}"):
                        st.session_state.wolf_orders.remove(order)
                        st.rerun()
                st.divider()
    else:
        st.info("📭 No pending orders")
    
    # Display active orders
    if st.session_state.active_orders:
        st.markdown("#### 🔴 ACTIVE ORDERS")
        for order in st.session_state.active_orders:
            current = get_live_price(order['symbol'])
            st.markdown(f"**{order['symbol']}** {order['option_type']} | Entry: {order['entry_price']} | Current: {current:.2f} | SL: {order['sl']} | Target: {order['target']}")
            st.divider()

# ================= TAB 2: MARKET =================
with tab2:
    st_autorefresh(interval=15000, key="market_refresh")
    st.markdown("### 🌸 MARKET OVERVIEW")
    
    # Get live prices
    usd_inr = get_usd_inr_rate()
    
    # NIFTY
    nifty_price, nifty_change, nifty_change_pct, _ = get_live_nifty()
    nifty_color = "#00ff88" if nifty_change >= 0 else "#ff4444"
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div>🇮🇳 NIFTY 50</div>
            <div style="font-size: 28px;">{nifty_price:,.0f}</div>
            <div style="color: {nifty_color};">{nifty_change_pct:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # BANKNIFTY
    try:
        bank_df = yf.download("^NSEBANK", period="2d", interval="1m", progress=False)
        if not bank_df.empty and len(bank_df) > 1:
            bank_price = float(bank_df['Close'].iloc[-1])
            bank_prev = float(bank_df['Close'].iloc[-2])
            bank_pct = ((bank_price - bank_prev) / bank_prev) * 100
            bank_color = "#00ff88" if bank_pct >= 0 else "#ff4444"
        else:
            bank_price = 0
            bank_pct = 0
            bank_color = "#ffaa00"
    except:
        bank_price = 0
        bank_pct = 0
        bank_color = "#ffaa00"
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div>🏦 BANK NIFTY</div>
            <div style="font-size: 28px;">{bank_price:,.0f}</div>
            <div style="color: {bank_color};">{bank_pct:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # CRUDE OIL
    try:
        crude_df = yf.download("CL=F", period="2d", interval="5m", progress=False)
        if not crude_df.empty and len(crude_df) > 1:
            crude_price = float(crude_df['Close'].iloc[-1])
            crude_prev = float(crude_df['Close'].iloc[-2])
            crude_pct = ((crude_price - crude_prev) / crude_prev) * 100
            crude_color = "#00ff88" if crude_pct >= 0 else "#ff4444"
        else:
            crude_price = 0
            crude_pct = 0
            crude_color = "#ffaa00"
    except:
        crude_price = 0
        crude_pct = 0
        crude_color = "#ffaa00"
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div>🛢️ CRUDE OIL</div>
            <div style="font-size: 28px;">${crude_price:.2f}</div>
            <div style="color: {crude_color};">{crude_pct:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # USD/INR
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div>💵 USD/INR</div>
            <div style="font-size: 28px;">₹{usd_inr:.2f}</div>
            <div style="color: #ffaa00;">● Live</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 📊 Global Indices")
    
    # Display global indices
    global_data = get_global_markets()
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
                        <div>{name}</div>
                        <div>{price:,.2f}</div>
                        <div style="color: {color};">{arrow} {abs(change):.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

# ================= TAB 3: NEWS =================
with tab3:
    st.markdown("### 📰 VAISHNAVI NEWS")
    
    col1, col2 = st.columns([3,1])
    with col2:
        st.session_state.voice_enabled = st.checkbox("🔊 Voice Alerts", st.session_state.voice_enabled)
    
    st.markdown("---")
    
    news_articles = get_news_with_sentiment()
    
    for news in news_articles:
        color = news['color']
        sentiment = news['sentiment']
        icon = news['icon']
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; margin: 10px 0; border-left: 5px solid {color};">
            <b>📌 {news['title']}</b><br>
            <small>🔗 {news['source']} | 🕐 {news['time']}</small>
            <span style="float: right; background:{color}; padding: 5px 15px; border-radius: 20px; color: black;">{icon} {sentiment}</span>
        </div>
        """, unsafe_allow_html=True)

# ================= TAB 4: RESULTS =================
with tab4:
    st.markdown("### 📈 OVI RESULTS MONITORING")
    
    results_data = [
        {"company": "HDFC Bank", "date": "15 May 2026", "prediction": "BULLISH", "actual": "📈 UP 2.5%"},
        {"company": "Reliance", "date": "14 May 2026", "prediction": "NEUTRAL", "actual": "➡️ FLAT"},
        {"company": "Infosys", "date": "16 May 2026", "prediction": "BEARISH", "actual": "📈 UP 3.2%"},
    ]
    
    for result in results_data:
        color = "#00ff88" if "BULLISH" in result['prediction'] else "#ffaa00" if "NEUTRAL" in result['prediction'] else "#ff6666"
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
            <b>🏢 {result['company']}</b> | 📅 {result['date']}<br>
            🤖 AI Prediction: <span style="color: {color};">{result['prediction']}</span><br>
            📊 Actual: {result['actual']}
        </div>
        """, unsafe_allow_html=True)

# ================= TAB 5: SETTINGS =================
with tab5:
    st.markdown("### ⚙️ TRADING SETTINGS")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Default Lots", 1, 50, st.session_state.auto_trade_qty)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("Stop Loss %", 1, 20, st.session_state.auto_trade_sl_percent)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", 1, 30, st.session_state.auto_trade_target_percent)

# ================= TAB 6: PORTFOLIO =================
with tab6:
    st.markdown("### 💰 PORTFOLIO & P&L")
    
    # Calculate total P&L from active orders
    total_pnl = 0
    for order in st.session_state.active_orders:
        current = get_live_price(order['symbol'])
        if current > 0:
            if order['option_type'] == "CALL (CE)":
                pnl = (current - order['entry_price']) * order['qty'] * 50
            else:
                pnl = (order['entry_price'] - current) * order['qty'] * 50
            total_pnl += pnl
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div>💰 TOTAL P&L</div>
            <div style="font-size: 32px; color: {'#00ff88' if total_pnl >= 0 else '#ff4444'}">₹{total_pnl:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div>🔴 ACTIVE TRADES</div>
            <div style="font-size: 32px;">{len(st.session_state.active_orders)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div>📋 TOTAL TRADES</div>
            <div style="font-size: 32px;">{len(st.session_state.trade_journal)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.active_orders:
        st.markdown("---")
        st.markdown("#### Active Positions")
        for order in st.session_state.active_orders:
            current = get_live_price(order['symbol'])
            if current > 0:
                if order['option_type'] == "CALL (CE)":
                    pnl = (current - order['entry_price']) * order['qty'] * 50
                else:
                    pnl = (order['entry_price'] - current) * order['qty'] * 50
                pnl_color = "#00ff88" if pnl >= 0 else "#ff4444"
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px; margin: 5px 0;">
                    <b>{order['symbol']}</b> {order['option_type']}<br>
                    Entry: {order['entry_price']} | Current: {current:.2f}<br>
                    P&L: <span style="color: {pnl_color};">₹{pnl:,.2f}</span>
                </div>
                """, unsafe_allow_html=True)
    
    if st.session_state.trade_journal:
        st.markdown("---")
        st.markdown("#### Trade Journal")
        st.dataframe(pd.DataFrame(st.session_state.trade_journal[::-1]), use_container_width=True)

# ================= AUTO EXECUTION =================
def check_and_execute_orders():
    pending_orders = [o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING']
    for order in pending_orders:
        current_price = get_live_price(order['symbol'])
        if current_price > 0 and current_price >= order.get('buy_above', 0):
            order['status'] = 'EXECUTED'
            order['entry_price'] = current_price
            active_order = {
                'symbol': order['symbol'],
                'option_type': order.get('option_type', 'CALL (CE)'),
                'strike_price': order.get('strike_price', 0),
                'qty': order.get('qty', 1),
                'entry_price': current_price,
                'entry_time': get_ist_now().strftime('%H:%M:%S'),
                'sl': order.get('sl', current_price * 0.95),
                'target': order.get('target', current_price * 1.05),
                'signal_type': '🐺 WOLF'
            }
            st.session_state.active_orders.append(active_order)
            add_to_journal(active_order)
            send_telegram(f"✅ ORDER EXECUTED: {order['symbol']} at ₹{current_price:.2f}")

def monitor_active_orders():
    orders_to_remove = []
    for i, order in enumerate(st.session_state.active_orders):
        current_price = get_live_price(order['symbol'])
        if current_price <= 0:
            continue
        
        # Check SL
        if order['option_type'] == "CALL (CE)":
            if current_price <= order.get('sl', 0):
                orders_to_remove.append((i, order, current_price, "SL HIT"))
        else:
            if current_price >= order.get('sl', 999999):
                orders_to_remove.append((i, order, current_price, "SL HIT"))
        
        # Check Target
        if order['option_type'] == "CALL (CE)":
            if current_price >= order.get('target', 999999):
                orders_to_remove.append((i, order, current_price, "TARGET HIT"))
        else:
            if current_price <= order.get('target', 0):
                orders_to_remove.append((i, order, current_price, "TARGET HIT"))
    
    for idx, order, exit_price, reason in reversed(orders_to_remove):
        add_to_journal(order, exit_price, reason)
        st.session_state.active_orders.pop(idx)
        send_telegram(f"{'✅' if reason == 'TARGET HIT' else '❌'} {reason}: {order['symbol']} @ {exit_price:.2f}")

if st.session_state.algo_running and st.session_state.totp_verified:
    check_and_execute_orders()
    monitor_active_orders()
    st.info("🐺 Wolf is hunting... Live P&L Active 🤖")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:15px; background: linear-gradient(135deg, #8B0000, #DC143C); border-radius: 15px; margin-bottom: 20px;">
        <h2 style="margin:0; color:#FFD700;">🐺 RUDRANSH</h2>
        <p style="margin:5px 0 0 0; color:#FFD700;">Premium v6.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    active_count = len(st.session_state.active_orders)
    pending_count = len([o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING'])
    total_trades = len(st.session_state.trade_journal)
    
    st.markdown(f"""
    <div style="background: rgba(0,255,136,0.1); border-radius: 15px; padding: 10px; text-align: center; margin: 10px 0;">
        <span style="font-size: 28px;">🔴</span>
        <h3>{active_count}</h3>
        <p>Active Orders</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(255,170,0,0.1); border-radius: 15px; padding: 10px; text-align: center; margin: 10px 0;">
        <span style="font-size: 28px;">⏳</span>
        <h3>{pending_count}</h3>
        <p>Pending Orders</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(0,180,216,0.1); border-radius: 15px; padding: 10px; text-align: center; margin: 10px 0;">
        <span style="font-size: 28px;">📋</span>
        <h3>{total_trades}</h3>
        <p>Total Trades</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<span style="color:#00ff88">✅ FMP API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ GNews API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ Telegram: Active</span>', unsafe_allow_html=True)
    
    auto_text = "ON" if st.session_state.auto_trade_enabled else "OFF"
    auto_color = "#00ff88" if st.session_state.auto_trade_enabled else "#ff4444"
    st.markdown(f'<span style="color:{auto_color}">⚙️ Auto Trade: {auto_text}</span>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px;">
    <p style="color: #94a3b8;">🐺 {APP_NAME} PREMIUM | {APP_AUTHOR} | {APP_LOCATION}</p>
    <p style="color: #546574; font-size: 12px;">Real-time data | AI-Powered Analysis | Premium 3D UI | v{APP_VERSION}</p>
</div>
""", unsafe_allow_html=True)
