from flask import Flask, request
import requests
import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from SmartApi import SmartConnect
import pyotp
import config
from datetime import datetime, timedelta
import time
import yfinance as yf
import feedparser
import winsound
import os
import random
from streamlit_autorefresh import st_autorefresh
import nsefin

# Try to import nsepython
try:
    from nsepython import nse_optionchain_scrapper
    NSEPYTHON_AVAILABLE = True
except ImportError:
    NSEPYTHON_AVAILABLE = False
    print("nsepython not available")

app = Flask(__name__)

# Define NIFTY50_SYMBOLS
NIFTY50_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "BAJFINANCE.NS",
    "ITC.NS", "AXISBANK.NS", "WIPRO.NS", "HCLTECH.NS", "SUNPHARMA.NS",
    "MARUTI.NS", "TITAN.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "POWERGRID.NS",
    "NTPC.NS", "M&M.NS", "ULTRACEMCO.NS", "ONGC.NS", "NESTLEIND.NS",
    "JSWSTEEL.NS", "TECHM.NS", "BAJAJFINSV.NS", "HDFC.NS", "ASIANPAINT.NS",
    "GRASIM.NS", "INDUSINDBK.NS", "HDFCLIFE.NS", "SBILIFE.NS", "DRREDDY.NS",
    "BPCL.NS", "HEROMOTOCO.NS", "EICHERMOT.NS", "BRITANNIA.NS", "COALINDIA.NS",
    "SHREECEM.NS", "CIPLA.NS", "BAJAJ-AUTO.NS", "DIVISLAB.NS", "UPL.NS"
]

TOP_STOCKS = NIFTY50_SYMBOLS[:20]

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(silent=True)
        response_data = {"status": "success", "message": "Webhook received"}
        return response_data, 200
    except Exception as e:
        return {"status": "success", "message": "Acknowledged"}, 200

def get_color(val):
    val = str(val).lower()
    if "bullish" in val or "buy" in val:
        return "#00ff88"
    elif "bearish" in val or "sell" in val:
        return "#ff4b4b"
    else:
        return "#facc15"

def clean_df(df):
    if df is None or df.empty:
        return df
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns = [str(c).lower().strip() for c in df.columns]
    if 'adj close' in df.columns and 'close' not in df.columns:
        df.rename(columns={'adj close': 'close'}, inplace=True)
    return df

# ===== UI CONFIG =====
st.set_page_config(page_title="RUDRANSH PRO-ALGO X", layout="wide", page_icon="📈")
                            
# Session State
if "nifty_trades_today" not in st.session_state:
    st.session_state.nifty_trades_today = 0
if "crude_trades_today" not in st.session_state:
    st.session_state.crude_trades_today = 0
if "ng_trades_today" not in st.session_state:
    st.session_state.ng_trades_today = 0
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = datetime.now().date()

if datetime.now().date() != st.session_state.last_trade_date:
    st.session_state.nifty_trades_today = 0
    st.session_state.crude_trades_today = 0
    st.session_state.ng_trades_today = 0
    st.session_state.last_trade_date = datetime.now().date()
    st.session_state.last_trade_side = ""

if "algo_running" not in st.session_state:
    st.session_state.algo_running = False
if 'active' not in st.session_state:
    st.session_state.active = False
if "last_trade_side" not in st.session_state:
    st.session_state.last_trade_side = ""
if "last_trade_time" not in st.session_state:
    st.session_state.last_trade_time = datetime.now() - timedelta(minutes=10)
if "last_msg" not in st.session_state:
    st.session_state.last_msg = ""
if "last_signal" not in st.session_state:
    st.session_state.last_signal = ""

if "journal_unlocked" not in st.session_state:
    st.session_state.journal_unlocked = False
if "journal_password_attempt" not in st.session_state:
    st.session_state.journal_password_attempt = 0

# ===== PREMIUM INSTITUTIONAL UI =====
st.markdown("""
<style>
.stApp{
    background: radial-gradient(circle at top left, rgba(0,255,136,0.08), transparent 25%),
                radial-gradient(circle at top right, rgba(255,0,80,0.08), transparent 25%),
                linear-gradient(135deg,#050816 0%,#0b1120 45%,#020617 100%);
    color:white;
    overflow-x:hidden;
}
::-webkit-scrollbar{ width:10px; }
::-webkit-scrollbar-track{ background:#0f172a; }
::-webkit-scrollbar-thumb{ background:linear-gradient(to bottom,#00ff88,#ff004f); border-radius:20px; }
.hero-box{
    position:relative;
    overflow:hidden;
    background: linear-gradient(135deg, rgba(0,255,136,0.08), rgba(255,0,80,0.08));
    border:1px solid rgba(255,255,255,0.08);
    border-radius:30px;
    padding:40px;
    margin-bottom:30px;
    backdrop-filter:blur(18px);
    box-shadow: 0 0 40px rgba(0,255,136,0.15), 0 0 60px rgba(255,0,80,0.12);
    animation:heroGlow 4s infinite alternate;
}
@keyframes heroGlow{
    from{ box-shadow: 0 0 30px rgba(0,255,136,0.12), 0 0 50px rgba(255,0,80,0.10); }
    to{ box-shadow: 0 0 50px rgba(0,255,136,0.25), 0 0 80px rgba(255,0,80,0.18); }
}
.hero-title{
    font-size:58px;
    font-weight:900;
    text-align:center;
    background:linear-gradient(90deg, #ff004f, #ffffff, #00ff88);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.hero-sub{ text-align:center; font-size:18px; color:#94a3b8; margin-top:12px; }
.hero-live{ text-align:center; margin-top:18px; color:#00ff88; font-weight:bold; animation:pulse 1.2s infinite; }
@keyframes pulse{ 0%{opacity:1;} 50%{opacity:0.4;} 100%{opacity:1;} }
[data-testid="metric-container"]{
    background: linear-gradient(145deg, rgba(15,23,42,0.95), rgba(30,41,59,0.88));
    border:1px solid rgba(255,255,255,0.08);
    padding:22px;
    border-radius:22px;
    backdrop-filter:blur(18px);
    transition:all 0.35s ease;
}
[data-testid="metric-container"]:hover{
    transform:translateY(-6px) scale(1.02);
    border:1px solid rgba(0,255,136,0.35);
}
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
    border-right:1px solid rgba(255,255,255,0.08);
}
.stButton > button{
    width:100%;
    border:none;
    border-radius:16px;
    padding:14px;
    font-weight:700;
    color:white;
    background: linear-gradient(135deg, #ff004f, #00ff88);
    transition:all 0.3s ease;
}
.stButton > button:hover{
    transform:translateY(-3px) scale(1.02);
    box-shadow: 0 0 30px rgba(0,255,136,0.35);
}
table{ border-radius:18px !important; overflow:hidden; }
thead tr th{ background:#111827 !important; color:#00ff88 !important; }
tbody tr{ background:#0f172a !important; }
tbody tr:hover{ background:#172033 !important; }
h1,h2,h3{ color:white !important; }
#MainMenu{ visibility:hidden; }
footer{ visibility:hidden; }
header{ visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ===== SYMBOL MAPPING =====
SYMBOL_MAP = {
    "NIFTY": {"token": "99926000", "exch": "NSE", "symbol": "NIFTY"},
    "CRUDEOIL": {"token": "210000", "exch": "MCX", "symbol": "CRUDEOIL"},
    "NATURALGAS": {"token": "210001", "exch": "MCX", "symbol": "NATURALGAS"}
}

# ===== TP CONFIGURATION =====
TP_CONFIG = {
    "NIFTY": {"tp1_points": 10, "tp2_points": 10, "tp3_points": 10},
    "CRUDEOIL": {"tp1_points": 10, "tp2_points": 10, "tp3_points": 10},
    "NATURALGAS": {"tp1_points": 1.0, "tp2_points": 1.5, "tp3_points": 2.0},
    "STOCK_OPTION": {"tp1_points": 5, "tp2_points": 10, "tp3_points": 15}
}
DEFAULT_TP_CONFIG = {"tp1_points": 10, "tp2_points": 10, "tp3_points": 10}

def calculate_target_levels_points(entry_price, side, market, is_option=False):
    if is_option or "OPTION" in market.upper():
        config = TP_CONFIG["STOCK_OPTION"]
    else:
        config = TP_CONFIG.get(market, DEFAULT_TP_CONFIG)
    tp1_points, tp2_points, tp3_points = config["tp1_points"], config["tp2_points"], config["tp3_points"]
    if side == "BUY":
        return entry_price + tp1_points, entry_price + tp2_points, entry_price + tp3_points, tp1_points, tp2_points, tp3_points
    else:
        return entry_price - tp1_points, entry_price - tp2_points, entry_price - tp3_points, tp1_points, tp2_points, tp3_points

# ===== ITM SETTINGS =====
ITM_SETTINGS = {
    "NIFTY": {"itm_points": 100, "strike_multiple": 50, "description": "100 Points ITM"},
    "CRUDEOIL": {"itm_points": 100, "strike_multiple": 50, "description": "100 Points ITM"},
    "NATURALGAS": {"itm_points": 10, "strike_multiple": 1, "description": "10 Points ITM"},
    "STOCK_OPTION": {"itm_strike_count": 2, "description": "2 Strike ITM"}
}

STRIKE_GAPS = {
    "RELIANCE": 20, "TCS": 50, "HDFCBANK": 25, "ICICIBANK": 20,
    "INFY": 40, "SBIN": 15, "HINDUNILVR": 50, "ITC": 10,
    "BAJFINANCE": 100, "KOTAKBANK": 25, "BHARTIARTL": 10,
    "WIPRO": 20, "HCLTECH": 50, "SUNPHARMA": 20, "MARUTI": 100,
    "TATAMOTORS": 10, "TATASTEEL": 10, "POWERGRID": 10,
    "NTPC": 10, "M&M": 25,
}

def get_stock_strike_gap(symbol):
    return STRIKE_GAPS.get(symbol, 20)

def get_itm_strike(current_price, market, option_type="CE", stock_symbol=None):
    settings = ITM_SETTINGS.get(market, ITM_SETTINGS["STOCK_OPTION"])
    
    if market == "STOCK_OPTION":
        strike_count = settings["itm_strike_count"]
        strike_gap = get_stock_strike_gap(stock_symbol) if stock_symbol else 20
        if option_type == "CE":
            itm_strike = current_price - (strike_count * strike_gap)
        else:
            itm_strike = current_price + (strike_count * strike_gap)
        remainder = itm_strike % strike_gap
        if remainder <= strike_gap / 2:
            itm_strike = itm_strike - remainder
        else:
            itm_strike = itm_strike + (strike_gap - remainder)
        return int(itm_strike)
    elif market == "NATURALGAS":
        itm_points = settings["itm_points"]
        itm_strike = current_price - itm_points if option_type == "CE" else current_price + itm_points
        return round(itm_strike, 1)
    else:
        strike_multiple = settings["strike_multiple"]
        itm_points = settings["itm_points"]
        itm_strike = current_price - itm_points if option_type == "CE" else current_price + itm_points
        itm_strike = round(itm_strike / strike_multiple) * strike_multiple
        return int(itm_strike)

print(f"✅ ITM Settings Loaded")

# ===== DATA FUNCTIONS =====
@st.cache_data(ttl=30)
def get_live_nifty_data():
    try:
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period="5d")
        if hist.empty or len(hist) < 2:
            return fallback_nifty_data()
        current = hist['Close'].iloc[-1]
        high = hist['High'].max()
        low = hist['Low'].min()
        prev_close = hist['Close'].iloc[-2]
        pivot = (high + low + current) / 3
        support = round(pivot * 2 - high, 2)
        resistance = round(pivot * 2 - low, 2)
        change = ((current - prev_close) / prev_close) * 100
        return {
            "pcr": round(1.2 if change > 0 else 0.8, 2),
            "support": support,
            "resistance": resistance,
            "current_price": round(current, 2),
            "change": round(change, 2),
            "long_strikes": [],
            "short_strikes": []
        }
    except Exception as e:
        print(f"NIFTY Error: {e}")
        return fallback_nifty_data()

def fallback_nifty_data():
    return {"pcr": 1.0, "support": 0, "resistance": 0, "current_price": 24500, "change": 0, "long_strikes": [], "short_strikes": []}

@st.cache_data(ttl=10)
def get_live_crude_data():
    try:
        crude = yf.Ticker("CRUDEOIL.NS")
        hist = crude.history(period="5d")
        if not hist.empty and len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            high = hist['High'].max()
            low = hist['Low'].min()
            pivot = (high + low + current) / 3
            support = round(pivot * 2 - high, 2)
            resistance = round(pivot * 2 - low, 2)
            change = ((current - prev) / prev) * 100
            if change > 0.5:
                crude_pcr = 1.5
            elif change > 0:
                crude_pcr = 1.2
            elif change < -0.5:
                crude_pcr = 0.6
            else:
                crude_pcr = 0.9
            return support, resistance, round(current, 2), round(change, 2), crude_pcr
    except:
        pass
    try:
        crude = yf.Ticker("CL=F")
        hist = crude.history(period="5d")
        usd_inr = 87.5
        if not hist.empty and len(hist) >= 2:
            current_usd = hist['Close'].iloc[-1]
            prev_usd = hist['Close'].iloc[-2]
            current = current_usd * usd_inr
            prev = prev_usd * usd_inr
            high = hist['High'].max() * usd_inr
            low = hist['Low'].min() * usd_inr
            pivot = (high + low + current) / 3
            support = round(pivot * 2 - high, 2)
            resistance = round(pivot * 2 - low, 2)
            change = ((current - prev) / prev) * 100
            if change > 0.5:
                crude_pcr = 1.5
            elif change > 0:
                crude_pcr = 1.2
            elif change < -0.5:
                crude_pcr = 0.6
            else:
                crude_pcr = 0.9
            return support, resistance, round(current, 2), round(change, 2), crude_pcr
    except:
        pass
    return 0, 0, 0, 0, 1.0

@st.cache_data(ttl=10)
def get_live_ng_data():
    try:
        ng = yf.Ticker("NATURALGAS.NS")
        hist = ng.history(period="5d")
        if not hist.empty and len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            high = hist['High'].max()
            low = hist['Low'].min()
            pivot = (high + low + current) / 3
            support = round(pivot * 2 - high, 2)
            resistance = round(pivot * 2 - low, 2)
            change = ((current - prev) / prev) * 100
            if change > 0.5:
                ng_pcr = 1.4
            elif change > 0:
                ng_pcr = 1.1
            elif change < -0.5:
                ng_pcr = 0.7
            else:
                ng_pcr = 0.8
            return support, resistance, round(current, 2), round(change, 2), ng_pcr
    except:
        pass
    try:
        ng = yf.Ticker("NG=F")
        hist = ng.history(period="5d")
        usd_inr = 87.5
        if not hist.empty and len(hist) >= 2:
            current_usd = hist['Close'].iloc[-1]
            prev_usd = hist['Close'].iloc[-2]
            current = current_usd * usd_inr
            prev = prev_usd * usd_inr
            high = hist['High'].max() * usd_inr
            low = hist['Low'].min() * usd_inr
            pivot = (high + low + current) / 3
            support = round(pivot * 2 - high, 2)
            resistance = round(pivot * 2 - low, 2)
            change = ((current - prev) / prev) * 100
            if change > 0.5:
                ng_pcr = 1.4
            elif change > 0:
                ng_pcr = 1.1
            elif change < -0.5:
                ng_pcr = 0.7
            else:
                ng_pcr = 0.8
            return support, resistance, round(current, 2), round(change, 2), ng_pcr
    except:
        pass
    return 0, 0, 0, 0, 1.0

def get_live_pnl(api):
    try:
        pos = api.position()
        if not pos or 'data' not in pos:
            return 0.0
        total = 0
        for p in pos['data']:
            total += float(p.get('pnl', 0))
        return total
    except:
        return 0.0

def square_off_all(api):
    try:
        pos = api.position()
        if pos.get('data'):
            for p in pos['data']:
                if int(p['netqty']) != 0:
                    side = "SELL" if int(p['netqty']) > 0 else "BUY"
                    api.placeOrder({"variety": "NORMAL", "tradingsymbol": p['tradingsymbol'], 
                                   "symboltoken": p['symboltoken'], "transactiontype": side, 
                                   "exchange": p['exchange'], "ordertype": "MARKET", 
                                   "producttype": "INTRADAY", "duration": "DAY", 
                                   "quantity": str(abs(int(p['netqty'])))})
            st.warning("🚨 ALL POSITIONS SQUARED OFF!")
            st.session_state.algo_running = False
    except:
        pass

def get_market_intel(df):
    if df is None or df.empty:
        return {"Trend": "NO DATA", "TrendCol": "#999999", "Signal": "NONE", "SL": 0, "S1": 0, "R1": 0}
    if 'close' not in df.columns:
        return {"Trend": "NO DATA", "TrendCol": "#999999", "Signal": "NONE", "SL": 0, "S1": 0, "R1": 0}
    c = df['close'].iloc[-1]
    h = df['high'].max() if 'high' in df.columns else c
    l = df['low'].min() if 'low' in df.columns else c
    pivot = (h + l + c) / 3
    s1 = (2 * pivot) - h
    r1 = (2 * pivot) - l
    if 'ema9' not in df.columns or df['ema9'].isna().all():
        if len(df) >= 9 and 'close' in df.columns:
            df['ema9'] = df['close'].ewm(span=9, adjust=False).mean()
        else:
            return {"Trend": "NEUTRAL ⚪", "TrendCol": "#facc15", "Signal": "NONE", "SL": 0, "S1": round(s1), "R1": round(r1)}
    ema9_value = df['ema9'].iloc[-1]
    if ema9_value is None or pd.isna(ema9_value):
        trend = "NEUTRAL ⚪"
        trend_col = "#facc15"
    else:
        if c > ema9_value:
            trend = "BULLISH 🚀"
            trend_col = "#00ff88"
        else:
            trend = "BEARISH 🔻"
            trend_col = "#ff4b4b"
    signal = "NONE"
    sl = 0
    if len(df) > 20 and 'ema20' in df.columns and 'rsi' in df.columns:
        try:
            prev_high = df['high'].iloc[-2] if 'high' in df.columns else c
            prev_low = df['low'].iloc[-2] if 'low' in df.columns else c
            ema9 = df['ema9'].iloc[-1] if 'ema9' in df.columns else c
            ema20 = df['ema20'].iloc[-1] if 'ema20' in df.columns else c
            rsi = df['rsi'].iloc[-1] if 'rsi' in df.columns else 50
            adx = df['adx'].iloc[-1] if 'adx' in df.columns else 0
            volume = df['volume'].iloc[-1] if 'volume' in df.columns else 0
            vol_sma = df['volume'].rolling(20).mean().iloc[-1] if 'volume' in df.columns else 1
            strongBull = c > df['open'].iloc[-1] and c > prev_high if 'open' in df.columns else False
            strongBear = c < df['open'].iloc[-1] and c < prev_low if 'open' in df.columns else False
            volumeFilter = volume > vol_sma if volume > 0 else False
            sideways = (rsi > 45 and rsi < 55 and adx < 20)
            if ema9 > ema20 and c > ema20 and c > prev_high and strongBull and adx > 20 and not sideways and volumeFilter:
                signal = "BUY"
                sl = round(c - 15)
            elif ema9 < ema20 and c < ema20 and c < prev_low and strongBear and adx > 20 and not sideways and volumeFilter:
                signal = "SELL"
                sl = round(c + 15)
        except Exception as e:
            print(f"Signal calculation error: {e}")
    return {"Trend": trend, "TrendCol": trend_col, "Signal": signal, "SL": sl, "S1": round(s1), "R1": round(r1)}

def get_api():
    try:
        api = SmartConnect(api_key=config.API_KEY)
        for i in range(3):
            try:
                totp = pyotp.TOTP(config.TOTP_SECRET).now()
                data = api.generateSession(config.CLIENT_CODE, config.PASSWORD, totp)
                if data['status']:
                    st.success("✅ API Connected Successfully")
                    return api
            except:
                time.sleep(2)
        st.error("❌ API Failed after retries")
        return None
    except Exception as e:
        st.error(f"❌ API Error: {e}")
        return None

@st.cache_data(ttl=600)
def get_nifty_news():
    try:
        ticker = yf.Ticker("^NSEI")
        return " | ".join([f"📰 {n['title']}" for n in ticker.news[:5]])
    except:
        return "🕒 News Syncing..."

@st.cache_data(ttl=60)
def get_global_trend():
    syms = {"🇮🇳 NIFTY 50": "^NSEI", "🇮🇳 BANK NIFTY": "^NSEBANK", "🇯🇵 NIKKEI": "^N225", "🇭🇰 HANG SENG": "^HSI", "🇬🇧 FTSE": "^FTSE", "🇩🇪 DAX": "^GDAXI", "🇺🇸 DOW JONES": "^DJI", "🥇 GOLD": "GC=F", "🛢️ CRUDE OIL": "CL=F"}
    bullish, bearish = 0, 0
    try:
        data = yf.download(list(syms.values()), period="2d", interval="1d", progress=False, auto_adjust=False)
        if 'Close' in data.columns:
            data = data['Close']
        else:
            data = clean_df(data)
            if 'close' in data.columns:
                data = data['close']
        for name, symbol in syms.items():
            try:
                if symbol not in data.columns:
                    continue
                series = data[symbol].dropna()
                if len(series) < 2:
                    continue
                prev, curr = float(series.iloc[-2]), float(series.iloc[-1])
                if curr > prev:
                    bullish += 1
                elif curr < prev:
                    bearish += 1
            except:
                continue
        if bullish > bearish:
            return "BULLISH 🟢", "#00ff88"
        elif bearish > bullish:
            return "BEARISH 🔴", "#ff4b4b"
        else:
            return "SIDEWAYS 🟡", "#ffa500"
    except:
        return "NO DATA ⚪", "#999999"

def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
        print(f"Telegram sent: {msg[:50]}...")
    except Exception as e:
        print(f"Telegram Error: {e}")

def send_alert(msg):
    send_telegram(msg)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START", use_container_width=True):
            st.session_state.algo_running = True
            send_alert("🤖 ALGO STARTED")
    with col2:
        if st.button("🛑 STOP", use_container_width=True):
            st.session_state.algo_running = False
            send_alert("🛑 ALGO STOPPED")
    
    st.markdown("---")
    
    if st.session_state.algo_running:
        st.markdown("""
        <div style='background-color:#0a2a1a; border:1px solid #00ff88; border-radius:10px; padding:10px; text-align:center;'>
            <span style='color:#00ff88; font-size:16px; font-weight:bold;'>🟢 ALGO IS RUNNING</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background-color:#2a0a1a; border:1px solid #ff4b4b; border-radius:10px; padding:10px; text-align:center;'>
            <span style='color:#ff4b4b; font-size:16px; font-weight:bold;'>🔴 ALGO IS STOPPED</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    market = st.selectbox("📌 Select Asset", list(SYMBOL_MAP.keys()))
    lot_size = {"NIFTY": 65, "CRUDEOIL": 100, "NATURALGAS": 1250}.get(market, 1)
    num_lots = st.number_input("📊 Number of Lots", min_value=1, value=1)
    
    st.markdown(f"""
    <div style='background:#1e293b; padding:15px; border-radius:12px; text-align:center;'>
        <span style='color:#9ca3af;'>Total Quantity</span><br>
        <span style='color:#00ff88; font-size:24px; font-weight:bold;'>{num_lots * lot_size}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

st.markdown("""
<style>
.hero-box-full {
    position: relative;
    width: 100%;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(0,255,136,0.08), rgba(255,0,80,0.08));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 0px;
    padding: 20px 0px;
    margin-bottom: 30px;
    backdrop-filter: blur(18px);
    box-shadow: 0 0 40px rgba(0,255,136,0.15), 0 0 60px rgba(255,0,80,0.12);
    text-align: center;
    animation: heroGlow 4s infinite alternate;
}
@keyframes heroGlow {
    from { box-shadow: 0 0 30px rgba(0,255,136,0.12), 0 0 50px rgba(255,0,80,0.10); }
    to { box-shadow: 0 0 50px rgba(0,255,136,0.25), 0 0 80px rgba(255,0,80,0.18); }
}
.hero-image-full {
    display: block;
    width: 100%;
    height: auto;
    margin: 0 auto;
    object-fit: cover;
}
@media (max-width: 768px) {
    .hero-image-full { width: 100%; }
    .hero-box-full { padding: 15px 0px; }
}
</style>
<div class="hero-box-full">
    <img class="hero-image-full" src="https://i.postimg.cc/tC4ZbMVL/Chat-GPT-Image-May-13-2026-05-24-45-AM.png">
</div>
""", unsafe_allow_html=True)

global_trend, global_color = get_global_trend()
st.markdown(f"""
<div style='background:#020617; padding:12px; border-radius:10px; border:1px solid {global_color}; text-align:center; margin-bottom:20px;'>
    🌍 GLOBAL TREND: <span style='color:{global_color}; font-weight:bold;'>{global_trend}</span>
</div>
""", unsafe_allow_html=True)

nifty_data = get_live_nifty_data()
crude_support, crude_resistance, crude_price, crude_change, crude_pcr = get_live_crude_data()
ng_support, ng_resistance, ng_price, ng_change, ng_pcr = get_live_ng_data()

@st.cache_data(ttl=30)
def get_real_option_chain():
    try:
        nse = nsefin.NSEClient()
        option_data = nse.get_option_chain("NIFTY")
        if option_data is not None and not option_data.empty:
            puts = option_data[option_data['option_type'] == 'PE']
            calls = option_data[option_data['option_type'] == 'CE']
            total_pe_oi = puts['open_interest'].sum() if 'open_interest' in puts.columns else 0
            total_ce_oi = calls['open_interest'].sum() if 'open_interest' in calls.columns else 0
            pe_strikes, pe_oi_values = [], []
            if not puts.empty and 'open_interest' in puts.columns:
                top_puts = puts.nlargest(6, 'open_interest')
                for idx, row in top_puts.iterrows():
                    pe_strikes.append(int(row['strike_price']))
                    pe_oi_values.append(int(row['open_interest']))
            ce_strikes, ce_oi_values = [], []
            if not calls.empty and 'open_interest' in calls.columns:
                top_calls = calls.nlargest(6, 'open_interest')
                for idx, row in top_calls.iterrows():
                    ce_strikes.append(int(row['strike_price']))
                    ce_oi_values.append(int(row['open_interest']))
            return {
                'pe_strikes': pe_strikes, 'ce_strikes': ce_strikes,
                'pe_oi': pe_oi_values, 'ce_oi': ce_oi_values,
                'pe_total': int(total_pe_oi), 'ce_total': int(total_ce_oi), 'success': True
            }
        return {'success': False}
    except Exception as e:
        print(f"Option Chain Error: {e}")
        return {'success': False}

# ===== NIFTY SECTION =====
st.markdown("## 📊 NIFTY 50")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center;'>
        <span style='color:#9ca3af; font-size:11px;'>💰 CURRENT PRICE</span><br>
        <span style='color:#00ff88; font-size:20px; font-weight:bold;'>₹{nifty_data['current_price']:,.2f}</span><br>
        <span style='color:#9ca3af; font-size:11px;'>{nifty_data['change']:+.2f}%</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    if 'buy_condition' in locals() and buy_condition:
        signal_text = "🔵 BUY"
        signal_color = "#00ff88"
    elif 'sell_condition' in locals() and sell_condition:
        signal_text = "🔴 SELL"
        signal_color = "#ff4b4b"
    else:
        signal_text = "⚪ WAIT"
        signal_color = "#facc15"
    
    st.markdown(f"""
    <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center; border:1px solid {signal_color};'>
        <span style='color:#9ca3af; font-size:11px;'>🎯 SIGNAL</span><br>
        <span style='color:{signal_color}; font-size:20px; font-weight:bold;'>{signal_text}</span>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center;'>
        <span style='color:#9ca3af; font-size:11px;'>🛡️ SUPPORT</span><br>
        <span style='color:#ff4b4b; font-size:20px; font-weight:bold;'>₹{nifty_data['support']:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center;'>
        <span style='color:#9ca3af; font-size:11px;'>⚡ RESISTANCE</span><br>
        <span style='color:#00ff88; font-size:20px; font-weight:bold;'>₹{nifty_data['resistance']:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

# ===== CRUDE OIL SECTION =====
st.markdown("---")
st.markdown("## 🛢️ CRUDE OIL")

if crude_price > 0:
    cr_met1, cr_met2, cr_met3, cr_met4 = st.columns(4)
    
    with cr_met1:
        crude_trend_color = "#00ff88" if crude_change > 0 else "#ff4b4b"
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center; border:1px solid {crude_trend_color};'>
            <span style='color:#9ca3af; font-size:11px;'>💰 CURRENT PRICE</span><br>
            <span style='color:#00ff88; font-size:20px; font-weight:bold;'>₹{crude_price:,.2f}</span><br>
            <span style='color:{crude_trend_color}; font-size:11px;'>{crude_change:+.2f}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with cr_met2:
        if crude_change > 0.2:
            signal_text = "🔵 BUY"
            signal_color = "#00ff88"
        elif crude_change < -0.2:
            signal_text = "🔴 SELL"
            signal_color = "#ff4b4b"
        else:
            signal_text = "⚪ WAIT"
            signal_color = "#facc15"
    
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center; border:1px solid {signal_color};'>
            <span style='color:#9ca3af; font-size:11px;'>🎯 SIGNAL</span><br>
            <span style='color:{signal_color}; font-size:20px; font-weight:bold;'>{signal_text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with cr_met3:
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center;'>
            <span style='color:#9ca3af; font-size:11px;'>🛡️ SUPPORT</span><br>
            <span style='color:#ff4b4b; font-size:20px; font-weight:bold;'>₹{crude_support:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with cr_met4:
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center;'>
            <span style='color:#9ca3af; font-size:11px;'>⚡ RESISTANCE</span><br>
            <span style='color:#00ff88; font-size:20px; font-weight:bold;'>₹{crude_resistance:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("⚠️ Crude Oil data temporarily unavailable")

# ===== NATURAL GAS SECTION =====
st.markdown("---")
st.markdown("## 🌿 NATURAL GAS")

if ng_price > 0:
    ng_met1, ng_met2, ng_met3, ng_met4 = st.columns(4)
    
    with ng_met1:
        ng_trend_color = "#00ff88" if ng_change > 0 else "#ff4b4b"
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center; border:1px solid {ng_trend_color};'>
            <span style='color:#9ca3af; font-size:11px;'>💰 CURRENT PRICE</span><br>
            <span style='color:#00ff88; font-size:20px; font-weight:bold;'>₹{ng_price:,.2f}</span><br>
            <span style='color:{ng_trend_color}; font-size:11px;'>{ng_change:+.2f}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with ng_met2:
        if ng_change > 0.2:
            signal_text = "🔵 BUY"
            signal_color = "#00ff88"
        elif ng_change < -0.2:
            signal_text = "🔴 SELL"
            signal_color = "#ff4b4b"
        else:
            signal_text = "⚪ WAIT"
            signal_color = "#facc15"
    
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center; border:1px solid {signal_color};'>
            <span style='color:#9ca3af; font-size:11px;'>🎯 SIGNAL</span><br>
            <span style='color:{signal_color}; font-size:20px; font-weight:bold;'>{signal_text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with ng_met3:
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center;'>
            <span style='color:#9ca3af; font-size:11px;'>🛡️ SUPPORT</span><br>
            <span style='color:#ff4b4b; font-size:20px; font-weight:bold;'>₹{ng_support:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with ng_met4:
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:15px; text-align:center;'>
            <span style='color:#9ca3af; font-size:11px;'>⚡ RESISTANCE</span><br>
            <span style='color:#00ff88; font-size:20px; font-weight:bold;'>₹{ng_resistance:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("⚠️ Natural Gas data temporarily unavailable")

# ===== DAILY TRADE STATUS =====
st.markdown("---")
st.markdown("## 📊 DAILY TRADE STATUS")

col_d1, col_d2, col_d3 = st.columns(3)

with col_d1:
    st.markdown(f"""
    <div style='background:#1e293b; padding:15px; border-radius:12px; text-align:center;'>
        <span style='color:#9ca3af;'>📊 NIFTY Trades</span><br>
        <span style='color:#00ff88; font-size:24px; font-weight:bold;'>{st.session_state.nifty_trades_today}/2</span>
        <br><span style='color:#9ca3af; font-size:11px;'>9:30 AM - 2:30 PM</span>
    </div>
    """, unsafe_allow_html=True)

with col_d2:
    st.markdown(f"""
    <div style='background:#1e293b; padding:15px; border-radius:12px; text-align:center;'>
        <span style='color:#9ca3af;'>🛢️ CRUDE Trades</span><br>
        <span style='color:#00ff88; font-size:24px; font-weight:bold;'>{st.session_state.crude_trades_today}/2</span>
        <br><span style='color:#9ca3af; font-size:11px;'>6:00 PM - 10:30 PM</span>
    </div>
    """, unsafe_allow_html=True)

with col_d3:
    st.markdown(f"""
    <div style='background:#1e293b; padding:15px; border-radius:12px; text-align:center;'>
        <span style='color:#9ca3af;'>🌿 NG Trades</span><br>
        <span style='color:#00ff88; font-size:24px; font-weight:bold;'>{st.session_state.ng_trades_today}/2</span>
        <br><span style='color:#9ca3af; font-size:11px;'>6:00 PM - 10:30 PM</span>
    </div>
    """, unsafe_allow_html=True)

# ===== API CONNECTION =====
api = get_api()
if api is None:
    st.error("❌ Angel API Connection Failed")
    st.stop()

asset = SYMBOL_MAP[market]

try:
    live_ltp = api.ltpData(asset['exch'], asset['symbol'], asset['token'])
    live_price = float(live_ltp['data']['ltp'])
    print(f"Live LTP: {live_price}")
except:
    live_price = 0

if market == "NIFTY":
    symbol = "^NSEI"
elif market == "CRUDEOIL":
    symbol = "CRUDEOIL.NS"
else:
    symbol = "NATURALGAS.NS"

df_live = yf.download(symbol, period="1d", interval="5m", progress=False, auto_adjust=False)
df_15m = yf.download(symbol, period="2d", interval="15m", progress=False, auto_adjust=False)

df_live = clean_df(df_live)
df_15m = clean_df(df_15m)

if not df_live.empty:
    df_live = df_live.dropna(subset=['close'])
if not df_15m.empty:
    df_15m = df_15m.dropna(subset=['close'])

if df_live.empty and not df_15m.empty:
    df_live = df_15m.copy()

if df_live.empty:
    st.error("❌ LIVE DATA NOT AVAILABLE")
    st.stop()

if not df_live.empty and 'close' in df_live.columns:
    df_live['ema9'] = ta.ema(df_live['close'], 9)
    df_live['ema20'] = ta.ema(df_live['close'], 20)
    df_live['rsi'] = ta.rsi(df_live['close'], 14)
    if len(df_live) >= 20:
        adx_data = ta.adx(df_live['high'], df_live['low'], df_live['close'], length=14)
        df_live['adx'] = adx_data['ADX_14'] if adx_data is not None else 0
    else:
        df_live['adx'] = 0

if not df_15m.empty and 'close' in df_15m.columns:
    df_15m['ema9'] = ta.ema(df_15m['close'], 9)
    df_15m['ema20'] = ta.ema(df_15m['close'], 20)

def calculate_vwap(df):
    if df is None or df.empty or 'volume' not in df.columns:
        return None
    try:
        df_copy = df.copy()
        df_copy['typical_price'] = (df_copy['high'] + df_copy['low'] + df_copy['close']) / 3
        df_copy['pv'] = df_copy['typical_price'] * df_copy['volume']
        df_copy['cum_vol'] = df_copy['volume'].cumsum()
        df_copy['cum_pv'] = df_copy['pv'].cumsum()
        df_copy['vwap'] = df_copy['cum_pv'] / df_copy['cum_vol']
        return df_copy['vwap'].iloc[-1]
    except:
        return None

current_vwap = None
if not df_live.empty and 'volume' in df_live.columns:
    current_vwap = calculate_vwap(df_live)

df_live.reset_index(inplace=True)
df_15m.reset_index(inplace=True)
if 'Datetime' in df_live.columns:
    df_live.rename(columns={'Datetime': 'time'}, inplace=True)
if 'Datetime' in df_15m.columns:
    df_15m.rename(columns={'Datetime': 'time'}, inplace=True)

intel = get_market_intel(df_live)

# ===== LIVE POSITIONS =====
st.markdown("## 📊 LIVE POSITIONS")
st.markdown("*(Select checkboxes to square off specific positions)*")

try:
    pos = api.position()
except:
    pos = {"data": []}

if pos and pos.get('data') and len(pos['data']) > 0:
    positions_data = []
    total_investment = 0
    total_pnl = 0
    today_date = datetime.now().date()
    
    for idx, p in enumerate(pos['data']):
        try:
            qty = abs(int(p.get('netqty', 0)))
            if qty == 0:
                continue
                
            buy_price = float(p.get('buyavgprice', 0))
            
            try:
                ltp_data = api.ltpData(p.get('exchange', 'NSE'), p.get('tradingsymbol', ''), p.get('symboltoken', ''))
                current_price = float(ltp_data['data']['ltp'])
            except:
                current_price = buy_price
            
            total_investment_qty = qty * buy_price
            pnl = (current_price - buy_price) * qty
            
            total_investment += total_investment_qty
            total_pnl += pnl
            
            if pnl > 0:
                status = "PROFIT"
                status_icon = "✅"
            elif pnl < 0:
                status = "LOSS"
                status_icon = "🔴"
            else:
                status = "HOLD"
                status_icon = "⏳"
            
            positions_data.append({
                "index": idx,
                "token": p.get('symboltoken', ''),
                "symbol": p.get('tradingsymbol', 'N/A'),
                "qty": qty,
                "buy_price": round(buy_price, 2),
                "current_price": round(current_price, 2),
                "investment": round(total_investment_qty, 2),
                "pnl": round(pnl, 2),
                "status": status,
                "status_icon": status_icon,
                "exchange": p.get('exchange', 'NSE'),
                "side": "BUY" if int(p.get('netqty', 0)) > 0 else "SELL"
            })
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    if positions_data:
        st.markdown("### 📈 P&L SUMMARY")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("💰 TOTAL INVESTMENT", f"₹{total_investment:,.2f}")
        with col_s2:
            pnl_color = "normal" if total_pnl >= 0 else "inverse"
            st.metric("💵 TOTAL P&L", f"₹{total_pnl:,.2f}", delta_color=pnl_color)
        with col_s3:
            win_count = len([p for p in positions_data if p['pnl'] > 0])
            loss_count = len([p for p in positions_data if p['pnl'] < 0])
            st.metric("🎯 WIN/LOSS", f"{win_count} / {loss_count}")
        
        st.markdown("---")
        
        df_display = pd.DataFrame([{
            "SELECT": False,
            "SYMBOL": p["symbol"],
            "QTY": p["qty"],
            "BUY PRICE": f"₹{p['buy_price']:.2f}",
            "CURRENT PRICE": f"₹{p['current_price']:.2f}",
            "INVESTMENT": f"₹{p['investment']:,.2f}",
            "P&L": f"₹{p['pnl']:,.2f}",
            "STATUS": f"{p['status_icon']} {p['status']}",
            "TOKEN": p["token"],
            "EXCHANGE": p["exchange"],
            "SIDE": p["side"]
        } for p in positions_data])
        
        edited_df = st.data_editor(
            df_display[["SELECT", "SYMBOL", "QTY", "BUY PRICE", "CURRENT PRICE", "INVESTMENT", "P&L", "STATUS"]],
            column_config={
                "SELECT": st.column_config.CheckboxColumn("SELECT", default=False),
                "SYMBOL": "SYMBOL",
                "QTY": st.column_config.NumberColumn("QTY", format="%.0f"),
                "BUY PRICE": "BUY PRICE",
                "CURRENT PRICE": "CURRENT PRICE",
                "INVESTMENT": "INVESTMENT",
                "P&L": "P&L",
                "STATUS": "STATUS",
            },
            use_container_width=True,
            height=400,
            key="positions_editor"
        )
        
        selected_rows = edited_df[edited_df["SELECT"] == True]
        
        if len(selected_rows) > 0:
            st.info(f"📌 {len(selected_rows)} position(s) selected")
            if st.button(f"🔴 SQUARE OFF SELECTED ({len(selected_rows)})", use_container_width=True):
                for idx, row in selected_rows.iterrows():
                    try:
                        orig = positions_data[idx]
                        tx_type = "SELL" if orig["side"] == "BUY" else "BUY"
                        api.placeOrder({
                            "variety": "NORMAL",
                            "tradingsymbol": row["SYMBOL"],
                            "symboltoken": orig["token"],
                            "transactiontype": tx_type,
                            "exchange": orig["exchange"],
                            "ordertype": "MARKET",
                            "producttype": "INTRADAY",
                            "duration": "DAY",
                            "quantity": str(orig["qty"])
                        })
                        st.success(f"✅ Squared off: {row['SYMBOL']}")
                        time.sleep(0.3)
                    except Exception as e:
                        st.error(f"❌ Failed: {row['SYMBOL']} - {e}")
                time.sleep(1)
                st.rerun()
    else:
        st.info("📭 No open positions with valid data")
else:
    st.info("📭 No open positions")

# Password Check
if not st.session_state.journal_unlocked:
    st.markdown("""
    <div style='background:#1e293b; padding:20px; border-radius:12px; text-align:center;'>
        <span style='color:#facc15; font-size:20px;'>🔒 LOCKED</span><br>
        <span style='color:#9ca3af;'>Enter password to view Trade Journal</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
    with col_p2:
        journal_password = st.text_input("Password", type="password", key="journal_pass")
        if st.button("🔓 UNLOCK", use_container_width=True):
            if journal_password == "Rudransh@8055":
                st.session_state.journal_unlocked = True
                st.session_state.journal_password_attempt = 0
                st.rerun()
            else:
                st.session_state.journal_password_attempt += 1
                remaining = 3 - st.session_state.journal_password_attempt
                if remaining > 0:
                    st.error(f"❌ Wrong password! {remaining} attempts remaining")
                else:
                    st.error("🔒 Too many failed attempts. Restart the app to try again.")
                    st.stop()
else:
    st.success("🔓 Journal Unlocked")
    history_file = "trade_history.csv"
    if os.path.exists(history_file):
        try:
            trade_df = pd.read_csv(history_file)
            if not trade_df.empty:
                display_cols = ['tradingsymbol', 'netqty', 'buyavgprice', 'sellavgprice', 'pnl', 'status', 'time']
                available_cols = [c for c in display_cols if c in trade_df.columns]
                trade_df = trade_df[available_cols]
                if 'pnl' in trade_df.columns:
                    trade_df['pnl'] = trade_df['pnl'].astype(float).round(0).astype(int)
                if 'buyavgprice' in trade_df.columns:
                    trade_df['buyavgprice'] = trade_df['buyavgprice'].astype(float).round(2)
                if 'sellavgprice' in trade_df.columns:
                    trade_df['sellavgprice'] = trade_df['sellavgprice'].astype(float).round(2)
                
                total_trades = len(trade_df)
                winning_trades = len(trade_df[trade_df['status'] == 'PROFIT']) if 'status' in trade_df.columns else 0
                total_pnl = trade_df['pnl'].sum() if 'pnl' in trade_df.columns else 0
                
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    st.metric("📊 Total Trades", total_trades)
                with col_s2:
                    win_rate = round((winning_trades / total_trades) * 100, 1) if total_trades > 0 else 0
                    st.metric("🏆 Win Rate", f"{win_rate}%")
                with col_s3:
                    pnl_color = "#00ff88" if total_pnl >= 0 else "#ff4b4b"
                    st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='color:#9ca3af;'>💰 Total P&L</span><br>
                        <span style='color:{pnl_color}; font-size:24px; font-weight:bold;'>₹{total_pnl:,}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("#### 📅 Filter Options")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    if 'time' in trade_df.columns:
                        trade_df['date'] = pd.to_datetime(trade_df['time']).dt.date
                        unique_dates = sorted(trade_df['date'].unique(), reverse=True)
                        selected_date = st.selectbox("Select Date", ["All"] + unique_dates)
                        if selected_date != "All":
                            trade_df = trade_df[trade_df['date'] == selected_date]
                with col_f2:
                    if 'status' in trade_df.columns:
                        status_filter = st.selectbox("Filter by Status", ["All", "PROFIT", "LOSS", "HOLD"])
                        if status_filter != "All":
                            trade_df = trade_df[trade_df['status'] == status_filter]
                
                st.markdown("#### 📋 Trade History")
                st.dataframe(trade_df, use_container_width=True, height=400)
                
                csv = trade_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Trade History (CSV)",
                    data=csv,
                    file_name=f"trade_journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("📭 No trade history found")
        except Exception as e:
            st.warning(f"Could not load trade history: {e}")
    else:
        st.info("📭 No trade history file found. Trades will be recorded automatically.")
    
    if st.button("🔒 LOCK JOURNAL", use_container_width=True):
        st.session_state.journal_unlocked = False
        st.rerun()

now_time = datetime.now().time()
time_allowed = True

if market == "NIFTY":
    default_start = datetime.now().replace(hour=9, minute=15).time()
    default_end = datetime.now().replace(hour=15, minute=15).time()
    time_allowed = default_start <= now_time <= default_end
elif market in ["CRUDEOIL", "NATURALGAS"]:
    default_start = datetime.now().replace(hour=9, minute=0).time()
    default_end = datetime.now().replace(hour=23, minute=30).time()
    time_allowed = default_start <= now_time <= default_end

# ===== TRADE CONDITIONS CALCULATION (Pine Script Match) =====
if not df_live.empty and len(df_live) >= 20:
    c1 = df_live.iloc[-2]
    c2 = df_live.iloc[-1]
    
    ema9 = df_live['ema9'].iloc[-1] if 'ema9' in df_live.columns else None
    ema20 = df_live['ema20'].iloc[-1] if 'ema20' in df_live.columns else None
    ema200 = df_live['ema200'].iloc[-1] if 'ema200' in df_live.columns else None
    
    strong_bull = c2['close'] > c2['open'] and c2['close'] > c1['high']
    strong_bear = c2['close'] < c2['open'] and c2['close'] < c1['low']
    
    volume_filter = c2['volume'] > df_live['volume'].rolling(20).mean().iloc[-1] if 'volume' in df_live.columns else True
    
    rsi = df_live['rsi'].iloc[-1] if 'rsi' in df_live.columns else 50
    adx = df_live['adx'].iloc[-1] if 'adx' in df_live.columns else 0
    sideways = (45 < rsi < 55) and adx < 20
    
    nifty_positive = "BULLISH" in intel['Trend'] if intel else True
    nifty_negative = "BEARISH" in intel['Trend'] if intel else False
    
    trend_5m_up = df_live['ema9'].iloc[-1] > df_live['ema20'].iloc[-1] if 'ema9' in df_live.columns else False
    
    if not df_15m.empty and 'ema9' in df_15m.columns:
        trend_15m_up = df_15m['ema9'].iloc[-1] > df_15m['ema20'].iloc[-1]
        trend_15m_down = df_15m['ema9'].iloc[-1] < df_15m['ema20'].iloc[-1]
    else:
        trend_15m_up = True
        trend_15m_down = True
    
    df_1h = yf.download(symbol, period="5d", interval="60m", progress=False, auto_adjust=False)
    df_1h = clean_df(df_1h)
    if not df_1h.empty and 'ema9' in df_1h.columns and 'ema20' in df_1h.columns:
        df_1h['ema9_1h'] = ta.ema(df_1h['close'], 9)
        df_1h['ema20_1h'] = ta.ema(df_1h['close'], 20)
        trend_1h_up = df_1h['ema9_1h'].iloc[-1] > df_1h['ema20_1h'].iloc[-1] if not df_1h.empty else True
    else:
        trend_1h_up = True
    
    strong_bull_stock = (
        ema9 is not None and ema20 is not None and ema9 > ema20 and
        c2['close'] > ema200 if ema200 is not None else True and
        rsi >= 60 and
        adx >= 25 and
        volume_filter and
        strong_bull and
        c2['close'] > c1['high']
    )
    
    strong_bear_stock = (
        ema9 is not None and ema20 is not None and ema9 < ema20 and
        c2['close'] < ema200 if ema200 is not None else True and
        rsi <= 40 and
        adx >= 25 and
        volume_filter and
        strong_bear and
        c2['close'] < c1['low']
    )
    
    sector_bullish = True
    sector_bearish = False
    
    buy_condition = (
        nifty_positive and
        not nifty_negative and
        not sideways and
        sector_bullish and
        strong_bull_stock and
        trend_5m_up and
        trend_15m_up and
        trend_1h_up and
        c2['close'] > ema20 if ema20 is not None else True
    )
    
    sell_condition = (
        nifty_negative and
        not nifty_positive and
        not sideways and
        sector_bearish and
        strong_bear_stock and
        not trend_5m_up and
        not trend_15m_up and
        not trend_1h_up and
        c2['close'] < ema20 if ema20 is not None else True
    )
    
    if market == "CRUDEOIL":
        buy_condition = buy_condition and crude_change > 0
        sell_condition = sell_condition and crude_change < 0
    elif market == "NATURALGAS":
        buy_condition = buy_condition and ng_change > 0
        sell_condition = sell_condition and ng_change < 0
    
    cooldown_ok = (datetime.now() - st.session_state.last_trade_time).seconds > 300
    st.session_state.nifty_buy_signal = buy_condition
    st.session_state.nifty_sell_signal = sell_condition
else:
    buy_condition = False
    sell_condition = False
    cooldown_ok = False

# ===== AUTO TRADING LOGIC =====
now_time = datetime.now().time()
today = datetime.now().date()

if today != st.session_state.last_trade_date:
    st.session_state.nifty_trades_today = 0
    st.session_state.crude_trades_today = 0
    st.session_state.ng_trades_today = 0
    st.session_state.last_trade_date = today
    st.session_state.last_trade_side = ""

time_allowed = False

if market == "NIFTY":
    start_time = datetime.now().replace(hour=9, minute=30).time()
    end_time = datetime.now().replace(hour=14, minute=30).time()
    square_off_time = datetime.now().replace(hour=15, minute=0).time()
    time_allowed = start_time <= now_time <= end_time
    max_trades = 2
    current_trades = st.session_state.nifty_trades_today
elif market == "CRUDEOIL":
    start_time = datetime.now().replace(hour=18, minute=0).time()
    end_time = datetime.now().replace(hour=22, minute=30).time()
    square_off_time = datetime.now().replace(hour=23, minute=0).time()
    time_allowed = start_time <= now_time <= end_time
    max_trades = 2
    current_trades = st.session_state.crude_trades_today
elif market == "NATURALGAS":
    start_time = datetime.now().replace(hour=18, minute=0).time()
    end_time = datetime.now().replace(hour=22, minute=30).time()
    square_off_time = datetime.now().replace(hour=23, minute=0).time()
    time_allowed = start_time <= now_time <= end_time
    max_trades = 2
    current_trades = st.session_state.ng_trades_today

if now_time >= square_off_time:
    if st.session_state.active:
        try:
            if st.session_state.side == "BUY":
                api.placeOrder({
                    "variety": "NORMAL",
                    "tradingsymbol": asset['symbol'],
                    "symboltoken": asset['token'],
                    "transactiontype": "SELL",
                    "exchange": asset['exch'],
                    "ordertype": "MARKET",
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "quantity": str(num_lots * lot_size)
                })
            elif st.session_state.side == "SELL":
                api.placeOrder({
                    "variety": "NORMAL",
                    "tradingsymbol": asset['symbol'],
                    "symboltoken": asset['token'],
                    "transactiontype": "BUY",
                    "exchange": asset['exch'],
                    "ordertype": "MARKET",
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "quantity": str(num_lots * lot_size)
                })
            st.warning(f"⏰ AUTO SQUARE OFF at {square_off_time}")
            send_alert(f"AUTO SQUARE OFF {market}")
            st.session_state.active = False
            st.session_state.last_trade_side = ""
        except:
            pass
    time_allowed = False

trade_limit_reached = current_trades >= max_trades

if trade_limit_reached:
    st.info(f"📊 Daily trade limit reached for {market} ({current_trades}/{max_trades} trades)")
    time_allowed = False

if st.session_state.algo_running and time_allowed and not trade_limit_reached and not df_live.empty and len(df_live) >= 20:
    
    if buy_condition and cooldown_ok and st.session_state.last_trade_side != "BUY":
        try:
            current_price = float(df_live['close'].iloc[-1])
            total_quantity = num_lots * lot_size
            
            api.placeOrder({
                "variety": "NORMAL",
                "tradingsymbol": asset['symbol'],
                "symboltoken": asset['token'],
                "transactiontype": "BUY",
                "exchange": asset['exch'],
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": str(total_quantity)
            })
            
            st.success(f"🚀 BUY {total_quantity} qty @ {current_price}")
            send_alert(f"🚀 BUY {market} | Qty: {total_quantity} | Price: {current_price}")
            
            if market == "NIFTY":
                st.session_state.nifty_trades_today += 1
            elif market == "CRUDEOIL":
                st.session_state.crude_trades_today += 1
            elif market == "NATURALGAS":
                st.session_state.ng_trades_today += 1
            
            st.session_state.last_trade_side = "BUY"
            st.session_state.last_trade_time = datetime.now()
            st.session_state.active = True
            st.session_state.side = "BUY"
            st.session_state.entry = current_price
            winsound.Beep(1000, 500)
        except Exception as e:
            st.error(f"BUY ERROR: {e}")
    
    if sell_condition and cooldown_ok and st.session_state.last_trade_side != "SELL":
        try:
            current_price = float(df_live['close'].iloc[-1])
            total_quantity = num_lots * lot_size
            
            api.placeOrder({
                "variety": "NORMAL",
                "tradingsymbol": asset['symbol'],
                "symboltoken": asset['token'],
                "transactiontype": "SELL",
                "exchange": asset['exch'],
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": str(total_quantity)
            })
            
            st.success(f"🔻 SELL {total_quantity} qty @ {current_price}")
            send_alert(f"🔻 SELL {market} | Qty: {total_quantity} | Price: {current_price}")
            
            if market == "NIFTY":
                st.session_state.nifty_trades_today += 1
            elif market == "CRUDEOIL":
                st.session_state.crude_trades_today += 1
            elif market == "NATURALGAS":
                st.session_state.ng_trades_today += 1
            
            st.session_state.last_trade_side = "SELL"
            st.session_state.last_trade_time = datetime.now()
            st.session_state.active = True
            st.session_state.side = "SELL"
            st.session_state.entry = current_price
            winsound.Beep(700, 500)
        except Exception as e:
            st.error(f"SELL ERROR: {e}")

# ===== STOP LOSS MANAGEMENT =====
if st.session_state.active and not df_live.empty and len(df_live) >= 2:
    try:
        current_price = float(df_live['close'].iloc[-1])
        current_ema9 = df_live['ema9'].iloc[-1] if 'ema9' in df_live.columns else None
        if current_ema9 and not pd.isna(current_ema9):
            if st.session_state.side == "BUY" and current_price < current_ema9:
                api.placeOrder({
                    "variety": "NORMAL",
                    "tradingsymbol": asset['symbol'],
                    "symboltoken": asset['token'],
                    "transactiontype": "SELL",
                    "exchange": asset['exch'],
                    "ordertype": "MARKET",
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "quantity": str(num_lots * lot_size)
                })
                st.warning(f"🛑 BUY STOP LOSS HIT at {current_price}")
                send_alert(f"🛑 STOP LOSS | {market} BUY | Exit: {current_price}")
                st.session_state.active = False
                winsound.Beep(500, 300)
            elif st.session_state.side == "SELL" and current_price > current_ema9:
                api.placeOrder({
                    "variety": "NORMAL",
                    "tradingsymbol": asset['symbol'],
                    "symboltoken": asset['token'],
                    "transactiontype": "BUY",
                    "exchange": asset['exch'],
                    "ordertype": "MARKET",
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "quantity": str(num_lots * lot_size)
                })
                st.warning(f"🛑 SELL STOP LOSS HIT at {current_price}")
                send_alert(f"🛑 STOP LOSS | {market} SELL | Exit: {current_price}")
                st.session_state.active = False
                winsound.Beep(500, 300)
    except:
        pass

# ===== DISPLAY TRADE STATUS =====
if st.session_state.active:
    st.success(f"⚡ ACTIVE TRADE: {st.session_state.side} | Entry: {st.session_state.entry}")
elif st.session_state.algo_running:
    st.info("🟢 ALGO RUNNING - Waiting for signal...")

st.caption("🔄 Auto Refresh Every 10 Seconds")
st_autorefresh(interval=10000, key="live_refresh")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, threaded=True)