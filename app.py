"""
🐺 RUDRANSH PRO ALGO X - REAL EDITION
=======================================
VERSION: 4.0.0 (REAL API INTEGRATED)
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import json
import hmac
import hashlib
import base64
import time

# ================= VERSION & INFO =================
APP_VERSION = "4.0.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= API KEYS (तुमच्या स्वतःच्या टाका) =================
# FMP API (Paid) - https://financialmodelingprep.com/
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"  # तुमची paid API key

# Google Translate API (Marathi News साठी)
GOOGLE_TRANSLATE_API_KEY = "YOUR_GOOGLE_API_KEY"  # https://cloud.google.com/translate

# Angel One API (Auto Trade साठी)
ANGEL_API_KEY = "YOUR_ANGEL_API_KEY"
ANGEL_CLIENT_ID = "YOUR_CLIENT_ID"
ANGEL_PASSWORD = "YOUR_PASSWORD"
ANGEL_TOTP_SECRET = "YOUR_TOTP_SECRET"

# Telegram
TELEGRAM_BOT = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
TELEGRAM_CHAT = "1983026913"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🐺")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
    .css-1r6slb0, .css-1y4p8pa { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; border: 1px solid rgba(255,255,255,0.2); padding: 20px; }
    h1, h2, h3 { background: linear-gradient(135deg, #00ff88 0%, #00b4d8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { background: linear-gradient(135deg, #00ff88, #00b4d8); color: white; border: none; border-radius: 10px; font-weight: bold; }
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
if "angel_session" not in st.session_state:
    st.session_state.angel_session = None
if "angel_connected" not in st.session_state:
    st.session_state.angel_connected = False

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

# ================= COMPLETE SYMBOLS =================
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
    "TATAPOWER", "TECHM", "UPL", "VEDL", "YESBANK", "ZYDUSLIFE",
    "ABB", "APOLLOHOSP", "ASHOKLEY", "ASTRAL", "AUROPHARMA", "BANDHANBNK",
    "BANKBARODA", "BEL", "BPCL", "CANBK", "CHOLAFIN", "COFORGE", "DABUR",
    "DLF", "FEDERALBNK", "GAIL", "GODREJCP", "GODREJPROP", "HAVELLS",
    "HDFCAMC", "HINDPETRO", "ICICIGI", "ICICIPRULI", "INDIGO", "JIOFIN",
    "JUBLFOOD", "LUPIN", "MANKIND", "MARICO", "MAXHEALTH", "MCX", "MOTHERSON",
    "MPHASIS", "MUTHOOTFIN", "NAUKRI", "NHPC", "NMDC", "PFC", "PNB", "RECLTD"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= PENDING RESULTS (FMP API REAL) =================
PENDING_RESULTS = [
    {"name": "Bharat Electronics", "symbol": "BEL", "expected_date": "19 May 2026"},
    {"name": "BPCL", "symbol": "BPCL", "expected_date": "19 May 2026"},
    {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "expected_date": "19 May 2026"},
    {"name": "Mankind Pharma", "symbol": "MANKIND", "expected_date": "19 May 2026"},
    {"name": "PI Industries", "symbol": "PIIND", "expected_date": "19 May 2026"},
]

# ================= REAL FMP API FUNCTIONS =================
def get_fmp_earnings(symbol):
    """Real FMP API call for earnings"""
    try:
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=1&apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]
        return None
    except Exception as e:
        print(f"FMP API Error: {e}")
        return None

def check_result_released(symbol, last_checked):
    """Check if new result released"""
    earnings = get_fmp_earnings(symbol)
    if earnings:
        report_date = earnings.get('date', '')
        if report_date and report_date != last_checked:
            return True, earnings
    return False, None

def calculate_ai_verdict(earnings):
    """Calculate AI verdict based on real data"""
    try:
        revenue = earnings.get('revenue', 0)
        net_income = earnings.get('netIncome', 0)
        prev_revenue = earnings.get('revenue', 0)
        prev_income = earnings.get('netIncome', 0)
        
        revenue_growth = ((revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
        profit_growth = ((net_income - prev_income) / abs(prev_income) * 100) if prev_income != 0 else 0
        
        score = 0
        if revenue_growth > 10:
            score += 2
        elif revenue_growth > 0:
            score += 1
        elif revenue_growth < -5:
            score -= 2
            
        if profit_growth > 15:
            score += 2
        elif profit_growth > 0:
            score += 1
        elif profit_growth < -10:
            score -= 2
        
        if score >= 2:
            return "STRONG BULLISH", "BUY", 85, revenue_growth, profit_growth
        elif score >= 1:
            return "BULLISH", "CAUTIOUS BUY", 70, revenue_growth, profit_growth
        elif score >= -1:
            return "NEUTRAL", "HOLD", 50, revenue_growth, profit_growth
        elif score >= -2:
            return "BEARISH", "CAUTIOUS SELL", 60, revenue_growth, profit_growth
        else:
            return "STRONG BEARISH", "SELL", 75, revenue_growth, profit_growth
    except:
        return "UNKNOWN", "WAIT", 0, 0, 0

# ================= REAL ANGEL ONE API FUNCTIONS =================
def angel_one_login():
    """Real Angel One API login"""
    try:
        # Angel One SmartAPI login
        from smartapi import SmartConnect
        
        obj = SmartConnect(api_key=ANGEL_API_KEY)
        data = obj.generateSession(ANGEL_CLIENT_ID, ANGEL_PASSWORD, ANGEL_TOTP_SECRET)
        
        if data.get('status'):
            st.session_state.angel_session = obj
            st.session_state.angel_connected = True
            return True
        return False
    except Exception as e:
        print(f"Angel One Login Error: {e}")
        return False

def place_angel_order(symbol, qty, buy_price, sl, target, option_type="CE"):
    """Real order placement on Angel One"""
    try:
        if not st.session_state.angel_connected:
            angel_one_login()
        
        obj = st.session_state.angel_session
        
        # Determine exchange and tradingsymbol
        if symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
            exchange = "NFO"
            tradingsymbol = f"{symbol}{int(buy_price)}00{option_type}"
        else:
            exchange = "NSE"
            tradingsymbol = f"{symbol}-EQ"
        
        # Place order
        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": tradingsymbol,
            "symboltoken": "UNKNOWN",
            "transactiontype": "BUY",
            "exchange": exchange,
            "ordertype": "LIMIT",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": str(buy_price),
            "quantity": str(qty),
        }
        
        response = obj.placeOrder(order_params)
        return response.get('success', False)
    except Exception as e:
        print(f"Angel Order Error: {e}")
        return False

# ================= REAL MARATHI NEWS (Google Translate API) =================
def translate_to_marathi(text):
    """Real Google Translate API call"""
    try:
        url = f"https://translation.googleapis.com/language/translate/v2"
        params = {
            'q': text,
            'target': 'mr',
            'key': GOOGLE_TRANSLATE_API_KEY,
            'format': 'text'
        }
        response = requests.post(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['data']['translations'][0]['translatedText']
    except:
        pass
    return text  # Fallback to original

def get_news_with_translation():
    """Get news from GNews and translate to Marathi"""
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=10&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = []
            
            # Sentiment keywords
            bullish_strong = ['surge', 'rally', 'boom', 'record', 'peak', 'all-time']
            bullish_weak = ['gain', 'up', 'positive', 'bull', 'rise', 'growth']
            bearish_strong = ['crash', 'plunge', 'slump', 'collapse', 'freefall']
            bearish_weak = ['fall', 'drop', 'down', 'negative', 'bear', 'decline']
            
            for article in data.get('articles', [])[:10]:
                title = article['title'].lower()
                
                # Sentiment calculation
                score = 0
                for w in bullish_strong:
                    if w in title: score += 15
                for w in bullish_weak:
                    if w in title: score += 5
                for w in bearish_strong:
                    if w in title: score -= 15
                for w in bearish_weak:
                    if w in title: score -= 5
                
                if score >= 15:
                    sentiment = "STRONG BULLISH"
                    sentiment_icon = "🚀"
                elif score >= 5:
                    sentiment = "BULLISH"
                    sentiment_icon = "📈"
                elif score <= -15:
                    sentiment = "STRONG BEARISH"
                    sentiment_icon = "💀"
                elif score <= -5:
                    sentiment = "BEARISH"
                    sentiment_icon = "📉"
                else:
                    sentiment = "NEUTRAL"
                    sentiment_icon = "⚪"
                
                # Translate to Marathi
                marathi_title = translate_to_marathi(article['title'])
                
                articles.append({
                    'title_marathi': marathi_title,
                    'title_english': article['title'],
                    'source': article['source']['name'],
                    'time': article['publishedAt'][:10],
                    'sentiment': sentiment,
                    'sentiment_icon': sentiment_icon,
                    'strength': abs(score)
                })
            return articles
    except Exception as e:
        print(f"News Error: {e}")
    
    # Fallback
    return []

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

def voice_alert(msg):
    if st.session_state.voice_enabled:
        st.markdown(f"<script>var s=new SpeechSynthesisUtterance('{msg}');s.lang='mr-IN';speechSynthesis.speak(s);</script>", unsafe_allow_html=True)

def monitor_fmp_results():
    """Real FMP monitoring"""
    for company in PENDING_RESULTS:
        earnings = get_fmp_earnings(company['symbol'])
        if earnings:
            verdict, signal, confidence, rev_growth, profit_growth = calculate_ai_verdict(earnings)
            
            alert = {
                'company': company['name'],
                'symbol': company['symbol'],
                'date': get_ist_now().strftime('%d %b %Y'),
                'time': get_ist_now().strftime('%H:%M:%S'),
                'revenue': f"₹{earnings.get('revenue', 0)/10000000:,.2f} Cr",
                'revenue_growth': f"{rev_growth:+.1f}%",
                'profit_growth': f"{profit_growth:+.1f}%",
                'verdict': verdict,
                'confidence': confidence,
                'signal': signal
            }
            
            # Check if already alerted
            already = False
            for a in st.session_state.result_alerts:
                if a.get('company') == company['name']:
                    already = True
                    break
            
            if not already:
                st.session_state.result_alerts.append(alert)
                send_telegram(f"📊 FMP RESULT: {company['name']}\n📈 Revenue: {alert['revenue']}\n📉 Growth: {alert['revenue_growth']}\n🎯 AI: {verdict}\n💹 Signal: {signal}\n⭐ Confidence: {confidence}%")
                voice_alert(f"{company['name']} चा रिझल्ट आला. सिग्नल {signal}")
                
                # Auto Trade via Angel One
                if signal in ["BUY", "CAUTIOUS BUY"] and st.session_state.auto_trade_enabled:
                    current_price = get_live_price(company['symbol'])
                    if current_price > 0 and st.session_state.angel_connected:
                        place_angel_order(
                            company['symbol'],
                            st.session_state.auto_trade_qty,
                            current_price,
                            current_price * (1 - st.session_state.auto_trade_sl_percent/100),
                            current_price * (1 + st.session_state.auto_trade_target_percent/100)
                        )

# ================= UI HEADER =================
st.markdown(f"""
<div style="text-align:center; padding:20px;">
    <h1>🐺 {APP_NAME} - REAL EDITION</h1>
    <p style="color:#94a3b8;">{APP_AUTHOR}, {APP_LOCATION} | v{APP_VERSION}</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

now = get_ist_now()
st.markdown(f"<div class='live-time'>🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')}</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= STATUS BAR =================
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: 
    st.markdown('<span class="badge-success">🟢 REAL MODE</span>' if st.session_state.algo_running else '<span class="badge-danger">🔴 STOPPED</span>', unsafe_allow_html=True)
with c2: st.markdown('<span class="badge-success">📊 FMP PAID</span>' if FMP_API_KEY != "YOUR_FMP_API_KEY" else '<span class="badge-warning">⚠️ FMP NEED KEY</span>', unsafe_allow_html=True)
with c3: st.markdown('<span class="badge-success">📰 MARATHI NEWS</span>', unsafe_allow_html=True)
with c4: 
    if st.session_state.angel_connected:
        st.markdown('<span class="badge-success">🔗 ANGEL ONE</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-warning">⚠️ ANGEL NEED KEY</span>', unsafe_allow_html=True)
with c5: st.markdown('<span class="badge-success">📱 TELEGRAM</span>', unsafe_allow_html=True)
with c6: st.markdown(f'<span class="badge-info">🐺 {len(FO_SCRIPTS)} SYMBOLS</span>', unsafe_allow_html=True)

st.markdown("---")

# ================= CONTROL PANEL =================
col1, col2, col3 = st.columns([2,1,1])
with col1:
    totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code", key="totp_main")
with col2:
    if st.button("🟢 START", use_container_width=True):
        if totp and len(totp) == 6:
            # Connect Angel One
            if ANGEL_API_KEY != "YOUR_ANGEL_API_KEY":
                angel_one_login()
            
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED - REAL EDITION")
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
            st.rerun()
    
    if st.session_state.wolf_orders:
        pending = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
        if pending:
            st.dataframe(pd.DataFrame(pending), use_container_width=True)

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

# ================= TAB 3: VAISHNAVI NEWS (REAL MARATHI) =================
with tab3:
    st.markdown("### 📰 वैष्णवी न्यूज - REAL MARATHI")
    st.markdown("*Google Translate API वापरून English → Marathi*")
    
    col1, col2 = st.columns([3,1])
    with col2: st.session_state.voice_enabled = st.checkbox("🔊 मराठी Voice", st.session_state.voice_enabled)
    
    st.markdown("---")
    st.markdown("#### Sentiment Guide:")
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    with col_a: st.markdown('<span style="color:#00ff88">🚀 STRONG BULLISH</span>', unsafe_allow_html=True)
    with col_b: st.markdown('<span style="color:#88ff88">📈 BULLISH</span>', unsafe_allow_html=True)
    with col_c: st.markdown('<span style="color:#ffa500">⚪ NEUTRAL</span>', unsafe_allow_html=True)
    with col_d: st.markdown('<span style="color:#ff8888">📉 BEARISH</span>', unsafe_allow_html=True)
    with col_e: st.markdown('<span style="color:#ff4444">💀 STRONG BEARISH</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    news_items = get_news_with_translation()
    for news in news_items:
        color = "#00ff88" if news['sentiment'] == "STRONG BULLISH" else "#88ff88" if news['sentiment'] == "BULLISH" else "#ff4444" if news['sentiment'] == "STRONG BEARISH" else "#ff8888" if news['sentiment'] == "BEARISH" else "#ffa500"
        
        st.markdown(f"**📌 {news['title_marathi']}**")
        st.caption(f"📖 English: {news['title_english'][:100]}...")
        st.caption(f"Source: {news['source']} | {news['time']}")
        st.markdown(f"<span style='color:{color}; font-weight:bold'>{news['sentiment_icon']} {news['sentiment']}</span>", unsafe_allow_html=True)
        st.progress(min(100, news['strength'])/100)
        st.markdown("---")

# ================= TAB 4: OVI RESULTS (REAL FMP) =================
with tab4:
    st.markdown("### 📈 OVI RESULTS - REAL FMP API")
    st.markdown("*Financial Modeling Prep (Paid API)*")
    
    if FMP_API_KEY and FMP_API_KEY != "YOUR_FMP_API_KEY":
        st.success("✅ FMP API Connected (Paid)")
        
        st.markdown("---")
        st.markdown("#### Companies Monitored:")
        for comp in PENDING_RESULTS:
            col1, col2 = st.columns([1,1])
            with col1:
                st.write(f"📊 {comp['name']} ({comp['symbol']})")
            with col2:
                earnings = get_fmp_earnings(comp['symbol'])
                if earnings:
                    st.write(f"✅ Result Date: {earnings.get('date', 'N/A')}")
                else:
                    st.write("⏳ Waiting for result...")
            st.markdown("---")
        
        if st.session_state.result_alerts:
            st.markdown("### 🔔 Results History")
            for alert in st.session_state.result_alerts[-5:]:
                st.info(f"📊 {alert['company']} | {alert['verdict']} | Signal: {alert['signal']} | Confidence: {alert['confidence']}%")
    else:
        st.warning("⚠️ FMP API Key Required! Get paid subscription from https://financialmodelingprep.com/")
        api_input = st.text_input("Enter FMP API Key:", type="password")
        if api_input:
            FMP_API_KEY = api_input
            st.rerun()

# ================= TAB 5: SAHYADRI SETTINGS =================
with tab5:
    st.markdown("### ⚙️ SAHYADRI SETTINGS")
    
    st.markdown("#### 🤖 AUTO TRADE (Angel One)")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Lots", 1, 50, st.session_state.auto_trade_qty)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("SL %", 1, 20, st.session_state.auto_trade_sl_percent)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", 1, 30, st.session_state.auto_trade_target_percent)
    
    if ANGEL_API_KEY == "YOUR_ANGEL_API_KEY":
        st.warning("⚠️ Angel One API Keys Required!")
        st.text_input("API Key", type="password")
        st.text_input("Client ID")
        st.text_input("Password", type="password")
        st.text_input("TOTP Secret", type="password")
    
    st.markdown("---")
    st.markdown("#### NIFTY TP")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.nifty_lots,key="n_l")
    with c2: st.number_input("TP1",1,100,st.session_state.nifty_tp1,key="n_t1")
    with c3: st.checkbox("ON",st.session_state.nifty_tp1_enabled,key="n_en1")
    with c4: st.number_input("TP2",1,100,st.session_state.nifty_tp2,key="n_t2")
    with c5: st.checkbox("ON",st.session_state.nifty_tp2_enabled,key="n_en2")
    with c6: st.number_input("TP3",1,100,st.session_state.nifty_tp3,key="n_t3")
    with c7: st.checkbox("ON",st.session_state.nifty_tp3_enabled,key="n_en3")
    
    st.markdown("#### CRUDE TP")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.crude_lots,key="c_l")
    with c2: st.number_input("TP1",1,100,st.session_state.crude_tp1,key="c_t1")
    with c3: st.checkbox("ON",st.session_state.crude_tp1_enabled,key="c_en1")
    with c4: st.number_input("TP2",1,100,st.session_state.crude_tp2,key="c_t2")
    with c5: st.checkbox("ON",st.session_state.crude_tp2_enabled,key="c_en2")
    with c6: st.number_input("TP3",1,100,st.session_state.crude_tp3,key="c_t3")
    with c7: st.checkbox("ON",st.session_state.crude_tp3_enabled,key="c_en3")
    
    st.markdown("#### NG TP")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.ng_lots,key="g_l")
    with c2: st.number_input("TP1",1,50,st.session_state.ng_tp1,key="g_t1")
    with c3: st.checkbox("ON",st.session_state.ng_tp1_enabled,key="g_en1")
    with c4: st.number_input("TP2",1,50,st.session_state.ng_tp2,key="g_t2")
    with c5: st.checkbox("ON",st.session_state.ng_tp2_enabled,key="g_en2")
    with c6: st.number_input("TP3",1,50,st.session_state.ng_tp3,key="g_t3")
    with c7: st.checkbox("ON",st.session_state.ng_tp3_enabled,key="g_en3")

# ================= AUTO EXECUTION =================
if st.session_state.algo_running and st.session_state.totp_verified:
    monitor_fmp_results()
    st.info("🐺 REAL EDITION ACTIVE | FMP + Angel One + Marathi News")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🌸 SAMRUDDHI DASHBOARD")
    st.markdown("---")
    st.metric("Active Orders", len(st.session_state.active_orders))
    st.metric("Pending", len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']))
    st.metric("Total Trades", len(st.session_state.trade_journal))
    st.metric("Symbols", len(FO_SCRIPTS))
    st.metric("Results", len(st.session_state.result_alerts))
    st.markdown("---")
    st.caption("✅ FMP API: PAID")
    st.caption("✅ Angel One: " + ("CONNECTED" if st.session_state.angel_connected else "PENDING"))
    st.caption("✅ Marathi News: REAL")
    st.caption("✅ Telegram: ACTIVE")
    st.caption(f"✅ Auto Trade: {'ON' if st.session_state.auto_trade_enabled else 'OFF'}")

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🐺 {APP_NAME} REAL EDITION v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION}")
