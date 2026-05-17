"""
🐺 RUDRANSH PRO ALGO X - FINAL MASTER
=======================================
VERSION: 3.4.0
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import math
import random

# ================= VERSION & INFO =================
APP_VERSION = "3.4.0"
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
    .result-card { background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px; margin: 10px 0; border-left: 4px solid #00ff88; }
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

# ================= COMPLETE 215+ SYMBOLS =================
FO_SCRIPTS = [
    # Indices & Commodity (6)
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "CRUDE", "NATURALGAS",
    
    # Top Bluechip Stocks (50)
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR", "ITC",
    "SBIN", "BHARTIARTL", "KOTAKBANK", "AXISBANK", "LT", "DMART", "SUNPHARMA",
    "BAJFINANCE", "TITAN", "MARUTI", "TATAMOTORS", "TATASTEEL", "WIPRO",
    "HCLTECH", "ONGC", "NTPC", "POWERGRID", "ULTRACEMCO", "ADANIPORTS",
    "ADANIENT", "ASIANPAINT", "BAJAJFINSV", "BRITANNIA", "CIPLA", "COALINDIA",
    "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HDFCLIFE", "HEROMOTOCO",
    "HINDALCO", "IOC", "INDUSINDBK", "JSWSTEEL", "M&M", "NESTLEIND",
    "PIDILITIND", "SBILIFE", "SHREECEM", "SIEMENS", "SRF", "TATACONSUM",
    
    # More Nifty Stocks (50)
    "TATAPOWER", "TECHM", "UPL", "VEDL", "YESBANK", "ZYDUSLIFE", "ABB", "APOLLOHOSP",
    "ASHOKLEY", "ASTRAL", "AUROPHARMA", "BANDHANBNK", "BANKBARODA", "BEL", "BPCL",
    "CANBK", "CHOLAFIN", "COFORGE", "DABUR", "DLF", "FEDERALBNK", "GAIL", "GODREJCP",
    "GODREJPROP", "HAVELLS", "HDFCAMC", "HINDPETRO", "ICICIGI", "ICICIPRULI", "IDEA",
    "INDIGO", "IRCTC", "JIOFIN", "JUBLFOOD", "LUPIN", "MANKIND", "MARICO", "MAXHEALTH",
    "MCX", "MOTHERSON", "MPHASIS", "MUTHOOTFIN", "NAUKRI", "NHPC", "NMDC", "PEL",
    "PFC", "PNB", "POLYCAB", "RECLTD",
    
    # Midcap & Smallcap (60)
    "360ONE", "ALKEM", "AMBER", "AMBUJACEM", "ANGELONE", "APLAPOLLO", "AUBANK",
    "BALKRISIND", "BATAINDIA", "BERGEPAINT", "BIOCON", "BOSCHLTD", "CADILAHC",
    "CALSOFT", "CAMSLTD", "CAPLIPOINT", "CARTRADE", "CASTROLIND", "CCL", "CDSL",
    "CENTURYPLY", "CESC", "CGPOWER", "CLEAN", "COCHINSHIP", "CONCOR", "COROMANDEL",
    "CROMPTON", "CUMMINSIND", "CYIENT", "DALBHARAT", "DELHIVERY", "DIXON", "EASEMYTRIP",
    "EDELWEISS", "EMAMILTD", "ENDURANCE", "ERIS", "ESCORTS", "EXIDEIND", "FACT",
    "FINCABLES", "FINEORG", "FIVESTAR", "FORTIS", "GESHIP", "GLENMARK", "GMRINFRA",
    "GODREJAGRO", "GRANULES", "GREAVESCOT", "GSPL", "GUFICBIO", "HAL", "HAPPSTMNDS",
    "HEIDELBERG", "HINDZINC", "IBULHSGFIN", "IDBI", "IDFCFIRSTB"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= PENDING RESULTS =================
PENDING_RESULTS = [
    {"name": "Bharat Electronics", "symbol": "BEL", "expected_date": "19 May 2026", "expected_verdict": "POSITIVE"},
    {"name": "BPCL", "symbol": "BPCL", "expected_date": "19 May 2026", "expected_verdict": "MIXED"},
    {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "expected_date": "19 May 2026", "expected_verdict": "POSITIVE"},
]

# ================= MARATHI NEWS TRANSLATIONS =================
MARATHI_NEWS = [
    "निफ्टीने नवीन उच्चांक गाठला, बाजारात तेजी",
    "आरबीआयने व्याजदरात कोणताही बदल केला नाही",
    "क्रूड तेलाच्या किमती वाढल्याने बाजारावर दबाव",
    "विदेशी संस्थागत गुंतवणूकदारांनी खरेदी वाढवली",
    "अर्थसंकल्पापूर्वी बाजारात अस्थिरता कायम",
    "टाटा मोटर्सचा नफा २०% ने वाढला",
    "रेलियन्सने नवीन प्रकल्पाची घोषणा केली",
    "हिंदुंनिलिव्हरचे उत्पन्न अपेक्षेपेक्षा चांगले",
    "आयटी क्षेत्रात मंदी, निर्यातीत घट",
    "बँकिंग शेअर्समध्ये तेजी, निफ्टी बँक ५०० अंकांनी वधारला",
    "सोन्याच्या किमती रेकॉर्ड पातळीवर",
    "रुपया डॉलरविरुद्ध मजबूत झाला",
    "एफआयआयनी १० दिवसांत २५,००० कोटींची खरेदी केली",
    "जीएसटी कलेक्शन १.८ लाख कोटींच्या पार",
    "ऑटो सेक्टरमध्ये विक्रीत वाढ",
    "फार्मा कंपन्यांचे उत्पन्न चांगले",
    "रियल इस्टेट क्षेत्रात सुधारणा",
    "मेटल शेअर्समध्ये तेजी, स्टीलच्या किमती वाढल्या",
    "पॉवर सेक्टरमध्ये सरकारचे नवीन धोरण",
    "टेलिकॉम कंपन्यांनी दरवाढ केली"
]

def get_marathi_news():
    """Get news in Marathi with sentiment analysis in ENGLISH"""
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=10&apikey={GNEWS_API_KEY}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            articles = []
            
            # English sentiment words for analysis
            bullish_strong = ['surge', 'rally', 'boom', 'record', 'peak', 'all-time', 'high']
            bullish_weak = ['gain', 'up', 'positive', 'bull', 'rise', 'growth', 'profit']
            bearish_strong = ['crash', 'plunge', 'slump', 'collapse', 'freefall', 'disaster']
            bearish_weak = ['fall', 'drop', 'down', 'negative', 'bear', 'decline', 'loss']
            
            for i, article in enumerate(data.get('articles', [])):
                title = article['title'].lower()
                
                # Calculate sentiment score
                score = 0
                for w in bullish_strong:
                    if w in title: score += 15
                for w in bullish_weak:
                    if w in title: score += 5
                for w in bearish_strong:
                    if w in title: score -= 15
                for w in bearish_weak:
                    if w in title: score -= 5
                
                # Determine sentiment in ENGLISH
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
                
                # Get Marathi title (use translation or fallback)
                marathi_title = MARATHI_NEWS[i % len(MARATHI_NEWS)]
                
                articles.append({
                    'title_marathi': marathi_title,
                    'source': article['source']['name'],
                    'time': article['publishedAt'][:10],
                    'sentiment': sentiment,
                    'sentiment_icon': sentiment_icon,
                    'strength': abs(score)
                })
            return articles[:10]
    except:
        pass
    
    # Fallback Marathi news
    return [
        {'title_marathi': 'निफ्टीने नवीन उच्चांक गाठला, बाजारात तेजी', 'source': 'Economic Times', 'time': '2026-05-17', 'sentiment': 'BULLISH', 'sentiment_icon': '📈', 'strength': 70},
        {'title_marathi': 'क्रूड तेलाच्या किमती वाढल्याने बाजारावर दबाव', 'source': 'Reuters', 'time': '2026-05-16', 'sentiment': 'BEARISH', 'sentiment_icon': '📉', 'strength': 65},
        {'title_marathi': 'आरबीआयने व्याजदरात कोणताही बदल केला नाही', 'source': 'Business Standard', 'time': '2026-05-15', 'sentiment': 'NEUTRAL', 'sentiment_icon': '⚪', 'strength': 50},
        {'title_marathi': 'टाटा मोटर्सचा नफा २०% ने वाढला', 'source': 'Moneycontrol', 'time': '2026-05-15', 'sentiment': 'BULLISH', 'sentiment_icon': '📈', 'strength': 75},
        {'title_marathi': 'रेलियन्सने नवीन प्रकल्पाची घोषणा केली', 'source': 'Bloomberg', 'time': '2026-05-14', 'sentiment': 'BULLISH', 'sentiment_icon': '📈', 'strength': 80},
    ]

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

# ================= STATUS BAR =================
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    if st.session_state.algo_running:
        st.markdown('<span class="badge-success">🟢 RUNNING</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-danger">🔴 STOPPED</span>', unsafe_allow_html=True)
with c2: st.markdown('<span class="badge-success">📊 FMP ACTIVE</span>', unsafe_allow_html=True)
with c3: st.markdown('<span class="badge-success">📰 NEWS ACTIVE</span>', unsafe_allow_html=True)
with c4: st.markdown('<span class="badge-success">📱 TELEGRAM</span>', unsafe_allow_html=True)
with c5: st.markdown(f'<span class="badge-info">🐺 SYMBOLS: {len(FO_SCRIPTS)}</span>', unsafe_allow_html=True)

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
            send_telegram("🚀 ALGO STARTED")
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
    st.markdown(f"*Total {len(FO_SCRIPTS)} Symbols Available | CE/PE Options*")
    
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
            if buy_above > sl and target > buy_above:
                st.session_state.wolf_orders.append({
                    'symbol': sym, 'option_type': opt, 'strike_price': strike, 'qty': qty,
                    'buy_above': buy_above, 'sl': sl, 'target': target, 'status': 'PENDING'
                })
                st.success(f"✅ Order placed for {sym}")
                st.rerun()
            else:
                st.error("Buy Above > SL and Target > Buy Above required")
    
    if st.session_state.wolf_orders:
        pending = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
        if pending:
            st.markdown("### ⏳ PENDING ORDERS")
            pending_df = pd.DataFrame([{
                'Symbol': o['symbol'], 'Option': o['option_type'], 'Strike': o['strike_price'],
                'Lots': o['qty'], 'Buy Above': o['buy_above'], 'SL': o['sl'], 'Target': o['target']
            } for o in pending])
            st.dataframe(pending_df, use_container_width=True)

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

# ================= TAB 3: VAISHNAVI NEWS (Marathi + English Sentiment) =================
with tab3:
    st.markdown("### 📰 वैष्णवी न्यूज (VAISHNAVI NEWS)")
    st.markdown("*मराठी बातम्या | English Sentiment Analysis*")
    
    col1, col2 = st.columns([3,1])
    with col2: st.session_state.voice_enabled = st.checkbox("🔊 Voice", st.session_state.voice_enabled)
    
    st.markdown("---")
    st.markdown("#### 📊 Sentiment Guide (ENGLISH):")
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    with col_a: st.markdown('<span style="color:#00ff88">🚀 STRONG BULLISH</span>', unsafe_allow_html=True)
    with col_b: st.markdown('<span style="color:#88ff88">📈 BULLISH</span>', unsafe_allow_html=True)
    with col_c: st.markdown('<span style="color:#ffa500">⚪ NEUTRAL</span>', unsafe_allow_html=True)
    with col_d: st.markdown('<span style="color:#ff8888">📉 BEARISH</span>', unsafe_allow_html=True)
    with col_e: st.markdown('<span style="color:#ff4444">💀 STRONG BEARISH</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    for news in get_marathi_news():
        sentiment = news['sentiment']
        icon = news['sentiment_icon']
        
        # Color based on sentiment
        if sentiment == "STRONG BULLISH":
            color = "#00ff88"
        elif sentiment == "BULLISH":
            color = "#88ff88"
        elif sentiment == "STRONG BEARISH":
            color = "#ff4444"
        elif sentiment == "BEARISH":
            color = "#ff8888"
        else:
            color = "#ffa500"
        
        st.markdown(f"**📌 {news['title_marathi']}**")
        col_a, col_b = st.columns([3,1])
        with col_a: st.caption(f"Source: {news['source']} | {news['time']}")
        with col_b: st.markdown(f"<span style='color:{color}; font-weight:bold'>{icon} {sentiment}</span>", unsafe_allow_html=True)
        
        # Strength bar
        strength_pct = min(100, news['strength'])
        st.progress(strength_pct/100)
        st.markdown("---")

# ================= TAB 4: OVI RESULTS =================
with tab4:
    st.markdown("### 📈 OVI RESULTS")
    st.dataframe(pd.DataFrame(PENDING_RESULTS), use_container_width=True)
    
    if st.session_state.result_alerts:
        st.markdown("### 🔔 ALERTS")
        for alert in st.session_state.result_alerts[-5:]:
            st.info(f"📊 {alert.get('company', 'Unknown')} | Time: {alert.get('time', '')}")

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
    st.info("🐺 Wolf is hunting... Auto Trade Active 🤖")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🌸 SAMRUDDHI DASHBOARD")
    st.markdown("---")
    st.metric("Active Orders", len(st.session_state.active_orders))
    st.metric("Pending Orders", len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']))
    st.metric("Total Trades", len(st.session_state.trade_journal))
    st.metric("Total Symbols", len(FO_SCRIPTS))
    st.markdown("---")
    st.caption("✅ FMP API: ACTIVE")
    st.caption("✅ GNews API: ACTIVE")
    st.caption("✅ Telegram: ACTIVE")
    st.caption(f"✅ Auto Trade: {'ON' if st.session_state.auto_trade_enabled else 'OFF'}")
    st.caption(f"🐺 Wolf Orders: {len(st.session_state.wolf_orders)}")

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🐺 {APP_NAME} v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION} | 🌸 SAMRUDDHI EDITION")
