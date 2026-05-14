import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests

st.set_page_config(page_title="Rudransh Pro-Algo - Real Trading System", layout="wide")

# ================= IST Timezone =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= MAX QUANTITY LIMIT FOR STOCKS =================
MAX_QTY_OPTIONS = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]

def calculate_trade_quantity(lot_size, max_qty_limit):
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

# ================= ASSET SPECIFIC LOT SIZES =================
ASSET_LOT_SIZES = {
    "NIFTY": 65,
    "CRUDEOIL": 100,
    "NATURALGAS": 1250
}

# ================= FIXED TP/SL SETTINGS =================
FIXED_TP_SL = {
    "NIFTY": {"sl": 30, "tp1": 15, "tp2": 22, "tp3": 30, "itm": 100},
    "CRUDEOIL": {"sl": 30, "tp1": 15, "tp2": 20, "tp3": 25, "itm": 100},
    "NATURALGAS": {"sl": 1.50, "tp1": 1.00, "tp2": 1.50, "tp3": 2.00, "itm": 10}
}

# ================= USD/INR LIVE RATE =================
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

# ================= LIVE PRICE FUNCTIONS =================
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

# ================= OPTION TP/SL BASED ON PREMIUM =================
def get_option_tp_sl(entry_premium):
    if entry_premium <= 50:
        return {"sl_percent": 30, "tp1_percent": 20, "tp2_percent": 40, "tp3_percent": 60}
    elif entry_premium <= 150:
        return {"sl_percent": 25, "tp1_percent": 15, "tp2_percent": 30, "tp3_percent": 50}
    elif entry_premium <= 300:
        return {"sl_percent": 20, "tp1_percent": 12, "tp2_percent": 25, "tp3_percent": 40}
    elif entry_premium <= 500:
        return {"sl_percent": 15, "tp1_percent": 10, "tp2_percent": 20, "tp3_percent": 30}
    elif entry_premium <= 1000:
        return {"sl_percent": 12, "tp1_percent": 8, "tp2_percent": 15, "tp3_percent": 25}
    else:
        return {"sl_percent": 10, "tp1_percent": 6, "tp2_percent": 12, "tp3_percent": 20}

def calculate_option_targets(entry_premium, quantity):
    tp_sl = get_option_tp_sl(entry_premium)
    
    sl_price = entry_premium * (1 - tp_sl["sl_percent"] / 100)
    tp1_price = entry_premium * (1 + tp_sl["tp1_percent"] / 100)
    tp2_price = entry_premium * (1 + tp_sl["tp2_percent"] / 100)
    tp3_price = entry_premium * (1 + tp_sl["tp3_percent"] / 100)
    
    qty_tp1 = quantity // 2
    qty_tp2 = quantity // 4
    qty_tp3 = quantity - qty_tp1 - qty_tp2
    
    tp1_profit = qty_tp1 * (tp1_price - entry_premium)
    tp2_profit = qty_tp2 * (tp2_price - entry_premium)
    tp3_profit = qty_tp3 * (tp3_price - entry_premium)
    sl_loss = quantity * (entry_premium - sl_price)
    
    return {
        "entry": entry_premium,
        "sl": sl_price,
        "sl_loss": sl_loss,
        "tp1": tp1_price,
        "tp1_profit": tp1_profit,
        "tp2": tp2_price,
        "tp2_profit": tp2_profit,
        "tp3": tp3_price,
        "tp3_profit": tp3_profit,
        "total_profit": tp1_profit + tp2_profit + tp3_profit,
        "sl_percent": tp_sl["sl_percent"],
        "tp1_percent": tp_sl["tp1_percent"],
        "tp2_percent": tp_sl["tp2_percent"],
        "tp3_percent": tp_sl["tp3_percent"]
    }

# ================= F&O Stocks List =================
FO_STOCKS = [
    {"symbol": "RELIANCE.NS", "lot": 250, "itm": 50, "name": "RELIANCE", "sector": "ENERGY"},
    {"symbol": "TCS.NS", "lot": 150, "itm": 100, "name": "TCS", "sector": "IT"},
    {"symbol": "HDFCBANK.NS", "lot": 500, "itm": 50, "name": "HDFC BANK", "sector": "BANK"},
    {"symbol": "INFY.NS", "lot": 200, "itm": 100, "name": "INFOSYS", "sector": "IT"},
    {"symbol": "ICICIBANK.NS", "lot": 550, "itm": 25, "name": "ICICI BANK", "sector": "BANK"},
    {"symbol": "SBIN.NS", "lot": 450, "itm": 25, "name": "SBI", "sector": "BANK"},
    {"symbol": "BHARTIARTL.NS", "lot": 700, "itm": 10, "name": "BHARTI AIRTEL", "sector": "TELECOM"},
    {"symbol": "KOTAKBANK.NS", "lot": 450, "itm": 50, "name": "KOTAK BANK", "sector": "BANK"},
    {"symbol": "BAJFINANCE.NS", "lot": 250, "itm": 100, "name": "BAJAJ FINANCE", "sector": "FINANCE"},
    {"symbol": "ITC.NS", "lot": 800, "itm": 10, "name": "ITC", "sector": "FMCG"},
    {"symbol": "HINDUNILVR.NS", "lot": 400, "itm": 100, "name": "HUL", "sector": "FMCG"},
    {"symbol": "TATAMOTORS.NS", "lot": 350, "itm": 10, "name": "TATA MOTORS", "sector": "AUTO"},
    {"symbol": "TATASTEEL.NS", "lot": 600, "itm": 10, "name": "TATA STEEL", "sector": "METAL"},
    {"symbol": "AXISBANK.NS", "lot": 500, "itm": 25, "name": "AXIS BANK", "sector": "BANK"},
    {"symbol": "MARUTI.NS", "lot": 150, "itm": 100, "name": "MARUTI", "sector": "AUTO"},
    {"symbol": "SUNPHARMA.NS", "lot": 400, "itm": 20, "name": "SUN PHARMA", "sector": "PHARMA"},
    {"symbol": "WIPRO.NS", "lot": 600, "itm": 40, "name": "WIPRO", "sector": "IT"},
    {"symbol": "HCLTECH.NS", "lot": 300, "itm": 100, "name": "HCL TECH", "sector": "IT"},
    {"symbol": "NTPC.NS", "lot": 1500, "itm": 10, "name": "NTPC", "sector": "ENERGY"},
    {"symbol": "POWERGRID.NS", "lot": 1200, "itm": 10, "name": "POWER GRID", "sector": "ENERGY"},
    {"symbol": "ONGC.NS", "lot": 1500, "itm": 10, "name": "ONGC", "sector": "ENERGY"},
    {"symbol": "M&M.NS", "lot": 500, "itm": 25, "name": "M&M", "sector": "AUTO"},
    {"symbol": "ULTRACEMCO.NS", "lot": 200, "itm": 100, "name": "ULTRATECH", "sector": "INFRA"},
    {"symbol": "NESTLEIND.NS", "lot": 100, "itm": 200, "name": "NESTLE", "sector": "FMCG"},
    {"symbol": "JSWSTEEL.NS", "lot": 600, "itm": 10, "name": "JSW STEEL", "sector": "METAL"},
    {"symbol": "TECHM.NS", "lot": 400, "itm": 50, "name": "TECH MAHINDRA", "sector": "IT"},
    {"symbol": "BAJAJFINSV.NS", "lot": 250, "itm": 100, "name": "BAJAJ FINSERV", "sector": "FINANCE"},
    {"symbol": "ASIANPAINT.NS", "lot": 300, "itm": 100, "name": "ASIAN PAINTS", "sector": "CONSUMER"},
    {"symbol": "GRASIM.NS", "lot": 200, "itm": 50, "name": "GRASIM", "sector": "INFRA"},
    {"symbol": "INDUSINDBK.NS", "lot": 350, "itm": 50, "name": "INDUSIND BANK", "sector": "BANK"},
    {"symbol": "BRITANNIA.NS", "lot": 300, "itm": 50, "name": "BRITANNIA", "sector": "FMCG"},
    {"symbol": "HDFCLIFE.NS", "lot": 350, "itm": 50, "name": "HDFC LIFE", "sector": "FINANCE"},
    {"symbol": "SBILIFE.NS", "lot": 300, "itm": 50, "name": "SBI LIFE", "sector": "FINANCE"},
    {"symbol": "DRREDDY.NS", "lot": 200, "itm": 100, "name": "DR REDDY", "sector": "PHARMA"},
    {"symbol": "DIVISLAB.NS", "lot": 200, "itm": 100, "name": "DIVIS LAB", "sector": "PHARMA"},
    {"symbol": "HAL.NS", "lot": 150, "itm": 20, "name": "HAL", "sector": "DEFENCE"},
    {"symbol": "ADANIENT.NS", "lot": 250, "itm": 50, "name": "ADANI ENTERPRISES", "sector": "ENERGY"},
    {"symbol": "ADANIPORTS.NS", "lot": 350, "itm": 25, "name": "ADANI PORTS", "sector": "ENERGY"},
]

# ================= Sector Mapping =================
SECTOR_INDEX = {
    "BANK": "^NSEBANK", "IT": "^CNXIT", "AUTO": "^CNXAUTO", "PHARMA": "^CNXPHARMA",
    "METAL": "^CNXMETAL", "FMCG": "^CNXFMCG", "FINANCE": "^CNXFINANCE", "ENERGY": "^CNXENERGY",
    "INFRA": "^CNXINFRA", "DEFENCE": "^CNXINFRA", "HEALTHCARE": "^NIFTY_HEALTHCARE",
    "CONSUMER": "^NIFTY_CONSR_DURBL", "TELECOM": "^CNXIT",
}

# ================= Session State =================
if "running" not in st.session_state:
    st.session_state.running = False
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
if "stock_trades" not in st.session_state:
    st.session_state.stock_trades = {}
    for stock in FO_STOCKS:
        qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit)
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
        qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit)
        st.session_state.stock_trades[stock["name"]] = {"buy_done": False, "sell_done": False, "trades": 0, "quantity": qty, "lots": lots}
    st.session_state.daily_loss = 0
    st.session_state.last_trade_date = get_ist_now().date()

MAX_DAILY_LOSS = 100000

# ================= Helper Functions =================
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
        if isinstance(close, pd.Series):
            close = close.dropna()
        ema9 = close.ewm(span=9).mean().iloc[-1]
        ema20 = close.ewm(span=20).mean().iloc[-1]
        if isinstance(ema9, pd.Series):
            ema9 = float(ema9.iloc[-1])
        if isinstance(ema20, pd.Series):
            ema20 = float(ema20.iloc[-1])
        if ema9 > ema20:
            return "BULLISH"
        elif ema9 < ema20:
            return "BEARISH"
    except:
        pass
    return "NEUTRAL"

def get_itm_strike(price, stock, option_type="CE"):
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

# ================= UI =================
st.markdown("<h1>📱 RUDRANSH PRO-ALGO - Real Trading System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>NIFTY | CRUDE OIL | NATURAL GAS | F&O STOCKS</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## 🎮 CONTROLS")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START ALL", use_container_width=True):
            st.session_state.running = True
            send_telegram("🤖 ALL ALGOS STARTED")
            st.success("All Algos Started!")
    with col2:
        if st.button("⏹️ STOP ALL", use_container_width=True):
            st.session_state.running = False
            send_telegram("🛑 ALL ALGOS STOPPED")
            st.warning("All Algos Stopped!")
    
    st.markdown("---")
    st.markdown("## 📌 ASSET SELECTION (ON/OFF)")
    
    st.session_state.enable_nifty = st.checkbox("📊 NIFTY", value=st.session_state.enable_nifty)
    if st.session_state.enable_nifty:
        st.session_state.nifty_lots = st.number_input("NIFTY Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots)
    
    st.session_state.enable_crude = st.checkbox("🛢️ CRUDE OIL", value=st.session_state.enable_crude)
    if st.session_state.enable_crude:
        st.session_state.crude_lots = st.number_input("CRUDE Lots", min_value=1, max_value=50, value=st.session_state.crude_lots)
    
    st.session_state.enable_ng = st.checkbox("🌿 NATURAL GAS", value=st.session_state.enable_ng)
    if st.session_state.enable_ng:
        st.session_state.ng_lots = st.number_input("NG Lots", min_value=1, max_value=50, value=st.session_state.ng_lots)
    
    st.session_state.enable_stocks = st.checkbox("📈 F&O STOCKS (50+)", value=st.session_state.enable_stocks)
    if st.session_state.enable_stocks:
        st.session_state.max_stocks_per_day = st.number_input("Max Stocks per Day", min_value=1, max_value=50, value=st.session_state.max_stocks_per_day)
        st.session_state.max_qty_limit = st.selectbox("Max Quantity per Trade", MAX_QTY_OPTIONS, index=MAX_QTY_OPTIONS.index(st.session_state.max_qty_limit) if st.session_state.max_qty_limit in MAX_QTY_OPTIONS else 14)
    
    st.markdown("---")
    st.markdown("### 📊 Daily Status")
    
    # Update stock quantities
    if st.session_state.enable_stocks:
        for stock in FO_STOCKS:
            qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit)
            st.session_state.stock_trades[stock["name"]]["quantity"] = qty
            st.session_state.stock_trades[stock["name"]]["lots"] = lots
        total_stocks_traded = sum([v["trades"] for v in st.session_state.stock_trades.values()])
        st.metric("Stocks Traded", f"{total_stocks_traded}/{st.session_state.max_stocks_per_day}")
    
    loss_color = "red" if st.session_state.daily_loss <= -MAX_DAILY_LOSS else "white"
    st.markdown(f"**Daily Loss:** <span style='color:{loss_color};'>₹{abs(st.session_state.daily_loss):,.0f}</span>", unsafe_allow_html=True)

# NIFTY Trend (Common for all)
nifty_trend = get_nifty_trend()
if nifty_trend == "BULLISH":
    st.success(f"🇮🇳 NIFTY TREND: BULLISH 🟢")
elif nifty_trend == "BEARISH":
    st.error(f"🇮🇳 NIFTY TREND: BEARISH 🔴")
else:
    st.info(f"🇮🇳 NIFTY TREND: SIDEWAYS 🟡")

st.markdown("---")

# ================= NIFTY SECTION =================
if st.session_state.enable_nifty and st.session_state.running:
    st.markdown("## 📊 NIFTY 50")
    
    symbol = SYMBOLS["NIFTY"]
    tp_sl = FIXED_TP_SL["NIFTY"]
    total_qty = st.session_state.nifty_lots * ASSET_LOT_SIZES["NIFTY"]
    current_price = get_live_price(symbol)
    
    if current_price > 0:
        itm_strike = int(current_price - tp_sl["itm"])
    else:
        itm_strike = 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("NIFTY Price", f"₹{current_price:,.2f}" if current_price > 0 else "Loading...")
    col2.metric(f"ITM Strike ({tp_sl['itm']} pts)", f"{itm_strike}")
    col3.metric("Quantity", total_qty)
    col4.metric("SL", f"{tp_sl['sl']} | TP: {tp_sl['tp1']}/{tp_sl['tp2']}/{tp_sl['tp3']}")
    
    now = get_ist_now()
    market_open = 9 <= now.hour < 14
    if market_open:
        st.info("🟢 NIFTY Market OPEN | 9:30 AM - 2:30 PM")
        st.success("🟢 NIFTY ALGO ACTIVE")
    else:
        st.info("⏸️ NIFTY Market CLOSED")
        st.warning("🔴 NIFTY ALGO WAITING")
    st.markdown("---")

# ================= CRUDE OIL SECTION =================
if st.session_state.enable_crude and st.session_state.running:
    st.markdown("## 🛢️ CRUDE OIL")
    
    symbol = SYMBOLS["CRUDEOIL"]
    tp_sl = FIXED_TP_SL["CRUDEOIL"]
    total_qty = st.session_state.crude_lots * ASSET_LOT_SIZES["CRUDEOIL"]
    current_price = get_live_price_inr(symbol)
    
    if current_price > 0:
        itm_strike = int(current_price - tp_sl["itm"])
    else:
        itm_strike = 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CRUDE Price", f"₹{current_price:,.2f}" if current_price > 0 else "Loading...")
    col2.metric(f"ITM Strike ({tp_sl['itm']} pts)", f"{itm_strike}")
    col3.metric("Quantity", total_qty)
    col4.metric("SL", f"{tp_sl['sl']} | TP: {tp_sl['tp1']}/{tp_sl['tp2']}/{tp_sl['tp3']}")
    
    now = get_ist_now()
    market_open = 18 <= now.hour < 22
    if market_open:
        st.info("🟢 CRUDE Market OPEN | 6:00 PM - 10:30 PM")
        st.success("🟢 CRUDE ALGO ACTIVE")
    else:
        st.info("⏸️ CRUDE Market CLOSED")
        st.warning("🔴 CRUDE ALGO WAITING")
    st.markdown("---")

# ================= NATURAL GAS SECTION =================
if st.session_state.enable_ng and st.session_state.running:
    st.markdown("## 🌿 NATURAL GAS")
    
    symbol = SYMBOLS["NATURALGAS"]
    tp_sl = FIXED_TP_SL["NATURALGAS"]
    total_qty = st.session_state.ng_lots * ASSET_LOT_SIZES["NATURALGAS"]
    current_price = get_live_price_inr(symbol)
    
    if current_price > 0:
        itm_strike = round(current_price - tp_sl["itm"], 1)
    else:
        itm_strike = 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("NG Price", f"₹{current_price:,.2f}" if current_price > 0 else "Loading...")
    col2.metric(f"ITM Strike ({tp_sl['itm']} pts)", f"{itm_strike}")
    col3.metric("Quantity", total_qty)
    col4.metric("SL", f"{tp_sl['sl']} | TP: {tp_sl['tp1']}/{tp_sl['tp2']}/{tp_sl['tp3']}")
    
    now = get_ist_now()
    market_open = 18 <= now.hour < 22
    if market_open:
        st.info("🟢 NG Market OPEN | 6:00 PM - 10:30 PM")
        st.success("🟢 NG ALGO ACTIVE")
    else:
        st.info("⏸️ NG Market CLOSED")
        st.warning("🔴 NG ALGO WAITING")
    st.markdown("---")

# ================= F&O STOCKS SECTION =================
if st.session_state.enable_stocks and st.session_state.running:
    st.markdown("## 🔍 SCANNING F&O STOCKS...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    results_container = st.container()
    
    signals_found = []
    trades_done = sum([v["trades"] for v in st.session_state.stock_trades.values()])
    loss_limit_hit = abs(st.session_state.daily_loss) >= MAX_DAILY_LOSS
    
    if loss_limit_hit:
        st.error(f"⚠️ DAILY LOSS LIMIT HIT (₹{MAX_DAILY_LOSS:,.0f})! Trading stopped for today. ⚠️")
    
    for idx, stock in enumerate(FO_STOCKS):
        progress_bar.progress((idx + 1) / len(FO_STOCKS))
        status_text.text(f"Scanning {stock['name']}...")
        if loss_limit_hit or trades_done >= st.session_state.max_stocks_per_day:
            if trades_done >= st.session_state.max_stocks_per_day:
                status_text.text(f"Daily limit reached ({st.session_state.max_stocks_per_day} stocks)")
            break
        
        try:
            current_price = get_live_price(stock["symbol"])
            if current_price <= 0:
                continue
            
            sector_bullish = get_sector_bullish(stock["sector"])
            sector_bearish = get_sector_bearish(stock["sector"])
            stock_trend = get_stock_trend(stock["symbol"])
            stock_bullish = (stock_trend == "BULLISH")
            stock_bearish = (stock_trend == "BEARISH")
            trade_done = st.session_state.stock_trades[stock["name"]]["trades"] >= 1
            trade_qty = st.session_state.stock_trades[stock["name"]]["quantity"]
            trade_lots = st.session_state.stock_trades[stock["name"]]["lots"]
            
            if nifty_trend == "BULLISH" and sector_bullish and stock_bullish and not trade_done:
                itm_strike = get_itm_strike(current_price, stock, "CE")
                estimated_premium = get_option_premium(stock["symbol"], itm_strike, "CE")
                tp_sl_calc = calculate_option_targets(estimated_premium, trade_qty)
                signals_found.append({"type": "BUY CE", "stock": stock["name"], "price": current_price, "itm_strike": itm_strike, "lots": trade_lots, "quantity": trade_qty, "itm_points": stock["itm"], "estimated_premium": estimated_premium, "tp_sl": tp_sl_calc})
                if st.session_state.running:
                    st.session_state.stock_trades[stock["name"]]["trades"] += 1
                    st.session_state.stock_trades[stock["name"]]["buy_done"] = True
                    trades_done += 1
                    send_telegram(f"🔵 REAL AUTO BUY {stock['name']} | {trade_lots} lots ({trade_qty} qty) | Strike: {itm_strike} CE")
            elif nifty_trend == "BEARISH" and sector_bearish and stock_bearish and not trade_done:
                itm_strike = get_itm_strike(current_price, stock, "PE")
                estimated_premium = get_option_premium(stock["symbol"], itm_strike, "PE")
                tp_sl_calc = calculate_option_targets(estimated_premium, trade_qty)
                signals_found.append({"type": "SELL PE", "stock": stock["name"], "price": current_price, "itm_strike": itm_strike, "lots": trade_lots, "quantity": trade_qty, "itm_points": stock["itm"], "estimated_premium": estimated_premium, "tp_sl": tp_sl_calc})
                if st.session_state.running:
                    st.session_state.stock_trades[stock["name"]]["trades"] += 1
                    st.session_state.stock_trades[stock["name"]]["sell_done"] = True
                    trades_done += 1
                    send_telegram(f"🔴 REAL AUTO SELL {stock['name']} | {trade_lots} lots ({trade_qty} qty) | Strike: {itm_strike} PE")
        except:
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    with results_container:
        if signals_found:
            st.success(f"✅ Found {len(signals_found)} Trading Opportunities!")
            for signal in signals_found:
                tp_sl_calc = signal["tp_sl"]
                color = "#00ff88" if signal["type"] == "BUY CE" else "#ff4b4b"
                st.markdown(f"<div style='background:#1e293b; padding:15px; border-radius:10px; margin:10px 0; border-left:5px solid {color};'><b>{'🟢' if signal['type'] == 'BUY CE' else '🔴'} {signal['stock']}</b><br>Action: <span style='color:{color};'>{signal['type']}</span><br>ITM Strike: {signal['itm_strike']} ({signal['itm_points']} pts ITM)<br>Est. Premium: ₹{signal['estimated_premium']:.2f}<br>🎯 TP/SL: SL: {tp_sl_calc['sl_percent']}% | TP1: {tp_sl_calc['tp1_percent']}% | TP2: {tp_sl_calc['tp2_percent']}% | TP3: {tp_sl_calc['tp3_percent']}%<br>Lots: {signal['lots']} | Qty: {signal['quantity']}<br>✅ Condition: {'NIFTY Bullish + Sector Bullish + Stock Bullish' if signal['type'] == 'BUY CE' else 'NIFTY Bearish + Sector Bearish + Stock Bearish'}</div>", unsafe_allow_html=True)
        else:
            st.info("📭 No trading opportunities found at this moment.")
    
    st.markdown("---")
    st.markdown("### 📊 Today's Executed Trades")
    trade_data = []
    for stock in FO_STOCKS:
        status = st.session_state.stock_trades[stock["name"]]
        if status["trades"] > 0:
            trade_data.append({"Stock": stock["name"], "Lots": status["lots"], "Quantity": status["quantity"], "Buy CE": "✅" if status["buy_done"] else "❌", "Sell PE": "✅" if status["sell_done"] else "❌"})
    if trade_data:
        st.dataframe(pd.DataFrame(trade_data), use_container_width=True)

# ================= Common Status =================
st.markdown("---")
loss_limit_hit = abs(st.session_state.daily_loss) >= MAX_DAILY_LOSS
if loss_limit_hit:
    st.error(f"⚠️ DAILY LOSS LIMIT HIT (₹{MAX_DAILY_LOSS:,.0f})! Trading stopped for today. ⚠️")
elif st.session_state.running:
    active_count = sum([st.session_state.enable_nifty, st.session_state.enable_crude, st.session_state.enable_ng, st.session_state.enable_stocks])
    st.success(f"🟢 ALGO RUNNING | {active_count} Assets Active")
else:
    st.warning("🔴 ALGO STOPPED")

# ================= TP/SL Info =================
st.markdown("---")
st.markdown("### 🎯 TP/SL Settings Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**NIFTY**")
    st.markdown(f"SL: {FIXED_TP_SL['NIFTY']['sl']} | TP1: {FIXED_TP_SL['NIFTY']['tp1']} | TP2: {FIXED_TP_SL['NIFTY']['tp2']} | TP3: {FIXED_TP_SL['NIFTY']['tp3']}")
with col2:
    st.markdown("**CRUDE OIL**")
    st.markdown(f"SL: {FIXED_TP_SL['CRUDEOIL']['sl']} | TP1: {FIXED_TP_SL['CRUDEOIL']['tp1']} | TP2: {FIXED_TP_SL['CRUDEOIL']['tp2']} | TP3: {FIXED_TP_SL['CRUDEOIL']['tp3']}")
with col3:
    st.markdown("**NATURAL GAS**")
    st.markdown(f"SL: {FIXED_TP_SL['NATURALGAS']['sl']} | TP1: {FIXED_TP_SL['NATURALGAS']['tp1']} | TP2: {FIXED_TP_SL['NATURALGAS']['tp2']} | TP3: {FIXED_TP_SL['NATURALGAS']['tp3']}")

# ================= Clock =================
st.caption(f"🕐 IST: {get_ist_now().strftime('%H:%M:%S')} | REAL TRADING MODE | Refresh manually for latest data")
