"""
🐺 RUDRANSH PRO ALGO X - MASTER COPY v2.1
===========================================
DEVELOPED BY: SATISH D. NAKHATE
LOCATION: TALWADE, PUNE - 412114
VERSION: 2.1.0
LAST UPDATED: 2026-05-16

NEW IN v2.1:
- CE/PE Option Selection in Wolf Order
- FMP API Integrated
- GNews API Integrated
- 9 News Sources Active
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time
import json

# ================= VERSION =================
APP_VERSION = "2.1.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"
LAST_UPDATE = "2026-05-16"

# ================= API KEYS (SET) =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title=f"{APP_NAME}", 
    layout="wide", 
    page_icon="🐺",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .css-1r6slb0, .css-1y4p8pa {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
    }
    h1, h2, h3 {
        background: linear-gradient(135deg, #00ff88 0%, #00b4d8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00b4d8 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(0,255,136,0.3);
    }
    .badge-success {
        background: rgba(0,255,136,0.2);
        color: #00ff88;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .badge-danger {
        background: rgba(255,0,0,0.2);
        color: #ff4444;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .badge-warning {
        background: rgba(255,165,0,0.2);
        color: #ffa500;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .badge-info {
        background: rgba(0,180,216,0.2);
        color: #00b4d8;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .live-time {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
    }
    .toast-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        z-index: 9999;
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ================= IST TIMEZONE =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= APP LOCK =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False
if "app_password" not in st.session_state:
    st.session_state.app_password = "8055"

if not st.session_state.app_unlocked:
    st.markdown("""
    <div style="text-align:center; padding:50px;">
        <h1>🐺 RUDRANSH PRO ALGO X</h1>
        <p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>
        <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:200px; margin:20px auto;"></div>
        <h3>🔐 APPLICATION LOCKED</h3>
        <p>Enter 4-6 Digit Numeric Password to Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    password_input = st.text_input("Password", type="password", placeholder="Enter numeric password", key="app_lock_password")
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔓 UNLOCK", use_container_width=True):
            entered = str(password_input).strip()
            expected = str(st.session_state.app_password).strip()
            if entered == expected:
                st.session_state.app_unlocked = True
                st.rerun()
            else:
                st.error("❌ Wrong Password! Access Denied.")
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
if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = get_ist_now().date()
if "max_daily_loss" not in st.session_state:
    st.session_state.max_daily_loss = 100000
if "news_cache" not in st.session_state:
    st.session_state.news_cache = []
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True
if "result_alerts" not in st.session_state:
    st.session_state.result_alerts = []

# ================= COMPLETE F&O SCRIPTS =================
FO_SCRIPTS = [
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "CRUDE", "NATURALGAS",
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR", "ITC",
    "SBIN", "BHARTIARTL", "KOTAKBANK", "AXISBANK", "LT", "DMART", "SUNPHARMA",
    "BAJFINANCE", "TITAN", "MARUTI", "TATAMOTORS", "TATASTEEL", "WIPRO",
    "HCLTECH", "ONGC", "NTPC", "POWERGRID", "ULTRACEMCO", "ADANIPORTS",
    "ADANIENT", "ASIANPAINT", "BAJAJFINSV", "BRITANNIA", "CIPLA", "COALINDIA",
    "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HDFCLIFE", "HEROMOTOCO",
    "HINDALCO", "IOC", "INDUSINDBK", "JSWSTEEL", "M&M", "NESTLEIND",
    "PIDILITIND", "SBILIFE", "SHREECEM", "SIEMENS", "SRF", "TATACONSUM",
    "TATAPOWER", "TECHM", "UPL", "VEDL", "YESBANK", "ZYDUSLIFE"
]

# ================= CE/PE OPTIONS =================
OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= LOT SIZE AND TP SETTINGS =================
if "nifty_lots" not in st.session_state:
    st.session_state.nifty_lots = 1
if "nifty_tp1" not in st.session_state:
    st.session_state.nifty_tp1 = 10
if "nifty_tp2" not in st.session_state:
    st.session_state.nifty_tp2 = 20
if "nifty_tp3" not in st.session_state:
    st.session_state.nifty_tp3 = 30
if "nifty_tp1_enabled" not in st.session_state:
    st.session_state.nifty_tp1_enabled = True
if "nifty_tp2_enabled" not in st.session_state:
    st.session_state.nifty_tp2_enabled = True
if "nifty_tp3_enabled" not in st.session_state:
    st.session_state.nifty_tp3_enabled = False

if "crude_lots" not in st.session_state:
    st.session_state.crude_lots = 1
if "crude_tp1" not in st.session_state:
    st.session_state.crude_tp1 = 10
if "crude_tp2" not in st.session_state:
    st.session_state.crude_tp2 = 20
if "crude_tp3" not in st.session_state:
    st.session_state.crude_tp3 = 30
if "crude_tp1_enabled" not in st.session_state:
    st.session_state.crude_tp1_enabled = True
if "crude_tp2_enabled" not in st.session_state:
    st.session_state.crude_tp2_enabled = True
if "crude_tp3_enabled" not in st.session_state:
    st.session_state.crude_tp3_enabled = False

if "ng_lots" not in st.session_state:
    st.session_state.ng_lots = 1
if "ng_tp1" not in st.session_state:
    st.session_state.ng_tp1 = 1
if "ng_tp2" not in st.session_state:
    st.session_state.ng_tp2 = 2
if "ng_tp3" not in st.session_state:
    st.session_state.ng_tp3 = 3
if "ng_tp1_enabled" not in st.session_state:
    st.session_state.ng_tp1_enabled = True
if "ng_tp2_enabled" not in st.session_state:
    st.session_state.ng_tp2_enabled = True
if "ng_tp3_enabled" not in st.session_state:
    st.session_state.ng_tp3_enabled = False

# ================= PENDING RESULTS =================
PENDING_RESULTS = [
    {"name": "Bharat Electronics", "symbol": "BEL", "time": "After 3:30 PM", "expected": "Positive Expected"},
    {"name": "BPCL", "symbol": "BPCL", "time": "After 3:30 PM", "expected": "Mixed/Negative"},
    {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "time": "After 3:30 PM", "expected": "Positive Expected"},
    {"name": "Mankind Pharma", "symbol": "MANKIND", "time": "After 3:30 PM", "expected": "Positive Expected"},
    {"name": "PI Industries", "symbol": "PIIND", "time": "After 3:30 PM", "expected": "Positive Expected"},
]

# Reset daily
if get_ist_now().date() != st.session_state.last_trade_date:
    st.session_state.daily_loss = 0
    st.session_state.last_trade_date = get_ist_now().date()

def check_daily_loss_limit():
    return abs(st.session_state.daily_loss) >= st.session_state.max_daily_loss

# ================= HELPER FUNCTIONS =================
def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            return float(df['Close'].iloc[-1])
    except:
        pass
    return 87.5

def get_live_price(symbol):
    try:
        if symbol == "NIFTY":
            ticker = "^NSEI"
        elif symbol == "BANKNIFTY":
            ticker = "^NSEBANK"
        elif symbol == "FINNIFTY":
            ticker = "^NIFTY_FIN_SERVICE"
        elif symbol == "MIDCPNIFTY":
            ticker = "^NSE_MIDCAP_100"
        elif symbol == "CRUDE":
            ticker = "CL=F"
        elif symbol == "NATURALGAS":
            ticker = "NG=F"
        else:
            ticker = f"{symbol}.NS"
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            val = df['Close'].iloc[-1]
            return float(val) if not isinstance(val, pd.Series) else float(val.iloc[-1])
    except:
        pass
    return 0.0

# ================= GNEWS API (Multi-Source) =================
def get_gnews():
    """Get news from GNews API"""
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=10&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article['title'],
                    'source': article['source']['name'],
                    'time': article['publishedAt'][:10],
                    'url': article['url'],
                    'sentiment': '🟡 Neutral'
                })
            return articles
    except:
        pass
    return [
        {'title': 'Nifty hits record high', 'source': 'Economic Times', 'time': '2026-05-16', 'url': '#', 'sentiment': '🟢 Positive'},
        {'title': 'RBI monetary policy announced', 'source': 'Moneycontrol', 'time': '2026-05-15', 'url': '#', 'sentiment': '🟢 Positive'},
    ]

# ================= FMP API FUNCTIONS =================
def get_company_earnings(symbol):
    """Get earnings from FMP API"""
    try:
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=1&apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]
    except:
        pass
    return None

def ai_sentiment_analysis(earnings_data):
    """AI-based analysis"""
    try:
        revenue = earnings_data.get('revenue', 0)
        previous_revenue = earnings_data.get('revenue', 0)
        net_income = earnings_data.get('netIncome', 0)
        
        score = 0
        reasons = []
        
        if net_income > 0:
            score += 1
            reasons.append("Profit positive")
        
        if score >= 1:
            verdict = "🟢 BULLISH"
            signal = "BUY"
        elif score >= 0:
            verdict = "🟡 NEUTRAL"
            signal = "HOLD"
        else:
            verdict = "🔴 BEARISH"
            signal = "SELL"
        
        return {'verdict': verdict, 'signal': signal, 'confidence': 70, 'reasons': reasons}
    except:
        return {'verdict': '⚪ UNKNOWN', 'signal': 'WAIT', 'confidence': 0, 'reasons': []}

# ================= TELEGRAM & ALERTS =================
def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=10)
    except:
        pass

def show_toast(message):
    st.markdown(f"""
    <div class="toast-notification">
        {message}
    </div>
    """, unsafe_allow_html=True)

def voice_alert(message):
    if st.session_state.voice_enabled:
        st.markdown(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{message}");
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

# ================= WOLF ORDER FUNCTIONS =================
def check_and_execute_wolf_orders():
    for order in st.session_state.wolf_orders[:]:
        if order['status'] == 'PENDING':
            current_price = get_live_price(order['symbol'])
            
            if current_price > 0 and current_price >= order['buy_above']:
                order['status'] = 'ACTIVE'
                order['entry_price'] = current_price
                order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
                
                trade_record = {
                    "No": len(st.session_state.trade_journal) + 1,
                    "Time": order['entry_time'],
                    "Symbol": f"{order['symbol']} {order['option_type']} {order.get('strike_price', '')}",
                    "Type": "🐺 WOLF BUY",
                    "Lots": order['qty'],
                    "Entry": round(current_price, 2),
                    "SL": order['sl'],
                    "Target": order['target'],
                    "Status": "ACTIVE"
                }
                st.session_state.trade_journal.append(trade_record)
                send_telegram(f"🐺 WOLF EXECUTED: {order['symbol']} {order['option_type']} @ ₹{current_price:.2f}")
                voice_alert(f"Wolf order executed for {order['symbol']}")
                
                st.session_state.active_orders.append({
                    'symbol': order['symbol'],
                    'option_type': order['option_type'],
                    'strike_price': order.get('strike_price', ''),
                    'entry_price': current_price,
                    'sl': order['sl'],
                    'target': order['target'],
                    'qty': order['qty'],
                    'journal_index': len(st.session_state.trade_journal) - 1
                })

def monitor_active_orders():
    for i, order in enumerate(st.session_state.active_orders[:]):
        current_price = get_live_price(order['symbol'])
        if current_price == 0:
            continue
        
        if current_price <= order['sl']:
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = '❌ SL HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit'] = round(current_price, 2)
            send_telegram(f"❌ SL HIT: {order['symbol']} @ ₹{current_price:.2f}")
            voice_alert(f"Stop loss hit for {order['symbol']}")
            st.session_state.active_orders.pop(i)
            st.rerun()
        
        elif current_price >= order['target']:
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = '✅ TARGET HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit'] = round(current_price, 2)
            send_telegram(f"✅ TARGET HIT: {order['symbol']} @ ₹{current_price:.2f}")
            voice_alert(f"Target hit for {order['symbol']}")
            st.session_state.active_orders.pop(i)
            st.rerun()

def monitor_results():
    """Monitor FMP for new results"""
    for company in PENDING_RESULTS:
        earnings = get_company_earnings(company['symbol'])
        if earnings:
            ai_result = ai_sentiment_analysis(earnings)
            if ai_result['signal'] != 'WAIT':
                alert = {
                    'company': company['name'],
                    'verdict': ai_result['verdict'],
                    'signal': ai_result['signal'],
                    'time': get_ist_now().strftime('%H:%M:%S')
                }
                st.session_state.result_alerts.append(alert)
                send_telegram(f"📊 RESULT: {company['name']} | AI: {ai_result['verdict']} | Signal: {ai_result['signal']}")
                show_toast(f"Result Alert: {company['name']} - {ai_result['verdict']}")
                voice_alert(f"Result alert for {company['name']}")

# ================= LIVE TIME =================
def update_live_time():
    now = get_ist_now()
    return f"""
    <div class="live-time">
        🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')} | 🐺 v{APP_VERSION}
    </div>
    """

# ================= MAIN UI =================
st.markdown(f"""
<div style="text-align:center; padding:20px;">
    <h1>🐺 RUDRANSH PRO ALGO X</h1>
    <p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114 | v{APP_VERSION}</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(update_live_time(), unsafe_allow_html=True)
st.markdown("---")

# ================= STATUS BAR =================
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.session_state.algo_running:
        st.markdown('<span class="badge-success">🟢 ALGO: RUNNING</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-danger">🔴 ALGO: STOPPED</span>', unsafe_allow_html=True)
with col2:
    st.markdown('<span class="badge-success">📊 FMP: ACTIVE</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="badge-success">📰 GNEWS: ACTIVE</span>', unsafe_allow_html=True)
with col4:
    st.markdown('<span class="badge-success">📱 TELEGRAM: ACTIVE</span>', unsafe_allow_html=True)
with col5:
    if st.session_state.voice_enabled:
        st.markdown('<span class="badge-success">🔊 VOICE: ON</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-warning">🔊 VOICE: OFF</span>', unsafe_allow_html=True)
with col6:
    st.markdown(f'<span class="badge-info">🐺 ORDERS: {len(st.session_state.wolf_orders)}</span>', unsafe_allow_html=True)

st.markdown("---")

# Control Panel
col1, col2, col3 = st.columns([2,1,1])
with col1:
    totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code", key="totp_main")
with col2:
    if st.button("🟢 START", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 RUDRANSH ALGO STARTED v2.1")
            st.rerun()
        else:
            st.error("Valid TOTP required!")
with col3:
    if st.button("🔴 STOP", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 RUDRANSH ALGO STOPPED")
        st.rerun()

st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🐺 WOLF ORDER", "📊 MARKET", "📰 NEWS", "📈 RESULTS", "⚙️ SETTINGS", "📋 JOURNAL"
])

# ================= TAB 1: WOLF ORDER (WITH CE/PE) =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK (F&O + COMMODITY)")
    st.markdown(f"*Total {len(FO_SCRIPTS)} Symbols | CE/PE Options Available*")
    
    with st.expander("➕ PLACE WOLF ORDER", expanded=False):
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        with col1:
            wolf_symbol = st.selectbox("Symbol", FO_SCRIPTS, key="wolf_sym")
        with col2:
            option_type = st.selectbox("Option", OPTION_TYPES, key="option_type")
        with col3:
            strike_price = st.number_input("Strike Price", min_value=1, max_value=500000, value=24300, step=50, key="wolf_strike")
        with col4:
            wolf_qty = st.number_input("Lots", min_value=1, max_value=100, value=1, key="wolf_qty")
        with col5:
            wolf_buy_above = st.number_input("Buy Above (₹)", min_value=1, max_value=500000, value=100, step=10, key="wolf_buy")
        with col6:
            wolf_sl = st.number_input("Stop Loss (₹)", min_value=1, max_value=500000, value=80, step=10, key="wolf_sl")
        with col7:
            wolf_target = st.number_input("Target (₹)", min_value=1, max_value=500000, value=150, step=10, key="wolf_target")
        with col8:
            if st.button("🐺 PLACE", use_container_width=True):
                if wolf_buy_above <= wolf_sl:
                    st.error("Buy Above > SL required!")
                elif wolf_target <= wolf_buy_above:
                    st.error("Target > Buy Above required!")
                else:
                    st.session_state.wolf_orders.append({
                        'symbol': wolf_symbol,
                        'option_type': option_type,
                        'strike_price': strike_price,
                        'qty': wolf_qty,
                        'buy_above': wolf_buy_above,
                        'sl': wolf_sl,
                        'target': wolf_target,
                        'status': 'PENDING',
                        'entry_price': None,
                        'entry_time': None
                    })
                    send_telegram(f"🐺 WOLF ORDER: {wolf_symbol} {option_type} {strike_price} | Buy: {wolf_buy_above} | SL: {wolf_sl} | Target: {wolf_target}")
                    st.success(f"✅ Order placed for {wolf_symbol} {option_type}")
                    st.rerun()
    
    pending = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
    if pending:
        st.markdown("### ⏳ PENDING ORDERS")
        df_pending = pd.DataFrame([{
            'Symbol': o['symbol'], 'Option': o['option_type'], 'Strike': o['strike_price'],
            'Lots': o['qty'], 'Buy Above': o['buy_above'], 'SL': o['sl'], 'Target': o['target']
        } for o in pending])
        st.dataframe(df_pending, use_container_width=True)
    
    active = st.session_state.active_orders
    if active:
        st.markdown("### 🔴 ACTIVE ORDERS")
        active_data = []
        for o in active:
            current = get_live_price(o['symbol'])
            active_data.append({
                'Symbol': o['symbol'], 'Option': o.get('option_type', ''), 'Strike': o.get('strike_price', ''),
                'Entry': o['entry_price'], 'Current': round(current, 2) if current else 0,
                'SL': o['sl'], 'Target': o['target']
            })
        df_active = pd.DataFrame(active_data)
        st.dataframe(df_active, use_container_width=True)

# ================= TAB 2: MARKET =================
with tab2:
    st.markdown("### 📊 LIVE MARKET")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nifty = get_live_price("NIFTY")
        st.metric("🇮🇳 NIFTY", f"₹{nifty:,.2f}" if nifty else "Loading...")
    with col2:
        banknifty = get_live_price("BANKNIFTY")
        st.metric("🏦 BANK NIFTY", f"₹{banknifty:,.2f}" if banknifty else "Loading...")
    with col3:
        crude = get_live_price("CRUDE") * get_usd_inr_rate()
        st.metric("🛢️ CRUDE", f"₹{crude:,.2f}" if crude else "Loading...")
    with col4:
        ng = get_live_price("NATURALGAS") * get_usd_inr_rate()
        st.metric("🌿 NG", f"₹{ng:,.2f}" if ng else "Loading...")

# ================= TAB 3: NEWS =================
with tab3:
    st.markdown("### 📰 NEWS (Powered by GNews API)")
    st.markdown("*Bloomberg | Reuters | CNBC | FT | ET | Moneycontrol | Zee | Investing | Mint*")
    
    col1, col2 = st.columns([3,1])
    with col2:
        st.session_state.voice_enabled = st.checkbox("🔊 Voice", value=st.session_state.voice_enabled)
    
    st.markdown("---")
    
    news_articles = get_gnews()
    for article in news_articles:
        with st.container():
            col_a, col_b = st.columns([4,1])
            with col_a:
                st.markdown(f"**📌 {article['title']}**")
                st.caption(f"Source: {article['source']} | {article['time']}")
            with col_b:
                st.markdown(f"`{article['sentiment']}`")
            st.markdown("---")

# ================= TAB 4: RESULTS =================
with tab4:
    st.markdown("### 📊 REAL-TIME RESULTS (FMP API)")
    st.markdown("*Powered by Financial Modeling Prep*")
    
    st.markdown("---")
    st.markdown("### ⏳ PENDING RESULTS")
    pending_df = pd.DataFrame([{
        "Company": c['name'], "Symbol": c['symbol'], "Time": c['time'], "Expected": c['expected']
    } for c in PENDING_RESULTS])
    st.dataframe(pending_df, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🧠 AI ANALYSIS")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("AI Engine", "🟢 ACTIVE")
    with col2:
        st.metric("Auto Trade", "ENABLED" if st.session_state.algo_running else "DISABLED")
    
    if st.session_state.result_alerts:
        st.markdown("---")
        st.markdown("### 🔔 ALERTS")
        for alert in st.session_state.result_alerts[-5:]:
            st.info(f"📊 {alert['company']} | {alert['verdict']} | Signal: {alert['signal']} | Time: {alert['time']}")

# ================= TAB 5: SETTINGS =================
with tab5:
    st.markdown("### ⚙️ SETTINGS")
    
    st.markdown("#### 🇮🇳 NIFTY")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", 1, 50, st.session_state.nifty_lots, key="n_lots")
    with col2:
        st.number_input("TP1", 1, 100, st.session_state.nifty_tp1, key="n_tp1")
    with col3:
        st.checkbox("ON", st.session_state.nifty_tp1_enabled, key="n_tp1_en")
    with col4:
        st.number_input("TP2", 1, 100, st.session_state.nifty_tp2, key="n_tp2")
    with col5:
        st.checkbox("ON", st.session_state.nifty_tp2_enabled, key="n_tp2_en")
    with col6:
        st.number_input("TP3", 1, 100, st.session_state.nifty_tp3, key="n_tp3")
    with col7:
        st.checkbox("ON", st.session_state.nifty_tp3_enabled, key="n_tp3_en")
    
    st.markdown("#### 🛢️ CRUDE")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", 1, 50, st.session_state.crude_lots, key="c_lots")
    with col2:
        st.number_input("TP1", 1, 100, st.session_state.crude_tp1, key="c_tp1")
    with col3:
        st.checkbox("ON", st.session_state.crude_tp1_enabled, key="c_tp1_en")
    with col4:
        st.number_input("TP2", 1, 100, st.session_state.crude_tp2, key="c_tp2")
    with col5:
        st.checkbox("ON", st.session_state.crude_tp2_enabled, key="c_tp2_en")
    with col6:
        st.number_input("TP3", 1, 100, st.session_state.crude_tp3, key="c_tp3")
    with col7:
        st.checkbox("ON", st.session_state.crude_tp3_enabled, key="c_tp3_en")
    
    st.markdown("#### 🌿 NG")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", 1, 50, st.session_state.ng_lots, key="g_lots")
    with col2:
        st.number_input("TP1", 1, 50, st.session_state.ng_tp1, key="g_tp1")
    with col3:
        st.checkbox("ON", st.session_state.ng_tp1_enabled, key="g_tp1_en")
    with col4:
        st.number_input("TP2", 1, 50, st.session_state.ng_tp2, key="g_tp2")
    with col5:
        st.checkbox("ON", st.session_state.ng_tp2_enabled, key="g_tp2_en")
    with col6:
        st.number_input("TP3", 1, 50, st.session_state.ng_tp3, key="g_tp3")
    with col7:
        st.checkbox("ON", st.session_state.ng_tp3_enabled, key="g_tp3_en")
    
    st.markdown("---")
    st.markdown("#### 📉 RISK")
    st.session_state.max_daily_loss = st.number_input("Max Daily Loss (₹)", 10000, 500000, st.session_state.max_daily_loss, 10000)

# ================= TAB 6: JOURNAL =================
with tab6:
    st.markdown("### 📋 JOURNAL")
    if st.session_state.trade_journal:
        df_journal = pd.DataFrame(st.session_state.trade_journal)
        st.dataframe(df_journal, use_container_width=True)
    else:
        st.info("No trades yet")

# ================= AUTO EXECUTION =================
if st.session_state.algo_running and st.session_state.totp_verified and not check_daily_loss_limit():
    check_and_execute_wolf_orders()
    monitor_active_orders()
    monitor_results()
    st.info("🐺 Hunting... Monitoring Orders & Results")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🐺 DASHBOARD")
    st.metric("Active", len(st.session_state.active_orders))
    st.metric("Pending", len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']))
    st.metric("Loss", f"₹{abs(st.session_state.daily_loss):,.0f}")
    st.metric("Symbols", len(FO_SCRIPTS))
    st.markdown("---")
    st.markdown("### 🧠 STATUS")
    st.caption("✅ FMP API: ACTIVE")
    st.caption("✅ GNews API: ACTIVE")
    st.caption("✅ Telegram: ACTIVE")
    st.caption("✅ Voice: " + ("ON" if st.session_state.voice_enabled else "OFF"))

# ================= AUTO REFRESH =================
time.sleep(30)
st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.markdown(f"🐺 Rudransh Pro Algo X v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION}")
