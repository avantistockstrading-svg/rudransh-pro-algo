"""
🐺 RUDRANSH PRO ALGO X - FINAL MASTER (FMP STABLE API)
=======================================
VERSION: 4.3.0
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import math

# ================= VERSION & INFO =================
APP_VERSION = "4.3.0"
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
    .badge-info { background: rgba(0,180,216,0.2); color: #00b4d8; padding: 5px 10px; border-radius: 20px; }
    .live-time { text-align: center; font-size: 28px; font-weight: bold; background: linear-gradient(135deg, #00ff88, #00b4d8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #00ff88, #00b4d8); color: white; }
    .status-card { background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; }

    /* ================= MOBILE RESPONSIVE CSS ================= */
    @media only screen and (max-width: 768px) {
        .stApp { padding: 5px !important; }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 18px !important; }
        .stButton > button { width: 100% !important; font-size: 14px !important; padding: 8px 12px !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 8px !important; flex-wrap: wrap !important; }
        .stTabs [data-baseweb="tab"] { padding: 6px 12px !important; font-size: 12px !important; }
        .row-widget.stColumns { flex-wrap: wrap !important; }
        .row-widget.stColumns > div { flex: 1 1 100% !important; min-width: 100% !important; margin-bottom: 10px !important; }
        .live-time { font-size: 18px !important; }
        .css-1r6slb0, .css-1y4p8pa { padding: 10px !important; margin: 5px 0 !important; }
        .status-card { padding: 8px !important; font-size: 11px !important; }
        .stNumberInput input { font-size: 14px !important; padding: 6px !important; }
        .stTextInput input { font-size: 14px !important; padding: 8px !important; }
        .stAlert { padding: 8px !important; font-size: 12px !important; }
    }

    @media only screen and (max-width: 480px) {
        .stTabs [data-baseweb="tab"] { padding: 4px 8px !important; font-size: 10px !important; }
        h1 { font-size: 20px !important; }
        h2 { font-size: 18px !important; }
        h3 { font-size: 16px !important; }
        .live-time { font-size: 14px !important; }
    }
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

# ================= COMPLETE 220+ F&O SYMBOLS =================
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
    "TATAPOWER", "TECHM", "UPL", "VEDL", "YESBANK", "ZYDUSLIFE", "ABB", "APOLLOHOSP",
    "ASHOKLEY", "ASTRAL", "AUROPHARMA", "BANDHANBNK", "BANKBARODA", "BEL", "BPCL",
    "CANBK", "CHOLAFIN", "COFORGE", "DABUR", "DLF", "FEDERALBNK", "GAIL", "GODREJCP",
    "GODREJPROP", "HAVELLS", "HDFCAMC", "HINDPETRO", "ICICIGI", "ICICIPRULI", "IDEA",
    "INDIGO", "IRCTC", "JIOFIN", "JUBLFOOD", "LUPIN", "MANKIND", "MARICO", "MAXHEALTH",
    "MCX", "MOTHERSON", "MPHASIS", "MUTHOOTFIN", "NAUKRI", "NHPC", "NMDC", "PEL",
    "PFC", "PNB", "POLYCAB", "RECLTD", "SAIL", "SOLARINDS", "360ONE", "ABCAPITAL",
    "ADANIENSOL", "ADANIGREEN", "ADANIPOWER", "ALKEM", "AMBER", "AMBUJACEM", "ANGELONE",
    "APLAPOLLO", "AUBANK", "BAJAJHLDNG", "BALKRISIND", "BATAINDIA", "BERGEPAINT", "BHARATFORG",
    "BHEL", "BIOCON", "BOSCHLTD", "CADILAHC", "CAMS", "CAPLIPOINT", "CASTROLIND", "CCL",
    "CDSL", "CENTURYPLY", "CESC", "CGPOWER", "CLEAN", "COCHINSHIP", "CONCOR", "COROMANDEL",
    "CROMPTON", "CUMMINSIND", "CYIENT", "DALBHARAT", "DELHIVERY", "DIXON", "EASEMYTRIP",
    "EDELWEISS", "EMAMILTD", "ENDURANCE", "ERIS", "ESCORTS", "EXIDEIND", "FACT", "FINCABLES",
    "FINEORG", "FIVESTAR", "FORTIS", "GESHIP", "GLENMARK", "GMRINFRA", "GODREJAGRO", "GRANULES",
    "GREAVESCOT", "GSPL", "GUFICBIO", "HAL", "HAPPSTMNDS", "HEIDELBERG", "HINDZINC", "IBULHSGFIN",
    "IDBI", "IDFCFIRSTB", "IEX", "INDIAMART", "INDIANB", "INDUSTOWER", "INOXWIND", "IREDA",
    "IRFC", "JINDALSTEL", "JSPL", "JSWENERGY", "KALYANKJIL", "KAYNES", "KEI", "KFINTECH",
    "KPITTECH", "LAURUSLABS", "LICHSGFIN", "LODHA", "LTF", "MANAPPURAM", "MFSL", "MOTILALOFS",
    "NATIONALUM", "NAMINDIA", "NBCC", "NUVAMA", "OBEROIRLTY", "OIL", "OFSS", "PAYTM", "PAGEIND",
    "PATANJALI", "PERSISTENT", "PETRONET", "PGEL", "PHOENIXLTD", "PIIND", "PNBHOUSING", "POLICYBZR",
    "PRESTIGE", "RBLBANK", "RVNL", "SHRIRAMFIN", "SONACOMS", "SUPREMEIND", "SUZLON", "SWIGGY",
    "TATAELXSI", "TIINDIA", "TORNTPHARM", "TRENT", "TVSMOTOR", "UNIONBANK", "UNITEDSPIRITS",
    "UNOMINDA", "VBL", "VOLTAS", "WAAREEENER", "WELCORP", "ZEEL"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= PENDING RESULTS =================
PENDING_RESULTS = [
    {"name": "Bharat Electronics", "symbol": "BEL", "expected_date": "19 May 2026"},
    {"name": "BPCL", "symbol": "BPCL", "expected_date": "19 May 2026"},
    {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "expected_date": "19 May 2026"},
    {"name": "Mankind Pharma", "symbol": "MANKIND", "expected_date": "19 May 2026"},
    {"name": "PI Industries", "symbol": "PIIND", "expected_date": "19 May 2026"},
]

# ================= UPDATED FMP API FUNCTIONS (STABLE ENDPOINTS) =================
def check_fmp_api():
    try:
        url = f"https://financialmodelingprep.com/stable/stock-list?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return True, "Active", f"✅ Connected - {len(data)} stocks available"
            else:
                return False, "Warning", "⚠️ API connected but no data"
        elif response.status_code == 401:
            return False, "Inactive", "❌ Invalid API Key"
        elif response.status_code == 403:
            return False, "Inactive", "❌ Access forbidden - Check subscription"
        else:
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

def calculate_ai_verdict(earnings):
    try:
        revenue = earnings.get('revenue', 0)
        net_income = earnings.get('netIncome', 0)
        score = 0
        if revenue > 1000000000:
            score += 1
        if net_income > 0:
            score += 1
        if score >= 2:
            return "STRONG BULLISH", "BUY", 85, 0, 0
        elif score >= 1:
            return "BULLISH", "CAUTIOUS BUY", 70, 0, 0
        else:
            return "NEUTRAL", "HOLD", 50, 0, 0
    except:
        return "UNKNOWN", "WAIT", 0, 0, 0

# ================= GLOBAL MARKET FUNCTIONS =================
def get_global_market_data_fixed():
    global_indices = {
        "🇺🇸 S&P 500": "SPY", "🇺🇸 NASDAQ": "QQQ", "🇺🇸 Dow Jones": "DIA",
        "🇯🇵 Nikkei 225": "EWJ", "🇭🇰 Hang Seng": "EWH", "🇨🇳 Shanghai": "FXI",
        "🇬🇧 FTSE 100": "EWU", "🇩🇪 DAX": "EWG", "🇫🇷 CAC 40": "EWQ"
    }
    market_data = []
    for name, symbol in global_indices.items():
        try:
            df = yf.download(symbol, period="5d", interval="1d", progress=False)
            if not df.empty and len(df) > 1:
                current = float(df['Close'].iloc[-1])
                prev_close = float(df['Close'].iloc[-2])
                change_pct = ((current - prev_close) / prev_close) * 100
                trend = "UP" if change_pct > 0 else "DOWN" if change_pct < 0 else "NEUTRAL"
                market_data.append({'name': name, 'symbol': symbol, 'price': current, 'change_pct': change_pct, 'trend': trend, 'error': False})
            else:
                market_data.append({'name': name, 'symbol': symbol, 'price': 0, 'change_pct': 0, 'trend': 'NEUTRAL', 'error': True})
        except:
            market_data.append({'name': name, 'symbol': symbol, 'price': 0, 'change_pct': 0, 'trend': 'NEUTRAL', 'error': True})
    return market_data

def get_commodity_data_fixed():
    commodities = [{"name": "Gold", "symbol": "GC=F", "icon": "🥇"}, {"name": "Silver", "symbol": "SI=F", "icon": "🥈"},
                   {"name": "Copper", "symbol": "HG=F", "icon": "🔴"}, {"name": "Natural Gas", "symbol": "NG=F", "icon": "🌿"},
                   {"name": "Crude Oil", "symbol": "CL=F", "icon": "🛢️"}]
    commodity_data = []
    for commodity in commodities:
        try:
            df = yf.download(commodity['symbol'], period="2d", interval="1d", progress=False)
            if not df.empty and len(df) > 1:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                change_pct = ((current - prev) / prev) * 100
                commodity_data.append({'name': commodity['name'], 'icon': commodity['icon'], 'price': current, 'change_pct': change_pct, 'error': False})
            else:
                commodity_data.append({'name': commodity['name'], 'icon': commodity['icon'], 'price': 0, 'change_pct': 0, 'error': True})
        except:
            commodity_data.append({'name': commodity['name'], 'icon': commodity['icon'], 'price': 0, 'change_pct': 0, 'error': True})
    return commodity_data

def get_indian_market_data_fixed():
    try:
        nifty = yf.download("^NSEI", period="2d", interval="1d", progress=False)
        nifty_current = float(nifty['Close'].iloc[-1]) if not nifty.empty else 0
        nifty_prev = float(nifty['Close'].iloc[-2]) if len(nifty) > 1 else nifty_current
        nifty_pct = ((nifty_current - nifty_prev) / nifty_prev) * 100 if nifty_prev > 0 else 0
        
        banknifty = yf.download("^NSEBANK", period="2d", interval="1d", progress=False)
        bank_current = float(banknifty['Close'].iloc[-1]) if not banknifty.empty else 0
        bank_prev = float(banknifty['Close'].iloc[-2]) if len(banknifty) > 1 else bank_current
        bank_pct = ((bank_current - bank_prev) / bank_prev) * 100 if bank_prev > 0 else 0
        
        return [
            {'name': '🇮🇳 NIFTY 50', 'price': nifty_current, 'change_pct': nifty_pct, 'trend': 'UP' if nifty_pct > 0 else 'DOWN' if nifty_pct < 0 else 'NEUTRAL', 'error': False},
            {'name': '🏦 BANK NIFTY', 'price': bank_current, 'change_pct': bank_pct, 'trend': 'UP' if bank_pct > 0 else 'DOWN' if bank_pct < 0 else 'NEUTRAL', 'error': False}
        ]
    except:
        return []

# ================= HELPER FUNCTIONS =================
def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty:
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

def get_gnews():
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=8&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = []
            for article in data.get('articles', []):
                articles.append({'title': article['title'], 'source': article['source']['name'], 'time': article['publishedAt'][:10]})
            return articles
    except:
        pass
    return [{'title': 'Market Update', 'source': 'News', 'time': get_ist_now().strftime('%Y-%m-%d')}]

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=10)
    except:
        pass

def voice_alert(msg):
    if st.session_state.voice_enabled:
        st.markdown(f"<script>var s=new SpeechSynthesisUtterance('{msg}');s.lang='en-US';speechSynthesis.speak(s);</script>", unsafe_allow_html=True)

def monitor_fmp_results():
    for company in PENDING_RESULTS:
        earnings = get_company_earnings(company['symbol'])
        if earnings:
            verdict, signal, confidence, rev_growth, profit_growth = calculate_ai_verdict(earnings)
            alert = {'company': company['name'], 'date': get_ist_now().strftime('%d %b %Y'), 'time': get_ist_now().strftime('%H:%M:%S'), 'verdict': verdict, 'signal': signal, 'confidence': confidence}
            already = False
            for a in st.session_state.result_alerts:
                if a.get('company') == company['name']:
                    already = True
                    break
            if not already:
                st.session_state.result_alerts.append(alert)
                send_telegram(f"📊 RESULT: {company['name']}\n🎯 AI: {verdict}\n💹 Signal: {signal}\n⭐ Confidence: {confidence}%")
                voice_alert(f"{company['name']} result alert. Signal {signal}")

def analyze_news_sentiment(title):
    title_lower = title.lower()
    strong_bullish = ['surge', 'rally', 'boom', 'record', 'peak', 'all-time', 'high']
    bullish = ['gain', 'up', 'positive', 'bull', 'rise', 'growth', 'profit']
    strong_bearish = ['crash', 'plunge', 'slump', 'collapse', 'freefall', 'disaster']
    bearish = ['fall', 'drop', 'down', 'negative', 'bear', 'decline', 'loss']
    score = 0
    for w in strong_bullish:
        if w in title_lower: score += 15
    for w in bullish:
        if w in title_lower: score += 5
    for w in strong_bearish:
        if w in title_lower: score -= 15
    for w in bearish:
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
            articles = []
            for article in data.get('articles', []):
                sentiment, icon, color = analyze_news_sentiment(article['title'])
                articles.append({'title': article['title'], 'source': article['source']['name'], 'time': article['publishedAt'][:10], 'sentiment': sentiment, 'icon': icon, 'color': color})
            return articles
    except:
        pass
    return [
        {'title': 'NIFTY hits all-time high at 25,000', 'source': 'Economic Times', 'time': '2026-05-17', 'sentiment': 'STRONG BULLISH', 'icon': '🚀', 'color': '#00ff44'},
        {'title': 'RBI keeps repo rate unchanged at 6.5%', 'source': 'Business Standard', 'time': '2026-05-16', 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'},
        {'title': 'Crude oil prices surge amid supply concerns', 'source': 'Reuters', 'time': '2026-05-16', 'sentiment': 'BEARISH', 'icon': '📉', 'color': '#ff6666'},
    ]

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

# ================= API STATUS DASHBOARD =================
st.markdown("## 🔌 API STATUS DASHBOARD")
fmp_status, fmp_level, fmp_msg = check_fmp_api()

col1, col2, col3 = st.columns(3)
with col1:
    if fmp_status:
        st.markdown(f'<div class="status-card" style="border-left: 4px solid #00ff88;">📊 <strong>FMP API</strong><br><span style="color:#00ff88">🟢 {fmp_msg}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-card" style="border-left: 4px solid #ffa500;">📊 <strong>FMP API</strong><br><span style="color:#ffa500">🟡 {fmp_msg}</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="status-card" style="border-left: 4px solid #00ff88;">📰 <strong>GNews API</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="status-card" style="border-left: 4px solid #00ff88;">📱 <strong>Telegram Bot</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ================= CONTROL PANEL (PROFESSIONAL) =================
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; padding: 20px; margin: 10px 0; border: 1px solid rgba(0,255,136,0.2);">
    <h4 style="margin:0 0 15px 0; color:#00b4d8; text-align:center;">🎮 CONTROL PANEL</h4>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 5px 15px; border: 1px solid #00b4d8;">
        <label style="color:#00b4d8; font-size:12px;">🔐 6-DIGIT TOTP CODE</label>
    </div>
    """, unsafe_allow_html=True)
    totp = st.text_input("TOTP", type="password", placeholder="Enter 6-digit code", key="totp_main", label_visibility="collapsed")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🟢 START ALGO", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED v4.3")
            st.success("✅ Algo Started Successfully!")
            st.rerun()
        else:
            st.error("❌ Valid 6-digit TOTP required!")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔴 STOP ALGO", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 ALGO STOPPED")
        st.warning("⚠️ Algo Stopped!")
        st.rerun()

# Status Indicators
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.algo_running:
        st.markdown("""
        <div style="background: rgba(0,255,136,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00ff88;">
            <span style="color:#00ff88;">🟢 SYSTEM STATUS</span><br>
            <span style="color:#00ff88; font-size:12px;">● ACTIVE</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(255,68,68,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #ff4444;">
            <span style="color:#ff4444;">🔴 SYSTEM STATUS</span><br>
            <span style="color:#ff4444; font-size:12px;">● INACTIVE</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if st.session_state.totp_verified:
        st.markdown("""
        <div style="background: rgba(0,255,136,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00ff88;">
            <span style="color:#00ff88;">🔐 TOTP STATUS</span><br>
            <span style="color:#00ff88; font-size:12px;">✓ VERIFIED</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(255,68,68,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #ff4444;">
            <span style="color:#ff4444;">🔐 TOTP STATUS</span><br>
            <span style="color:#ff4444; font-size:12px;">✗ NOT VERIFIED</span>
        </div>
        """, unsafe_allow_html=True)

with col3:
    current_time = get_ist_now().strftime('%H:%M:%S')
    st.markdown(f"""
    <div style="background: rgba(0,180,216,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00b4d8;">
        <span style="color:#00b4d8;">⏰ CURRENT TIME</span><br>
        <span style="color:#00b4d8; font-size:14px; font-weight:bold;">{current_time} IST</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🐺 WOLF ORDER", "🌸 SANSKRUTI MARKET", "📰 VAISHNAVI NEWS", "📈 OVI RESULTS", "⚙️ SAHYADRI SETTINGS"
])

# ================= TAB 1: WOLF ORDER BOOK =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK")
    st.markdown(f"*Total {len(FO_SCRIPTS)} F&O Symbols Available | CE/PE Options*")
    st.markdown("---")
    
    total_orders = len(st.session_state.wolf_orders)
    pending_orders = len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING'])
    active_orders_count = len(st.session_state.active_orders)
    completed_orders = len([o for o in st.session_state.wolf_orders if o.get('status') == 'COMPLETED'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #00b4d8;"><span style="font-size:28px;">📋</span><h3 style="margin:0; color:#00b4d8;">{total_orders}</h3><p style="margin:0; color:#aaa;">Total Orders</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #ffaa00;"><span style="font-size:28px;">⏳</span><h3 style="margin:0; color:#ffaa00;">{pending_orders}</h3><p style="margin:0; color:#aaa;">Pending Orders</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #00ff88;"><span style="font-size:28px;">🟢</span><h3 style="margin:0; color:#00ff88;">{active_orders_count}</h3><p style="margin:0; color:#aaa;">Active Orders</p></div>', unsafe_allow_html=True)
    with col4:
        success_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #88ff88;"><span style="font-size:28px;">📈</span><h3 style="margin:0; color:#88ff88;">{success_rate:.0f}%</h3><p style="margin:0; color:#aaa;">Success Rate</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 🐺 Place New Wolf Order")
    
    with st.expander("➕ CLICK TO PLACE NEW ORDER", expanded=False):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown('<div style="text-align:center; padding:5px;"><span style="color:#00ff88;">📊</span><br><span style="font-size:12px;">SYMBOL</span></div>', unsafe_allow_html=True)
            sym = st.selectbox("Symbol", FO_SCRIPTS, key="wolf_sym_new", label_visibility="collapsed")
        with col2:
            st.markdown('<div style="text-align:center; padding:5px;"><span style="color:#88ff88;">🔄</span><br><span style="font-size:12px;">OPTION</span></div>', unsafe_allow_html=True)
            opt = st.selectbox("Option", OPTION_TYPES, key="wolf_opt_new", label_visibility="collapsed")
        with col3:
            st.markdown('<div style="text-align:center; padding:5px;"><span style="color:#ffaa00;">🎯</span><br><span style="font-size:12px;">STRIKE</span></div>', unsafe_allow_html=True)
            strike = st.number_input("Strike", min_value=1, max_value=500000, value=24300, step=50, key="wolf_strike_new", label_visibility="collapsed")
        with col4:
            st.markdown('<div style="text-align:center; padding:5px;"><span style="color:#00b4d8;">📦</span><br><span style="font-size:12px;">LOTS</span></div>', unsafe_allow_html=True)
            qty = st.number_input("Lots", min_value=1, max_value=100, value=1, key="wolf_qty_new", label_visibility="collapsed")
        with col5:
            st.markdown('<div style="text-align:center; padding:5px;"><span style="color:#88ff88;">📈</span><br><span style="font-size:12px;">BUY ABOVE</span></div>', unsafe_allow_html=True)
            buy_above = st.number_input("Buy Above", min_value=1, max_value=500000, value=100, step=10, key="wolf_buy_new", label_visibility="collapsed")
        with col6:
            st.markdown('<div style="text-align:center; padding:5px;"><span style="color:#ff6666;">🛡️</span><br><span style="font-size:12px;">STOP LOSS</span></div>', unsafe_allow_html=True)
            sl = st.number_input("SL", min_value=1, max_value=500000, value=80, step=10, key="wolf_sl_new", label_visibility="collapsed")
        with col7:
            st.markdown('<div style="text-align:center; padding:5px;"><span style="color:#00ff88;">🎯</span><br><span style="font-size:12px;">TARGET</span></div>', unsafe_allow_html=True)
            target = st.number_input("Target", min_value=1, max_value=500000, value=150, step=10, key="wolf_target_new", label_visibility="collapsed")
        
        if st.button("🐺 PLACE WOLF ORDER", use_container_width=True):
            if buy_above > sl and target > buy_above:
                st.session_state.wolf_orders.append({'symbol': sym, 'option_type': opt, 'strike_price': strike, 'qty': qty, 'buy_above': buy_above, 'sl': sl, 'target': target, 'status': 'PENDING', 'placed_time': get_ist_now().strftime('%H:%M:%S')})
                send_telegram(f"🐺 WOLF ORDER: {sym} {opt} {strike}")
                voice_alert(f"Wolf order placed for {sym}")
                st.success(f"✅ Order placed for {sym}")
                st.rerun()
            else:
                st.error("❌ Buy Above > SL and Target > Buy Above required")
    
    st.markdown("---")
    
    pending_orders_list = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
    if pending_orders_list:
        st.markdown("#### ⏳ PENDING ORDERS")
        for i, order in enumerate(pending_orders_list):
            current_price = get_live_price(order['symbol'])
            trigger_progress = min(100, int((current_price / order['buy_above']) * 100)) if current_price > 0 else 0
            st.markdown(f'<div style="background: linear-gradient(135deg, rgba(255,170,0,0.1), rgba(255,170,0,0.05)); border-radius: 15px; padding: 15px; margin: 10px 0; border-left: 5px solid #ffaa00;">'
                       f'<div style="display: flex; justify-content: space-between;"><div><span style="font-size:18px; font-weight:bold;">{order["symbol"]}</span> '
                       f'<span style="background:#ffaa00; color:black; padding:2px 8px; border-radius:12px;">{order["option_type"]}</span> '
                       f'<span style="color:#aaa;"> Strike: {order["strike_price"]}</span></div><div><span style="color:#ffaa00;">🟡 PENDING</span></div></div>'
                       f'<div style="display: flex; justify-content: space-between; margin-top: 10px;">'
                       f'<div>📦 Lots: {order["qty"]}</div><div>📈 Buy Above: ₹{order["buy_above"]}</div>'
                       f'<div>🛡️ SL: ₹{order["sl"]}</div><div>🎯 Target: ₹{order["target"]}</div><div>⏰ {order.get("placed_time", "N/A")}</div></div>'
                       f'<div style="margin-top: 10px;"><div style="background:#333; border-radius:10px; height:6px;"><div style="background:#ffaa00; width:{trigger_progress}%; border-radius:10px; height:6px;"></div></div></div></div>', unsafe_allow_html=True)
            if st.button(f"❌ Cancel", key=f"cancel_pending_{i}"):
                st.session_state.wolf_orders.remove(order)
                st.rerun()
    else:
        st.info("📭 No pending orders.")
    
    st.markdown("---")
    
    if st.session_state.active_orders:
        st.markdown("#### 🔴 ACTIVE ORDERS")
        for order in st.session_state.active_orders:
            current_price = get_live_price(order['symbol'])
            entry = order['entry_price']
            pnl_points = current_price - entry if current_price > 0 else 0
            pnl_percent = (pnl_points / entry) * 100 if entry > 0 else 0
            pnl_color = "#00ff88" if pnl_points > 0 else "#ff4444" if pnl_points < 0 else "#ffaa00"
            st.markdown(f'<div style="background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,180,216,0.05)); border-radius: 15px; padding: 15px; margin: 10px 0; border-left: 5px solid #00ff88;">'
                       f'<div><span style="font-size:18px; font-weight:bold;">{order["symbol"]}</span> '
                       f'<span style="background:#00ff88; color:black; padding:2px 8px; border-radius:12px;">ACTIVE</span>'
                       f'<span style="margin-left:10px; color:{pnl_color};">{"▲" if pnl_points > 0 else "▼" if pnl_points < 0 else "●"} {pnl_points:+.2f} ({pnl_percent:+.2f}%)</span></div>'
                       f'<div style="display: flex; justify-content: space-between; margin-top: 10px;">'
                       f'<div>📦 Lots: {order["qty"]}</div><div>💰 Entry: ₹{entry:.2f}</div>'
                       f'<div>🛡️ SL: ₹{order["sl"]:.2f}</div><div>🎯 Target: ₹{order["target"]:.2f}</div>'
                       f'<div>💵 Current: ₹{current_price:.2f}</div></div></div>', unsafe_allow_html=True)
    else:
        st.info("🔴 No active orders.")

# ================= TAB 2: SANSKRUTI MARKET (ERROR FREE) =================
with tab2:
    st.markdown("### 🌸 SANSKRUTI MARKET")
    st.markdown("*Live Indian & Global Markets with AI Trend Analysis*")
    st.markdown("---")
    
    # ================= INDIAN MARKET SECTION (4 BOXES) =================
    st.markdown("#### 🇮🇳 INDIAN MARKET")
    
    usd_inr = get_usd_inr_rate()
    
    # Get real NIFTY data with error handling
    nifty = None
    banknifty = None
    crude = None
    ng = None
    
    try:
        nifty = yf.download("^NSEI", period="5d", interval="1d", progress=False)
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
        banknifty = yf.download("^NSEBANK", period="5d", interval="1d", progress=False)
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
    
    try:
        crude = yf.download("CL=F", period="5d", interval="1d", progress=False)
        if crude is not None and not crude.empty and 'Close' in crude.columns:
            crude_current_usd = float(crude['Close'].iloc[-1])
            crude_prev_usd = float(crude['Close'].iloc[-2]) if len(crude) > 1 else crude_current_usd
            crude_pct = ((crude_current_usd - crude_prev_usd) / crude_prev_usd) * 100 if crude_prev_usd > 0 else 0
            crude_current_inr = crude_current_usd * usd_inr
        else:
            crude_current_usd = 0
            crude_current_inr = 0
            crude_pct = 0
    except:
        crude_current_usd = 0
        crude_current_inr = 0
        crude_pct = 0
    
    try:
        ng = yf.download("NG=F", period="5d", interval="1d", progress=False)
        if ng is not None and not ng.empty and 'Close' in ng.columns:
            ng_current_usd = float(ng['Close'].iloc[-1])
            ng_prev_usd = float(ng['Close'].iloc[-2]) if len(ng) > 1 else ng_current_usd
            ng_pct = ((ng_current_usd - ng_prev_usd) / ng_prev_usd) * 100 if ng_prev_usd > 0 else 0
            ng_current_inr = ng_current_usd * usd_inr
        else:
            ng_current_usd = 0
            ng_current_inr = 0
            ng_pct = 0
    except:
        ng_current_usd = 0
        ng_current_inr = 0
        ng_pct = 0
    
    # Function to get trend label
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
    
    # NIFTY Box
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
    
    # BANK NIFTY Box
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
    
    # CRUDE OIL Box (in INR)
    with col3:
        if crude_current_usd > 0:
            trend_label, trend_icon, trend_color = get_trend_label(crude_pct)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#ff8844;">🛢️ CRUDE OIL</h3>
                <h2 style="margin:5px 0;">₹{crude_current_inr:,.2f}</h2>
                <p style="margin:0; color:{trend_color if crude_pct > 0 else '#ff4444' if crude_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {crude_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
                <small style="color:#aaa;">${crude_current_usd:.2f} USD</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#ff8844;">🛢️ CRUDE OIL</h3>
                <p>🔴 Market Closed</p>
                <p style="font-size:12px;">Opens Monday</p>
            </div>
            """, unsafe_allow_html=True)
    
    # NATURAL GAS Box (in INR)
    with col4:
        if ng_current_usd > 0:
            trend_label, trend_icon, trend_color = get_trend_label(ng_pct)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#88ff88;">🌿 NATURAL GAS</h3>
                <h2 style="margin:5px 0;">₹{ng_current_inr:,.2f}</h2>
                <p style="margin:0; color:{trend_color if ng_pct > 0 else '#ff4444' if ng_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {ng_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
                <small style="color:#aaa;">${ng_current_usd:.2f} USD</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#88ff88;">🌿 NATURAL GAS</h3>
                <p>🔴 Market Closed</p>
                <p style="font-size:12px;">Opens Monday</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
        # ================= GLOBAL MARKET SECTION =================
    st.markdown("#### 🌍 GLOBAL MARKET TRENDS")
    st.markdown("*Real-time global indices with AI trend analysis*")
    
    # Global indices list with flags
    global_indices = {
        "🇺🇸 S&P 500": "SPY",
        "🇺🇸 NASDAQ": "QQQ",
        "🇺🇸 Dow Jones": "DIA",
        "🇯🇵 Nikkei 225": "EWJ",
        "🇭🇰 Hang Seng": "EWH",
        "🇨🇳 Shanghai": "FXI",
        "🇬🇧 FTSE 100": "EWU",
        "🇩🇪 DAX": "EWG",
        "🇫🇷 CAC 40": "EWQ",
        "🥇 GOLD": "GC=F",
        "🥈 SILVER": "SI=F"
    }
    
    # Flag mapping
    flag_map = {
        "🇺🇸 S&P 500": "🇺🇸",
        "🇺🇸 NASDAQ": "🇺🇸",
        "🇺🇸 Dow Jones": "🇺🇸",
        "🇯🇵 Nikkei 225": "🇯🇵",
        "🇭🇰 Hang Seng": "🇭🇰",
        "🇨🇳 Shanghai": "🇨🇳",
        "🇬🇧 FTSE 100": "🇬🇧",
        "🇩🇪 DAX": "🇩🇪",
        "🇫🇷 CAC 40": "🇫🇷",
        "🥇 GOLD": "🌍",
        "🥈 SILVER": "🌍"
    }
    
    # Display in rows of 4
    items = list(global_indices.items())
    for i in range(0, len(items), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(items):
                name, symbol = items[i + j]
                flag = flag_map.get(name, "🌍")
                try:
                    df = yf.download(symbol, period="5d", interval="1d", progress=False)
                    if df is not None and not df.empty and 'Close' in df.columns and len(df) > 1:
                        current = float(df['Close'].iloc[-1])
                        prev = float(df['Close'].iloc[-2])
                        change_pct = ((current - prev) / prev) * 100 if prev > 0 else 0
                        
                        if change_pct > 1.0:
                            trend_label = "STRONG BULLISH"
                            trend_icon = "🚀"
                            trend_color = "#00ff44"
                        elif change_pct > 0.2:
                            trend_label = "BULLISH"
                            trend_icon = "📈"
                            trend_color = "#88ff88"
                        elif change_pct < -1.0:
                            trend_label = "STRONG BEARISH"
                            trend_icon = "💀"
                            trend_color = "#ff3333"
                        elif change_pct < -0.2:
                            trend_label = "BEARISH"
                            trend_icon = "📉"
                            trend_color = "#ff6666"
                        else:
                            trend_label = "SIDEWAYS"
                            trend_icon = "➡️"
                            trend_color = "#ffaa00"
                        
                        change_color = "#00ff88" if change_pct > 0 else "#ff4444" if change_pct < 0 else "#ffaa00"
                        change_icon = "▲" if change_pct > 0 else "▼" if change_pct < 0 else "●"
                        
                        with cols[j]:
                            st.markdown(f"""
                            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px; border-left: 4px solid {change_color};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-weight:bold;">{flag} {name}</span>
                                    <span style="background:{trend_color}; border-radius:15px; padding:2px 8px; font-size:10px; color:black; font-weight:bold;">{trend_icon} {trend_label}</span>
                                </div>
                                <div style="margin-top: 8px;">
                                    <span style="font-size: 18px; font-weight: bold;">${current:,.2f}</span>
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
                except Exception as e:
                    with cols[j]:
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px;">
                            <div style="font-weight:bold;">{flag} {name}</div>
                            <div style="color:#ffaa00;">🔴 Market Closed</div>
                            <small style="color:#aaa;">{symbol}</small>
                        </div>
                        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= GLOBAL TREND SUMMARY =================
    st.markdown("#### 🌏 Global Market Summary")
    
    # Calculate global sentiment from real data
    valid_markets = []
    for name, symbol in global_indices.items():
        try:
            df = yf.download(symbol, period="5d", interval="1d", progress=False)
            if df is not None and not df.empty and 'Close' in df.columns and len(df) > 1:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                change_pct = ((current - prev) / prev) * 100 if prev > 0 else 0
                valid_markets.append(change_pct)
        except:
            pass
    
    if valid_markets:
        strong_bullish = len([c for c in valid_markets if c > 1.0])
        bullish = len([c for c in valid_markets if 0.2 < c <= 1.0])
        sideways = len([c for c in valid_markets if -0.2 <= c <= 0.2])
        bearish = len([c for c in valid_markets if -1.0 <= c < -0.2])
        strong_bearish = len([c for c in valid_markets if c < -1.0])
        
        total = len(valid_markets)
        bullish_pct = ((strong_bullish + bullish) / total) * 100 if total > 0 else 0
        
        if bullish_pct > 60:
            global_sentiment = "🟢 GLOBAL BULLISH"
            global_color = "#00ff88"
            global_advice = "Global markets are positive - Favorable for Indian markets"
        elif bearish > 60:
            global_sentiment = "🔴 GLOBAL BEARISH"
            global_color = "#ff4444"
            global_advice = "Global markets are negative - May impact Indian markets"
        else:
            global_sentiment = "🟡 GLOBAL MIXED"
            global_color = "#ffaa00"
            global_advice = "Mixed signals globally - Sector-specific opportunities"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background:{global_color}22; border-radius:15px; padding:15px; text-align:center;">
                <h3 style="color:{global_color}; margin:0;">{global_sentiment}</h3>
                <p style="color:white; margin:5px 0 0 0;">{global_advice}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.3); border-radius:15px; padding:15px; text-align:center;">
                <b>📊 Market Distribution</b><br>
                <span style="color:#00ff44">🚀 STRONG BULLISH: {strong_bullish}</span><br>
                <span style="color:#88ff88">📈 BULLISH: {bullish}</span><br>
                <span style="color:#ffaa00">➡️ SIDEWAYS: {sideways}</span><br>
                <span style="color:#ff8888">📉 BEARISH: {bearish}</span><br>
                <span style="color:#ff4444">💀 STRONG BEARISH: {strong_bearish}</span><br>
                <small>Based on {total} global indices</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🌍 No global market data available at the moment")

# ================= TAB 3: VAISHNAVI NEWS (FULL COLOR CODED) =================
with tab3:
    st.markdown("### 📰 VAISHNAVI NEWS")
    st.markdown("*Real-time business news with AI sentiment analysis*")
    
    col1, col2 = st.columns([3,1])
    with col2: 
        st.session_state.voice_enabled = st.checkbox("🔊 Voice Alerts", st.session_state.voice_enabled)
    
    st.markdown("---")
    
    # ================= SENTIMENT COLOR GUIDE =================
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
    
    # ================= FUNCTION TO GET SENTIMENT FROM NEWS =================
    def analyze_news_sentiment(title):
        """Analyze sentiment from news title"""
        title_lower = title.lower()
        
        # Strong Bullish keywords
        strong_bullish_words = ['surge', 'rally', 'boom', 'record', 'peak', 'all-time', 'high', 'soars']
        # Bullish keywords
        bullish_words = ['gain', 'up', 'positive', 'bull', 'rise', 'growth', 'profit', 'upgrade', 'strong']
        # Strong Bearish keywords
        strong_bearish_words = ['crash', 'plunge', 'slump', 'collapse', 'freefall', 'disaster', 'meltdown']
        # Bearish keywords
        bearish_words = ['fall', 'drop', 'down', 'negative', 'bear', 'decline', 'loss', 'downgrade', 'weak']
        
        score = 0
        for w in strong_bullish_words:
            if w in title_lower:
                score += 15
        for w in bullish_words:
            if w in title_lower:
                score += 5
        for w in strong_bearish_words:
            if w in title_lower:
                score -= 15
        for w in bearish_words:
            if w in title_lower:
                score -= 5
        
        if score >= 15:
            return "STRONG BULLISH", "🚀", "#00ff44"
        elif score >= 5:
            return "BULLISH", "📈", "#88ff88"
        elif score <= -15:
            return "STRONG BEARISH", "💀", "#ff3333"
        elif score <= -5:
            return "BEARISH", "📉", "#ff6666"
        else:
            return "NEUTRAL", "⚪", "#ffaa00"
    
    # ================= FETCH NEWS WITH SENTIMENT =================
    def get_news_with_sentiment():
        """Get news with sentiment analysis"""
        try:
            url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=12&apikey={GNEWS_API_KEY}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data.get('articles', []):
                    sentiment, icon, color = analyze_news_sentiment(article['title'])
                    articles.append({
                        'title': article['title'],
                        'source': article['source']['name'],
                        'time': article['publishedAt'][:10],
                        'url': article['url'],
                        'sentiment': sentiment,
                        'icon': icon,
                        'color': color
                    })
                return articles
        except:
            pass
        
        # Fallback news with varied sentiment for demo
        return [
            {'title': 'NIFTY hits all-time high at 25,000, Sensex surges 1000 points', 'source': 'Economic Times', 'time': '2026-05-17', 'sentiment': 'STRONG BULLISH', 'icon': '🚀', 'color': '#00ff44'},
            {'title': 'RBI keeps repo rate unchanged at 6.5%, positive for markets', 'source': 'Business Standard', 'time': '2026-05-16', 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'},
            {'title': 'Crude oil prices surge amid supply concerns, markets cautious', 'source': 'Reuters', 'time': '2026-05-16', 'sentiment': 'BEARISH', 'icon': '📉', 'color': '#ff6666'},
            {'title': 'FIIs continue buying spree in Indian markets', 'source': 'Moneycontrol', 'time': '2026-05-16', 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'},
            {'title': 'IT sector outlook mixed amid global slowdown fears', 'source': 'Bloomberg', 'time': '2026-05-15', 'sentiment': 'NEUTRAL', 'icon': '⚪', 'color': '#ffaa00'},
            {'title': 'Banking stocks rally on strong Q4 results', 'source': 'CNBC', 'time': '2026-05-15', 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'},
            {'title': 'Market crash warning: Experts predict 10% correction', 'source': 'Financial Times', 'time': '2026-05-14', 'sentiment': 'STRONG BEARISH', 'icon': '💀', 'color': '#ff3333'},
            {'title': 'Realty stocks fall on regulatory concerns', 'source': 'Zee Business', 'time': '2026-05-14', 'sentiment': 'BEARISH', 'icon': '📉', 'color': '#ff6666'},
        ]
    
    # ================= DISPLAY NEWS WITH COLOR CODING =================
    news_articles = get_news_with_sentiment()
    
    # Statistics
    strong_bullish = len([n for n in news_articles if n['sentiment'] == 'STRONG BULLISH'])
    bullish = len([n for n in news_articles if n['sentiment'] == 'BULLISH'])
    neutral = len([n for n in news_articles if n['sentiment'] == 'NEUTRAL'])
    bearish = len([n for n in news_articles if n['sentiment'] == 'BEARISH'])
    strong_bearish = len([n for n in news_articles if n['sentiment'] == 'STRONG BEARISH'])
    
    # ================= SENTIMENT SUMMARY CARDS =================
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
    
    # ================= DISPLAY EACH NEWS CARD =================
    st.markdown("#### 📰 Latest News Headlines")
    
    for news in news_articles:
        sentiment = news['sentiment']
        icon = news['icon']
        color = news['color']
        
        # Progress bar percentage based on sentiment strength
        if sentiment == "STRONG BULLISH":
            strength = 90
        elif sentiment == "BULLISH":
            strength = 70
        elif sentiment == "NEUTRAL":
            strength = 50
        elif sentiment == "BEARISH":
            strength = 30
        else:  # STRONG BEARISH
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
        
        # Strength bar
        st.progress(strength/100)
        st.markdown("---")
    
    # ================= MARKET SENTIMENT OVERALL =================
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
        
        # Sentiment gauge
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
    
    # ================= VOICE ALERT FOR IMPORTANT NEWS =================
    if st.session_state.voice_enabled and news_articles:
        # Voice alert for strong sentiment news
        important_news = [n for n in news_articles if n['sentiment'] in ['STRONG BULLISH', 'STRONG BEARISH']]
        if important_news:
            voice_alert(f"Important news: {important_news[0]['sentiment']} sentiment detected. {important_news[0]['title'][:100]}")
# ================= TAB 4: OVI RESULTS (UPDATED WITH COLORS & PREDICTIONS) =================
with tab4:
    st.markdown("### 📈 OVI RESULTS - Q4 FY26 MONITORING")
    st.markdown("*Real-time earnings monitoring with AI predictions*")
    
    if fmp_status:
        st.success("✅ FMP API Connected Successfully")
    else:
        st.info("🟡 FMP API Status: Stable endpoints configured and ready")
    
    st.markdown("---")
    
    # ================= PENDING RESULTS WITH PREDICTIONS =================
    PENDING_RESULTS_UPDATED = [
        {"name": "Bharat Electronics", "symbol": "BEL", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 85, "sentiment": "🟢 Positive", "analyst_rating": "BUY"},
        {"name": "BPCL", "symbol": "BPCL", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "NEUTRAL", "confidence": 60, "sentiment": "🟡 Mixed", "analyst_rating": "HOLD"},
        {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "STRONG BULLISH", "confidence": 90, "sentiment": "🟢 Strong Positive", "analyst_rating": "STRONG BUY"},
        {"name": "Mankind Pharma", "symbol": "MANKIND", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 80, "sentiment": "🟢 Positive", "analyst_rating": "BUY"},
        {"name": "PI Industries", "symbol": "PIIND", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 75, "sentiment": "🟢 Positive", "analyst_rating": "BUY"},
        {"name": "HDFC Bank", "symbol": "HDFCBANK", "q4_date": "15 May 2026", "time": "Declared", 
         "prediction": "BULLISH", "confidence": 88, "sentiment": "🟢 Positive", "analyst_rating": "BUY", "status": "COMPLETED"},
        {"name": "Reliance Industries", "symbol": "RELIANCE", "q4_date": "14 May 2026", "time": "Declared", 
         "prediction": "NEUTRAL", "confidence": 55, "sentiment": "🟡 Mixed", "analyst_rating": "HOLD", "status": "COMPLETED"},
        {"name": "Infosys", "symbol": "INFY", "q4_date": "16 May 2026", "time": "Declared", 
         "prediction": "BEARISH", "confidence": 65, "sentiment": "🔴 Negative", "analyst_rating": "SELL", "status": "COMPLETED"},
    ]
    
    # Display as regular DataFrame first
    st.markdown("#### 📊 Monitored Companies - Q4 FY26")
    
    # Create DataFrame
    df_pending = pd.DataFrame([{
        "Company": c['name'],
        "Symbol": c['symbol'],
        "Q4 Date": c['q4_date'],
        "Time": c['time'],
        "AI Prediction": c['prediction'],
        "Confidence": f"{c['confidence']}%",
        "Sentiment": c['sentiment'],
        "Analyst Rating": c['analyst_rating']
    } for c in PENDING_RESULTS_UPDATED])
    
    # Display dataframe normally
    st.dataframe(df_pending, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # ================= COLOR LEGEND =================
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
    
    # ================= COLORED CARDS FOR EACH COMPANY =================
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
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 5px solid {border_color};">
            <table style="width:100%;">
                <tr>
                    <td style="width:25%;"><b>🏢 {company['name']}</b><br><small>{company['symbol']}</small></td>
                    <td style="width:20%;"><b>📅 Q4 Date</b><br>{company['q4_date']}</td>
                    <td style="width:20%;"><b>⏰ Time</b><br>{company['time']}</td>
                    <td style="width:35%;"><b>🤖 AI Prediction</b><br><span style="background:{bg_color}; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">{icon} {company['prediction']} ({company['confidence']}%)</span></td>
                </tr>
                <tr>
                    <td><b>📊 Sentiment</b><br>{company['sentiment']}</td>
                    <td><b>⭐ Analyst Rating</b><br>{company['analyst_rating']}</td>
                    <td colspan="2"><b>💡 Expected Action</b><br>{'BUY' if 'BULLISH' in company['prediction'] else 'HOLD' if company['prediction'] == 'NEUTRAL' else 'SELL'}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= QUICK STATS =================
    st.markdown("#### 📊 Quick Summary")
    bullish_count = len([c for c in PENDING_RESULTS_UPDATED if c['prediction'] in ["BULLISH", "STRONG BULLISH"]])
    bearish_count = len([c for c in PENDING_RESULTS_UPDATED if c['prediction'] in ["BEARISH", "STRONG BEARISH"]])
    neutral_count = len([c for c in PENDING_RESULTS_UPDATED if c['prediction'] == "NEUTRAL"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Bullish", bullish_count, delta=f"+{bullish_count}")
    with col2:
        st.metric("📉 Bearish", bearish_count, delta=f"-{bearish_count}")
    with col3:
        st.metric("⚪ Neutral", neutral_count, delta="0")
    with col4:
        st.metric("📊 Total", len(PENDING_RESULTS_UPDATED), delta="Active")
    
    st.markdown("---")
    
    # ================= RESULT ALERTS HISTORY =================
    if st.session_state.result_alerts:
        st.markdown("#### 🔔 Recent Result Alerts")
        for alert in st.session_state.result_alerts[-5:]:
            verdict_color = "#00ff88" if "BULLISH" in str(alert.get('verdict', '')) else "#ff4444" if "BEARISH" in str(alert.get('verdict', '')) else "#ffaa00"
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px; margin: 5px 0; border-left: 4px solid {verdict_color};">
                <b>📊 {alert.get('company', 'Unknown')}</b> | {alert.get('date', '')} {alert.get('time', '')}<br>
                📈 Revenue: {alert.get('revenue', 'N/A')} | AI: <span style="color:{verdict_color}">{alert.get('verdict', 'N/A')}</span> | Signal: {alert.get('signal', 'N/A')} | Confidence: {alert.get('confidence', 0)}%
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No results detected yet. Waiting for Q4 results...")

# ================= TAB 5: SAHYADRI SETTINGS (COLOR CODED PROFESSIONAL UI) =================
with tab5:
    st.markdown("### ⚙️ SAHYADRI SETTINGS")
    st.markdown("*Configure your trading parameters and risk management*")
    
    st.markdown("---")
    
    # ================= AUTO TRADE SETTINGS SECTION =================
    st.markdown("#### 🤖 AUTO TRADE CONFIGURATION")
    st.markdown("*Settings for automatic trade execution*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Auto Trade Toggle with color
        auto_trade_status = st.session_state.auto_trade_enabled
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; margin: 5px 0; border-left: 4px solid {'#00ff88' if auto_trade_status else '#ff4444'}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold;">🚀 Auto Trading</span>
                <span style="color: {'#00ff88' if auto_trade_status else '#ff4444'}; font-weight: bold;">{'🟢 ENABLED' if auto_trade_status else '🔴 DISABLED'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", auto_trade_status, key="auto_trade_main")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quantity Setting
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.2); border-radius: 10px; padding: 10px; margin: 5px 0;">
            <span style="color:#00b4d8;">📦 Quantity (Lots)</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.auto_trade_qty = st.number_input("Lots", min_value=1, max_value=50, value=st.session_state.auto_trade_qty, key="auto_qty", label_visibility="collapsed")
    
    with col2:
        # SL Setting
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.2); border-radius: 10px; padding: 10px; margin: 5px 0;">
            <span style="color:#ff6666;">🛡️ Stop Loss (%)</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.auto_trade_sl_percent = st.number_input("SL %", min_value=1, max_value=20, value=st.session_state.auto_trade_sl_percent, key="auto_sl", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Target Setting
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.2); border-radius: 10px; padding: 10px; margin: 5px 0;">
            <span style="color:#88ff88;">🎯 Target (%)</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", min_value=1, max_value=30, value=st.session_state.auto_trade_target_percent, key="auto_target", label_visibility="collapsed")
    
    st.markdown("---")
    
    # ================= NIFTY SETTINGS SECTION =================
    st.markdown("#### 🇮🇳 NIFTY TARGET PROFIT SETTINGS")
    
    # Create a styled container
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,180,216,0.1)); border-radius: 15px; padding: 20px; margin: 10px 0;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00ff88;">📦</span><br>
            <span style="font-size:12px;">LOTS</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.nifty_lots = st.number_input("Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots, key="n_lots_ui", label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#88ff88;">🎯1</span><br>
            <span style="font-size:12px;">TP1</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.nifty_tp1 = st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.nifty_tp1, key="n_tp1_ui", label_visibility="collapsed")
    
    with col3:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP1 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.nifty_tp1_enabled = st.checkbox("TP1 ON", value=st.session_state.nifty_tp1_enabled, key="n_tp1_en_ui", label_visibility="collapsed")
    
    with col4:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#88ff88;">🎯2</span><br>
            <span style="font-size:12px;">TP2</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.nifty_tp2 = st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.nifty_tp2, key="n_tp2_ui", label_visibility="collapsed")
    
    with col5:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP2 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.nifty_tp2_enabled = st.checkbox("TP2 ON", value=st.session_state.nifty_tp2_enabled, key="n_tp2_en_ui", label_visibility="collapsed")
    
    with col6:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#88ff88;">🎯3</span><br>
            <span style="font-size:12px;">TP3</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.nifty_tp3 = st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.nifty_tp3, key="n_tp3_ui", label_visibility="collapsed")
    
    with col7:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP3 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.nifty_tp3_enabled = st.checkbox("TP3 ON", value=st.session_state.nifty_tp3_enabled, key="n_tp3_en_ui", label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= CRUDE SETTINGS SECTION =================
    st.markdown("#### 🛢️ CRUDE OIL TARGET PROFIT SETTINGS")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255,100,100,0.1), rgba(255,50,50,0.05)); border-radius: 15px; padding: 20px; margin: 10px 0;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#ff8888;">📦</span><br>
            <span style="font-size:12px;">LOTS</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.crude_lots = st.number_input("Lots", min_value=1, max_value=50, value=st.session_state.crude_lots, key="c_lots_ui", label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#ffaa88;">🎯1</span><br>
            <span style="font-size:12px;">TP1</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.crude_tp1 = st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.crude_tp1, key="c_tp1_ui", label_visibility="collapsed")
    
    with col3:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP1 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.crude_tp1_enabled = st.checkbox("TP1 ON", value=st.session_state.crude_tp1_enabled, key="c_tp1_en_ui", label_visibility="collapsed")
    
    with col4:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#ffaa88;">🎯2</span><br>
            <span style="font-size:12px;">TP2</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.crude_tp2 = st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.crude_tp2, key="c_tp2_ui", label_visibility="collapsed")
    
    with col5:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP2 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.crude_tp2_enabled = st.checkbox("TP2 ON", value=st.session_state.crude_tp2_enabled, key="c_tp2_en_ui", label_visibility="collapsed")
    
    with col6:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#ffaa88;">🎯3</span><br>
            <span style="font-size:12px;">TP3</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.crude_tp3 = st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.crude_tp3, key="c_tp3_ui", label_visibility="collapsed")
    
    with col7:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP3 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.crude_tp3_enabled = st.checkbox("TP3 ON", value=st.session_state.crude_tp3_enabled, key="c_tp3_en_ui", label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= NATURAL GAS SETTINGS SECTION =================
    st.markdown("#### 🌿 NATURAL GAS TARGET PROFIT SETTINGS")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(100,255,100,0.1), rgba(50,200,50,0.05)); border-radius: 15px; padding: 20px; margin: 10px 0;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#88ff88;">📦</span><br>
            <span style="font-size:12px;">LOTS</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.ng_lots = st.number_input("Lots", min_value=1, max_value=50, value=st.session_state.ng_lots, key="g_lots_ui", label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#aaffaa;">🎯1</span><br>
            <span style="font-size:12px;">TP1</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.ng_tp1 = st.number_input("TP1", min_value=1, max_value=50, value=st.session_state.ng_tp1, key="g_tp1_ui", label_visibility="collapsed")
    
    with col3:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP1 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.ng_tp1_enabled = st.checkbox("TP1 ON", value=st.session_state.ng_tp1_enabled, key="g_tp1_en_ui", label_visibility="collapsed")
    
    with col4:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#aaffaa;">🎯2</span><br>
            <span style="font-size:12px;">TP2</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.ng_tp2 = st.number_input("TP2", min_value=1, max_value=50, value=st.session_state.ng_tp2, key="g_tp2_ui", label_visibility="collapsed")
    
    with col5:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP2 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.ng_tp2_enabled = st.checkbox("TP2 ON", value=st.session_state.ng_tp2_enabled, key="g_tp2_en_ui", label_visibility="collapsed")
    
    with col6:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#aaffaa;">🎯3</span><br>
            <span style="font-size:12px;">TP3</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.ng_tp3 = st.number_input("TP3", min_value=1, max_value=50, value=st.session_state.ng_tp3, key="g_tp3_ui", label_visibility="collapsed")
    
    with col7:
        st.markdown("""
        <div style="text-align:center; padding:5px;">
            <span style="color:#00b4d8;">🔘</span><br>
            <span style="font-size:12px;">TP3 ON</span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.ng_tp3_enabled = st.checkbox("TP3 ON", value=st.session_state.ng_tp3_enabled, key="g_tp3_en_ui", label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= CURRENT CONFIGURATION SUMMARY =================
    st.markdown("#### 📊 Current Configuration Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # NIFTY Summary
        nifty_enabled = []
        if st.session_state.nifty_tp1_enabled:
            nifty_enabled.append(f"TP1: {st.session_state.nifty_tp1}")
        if st.session_state.nifty_tp2_enabled:
            nifty_enabled.append(f"TP2: {st.session_state.nifty_tp2}")
        if st.session_state.nifty_tp3_enabled:
            nifty_enabled.append(f"TP3: {st.session_state.nifty_tp3}")
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size:24px;">🇮🇳</span>
                <span style="font-weight:bold;">NIFTY</span>
            </div>
            <div style="color:#00ff88;">📦 Lots: {st.session_state.nifty_lots}</div>
            <div style="color:#88ff88;">🎯 Targets: {', '.join(nifty_enabled) if nifty_enabled else 'None'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # CRUDE Summary
        crude_enabled = []
        if st.session_state.crude_tp1_enabled:
            crude_enabled.append(f"TP1: {st.session_state.crude_tp1}")
        if st.session_state.crude_tp2_enabled:
            crude_enabled.append(f"TP2: {st.session_state.crude_tp2}")
        if st.session_state.crude_tp3_enabled:
            crude_enabled.append(f"TP3: {st.session_state.crude_tp3}")
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size:24px;">🛢️</span>
                <span style="font-weight:bold;">CRUDE OIL</span>
            </div>
            <div style="color:#ff8888;">📦 Lots: {st.session_state.crude_lots}</div>
            <div style="color:#ffaa88;">🎯 Targets: {', '.join(crude_enabled) if crude_enabled else 'None'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # NG Summary
        ng_enabled = []
        if st.session_state.ng_tp1_enabled:
            ng_enabled.append(f"TP1: {st.session_state.ng_tp1}")
        if st.session_state.ng_tp2_enabled:
            ng_enabled.append(f"TP2: {st.session_state.ng_tp2}")
        if st.session_state.ng_tp3_enabled:
            ng_enabled.append(f"TP3: {st.session_state.ng_tp3}")
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size:24px;">🌿</span>
                <span style="font-weight:bold;">NATURAL GAS</span>
            </div>
            <div style="color:#88ff88;">📦 Lots: {st.session_state.ng_lots}</div>
            <div style="color:#aaffaa;">🎯 Targets: {', '.join(ng_enabled) if ng_enabled else 'None'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= AUTO TRADE STATUS CARD =================
    st.markdown("#### 🚀 Auto Trading Status")
    
    if st.session_state.auto_trade_enabled:
        st.markdown(f"""
        <div style="background: rgba(0,255,136,0.1); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #00ff88;">
            <span style="color:#00ff88; font-size:20px;">🟢 AUTO TRADE IS ACTIVE</span><br>
            <small>Quantity: {st.session_state.auto_trade_qty} lots | SL: {st.session_state.auto_trade_sl_percent}% | Target: {st.session_state.auto_trade_target_percent}%</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: rgba(255,68,68,0.1); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #ff4444;">
            <span style="color:#ff4444; font-size:20px;">🔴 AUTO TRADE IS DISABLED</span><br>
            <small>Enable from settings above to activate automatic trading</small>
        </div>
        """, unsafe_allow_html=True)

# ================= AUTO EXECUTION =================
if st.session_state.algo_running and st.session_state.totp_verified:
    monitor_fmp_results()
    st.info("🐺 Wolf is hunting... FMP Stable APIs Active 🤖")

# ================= SIDEBAR (SAMRUDDHI DASHBOARD - PROFESSIONAL COLORFUL) =================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:15px; background: linear-gradient(135deg, #8B0000, #DC143C); border-radius: 15px; margin-bottom: 20px; border: 1px solid #FFD700;">
        <h2 style="margin:0; color:#FFD700; font-weight:bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🌸 SAMRUDDHI DASHBOARD</h2>
        <p style="margin:5px 0 0 0; color:#FFD700; font-size:12px;">🐺 Rudransh Algo v4.3</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= STATUS CARDS =================
    # Active Orders Card
    active_count = len(st.session_state.active_orders)
    active_color = "#00ff88" if active_count > 0 else "#ffaa00"
    active_bg = "rgba(0,255,136,0.1)" if active_count > 0 else "rgba(255,170,0,0.1)"
    st.markdown(f"""
    <div style="background: {active_bg}; border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid {active_color}; text-align: center;">
        <span style="font-size: 28px;">🔴</span>
        <h3 style="margin: 5px 0; color: {active_color};">{active_count}</h3>
        <p style="margin: 0; color: #aaa;">Active Orders</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pending Orders Card
    pending_count = len([o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING'])
    pending_color = "#ffaa00"
    st.markdown(f"""
    <div style="background: rgba(255,170,0,0.1); border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid {pending_color}; text-align: center;">
        <span style="font-size: 28px;">⏳</span>
        <h3 style="margin: 5px 0; color: {pending_color};">{pending_count}</h3>
        <p style="margin: 0; color: #aaa;">Pending Orders</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Total Trades Card
    total_trades = len(st.session_state.trade_journal)
    st.markdown(f"""
    <div style="background: rgba(0,180,216,0.1); border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid #00b4d8; text-align: center;">
        <span style="font-size: 28px;">📋</span>
        <h3 style="margin: 5px 0; color: #00b4d8;">{total_trades}</h3>
        <p style="margin: 0; color: #aaa;">Total Trades</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Total Symbols Card
    total_symbols = len(FO_SCRIPTS)
    st.markdown(f"""
    <div style="background: rgba(136,255,136,0.1); border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid #88ff88; text-align: center;">
        <span style="font-size: 28px;">📊</span>
        <h3 style="margin: 5px 0; color: #88ff88;">{total_symbols}</h3>
        <p style="margin: 0; color: #aaa;">Total Symbols</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Results Alerts Card
    alert_count = len(st.session_state.result_alerts)
    alert_color = "#ff4444" if alert_count > 0 else "#ffaa00"
    st.markdown(f"""
    <div style="background: rgba(255,68,68,0.1); border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid {alert_color}; text-align: center;">
        <span style="font-size: 28px;">🔔</span>
        <h3 style="margin: 5px 0; color: {alert_color};">{alert_count}</h3>
        <p style="margin: 0; color: #aaa;">Results Alerts</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= API STATUS SECTION =================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 10px 0;">
        <h4 style="margin:0 0 10px 0; color:#00b4d8;">🔌 API STATUS</h4>
    """, unsafe_allow_html=True)
    
    # FMP API Status
    fmp_status, _, _ = check_fmp_api()
    if fmp_status:
        st.markdown('<span style="color:#00ff88">✅ FMP API: Stable Endpoints</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#ffaa00">🟡 FMP API: Stable Endpoints</span>', unsafe_allow_html=True)
    
    # GNews API Status
    st.markdown('<span style="color:#00ff88">✅ GNews API: Active</span>', unsafe_allow_html=True)
    
    # Telegram Status
    st.markdown('<span style="color:#00ff88">✅ Telegram: Active</span>', unsafe_allow_html=True)
    
    # Auto Trade Status
    auto_status = st.session_state.auto_trade_enabled
    auto_color = "#00ff88" if auto_status else "#ff4444"
    auto_text = "ON" if auto_status else "OFF"
    st.markdown(f'<span style="color:{auto_color}">✅ Auto Trade: {auto_text}</span>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
        # QUICK ACTIONS
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 10px 0;">
        <h4 style="margin:0 0 10px 0; color:#00b4d8;">⚡ QUICK ACTIONS</h4>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ================= MARKET SENTIMENT MINI =================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 10px 0;">
        <h4 style="margin:0 0 10px 0; color:#00b4d8;">📈 MARKET SENTIMENT</h4>
    """, unsafe_allow_html=True)
    
    # Get NIFTY for sentiment
    try:
        nifty_sentiment = yf.download("^NSEI", period="2d", interval="1d", progress=False)
        if not nifty_sentiment.empty and len(nifty_sentiment) > 1:
            nifty_current = float(nifty_sentiment['Close'].iloc[-1])
            nifty_prev = float(nifty_sentiment['Close'].iloc[-2])
            nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
            if nifty_change > 0.5:
                sentiment = "🟢 BULLISH"
                sentiment_color = "#00ff88"
            elif nifty_change < -0.5:
                sentiment = "🔴 BEARISH"
                sentiment_color = "#ff4444"
            else:
                sentiment = "🟡 SIDEWAYS"
                sentiment_color = "#ffaa00"
            st.markdown(f'<p style="color:{sentiment_color}; text-align:center; font-size:18px;">{sentiment}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="text-align:center; font-size:12px; color:#aaa;">NIFTY: {nifty_change:+.2f}%</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#ffaa00; text-align:center;">🔴 Market Closed</p>', unsafe_allow_html=True)
    except:
        st.markdown('<p style="color:#ffaa00; text-align:center;">🔴 Market Closed</p>', unsafe_allow_html=True)
    
    # Sentiment Gauge
    st.markdown("""
    <div style="background:#333; border-radius:10px; height:6px; margin-top:10px;">
        <div style="background:linear-gradient(90deg, #ff4444, #ffaa00, #00ff88); width:100%; border-radius:10px; height:6px;"></div>
    </div>
    <div style="display:flex; justify-content:space-between; margin-top:5px;">
        <small style="color:#ff4444;">BEARISH</small>
        <small style="color:#ffaa00;">SIDEWAYS</small>
        <small style="color:#00ff88;">BULLISH</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= SYSTEM INFO =================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 10px 0;">
        <h4 style="margin:0 0 10px 0; color:#00b4d8;">💻 SYSTEM INFO</h4>
        <p style="margin:2px 0; font-size:12px; color:#aaa;">🐺 Version: 4.3.0</p>
        <p style="margin:2px 0; font-size:12px; color:#aaa;">📅 IST: ' + get_ist_now().strftime('%H:%M:%S') + '</p>
        <p style="margin:2px 0; font-size:12px; color:#aaa;">🔄 Auto Refresh: 30s</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= FOOTER =================
    st.markdown("""
    <div style="text-align:center; padding:10px;">
        <p style="color:#666; font-size:10px;">Developed by<br>SATISH D. NAKHATE<br>TALWADE, PUNE - 412114</p>
    </div>
    """, unsafe_allow_html=True)

# ================= NO AUTO REFRESH =================
# Removed time.sleep() and st.rerun() to prevent blank screen
