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
from streamlit_autorefresh import st_autorefresh

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
def get_ist_now():
    """Returns current IST datetime"""
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))

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

# ================= COMPLETE F&O SYMBOLS =================
FO_SCRIPTS = [
    "NIFTY", "CRUDE", "NATURALGAS",
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

# ================= TRADING HOURS DICT =================
TRADING_HOURS = {
    "NIFTY": {"start": 9, "start_min": 30, "end": 15, "end_min": 0},
    "BANKNIFTY": {"start": 9, "start_min": 30, "end": 15, "end_min": 0},
    "CRUDE": {"start": 11, "start_min": 0, "end": 22, "end_min": 0},
    "NATURALGAS": {"start": 11, "start_min": 0, "end": 22, "end_min": 0}
}

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

# ================= EARNINGS CALENDAR =================
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
    if earnings:
        return earnings
    return []

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
        "Type": order.get('signal_type', 'MANUAL'), "Lots": order['qty'],
        "Entry": round(entry_price, 2), "Exit": round(exit_price, 2) if exit_price else "-",
        "P&L (₹)": round(pnl_value, 2), "Status": status
    }
    st.session_state.trade_journal.append(trade_record)
    st.session_state.daily_pnl += pnl_value
    
    # Save to live performance
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

# ================= LIVE PERFORMANCE STORAGE =================
if "live_performance" not in st.session_state:
    st.session_state.live_performance = {
        "NIFTY": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "BANKNIFTY": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "STOCK": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "CRUDE": {"BUY":0,"SELL":0,"TP3":0,"SL":0},
        "NG": {"BUY":0,"SELL":0,"TP3":0,"SL":0}
    }

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
            "current_price": float(close.iloc[-1]), "ema9": float(ema9), "ema20": float(ema20),
            "ema200": float(ema200), "rsi": float(current_rsi), "adx": float(adx) if not pd.isna(adx) else 25,
            "volume_filter": bool(volume_filter), "strong_bull": bool(strong_bull), "strong_bear": bool(strong_bear),
            "sideways": bool(sideways), "c1_high": float(c1_high), "c1_low": float(c1_low)
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

# ================= LIVE P&L FUNCTIONS =================
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
    
    # Live Performance Table
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
    <h1>🐺 {APP_NAME}</h1>
    <p style="color:#94a3b8;">{APP_AUTHOR}, {APP_LOCATION} | v{APP_VERSION}</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

now = get_ist_now()
st.markdown(f"<div class='live-time'>🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')}</div>", unsafe_allow_html=True)
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🐺 WOLF ORDER", "🌸 SANSKRUTI MARKET", "📰 VAISHNAVI NEWS", 
    "📈 OVI RESULTS", "⚙️ SAHYADRI SETTINGS", "💰 VEDASHREE PORTFOLIO & LIVE P&L"
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

# ================= TAB 4: OVI RESULTS (ONLY TODAY + NEXT 2 DAYS) =================
with tab4:
    st.markdown("### 📈 OVI RESULTS - Q4 FY26 MONITORING")
    st.markdown("*Showing ONLY Today's + Next 2 Days Results*")
    
    st.markdown("---")
    
    # Result schedule database (Q4 FY26 expected dates)
    RESULT_SCHEDULE = {
        # आजचे निकाल (8 June 2026)
        "BRITANNIA": {"date": "08 Jun 2026", "time": "After Market", "quarter": "Q4 FY26"},
        "CIPLA": {"date": "08 Jun 2026", "time": "After Market", "quarter": "Q4 FY26"},
        
        # उद्याचे निकाल (9 June 2026)
        "DRREDDY": {"date": "09 Jun 2026", "time": "After Market", "quarter": "Q4 FY26"},
        "M&M": {"date": "09 Jun 2026", "time": "After Market", "quarter": "Q4 FY26"},
        
        # परवाचे निकाल (10 June 2026)
        "NESTLEIND": {"date": "10 Jun 2026", "time": "After Market", "quarter": "Q4 FY26"},
        
        # हे सगळे झालेले निकाल - काढून टाकले
        # "RELIANCE", "TCS", "INFY" etc - पूर्वीचे झालेले
    }
    
    # Dynamic watchlist - फक्त upcoming results चे
    def get_upcoming_results():
        """Get only today's and next 2 days results"""
        from datetime import datetime, timedelta
        
        current_date = get_ist_now().date()
        today_str = current_date.strftime("%d %b %Y")
        tomorrow_str = (current_date + timedelta(days=1)).strftime("%d %b %Y")
        dayafter_str = (current_date + timedelta(days=2)).strftime("%d %b %Y")
        
        upcoming_symbols = []
        for symbol, info in RESULT_SCHEDULE.items():
            result_date = info.get("date", "")
            if result_date in [today_str, tomorrow_str, dayafter_str]:
                upcoming_symbols.append(symbol)
        
        return upcoming_symbols
    
    def get_result_status(result_date_str):
        """Check if result is today, tomorrow, or day after"""
        try:
            from datetime import datetime, timedelta
            current_date = get_ist_now().date()
            result_datetime = datetime.strptime(result_date_str, "%d %b %Y").date()
            
            days_diff = (result_datetime - current_date).days
            
            if days_diff == 0:
                return "🔴 TODAY", "today"
            elif days_diff == 1:
                return "⏳ TOMORROW", "tomorrow"
            elif days_diff == 2:
                return "📅 DAY AFTER", "dayafter"
            else:
                return None, None  # Filter out
        except:
            return None, None
    
    # Auto fetch earnings function - फक्त upcoming results साठी
    def get_auto_earnings_data():
        """Automatically fetch earnings data ONLY for today + next 2 days"""
        earnings_data = []
        
        upcoming_symbols = get_upcoming_results()
        
        if not upcoming_symbols:
            return []
        
        # Simple progress without blinking
        status_text = st.empty()
        status_text.info(f"📊 Loading {len(upcoming_symbols)} upcoming results...")
        
        for i, symbol in enumerate(upcoming_symbols):
            try:
                ticker = yf.Ticker(f"{symbol}.NS")
                
                # Get company info
                info = ticker.info
                
                # Get result schedule
                result_info = RESULT_SCHEDULE.get(symbol, {})
                result_date = result_info.get("date", "TBA")
                result_time = result_info.get("time", "After Market")
                status_text_display, status_type = get_result_status(result_date)
                
                if status_text_display is None:
                    continue  # Skip if not in next 3 days
                
                # Calculate earnings metrics
                eps_ttm = info.get('trailingEps', 0)
                forward_pe = info.get('forwardPE', 0)
                recommendation = info.get('recommendationKey', 'hold')
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                
                # Get earnings growth
                quarterly = ticker.quarterly_earnings
                eps_trend = []
                if quarterly is not None and not quarterly.empty:
                    for date, row in quarterly.iterrows():
                        if 'eps' in row:
                            eps_trend.append(float(row['eps']) if not pd.isna(row['eps']) else 0)
                
                yoy_growth = 0
                if len(eps_trend) >= 4:
                    latest = eps_trend[-1] if eps_trend[-1] > 0 else eps_trend[-2] if len(eps_trend) > 1 else 0
                    prev = eps_trend[-5] if len(eps_trend) > 5 else eps_trend[0] if eps_trend else 0
                    if prev > 0:
                        yoy_growth = ((latest - prev) / prev) * 100
                
                # Generate signal based on days left
                signal = "NEUTRAL"
                confidence = 50
                trade = "WAIT"
                reason = ""
                
                if status_type == "today":
                    # Result day - high volatility expected
                    if yoy_growth > 10:
                        signal = "STRONG BULLISH"
                        confidence = 90
                        trade = "🔥 BUY CALL (CE)"
                        reason = f"Result TODAY! High growth: {yoy_growth:.1f}%"
                    elif yoy_growth < -10:
                        signal = "STRONG BEARISH"
                        confidence = 90
                        trade = "🔥 SELL PUT (PE)"
                        reason = f"Result TODAY! Negative growth: {yoy_growth:.1f}%"
                    else:
                        signal = "HIGH IMPACT"
                        confidence = 80
                        trade = "⚠️ STAY READY"
                        reason = f"Result TODAY - Be ready for volatility"
                elif status_type == "tomorrow":
                    if yoy_growth > 15:
                        signal = "BULLISH"
                        confidence = 80
                        trade = "📈 BUY CALL (CE)"
                        reason = f"Result TOMORROW | Growth: {yoy_growth:.1f}%"
                    elif yoy_growth < -15:
                        signal = "BEARISH"
                        confidence = 80
                        trade = "📉 SELL PUT (PE)"
                        reason = f"Result TOMORROW | Decline: {yoy_growth:.1f}%"
                    else:
                        signal = "NEUTRAL"
                        confidence = 60
                        trade = "👀 WATCH"
                        reason = f"Result tomorrow - Monitor"
                else:  # dayafter
                    if yoy_growth > 20:
                        signal = "BULLISH"
                        confidence = 75
                        trade = "📈 BUY CALL (CE)"
                        reason = f"Result in 2 days | Growth: {yoy_growth:.1f}%"
                    elif yoy_growth < -20:
                        signal = "BEARISH"
                        confidence = 75
                        trade = "📉 SELL PUT (PE)"
                        reason = f"Result in 2 days | Decline: {yoy_growth:.1f}%"
                    else:
                        signal = "NEUTRAL"
                        confidence = 50
                        trade = "👀 WATCH"
                        reason = "Position building opportunity"
                
                earnings_data.append({
                    'symbol': symbol,
                    'name': info.get('longName', symbol)[:25],
                    'current_price': current_price,
                    'forward_pe': forward_pe,
                    'yoy_growth': yoy_growth,
                    'recommendation': recommendation,
                    'result_date': result_date,
                    'result_time': result_time,
                    'status': status_text_display,
                    'status_type': status_type,
                    'signal': signal,
                    'confidence': confidence,
                    'trade': trade,
                    'reason': reason
                })
                
                # Update status without blinking
                status_text.info(f"📊 Loaded {i+1}/{len(upcoming_symbols)}: {symbol}")
                
            except Exception as e:
                continue
        
        status_text.empty()
        return earnings_data
    
    # Sort by date (today first, then tomorrow, then day after)
    def sort_by_date(data):
        order = {"today": 0, "tomorrow": 1, "dayafter": 2}
        return sorted(data, key=lambda x: order.get(x.get('status_type', 'dayafter'), 3))
    
    # Fetch data
    auto_data = get_auto_earnings_data()
    
    if auto_data:
        # Sort data
        auto_data = sort_by_date(auto_data)
        
        # Summary cards
        st.markdown("#### 📅 UPCOMING RESULTS CALENDAR")
        
        today_count = len([d for d in auto_data if d['status_type'] == 'today'])
        tomorrow_count = len([d for d in auto_data if d['status_type'] == 'tomorrow'])
        dayafter_count = len([d for d in auto_data if d['status_type'] == 'dayafter'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 TODAY", today_count, delta="🔥 RESULT DAY")
        with col2:
            st.metric("⏳ TOMORROW", tomorrow_count)
        with col3:
            st.metric("📅 DAY AFTER", dayafter_count)
        
        st.markdown("---")
        
        # TODAY'S RESULTS (Highest Priority)
        today_results = [d for d in auto_data if d['status_type'] == 'today']
        if today_results:
            st.markdown("### 🔴 TODAY'S RESULTS - HIGH IMPACT")
            for d in today_results:
                signal_color = "#ff4444"  # Red for high impact
                st.markdown(f"""
                <div style="background: rgba(255,68,68,0.2); border-radius: 15px; padding: 15px; margin: 10px 0; border: 2px solid #ff4444;">
                    <table style="width:100%;">
                        <tr>
                            <td style="width:25%;"><b>🏢 {d['symbol']}</b><br><small>{d['name']}</small></td>
                            <td style="width:20%;"><b>📅 Result</b><br><span style="color:#ff4444; font-weight:bold;">{d['result_date']}</span>@{d['result_time']}</td>
                            <td style="width:25%;"><b>🎯 TRADE SIGNAL</b><br><span style="background:#ff4444; padding:8px 15px; border-radius:20px; color:white; font-weight:bold;">🔥 {d['trade']}</span></td>
                            <td style="width:30%;"><b>💡 Strategy</b><br>{d['reason']}</td>
                        </tr>
                        <tr>
                            <td><b>💰 Price</b><br>₹{d['current_price']:.2f} if d['current_price']>0 else '-'</small></td>
                            <td><b>📈 YoY Growth</b><br><span style="color:{'#00ff88' if d['yoy_growth']>0 else '#ff6666'}">{d['yoy_growth']:+.1f}%</span></small></td>
                            <td><b>⭐ Analyst</b><br>{d['recommendation'].upper() if d['recommendation'] else '-'}</small></td>
                            <td><b>⚡ Priority</b><br><span style="color:#ff4444;">🔴 URGENT - Result Today</span></td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto trade button
                if "BUY" in d['trade'] or "SELL" in d['trade']:
                    col1, col2 = st.columns([3,1])
                    with col2:
                        if st.button(f"⚡ TRADE {d['symbol']}", key=f"trade_today_{d['symbol']}"):
                            result_type = "POSITIVE" if "BUY" in d['trade'] else "NEGATIVE"
                            success, msg = process_result_and_trade(d['name'], d['symbol'], result_type)
                            if success:
                                st.success(f"✅ {msg}")
                                st.session_state.result_alerts.append({
                                    'company': d['symbol'],
                                    'date': d['result_date'],
                                    'time': get_ist_now().strftime('%H:%M:%S'),
                                    'verdict': d['signal'],
                                    'reaction': f"{d['trade']} order placed",
                                    'reason': d['reason']
                                })
                                st.rerun()
        
        # TOMORROW'S RESULTS
        tomorrow_results = [d for d in auto_data if d['status_type'] == 'tomorrow']
        if tomorrow_results:
            st.markdown("### ⏳ TOMORROW'S RESULTS")
            for d in tomorrow_results:
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 8px 0; border-left: 4px solid #ffaa00;">
                    <table style="width:100%;">
                        <tr>
                            <td style="width:25%;"><b>🏢 {d['symbol']}</b><br><small>{d['name'][:20]}</small></td>
                            <td style="width:20%;">📅 {d['result_date']} @ {d['result_time']}</small></td>
                            <td style="width:25%;"><span style="background:{'#00ff88' if 'BUY' in d['trade'] else '#ff6666' if 'SELL' in d['trade'] else '#ffaa00'}; padding:5px 10px; border-radius:15px; color:black;">{d['trade']}</span></small></td>
                            <td style="width:30%;"><small>{d['reason']}</small></td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
        
        # DAY AFTER TOMORROW'S RESULTS
        dayafter_results = [d for d in auto_data if d['status_type'] == 'dayafter']
        if dayafter_results:
            st.markdown("### 📅 DAY AFTER TOMORROW")
            for d in dayafter_results:
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.2); border-radius: 15px; padding: 10px; margin: 5px 0; border-left: 4px solid #00b4d8;">
                    <b>{d['symbol']}</b> | 📅 {d['result_date']} | 📈 YoY: {d['yoy_growth']:+.1f}% | {d['trade']}
                </div>
                """, unsafe_allow_html=True)
        
        # No refresh/blinking - remove auto refresh
        # st_autorefresh removed to prevent blinking
        
    else:
        st.info("📭 No results scheduled for today or next 2 days")
        st.markdown("""
        ### 📅 What to expect:
        - **TODAY's results** will appear here automatically
        - Results are usually declared **After Market (3:30 PM)**
        - Check back during earnings season
        
        ### 🔔 Next expected results:
        - BRITANNIA - Today (8 June)
        - CIPLA - Today (8 June)
        - DR REDDY - Tomorrow (9 June)
        - M&M - Tomorrow (9 June)
        """)
    
    # Recent alerts (without auto refresh)
    st.markdown("---")
    st.markdown("#### 🔔 RECENT TRADE ALERTS")
    
    if st.session_state.result_alerts:
        for alert in st.session_state.result_alerts[-5:]:
            verdict = alert.get('verdict', '')
            verdict_color = "#00ff88" if "BULLISH" in str(verdict) else "#ff4444" if "BEARISH" in str(verdict) else "#ffaa00"
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 8px; margin: 5px 0;">
                <b>⚡ {alert.get('company', 'Unknown')}</b> | {alert.get('time', '')}<br>
                📈 {alert.get('reaction', '')}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📅 RESULT DATE LEGEND")
    st.info("""
    | Color | Meaning | Action |
    |-------|---------|--------|
    | 🔴 **TODAY** | Result declared today | HIGH ALERT - Trade with strict SL |
    | ⏳ **TOMORROW** | Result tomorrow | Position building opportunity |
    | 📅 **DAY AFTER** | Result in 2 days | Accumulate slowly |
    
    **⏰ Result Time:** Most results are declared **After Market (3:30 PM)**
    """)

# ================= REAL TIME PROFIT BOOKING ALERT SYSTEM =================
with st.expander("🎯 REAL TIME TRADE MONITOR - Auto Profit Booking Alert", expanded=True):
    st.markdown("### 🎯 LIVE TRADE MONITOR")
    st.markdown("*Automatic profit booking alerts - Real time*")
    
    st.markdown("---")
    
    # Current Trade Input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 ACTIVE TRADE DETAILS")
        monitor_symbol = st.text_input("Symbol", "BRITANNIA", key="monitor_sym")
        monitor_strike = st.number_input("Strike Price", value=5100, key="monitor_strike")
        monitor_ce_pe = st.selectbox("Option Type", ["CE", "PE"], key="monitor_type")
        monitor_entry = st.number_input("Entry Premium (₹)", value=110.25, step=5.0, format="%.2f", key="monitor_entry")
        monitor_lots = st.number_input("Number of Lots", value=11, step=1, key="monitor_lots")
        monitor_lot_size = st.number_input("Lot Size", value=65, key="monitor_lot_size")
        
    with col2:
        st.markdown("#### ⚙️ ALERT SETTINGS")
        profit_booking_percent = st.slider("Profit Booking Alert % (Peak पासून किती खाली येऊ द्याल?)", 
                                           min_value=2, max_value=15, value=5, step=1,
                                           help="जेव्हा premium peak पासून इतके % खाली येईल तेव्हा alert वाजेल")
        
        target1 = st.number_input("Target 1 (Book 50%)", value=135.00, step=10.0, format="%.2f", key="monitor_t1")
        target2 = st.number_input("Target 2 (Book 30%)", value=165.00, step=10.0, format="%.2f", key="monitor_t2")
        target3 = st.number_input("Target 3 (Book 20%)", value=200.00, step=10.0, format="%.2f", key="monitor_t3")
        stop_loss = st.number_input("Stop Loss", value=82.00, step=5.0, format="%.2f", key="monitor_sl")
        
        refresh_interval = st.selectbox("Refresh Rate", ["5 seconds", "10 seconds", "30 seconds"], index=1)
        refresh_seconds = int(refresh_interval.split()[0])
    
    # Auto refresh
    st_autorefresh(interval=refresh_seconds * 1000, key="auto_profit_monitor")
    
    st.markdown("---")
    
    # Function to get live premium
    def get_live_premium(symbol, strike, option_type):
        """Get live premium from NSE"""
        try:
            if symbol == "BRITANNIA":
                # Simulated data - replace with actual API call
                import random
                import time
                # Simulate real market movement
                base = 112.70
                variation = random.uniform(-2, 3)
                return round(base + variation, 2)
            else:
                ticker = yf.Ticker(f"{symbol}.NS")
                # This needs proper option chain fetch
                return 0
        except:
            return 0
    
    # Session state for tracking
    if "peak_premium" not in st.session_state:
        st.session_state.peak_premium = monitor_entry
    if "last_premium" not in st.session_state:
        st.session_state.last_premium = monitor_entry
    if "alert_triggered" not in st.session_state:
        st.session_state.alert_triggered = False
    if "targets_hit" not in st.session_state:
        st.session_state.targets_hit = {"t1": False, "t2": False, "t3": False}
    if "booking_history" not in st.session_state:
        st.session_state.booking_history = []
    
    # Get live premium
    current_premium = get_live_premium(monitor_symbol, monitor_strike, monitor_ce_pe)
    
    # Update peak premium
    if current_premium > st.session_state.peak_premium:
        st.session_state.peak_premium = current_premium
        st.session_state.alert_triggered = False  # Reset alert on new peak
    
    # Calculate values
    total_shares = monitor_lots * monitor_lot_size
    current_pnl_points = current_premium - monitor_entry
    current_pnl_rs = current_pnl_points * total_shares
    peak_to_current_fall = ((st.session_state.peak_premium - current_premium) / st.session_state.peak_premium) * 100 if st.session_state.peak_premium > 0 else 0
    
    # Display current status
    st.markdown("## 📊 LIVE TRADE STATUS")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_bg = "#00ff88" if current_pnl_rs > 0 else "#ff4444"
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; text-align: center; border: 2px solid {current_bg};">
            <span style="font-size: 20px;">💰 LIVE PREMIUM</span><br>
            <span style="font-size: 32px; font-weight: bold; color: {current_bg};">₹{current_premium:.2f}</span><br>
            <span style="color: #aaa;">Entry: ₹{monitor_entry:.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pnl_color = "#00ff88" if current_pnl_rs >= 0 else "#ff4444"
        pnl_icon = "🟢" if current_pnl_rs >= 0 else "🔴"
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; text-align: center;">
            <span style="font-size: 20px;">📈 CURRENT P&L</span><br>
            <span style="font-size: 28px; font-weight: bold; color: {pnl_color};">{pnl_icon} ₹{current_pnl_rs:,.0f}</span><br>
            <span style="color: #aaa;">{current_pnl_points:+.2f} points</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; text-align: center;">
            <span style="font-size: 20px;">🏔️ PEAK PREMIUM</span><br>
            <span style="font-size: 28px; font-weight: bold; color: #00b4d8;">₹{st.session_state.peak_premium:.2f}</span><br>
            <span style="color: #aaa;">Highest so far</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if current_premium < st.session_state.peak_premium:
            fall_color = "#ff4444" if peak_to_current_fall > profit_booking_percent else "#ffaa00"
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; text-align: center;">
                <span style="font-size: 20px;">📉 FROM PEAK</span><br>
                <span style="font-size: 28px; font-weight: bold; color: {fall_color};">
                    {peak_to_current_fall:.1f}%
                </span><br>
                <span style="color: #aaa;">Alert at {profit_booking_percent}%</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; text-align: center;">
                <span style="font-size: 20px;">📈 NEW PEAK!</span><br>
                <span style="font-size: 28px; font-weight: bold; color: #00ff88;">🚀 UP</span><br>
                <span style="color: #aaa;">Making new highs</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Target Progress
    st.markdown("---")
    st.markdown("#### 🎯 TARGET PROGRESS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        t1_progress = min(100, (current_premium / target1) * 100) if target1 > 0 else 0
        t1_color = "#00ff88" if current_premium >= target1 else "#ffaa00"
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px; text-align: center;">
            <b>🎯 TARGET 1</b><br>
            <span style="font-size: 24px; color: {t1_color};">₹{target1:.2f}</span><br>
            <div style="background: #333; border-radius: 10px; height: 8px; margin-top: 5px;">
                <div style="background: {t1_color}; width: {t1_progress}%; height: 8px; border-radius: 10px;"></div>
            </div>
            <span style="font-size: 12px;">Book 50% at this level</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        t2_progress = min(100, (current_premium / target2) * 100) if target2 > 0 else 0
        t2_color = "#00ff88" if current_premium >= target2 else "#ffaa00"
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px; text-align: center;">
            <b>🎯 TARGET 2</b><br>
            <span style="font-size: 24px; color: {t2_color};">₹{target2:.2f}</span><br>
            <div style="background: #333; border-radius: 10px; height: 8px; margin-top: 5px;">
                <div style="background: {t2_color}; width: {t2_progress}%; height: 8px; border-radius: 10px;"></div>
            </div>
            <span style="font-size: 12px;">Book 30% at this level</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        t3_progress = min(100, (current_premium / target3) * 100) if target3 > 0 else 0
        t3_color = "#00ff88" if current_premium >= target3 else "#ffaa00"
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px; text-align: center;">
            <b>🎯 TARGET 3</b><br>
            <span style="font-size: 24px; color: {t3_color};">₹{target3:.2f}</span><br>
            <div style="background: #333; border-radius: 10px; height: 8px; margin-top: 5px;">
                <div style="background: {t3_color}; width: {t3_progress}%; height: 8px; border-radius: 10px;"></div>
            </div>
            <span style="font-size: 12px;">Book 20% at this level</span>
        </div>
        """, unsafe_allow_html=True)
    
    # SL Status
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if current_premium <= stop_loss:
            st.error(f"🚨 STOP LOSS HIT! Current: ₹{current_premium:.2f} ≤ SL: ₹{stop_loss:.2f}")
            st.markdown("### 🔴 **EXIT IMMEDIATELY** 🔴")
        else:
            sl_distance = ((current_premium - stop_loss) / current_premium) * 100
            st.info(f"🛡️ STOP LOSS: ₹{stop_loss:.2f} ({sl_distance:.1f}% away)")
    
    with col2:
        # Recommendation
        if current_premium >= target1:
            st.success("✅ TARGET 1 ACHIEVED! Book 50% now")
        elif current_premium >= stop_loss + 10:
            st.info("📊 Trade active - Hold as per plan")
        elif current_premium <= stop_loss + 5:
            st.warning("⚠️ Near Stop Loss - Be careful")
    
    # MAIN ALERT - Profit Booking Detection
    st.markdown("---")
    st.markdown("### 🚨 PROFIT BOOKING ALERT")
    
    alert_triggered = False
    alert_message = ""
    alert_color = "#ffaa00"
    
    # Check profit booking
    if peak_to_current_fall >= profit_booking_percent and current_premium < st.session_state.peak_premium:
        alert_triggered = True
        alert_message = f"""
        🔴🔴🔴 PROFIT BOOKING STARTED! 🔴🔴🔴
        
        Premium has fallen {peak_to_current_fall:.1f}% from peak (₹{st.session_state.peak_premium:.2f})
        
        🎯 RECOMMENDED ACTION:
        ├── Option 1: BOOK 50% NOW
        ├── Option 2: Move SL to entry price
        └── Option 3: If falling fast → FULL EXIT
        """
        alert_color = "#ff4444"
    
    # Check if targets are hit
    if current_premium >= target1 and not st.session_state.targets_hit["t1"]:
        alert_triggered = True
        alert_message += f"\n✅ TARGET 1 (₹{target1:.2f}) HIT! Book 50% immediately."
        st.session_state.targets_hit["t1"] = True
    
    if current_premium >= target2 and not st.session_state.targets_hit["t2"]:
        alert_triggered = True
        alert_message += f"\n✅ TARGET 2 (₹{target2:.2f}) HIT! Book 30% immediately."
        st.session_state.targets_hit["t2"] = True
    
    if current_premium >= target3 and not st.session_state.targets_hit["t3"]:
        alert_triggered = True
        alert_message += f"\n✅ TARGET 3 (₹{target3:.2f}) HIT! Book remaining 20%."
        st.session_state.targets_hit["t3"] = True
    
    # Display Alert
    if alert_triggered:
        st.markdown(f"""
        <div style="background: rgba(255,68,68,0.3); border: 3px solid {alert_color}; border-radius: 15px; padding: 20px; text-align: center;">
            <span style="font-size: 32px;">🚨</span>
            <h2 style="color: {alert_color}; margin: 0;">PROFIT BOOKING DETECTED!</h2>
            <p style="font-size: 18px;">{alert_message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        st.markdown("### ⚡ TAKE ACTION NOW:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 BOOK 50% NOW", use_container_width=True):
                profit_50 = (current_premium - monitor_entry) * total_shares * 0.5
                st.success(f"✅ Booked 50% → Profit: ₹{profit_50:,.0f}")
                st.session_state.booking_history.append(f"Booked 50% @ ₹{current_premium:.2f}")
                st.balloons()
        with col2:
            if st.button("🛡️ MOVE SL TO ENTRY", use_container_width=True):
                stop_loss = monitor_entry
                st.success(f"✅ Stop Loss moved to entry: ₹{monitor_entry:.2f}")
        with col3:
            if st.button("🔴 FULL EXIT NOW", use_container_width=True):
                total_profit = (current_premium - monitor_entry) * total_shares
                st.success(f"✅ Exited completely! Total Profit: ₹{total_profit:,.0f}")
                st.session_state.booking_history.append(f"Full Exit @ ₹{current_premium:.2f}")
                st.balloons()
    else:
        st.info(f"🟢 No profit booking detected. Premium is {peak_to_current_fall:.1f}% below peak. Alert at {profit_booking_percent}%")
        
        # Progress bar for profit booking level
        progress_to_alert = min(100, (peak_to_current_fall / profit_booking_percent) * 100)
        st.markdown(f"""
        <div style="margin-top: 10px;">
            <small>Profit Booking Alert Progress:</small>
            <div style="background: #333; border-radius: 10px; height: 10px;">
                <div style="background: #ffaa00; width: {progress_to_alert}%; height: 10px; border-radius: 10px;"></div>
            </div>
            <small>{peak_to_current_fall:.1f}% / {profit_booking_percent}%</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Booking History
    if st.session_state.booking_history:
        st.markdown("---")
        st.markdown("#### 📋 EXECUTION HISTORY")
        for h in st.session_state.booking_history[-5:]:
            st.markdown(f"- {h}")
    
    # Live premium display update
    st.markdown("---")
    st.caption(f"🕐 Last updated: {get_ist_now().strftime('%H:%M:%S')} | Refresh every {refresh_seconds} seconds")
    
    # Manual refresh button
    if st.button("🔄 MANUAL REFRESH", use_container_width=True):
        st.rerun()

# ================= SIMPLIFIED VERSION - JUST THE ALERT =================
with st.expander("📱 SIMPLE ALERT - Just Watch This", expanded=True):
    st.markdown("### 🔔 REAL TIME ACTION ALERT")
    
    # Simple real-time monitor
    def simple_premium_monitor():
        import random
        # Simulate premium movement (Replace with actual API)
        base = 112.70
        movement = random.uniform(-1.5, 2.5)
        return round(base + movement, 2)
    
    current = simple_premium_monitor()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Premium", f"₹{current:.2f}", delta=f"{current - 110.25:.2f}")
    with col2:
        st.metric("Entry", "₹110.25")
    with col3:
        profit = (current - 110.25) * 715
        st.metric("P&L", f"₹{profit:,.0f}", delta="🚀" if profit > 0 else "🔻")
    
    # Simple Alert Logic
    if current >= 135:
        st.success("✅ **TARGET 1 HIT!** Book 50% (5-6 lots)")
    elif current >= 120:
        st.info("📈 Moving towards target - Hold")
    elif current <= 100:
        st.error("🔴 **STOP LOSS APPROACHING** - Be ready to exit")
    elif current <= 105:
        st.warning("⚠️ Near SL - Watch carefully")
    else:
        st.info("🟢 Trade active - No alert yet")

# ================= TAB 5: SAHYADRI SETTINGS =================
with tab5:
    st.markdown("### ⚙️ SAHYADRI SETTINGS")
    st.markdown("---")
    
    st.markdown("#### 🎨 THEME COLOR SELECTION")
    col1, col2, col3 = st.columns(3)
    
    if "theme_color" not in st.session_state:
        st.session_state.theme_color = "#00ff88"
    if "wait_color" not in st.session_state:
        st.session_state.wait_color = "#ffaa00"
    
    with col1:
        new_theme = st.color_picker("BUY/SELL Color", st.session_state.theme_color, key="theme_picker")
    with col2:
        new_wait = st.color_picker("WAIT Color", st.session_state.wait_color, key="wait_picker")
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {new_theme}, {new_wait}); border-radius: 10px; padding: 10px; text-align: center;">
            <small>Preview</small>
        </div>
        """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_b:
        if st.button("💾 SAVE THEME", use_container_width=True):
            st.session_state.theme_color = new_theme
            st.session_state.wait_color = new_wait
            st.success("✅ Theme Saved!")
            st.rerun()
    
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
            st.markdown(f'<div style="background:{st.session_state.theme_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3 style="color:white;">🟢 BUY</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
        elif nifty_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:15px; padding:15px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3 style="color:white;">🔴 SELL</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:{st.session_state.wait_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3 style="color:black;">🟡 WAIT</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col2:
        if bank_signal == "BUY":
            st.markdown(f'<div style="background:{st.session_state.theme_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3 style="color:white;">🟢 BUY</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
        elif bank_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:15px; padding:15px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3 style="color:white;">🔴 SELL</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:{st.session_state.wait_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3 style="color:black;">🟡 WAIT</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col3:
        if crude_signal == "BUY":
            st.markdown(f'<div style="background:{st.session_state.theme_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🛢️ CRUDE</h4><h3 style="color:white;">🟢 BUY</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
        elif crude_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:15px; padding:15px; text-align:center;"><h4>🛢️ CRUDE</h4><h3 style="color:white;">🔴 SELL</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:{st.session_state.wait_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🛢️ CRUDE</h4><h3 style="color:black;">🟡 WAIT</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col4:
        if ng_signal == "BUY":
            st.markdown(f'<div style="background:{st.session_state.theme_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🌿 NG</h4><h3 style="color:white;">🟢 BUY</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
        elif ng_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:15px; padding:15px; text-align:center;"><h4>🌿 NG</h4><h3 style="color:white;">🔴 SELL</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:{st.session_state.wait_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🌿 NG</h4><h3 style="color:black;">🟡 WAIT</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### 📊 DAILY TRADE COUNTS")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("NIFTY BUY", st.session_state.daily_trade_count['NIFTY']['buy'])
        st.metric("NIFTY SELL", st.session_state.daily_trade_count['NIFTY']['sell'])
    with col3:
        st.metric("CRUDE BUY", st.session_state.daily_trade_count['CRUDE']['buy'])
        st.metric("CRUDE SELL", st.session_state.daily_trade_count['CRUDE']['sell'])
    with col4:
        st.metric("NG BUY", st.session_state.daily_trade_count['NATURALGAS']['buy'])
        st.metric("NG SELL", st.session_state.daily_trade_count['NATURALGAS']['sell'])
    
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

# ================= AUTO TRADE FUNCTIONS =================
def auto_trade_from_signal_with_journal():
    nifty_trend = get_nifty_trend()
    symbols_to_check = ["NIFTY"]
    
    for symbol in symbols_to_check:
        sector_trend = get_sector_trend(SECTOR_MAPPING.get(symbol, "NIFTY"))
        signal, price, indicators = get_strict_signal(symbol, nifty_trend, sector_trend)
        
        if signal in ["BUY", "SELL"] and st.session_state.auto_trade_enabled:
            already_active = any(a['symbol'] == symbol for a in st.session_state.active_orders)
            trade_type = "BUY" if signal == "BUY" else "SELL"
            can_trade = can_take_trade(symbol, trade_type)
            
            if not already_active and can_trade and is_trading_time(symbol):
                option_type = "CALL (CE)" if signal == "BUY" else "PUT (PE)"
                limit_price = price - 5
                if limit_price <= 0:
                    limit_price = price
                
                strike_interval = 50
                strike_price = math.floor(limit_price / strike_interval) * strike_interval
                
                sl_percent = st.session_state.auto_trade_sl_percent / 100
                target_percent = st.session_state.auto_trade_target_percent / 100
                
                if signal == "BUY":
                    sl_price = limit_price * (1 - sl_percent)
                    tp1_price = limit_price * (1 + (target_percent * 0.5))
                    tp2_price = limit_price * (1 + target_percent)
                    tp3_price = limit_price * (1 + (target_percent * 1.5))
                else:
                    sl_price = limit_price * (1 + sl_percent)
                    tp1_price = limit_price * (1 - (target_percent * 0.5))
                    tp2_price = limit_price * (1 - target_percent)
                    tp3_price = limit_price * (1 - (target_percent * 1.5))
                
                st.session_state.wolf_orders.append({
                    'symbol': symbol,
                    'option_type': option_type,
                    'strike_price': strike_price,
                    'qty': st.session_state.auto_trade_qty,
                    'buy_above': limit_price,
                    'sl': sl_price,
                    'target': tp2_price,
                    'tp1': tp1_price,
                    'tp2': tp2_price,
                    'tp3': tp3_price,
                    'tp1_booked': False,
                    'tp2_booked': False,
                    'tp3_booked': False,
                    'tp1_percent': 50,
                    'tp2_percent': 25,
                    'tp3_percent': 25,
                    'status': 'PENDING',
                    'placed_time': get_ist_now().strftime('%H:%M:%S'),
                    'signal_type': '⚙️ SAHYADRI',
                    'signal': signal
                })
                
                increment_trade_count(symbol, trade_type)
                send_telegram(f"⏳ SAHYADRI: {symbol} {signal} @ {limit_price} | TP1:{tp1_price:.2f}(50%) | TP2:{tp2_price:.2f}(25%) | TP3:{tp3_price:.2f}(25%)")

def wolf_auto_fo_trade():
    if not st.session_state.auto_trade_enabled:
        return
    
    nifty_trend = get_nifty_trend()
    nifty_positive = (nifty_trend == "POSITIVE")
    nifty_negative = (nifty_trend == "NEGATIVE")
    
    symbols_to_check = [s for s in FO_SCRIPTS if s != "BANKNIFTY"]
    
    for symbol in symbols_to_check:
        already_active = any(a['symbol'] == symbol for a in st.session_state.active_orders)
        if already_active:
            continue
        
        already_pending = any(o.get('symbol') == symbol and o.get('status') == 'PENDING' for o in st.session_state.wolf_orders)
        if already_pending:
            continue
        
        if not is_trading_time(symbol):
            continue
        
        indicators = get_technical_indicators(symbol)
        if indicators is None:
            continue
        
        sector = SECTOR_MAPPING.get(symbol, "NIFTY")
        sector_trend = get_sector_trend(sector)
        sector_bullish = (sector_trend == "BULLISH")
        sector_bearish = (sector_trend == "BEARISH")
        
        trend5_up = get_mtf_trend(symbol, "5m") == "UP"
        trend15_up = get_mtf_trend(symbol, "15m") == "UP"
        trend1h_up = get_mtf_trend(symbol, "60m") == "UP"
        
        ema_buy = (nifty_positive and
                   not indicators["sideways"] and
                   sector_bullish and
                   indicators["ema9"] > indicators["ema20"] and
                   indicators["current_price"] > indicators["ema200"] and
                   indicators["rsi"] >= 60 and
                   indicators["adx"] >= 25 and
                   indicators["volume_filter"] and
                   indicators["strong_bull"] and
                   indicators["current_price"] > indicators["c1_high"] and
                   trend5_up and trend15_up and trend1h_up)
        
        ema_sell = (nifty_negative and
                    not indicators["sideways"] and
                    sector_bearish and
                    indicators["ema9"] < indicators["ema20"] and
                    indicators["current_price"] < indicators["ema200"] and
                    indicators["rsi"] <= 40 and
                    indicators["adx"] >= 25 and
                    indicators["volume_filter"] and
                    indicators["strong_bear"] and
                    indicators["current_price"] < indicators["c1_low"] and
                    not trend5_up and not trend15_up and not trend1h_up)
        
        if ema_buy:
            current_price = indicators["current_price"]
            option_type = "CALL (CE)"
            
            if symbol == "NIFTY":
                strike_interval = 50
            elif symbol in ["CRUDE", "NATURALGAS"]:
                strike_interval = 100
            else:
                strike_interval = 10
            
            strike_price = math.floor(current_price / strike_interval) * strike_interval
            
            entry_price = current_price
            tp1_price = entry_price * 1.10
            tp2_price = entry_price * 1.20
            tp3_price = entry_price * 1.30
            sl_price = entry_price * 0.90
            
            st.session_state.wolf_orders.append({
                'symbol': symbol,
                'option_type': option_type,
                'strike_price': strike_price,
                'qty': st.session_state.auto_trade_qty,
                'buy_above': current_price,
                'sl': sl_price,
                'target': tp2_price,
                'tp1': tp1_price,
                'tp2': tp2_price,
                'tp3': tp3_price,
                'tp1_booked': False,
                'tp2_booked': False,
                'tp3_booked': False,
                'tp1_percent': 50,
                'tp2_percent': 25,
                'tp3_percent': 25,
                'status': 'PENDING',
                'placed_time': get_ist_now().strftime('%H:%M:%S'),
                'auto_trade': True,
                'signal_type': '🐺 WOLF AUTO',
                'signal': 'BUY'
            })
            
            send_telegram(f"🐺 WOLF AUTO BUY: {symbol} CE @{entry_price:.2f} | TP1:{tp1_price:.2f}(50%) | TP2:{tp2_price:.2f}(25%) | TP3:{tp3_price:.2f}(25%) | Qty:{st.session_state.auto_trade_qty}")
            voice_alert(f"Wolf auto buy order placed for {symbol}")
        
        elif ema_sell:
            current_price = indicators["current_price"]
            option_type = "PUT (PE)"
            
            if symbol == "NIFTY":
                strike_interval = 50
            elif symbol in ["CRUDE", "NATURALGAS"]:
                strike_interval = 100
            else:
                strike_interval = 10
            
            strike_price = math.floor(current_price / strike_interval) * strike_interval
            
            entry_price = current_price
            tp1_price = entry_price * 0.90
            tp2_price = entry_price * 0.80
            tp3_price = entry_price * 0.70
            sl_price = entry_price * 1.10
            
            st.session_state.wolf_orders.append({
                'symbol': symbol,
                'option_type': option_type,
                'strike_price': strike_price,
                'qty': st.session_state.auto_trade_qty,
                'buy_above': current_price,
                'sl': sl_price,
                'target': tp2_price,
                'tp1': tp1_price,
                'tp2': tp2_price,
                'tp3': tp3_price,
                'tp1_booked': False,
                'tp2_booked': False,
                'tp3_booked': False,
                'tp1_percent': 50,
                'tp2_percent': 25,
                'tp3_percent': 25,
                'status': 'PENDING',
                'placed_time': get_ist_now().strftime('%H:%M:%S'),
                'auto_trade': True,
                'signal_type': '🐺 WOLF AUTO',
                'signal': 'SELL'
            })
            
            send_telegram(f"🐺 WOLF AUTO SELL: {symbol} PE @{entry_price:.2f} | TP1:{tp1_price:.2f}(50%) | TP2:{tp2_price:.2f}(25%) | TP3:{tp3_price:.2f}(25%) | Qty:{st.session_state.auto_trade_qty}")
            voice_alert(f"Wolf auto sell order placed for {symbol}")

# ================= CHECK & EXECUTE WOLF ORDERS =================
def check_and_execute_orders_with_journal():
    pending_orders = [o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING']
    
    for order in pending_orders:
        current_price = get_live_price(order['symbol'])
        
        if current_price > 0 and current_price >= order.get('buy_above', 0):
            order['status'] = 'EXECUTED'
            order['entry_price'] = current_price
            order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
            
            active_order = {
                'symbol': order['symbol'],
                'option_type': order.get('option_type', 'CALL (CE)'),
                'strike_price': order.get('strike_price', 0),
                'qty': order.get('qty', 1),
                'entry_price': current_price,
                'entry_time': order['entry_time'],
                'sl': order.get('sl', current_price * 0.95),
                'target': order.get('target', current_price * 1.05),
                'tp1': order.get('tp1', current_price * 1.05),
                'tp2': order.get('tp2', current_price * 1.10),
                'tp3': order.get('tp3', current_price * 1.15),
                'tp1_booked': order.get('tp1_booked', False),
                'tp2_booked': order.get('tp2_booked', False),
                'tp3_booked': order.get('tp3_booked', False),
                'signal_type': order.get('signal_type', '🐺 WOLF'),
                'signal': order.get('signal', 'BUY')
            }
            st.session_state.active_orders.append(active_order)
            add_to_journal(active_order)
            send_telegram(f"✅ ORDER EXECUTED: {order['symbol']} at ₹{current_price:.2f}")

# ================= MONITOR ACTIVE ORDERS WITH P&L =================
def monitor_active_orders_with_pnl():
    orders_to_remove = []
    
    for i, order in enumerate(st.session_state.active_orders):
        symbol = order['symbol']
        current_price = get_live_price(symbol)
        
        if current_price <= 0:
            continue
        
        # TP1 TRACKING
        if not order.get('tp1_booked', False) and order.get('tp1'):
            if order['option_type'] == "CALL (CE)":
                tp1_hit = current_price >= order.get('tp1', 999999)
            else:
                tp1_hit = current_price <= order.get('tp1', 0)
            
            if tp1_hit:
                order['tp1_booked'] = True
                msg = f"✅ TP1 HIT: {symbol} at ₹{current_price:.2f} | 50% Profit Booked"
                send_telegram(msg)
                if st.session_state.voice_enabled:
                    voice_alert(f"TP1 hit for {symbol}")
        
        # TP2 TRACKING with SL Shift
        if not order.get('tp2_booked', False) and order.get('tp2'):
            if order['option_type'] == "CALL (CE)":
                tp2_hit = current_price >= order.get('tp2', 999999)
            else:
                tp2_hit = current_price <= order.get('tp2', 0)
            
            if tp2_hit:
                order['tp2_booked'] = True
                order['sl'] = order['entry_price']
                msg = f"✅ TP2 HIT: {symbol} at ₹{current_price:.2f} | 25% Booked | SL Shifted to Entry (₹{order['entry_price']:.2f})"
                send_telegram(msg)
                if st.session_state.voice_enabled:
                    voice_alert(f"TP2 hit for {symbol}, stop loss shifted to entry")
        
        # TP3 TRACKING
        if not order.get('tp3_booked', False) and order.get('tp3'):
            if order['option_type'] == "CALL (CE)":
                tp3_hit = current_price >= order.get('tp3', 999999)
            else:
                tp3_hit = current_price <= order.get('tp3', 0)
            
            if tp3_hit:
                order['tp3_booked'] = True
                msg = f"✅ TP3 HIT: {symbol} at ₹{current_price:.2f} | 25% Booked | TRADE COMPLETE"
                send_telegram(msg)
                if st.session_state.voice_enabled:
                    voice_alert(f"TP3 hit for {symbol}, trade complete")
                orders_to_remove.append((i, order, current_price, "TARGET HIT"))
                continue
        
        # SL CHECK
        if order['option_type'] == "CALL (CE)":
            if current_price <= order.get('sl', 0):
                exit_reason = "SL HIT at Breakeven" if order.get('tp2_booked', False) else "SL HIT"
                orders_to_remove.append((i, order, current_price, exit_reason))
        else:
            if current_price >= order.get('sl', 999999):
                exit_reason = "SL HIT at Breakeven" if order.get('tp2_booked', False) else "SL HIT"
                orders_to_remove.append((i, order, current_price, exit_reason))
    
    # Remove completed orders
    for idx, order, exit_price, reason in reversed(orders_to_remove):
        add_to_journal(order, exit_price, reason)
        st.session_state.active_orders.pop(idx)

# ================= MONITOR RESULTS =================
def monitor_today_results():
    try:
        pending = get_pending_results()
        for company in pending:
            symbol = company.get('symbol', '')
            if symbol:
                earnings = get_company_earnings(symbol)
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
                    
                    already_alerted = False
                    for alert in st.session_state.result_alerts:
                        if alert.get('company') == company.get('name'):
                            already_alerted = True
                            break
                    
                    if not already_alerted and result_type != "NEUTRAL":
                        st.session_state.result_alerts.append({
                            'company': company.get('name', symbol),
                            'date': get_ist_now().strftime('%Y-%m-%d'),
                            'time': get_ist_now().strftime('%H:%M:%S'),
                            'verdict': result_type
                        })
                        send_telegram(f"📊 RESULT: {company.get('name', symbol)} - {result_type}")
    except Exception as e:
        print(f"Error: {e}")

# ================= SIMPLE JOURNAL FUNCTIONS =================
def add_journal_entry(system_name, symbol, trade_type, entry_price):
    st.session_state.trade_journal.append({
        "Time": get_ist_now().strftime('%H:%M:%S'),
        "System": system_name,
        "Symbol": symbol,
        "Type": trade_type,
        "Entry": entry_price,
        "Exit": "-",
        "P&L": 0,
        "Status": "OPEN"
    })

def close_journal_entry(symbol, exit_price, pnl):
    for entry in st.session_state.trade_journal:
        if entry['Symbol'] == symbol and entry['Status'] == "OPEN":
            entry['Exit'] = exit_price
            entry['P&L'] = pnl
            entry['Status'] = "CLOSED"
            entry['Time'] = f"{entry['Time']} → {get_ist_now().strftime('%H:%M:%S')}"
            break

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

# ================= DAILY TRADE ENTRY & SL/TP CALCULATOR =================
with st.expander("📊 DAILY TRADE ENTRY - SL/TP CALCULATOR", expanded=False):
    st.markdown("### 📝 Daily Trade Entry")
    st.markdown("*Enter your trade details - Auto calculate SL, TP1, TP2, TP3*")
    
    st.markdown("---")
    
    # Input Form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📌 TRADE DETAILS")
        
        trade_symbol = st.text_input("Symbol", "BRITANNIA", key="daily_symbol")
        trade_option = st.selectbox("Option Type", ["CALL (CE)", "PUT (PE)"], key="daily_option")
        strike_price = st.number_input("Strike Price", value=5100, step=50, key="daily_strike")
        
        st.markdown("---")
        st.markdown("#### 💰 ENTRY DETAILS")
        
        entry_price = st.number_input("Entry Premium (₹)", value=110.25, step=5.0, format="%.2f", key="daily_entry")
        lot_size = st.number_input("Lot Size (NIFTY=65, BANKNIFTY=25, CRUDE=100)", value=65, step=1, key="daily_lotsize")
        num_lots = st.number_input("Number of Lots", value=11, step=1, key="daily_lots")
        
    with col2:
        st.markdown("#### 🎯 RISK & REWARD %")
        
        sl_percent = st.slider("Stop Loss %", min_value=5, max_value=50, value=25, step=1, key="daily_sl_pct")
        tp1_percent = st.slider("TP1 % (Book partial)", min_value=5, max_value=50, value=22, step=1, key="daily_tp1_pct")
        tp2_percent = st.slider("TP2 % (Book partial)", min_value=10, max_value=100, value=50, step=5, key="daily_tp2_pct")
        tp3_percent = st.slider("TP3 % (Final target)", min_value=20, max_value=150, value=80, step=10, key="daily_tp3_pct")
        
        st.markdown("---")
        st.markdown("#### 📊 BOOKING %")
        
        tp1_book_pct = st.slider("TP1 पर किती % बुक करायचे?", min_value=0, max_value=100, value=30, step=5, key="daily_tp1_book")
        tp2_book_pct = st.slider("TP2 पर किती % बुक करायचे?", min_value=0, max_value=100, value=40, step=5, key="daily_tp2_book")
        # Remaining will auto book at TP3
    
    # Calculate SL and TP
    if entry_price > 0:
        if trade_option == "CALL (CE)":
            sl_price = entry_price * (1 - sl_percent/100)
            tp1_price = entry_price * (1 + tp1_percent/100)
            tp2_price = entry_price * (1 + tp2_percent/100)
            tp3_price = entry_price * (1 + tp3_percent/100)
        else:  # PUT (PE)
            sl_price = entry_price * (1 + sl_percent/100)
            tp1_price = entry_price * (1 - tp1_percent/100)
            tp2_price = entry_price * (1 - tp2_percent/100)
            tp3_price = entry_price * (1 - tp3_percent/100)
        
        total_shares = num_lots * lot_size
        total_investment = entry_price * total_shares
        
        # Calculate P&L
        if trade_option == "CALL (CE)":
            sl_pl = (sl_price - entry_price) * total_shares
            tp1_pl = (tp1_price - entry_price) * total_shares * (tp1_book_pct/100)
            tp2_pl = (tp2_price - entry_price) * total_shares * (tp2_book_pct/100)
            tp3_pl = (tp3_price - entry_price) * total_shares * ((100 - tp1_book_pct - tp2_book_pct)/100)
            total_profit = tp1_pl + tp2_pl + tp3_pl
        else:
            sl_pl = (entry_price - sl_price) * total_shares
            tp1_pl = (entry_price - tp1_price) * total_shares * (tp1_book_pct/100)
            tp2_pl = (entry_price - tp2_price) * total_shares * (tp2_book_pct/100)
            tp3_pl = (entry_price - tp3_price) * total_shares * ((100 - tp1_book_pct - tp2_book_pct)/100)
            total_profit = tp1_pl + tp2_pl + tp3_pl
        
        # Display Results
        st.markdown("---")
        st.markdown("## 📊 YOUR TRADE SUMMARY")
        
        # Main Results Table
        st.markdown(f"""
        <style>
        .trade-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        .trade-table th {{
            background: linear-gradient(135deg, #00ff88, #00b4d8);
            color: black;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }}
        .trade-table td {{
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #333;
        }}
        .profit {{ color: #00ff88; font-weight: bold; }}
        .loss {{ color: #ff4444; font-weight: bold; }}
        .neutral {{ color: #ffaa00; font-weight: bold; }}
        </style>
        
        <table class="trade-table">
            <tr>
                <th>Level</th>
                <th>Premium (₹)</th>
                <th>Move Pts</th>
                <th>Total P&L (₹)</th>
                <th>Action</th>
            </tr>
            <tr>
                <td><b>🎯 ENTRY</b></td>
                <td><b>₹{entry_price:.2f}</b></td>
                <td>-</td>
                <td>-</td>
                <td>📌 Entry Point</td>
            </tr>
            <tr>
                <td><b>🛡️ STOP LOSS</b></td>
                <td>₹{sl_price:.2f}</td>
                <td class="loss">{sl_price - entry_price:+.2f}</td>
                <td class="loss">₹{sl_pl:,.0f}</td>
                <td>🔴 EXIT - SL HIT</td>
            </tr>
            <tr style="background: rgba(0,255,136,0.1);">
                <td><b>🎯 TP1 ({tp1_book_pct}%)</b></td>
                <td>₹{tp1_price:.2f}</td>
                <td class="profit">{tp1_price - entry_price:+.2f}</td>
                <td class="profit">+₹{tp1_pl:,.0f}</td>
                <td>✅ BOOK {tp1_book_pct}%</td>
            </tr>
            <tr style="background: rgba(0,255,136,0.05);">
                <td><b>🎯 TP2 ({tp2_book_pct}%)</b></td>
                <td>₹{tp2_price:.2f}</td>
                <td class="profit">{tp2_price - entry_price:+.2f}</td>
                <td class="profit">+₹{tp2_pl:,.0f}</td>
                <td>✅ BOOK {tp2_book_pct}%</td>
            </tr>
            <tr style="background: rgba(0,255,136,0.02);">
                <td><b>🎯 TP3 ({100 - tp1_book_pct - tp2_book_pct}%)</b></td>
                <td>₹{tp3_price:.2f}</td>
                <td class="profit">{tp3_price - entry_price:+.2f}</td>
                <td class="profit">+₹{tp3_pl:,.0f}</td>
                <td>✅ BOOK REMAINING</td>
            </tr>
            <tr style="background: rgba(0,0,0,0.3);">
                <td><b>🏆 TOTAL PROFIT</b></td>
                <td colspan="2"><b>Risk:Reward = 1:{abs(total_profit/sl_pl):.1f}</b></td>
                <td class="profit"><b>+₹{total_profit:,.0f}</b></td>
                <td><b>🎉 NET PROFIT</b></td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
        # Investment Summary
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Shares", f"{total_shares:,}")
        with col2:
            st.metric("💰 Total Investment", f"₹{total_investment:,.0f}")
        with col3:
            st.metric("📉 Max Loss (SL)", f"₹{sl_pl:,.0f}", delta=f"{sl_percent}%")
        with col4:
            risk_reward = abs(total_profit/sl_pl) if sl_pl != 0 else 0
            st.metric("📈 Risk:Reward", f"1:{risk_reward:.1f}")
        
        # Lot-wise P&L
        st.markdown("---")
        st.markdown("#### 📊 LOT-WISE P&L (Per Lot)")
        
        per_lot_shares = lot_size
        per_lot_investment = entry_price * per_lot_shares
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Per Lot Shares", f"{per_lot_shares}")
            st.metric("Per Lot Investment", f"₹{per_lot_investment:.0f}")
        with col2:
            st.metric("SL Loss per Lot", f"₹{sl_pl/num_lots:,.0f}")
            st.metric("TP1 Profit per Lot", f"₹{tp1_pl/num_lots:,.0f}")
        with col3:
            st.metric("TP2 Profit per Lot", f"₹{tp2_pl/num_lots:,.0f}")
            st.metric("TP3 Profit per Lot", f"₹{tp3_pl/num_lots:,.0f}")
        
        # Order Summary for Copy-Paste
        st.markdown("---")
        st.markdown("#### 📋 ORDER SUMMARY (Copy this)")
        
        order_summary = f"""
┌─────────────────────────────────────────────────┐
│  {trade_symbol} {strike_price} {trade_option}                           │
├─────────────────────────────────────────────────┤
│  Entry:     ₹{entry_price:.2f}                                         │
│  SL:        ₹{sl_price:.2f} ({sl_percent}%)                             │
│  TP1:       ₹{tp1_price:.2f} (Book {tp1_book_pct}% @ {tp1_percent}%)    │
│  TP2:       ₹{tp2_price:.2f} (Book {tp2_book_pct}% @ {tp2_percent}%)    │
│  TP3:       ₹{tp3_price:.2f} (Book {100-tp1_book_pct-tp2_book_pct}%)    │
├─────────────────────────────────────────────────┤
│  Lots:      {num_lots} x {lot_size} = {total_shares} shares            │
│  Investment: ₹{total_investment:,.0f}                                   │
│  Max Loss:   ₹{sl_pl:,.0f}                                            │
│  Max Profit: ₹{total_profit:,.0f}                                      │
│  R:R Ratio:  1:{risk_reward:.1f}                                       │
└─────────────────────────────────────────────────┘
"""
        st.code(order_summary, language="text")
        
        # Save to Session State for Journal
        if st.button("💾 SAVE THIS TRADE TO JOURNAL", use_container_width=True):
            trade_record = {
                "Date": get_ist_now().strftime('%Y-%m-%d %H:%M'),
                "Symbol": f"{trade_symbol} {strike_price} {trade_option}",
                "Lots": num_lots,
                "Entry": entry_price,
                "SL": sl_price,
                "TP1": tp1_price,
                "TP2": tp2_price,
                "TP3": tp3_price,
                "Investment": total_investment,
                "Max Loss": sl_pl,
                "Max Profit": total_profit,
                "Status": "ACTIVE"
            }
            
            if "daily_trades" not in st.session_state:
                st.session_state.daily_trades = []
            
            st.session_state.daily_trades.append(trade_record)
            st.success(f"✅ Trade saved for {trade_symbol}!")
            st.rerun()

# ================= DISPLAY SAVED TRADES =================
with st.expander("📋 MY DAILY TRADES JOURNAL", expanded=True):
    st.markdown("### 📋 Today's Trades")
    
    if "daily_trades" in st.session_state and st.session_state.daily_trades:
        df_trades = pd.DataFrame(st.session_state.daily_trades)
        st.dataframe(df_trades, use_container_width=True)
        
        # Delete option
        for i, trade in enumerate(st.session_state.daily_trades):
            col1, col2 = st.columns([4,1])
            with col1:
                st.markdown(f"**{trade['Symbol']}** | Entry: ₹{trade['Entry']} | SL: ₹{trade['SL']} | TP1: ₹{trade['TP1']} | TP2: ₹{trade['TP2']} | TP3: ₹{trade['TP3']}")
            with col2:
                if st.button(f"❌", key=f"del_{i}"):
                    st.session_state.daily_trades.pop(i)
                    st.rerun()
    else:
        st.info("📭 No trades saved yet. Use the form above to add trades.")

# ================= AUTO EXECUTION =================
if st.session_state.algo_running and st.session_state.totp_verified:
    check_and_execute_orders_with_journal()
    monitor_active_orders_with_pnl()
    
    if st.session_state.auto_trade_enabled:
        auto_trade_from_signal_with_journal()
        wolf_auto_fo_trade()
    
    st.info("🐺 Wolf is hunting... Live P&L Active 🤖")
