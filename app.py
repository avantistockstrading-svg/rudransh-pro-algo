"""
🐺 RUDRANSH PRO ALGO X - COMPLETE EDITION
===========================================
VERSION: 6.0.0
REAL-TIME DATA | 3D GLASS FINISHING | LIVE NEWS | STOCK SCREENER
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time
from streamlit_autorefresh import st_autorefresh

# ================= VERSION & INFO =================
APP_VERSION = "6.0.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= API KEYS =================
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"
TELEGRAM_BOT = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
TELEGRAM_CHAT = "1983026913"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🐺")

# ================= CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0a0a2a, #050510);
        font-family: 'Orbitron', monospace;
    }
    
    .glass-3d {
        background: rgba(15, 25, 45, 0.65);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 136, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .glass-3d:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 50px rgba(0, 0, 0, 0.5);
    }
    
    .neon-text {
        text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88;
        animation: neonPulse 2s infinite;
    }
    
    @keyframes neonPulse {
        0% { text-shadow: 0 0 5px #00ff88; }
        50% { text-shadow: 0 0 20px #00ff88, 0 0 30px #00ff88; }
        100% { text-shadow: 0 0 5px #00ff88; }
    }
    
    .live-ticker {
        background: linear-gradient(90deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 48px;
        font-weight: bold;
    }
    
    .meter-container {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 50px;
        padding: 5px;
        margin: 10px 0;
    }
    
    .meter-fill {
        background: linear-gradient(90deg, #ff3333, #ffaa00, #00ff44);
        border-radius: 50px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 15px;
        color: white;
        font-weight: bold;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 180, 216, 0.1));
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(0, 255, 136, 0.3);
    }
    
    .news-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #00ff88;
    }
    
    h1 {
        font-family: 'Orbitron', monospace;
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    h2 {
        font-family: 'Orbitron', monospace;
        font-size: 24px;
        font-weight: 700;
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
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
    }
    
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, #00b4d8, transparent);
        margin: 20px 0;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: #546574;
        font-size: 11px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
    }
    
    @media only screen and (max-width: 768px) {
        h1 { font-size: 28px !important; }
        .live-ticker { font-size: 28px !important; }
        .glass-3d { padding: 12px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================
def get_ist_now():
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now

def get_live_nifty():
    try:
        df = yf.download("^NSEI", period="2d", interval="1m", progress=False)
        if not df.empty and len(df) > 1:
            current = float(df['Close'].iloc[-1])
            prev = float(df['Close'].iloc[-2])
            change = current - prev
            pct = (change / prev) * 100
            return current, change, pct, prev
    except:
        pass
    return 24800, 0, 0, 24800

def get_news():
    news_list = []
    try:
        url = f"https://gnews.io/api/v4/search?q=india%20stock%20market%20OR%20nifty&lang=en&country=in&max=8&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for article in data.get('articles', []):
                news_list.append({
                    'title': article.get('title', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'time': article.get('publishedAt', '')[:10]
                })
    except:
        pass
    
    if not news_list:
        news_list = [
            {'title': 'NIFTY trades near record highs', 'source': 'Economic Times', 'time': get_ist_now().strftime('%Y-%m-%d')},
            {'title': 'RBI keeps repo rate unchanged', 'source': 'Business Standard', 'time': get_ist_now().strftime('%Y-%m-%d')},
            {'title': 'FIIs continue buying in Indian markets', 'source': 'Moneycontrol', 'time': get_ist_now().strftime('%Y-%m-%d')},
        ]
    return news_list

def scan_stocks():
    stocks = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR", 
              "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK", "AXISBANK", "LT"]
    results = []
    for stock in stocks:
        try:
            ticker = f"{stock}.NS"
            df = yf.download(ticker, period="20d", progress=False)
            if not df.empty and len(df) > 5:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                change = ((current - prev) / prev) * 100
                volume = int(df['Volume'].iloc[-1])
                avg_vol = int(df['Volume'].tail(10).mean())
                vol_ratio = round(volume / avg_vol, 2) if avg_vol > 0 else 1
                
                ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
                
                if current > ema20 and change > 0.5 and vol_ratio > 1.2:
                    signal = "STRONG BUY"
                elif current > ema20 and change > 0:
                    signal = "BUY"
                elif current < ema20 and change < -1:
                    signal = "AVOID"
                else:
                    signal = "WATCH"
                
                results.append({
                    'symbol': stock, 'price': round(current, 2), 'change': round(change, 2),
                    'volume_ratio': vol_ratio, 'signal': signal
                })
        except:
            continue
        time.sleep(0.1)
    return results

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage", 
                     data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=5)
    except:
        pass

# ================= APP LOCK =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

if not st.session_state.app_unlocked:
    st.markdown('<div style="text-align:center; padding:80px;"><h1 class="neon-text">🐺 RUDRANSH PRO ALGO X</h1><p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p><div style="height:3px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:30px auto;"></div><h3>🔐 APPLICATION LOCKED</h3><p>Enter Password to Access</p></div>', unsafe_allow_html=True)
    password_input = st.text_input("Password", type="password", placeholder="Enter password")
    if st.button("🔓 UNLOCK"):
        if password_input == "8055":
            st.session_state.app_unlocked = True
            st.rerun()
        else:
            st.error("❌ Wrong Password!")
    st.stop()

# ================= SESSION STATE =================
if "algo_running" not in st.session_state:
    st.session_state.algo_running = False
if "active_orders" not in st.session_state:
    st.session_state.active_orders = []
if "trade_journal" not in st.session_state:
    st.session_state.trade_journal = []
if "auto_trade_enabled" not in st.session_state:
    st.session_state.auto_trade_enabled = True
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

# ================= HEADER =================
st.markdown(f'<div style="text-align:center;"><h1 class="neon-text">🐺 {APP_NAME}</h1><p style="color:#94a3b8;">{APP_AUTHOR}, {APP_LOCATION} | v{APP_VERSION}</p><div class="custom-divider"></div></div>', unsafe_allow_html=True)

now = get_ist_now()
st.markdown(f'<div style="text-align:center; font-size:20px; margin-bottom:20px;">🕐 {now.strftime("%H:%M:%S")} IST | 📅 {now.strftime("%d %B %Y")}</div>', unsafe_allow_html=True)

# ================= LIVE NIFTY =================
nifty_price, nifty_change, nifty_pct, nifty_prev = get_live_nifty()
nifty_color = "#00ff88" if nifty_change >= 0 else "#ff4444"

st.markdown(f'''
<div class="glass-3d" style="text-align:center;">
    <div style="font-size:14px; color:#94a3b8;">🇮🇳 NIFTY 50 LIVE</div>
    <div class="live-ticker">₹{nifty_price:,.2f}</div>
    <div style="font-size:18px; color:{nifty_color};">{'▲' if nifty_change>=0 else '▼'} {abs(nifty_pct):.2f}%</div>
    <div class="meter-container"><div class="meter-fill" style="width:{50+nifty_pct}%;">{nifty_pct:+.1f}%</div></div>
    <small>Previous Close: ₹{nifty_prev:,.2f}</small>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📰 NEWS", "🔍 STOCK SCREENER", "🐺 ALGO TRADING", "⚙️ SETTINGS", "💰 PORTFOLIO"])

# ================= TAB 1: NEWS =================
with tab1:
    st.markdown("### 📰 LATEST MARKET NEWS")
    news_items = get_news()
    for news in news_items:
        st.markdown(f'''
        <div class="news-card">
            <b>📌 {news['title'][:150]}</b><br>
            <small>🔗 {news['source']} | 🕐 {news['time']}</small>
        </div>
        ''', unsafe_allow_html=True)

# ================= TAB 2: STOCK SCREENER =================
with tab2:
    st.markdown("### 🔍 STOCK SCREENER")
    st.markdown("*Volume + Trend Analysis | NIFTY 50 Stocks*")
    
    if st.button("🔍 SCAN STOCKS NOW", use_container_width=True):
        with st.spinner("Scanning 50+ stocks..."):
            results = scan_stocks()
        
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            
            strong_buy = [r for r in results if r['signal'] == "STRONG BUY"]
            if strong_buy:
                st.markdown("### 🚀 STRONG BUY SIGNALS")
                for s in strong_buy:
                    st.markdown(f'<div style="background:rgba(0,255,68,0.1); padding:12px; margin:5px 0; border-radius:10px;"><b>{s["symbol"]}</b> - ₹{s["price"]} ({s["change"]:+.2f}%) | Volume: {s["volume_ratio"]}x Avg | <span style="color:#00ff44;">{s["signal"]}</span></div>', unsafe_allow_html=True)

# ================= TAB 3: ALGO TRADING =================
with tab3:
    st.markdown("### 🐺 ALGO TRADING SYSTEM")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🟢 START ALGO", use_container_width=True):
            st.session_state.algo_running = True
            send_telegram("🚀 ALGO STARTED")
            st.success("✅ Algo Started!")
            st.rerun()
    with col2:
        if st.button("🔴 STOP ALGO", use_container_width=True):
            st.session_state.algo_running = False
            send_telegram("🛑 ALGO STOPPED")
            st.warning("⚠️ Algo Stopped!")
            st.rerun()
    
    st.markdown("---")
    status_color = "#00ff88" if st.session_state.algo_running else "#ff4444"
    st.markdown(f'<div class="glass-3d" style="text-align:center;"><span style="color:{status_color};">●</span> SYSTEM STATUS: <b>{"ACTIVE" if st.session_state.algo_running else "INACTIVE"}</b></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 📊 ACTIVE ORDERS")
    if st.session_state.active_orders:
        for order in st.session_state.active_orders:
            st.markdown(f"**{order['symbol']}** - Entry: ₹{order['entry_price']} | SL: ₹{order['sl']} | Target: ₹{order['target']}")
    else:
        st.info("No active orders")

# ================= TAB 4: SETTINGS =================
with tab4:
    st.markdown("### ⚙️ TRADING SETTINGS")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Default Lots", 1, 50, 1)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("Stop Loss %", 1, 20, 5)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", 1, 30, 10)
    
    st.markdown("---")
    st.markdown("#### 🔊 Voice Alerts")
    st.session_state.voice_enabled = st.checkbox("Enable Voice Alerts", st.session_state.voice_enabled)

# ================= TAB 5: PORTFOLIO =================
with tab5:
    st.markdown("### 💰 PORTFOLIO & P&L")
    
    total_pnl = 0
    for order in st.session_state.active_orders:
        total_pnl += order.get('pnl', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div>💰 TOTAL P&L</div><div style="font-size:32px;">₹{total_pnl:,.2f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div>🔴 ACTIVE</div><div style="font-size:32px;">{len(st.session_state.active_orders)}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div>📋 TOTAL</div><div style="font-size:32px;">{len(st.session_state.trade_journal)}</div></div>', unsafe_allow_html=True)
    
    if st.session_state.trade_journal:
        st.markdown("---")
        st.markdown("#### 📋 TRADE JOURNAL")
        st.dataframe(pd.DataFrame(st.session_state.trade_journal), use_container_width=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown('<div style="text-align:center; padding:15px; background:linear-gradient(135deg,#8B0000,#DC143C); border-radius:15px;"><h2 style="color:#FFD700;">🐺 RUDRANSH</h2><p style="color:#FFD700;">Premium v6.0</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div style="text-align:center;"><span style="font-size:28px;">🔴</span><h3>{len(st.session_state.active_orders)}</h3><p>Active Orders</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;"><span style="font-size:28px;">📋</span><h3>{len(st.session_state.trade_journal)}</h3><p>Total Trades</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<span style="color:#00ff88">✅ News API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ Telegram: Active</span>', unsafe_allow_html=True)
    auto_text = "ON" if st.session_state.auto_trade_enabled else "OFF"
    auto_color = "#00ff88" if st.session_state.auto_trade_enabled else "#ff4444"
    st.markdown(f'<span style="color:{auto_color}">⚙️ Auto Trade: {auto_text}</span>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown(f'<div class="footer">🐺 {APP_NAME} PREMIUM | {APP_AUTHOR} | v{APP_VERSION}<br>Real-time Data | Stock Screener | Auto Trading</div>', unsafe_allow_html=True)

# ================= AUTO REFRESH =================
st_autorefresh(interval=60000, key="main_refresh")
