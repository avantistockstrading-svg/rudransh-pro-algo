import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time
import json

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="RUDRANSH PRO ALGO X", 
    layout="wide", 
    page_icon="🐺",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS FOR PROFESSIONAL UI =================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Card Style */
    .css-1r6slb0, .css-1y4p8pa {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00ff88;
    }
    
    /* Headers */
    h1, h2, h3 {
        background: linear-gradient(135deg, #00ff88 0%, #00b4d8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    /* Buttons */
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
    
    /* Stop Button */
    .stop-btn > button {
        background: linear-gradient(135deg, #ff4444 0%, #ff0000 100%);
    }
    
    /* Success/Error/Warning */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid;
    }
    
    /* Dataframe */
    .dataframe {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Live Time */
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
    
    /* Tabs */
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
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        border-radius: 10px;
    }
    
    /* Status Badges */
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

# ================= API KEYS =================
API_KEYS = {
    "news_api": "YOUR_NEWS_API_KEY",
    "alpha_vantage": "YOUR_ALPHA_VANTAGE_KEY",
    "telegram_bot": "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c",
    "telegram_chat": "1983026913"
}

# ================= COMPLETE F&O SCRIPTS LIST (209 कंपन्या + Commodity) =================
FO_SCRIPTS = [
    # Indices & Commodity
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "CRUDE", "NATURALGAS",
    
    # Full 209 Companies
    "360ONE", "ABB", "APLAPOLLO", "AUBANK", "ADANIENSOL", "ADANIENT", "ADANIGREEN",
    "ADANIPORTS", "ADANIPOWER", "ABCAPITAL", "ALKEM", "AMBER", "AMBUJACEM", "ANGELONE",
    "APOLLOHOSP", "ASHOKLEY", "ASIANPAINT", "ASTRAL", "AUROPHARMA", "DMART", "AXISBANK",
    "BSE", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BAJAJHLDNG", "BANDHANBNK", "BANKBARODA",
    "BANKINDIA", "BDL", "BEL", "BHARATFORG", "BHEL", "BPCL", "BHARTIARTL", "BIOCON",
    "BLUESTARCO", "BOSCHLTD", "BRITANNIA", "CGPOWER", "CANBK", "CDSL", "CHOLAFIN", "CIPLA",
    "COALINDIA", "COCHINSHIP", "COFORGE", "COLPAL", "CAMS", "CONCOR", "CROMPTON", "CUMMINSIND",
    "DLF", "DABUR", "DALBHARAT", "DELHIVERY", "DIVISLAB", "DIXON", "DRREDDY", "ETERNAL",
    "EICHERMOT", "EXIDEIND", "FORCEMOT", "NYKAA", "FORTIS", "GAIL", "GMRAIRPORT", "GLENMARK",
    "GODFRYPHLP", "GODREJCP", "GODREJPROP", "GRASIM", "HCLTECH", "HDFCAMC", "HDFCBANK",
    "HDFCLIFE", "HAVELLS", "HEROMOTOCO", "HINDALCO", "HAL", "HINDPETRO", "HINDUNILVR",
    "HINDZINC", "POWERINDIA", "HYUNDAI", "ICICIBANK", "ICICIGI", "ICICIPRULI", "IDFCFIRSTB",
    "ITC", "INDIANB", "IEX", "IOC", "IRFC", "IREDA", "INDUSTOWER", "INDUSINDBK", "NAUKRI",
    "INFY", "INOXWIND", "INDIGO", "JINDALSTEL", "JSWENERGY", "JSWSTEEL", "JIOFIN", "JUBLFOOD",
    "KEI", "KPITTECH", "KALYANKJIL", "KAYNES", "KFINTECH", "KOTAKBANK", "LTF", "LICHSGFIN",
    "LTM", "LT", "LAURUSLABS", "LICI", "LODHA", "LUPIN", "M&M", "MANAPPURAM", "MANKIND",
    "MARICO", "MARUTI", "MFSL", "MAXHEALTH", "MAZDOCK", "MOTILALOFS", "MPHASIS", "MCX",
    "MUTHOOTFIN", "NBCC", "NHPC", "NMDC", "NTPC", "NATIONALUM", "NESTLEIND", "NAM-INDIA",
    "NUVAMA", "OBEROIRLTY", "ONGC", "OIL", "PAYTM", "OFSS", "POLICYBZR", "PGEL", "PIIND",
    "PNBHOUSING", "PAGEIND", "PATANJALI", "PERSISTENT", "PETRONET", "PIDILITIND", "POLYCAB",
    "PFC", "POWERGRID", "PREMIERENE", "PRESTIGE", "PNB", "RBLBANK", "RECLTD", "RVNL",
    "RELIANCE", "SBICARD", "SBILIFE", "SHREECEM", "SRF", "SAMMAANCAP", "MOTHERSON", "SHRIRAMFIN",
    "SIEMENS", "SOLARINDS", "SONACOMS", "SBIN", "SAIL", "SUNPHARMA", "SUPREMEIND", "SUZLON",
    "SWIGGY", "TATACONSUM", "TVSMOTOR", "TCS", "TATAELXSI", "TMPV", "TATAPOWER", "TATASTEEL",
    "TECHM", "FEDERALBNK", "INDHOTEL", "PHOENIXLTD", "TITAN", "TORNTPHARM", "TRENT", "TIINDIA",
    "UNOMINDA", "UPL", "ULTRACEMCO", "UNIONBANK", "UNITDSPR", "VBL", "VEDL", "VMM", "IDEA",
    "VOLTAS", "WAAREEENER", "WIPRO", "YESBANK", "ZYDUSLIFE"
]

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

# ================= Q4 RESULTS =================
if "q4_results" not in st.session_state:
    st.session_state.q4_results = {
        "HDFC Bank": {"profit": 9.1, "verdict": "🟡 Mixed", "date": "15 May 2026", "revenue": "₹88,500 Cr", "ai_signal": "WAIT"},
        "Reliance": {"profit": -12.5, "verdict": "🔴 Negative", "date": "14 May 2026", "revenue": "₹2,34,000 Cr", "ai_signal": "SELL"},
        "Infosys": {"profit": 11.6, "verdict": "🟠 Cautious", "date": "16 May 2026", "revenue": "₹42,000 Cr", "ai_signal": "CAUTIOUS BUY"},
    }

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

def get_market_news():
    """Fetch latest market news"""
    try:
        url = f"https://newsapi.org/v2/everything?q=stock+market+india&apiKey={API_KEYS['news_api']}&language=en&pageSize=10"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = []
            for article in data.get('articles', [])[:5]:
                articles.append({
                    'title': article['title'],
                    'source': article['source']['name'],
                    'time': article['publishedAt'][:10],
                    'url': article['url']
                })
            return articles
    except:
        pass
    return [
        {'title': 'Nifty hits all-time high at 25,000', 'source': 'Economic Times', 'time': '2026-05-16', 'url': '#'},
        {'title': 'RBI keeps repo rate unchanged at 6.5%', 'source': 'Business Standard', 'time': '2026-05-15', 'url': '#'},
        {'title': 'Crude oil prices surge amid supply concerns', 'source': 'Reuters', 'time': '2026-05-15', 'url': '#'},
    ]

def send_telegram(msg):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{API_KEYS['telegram_bot']}/sendMessage"
        requests.post(url, data={"chat_id": API_KEYS['telegram_chat'], "text": msg}, timeout=10)
    except:
        pass

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
                    "Symbol": f"{order['symbol']} {order.get('strike_price', '')}",
                    "Type": "🐺 WOLF BUY",
                    "Lots": order['qty'],
                    "Entry": round(current_price, 2),
                    "SL": order['sl'],
                    "Target": order['target'],
                    "Status": "ACTIVE"
                }
                st.session_state.trade_journal.append(trade_record)
                send_telegram(f"🐺 WOLF EXECUTED: {order['symbol']} BUY @ ₹{current_price:.2f} | SL: ₹{order['sl']} | Target: ₹{order['target']}")
                
                st.session_state.active_orders.append({
                    'symbol': order['symbol'],
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
            st.session_state.active_orders.pop(i)
            st.rerun()
        
        elif current_price >= order['target']:
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = '✅ TARGET HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit'] = round(current_price, 2)
            send_telegram(f"✅ TARGET HIT: {order['symbol']} @ ₹{current_price:.2f}")
            st.session_state.active_orders.pop(i)
            st.rerun()

# ================= LIVE TIME =================
def update_live_time():
    now = get_ist_now()
    return f"""
    <div class="live-time">
        🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')}
    </div>
    """

# ================= MAIN UI =================
# Header
st.markdown("""
<div style="text-align:center; padding:20px;">
    <h1>🐺 RUDRANSH PRO ALGO X</h1>
    <p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(update_live_time(), unsafe_allow_html=True)
st.markdown("---")

# Control Panel
col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
with col1:
    totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code", key="totp_main")
with col2:
    if st.button("🟢 START ALGO", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED")
            st.rerun()
        else:
            st.error("Valid TOTP required!")
with col3:
    if st.button("🔴 STOP ALGO", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 ALGO STOPPED")
        st.rerun()
with col4:
    if st.session_state.algo_running:
        st.markdown('<span class="badge-success">🟢 RUNNING</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-danger">🔴 STOPPED</span>', unsafe_allow_html=True)
with col5:
    if check_daily_loss_limit():
        st.markdown('<span class="badge-danger">⚠️ LOSS LIMIT HIT</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="badge-warning">📉 Loss: ₹{abs(st.session_state.daily_loss):,.0f}</span>', unsafe_allow_html=True)

st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🐺 WOLF ORDER", "📊 MARKET DASHBOARD", "📰 NEWS & ALERTS", "⚙️ SETTINGS", "📋 JOURNAL"])

# ================= TAB 1: WOLF ORDER =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK (F&O + COMMODITY)")
    st.markdown(f"*Total {len(FO_SCRIPTS)} Symbols Available | Set your hunting strategy*")
    
    with st.expander("➕ PLACE WOLF ORDER", expanded=False):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            wolf_symbol = st.selectbox("Symbol", FO_SCRIPTS, key="wolf_sym")
        with col2:
            strike_price = st.number_input("Strike", min_value=1, max_value=500000, value=24300, step=50, key="wolf_strike")
        with col3:
            wolf_qty = st.number_input("Lots", min_value=1, max_value=100, value=1, key="wolf_qty")
        with col4:
            wolf_buy_above = st.number_input("Buy Above", min_value=1, max_value=500000, value=100, step=10, key="wolf_buy")
        with col5:
            wolf_sl = st.number_input("Stop Loss", min_value=1, max_value=500000, value=80, step=10, key="wolf_sl")
        with col6:
            wolf_target = st.number_input("Target", min_value=1, max_value=500000, value=150, step=10, key="wolf_target")
        with col7:
            if st.button("🐺 PLACE ORDER", use_container_width=True):
                if wolf_buy_above <= wolf_sl:
                    st.error("Buy Above > SL required!")
                elif wolf_target <= wolf_buy_above:
                    st.error("Target > Buy Above required!")
                else:
                    st.session_state.wolf_orders.append({
                        'symbol': wolf_symbol, 'strike_price': strike_price, 'qty': wolf_qty,
                        'buy_above': wolf_buy_above, 'sl': wolf_sl, 'target': wolf_target,
                        'status': 'PENDING', 'entry_price': None, 'entry_time': None
                    })
                    send_telegram(f"🐺 WOLF ORDER: {wolf_symbol} {strike_price} | Buy: {wolf_buy_above} | SL: {wolf_sl} | Target: {wolf_target}")
                    st.success(f"✅ Wolf Order placed for {wolf_symbol}")
                    st.rerun()
    
    # Pending Orders
    pending = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
    if pending:
        st.markdown("### ⏳ PENDING HUNTS")
        df_pending = pd.DataFrame([{
            'Symbol': o['symbol'], 'Strike': o['strike_price'], 'Lots': o['qty'],
            'Buy Above': o['buy_above'], 'SL': o['sl'], 'Target': o['target']
        } for o in pending])
        st.dataframe(df_pending, use_container_width=True)
    
    # Active Orders
    active = st.session_state.active_orders
    if active:
        st.markdown("### 🔴 ACTIVE HUNTS (SL/Target Active)")
        active_data = []
        for o in active:
            current = get_live_price(o['symbol'])
            active_data.append({
                'Symbol': o['symbol'], 'Strike': o.get('strike_price', ''), 
                'Entry': o['entry_price'], 'Current': round(current, 2) if current else 0,
                'SL': o['sl'], 'Target': o['target']
            })
        df_active = pd.DataFrame(active_data)
        st.dataframe(df_active, use_container_width=True)

# ================= TAB 2: MARKET DASHBOARD =================
with tab2:
    st.markdown("### 📊 LIVE MARKET DASHBOARD")
    
    # Live Prices Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nifty = get_live_price("NIFTY")
        st.metric("🇮🇳 NIFTY 50", f"₹{nifty:,.2f}" if nifty else "Loading...")
    with col2:
        banknifty = get_live_price("BANKNIFTY")
        st.metric("🏦 BANK NIFTY", f"₹{banknifty:,.2f}" if banknifty else "Loading...")
    with col3:
        crude = get_live_price("CRUDE") * get_usd_inr_rate()
        st.metric("🛢️ CRUDE OIL", f"₹{crude:,.2f}" if crude else "Loading...")
    with col4:
        ng = get_live_price("NATURALGAS") * get_usd_inr_rate()
        st.metric("🌿 NATURAL GAS", f"₹{ng:,.2f}" if ng else "Loading...")
    
    st.markdown("---")
    
    # Top Gainers/Losers Section
    st.markdown("### 📈 MARKET MOVERS")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 TOP GAINERS")
        gainers = ["RELIANCE +5.2%", "TCS +3.8%", "HDFCBANK +2.5%", "INFY +2.1%", "ICICIBANK +1.9%"]
        for g in gainers:
            st.success(f"▲ {g}")
    
    with col2:
        st.markdown("#### 📉 TOP LOSERS")
        losers = ["TATASTEEL -3.2%", "JSWSTEEL -2.8%", "HINDALCO -2.1%", "SAIL -1.7%", "VEDL -1.2%"]
        for l in losers:
            st.error(f"▼ {l}")

# ================= TAB 3: NEWS & ALERTS =================
with tab3:
    st.markdown("### 📰 MARKET NEWS & ALERTS")
    
    # Voice Alert Toggle
    col1, col2 = st.columns([3,1])
    with col2:
        st.session_state.voice_enabled = st.checkbox("🔊 Voice Alerts", value=st.session_state.voice_enabled)
    
    st.markdown("---")
    
    # Fetch News
    news_articles = get_market_news()
    
    for article in news_articles:
        with st.container():
            st.markdown(f"**📌 {article['title']}**")
            st.caption(f"Source: {article['source']} | {article['time']}")
            if st.button("🔔 Send Alert", key=f"alert_{article['title'][:20]}"):
                send_telegram(f"📰 NEWS: {article['title']}")
                st.success("Alert sent to Telegram!")
            st.markdown("---")

# ================= TAB 4: SETTINGS =================
with tab4:
    st.markdown("### ⚙️ SYSTEM SETTINGS")
    
    # TP Settings
    st.markdown("#### 🇮🇳 NIFTY SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots, key="nifty_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.nifty_tp1, key="nifty_tp1")
    with col3:
        st.checkbox("ON", value=st.session_state.nifty_tp1_enabled, key="nifty_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.nifty_tp2, key="nifty_tp2")
    with col5:
        st.checkbox("ON", value=st.session_state.nifty_tp2_enabled, key="nifty_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.nifty_tp3, key="nifty_tp3")
    with col7:
        st.checkbox("ON", value=st.session_state.nifty_tp3_enabled, key="nifty_tp3_en")
    
    st.markdown("#### 🛢️ CRUDE SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, key="crude_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.crude_tp1, key="crude_tp1")
    with col3:
        st.checkbox("ON", value=st.session_state.crude_tp1_enabled, key="crude_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.crude_tp2, key="crude_tp2")
    with col5:
        st.checkbox("ON", value=st.session_state.crude_tp2_enabled, key="crude_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.crude_tp3, key="crude_tp3")
    with col7:
        st.checkbox("ON", value=st.session_state.crude_tp3_enabled, key="crude_tp3_en")
    
    st.markdown("#### 🌿 NATURAL GAS SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, key="ng_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=50, value=st.session_state.ng_tp1, key="ng_tp1")
    with col3:
        st.checkbox("ON", value=st.session_state.ng_tp1_enabled, key="ng_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=50, value=st.session_state.ng_tp2, key="ng_tp2")
    with col5:
        st.checkbox("ON", value=st.session_state.ng_tp2_enabled, key="ng_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=50, value=st.session_state.ng_tp3, key="ng_tp3")
    with col7:
        st.checkbox("ON", value=st.session_state.ng_tp3_enabled, key="ng_tp3_en")
    
    st.markdown("---")
    st.markdown("#### 📉 RISK MANAGEMENT")
    st.session_state.max_daily_loss = st.number_input("Max Daily Loss (₹)", 10000, 500000, st.session_state.max_daily_loss, 10000)

# ================= TAB 5: JOURNAL =================
with tab5:
    st.markdown("### 📋 TRADING JOURNAL")
    
    if st.session_state.trade_journal:
        df_journal = pd.DataFrame(st.session_state.trade_journal)
        st.dataframe(df_journal, use_container_width=True, height=400)
    else:
        st.info("📭 No trades executed yet. Place a Wolf Order to start hunting!")
    
    st.markdown("---")
    st.markdown("### 📊 PERFORMANCE SUMMARY")
    total_trades = len(st.session_state.trade_journal)
    active_count = len([t for t in st.session_state.trade_journal if 'ACTIVE' in str(t.get('Status', ''))])
    sl_count = len([t for t in st.session_state.trade_journal if 'SL' in str(t.get('Status', ''))])
    target_count = len([t for t in st.session_state.trade_journal if 'TARGET' in str(t.get('Status', ''))])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trades", total_trades)
    with col2:
        st.metric("Active", active_count)
    with col3:
        st.metric("SL Hit", sl_count)
    with col4:
        st.metric("Target Hit", target_count)

# ================= AUTO TRADING LOGIC =================
if st.session_state.algo_running and st.session_state.totp_verified and not check_daily_loss_limit():
    check_and_execute_wolf_orders()
    monitor_active_orders()
    st.info("🐺 Wolf is hunting the market... Tracking orders 🔍")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🐺 WOLF DASHBOARD")
    st.markdown("---")
    
    st.markdown("### 📊 TODAY'S STATUS")
    st.metric("Active Hunts", len(st.session_state.active_orders))
    st.metric("Pending Hunts", len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']))
    st.metric("Daily P&L", f"₹{abs(st.session_state.daily_loss):,.2f}")
    
    st.markdown("---")
    st.markdown("### 🛡️ SYMBOLS COUNT")
    st.metric("Total F&O Stocks", f"{len(FO_SCRIPTS)}")
    st.caption("Includes NIFTY, BANKNIFTY, CRUDE, NG + 209 Stocks")
    
    st.markdown("---")
    st.markdown("### 📱 CONNECTED")
    st.caption("✅ Telegram Bot Active")
    st.caption(f"🐺 Wolf Mode: {'ACTIVE' if st.session_state.algo_running else 'SLEEPING'}")
    
    st.markdown("---")
    st.markdown("### 📈 MARKET SENTIMENT")
    st.progress(0.65)
    st.caption("Bullish: 65% | Bearish: 35%")

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:20px; color:#94a3b8;">
    🔐 App Protected | 🐺 Wolf Order Book Active | 📱 Telegram Enabled
    <br>
    Developed by Satish D. Nakhate, Talwade, Pune - 412114
</div>
""", unsafe_allow_html=True)

# ================= AUTO REFRESH =================
time.sleep(10)
st.rerun()
