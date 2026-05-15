import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO-ALGO X", layout="wide", page_icon="🇮🇳")

# ================= IST Timezone =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= APP LOCK SESSION STATE =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False
if "app_password" not in st.session_state:
    st.session_state.app_password = "RUDRANSH@2025"  # तुमचा password इथे set करा

# ================= APP LOCK SCREEN =================
if not st.session_state.app_unlocked:
    st.markdown("<h1 style='text-align:center;'>🇮🇳 RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>🔐 APPLICATION LOCKED</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Enter Password to Access the Application</p>", unsafe_allow_html=True)
    
    password_input = st.text_input("Password", type="password", placeholder="Enter password", key="app_lock_password")
    
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔓 UNLOCK", use_container_width=True):
            if password_input == st.session_state.app_password:
                st.session_state.app_unlocked = True
                st.rerun()
            else:
                st.error("❌ Wrong Password! Access Denied.")
    
    st.stop()  # Stop execution until password is entered

# ================= FIXED TARGETS =================
FIXED_TARGETS = {
    "NIFTY": 10,
    "CRUDEOIL": 10,
    "NATURALGAS": 1,
}

# ================= TRADE COUNTERS (Max 2 Trades per Asset) =================
if "nifty_trades_count" not in st.session_state:
    st.session_state.nifty_trades_count = 0
if "crude_trades_count" not in st.session_state:
    st.session_state.crude_trades_count = 0
if "ng_trades_count" not in st.session_state:
    st.session_state.ng_trades_count = 0

# ================= MAX QUANTITY LIMIT =================
MAX_QTY_OPTIONS = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]

def calculate_trade_quantity(lot_size, max_qty_limit, enable_big_lot_mode=False, big_lot_qty=None):
    if enable_big_lot_mode and big_lot_qty:
        return big_lot_qty, big_lot_qty // lot_size
    max_lots = max_qty_limit // lot_size
    if max_lots < 1:
        max_lots = 1
    quantity = max_lots * lot_size
    return quantity, max_lots

# ================= SYMBOLS =================
SYMBOLS = {
    "NIFTY": "^NSEI",
    "CRUDEOIL": "CL=F",
    "NATURALGAS": "NG=F"
}

# ================= USD/INR RATE =================
def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if df.empty:
            df = yf.download("INR=X", period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            rate = df['Close'].iloc[-1]
            if isinstance(rate, pd.Series):
                rate = float(rate.iloc[-1])
            return rate
    except:
        pass
    return 87.5

def get_live_price(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            val = df['Close'].iloc[-1]
            if isinstance(val, pd.Series):
                val = float(val.iloc[-1]) if not val.empty else 0.0
            return float(val)
    except:
        pass
    return 0.0

def get_live_price_inr(symbol):
    price_usd = get_live_price(symbol)
    if price_usd > 0:
        usd_inr = get_usd_inr_rate()
        return price_usd * usd_inr
    return 0.0

def get_itm_strike_nifty(price, itm_points=100, strike_interval=50):
    if price <= 0:
        return 0, 0
    target_strike = price - itm_points
    rounded_strike = round(target_strike / strike_interval) * strike_interval
    if rounded_strike < 100:
        rounded_strike = 100
    actual_itm = price - rounded_strike
    return int(rounded_strike), actual_itm

# ================= AUTO ITM STRIKE DETECTION =================
def get_stock_itm_strike_auto(price, stock, option_type="CE", strike_offset=2):
    if price <= 0:
        return 0, 0, 50
    
    if price < 100:
        strike_interval = 2.5
    elif price < 250:
        strike_interval = 5
    elif price < 500:
        strike_interval = 10
    elif price < 1000:
        strike_interval = 20
    elif price < 2000:
        strike_interval = 50
    elif price < 5000:
        strike_interval = 100
    else:
        strike_interval = 200
    
    atm_strike = round(price / strike_interval) * strike_interval
    
    if option_type == "CE":
        itm_strike = atm_strike - (strike_offset * strike_interval)
        actual_itm = price - itm_strike
    else:
        itm_strike = atm_strike + (strike_offset * strike_interval)
        actual_itm = itm_strike - price
    
    if itm_strike <= 0:
        itm_strike = strike_interval
    
    return int(itm_strike), round(actual_itm, 2), strike_interval

# ================= GLOBAL TREND FUNCTIONS =================
def get_us_market_trend():
    try:
        spx = yf.download("^GSPC", period="7d", interval="15m", progress=False)
        nasdaq = yf.download("^IXIC", period="7d", interval="15m", progress=False)
        dow = yf.download("^DJI", period="7d", interval="15m", progress=False)
        
        trends = []
        
        if not spx.empty and 'Close' in spx.columns:
            ema20_spx = spx['Close'].ewm(span=20).mean().iloc[-1]
            current_spx = spx['Close'].iloc[-1]
            trends.append("BULLISH" if current_spx > ema20_spx else "BEARISH")
        
        if not nasdaq.empty and 'Close' in nasdaq.columns:
            ema20_nasdaq = nasdaq['Close'].ewm(span=20).mean().iloc[-1]
            current_nasdaq = nasdaq['Close'].iloc[-1]
            trends.append("BULLISH" if current_nasdaq > ema20_nasdaq else "BEARISH")
        
        if not dow.empty and 'Close' in dow.columns:
            ema20_dow = dow['Close'].ewm(span=20).mean().iloc[-1]
            current_dow = dow['Close'].iloc[-1]
            trends.append("BULLISH" if current_dow > ema20_dow else "BEARISH")
        
        if not trends:
            return "NEUTRAL"
        
        bullish_count = trends.count("BULLISH")
        if bullish_count >= 2:
            return "BULLISH"
        elif bullish_count <= 1:
            return "BEARISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_asia_market_trend():
    try:
        nikkei = yf.download("^N225", period="7d", interval="15m", progress=False)
        hangseng = yf.download("^HSI", period="7d", interval="15m", progress=False)
        shanghai = yf.download("000001.SS", period="7d", interval="15m", progress=False)
        
        trends = []
        
        if not nikkei.empty and 'Close' in nikkei.columns:
            ema20_nikkei = nikkei['Close'].ewm(span=20).mean().iloc[-1]
            current_nikkei = nikkei['Close'].iloc[-1]
            trends.append("BULLISH" if current_nikkei > ema20_nikkei else "BEARISH")
        
        if not hangseng.empty and 'Close' in hangseng.columns:
            ema20_hangseng = hangseng['Close'].ewm(span=20).mean().iloc[-1]
            current_hangseng = hangseng['Close'].iloc[-1]
            trends.append("BULLISH" if current_hangseng > ema20_hangseng else "BEARISH")
        
        if not shanghai.empty and 'Close' in shanghai.columns:
            ema20_shanghai = shanghai['Close'].ewm(span=20).mean().iloc[-1]
            current_shanghai = shanghai['Close'].iloc[-1]
            trends.append("BULLISH" if current_shanghai > ema20_shanghai else "BEARISH")
        
        if not trends:
            return "NEUTRAL"
        
        bullish_count = trends.count("BULLISH")
        if bullish_count >= 2:
            return "BULLISH"
        elif bullish_count <= 1:
            return "BEARISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_dxy_trend():
    try:
        dxy = yf.download("DX-Y.NYB", period="7d", interval="15m", progress=False)
        if dxy.empty or 'Close' not in dxy.columns:
            return "NEUTRAL"
        
        ema20_dxy = dxy['Close'].ewm(span=20).mean().iloc[-1]
        current_dxy = dxy['Close'].iloc[-1]
        
        if current_dxy > ema20_dxy:
            return "BEARISH"
        elif current_dxy < ema20_dxy:
            return "BULLISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_global_trend():
    us_trend = get_us_market_trend()
    asia_trend = get_asia_market_trend()
    dxy_trend = get_dxy_trend()
    
    scores = []
    scores.append(1 if us_trend == "BULLISH" else -1 if us_trend == "BEARISH" else 0)
    scores.append(1 if asia_trend == "BULLISH" else -1 if asia_trend == "BEARISH" else 0)
    scores.append(1 if dxy_trend == "BULLISH" else -1 if dxy_trend == "BEARISH" else 0)
    
    total_score = sum(scores)
    
    if total_score >= 2:
        return "BULLISH", us_trend, asia_trend, dxy_trend
    elif total_score <= -2:
        return "BEARISH", us_trend, asia_trend, dxy_trend
    else:
        return "NEUTRAL", us_trend, asia_trend, dxy_trend

# ================= 69 F&O STOCKS =================
FO_STOCKS = [
    {"symbol": "RELIANCE.NS", "lot": 500, "name": "RELIANCE", "sector": "ENERGY", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "TCS.NS", "lot": 174, "name": "TCS", "sector": "IT", "tp1": 4, "tp2": 4, "big_lot_qty": 5220, "big_lot_lots": 30},
    {"symbol": "HDFCBANK.NS", "lot": 550, "name": "HDFC BANK", "sector": "BANK", "tp1": 3, "tp2": 3, "big_lot_qty": 7150, "big_lot_lots": 13},
    {"symbol": "INFY.NS", "lot": 400, "name": "INFOSYS", "sector": "IT", "tp1": 3, "tp2": 3, "big_lot_qty": 6800, "big_lot_lots": 17},
    {"symbol": "ICICIBANK.NS", "lot": 700, "name": "ICICI BANK", "sector": "BANK", "tp1": 2, "tp2": 2, "big_lot_qty": 10500, "big_lot_lots": 15},
    {"symbol": "SBIN.NS", "lot": 750, "name": "SBI", "sector": "BANK", "tp1": 3, "tp2": 2, "big_lot_qty": 8250, "big_lot_lots": 11},
    {"symbol": "BHARTIARTL.NS", "lot": 476, "name": "BHARTI AIRTEL", "sector": "TELECOM", "tp1": 3, "tp2": 3, "big_lot_qty": 7616, "big_lot_lots": 16},
    {"symbol": "KOTAKBANK.NS", "lot": 2000, "name": "KOTAK BANK", "sector": "BANK", "tp1": 3, "tp2": 3, "big_lot_qty": 8000, "big_lot_lots": 4},
    {"symbol": "BAJFINANCE.NS", "lot": 750, "name": "BAJAJ FINANCE", "sector": "FINANCE", "tp1": 3, "tp2": 3, "big_lot_qty": 6750, "big_lot_lots": 9},
    {"symbol": "ITC.NS", "lot": 1600, "name": "ITC", "sector": "FMCG", "tp1": 1, "tp2": 1, "big_lot_qty": 20800, "big_lot_lots": 13},
    {"symbol": "HINDUNILVR.NS", "lot": 300, "name": "HUL", "sector": "FMCG", "tp1": 3, "tp2": 3, "big_lot_qty": 6900, "big_lot_lots": 23},
    {"symbol": "TATAMOTORS.NS", "lot": 800, "name": "TMPV", "sector": "AUTO", "tp1": 0.75, "tp2": 0.75, "big_lot_qty": 27200, "big_lot_lots": 34},
    {"symbol": "TATASTEEL.NS", "lot": 600, "name": "TATA STEEL", "sector": "METAL", "tp1": 1, "tp2": 1, "big_lot_qty": 20400, "big_lot_lots": 34},
    {"symbol": "AXISBANK.NS", "lot": 624, "name": "AXIS BANK", "sector": "BANK", "tp1": 3, "tp2": 3, "big_lot_qty": 7488, "big_lot_lots": 12},
    {"symbol": "MARUTI.NS", "lot": 50, "name": "MARUTI", "sector": "AUTO", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 80},
    {"symbol": "SUNPHARMA.NS", "lot": 350, "name": "SUN PHARMA", "sector": "PHARMA", "tp1": 3, "tp2": 3, "big_lot_qty": 7000, "big_lot_lots": 20},
    {"symbol": "WIPRO.NS", "lot": 3000, "name": "WIPRO", "sector": "IT", "tp1": 0.50, "tp2": 0.50, "big_lot_qty": 42000, "big_lot_lots": 14},
    {"symbol": "HCLTECH.NS", "lot": 350, "name": "HCL TECH", "sector": "IT", "tp1": 3, "tp2": 3, "big_lot_qty": 7000, "big_lot_lots": 20},
    {"symbol": "NTPC.NS", "lot": 1500, "name": "NTPC", "sector": "ENERGY", "tp1": 0.50, "tp2": 0.50, "big_lot_qty": 40500, "big_lot_lots": 27},
    {"symbol": "POWERGRID.NS", "lot": 1900, "name": "POWER GRID", "sector": "ENERGY", "tp1": 0.75, "tp2": 0.75, "big_lot_qty": 28500, "big_lot_lots": 15},
    {"symbol": "ONGC.NS", "lot": 2250, "name": "ONGC", "sector": "ENERGY", "tp1": 0.50, "tp2": 0.50, "big_lot_qty": 40500, "big_lot_lots": 18},
    {"symbol": "M&M.NS", "lot": 200, "name": "M&M", "sector": "AUTO", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 10},
    {"symbol": "ULTRACEMCO.NS", "lot": 50, "name": "ULTRATECH", "sector": "INFRA", "tp1": 20, "tp2": 20, "big_lot_qty": 1000, "big_lot_lots": 20},
    {"symbol": "NESTLEIND.NS", "lot": 500, "name": "NESTLE", "sector": "FMCG", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "JSWSTEEL.NS", "lot": 674, "name": "JSW STEEL", "sector": "METAL", "tp1": 5, "tp2": 5, "big_lot_qty": 4044, "big_lot_lots": 6},
    {"symbol": "TECHM.NS", "lot": 600, "name": "TECH MAHINDRA", "sector": "IT", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 7},
    {"symbol": "BAJAJFINSV.NS", "lot": 250, "name": "BAJAJ FINSERV", "sector": "FINANCE", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 16},
    {"symbol": "ASIANPAINT.NS", "lot": 250, "name": "ASIAN PAINTS", "sector": "CONSUMER", "tp1": 4, "tp2": 4, "big_lot_qty": 5000, "big_lot_lots": 20},
    {"symbol": "GRASIM.NS", "lot": 250, "name": "GRASIM", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 16},
    {"symbol": "INDUSINDBK.NS", "lot": 700, "name": "INDUSIND BANK", "sector": "BANK", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 6},
    {"symbol": "BRITANNIA.NS", "lot": 124, "name": "BRITANNIA", "sector": "FMCG", "tp1": 5, "tp2": 5, "big_lot_qty": 4216, "big_lot_lots": 34},
    {"symbol": "DRREDDY.NS", "lot": 624, "name": "DR REDDY", "sector": "PHARMA", "tp1": 5, "tp2": 5, "big_lot_qty": 4992, "big_lot_lots": 8},
    {"symbol": "DIVISLAB.NS", "lot": 100, "name": "DIVIS LAB", "sector": "PHARMA", "tp1": 15, "tp2": 15, "big_lot_qty": 1400, "big_lot_lots": 14},
    {"symbol": "HAL.NS", "lot": 150, "name": "HAL", "sector": "DEFENCE", "tp1": 10, "tp2": 10, "big_lot_qty": 2100, "big_lot_lots": 14},
    {"symbol": "ADANIENT.NS", "lot": 308, "name": "ADANI ENTERPRISES", "sector": "ENERGY", "tp1": 5, "tp2": 5, "big_lot_qty": 4312, "big_lot_lots": 14},
    {"symbol": "ADANIPORTS.NS", "lot": 476, "name": "ADANI PORTS", "sector": "ENERGY", "tp1": 3, "tp2": 3, "big_lot_qty": 7616, "big_lot_lots": 16},
    {"symbol": "HEROMOTOCO.NS", "lot": 150, "name": "HERO MOTOCORP", "sector": "AUTO", "tp1": 10, "tp2": 10, "big_lot_qty": 2100, "big_lot_lots": 14},
    {"symbol": "EICHERMOT.NS", "lot": 100, "name": "EICHER MOTORS", "sector": "AUTO", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 20},
    {"symbol": "PIDILITIND.NS", "lot": 500, "name": "PIDILITE", "sector": "CONSUMER", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "DABUR.NS", "lot": 1250, "name": "DABUR", "sector": "FMCG", "tp1": 2, "tp2": 2, "big_lot_qty": 10000, "big_lot_lots": 8},
    {"symbol": "HAVELLS.NS", "lot": 500, "name": "HAVELLS", "sector": "CONSUMER", "tp1": 3, "tp2": 3, "big_lot_qty": 7000, "big_lot_lots": 14},
    {"symbol": "UPL.NS", "lot": 1356, "name": "UPL", "sector": "CHEMICAL", "tp1": 3, "tp2": 3, "big_lot_qty": 8136, "big_lot_lots": 6},
    {"symbol": "LT.NS", "lot": 174, "name": "LT", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4176, "big_lot_lots": 24},
    {"symbol": "ADANIGREEN.NS", "lot": 600, "name": "ADANI GREEN", "sector": "ENERGY", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 7},
    {"symbol": "VEDANTA.NS", "lot": 1150, "name": "VEDANTA", "sector": "METAL", "tp1": 3, "tp2": 3, "big_lot_qty": 6900, "big_lot_lots": 6},
    {"symbol": "ABB.NS", "lot": 125, "name": "ABB", "sector": "INFRA", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 16},
    {"symbol": "TITAN.NS", "lot": 175, "name": "TITAN", "sector": "CONSUMER", "tp1": 10, "tp2": 10, "big_lot_qty": 2100, "big_lot_lots": 12},
    {"symbol": "INDIGO.NS", "lot": 150, "name": "INDIGO", "sector": "TRAVEL", "tp1": 5, "tp2": 5, "big_lot_qty": 4050, "big_lot_lots": 27},
    {"symbol": "BAJAJ-AUTO.NS", "lot": 50, "name": "BAJAJAUTO", "sector": "AUTO", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 40},
    {"symbol": "TVSMOTOR.NS", "lot": 175, "name": "TVSMOTOR", "sector": "AUTO", "tp1": 5, "tp2": 5, "big_lot_qty": 4025, "big_lot_lots": 23},
    {"symbol": "COFORGE.NS", "lot": 375, "name": "COFORGE", "sector": "IT", "tp1": 5, "tp2": 5, "big_lot_qty": 4125, "big_lot_lots": 11},
    {"symbol": "PERSISTENT.NS", "lot": 100, "name": "PERSISTENT", "sector": "IT", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 20},
    {"symbol": "LUPIN.NS", "lot": 425, "name": "LUPIN", "sector": "PHARMA", "tp1": 5, "tp2": 5, "big_lot_qty": 4250, "big_lot_lots": 10},
    {"symbol": "AUROPHARMA.NS", "lot": 550, "name": "AUROPHARMA", "sector": "PHARMA", "tp1": 5, "tp2": 5, "big_lot_qty": 4400, "big_lot_lots": 8},
    {"symbol": "HINDALCO.NS", "lot": 700, "name": "HINDALCO", "sector": "METAL", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 6},
    {"symbol": "DMART.NS", "lot": 150, "name": "DMART", "sector": "CONSUMER", "tp1": 5, "tp2": 5, "big_lot_qty": 4050, "big_lot_lots": 27},
    {"symbol": "GODREJPROP.NS", "lot": 275, "name": "GODREJPROP", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4125, "big_lot_lots": 15},
    {"symbol": "JSWENERGY.NS", "lot": 1000, "name": "JSWENERGY", "sector": "ENERGY", "tp1": 3, "tp2": 3, "big_lot_qty": 7000, "big_lot_lots": 7},
    {"symbol": "CHOLAFIN.NS", "lot": 625, "name": "CHOLAFIN", "sector": "FINANCE", "tp1": 5, "tp2": 5, "big_lot_qty": 4375, "big_lot_lots": 7},
    {"symbol": "SHRIRAMFIN.NS", "lot": 825, "name": "SHRIRAMFIN", "sector": "FINANCE", "tp1": 5, "tp2": 5, "big_lot_qty": 4125, "big_lot_lots": 5},
    {"symbol": "SIEMENS.NS", "lot": 175, "name": "SIEMENS", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4025, "big_lot_lots": 23},
    {"symbol": "KEI.NS", "lot": 175, "name": "KEI", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4025, "big_lot_lots": 23},
    {"symbol": "POLYCAB.NS", "lot": 125, "name": "POLYCAB", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 32},
    {"symbol": "APOLLOHOSP.NS", "lot": 125, "name": "APOLLOHOSP", "sector": "HEALTHCARE", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 32},
    {"symbol": "MAXHEALTH.NS", "lot": 525, "name": "MAXHEALTH", "sector": "HEALTHCARE", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 8},
    {"symbol": "AMBER.NS", "lot": 100, "name": "AMBER", "sector": "CONSUMER", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 20},
    {"symbol": "VOLTAS.NS", "lot": 375, "name": "VOLTAS", "sector": "CONSUMER", "tp1": 10, "tp2": 10, "big_lot_qty": 2250, "big_lot_lots": 6},
    {"symbol": "MCX.NS", "lot": 225, "name": "MCX", "sector": "FINANCE", "tp1": 5, "tp2": 5, "big_lot_qty": 4050, "big_lot_lots": 18},
    {"symbol": "TRENT.NS", "lot": 100, "name": "TRENT", "sector": "CONSUMER", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 40},
]

# ================= SECTOR MAPPING =================
SECTOR_INDEX = {
    "BANK": "^NSEBANK", "IT": "^CNXIT", "AUTO": "^CNXAUTO", "PHARMA": "^CNXPHARMA",
    "METAL": "^CNXMETAL", "FMCG": "^CNXFMCG", "FINANCE": "^CNXFINANCE", "ENERGY": "^CNXENERGY",
    "INFRA": "^CNXINFRA", "DEFENCE": "^CNXINFRA", "CONSUMER": "^NIFTY_CONSR_DURBL", 
    "TELECOM": "^CNXIT", "CHEMICAL": "^NIFTY_CHEMICAL", "HEALTHCARE": "^NIFTY_HEALTHCARE",
    "TRAVEL": "^CNXSERVICE",
}

# ================= SESSION STATE =================
if "algo_running" not in st.session_state:
    st.session_state.algo_running = False
if "totp_verified" not in st.session_state:
    st.session_state.totp_verified = False
if "enable_nifty" not in st.session_state:
    st.session_state.enable_nifty = True
if "enable_crude" not in st.session_state:
    st.session_state.enable_crude = True
if "enable_ng" not in st.session_state:
    st.session_state.enable_ng = True
if "enable_stocks" not in st.session_state:
    st.session_state.enable_stocks = True
if "nifty_lots" not in st.session_state:
    st.session_state.nifty_lots = 1
if "crude_lots" not in st.session_state:
    st.session_state.crude_lots = 1
if "ng_lots" not in st.session_state:
    st.session_state.ng_lots = 1
if "max_qty_limit" not in st.session_state:
    st.session_state.max_qty_limit = 1500
if "enable_big_lot_mode" not in st.session_state:
    st.session_state.enable_big_lot_mode = False
if "trade_journal" not in st.session_state:
    st.session_state.trade_journal = []
if "stock_trades" not in st.session_state:
    st.session_state.stock_trades = {}
    for stock in FO_STOCKS:
        qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit, False, stock.get("big_lot_qty"))
        st.session_state.stock_trades[stock["name"]] = {"buy_done": False, "sell_done": False, "trades": 0, "quantity": qty, "lots": lots}
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = get_ist_now().date()
if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0
if "max_stocks_per_day" not in st.session_state:
    st.session_state.max_stocks_per_day = 10

# Reset daily trades
if get_ist_now().date() != st.session_state.last_trade_date:
    for stock in FO_STOCKS:
        qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit, st.session_state.enable_big_lot_mode, stock.get("big_lot_qty"))
        st.session_state.stock_trades[stock["name"]] = {"buy_done": False, "sell_done": False, "trades": 0, "quantity": qty, "lots": lots}
    st.session_state.daily_loss = 0
    st.session_state.nifty_trades_count = 0
    st.session_state.crude_trades_count = 0
    st.session_state.ng_trades_count = 0
    st.session_state.last_trade_date = get_ist_now().date()

MAX_DAILY_LOSS = 100000  # 1 Lakh

def check_daily_loss_limit():
    return abs(st.session_state.daily_loss) >= MAX_DAILY_LOSS

# ================= HELPER FUNCTIONS =================
def get_technical_indicators(df):
    if df.empty or len(df) < 200:
        return None
    close = df['Close']
    high = df['High'] if 'High' in df.columns else close
    low = df['Low'] if 'Low' in df.columns else close
    volume = df['Volume'] if 'Volume' in df.columns else pd.Series([1000000] * len(df))
    
    ema9 = close.ewm(span=9, adjust=False).mean()
    ema20 = close.ewm(span=20, adjust=False).mean()
    ema200 = close.ewm(span=200, adjust=False).mean()
    
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    volume_sma = volume.rolling(20).mean()
    volume_filter = volume.iloc[-1] > volume_sma.iloc[-1] if not volume_sma.isna().iloc[-1] else True
    
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm = plus_dm.where(plus_dm > 0, 0)
    minus_dm = minus_dm.where(minus_dm > 0, 0)
    tr = pd.DataFrame({
        'hl': high - low,
        'hc': abs(high - close.shift()),
        'lc': abs(low - close.shift())
    }).max(axis=1)
    atr = tr.rolling(14).mean()
    
    plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(14).mean() / atr)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(14).mean().iloc[-1] if len(dx) > 14 else 25
    
    c1 = df.iloc[-2]
    c2 = df.iloc[-1]
    strong_bull = c2['Close'] > c2['Open'] and c2['Close'] > c1['High']
    strong_bear = c2['Close'] < c2['Open'] and c2['Close'] < c1['Low']
    
    current_rsi = rsi.iloc[-1]
    sideways = (45 < current_rsi < 55) and adx < 20
    
    return {
        "current_price": close.iloc[-1],
        "ema9": ema9.iloc[-1],
        "ema20": ema20.iloc[-1],
        "ema200": ema200.iloc[-1],
        "rsi": current_rsi,
        "adx": adx,
        "volume_filter": volume_filter,
        "strong_bull": strong_bull,
        "strong_bear": strong_bear,
        "sideways": sideways,
        "c1_high": c1['High'] if 'High' in df.columns else close.iloc[-2],
        "c1_low": c1['Low'] if 'Low' in df.columns else close.iloc[-2]
    }

def get_mtf_trend(symbol, timeframe):
    try:
        df = yf.download(symbol, period="7d", interval=timeframe, progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        close = df['Close']
        ema20 = close.ewm(span=20).mean().iloc[-1]
        current = close.iloc[-1]
        if current > ema20:
            return "UP"
        elif current < ema20:
            return "DOWN"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_nifty_trend():
    try:
        df = yf.download("^NSEI", period="7d", interval="15m", progress=False)
        if not df.empty and 'Close' in df.columns:
            ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
            if isinstance(current, pd.Series):
                current = float(current.iloc[-1])
            if isinstance(ema20, pd.Series):
                ema20 = float(ema20.iloc[-1])
            if current > ema20:
                return "BULLISH"
            elif current < ema20:
                return "BEARISH"
    except:
        pass
    return "NEUTRAL"

def get_sector_bullish(sector_name):
    try:
        index_symbol = SECTOR_INDEX.get(sector_name, "^NSEI")
        df = yf.download(index_symbol, period="7d", interval="15m", progress=False)
        if not df.empty and 'Close' in df.columns:
            ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
            if isinstance(current, pd.Series):
                current = float(current.iloc[-1])
            if isinstance(ema20, pd.Series):
                ema20 = float(ema20.iloc[-1])
            return current > ema20
    except:
        pass
    return False

def get_sector_bearish(sector_name):
    try:
        index_symbol = SECTOR_INDEX.get(sector_name, "^NSEI")
        df = yf.download(index_symbol, period="7d", interval="15m", progress=False)
        if not df.empty and 'Close' in df.columns:
            ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
            if isinstance(current, pd.Series):
                current = float(current.iloc[-1])
            if isinstance(ema20, pd.Series):
                ema20 = float(ema20.iloc[-1])
            return current < ema20
    except:
        pass
    return False

def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
    except:
        pass

# ================= TRADING HOURS =================
def is_nifty_market_open():
    now = get_ist_now()
    if now.hour == 9 and now.minute >= 30:
        return True
    elif 10 <= now.hour < 14:
        return True
    elif now.hour == 14 and now.minute <= 30:
        return True
    return False

def is_commodity_market_open():
    now = get_ist_now()
    if now.hour == 18 and now.minute >= 0:
        return True
    elif 19 <= now.hour < 22:
        return True
    elif now.hour == 22 and now.minute <= 15:
        return True
    return False

def is_stock_market_open():
    now = get_ist_now()
    if now.hour == 9 and now.minute >= 30:
        return True
    elif 10 <= now.hour < 14:
        return True
    elif now.hour == 14 and now.minute <= 30:
        return True
    return False

def get_nifty_signal():
    try:
        df = yf.download("^NSEI", period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return "WAIT", 0
        
        indicators = get_technical_indicators(df)
        if indicators is None:
            return "WAIT", 0
        
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        c1_low_val = indicators["c1_low"]
        
        trend5_up = get_mtf_trend("^NSEI", "5m") == "UP"
        trend15_up = get_mtf_trend("^NSEI", "15m") == "UP"
        trend1h_up = get_mtf_trend("^NSEI", "60m") == "UP"
        
        buy_conditions = (not sideways_val and ema9_val > ema20_val and current_price > ema200_val and
            rsi_val >= 55 and adx_val >= 22 and volume_filter_val and 
            strong_bull_val and current_price > c1_high_val and
            trend5_up and trend15_up and trend1h_up)
        
        sell_conditions = (not sideways_val and ema9_val < ema20_val and current_price < ema200_val and
            rsi_val <= 45 and adx_val >= 22 and volume_filter_val and 
            strong_bear_val and current_price < c1_low_val and
            not trend5_up and not trend15_up and not trend1h_up)
        
        if buy_conditions:
            return "BUY", current_price
        elif sell_conditions:
            return "SELL", current_price
        return "WAIT", current_price
    except:
        return "WAIT", 0

def get_crude_signal():
    try:
        df = yf.download("CL=F", period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return "WAIT", 0
        
        indicators = get_technical_indicators(df)
        if indicators is None:
            return "WAIT", 0
        
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        c1_low_val = indicators["c1_low"]
        
        trend5_up = get_mtf_trend("CL=F", "5m") == "UP"
        trend15_up = get_mtf_trend("CL=F", "15m") == "UP"
        trend1h_up = get_mtf_trend("CL=F", "60m") == "UP"
        
        buy_conditions = (not sideways_val and ema9_val > ema20_val and current_price > ema200_val and
            rsi_val >= 55 and adx_val >= 22 and volume_filter_val and 
            strong_bull_val and current_price > c1_high_val and
            trend5_up and trend15_up and trend1h_up)
        
        sell_conditions = (not sideways_val and ema9_val < ema20_val and current_price < ema200_val and
            rsi_val <= 45 and adx_val >= 22 and volume_filter_val and 
            strong_bear_val and current_price < c1_low_val and
            not trend5_up and not trend15_up and not trend1h_up)
        
        if buy_conditions:
            return "BUY", current_price
        elif sell_conditions:
            return "SELL", current_price
        return "WAIT", current_price
    except:
        return "WAIT", 0

def get_ng_signal():
    try:
        df = yf.download("NG=F", period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return "WAIT", 0
        
        indicators = get_technical_indicators(df)
        if indicators is None:
            return "WAIT", 0
        
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        c1_low_val = indicators["c1_low"]
        
        trend5_up = get_mtf_trend("NG=F", "5m") == "UP"
        trend15_up = get_mtf_trend("NG=F", "15m") == "UP"
        trend1h_up = get_mtf_trend("NG=F", "60m") == "UP"
        
        buy_conditions = (not sideways_val and ema9_val > ema20_val and current_price > ema200_val and
            rsi_val >= 55 and adx_val >= 22 and volume_filter_val and 
            strong_bull_val and current_price > c1_high_val and
            trend5_up and trend15_up and trend1h_up)
        
        sell_conditions = (not sideways_val and ema9_val < ema20_val and current_price < ema200_val and
            rsi_val <= 45 and adx_val >= 22 and volume_filter_val and 
            strong_bear_val and current_price < c1_low_val and
            not trend5_up and not trend15_up and not trend1h_up)
        
        if buy_conditions:
            return "BUY", current_price
        elif sell_conditions:
            return "SELL", current_price
        return "WAIT", current_price
    except:
        return "WAIT", 0

def calculate_signals_stock(symbol, stock_name, sector_name):
    try:
        df = yf.download(symbol, period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return None
        
        df.columns = [str(c).lower() for c in df.columns]
        
        indicators = get_technical_indicators(df)
        if indicators is None:
            return None
        
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        c1_low_val = indicators["c1_low"]
        
        nifty_trend = get_nifty_trend()
        nifty_bullish = nifty_trend == "BULLISH"
        nifty_bearish = nifty_trend == "BEARISH"
        
        sector_bullish = get_sector_bullish(sector_name)
        sector_bearish = get_sector_bearish(sector_name)
        
        trend5_up = get_mtf_trend(symbol, "5m") == "UP"
        trend15_up = get_mtf_trend(symbol, "15m") == "UP"
        trend1h_up = get_mtf_trend(symbol, "60m") == "UP"
        
        buy_conditions = (nifty_bullish and not sideways_val and sector_bullish and
            ema9_val > ema20_val and current_price > ema200_val and
            rsi_val >= 55 and adx_val >= 22 and volume_filter_val and 
            strong_bull_val and current_price > c1_high_val and
            trend5_up and trend15_up and trend1h_up)
        
        sell_conditions = (nifty_bearish and not sideways_val and sector_bearish and
            ema9_val < ema20_val and current_price < ema200_val and
            rsi_val <= 45 and adx_val >= 22 and volume_filter_val and 
            strong_bear_val and current_price < c1_low_val and
            not trend5_up and not trend15_up and not trend1h_up)
        
        return {
            "signal": "BUY" if buy_conditions else "SELL" if sell_conditions else "WAIT",
            "buy": buy_conditions,
            "sell": sell_conditions,
            "price": current_price,
            "rsi": rsi_val,
            "adx": adx_val,
            "strong_bull": strong_bull_val,
            "strong_bear": strong_bear_val,
            "nifty_bullish": nifty_bullish,
            "sector_bullish": sector_bullish
        }
    except Exception as e:
        return None

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .stButton > button {
        background: linear-gradient(90deg, #00ff88, #00bcd4);
        color: black;
        font-weight: bold;
        border-radius: 30px;
        padding: 8px 20px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,255,136,0.3);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,255,136,0.5);
    }
    h1, h2, h3 {
        background: linear-gradient(135deg, #ffd89b, #19547b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ================= UI HEADER =================
st.markdown("<h1 style='text-align:center;'>🇮🇳 RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)

# ================= ONE LINE CONTROL =================
col_a, col_b, col_c, col_d = st.columns([2.2, 1, 1, 1.2])

with col_a:
    totp = st.text_input("🔐 TOTP Code", type="password", placeholder="6-digit code", key="totp_main", label_visibility="collapsed")

with col_b:
    if st.button("🟢 START", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED")
            st.rerun()
        else:
            st.error("❌ Valid TOTP required!")

with col_c:
    if st.button("🔴 STOP", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 ALGO STOPPED")
        st.rerun()

with col_d:
    if st.session_state.algo_running:
        st.markdown(f"""
        <div style="background:linear-gradient(90deg,#00c853,#69f0ae); padding:10px; border-radius:18px; text-align:center; font-weight:bold; color:black; box-shadow:0 0 12px #00ff88; font-size:14px;">
            🟢 RUNNING<br>{get_ist_now().strftime('%H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:linear-gradient(90deg,#d50000,#ff5252); padding:10px; border-radius:18px; text-align:center; font-weight:bold; color:white; box-shadow:0 0 12px #ff0000; font-size:14px;">
            🔴 STOPPED<br>{get_ist_now().strftime('%H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ================= DAILY LOSS LIMIT WARNING =================
if check_daily_loss_limit():
    st.error(f"🚨 DAILY LOSS LIMIT HIT: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{MAX_DAILY_LOSS:,.0f} - TRADING STOPPED FOR TODAY! 🚨")
else:
    st.info(f"📉 Daily Loss: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{MAX_DAILY_LOSS:,.0f} (Limit: ₹1,00,000)")

st.markdown("---")

# ================= FIXED TARGETS DISPLAY =================
st.markdown("### 🎯 FIXED TARGETS")
col1, col2, col3 = st.columns(3)
col1.metric("🇮🇳 NIFTY", "Target ₹10", delta="per point")
col2.metric("🛢️ CRUDE OIL", "Target ₹10", delta="per point")
col3.metric("🌿 NATURAL GAS", "Target ₹1", delta="per point")

st.markdown("---")

# ================= GLOBAL TREND DISPLAY =================
st.markdown("### 🌍 GLOBAL MARKET TREND")
global_trend, us_trend, asia_trend, dxy_trend = get_global_trend()

col1, col2, col3, col4 = st.columns(4)

with col1:
    if global_trend == "BULLISH":
        st.success(f"🌏 GLOBAL\n🟢 {global_trend}")
    elif global_trend == "BEARISH":
        st.error(f"🌏 GLOBAL\n🔴 {global_trend}")
    else:
        st.warning(f"🌏 GLOBAL\n🟡 {global_trend}")

with col2:
    if us_trend == "BULLISH":
        st.success(f"🇺🇸 US MARKET\n🟢 {us_trend}")
    elif us_trend == "BEARISH":
        st.error(f"🇺🇸 US MARKET\n🔴 {us_trend}")
    else:
        st.warning(f"🇺🇸 US MARKET\n🟡 {us_trend}")

with col3:
    if asia_trend == "BULLISH":
        st.success(f"🌏 ASIA MARKET\n🟢 {asia_trend}")
    elif asia_trend == "BEARISH":
        st.error(f"🌏 ASIA MARKET\n🔴 {asia_trend}")
    else:
        st.warning(f"🌏 ASIA MARKET\n🟡 {asia_trend}")

with col4:
    if dxy_trend == "BULLISH":
        st.success(f"💵 DOLLAR INDEX\n🟢 {dxy_trend} (Weak $)")
    elif dxy_trend == "BEARISH":
        st.error(f"💵 DOLLAR INDEX\n🔴 {dxy_trend} (Strong $)")
    else:
        st.warning(f"💵 DOLLAR INDEX\n🟡 {dxy_trend}")

st.markdown("---")

# ================= NIFTY TREND =================
nifty_trend = get_nifty_trend()
st.markdown("### 🇮🇳 NIFTY TREND")
if nifty_trend == "BULLISH":
    st.success("🟢 BULLISH")
elif nifty_trend == "BEARISH":
    st.error("🔴 BEARISH")
else:
    st.warning("🟡 SIDEWAYS")

st.markdown("---")

# ================= TRADE COUNTERS DISPLAY =================
st.markdown("### 📊 DAILY TRADE COUNTERS (Max 2 per asset)")
col1, col2, col3 = st.columns(3)
col1.metric("🇮🇳 NIFTY Trades", f"{st.session_state.nifty_trades_count}/2")
col2.metric("🛢️ CRUDE Trades", f"{st.session_state.crude_trades_count}/2")
col3.metric("🌿 NG Trades", f"{st.session_state.ng_trades_count}/2")
st.markdown("---")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ SETTINGS")
    
    st.markdown("### 📌 ASSETS")
    st.session_state.enable_nifty = st.checkbox("🇮🇳 NIFTY", value=st.session_state.enable_nifty)
    if st.session_state.enable_nifty:
        st.session_state.nifty_lots = st.number_input("NIFTY Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots, step=1)
        st.caption(f"📦 Qty: {st.session_state.nifty_lots * 65}")
    
    st.session_state.enable_crude = st.checkbox("🛢️ CRUDE OIL", value=st.session_state.enable_crude)
    if st.session_state.enable_crude:
        st.session_state.crude_lots = st.number_input("CRUDE Lots", min_value=1, max_value=50, value=st.session_state.crude_lots, step=1)
        st.caption(f"📦 Qty: {st.session_state.crude_lots * 100}")
    
    st.session_state.enable_ng = st.checkbox("🌿 NATURAL GAS", value=st.session_state.enable_ng)
    if st.session_state.enable_ng:
        st.session_state.ng_lots = st.number_input("NG Lots", min_value=1, max_value=50, value=st.session_state.ng_lots, step=1)
        st.caption(f"📦 Qty: {st.session_state.ng_lots * 1250}")
    
    st.session_state.enable_stocks = st.checkbox("📈 F&O STOCKS (69)", value=st.session_state.enable_stocks)
    
    if st.session_state.enable_stocks:
        st.markdown("---")
        st.markdown("### 📊 STOCK SETTINGS")
        st.session_state.max_stocks_per_day = st.number_input("Max Stocks/Day", 1, 69, 10)
        st.session_state.max_qty_limit = st.selectbox("Max Qty per Trade", MAX_QTY_OPTIONS, index=14)
        st.session_state.enable_big_lot_mode = st.checkbox("🔥 BIG LOT MODE", value=st.session_state.enable_big_lot_mode)
        if st.session_state.enable_big_lot_mode:
            st.success("✅ BIG LOT ACTIVE - ₹20k profit @ target")
    
    st.markdown("---")
    st.markdown("### 📊 DAILY STATUS")
    total_stocks_traded = sum(v["trades"] for v in st.session_state.stock_trades.values())
    st.metric("Stocks Traded", f"{total_stocks_traded}/{st.session_state.max_stocks_per_day}")
    st.metric("Daily Loss", f"₹{abs(st.session_state.daily_loss):,.0f} / ₹{MAX_DAILY_LOSS:,.0f}")
    
    st.markdown("---")
    st.markdown("### 🎯 RULES")
    st.caption("NIFTY/CRUDE/NG: Max 2 trades/day (1 Buy + 1 Sell)")
    st.caption("Stocks: Max stocks/day limit")
    st.caption("Daily Loss Limit: ₹1,00,000")
    st.caption("TP1=50% Book | TP2=50% Book")
    st.caption("🔐 App Protected with Password")

# ================= TRADING JOURNAL =================
st.markdown("## 📋 TRADING JOURNAL")

if st.session_state.trade_journal:
    df_journal = pd.DataFrame(st.session_state.trade_journal)
    st.dataframe(df_journal, use_container_width=True, height=400)
    
    if 'Profit/Loss' in df_journal.columns:
        total_profit = df_journal[df_journal['Profit/Loss'] > 0]['Profit/Loss'].sum() if len(df_journal[df_journal['Profit/Loss'] > 0]) > 0 else 0
        total_loss = df_journal[df_journal['Profit/Loss'] < 0]['Profit/Loss'].sum() if len(df_journal[df_journal['Profit/Loss'] < 0]) > 0 else 0
        win_trades = len(df_journal[df_journal['Profit/Loss'] > 0])
        loss_trades = len(df_journal[df_journal['Profit/Loss'] < 0])
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 Total Trades", len(df_journal))
        col2.metric("✅ Win Trades", win_trades)
        col3.metric("❌ Loss Trades", loss_trades)
        col4.metric("💰 Net P&L", f"₹{total_profit + total_loss:,.2f}")
else:
    st.info("📭 No trades executed yet.")

st.markdown("---")

# ================= MAIN TRADING LOGIC =================
if st.session_state.algo_running and st.session_state.totp_verified and not check_daily_loss_limit():
    
    # ================= NIFTY TRADING =================
    if st.session_state.enable_nifty and st.session_state.nifty_trades_count < 2:
        if is_nifty_market_open():
            signal, price = get_nifty_signal()
            st.write(f"🇮🇳 NIFTY Signal: {signal} at ₹{price:.2f}")
            
            if signal != "WAIT":
                trade_type = "BUY" if signal == "BUY" else "SELL"
                qty = st.session_state.nifty_lots * 65
                
                trade_record = {
                    "No": len(st.session_state.trade_journal) + 1,
                    "Symbol": "NIFTY",
                    "Type": trade_type,
                    "Qty": qty,
                    "Lots": st.session_state.nifty_lots,
                    "Entry Price": round(price, 2),
                    "Target": FIXED_TARGETS["NIFTY"],
                    "Status": "OPEN",
                    "Entry Time": get_ist_now().strftime('%H:%M:%S')
                }
                st.session_state.trade_journal.append(trade_record)
                st.session_state.nifty_trades_count += 1
                send_telegram(f"🇮🇳 NIFTY {trade_type} | {st.session_state.nifty_lots} lots ({qty} qty) | Entry: ₹{price:.2f} | Target: ₹{FIXED_TARGETS['NIFTY']}")
                st.success(f"✅ NIFTY {trade_type} Executed!")
                st.rerun()
    
    # ================= CRUDE TRADING =================
    if st.session_state.enable_crude and st.session_state.crude_trades_count < 2:
        if is_commodity_market_open():
            signal, price = get_crude_signal()
            st.write(f"🛢️ CRUDE Signal: {signal} at ${price:.2f}")
            
            if signal != "WAIT":
                trade_type = "BUY" if signal == "BUY" else "SELL"
                qty = st.session_state.crude_lots * 100
                price_inr = price * get_usd_inr_rate()
                
                trade_record = {
                    "No": len(st.session_state.trade_journal) + 1,
                    "Symbol": "CRUDE OIL",
                    "Type": trade_type,
                    "Qty": qty,
                    "Lots": st.session_state.crude_lots,
                    "Entry Price": round(price_inr, 2),
                    "Target": FIXED_TARGETS["CRUDEOIL"],
                    "Status": "OPEN",
                    "Entry Time": get_ist_now().strftime('%H:%M:%S')
                }
                st.session_state.trade_journal.append(trade_record)
                st.session_state.crude_trades_count += 1
                send_telegram(f"🛢️ CRUDE {trade_type} | {st.session_state.crude_lots} lots ({qty} qty) | Entry: ₹{price_inr:.2f} | Target: ₹{FIXED_TARGETS['CRUDEOIL']}")
                st.success(f"✅ CRUDE {trade_type} Executed!")
                st.rerun()
    
    # ================= NG TRADING =================
    if st.session_state.enable_ng and st.session_state.ng_trades_count < 2:
        if is_commodity_market_open():
            signal, price = get_ng_signal()
            st.write(f"🌿 NG Signal: {signal} at ${price:.2f}")
            
            if signal != "WAIT":
                trade_type = "BUY" if signal == "BUY" else "SELL"
                qty = st.session_state.ng_lots * 1250
                price_inr = price * get_usd_inr_rate()
                
                trade_record = {
                    "No": len(st.session_state.trade_journal) + 1,
                    "Symbol": "NATURAL GAS",
                    "Type": trade_type,
                    "Qty": qty,
                    "Lots": st.session_state.ng_lots,
                    "Entry Price": round(price_inr, 2),
                    "Target": FIXED_TARGETS["NATURALGAS"],
                    "Status": "OPEN",
                    "Entry Time": get_ist_now().strftime('%H:%M:%S')
                }
                st.session_state.trade_journal.append(trade_record)
                st.session_state.ng_trades_count += 1
                send_telegram(f"🌿 NG {trade_type} | {st.session_state.ng_lots} lots ({qty} qty) | Entry: ₹{price_inr:.2f} | Target: ₹{FIXED_TARGETS['NATURALGAS']}")
                st.success(f"✅ NG {trade_type} Executed!")
                st.rerun()
    
    # ================= STOCKS TRADING =================
    if st.session_state.enable_stocks:
        st.markdown("## 🔍 SCANNING F&O STOCKS")
        
        if not is_stock_market_open():
            st.info("⏸️ Market Closed | 9:30 AM - 2:30 PM IST")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = st.container()
            
            signals_found = []
            trades_done = sum(v["trades"] for v in st.session_state.stock_trades.values())
            
            for idx, stock in enumerate(FO_STOCKS):
                progress_bar.progress((idx+1)/len(FO_STOCKS))
                status_text.text(f"Scanning {stock['name']}...")
                
                if trades_done >= st.session_state.max_stocks_per_day:
                    status_text.text(f"Daily limit reached: {st.session_state.max_stocks_per_day}")
                    break
                
                sig = calculate_signals_stock(stock["symbol"], stock["name"], stock["sector"])
                if sig and (sig["buy"] or sig["sell"]):
                    trade_done = st.session_state.stock_trades[stock["name"]]["trades"] >= 1
                    if not trade_done:
                        qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit, 
                                                              st.session_state.enable_big_lot_mode, stock.get("big_lot_qty"))
                        
                        buy_price = sig["price"]
                        option_type = "CE" if sig["buy"] else "PE"
                        
                        itm_strike, actual_itm, strike_interval = get_stock_itm_strike_auto(buy_price, stock, option_type, strike_offset=2)
                        
                        trade_record = {
                            "No": len(st.session_state.trade_journal) + 1,
                            "Symbol": stock["name"],
                            "Type": f"BUY {option_type}" if sig["buy"] else f"SELL {option_type}",
                            "Qty": qty,
                            "Lots": lots,
                            "Entry Price": round(buy_price, 2),
                            "ITM Strike": itm_strike,
                            "TP1": stock["tp1"],
                            "TP2": stock["tp2"],
                            "Status": "OPEN",
                            "Entry Time": get_ist_now().strftime('%H:%M:%S')
                        }
                        st.session_state.trade_journal.append(trade_record)
                        
                        signals_found.append({
                            "stock": stock["name"],
                            "type": f"BUY {option_type}" if sig["buy"] else f"SELL {option_type}",
                            "price": buy_price,
                            "lots": lots,
                            "qty": qty,
                            "itm_strike": itm_strike,
                            "itm_points": actual_itm,
                            "tp1": stock["tp1"],
                            "tp2": stock["tp2"],
                            "rsi": sig["rsi"],
                            "adx": sig["adx"]
                        })
                        st.session_state.stock_trades[stock["name"]]["trades"] += 1
                        trades_done += 1
                        send_telegram(f"{'🔵 BUY' if sig['buy'] else '🔴 SELL'} {stock['name']} {option_type} | Strike: {itm_strike} ({actual_itm} pts ITM) | {lots} lots ({qty} qty) | TP1: ₹{stock['tp1']} TP2: ₹{stock['tp2']}")
            
            progress_bar.empty()
            status_text.empty()
            
            with results:
                if signals_found:
                    st.success(f"✅ {len(signals_found)} Signals Found!")
                    for s in signals_found:
                        st.markdown(f"""
                        <div style='background:rgba(0,255,136,0.1); padding:15px; border-radius:10px; margin:10px 0; border-left:4px solid #00ff88;'>
                            <b>{'🟢' if 'BUY' in s['type'] else '🔴'} {s['stock']}</b><br>
                            Action: {s['type']}<br>
                            🎯 ITM Strike: {s['itm_strike']} ({s['itm_points']} pts ITM)<br>
                            Lots: {s['lots']} | Qty: {s['qty']}<br>
                            TP1: ₹{s['tp1']} (50% Book) | TP2: ₹{s['tp2']} (50% Book)<br>
                            📊 RSI: {s['rsi']:.0f} | ADX: {s['adx']:.0f}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("📭 No signals found")
    
elif not st.session_state.algo_running:
    st.warning("⏸️ ALGO IS STOPPED. Press START to begin trading.")
elif not st.session_state.totp_verified:
    st.warning("🔐 Please enter valid 6-digit TOTP code and press START.")
elif check_daily_loss_limit():
    st.error(f"🚨 DAILY LOSS LIMIT HIT (₹{MAX_DAILY_LOSS:,.0f})! Trading stopped for today. 🚨")

# ================= FOOTER =================
st.markdown("---")
st.caption(f"📊 Trading Journal | NIFTY: {st.session_state.nifty_trades_count}/2 | CRUDE: {st.session_state.crude_trades_count}/2 | NG: {st.session_state.ng_trades_count}/2 | Daily Loss Limit: ₹{MAX_DAILY_LOSS:,.0f}")
st.caption("🔐 App Protected with Password | Developed by Satish D. Nakhate")
