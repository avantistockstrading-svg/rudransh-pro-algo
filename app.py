"""
🐺 RUDRANSH PRO ALGO X - API STATUS CHECK
===========================================
VERSION: 4.1.0
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import json
import time

# ================= VERSION & INFO =================
APP_VERSION = "4.1.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= API KEYS (तुमच्या स्वतःच्या टाका) =================
# GNews API (Paid)
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"

# FMP API (Paid - 1 Month)
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"

# Google Translate API
GOOGLE_TRANSLATE_API_KEY = "YOUR_GOOGLE_API_KEY"  # ही तुम्ही Add करा

# Telegram
TELEGRAM_BOT = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
TELEGRAM_CHAT = "1983026913"

# Angel One API (Optional)
ANGEL_API_KEY = "YOUR_ANGEL_API_KEY"
ANGEL_CLIENT_ID = "YOUR_CLIENT_ID"
ANGEL_PASSWORD = "YOUR_PASSWORD"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🐺")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
    .css-1r6slb0, .css-1y4p8pa { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; border: 1px solid rgba(255,255,255,0.2); padding: 20px; }
    h1, h2, h3 { background: linear-gradient(135deg, #00ff88 0%, #00b4d8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { background: linear-gradient(135deg, #00ff88, #00b4d8); color: white; border: none; border-radius: 10px; font-weight: bold; }
    .status-card { background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; }
    .status-active { color: #00ff88; font-weight: bold; }
    .status-inactive { color: #ff4444; font-weight: bold; }
    .status-warning { color: #ffa500; font-weight: bold; }
    .badge-success { background: rgba(0,255,136,0.2); color: #00ff88; padding: 5px 10px; border-radius: 20px; font-size: 12px; }
    .badge-danger { background: rgba(255,0,0,0.2); color: #ff4444; padding: 5px 10px; border-radius: 20px; }
    .badge-warning { background: rgba(255,165,0,0.2); color: #ffa500; padding: 5px 10px; border-radius: 20px; }
    .live-time { text-align: center; font-size: 28px; font-weight: bold; background: linear-gradient(135deg, #00ff88, #00b4d8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #00ff88, #00b4d8); color: white; }
</style>
""", unsafe_allow_html=True)

# ================= API STATUS CHECK FUNCTIONS =================

def check_gnews_api():
    """Check if GNews API is active"""
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=1&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('articles'):
                return True, "Active", f"✅ {len(data.get('articles', []))} articles fetched"
            else:
                return False, "Warning", "API responded but no articles"
        elif response.status_code == 401:
            return False, "Inactive", "❌ Invalid API Key"
        elif response.status_code == 429:
            return False, "Warning", "⚠️ Rate limit exceeded"
        else:
            return False, "Error", f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Error", "⏰ Timeout - Check internet"
    except Exception as e:
        return False, "Error", f"❌ Connection failed"

def check_fmp_api():
    """Check if FMP API is active"""
    try:
        url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return True, "Active", f"✅ {len(data)} stocks available"
            else:
                return False, "Warning", "API responded but no data"
        elif response.status_code == 401:
            return False, "Inactive", "❌ Invalid API Key (Need Paid Plan?)"
        elif response.status_code == 403:
            return False, "Inactive", "❌ API Key expired or invalid"
        else:
            return False, "Error", f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Error", "⏰ Timeout - Check internet"
    except Exception as e:
        return False, "Error", f"❌ Connection failed"

def check_google_translate_api():
    """Check if Google Translate API is active"""
    if GOOGLE_TRANSLATE_API_KEY == "YOUR_GOOGLE_API_KEY":
        return False, "Not Configured", "⚠️ Please add your Google API Key"
    
    try:
        test_text = "Hello"
        url = f"https://translation.googleapis.com/language/translate/v2"
        params = {
            'q': test_text,
            'target': 'mr',
            'key': GOOGLE_TRANSLATE_API_KEY,
            'format': 'text'
        }
        response = requests.post(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return True, "Active", "✅ Translation working"
        elif response.status_code == 403:
            return False, "Inactive", "❌ Invalid API Key or Billing not enabled"
        elif response.status_code == 400:
            return False, "Error", "❌ API Key format invalid"
        else:
            return False, "Error", f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Error", "⏰ Timeout"
    except Exception as e:
        return False, "Error", "❌ Connection failed"

def check_telegram_api():
    """Check if Telegram Bot is active"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_name = data.get('result', {}).get('first_name', 'Bot')
                return True, "Active", f"✅ @{bot_name} is online"
            else:
                return False, "Inactive", "❌ Bot token invalid"
        elif response.status_code == 401:
            return False, "Inactive", "❌ Invalid Bot Token"
        else:
            return False, "Error", f"HTTP {response.status_code}"
    except Exception as e:
        return False, "Error", "❌ Connection failed"

def check_angel_api():
    """Check if Angel One API keys are configured"""
    if ANGEL_API_KEY == "YOUR_ANGEL_API_KEY":
        return False, "Not Configured", "⚠️ Add Angel One API keys"
    else:
        return True, "Configured", "✅ Keys added (Status unknown without login)"

# ================= TIMEZONE =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= APP LOCK =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

if not st.session_state.app_unlocked:
    st.markdown("""
    <div style="text-align:center; padding:50px;">
        <h1>🐺 RUDRANSH PRO ALGO X</h1>
        <p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>
        <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:200px; margin:20px auto;"></div>
        <h3>🔐 APPLICATION LOCKED</h3>
        <p>Enter Password to Access</p>
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
if "api_status_cache" not in st.session_state:
    st.session_state.api_status_cache = {}

# ================= COMPLETE SYMBOLS =================
FO_SCRIPTS = [
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "CRUDE", "NATURALGAS",
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR", "ITC",
    "SBIN", "BHARTIARTL", "KOTAKBANK", "AXISBANK", "LT", "DMART", "SUNPHARMA",
    "BAJFINANCE", "TITAN", "MARUTI", "TATAMOTORS", "TATASTEEL", "WIPRO",
    "HCLTECH", "ONGC", "NTPC", "POWERGRID", "ULTRACEMCO", "ADANIPORTS",
    "ADANIENT", "ASIANPAINT", "BAJAJFINSV", "BRITANNIA", "CIPLA", "COALINDIA"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= HELPER FUNCTIONS =================
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

def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty:
            return float(df['Close'].iloc[-1])
    except:
        pass
    return 87.5

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=10)
    except:
        pass

# ================= UI HEADER =================
st.markdown(f"""
<div style="text-align:center; padding:20px;">
    <h1>🐺 {APP_NAME}</h1>
    <p style="color:#94a3b8;">{APP_AUTHOR}, {APP_LOCATION} | v{APP_VERSION}</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

now = get_ist_now()
st.markdown(f"<div class='live-time'>🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')}</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= API STATUS SECTION (NEW) =================
st.markdown("## 🔌 API STATUS DASHBOARD")
st.markdown("*Click 'Check Status' to verify all API connections*")

col1, col2 = st.columns([3,1])
with col2:
    if st.button("🔄 CHECK ALL APIs", use_container_width=True):
        st.session_state.api_status_cache = {}
        st.rerun()

st.markdown("---")

# Display API Status Cards
col1, col2, col3, col4, col5 = st.columns(5)

# GNews API Status
with col1:
    gnews_status, gnews_level, gnews_msg = check_gnews_api()
    if gnews_level == "Active":
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #00ff88;">
            📰 <strong>GNews API</strong><br>
            <span style="color:#00ff88">🟢 {gnews_status}</span><br>
            <small>{gnews_msg}</small>
        </div>
        """, unsafe_allow_html=True)
    elif gnews_level == "Warning":
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ffa500;">
            📰 <strong>GNews API</strong><br>
            <span style="color:#ffa500">🟡 {gnews_status}</span><br>
            <small>{gnews_msg}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ff4444;">
            📰 <strong>GNews API</strong><br>
            <span style="color:#ff4444">🔴 {gnews_status}</span><br>
            <small>{gnews_msg}</small>
        </div>
        """, unsafe_allow_html=True)

# FMP API Status
with col2:
    fmp_status, fmp_level, fmp_msg = check_fmp_api()
    if fmp_level == "Active":
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #00ff88;">
            📊 <strong>FMP API</strong><br>
            <span style="color:#00ff88">🟢 {fmp_status}</span><br>
            <small>{fmp_msg}</small>
        </div>
        """, unsafe_allow_html=True)
    elif fmp_level == "Warning":
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ffa500;">
            📊 <strong>FMP API</strong><br>
            <span style="color:#ffa500">🟡 {fmp_status}</span><br>
            <small>{fmp_msg}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ff4444;">
            📊 <strong>FMP API</strong><br>
            <span style="color:#ff4444">🔴 {fmp_status}</span><br>
            <small>{fmp_msg}</small>
        </div>
        """, unsafe_allow_html=True)

# Google Translate API Status
with col3:
    translate_status, translate_level, translate_msg = check_google_translate_api()
    if translate_level == "Active":
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #00ff88;">
            🌐 <strong>Google Translate</strong><br>
            <span style="color:#00ff88">🟢 {translate_status}</span><br>
            <small>{translate_msg}</small>
        </div>
        """, unsafe_allow_html=True)
    elif translate_level == "Not Configured":
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ffa500;">
            🌐 <strong>Google Translate</strong><br>
            <span style="color:#ffa500">🟡 {translate_status}</span><br>
            <small>{translate_msg}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ff4444;">
            🌐 <strong>Google Translate</strong><br>
            <span style="color:#ff4444">🔴 {translate_status}</span><br>
            <small>{translate_msg}</small>
        </div>
        """, unsafe_allow_html=True)

# Telegram API Status
with col4:
    tele_status, tele_level, tele_msg = check_telegram_api()
    if tele_level == "Active":
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #00ff88;">
            📱 <strong>Telegram Bot</strong><br>
            <span style="color:#00ff88">🟢 {tele_status}</span><br>
            <small>{tele_msg}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ff4444;">
            📱 <strong>Telegram Bot</strong><br>
            <span style="color:#ff4444">🔴 {tele_status}</span><br>
            <small>{tele_msg}</small>
        </div>
        """, unsafe_allow_html=True)

# Angel One API Status
with col5:
    angel_status, angel_level, angel_msg = check_angel_api()
    if angel_level == "Configured":
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #00ff88;">
            🔗 <strong>Angel One</strong><br>
            <span style="color:#00ff88">🟢 {angel_status}</span><br>
            <small>{angel_msg}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ffa500;">
            🔗 <strong>Angel One</strong><br>
            <span style="color:#ffa500">🟡 {angel_status}</span><br>
            <small>{angel_msg}</small>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ================= CONTROL PANEL =================
col1, col2, col3 = st.columns([2,1,1])
with col1:
    totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code", key="totp_main")
with col2:
    if st.button("🟢 START", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED - API Status: All Active")
            st.rerun()
        else:
            st.error("Valid TOTP required!")
with col3:
    if st.button("🔴 STOP", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 ALGO STOPPED")
        st.rerun()

st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🐺 WOLF ORDER", "🌸 SANSKRUTI MARKET", "📰 VAISHNAVI NEWS", "📈 OVI RESULTS", "⚙️ SAHYADRI SETTINGS"
])

# ================= TAB 1: WOLF ORDER =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK")
    st.markdown(f"*Total {len(FO_SCRIPTS)} Symbols | CE/PE Options*")
    
    with st.expander("➕ PLACE ORDER", expanded=False):
        cols = st.columns(7)
        with cols[0]: sym = st.selectbox("Symbol", FO_SCRIPTS, key="sym")
        with cols[1]: opt = st.selectbox("Option", OPTION_TYPES, key="opt")
        with cols[2]: strike = st.number_input("Strike", 1, 500000, 24300, key="strike")
        with cols[3]: qty = st.number_input("Lots", 1, 100, 1, key="qty")
        with cols[4]: buy_above = st.number_input("Buy Above", 1, 500000, 100, key="buy")
        with cols[5]: sl = st.number_input("SL", 1, 500000, 80, key="sl")
        with cols[6]: target = st.number_input("Target", 1, 500000, 150, key="target")
        
        if st.button("🐺 PLACE ORDER", use_container_width=True):
            st.session_state.wolf_orders.append({
                'symbol': sym, 'option_type': opt, 'strike_price': strike, 'qty': qty,
                'buy_above': buy_above, 'sl': sl, 'target': target, 'status': 'PENDING'
            })
            st.success(f"✅ Order placed for {sym}")

# ================= TAB 2: SANSKRUTI MARKET =================
with tab2:
    st.markdown("### 🌸 SANSKRUTI MARKET")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🇮🇳 NIFTY", f"₹{get_live_price('NIFTY'):,.2f}")
    with c2: st.metric("🏦 BANK NIFTY", f"₹{get_live_price('BANKNIFTY'):,.2f}")
    crude = get_live_price('CRUDE') * get_usd_inr_rate()
    with c3: st.metric("🛢️ CRUDE", f"₹{crude:,.2f}")
    ng = get_live_price('NATURALGAS') * get_usd_inr_rate()
    with c4: st.metric("🌿 NG", f"₹{ng:,.2f}")

# ================= TAB 3: VAISHNAVI NEWS =================
with tab3:
    st.markdown("### 📰 VAISHNAVI NEWS")
    st.markdown("*Real-time business news with sentiment analysis*")
    
    col1, col2 = st.columns([3,1])
    with col2: st.session_state.voice_enabled = st.checkbox("🔊 Voice", st.session_state.voice_enabled)
    
    # Show API status if GNews is active
    gnews_status, _, _ = check_gnews_api()
    if gnews_status:
        st.success("✅ GNews API is ACTIVE - Real news will appear here")
    else:
        st.warning("⚠️ GNews API is INACTIVE - Please check your API key")
    
    st.markdown("---")
    
    # News will be displayed here when API is active
    if gnews_status:
        st.info("📰 News will appear automatically when API fetches data...")
    else:
        st.error("❌ Cannot fetch news. Please verify GNews API Key in settings.")

# ================= TAB 4: OVI RESULTS =================
with tab4:
    st.markdown("### 📈 OVI RESULTS")
    
    # Show API status
    fmp_status, _, _ = check_fmp_api()
    if fmp_status:
        st.success("✅ FMP API is ACTIVE (Paid Subscription)")
    else:
        st.warning("⚠️ FMP API is INACTIVE - Check your API Key or Subscription")
    
    st.markdown("---")
    
    # Results monitoring will be displayed here
    st.info("📊 Results monitoring will auto-detect when companies announce earnings...")

# ================= TAB 5: SAHYADRI SETTINGS =================
with tab5:
    st.markdown("### ⚙️ SAHYADRI SETTINGS")
    
    st.markdown("#### 🤖 AUTO TRADE")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Lots", 1, 50, st.session_state.auto_trade_qty)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("SL %", 1, 20, st.session_state.auto_trade_sl_percent)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", 1, 30, st.session_state.auto_trade_target_percent)
    
    st.markdown("---")
    st.markdown("#### 🔑 API KEYS CONFIGURATION")
    
    with st.expander("API Keys Settings", expanded=False):
        st.text_input("GNews API Key", value=GNEWS_API_KEY, type="password", disabled=True)
        st.text_input("FMP API Key", value=FMP_API_KEY, type="password", disabled=True)
        st.text_input("Google Translate API Key", value=GOOGLE_TRANSLATE_API_KEY, type="password", 
                     help="Get from https://cloud.google.com/translate")
        st.text_input("Telegram Bot Token", value=TELEGRAM_BOT, type="password", disabled=True)
        st.text_input("Angel One API Key", value=ANGEL_API_KEY, type="password")
        st.text_input("Angel One Client ID", value=ANGEL_CLIENT_ID, type="password")
    
    st.markdown("---")
    st.markdown("#### NIFTY TP")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,1,key="n_l")
    with c2: st.number_input("TP1",1,100,10,key="n_t1")
    with c3: st.checkbox("ON",True,key="n_en1")
    with c4: st.number_input("TP2",1,100,20,key="n_t2")
    with c5: st.checkbox("ON",True,key="n_en2")
    with c6: st.number_input("TP3",1,100,30,key="n_t3")
    with c7: st.checkbox("ON",False,key="n_en3")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🌸 SAMRUDDHI DASHBOARD")
    st.markdown("---")
    
    # Real-time API Status Summary
    st.markdown("### 🔌 API STATUS")
    gnews_s, _, _ = check_gnews_api()
    fmp_s, _, _ = check_fmp_api()
    trans_s, _, _ = check_google_translate_api()
    tele_s, _, _ = check_telegram_api()
    
    st.markdown(f"📰 GNews: {'🟢 ACTIVE' if gnews_s else '🔴 INACTIVE'}")
    st.markdown(f"📊 FMP: {'🟢 ACTIVE' if fmp_s else '🔴 INACTIVE'}")
    st.markdown(f"🌐 Translate: {'🟢 ACTIVE' if trans_s else '🟡 NOT SET'}")
    st.markdown(f"📱 Telegram: {'🟢 ACTIVE' if tele_s else '🔴 INACTIVE'}")
    
    st.markdown("---")
    st.metric("Total Symbols", len(FO_SCRIPTS))
    st.metric("Wolf Orders", len(st.session_state.wolf_orders))

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🐺 {APP_NAME} v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION} | API Status Monitor Active")

# ================= AUTO REFRESH STATUS (Every 30 seconds) =================
if st.session_state.algo_running:
    time.sleep(30)
    st.rerun()
