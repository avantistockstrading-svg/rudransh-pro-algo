import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO-ALGO X", layout="wide", page_icon="📈")

# ================= IST Timezone =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= FIXED TARGETS =================
FIXED_TARGETS = {
    "NIFTY": 10,
    "CRUDEOIL": 10,
    "NATURALGAS": 1,
    "STOCKS": 5
}

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

# ================= LOT SIZES =================
ASSET_LOT_SIZES = {
    "NIFTY": 65,
    "CRUDEOIL": 100,
    "NATURALGAS": 1250
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

def get_itm_strike(price, asset_type, itm_points=100, strike_interval=50):
    if price <= 0:
        return 0, 0
    target_strike = price - itm_points
    rounded_strike = round(target_strike / strike_interval) * strike_interval
    if rounded_strike < 100:
        rounded_strike = 100
    actual_itm = price - rounded_strike
    return int(rounded_strike), actual_itm

def get_option_tp_sl(entry_premium):
    if entry_premium <= 50:
        return {"sl_points": 1.50, "tp1_points": 1.00, "tp2_points": 1.50, "tp3_points": 2.00}
    elif entry_premium <= 150:
        return {"sl_points": 2.00, "tp1_points": 1.50, "tp2_points": 3.00, "tp3_points": 5.00}
    elif entry_premium <= 300:
        return {"sl_points": 5.00, "tp1_points": 3.00, "tp2_points": 6.00, "tp3_points": 10.00}
    elif entry_premium <= 500:
        return {"sl_points": 10.00, "tp1_points": 5.00, "tp2_points": 10.00, "tp3_points": 15.00}
    else:
        return {"sl_points": 20.00, "tp1_points": 10.00, "tp2_points": 20.00, "tp3_points": 30.00}

# ================= 50 F&O STOCKS =================
FO_STOCKS = [
    {"symbol": "RELIANCE.NS", "lot": 250, "itm": 50, "name": "RELIANCE", "sector": "ENERGY", "big_lot_qty": 4000, "big_lot_lots": 16},
    {"symbol": "TCS.NS", "lot": 150, "itm": 100, "name": "TCS", "sector": "IT", "big_lot_qty": 4050, "big_lot_lots": 27},
    {"symbol": "HDFCBANK.NS", "lot": 500, "itm": 50, "name": "HDFC BANK", "sector": "BANK", "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "INFY.NS", "lot": 200, "itm": 100, "name": "INFOSYS", "sector": "IT", "big_lot_qty": 4000, "big_lot_lots": 20},
    {"symbol": "ICICIBANK.NS", "lot": 550, "itm": 25, "name": "ICICI BANK", "sector": "BANK", "big_lot_qty": 4400, "big_lot_lots": 8},
    {"symbol": "SBIN.NS", "lot": 450, "itm": 25, "name": "SBI", "sector": "BANK", "big_lot_qty": 4050, "big_lot_lots": 9},
    {"symbol": "BHARTIARTL.NS", "lot": 700, "itm": 10, "name": "BHARTI AIRTEL", "sector": "TELECOM", "big_lot_qty": 4200, "big_lot_lots": 6},
    {"symbol": "KOTAKBANK.NS", "lot": 450, "itm": 50, "name": "KOTAK BANK", "sector": "BANK", "big_lot_qty": 4050, "big_lot_lots": 9},
    {"symbol": "BAJFINANCE.NS", "lot": 250, "itm": 100, "name": "BAJAJ FINANCE", "sector": "FINANCE", "big_lot_qty": 4000, "big_lot_lots": 16},
    {"symbol": "ITC.NS", "lot": 800, "itm": 10, "name": "ITC", "sector": "FMCG", "big_lot_qty": 4000, "big_lot_lots": 5},
    {"symbol": "HINDUNILVR.NS", "lot": 400, "itm": 100, "name": "HUL", "sector": "FMCG", "big_lot_qty": 4000, "big_lot_lots": 10},
    {"symbol": "TATAMOTORS.NS", "lot": 350, "itm": 10, "name": "TATA MOTORS", "sector": "AUTO", "big_lot_qty": 4200, "big_lot_lots": 12},
    {"symbol": "TATASTEEL.NS", "lot": 600, "itm": 10, "name": "TATA STEEL", "sector": "METAL", "big_lot_qty": 4200, "big_lot_lots": 7},
    {"symbol": "AXISBANK.NS", "lot": 500, "itm": 25, "name": "AXIS BANK", "sector": "BANK", "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "MARUTI.NS", "lot": 150, "itm": 100, "name": "MARUTI", "sector": "AUTO", "big_lot_qty": 4050, "big_lot_lots": 27},
    {"symbol": "SUNPHARMA.NS", "lot": 400, "itm": 20, "name": "SUN PHARMA", "sector": "PHARMA", "big_lot_qty": 4000, "big_lot_lots": 10},
    {"symbol": "WIPRO.NS", "lot": 600, "itm": 40, "name": "WIPRO", "sector": "IT", "big_lot_qty": 4200, "big_lot_lots": 7},
    {"symbol": "HCLTECH.NS", "lot": 300, "itm": 100, "name": "HCL TECH", "sector": "IT", "big_lot_qty": 4200, "big_lot_lots": 14},
    {"symbol": "NTPC.NS", "lot": 1500, "itm": 10, "name": "NTPC", "sector": "ENERGY", "big_lot_qty": 4500, "big_lot_lots": 3},
    {"symbol": "POWERGRID.NS", "lot": 1200, "itm": 10, "name": "POWER GRID", "sector": "ENERGY", "big_lot_qty": 4800, "big_lot_lots": 4},
    {"symbol": "ONGC.NS", "lot": 1500, "itm": 10, "name": "ONGC", "sector": "ENERGY", "big_lot_qty": 4500, "big_lot_lots": 3},
    {"symbol": "M&M.NS", "lot": 500, "itm": 25, "name": "M&M", "sector": "AUTO", "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "ULTRACEMCO.NS", "lot": 200, "itm": 100, "name": "ULTRATECH", "sector": "INFRA", "big_lot_qty": 4000, "big_lot_lots": 20},
    {"symbol": "NESTLEIND.NS", "lot": 100, "itm": 200, "name": "NESTLE", "sector": "FMCG", "big_lot_qty": 4000, "big_lot_lots": 40},
    {"symbol": "JSWSTEEL.NS", "lot": 600, "itm": 10, "name": "JSW STEEL", "sector": "METAL", "big_lot_qty": 4200, "big_lot_lots": 7},
    {"symbol": "TECHM.NS", "lot": 400, "itm": 50, "name": "TECH MAHINDRA", "sector": "IT", "big_lot_qty": 4000, "big_lot_lots": 10},
    {"symbol": "BAJAJFINSV.NS", "lot": 250, "itm": 100, "name": "BAJAJ FINSERV", "sector": "FINANCE", "big_lot_qty": 4000, "big_lot_lots": 16},
    {"symbol": "ASIANPAINT.NS", "lot": 300, "itm": 100, "name": "ASIAN PAINTS", "sector": "CONSUMER", "big_lot_qty": 4200, "big_lot_lots": 14},
    {"symbol": "GRASIM.NS", "lot": 200, "itm": 50, "name": "GRASIM", "sector": "INFRA", "big_lot_qty": 4000, "big_lot_lots": 20},
    {"symbol": "INDUSINDBK.NS", "lot": 350, "itm": 50, "name": "INDUSIND BANK", "sector": "BANK", "big_lot_qty": 4200, "big_lot_lots": 12},
    {"symbol": "BRITANNIA.NS", "lot": 300, "itm": 50, "name": "BRITANNIA", "sector": "FMCG", "big_lot_qty": 4200, "big_lot_lots": 14},
    {"symbol": "HDFCLIFE.NS", "lot": 350, "itm": 50, "name": "HDFC LIFE", "sector": "FINANCE", "big_lot_qty": 4200, "big_lot_lots": 12},
    {"symbol": "SBILIFE.NS", "lot": 300, "itm": 50, "name": "SBI LIFE", "sector": "FINANCE", "big_lot_qty": 4200, "big_lot_lots": 14},
    {"symbol": "DRREDDY.NS", "lot": 200, "itm": 100, "name": "DR REDDY", "sector": "PHARMA", "big_lot_qty": 4000, "big_lot_lots": 20},
    {"symbol": "DIVISLAB.NS", "lot": 200, "itm": 100, "name": "DIVIS LAB", "sector": "PHARMA", "big_lot_qty": 4000, "big_lot_lots": 20},
    {"symbol": "HAL.NS", "lot": 150, "itm": 20, "name": "HAL", "sector": "DEFENCE", "big_lot_qty": 4050, "big_lot_lots": 27},
    {"symbol": "ADANIENT.NS", "lot": 250, "itm": 50, "name": "ADANI ENTERPRISES", "sector": "ENERGY", "big_lot_qty": 4000, "big_lot_lots": 16},
    {"symbol": "ADANIPORTS.NS", "lot": 350, "itm": 25, "name": "ADANI PORTS", "sector": "ENERGY", "big_lot_qty": 4200, "big_lot_lots": 12},
    {"symbol": "HEROMOTOCO.NS", "lot": 300, "itm": 50, "name": "HERO MOTOCORP", "sector": "AUTO", "big_lot_qty": 4200, "big_lot_lots": 14},
    {"symbol": "COALINDIA.NS", "lot": 1500, "itm": 10, "name": "COAL INDIA", "sector": "ENERGY", "big_lot_qty": 4500, "big_lot_lots": 3},
    {"symbol": "BPCL.NS", "lot": 1000, "itm": 10, "name": "BPCL", "sector": "ENERGY", "big_lot_qty": 4000, "big_lot_lots": 4},
    {"symbol": "SHREECEM.NS", "lot": 200, "itm": 100, "name": "SHREE CEMENT", "sector": "INFRA", "big_lot_qty": 4000, "big_lot_lots": 20},
    {"symbol": "EICHERMOT.NS", "lot": 300, "itm": 50, "name": "EICHER MOTORS", "sector": "AUTO", "big_lot_qty": 4200, "big_lot_lots": 14},
    {"symbol": "PIDILITIND.NS", "lot": 350, "itm": 50, "name": "PIDILITE", "sector": "CONSUMER", "big_lot_qty": 4200, "big_lot_lots": 12},
    {"symbol": "DABUR.NS", "lot": 600, "itm": 25, "name": "DABUR", "sector": "FMCG", "big_lot_qty": 4200, "big_lot_lots": 7},
    {"symbol": "HAVELLS.NS", "lot": 500, "itm": 25, "name": "HAVELLS", "sector": "CONSUMER", "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "UPL.NS", "lot": 1000, "itm": 10, "name": "UPL", "sector": "CHEMICAL", "big_lot_qty": 4000, "big_lot_lots": 4},
    {"symbol": "LT.NS", "lot": 200, "itm": 100, "name": "LT", "sector": "INFRA", "big_lot_qty": 4000, "big_lot_lots": 20},
    {"symbol": "ADANIGREEN.NS", "lot": 300, "itm": 50, "name": "ADANI GREEN", "sector": "ENERGY", "big_lot_qty": 4200, "big_lot_lots": 14},
    {"symbol": "VEDANTA.NS", "lot": 800, "itm": 10, "name": "VEDANTA", "sector": "METAL", "big_lot_qty": 4000, "big_lot_lots": 5},
]

# ================= SECTOR MAPPING =================
SECTOR_INDEX = {
    "BANK": "^NSEBANK", "IT": "^CNXIT", "AUTO": "^CNXAUTO", "PHARMA": "^CNXPHARMA",
    "METAL": "^CNXMETAL", "FMCG": "^CNXFMCG", "FINANCE": "^CNXFINANCE", "ENERGY": "^CNXENERGY",
    "INFRA": "^CNXINFRA", "DEFENCE": "^CNXINFRA", "CONSUMER": "^NIFTY_CONSR_DURBL", "TELECOM": "^CNXIT", "CHEMICAL": "^NIFTY_CHEMICAL",
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
    st.session_state.last_trade_date = get_ist_now().date()

MAX_DAILY_LOSS = 100000

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

def get_stock_trend(symbol):
    try:
        df = yf.download(symbol, period="7d", interval="15m", progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        close = df['Close']
        ema9 = close.ewm(span=9).mean().iloc[-1]
        ema20 = close.ewm(span=20).mean().iloc[-1]
        if ema9 > ema20:
            return "BULLISH"
        elif ema9 < ema20:
            return "BEARISH"
    except:
        pass
    return "NEUTRAL"

def get_stock_itm_strike(price, stock, option_type="CE"):
    if price <= 0:
        return 0
    itm_points = stock["itm"]
    if option_type == "CE":
        itm_strike = price - itm_points
    else:
        itm_strike = price + itm_points
    if itm_strike <= 0:
        itm_strike = 5
    if itm_strike > 1000:
        itm_strike = round(itm_strike / 50) * 50
    elif itm_strike > 100:
        itm_strike = round(itm_strike / 10) * 10
    else:
        itm_strike = round(itm_strike / 5) * 5
    return int(itm_strike)

def get_option_premium(symbol, strike_price, option_type):
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            stock_price = df['Close'].iloc[-1]
            if isinstance(stock_price, pd.Series):
                stock_price = float(stock_price.iloc[-1])
            if option_type == "CE":
                intrinsic_value = max(0, stock_price - strike_price)
            else:
                intrinsic_value = max(0, strike_price - stock_price)
            premium = intrinsic_value + (intrinsic_value * 0.1)
            return max(premium, 5)
    except:
        pass
    return 50

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
            "ema9": ema9_val,
            "ema20": ema20_val,
            "ema200": ema200_val,
            "sideways": sideways_val,
            "trend5_up": trend5_up,
            "trend15_up": trend15_up,
            "trend1h_up": trend1h_up,
            "nifty_bullish": nifty_bullish,
            "sector_bullish": sector_bullish
        }
    except Exception as e:
        return None

# ================= CUSTOM CSS FOR 3D UI =================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .status-running {
        background: linear-gradient(90deg, #00c853, #69f0ae);
        padding: 15px;
        border-radius: 50px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: black;
        box-shadow: 0 0 20px #00ff88;
        animation: pulse 1.5s infinite;
    }
    .status-stopped {
        background: linear-gradient(90deg, #d50000, #ff5252);
        padding: 15px;
        border-radius: 50px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        box-shadow: 0 0 20px #ff0000;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 #00ff88; }
        70% { box-shadow: 0 0 0 20px rgba(0,255,136,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,255,136,0); }
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
    .trade-profit {
        color: #00ff88;
        font-weight: bold;
    }
    .trade-loss {
        color: #ff5252;
        font-weight: bold;
    }
    /* One line control */
    .control-row {
        display: flex;
        align-items: center;
        gap: 15px;
        background: rgba(0,0,0,0.3);
        padding: 10px 20px;
        border-radius: 50px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ================= UI HEADER =================
st.markdown("<h1 style='text-align:center;'>📱 RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)

# ================= ONE LINE CONTROL (TOTP + START + STOP) =================
col_a, col_b, col_c = st.columns([2, 1, 1])

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

# ================= LIVE STATUS & CLOCK =================
st.markdown("---")
if st.session_state.algo_running:
    st.markdown(f"""
    <div class="status-running">
        🟢 ALGO RUNNING | {get_ist_now().strftime('%H:%M:%S')} 🟢
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="status-stopped">
        🔴 ALGO STOPPED | {get_ist_now().strftime('%H:%M:%S')} 🔴
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ================= FIXED TARGETS DISPLAY =================
st.markdown("### 🎯 FIXED TARGETS")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 NIFTY", "Target ₹10", delta="per point")
col2.metric("🛢️ CRUDE OIL", "Target ₹10", delta="per point")
col3.metric("🌿 NATURAL GAS", "Target ₹1", delta="per point")
col4.metric("📈 F&O STOCKS", "Target ₹5", delta="per share")

# ================= NIFTY TREND =================
nifty_trend = get_nifty_trend()
st.markdown("### 🇮🇳 NIFTY TREND")
if nifty_trend == "BULLISH":
    st.success("🟢 BULLISH")
elif nifty_trend == "BEARISH":
    st.error("🔴 BEARISH")
else:
    st.warning("🟡 SIDEWAYS")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ SETTINGS")
    
    st.markdown("### 📌 ASSETS")
    st.session_state.enable_nifty = st.checkbox("NIFTY", value=st.session_state.enable_nifty)
    st.session_state.enable_crude = st.checkbox("CRUDE OIL", value=st.session_state.enable_crude)
    st.session_state.enable_ng = st.checkbox("NATURAL GAS", value=st.session_state.enable_ng)
    st.session_state.enable_stocks = st.checkbox("F&O STOCKS (50)", value=st.session_state.enable_stocks)
    
    if st.session_state.enable_stocks:
        st.session_state.max_stocks_per_day = st.number_input("Max Stocks/Day", 1, 50, 10)
        st.session_state.max_qty_limit = st.selectbox("Max Qty", MAX_QTY_OPTIONS, index=14)
        st.session_state.enable_big_lot_mode = st.checkbox("🔥 BIG LOT MODE (₹20k @ ₹5)", value=st.session_state.enable_big_lot_mode)
        if st.session_state.enable_big_lot_mode:
            st.warning("⚠️ BIG LOT ACTIVE - ~4000 qty per stock")
    
    st.markdown("---")
    st.markdown("### 📊 DAILY STATUS")
    total_trades = sum(v["trades"] for v in st.session_state.stock_trades.values())
    st.metric("Stocks Traded", f"{total_trades}/{st.session_state.max_stocks_per_day}")
    st.metric("Daily Loss", f"₹{abs(st.session_state.daily_loss):,.0f}", delta_color="inverse")

# ================= TRADING JOURNAL TABLE =================
st.markdown("---")
st.markdown("## 📋 TRADING JOURNAL")

if st.session_state.trade_journal:
    df_journal = pd.DataFrame(st.session_state.trade_journal)
    st.dataframe(df_journal, use_container_width=True)
    
    # Summary Stats
    total_profit = df_journal[df_journal['Profit/Loss'] > 0]['Profit/Loss'].sum() if 'Profit/Loss' in df_journal.columns else 0
    total_loss = df_journal[df_journal['Profit/Loss'] < 0]['Profit/Loss'].sum() if 'Profit/Loss' in df_journal.columns else 0
    win_trades = len(df_journal[df_journal['Profit/Loss'] > 0]) if 'Profit/Loss' in df_journal.columns else 0
    loss_trades = len(df_journal[df_journal['Profit/Loss'] < 0]) if 'Profit/Loss' in df_journal.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Trades", len(df_journal))
    col2.metric("Win Trades", win_trades)
    col3.metric("Loss Trades", loss_trades)
    col4.metric("Net P&L", f"₹{total_profit + total_loss:,.2f}" if total_profit or total_loss else "₹0", delta_color="normal")
else:
    st.info("📭 No trades executed yet. Trades will appear here once the algo runs.")

# ================= MAIN CONTENT (Only when RUNNING) =================
if st.session_state.algo_running and st.session_state.totp_verified:
    
    # NIFTY Section
    if st.session_state.enable_nifty:
        st.markdown("## 📊 NIFTY 50")
        price = get_live_price("^NSEI")
        strike, itm = get_itm_strike(price, "NIFTY", itm_points=100, strike_interval=50)
        col1, col2, col3 = st.columns(3)
        col1.metric("Price", f"₹{price:,.2f}" if price > 0 else "Loading...")
        col2.metric("ITM Strike", strike)
        col3.metric("Target", "₹10")
        st.markdown("---")
    
    # CRUDE Section
    if st.session_state.enable_crude:
        st.markdown("## 🛢️ CRUDE OIL")
        price = get_live_price_inr("CL=F")
        col1, col2, col3 = st.columns(3)
        col1.metric("Price (INR)", f"₹{price:,.2f}" if price > 0 else "Loading...")
        col2.metric("Lot Size", "100")
        col3.metric("Target", "₹10")
        st.markdown("---")
    
    # NG Section
    if st.session_state.enable_ng:
        st.markdown("## 🌿 NATURAL GAS")
        price = get_live_price_inr("NG=F")
        col1, col2, col3 = st.columns(3)
        col1.metric("Price (INR)", f"₹{price:,.2f}" if price > 0 else "Loading...")
        col2.metric("Lot Size", "1250")
        col3.metric("Target", "₹1")
        st.markdown("---")
    
    # STOCKS Scanning
    if st.session_state.enable_stocks:
        st.markdown("## 🔍 SCANNING F&O STOCKS")
        
        if not is_stock_market_open():
            st.info("⏸️ Market Closed | Trading Hours: 9:30 AM - 2:30 PM IST")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = st.container()
            
            signals = []
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
                        target_price = buy_price + FIXED_TARGETS["STOCKS"] if sig["buy"] else buy_price - FIXED_TARGETS["STOCKS"]
                        
                        # Add to Trade Journal
                        trade_record = {
                            "No": len(st.session_state.trade_journal) + 1,
                            "Symbol": stock["name"],
                            "Type": "BUY CE" if sig["buy"] else "SELL PE",
                            "Qty": qty,
                            "Lots": lots,
                            "Entry Price": round(buy_price, 2),
                            "Target": round(target_price, 2),
                            "Status": "OPEN",
                            "Entry Time": get_ist_now().strftime('%H:%M:%S')
                        }
                        st.session_state.trade_journal.append(trade_record)
                        
                        signals.append({
                            "stock": stock["name"],
                            "type": "BUY CE" if sig["buy"] else "SELL PE",
                            "price": buy_price,
                            "lots": lots,
                            "qty": qty,
                            "target": FIXED_TARGETS["STOCKS"],
                            "rsi": sig["rsi"],
                            "adx": sig["adx"]
                        })
                        st.session_state.stock_trades[stock["name"]]["trades"] += 1
                        trades_done += 1
                        send_telegram(f"{'🔵 BUY' if sig['buy'] else '🔴 SELL'} {stock['name']} | {lots} lots ({qty} qty) | Target ₹{FIXED_TARGETS['STOCKS']}")
            
            progress_bar.empty()
            status_text.empty()
            
            with results:
                if signals:
                    st.success(f"✅ {len(signals)} Signals Found!")
                    for s in signals:
                        st.markdown(f"""
                        <div style='background:rgba(0,255,136,0.1); padding:15px; border-radius:10px; margin:10px 0; border-left:4px solid #00ff88;'>
                            <b>{'🟢' if 'BUY' in s['type'] else '🔴'} {s['stock']}</b><br>
                            Action: {s['type']}<br>
                            Lots: {s['lots']} | Qty: {s['qty']}<br>
                            Target: ₹{s['target']} | RSI: {s['rsi']:.0f} | ADX: {s['adx']:.0f}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("📭 No signals found")
    
else:
    if not st.session_state.algo_running:
        st.warning("⏸️ ALGO IS STOPPED. Press START to begin trading.")
    elif not st.session_state.totp_verified:
        st.warning("🔐 Please enter valid 6-digit TOTP code and press START.")

# ================= FOOTER =================
st.markdown("---")
st.caption(f"📊 Trading Journal | Total Records: {len(st.session_state.trade_journal)}")
