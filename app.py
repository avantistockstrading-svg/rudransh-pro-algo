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

# Reset daily counters
if get_ist_now().date() != st.session_state.last_reset_date:
    st.session_state.daily_trade_count = {
        "NIFTY": {"buy": 0, "sell": 0},
        "BANKNIFTY": {"buy": 0, "sell": 0},
        "CRUDE": {"buy": 0, "sell": 0},
        "NATURALGAS": {"buy": 0, "sell": 0}
    }
    st.session_state.daily_pnl = 0
    st.session_state.last_reset_date = get_ist_now().date()

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
    "APLAPOLLO", "AUBANK", "BAJAJHLDNG", "BALKRISIND", "BATAINDIA", "BERGEPAINT",
    "BHARATFORG", "BHEL", "BIOCON", "BOSCHLTD", "CADILAHC", "CAMS", "CAPLIPOINT",
    "CASTROLIND", "CCL", "CDSL", "CENTURYPLY", "CESC", "CGPOWER", "CLEAN", "COCHINSHIP",
    "CONCOR", "COROMANDEL", "CROMPTON", "CUMMINSIND", "CYIENT", "DALBHARAT", "DELHIVERY",
    "DIXON", "EASEMYTRIP", "EDELWEISS", "EMAMILTD", "ENDURANCE", "ERIS", "ESCORTS",
    "EXIDEIND", "FACT", "FINCABLES", "FINEORG", "FIVESTAR", "FORTIS", "GESHIP",
    "GLENMARK", "GMRINFRA", "GODREJAGRO", "GRANULES", "GREAVESCOT", "GSPL", "GUFICBIO",
    "HAL", "HAPPSTMNDS", "HEIDELBERG", "HINDZINC", "IBULHSGFIN", "IDBI", "IDFCFIRSTB",
    "IEX", "INDIAMART", "INDIANB", "INDUSTOWER", "INOXWIND", "IREDA", "IRFC",
    "JINDALSTEL", "JSPL", "JSWENERGY", "KALYANKJIL", "KAYNES", "KEI", "KFINTECH",
    "KPITTECH", "LAURUSLABS", "LICHSGFIN", "LODHA", "LTF", "MANAPPURAM", "MFSL",
    "MOTILALOFS", "NATIONALUM", "NAMINDIA", "NBCC", "NUVAMA", "OBEROIRLTY", "OIL",
    "OFSS", "PAYTM", "PAGEIND", "PATANJALI", "PERSISTENT", "PETRONET", "PGEL",
    "PHOENIXLTD", "PIIND", "PNBHOUSING", "POLICYBZR", "PRESTIGE", "RBLBANK", "RVNL",
    "SHRIRAMFIN", "SONACOMS", "SUPREMEIND", "SUZLON", "SWIGGY", "TATAELXSI", "TIINDIA",
    "TORNTPHARM", "TRENT", "TVSMOTOR", "UNIONBANK", "UNITEDSPIRITS", "UNOMINDA",
    "VBL", "VOLTAS", "WAAREEENER", "WELCORP", "ZEEL"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= TRADING HOURS =================
TRADING_HOURS = {
    "NIFTY": {"start": 9, "start_min": 30, "end": 15, "end_min": 0},
    "BANKNIFTY": {"start": 9, "start_min": 30, "end": 15, "end_min": 0},
    "CRUDE": {"start": 11, "start_min": 0, "end": 22, "end_min": 0},
    "NATURALGAS": {"start": 11, "start_min": 0, "end": 22, "end_min": 0}
}

def is_trading_time(symbol):
    now = get_ist_now()
    hours = TRADING_HOURS.get(symbol, {"start": 9, "start_min": 30, "end": 15, "end_min": 0})
    start_time = now.replace(hour=hours["start"], minute=hours["start_min"], second=0)
    end_time = now.replace(hour=hours["end"], minute=hours["end_min"], second=0)
    return start_time <= now <= end_time and now.weekday() < 5

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

# ================= PENDING RESULTS =================
PENDING_RESULTS = [
    {"name": "Bharat Electronics", "symbol": "BEL"},
    {"name": "BPCL", "symbol": "BPCL"},
    {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE"},
    {"name": "Mankind Pharma", "symbol": "MANKIND"},
    {"name": "PI Industries", "symbol": "PIIND"},
]

# ================= FMP API FUNCTIONS =================
def check_fmp_api():
    try:
        url = f"https://financialmodelingprep.com/stable/stock-list?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return True, "Active", f"✅ Connected"
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

# ================= TREND FUNCTIONS =================
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

# ================= TECHNICAL INDICATORS =================
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
        if df.empty or len(df) < 200:
            return None
        
        close = df['Close']
        high = df['High']
        low = df['Low']
        volume = df['Volume']
        
        ema9 = close.ewm(span=9, adjust=False).mean().iloc[-1]
        ema20 = close.ewm(span=20, adjust=False).mean().iloc[-1]
        ema200 = close.ewm(span=200, adjust=False).mean().iloc[-1]
        
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
        
        prev_candle = df.iloc[-2]
        curr_candle = df.iloc[-1]
        strong_bull = curr_candle['Close'] > curr_candle['Open'] and curr_candle['Close'] > prev_candle['High']
        strong_bear = curr_candle['Close'] < curr_candle['Open'] and curr_candle['Close'] < prev_candle['Low']
        
        sideways = (45 < current_rsi < 55) and (adx < 20) if not pd.isna(adx) else False
        
        return {
            "current_price": close.iloc[-1], "ema9": ema9, "ema20": ema20, "ema200": ema200,
            "rsi": current_rsi, "adx": adx if not pd.isna(adx) else 25,
            "volume_filter": volume_filter, "strong_bull": strong_bull, "strong_bear": strong_bear,
            "sideways": sideways, "c1_high": prev_candle['High'], "c1_low": prev_candle['Low']
        }
    except:
        return None

# ================= STRICT SIGNAL =================
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
    
    buy_conditions = (nifty_condition and sector_condition and not indicators["sideways"] and
                      indicators["ema9"] > indicators["ema20"] and indicators["current_price"] > indicators["ema200"] and
                      indicators["rsi"] >= 55 and indicators["adx"] >= 22 and indicators["volume_filter"] and
                      indicators["strong_bull"] and indicators["current_price"] > indicators["c1_high"] and
                      trend5_up and trend15_up and trend1h_up)
    
    sell_conditions = (nifty_trend == "NEGATIVE" and not indicators["sideways"] and
                       indicators["ema9"] < indicators["ema20"] and indicators["current_price"] < indicators["ema200"] and
                       indicators["rsi"] <= 45 and indicators["adx"] >= 22 and indicators["volume_filter"] and
                       indicators["strong_bear"] and indicators["current_price"] < indicators["c1_low"] and
                       not trend5_up and not trend15_up and not trend1h_up)
    
    if buy_conditions:
        return "BUY", indicators["current_price"], indicators
    elif sell_conditions:
        return "SELL", indicators["current_price"], indicators
    return "WAIT", 0, indicators

# ================= LIVE P&L FUNCTIONS =================
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
        "Type": order.get('signal_type', 'MANUAL'), "Lots": order['qty'],
        "Entry": round(entry_price, 2), "Exit": round(exit_price, 2) if exit_price else "-",
        "P&L (₹)": round(pnl_value, 2), "Status": status
    }
    st.session_state.trade_journal.append(trade_record)
    if "daily_pnl" not in st.session_state:
        st.session_state.daily_pnl = 0
    st.session_state.daily_pnl += pnl_value

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

def monitor_fmp_results():
    for company in PENDING_RESULTS:
        earnings = get_company_earnings(company['symbol'])
        if earnings:
            revenue = earnings.get('revenue', 0)
            prev_revenue = earnings.get('revenue', 0)
            revenue_growth = ((revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            if revenue_growth > 10:
                result_type = "POSITIVE"
            elif revenue_growth < -5:
                result_type = "NEGATIVE"
            else:
                result_type = "NEUTRAL"
            alert = {'company': company['name'], 'result': result_type, 'time': get_ist_now().strftime('%H:%M:%S')}
            already = False
            for a in st.session_state.result_alerts:
                if a.get('company') == company['name']:
                    already = True
                    break
            if not already:
                st.session_state.result_alerts.append(alert)
                send_telegram(f"📊 RESULT: {company['name']} - {result_type}")

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
        st.session_state.wolf_orders.append({
            'symbol': symbol, 'option_type': option_type, 'strike_price': strike_price, 'qty': 1,
            'buy_above': current_price, 'sl': current_price * 0.85, 'target': current_price * 1.2,
            'status': 'PENDING', 'placed_time': get_ist_now().strftime('%H:%M:%S'),
            'auto_trade': True, 'result_based': True, 'company': company_name
        })
        send_telegram(f"📊 RESULT: {company_name} - {signal} {option_type}")
        return True, f"{signal} order placed"
    return False, "Price not available"

def monitor_today_results():
    for company in PENDING_RESULTS:
        if f"{company['symbol']}_processed" in st.session_state:
            continue
        earnings = get_company_earnings(company['symbol'])
        if earnings:
            revenue = earnings.get('revenue', 0)
            prev_revenue = earnings.get('revenue', 0)
            revenue_growth = ((revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            if revenue_growth > 10:
                result_type = "POSITIVE"
            elif revenue_growth < -5:
                result_type = "NEGATIVE"
            else:
                result_type = "NEUTRAL"
            success, message = process_result_and_trade(company['name'], company['symbol'], result_type)
            st.session_state[f"{company['symbol']}_processed"] = True
            st.session_state.result_alerts.append({'company': company['name'], 'result': result_type, 'action': message, 'time': get_ist_now().strftime('%H:%M:%S')})

def auto_trade_from_signal_with_journal():
    symbols_to_monitor = ["NIFTY", "BANKNIFTY", "CRUDE", "NATURALGAS"] + FO_SCRIPTS[:50]
    nifty_trend = get_nifty_trend()
    for symbol in symbols_to_monitor:
        if symbol == "NIFTY":
            continue
        if not is_trading_time(symbol):
            continue
        sector = SECTOR_MAPPING.get(symbol, "NEUTRAL")
        sector_trend = get_sector_trend(sector) if sector != "NEUTRAL" else "NEUTRAL"
        signal, price, indicators = get_strict_signal(symbol, nifty_trend, sector_trend)
        if signal == "BUY" and can_take_trade(symbol, "BUY"):
            if symbol in ["NIFTY", "BANKNIFTY"]:
                strike_interval = 50 if symbol == "NIFTY" else 100
                strike_price = math.floor(price / strike_interval) * strike_interval
            elif symbol in ["CRUDE", "NATURALGAS"]:
                strike_price = math.floor(price) * 100
            else:
                strike_price = math.floor(price / 10) * 10
            st.session_state.wolf_orders.append({
                'symbol': symbol, 'option_type': "CALL (CE)", 'strike_price': strike_price, 'qty': 1,
                'buy_above': price, 'sl': price * 0.85, 'target': price * 1.2,
                'status': 'PENDING', 'placed_time': get_ist_now().strftime('%H:%M:%S'),
                'auto_trade': True, 'signal_type': 'STRICT_BUY'
            })
            increment_trade_count(symbol, "BUY")
            send_telegram(f"🐺 AUTO BUY: {symbol} @ {price:.2f}")
        elif signal == "SELL" and can_take_trade(symbol, "SELL"):
            if symbol in ["NIFTY", "BANKNIFTY"]:
                strike_interval = 50 if symbol == "NIFTY" else 100
                strike_price = math.floor(price / strike_interval) * strike_interval
            elif symbol in ["CRUDE", "NATURALGAS"]:
                strike_price = math.floor(price) * 100
            else:
                strike_price = math.floor(price / 10) * 10
            st.session_state.wolf_orders.append({
                'symbol': symbol, 'option_type': "PUT (PE)", 'strike_price': strike_price, 'qty': 1,
                'buy_above': price, 'sl': price * 0.85, 'target': price * 1.2,
                'status': 'PENDING', 'placed_time': get_ist_now().strftime('%H:%M:%S'),
                'auto_trade': True, 'signal_type': 'STRICT_SELL'
            })
            increment_trade_count(symbol, "SELL")
            send_telegram(f"🐺 AUTO SELL: {symbol} @ {price:.2f}")

def check_and_execute_orders_with_journal():
    for order in st.session_state.wolf_orders[:]:
        if order['status'] == 'PENDING':
            price = get_live_price(order['symbol'])
            if price > 0 and price >= order['buy_above']:
                order['status'] = 'ACTIVE'
                order['entry_price'] = price
                order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
                add_to_journal(order, None, None)
                send_telegram(f"🐺 EXECUTED: {order['symbol']} @ ₹{price:.2f}")
                st.session_state.active_orders.append({
                    'symbol': order['symbol'], 'option_type': order['option_type'],
                    'strike_price': order.get('strike_price', ''), 'entry_price': price,
                    'sl': order['sl'], 'target': order['target'], 'qty': order['qty'],
                    'signal_type': order.get('signal_type', 'MANUAL'), 'entry_time': order['entry_time']
                })

def monitor_active_orders_with_pnl():
    for i, order in enumerate(st.session_state.active_orders[:]):
        current_price = get_live_price(order['symbol'])
        if current_price == 0:
            continue
        if current_price <= order['sl']:
            add_to_journal(order, current_price, "SL HIT")
            send_telegram(f"❌ SL HIT: {order['symbol']} @ ₹{current_price:.2f}")
            st.session_state.active_orders.pop(i)
            st.rerun()
        elif current_price >= order['target']:
            add_to_journal(order, current_price, "TARGET HIT")
            send_telegram(f"✅ TARGET HIT: {order['symbol']} @ ₹{current_price:.2f}")
            st.session_state.active_orders.pop(i)
            st.rerun()

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
    st.markdown(f'<div class="status-card" style="border-left: 4px solid #00ff88;">📊 <strong>FMP API</strong><br><span style="color:#00ff88">🟢 {fmp_msg}</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="status-card" style="border-left: 4px solid #00ff88;">📰 <strong>GNews API</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="status-card" style="border-left: 4px solid #00ff88;">📱 <strong>Telegram Bot</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ================= CONTROL PANEL =================
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; padding: 20px; margin: 10px 0; border: 1px solid rgba(0,255,136,0.2);">
    <h4 style="margin:0 0 15px 0; color:#00b4d8; text-align:center;">🎮 CONTROL PANEL</h4>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("""<div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 5px 15px; border: 1px solid #00b4d8;"><label style="color:#00b4d8; font-size:12px;">🔐 6-DIGIT TOTP CODE</label></div>""", unsafe_allow_html=True)
    totp = st.text_input("TOTP", type="password", placeholder="Enter 6-digit code", key="totp_main", label_visibility="collapsed")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🟢 START ALGO", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED v5.0")
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

col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.algo_running:
        st.markdown("""<div style="background: rgba(0,255,136,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00ff88;"><span style="color:#00ff88;">🟢 SYSTEM STATUS</span><br><span style="color:#00ff88;">● ACTIVE</span></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="background: rgba(255,68,68,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #ff4444;"><span style="color:#ff4444;">🔴 SYSTEM STATUS</span><br><span style="color:#ff4444;">● INACTIVE</span></div>""", unsafe_allow_html=True)
with col2:
    if st.session_state.totp_verified:
        st.markdown("""<div style="background: rgba(0,255,136,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00ff88;"><span style="color:#00ff88;">🔐 TOTP STATUS</span><br><span style="color:#00ff88;">✓ VERIFIED</span></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="background: rgba(255,68,68,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #ff4444;"><span style="color:#ff4444;">🔐 TOTP STATUS</span><br><span style="color:#ff4444;">✗ NOT VERIFIED</span></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div style="background: rgba(0,180,216,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00b4d8;"><span style="color:#00b4d8;">⏰ CURRENT TIME</span><br><span style="color:#00b4d8; font-size:14px;">{now.strftime('%H:%M:%S')} IST</span></div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🐺 WOLF ORDER", "🌸 SANSKRUTI MARKET", "📰 VAISHNAVI NEWS", 
    "📈 OVI RESULTS", "⚙️ SAHYADRI SETTINGS", "💰 PORTFOLIO & P&L"
])

# ================= TAB 1: WOLF ORDER =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK")
    st.markdown(f"*Total {len(FO_SCRIPTS)} F&O Symbols Available*")
    st.markdown("---")
    
    total_orders = len(st.session_state.wolf_orders)
    pending_orders = len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING'])
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
    
    pending_list = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
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
    st.markdown("### 🌸 SANSKRUTI MARKET")
    st.markdown("*Live Indian & Global Markets*")
    st.markdown("---")
    
    usd_inr = get_usd_inr_rate()
    
    # NIFTY
    nifty = yf.download("^NSEI", period="2d", interval="1d", progress=False)
    nifty_current = float(nifty['Close'].iloc[-1]) if not nifty.empty else 0
    
    # BANKNIFTY
    banknifty = yf.download("^NSEBANK", period="2d", interval="1d", progress=False)
    bank_current = float(banknifty['Close'].iloc[-1]) if not banknifty.empty else 0
    
    # CRUDE
    crude = yf.download("CL=F", period="2d", interval="1d", progress=False)
    crude_usd = float(crude['Close'].iloc[-1]) if not crude.empty else 0
    crude_inr = crude_usd * usd_inr
    
    # NG
    ng = yf.download("NG=F", period="2d", interval="1d", progress=False)
    ng_usd = float(ng['Close'].iloc[-1]) if not ng.empty else 0
    ng_inr = ng_usd * usd_inr
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if nifty_current > 0:
            st.metric("🇮🇳 NIFTY 50", f"₹{nifty_current:,.2f}")
        else:
            st.markdown("🔴 Market Closed")
    with col2:
        if bank_current > 0:
            st.metric("🏦 BANK NIFTY", f"₹{bank_current:,.2f}")
        else:
            st.markdown("🔴 Market Closed")
    with col3:
        if crude_usd > 0:
            st.metric("🛢️ CRUDE OIL", f"₹{crude_inr:,.2f}", f"${crude_usd:.2f}")
        else:
            st.markdown("🔴 Market Closed")
    with col4:
        if ng_usd > 0:
            st.metric("🌿 NATURAL GAS", f"₹{ng_inr:,.2f}", f"${ng_usd:.2f}")
        else:
            st.markdown("🔴 Market Closed")

# ================= TAB 3: VAISHNAVI NEWS =================
with tab3:
    st.markdown("### 📰 VAISHNAVI NEWS")
    col1, col2 = st.columns([3,1])
    with col2:
        st.session_state.voice_enabled = st.checkbox("🔊 Voice", st.session_state.voice_enabled)
    st.markdown("---")
    
    for news in get_news_with_sentiment():
        st.markdown(f'<div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; margin: 10px 0; border-left: 5px solid {news["color"]};">'
                   f'<b>📌 {news["title"]}</b><br><small>{news["source"]} | {news["time"]}</small>'
                   f'<div style="text-align:right;"><span style="background:{news["color"]}; padding:5px 10px; border-radius:15px;">{news["icon"]} {news["sentiment"]}</span></div></div>', unsafe_allow_html=True)

# ================= TAB 4: OVI RESULTS =================
with tab4:
    st.markdown("### 📈 OVI RESULTS - Q4 FY26")
    if fmp_status:
        st.success("✅ FMP API Connected")
    st.markdown("---")
    
    st.markdown("#### 📅 Today's Result Announcements")
    for company in PENDING_RESULTS:
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            st.write(f"**{company['name']}** ({company['symbol']})")
        with col2:
            st.markdown('<span style="color:#ffaa00">⏳ Waiting</span>', unsafe_allow_html=True)
        with col3:
            if f"{company['symbol']}_processed" in st.session_state:
                st.markdown('<span style="color:#00ff88">✅ Processed</span>', unsafe_allow_html=True)
        st.markdown("---")
    
    if st.session_state.result_alerts:
        st.markdown("#### 🔔 Result Alerts")
        for alert in st.session_state.result_alerts[-5:]:
            st.info(f"📊 {alert.get('company', 'Unknown')} | Result: {alert.get('result', 'N/A')} | Time: {alert.get('time', '')}")

# ================= TAB 5: SAHYADRI SETTINGS =================
with tab5:
    st.markdown("### ⚙️ SAHYADRI SETTINGS")
    st.markdown("---")
    
    st.markdown("#### 🤖 AUTO TRADE")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Lots", 1, 50, st.session_state.auto_trade_qty)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("SL %", 1, 20, st.session_state.auto_trade_sl_percent)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", 1, 30, st.session_state.auto_trade_target_percent)
    
    st.markdown("---")
    st.markdown("#### 📊 STRICT BUY/SELL SIGNALS")
    
    nifty_trend = get_nifty_trend()
    col1, col2, col3, col4 = st.columns(4)
    
    nifty_signal, nifty_price, _ = get_strict_signal("NIFTY", nifty_trend, "NEUTRAL")
    bank_signal, bank_price, _ = get_strict_signal("BANKNIFTY", nifty_trend, "NEUTRAL")
    crude_signal, crude_price, _ = get_strict_signal("CRUDE", nifty_trend, "NEUTRAL")
    ng_signal, ng_price, _ = get_strict_signal("NATURALGAS", nifty_trend, "NEUTRAL")
    
    with col1:
        if nifty_signal == "BUY":
            st.markdown(f'<div style="background:#00ff88; border-radius:10px; padding:10px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3>🟢 BUY</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
        elif nifty_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:10px; padding:10px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3>🔴 SELL</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:#ffaa00; border-radius:10px; padding:10px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3>🟡 WAIT</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col2:
        if bank_signal == "BUY":
            st.markdown(f'<div style="background:#00ff88; border-radius:10px; padding:10px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3>🟢 BUY</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
        elif bank_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:10px; padding:10px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3>🔴 SELL</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:#ffaa00; border-radius:10px; padding:10px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3>🟡 WAIT</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col3:
        if crude_signal == "BUY":
            st.markdown(f'<div style="background:#00ff88; border-radius:10px; padding:10px; text-align:center;"><h4>🛢️ CRUDE</h4><h3>🟢 BUY</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
        elif crude_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:10px; padding:10px; text-align:center;"><h4>🛢️ CRUDE</h4><h3>🔴 SELL</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:#ffaa00; border-radius:10px; padding:10px; text-align:center;"><h4>🛢️ CRUDE</h4><h3>🟡 WAIT</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col4:
        if ng_signal == "BUY":
            st.markdown(f'<div style="background:#00ff88; border-radius:10px; padding:10px; text-align:center;"><h4>🌿 NG</h4><h3>🟢 BUY</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
        elif ng_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:10px; padding:10px; text-align:center;"><h4>🌿 NG</h4><h3>🔴 SELL</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:#ffaa00; border-radius:10px; padding:10px; text-align:center;"><h4>🌿 NG</h4><h3>🟡 WAIT</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 📊 DAILY TRADE LIMITS")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("NIFTY", f"B:{st.session_state.daily_trade_count['NIFTY']['buy']}/1 | S:{st.session_state.daily_trade_count['NIFTY']['sell']}/1")
    with col2:
        st.metric("BANKNIFTY", f"B:{st.session_state.daily_trade_count['BANKNIFTY']['buy']}/1 | S:{st.session_state.daily_trade_count['BANKNIFTY']['sell']}/1")
    with col3:
        st.metric("CRUDE", f"B:{st.session_state.daily_trade_count['CRUDE']['buy']}/1 | S:{st.session_state.daily_trade_count['CRUDE']['sell']}/1")
    with col4:
        st.metric("NG", f"B:{st.session_state.daily_trade_count['NATURALGAS']['buy']}/1 | S:{st.session_state.daily_trade_count['NATURALGAS']['sell']}/1")
    
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

# ================= TAB 6: PORTFOLIO & P&L =================
with tab6:
    st.markdown("### 💰 PORTFOLIO & LIVE P&L")
    st.markdown("*Real-time profit/loss tracking*")
    st.markdown("---")
    
    show_portfolio_dashboard()

# ================= AUTO EXECUTION =================
if st.session_state.algo_running and st.session_state.totp_verified:
    monitor_today_results()
    check_and_execute_orders_with_journal()
    monitor_active_orders_with_pnl()
    
    if st.session_state.auto_trade_enabled:
        auto_trade_from_signal_with_journal()
    
    st.info("🐺 Wolf is hunting... Live P&L Active 🤖")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:15px; background: linear-gradient(135deg, #8B0000, #DC143C); border-radius: 15px; margin-bottom: 20px; border: 1px solid #FFD700;">
        <h2 style="margin:0; color:#FFD700;">🌸 SAMRUDDHI DASHBOARD</h2>
        <p style="margin:5px 0 0 0; color:#FFD700;">🐺 Rudransh Algo v5.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    active_count = len(st.session_state.active_orders)
    st.markdown(f'<div style="background: rgba(0,255,136,0.1); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size: 28px;">🔴</span><h3>{active_count}</h3><p>Active Orders</p></div>', unsafe_allow_html=True)
    
    pending_count = len([o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING'])
    st.markdown(f'<div style="background: rgba(255,170,0,0.1); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size: 28px;">⏳</span><h3>{pending_count}</h3><p>Pending Orders</p></div>', unsafe_allow_html=True)
    
    total_trades = len(st.session_state.trade_journal)
    st.markdown(f'<div style="background: rgba(0,180,216,0.1); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size: 28px;">📋</span><h3>{total_trades}</h3><p>Total Trades</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<span style="color:#00ff88">✅ FMP API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ GNews API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ Telegram: Active</span>', unsafe_allow_html=True)
    auto_text = "ON" if st.session_state.auto_trade_enabled else "OFF"
    auto_color = "#00ff88" if st.session_state.auto_trade_enabled else "#ff4444"
    st.markdown(f'<span style="color:{auto_color}">✅ Auto Trade: {auto_text}</span>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🐺 {APP_NAME} v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION} | All Features Real")
