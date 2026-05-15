import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests

st.set_page_config(page_title="Rudransh Pro-Algo - Complete Auto Trading", layout="wide")

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
    "NIFTY": {"sl": 30, "tp1": 15, "tp2": 22, "tp3": 30, "itm": 100, "strike_interval": 50, "use_nifty_filter": True},
    "CRUDEOIL": {"sl": 30, "tp1": 15, "tp2": 20, "tp3": 25, "itm": 100, "strike_interval": 50, "use_nifty_filter": False},
    "NATURALGAS": {"sl": 1.50, "tp1": 1.00, "tp2": 1.50, "tp3": 2.00, "itm": 10, "strike_interval": 5, "use_nifty_filter": False}
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

# ================= ITM STRIKE CALCULATION =================
def get_itm_strike(price, asset_type):
    if price <= 0:
        return 0, 0
    
    settings = FIXED_TP_SL[asset_type]
    itm_points = settings["itm"]
    strike_interval = settings["strike_interval"]
    
    target_strike = price - itm_points
    rounded_strike = round(target_strike / strike_interval) * strike_interval
    
    if asset_type == "NATURALGAS" and rounded_strike < 50:
        rounded_strike = 50
    elif rounded_strike < 100:
        rounded_strike = 100
    
    actual_itm = price - rounded_strike
    
    return int(rounded_strike), actual_itm

# ================= OPTION TP/SL BASED ON PREMIUM (FOR STOCKS) =================
def get_option_tp_sl(entry_premium):
    if entry_premium <= 50:
        return {"sl_percent": 30, "tp1_percent": 20, "tp2_percent": 40, "tp3_percent": 60, "sl_points": 1.50, "tp1_points": 1.00, "tp2_points": 1.50, "tp3_points": 2.00}
    elif entry_premium <= 150:
        return {"sl_percent": 25, "tp1_percent": 15, "tp2_percent": 30, "tp3_percent": 50, "sl_points": 2.00, "tp1_points": 1.50, "tp2_points": 3.00, "tp3_points": 5.00}
    elif entry_premium <= 300:
        return {"sl_percent": 20, "tp1_percent": 12, "tp2_percent": 25, "tp3_percent": 40, "sl_points": 5.00, "tp1_points": 3.00, "tp2_points": 6.00, "tp3_points": 10.00}
    elif entry_premium <= 500:
        return {"sl_percent": 15, "tp1_percent": 10, "tp2_percent": 20, "tp3_percent": 30, "sl_points": 10.00, "tp1_points": 5.00, "tp2_points": 10.00, "tp3_points": 15.00}
    elif entry_premium <= 1000:
        return {"sl_percent": 12, "tp1_percent": 8, "tp2_percent": 15, "tp3_percent": 25, "sl_points": 15.00, "tp1_points": 8.00, "tp2_points": 15.00, "tp3_points": 25.00}
    else:
        return {"sl_percent": 10, "tp1_percent": 6, "tp2_percent": 12, "tp3_percent": 20, "sl_points": 20.00, "tp1_points": 10.00, "tp2_points": 20.00, "tp3_points": 30.00}

def calculate_option_targets(entry_premium, quantity):
    tp_sl = get_option_tp_sl(entry_premium)
    
    sl_price = entry_premium - tp_sl["sl_points"]
    tp1_price = entry_premium + tp_sl["tp1_points"]
    tp2_price = entry_premium + tp_sl["tp2_points"]
    tp3_price = entry_premium + tp_sl["tp3_points"]
    
    qty_tp1 = quantity // 2
    qty_tp2 = quantity // 4
    qty_tp3 = quantity - qty_tp1 - qty_tp2
    
    tp1_profit = qty_tp1 * tp_sl["tp1_points"]
    tp2_profit = qty_tp2 * tp_sl["tp2_points"]
    tp3_profit = qty_tp3 * tp_sl["tp3_points"]
    sl_loss = quantity * tp_sl["sl_points"]
    
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
        "sl_points": tp_sl["sl_points"],
        "tp1_points": tp_sl["tp1_points"],
        "tp2_points": tp_sl["tp2_points"],
        "tp3_points": tp_sl["tp3_points"]
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
if "control_mode" not in st.session_state:
    st.session_state.control_mode = "AUTO"
if "force_start" not in st.session_state:
    st.session_state.force_start = False
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
def get_sector_symbol(ticker):
    ticker_upper = ticker.upper()
    
    if any(x in ticker_upper for x in ["HDFCBANK", "ICICIBANK", "SBIN", "AXISBANK", "KOTAKBANK", "PNB"]):
        return "^NSEBANK"
    elif any(x in ticker_upper for x in ["TCS", "INFY", "WIPRO", "TECHM", "HCLTECH"]):
        return "^CNXIT"
    elif any(x in ticker_upper for x in ["TATAMOTORS", "MARUTI", "M&M", "BAJAJ-AUTO", "EICHERMOT"]):
        return "^CNXAUTO"
    elif any(x in ticker_upper for x in ["SUNPHARMA", "DRREDDY", "CIPLA", "LUPIN"]):
        return "^CNXPHARMA"
    elif any(x in ticker_upper for x in ["TATASTEEL", "HINDALCO", "JSWSTEEL", "SAIL"]):
        return "^CNXMETAL"
    elif any(x in ticker_upper for x in ["HINDUNILVR", "ITC", "NESTLEIND", "BRITANNIA"]):
        return "^CNXFMCG"
    elif any(x in ticker_upper for x in ["DLF", "GODREJPROP", "OBEROIRLTY"]):
        return "^CNXREALTY"
    elif any(x in ticker_upper for x in ["RELIANCE", "ONGC", "POWERGRID"]):
        return "^CNXENERGY"
    elif any(x in ticker_upper for x in ["BANKBARODA", "CANBK", "UNIONBANK"]):
        return "^CNXPSUBANK"
    elif any(x in ticker_upper for x in ["BAJFINANCE", "CHOLAFIN", "SHRIRAMFIN"]):
        return "^CNXFINANCE"
    elif any(x in ticker_upper for x in ["LT", "NBCC", "IRB"]):
        return "^CNXINFRA"
    elif any(x in ticker_upper for x in ["HAL", "BEL", "BDL"]):
        return "^NIFTY_IND_DEFENCE"
    elif any(x in ticker_upper for x in ["APOLLOHOSP", "MAXHEALTH", "FORTIS"]):
        return "^NIFTY_HEALTHCARE"
    elif any(x in ticker_upper for x in ["DIXON", "VOLTAS", "WHIRLPOOL"]):
        return "^NIFTY_CONSR_DURBL"
    else:
        return "^NSEI"

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

# ================= Trading Hours Check Functions =================
def is_nifty_market_open():
    now = get_ist_now()
    return 9 <= now.hour < 14

def is_commodity_market_open():
    now = get_ist_now()
    return 18 <= now.hour < 22

def is_stock_market_open():
    now = get_ist_now()
    return 9 <= now.hour < 14

def should_algo_run(asset_type):
    if st.session_state.control_mode == "MANUAL":
        return st.session_state.running
    if st.session_state.force_start:
        return True
    if asset_type == "NIFTY":
        return is_nifty_market_open()
    elif asset_type in ["CRUDEOIL", "NATURALGAS"]:
        return is_commodity_market_open()
    elif asset_type == "STOCKS":
        return is_stock_market_open()
    return False

# ================= Display Asset Section =================
def display_asset_section(asset_type, display_name, symbol, tp_sl, lot_size, total_qty, is_commodity=False):
    if is_commodity:
        current_price = get_live_price_inr(symbol)
    else:
        current_price = get_live_price(symbol)
    
    if current_price > 0:
        strike, actual_itm = get_itm_strike(current_price, asset_type)
    else:
        strike = 0
        actual_itm = 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"📊 {display_name} Price", f"₹{current_price:,.2f}" if current_price > 0 else "Loading...")
    col2.metric(f"🎯 ITM Strike ({tp_sl['itm']} pts)", f"{strike} ({actual_itm:.1f} pts ITM)" if strike > 0 else "N/A")
    col3.metric("📦 Quantity", total_qty)
    col4.metric("🎯 TP/SL", f"SL: {tp_sl['sl']} | T1:{tp_sl['tp1']} T2:{tp_sl['tp2']} T3:{tp_sl['tp3']}")
    
    st.markdown("---")
    
    if asset_type == "NIFTY":
        market_open = is_nifty_market_open()
        hours_text = "9:30 AM - 2:30 PM IST"
    else:
        market_open = is_commodity_market_open()
        hours_text = "6:00 PM - 10:30 PM IST"
    
    algo_active = should_algo_run(asset_type) and st.session_state.enable_nifty if asset_type == "NIFTY" else should_algo_run(asset_type) and (st.session_state.enable_crude if asset_type == "CRUDEOIL" else st.session_state.enable_ng if asset_type == "NATURALGAS" else True)
    
    if market_open:
        st.info(f"🟢 {display_name} Market OPEN | {hours_text}")
        if algo_active:
            st.success(f"🟢 {display_name} ALGO ACTIVE")
        else:
            if st.session_state.control_mode == "AUTO":
                st.warning(f"🔴 {display_name} ALGO WAITING (Auto Mode - Market Hours)")
            else:
                st.warning(f"🔴 {display_name} ALGO STOPPED (Manual Mode - Press START ALL)")
    else:
        st.info(f"⏸️ {display_name} Market CLOSED | {hours_text}")
        if st.session_state.force_start and st.session_state.control_mode == "AUTO":
            st.warning(f"⚠️ {display_name} FORCE START ACTIVE (Testing Mode)")
    
    st.markdown("---")

# ================= CALCULATE SIGNALS (BREAKOUT/BREAKDOWN CONFIRMATION ONLY) =================
def calculate_signals():
    symbol = SYMBOLS[asset]
    
    # NIFTY data
    nifty_df = yf.download("^NSEI", period="7d", interval="5m", progress=False)
    nifty_df.columns = [str(c).lower() for c in nifty_df.columns]
    
    # Sector data
    sector_symbol = get_sector_symbol(asset)
    sector_df = yf.download(sector_symbol, period="7d", interval="5m", progress=False)
    sector_df.columns = [str(c).lower() for c in sector_df.columns]
    
    # Stock data
    stock_df = yf.download(symbol, period="7d", interval="5m", progress=False)
    
    if stock_df.empty or len(stock_df) < 30:
        return {"signal": "WAIT", "buy": False, "sell": False, "price": price, "trend": "NEUTRAL", "rsi": 50, "adx": 0, "ema20": price}
    
    stock_df.columns = [str(c).lower() for c in stock_df.columns]
    
    if 'close' not in stock_df.columns:
        return {"signal": "WAIT", "buy": False, "sell": False, "price": price, "trend": "NEUTRAL", "rsi": 50, "adx": 0, "ema20": price}
    
    # NIFTY Trend
    nifty_positive = False
    nifty_negative = False
    
    if not nifty_df.empty and 'close' in nifty_df.columns:
        nifty_ema20 = nifty_df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
        nifty_current = nifty_df['close'].iloc[-1]
        nifty_positive = nifty_current > nifty_ema20
        nifty_negative = nifty_current < nifty_ema20
    
    # Sector Trend
    sector_bullish = False
    sector_bearish = False
    
    if not sector_df.empty and 'close' in sector_df.columns:
        sector_ema20 = sector_df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
        sector_current = sector_df['close'].iloc[-1]
        sector_bullish = sector_current > sector_ema20
        sector_bearish = sector_current < sector_ema20
    
    # Stock Calculations
    close = stock_df['close']
    high = stock_df['high'] if 'high' in stock_df.columns else close
    low = stock_df['low'] if 'low' in stock_df.columns else close
    volume = stock_df['volume'] if 'volume' in stock_df.columns else pd.Series([1000000] * len(stock_df))
    
    ema9 = close.ewm(span=9, adjust=False).mean()
    ema20 = close.ewm(span=20, adjust=False).mean()
    ema200 = close.ewm(span=200, adjust=False).mean()
    
    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Volume Filter
    volume_sma = volume.rolling(20).mean()
    volume_filter = volume.iloc[-1] > volume_sma.iloc[-1] if not volume_sma.isna().iloc[-1] else True
    
    # ADX
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
    
    # Sideways
    current_rsi = rsi.iloc[-1]
    sideways = (45 < current_rsi < 55) and adx < 20
    
    # Strong Bull/Bear
    c1 = stock_df.iloc[-2]
    c2 = stock_df.iloc[-1]
    
    strong_bull = c2['close'] > c2['open'] and c2['close'] > c1['high']
    strong_bear = c2['close'] < c2['open'] and c2['close'] < c1['low']
    
    current_price = close.iloc[-1]
    current_ema9 = ema9.iloc[-1]
    current_ema20 = ema20.iloc[-1]
    current_ema200 = ema200.iloc[-1] if not ema200.isna().all() else current_price
    
    # MTF Trends
    tf5_df = yf.download(symbol, period="2d", interval="5m", progress=False)
    if not tf5_df.empty and 'Close' in tf5_df.columns:
        tf5_close = tf5_df['Close'].iloc[-1]
        tf5_ema = tf5_df['Close'].ewm(span=20).mean().iloc[-1]
        trend5_up = tf5_close > tf5_ema
    else:
        trend5_up = current_price > current_ema20
    
    tf15_df = yf.download(symbol, period="3d", interval="15m", progress=False)
    if not tf15_df.empty and 'Close' in tf15_df.columns:
        tf15_close = tf15_df['Close'].iloc[-1]
        tf15_ema = tf15_df['Close'].ewm(span=20).mean().iloc[-1]
        trend15_up = tf15_close > tf15_ema
    else:
        trend15_up = current_price > current_ema20
    
    tf1h_df = yf.download(symbol, period="5d", interval="60m", progress=False)
    if not tf1h_df.empty and 'Close' in tf1h_df.columns:
        tf1h_close = tf1h_df['Close'].iloc[-1]
        tf1h_ema = tf1h_df['Close'].ewm(span=20).mean().iloc[-1]
        trend1h_up = tf1h_close > tf1h_ema
    else:
        trend1h_up = current_price > current_ema20
    
    # Strict Conditions
    strong_bull_stock = (current_ema9 > current_ema20 and current_price > current_ema200 and current_rsi >= 60 and adx >= 25 and volume_filter and strong_bull and current_price > c1['high'])
    strong_bear_stock = (current_ema9 < current_ema20 and current_price < current_ema200 and current_rsi <= 40 and adx >= 25 and volume_filter and strong_bear and current_price < c1['low'])
    
    # ================= RESISTANCE / SUPPORT CONFIRMATION =================
    lookback = 20
    resistance = high.rolling(lookback).max().iloc[-1]
    support = low.rolling(lookback).min().iloc[-1]
    
    # TRUE BREAKOUT = प्राइस रेझिस्टन्सच्या वर बंद झाली
    confirmed_breakout = current_price > resistance
    # TRUE BREAKDOWN = प्राइस सपोर्टच्या खाली बंद झाली
    confirmed_breakdown = current_price < support
    
    # ================= FINAL BUY/SELL (STRICT + CONFIRMATION) =================
    strict_buy = (nifty_positive and not nifty_negative and not sideways and sector_bullish and strong_bull_stock and trend5_up and trend15_up and trend1h_up and current_price > current_ema20)
    strict_sell = (nifty_negative and not nifty_positive and not sideways and sector_bearish and strong_bear_stock and not trend5_up and not trend15_up and not trend1h_up and current_price < current_ema20)
    
    # फक्त कन्फर्म्ड ब्रेकआउट झाल्यावरच बाय सिग्नल, आणि ब्रेकडाउन झाल्यावरच सेल सिग्नल
    buy_condition = strict_buy and confirmed_breakout
    sell_condition = strict_sell and confirmed_breakdown
    
    # Cooldown
    cooldown_ok = (get_ist_now() - st.session_state.last_trade_time).seconds > 300
    
    if buy_condition and cooldown_ok and st.session_state.last_trade_side != "BUY":
        signal = "BUY"
        buy_signal = True
        sell_signal = False
    elif sell_condition and cooldown_ok and st.session_state.last_trade_side != "SELL":
        signal = "SELL"
        buy_signal = False
        sell_signal = True
    else:
        signal = "WAIT"
        buy_signal = False
        sell_signal = False
    
    return {
        "signal": signal,
        "buy": buy_signal,
        "sell": sell_signal,
        "price": current_price,
        "trend": "BULLISH" if current_price > current_ema20 else "BEARISH",
        "rsi": current_rsi,
        "adx": adx,
        "ema20": current_ema20,
        "sideways": sideways,
        "sector_bullish": sector_bullish,
        "nifty_positive": nifty_positive,
        "strict_buy": strict_buy,
        "resistance": resistance,
        "support": support,
        "breakout": confirmed_breakout,
        "breakdown": confirmed_breakdown
    }

# ================= UI =================
st.markdown("<h1>📱 RUDRANSH PRO-ALGO - Complete Auto Trading System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>NIFTY | CRUDE OIL | NATURAL GAS | F&O STOCKS</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ffaa00;'>🎯 TP2 Hit = SL Shift to TP1 | TP3 Hit = Auto Exit</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ffaa00;'>🔒 BUY Signal only after CONFIRMED BREAKOUT | SELL Signal only after CONFIRMED BREAKDOWN</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## 🎮 CONTROL MODE")
    
    control_mode = st.radio(
        "Select Control Mode",
        ["🤖 AUTO MODE (Trading Hours)", "👆 MANUAL MODE"],
        index=0 if st.session_state.control_mode == "AUTO" else 1
    )
    st.session_state.control_mode = "AUTO" if "AUTO" in control_mode else "MANUAL"
    
    if st.session_state.control_mode == "AUTO":
        st.info("🕐 AUTO MODE: Trading Hours नुसार Auto Start/Stop")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚠️ FORCE START", use_container_width=True):
                st.session_state.force_start = True
                send_telegram("⚠️ FORCE START ACTIVATED (Testing Mode)")
                st.success("Force Start ON!")
        with col2:
            if st.button("🔴 FORCE STOP", use_container_width=True):
                st.session_state.force_start = False
                st.session_state.running = False
                send_telegram("🔴 FORCE STOP ACTIVATED")
                st.warning("Force Start OFF!")
        st.caption("Force Start = Market बंद असताना पण Algo सुरू करण्यासाठी (Testing)")
    
    else:
        st.info("👆 MANUAL MODE: तुम्ही स्वतः START/STOP करा")
        st.session_state.force_start = False
        totp_code = st.text_input("🔐 TOTP Code (Google Authenticator)", type="password", placeholder="Enter 6 digit code", key="totp_input")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ START", use_container_width=True):
                if totp_code and len(totp_code) == 6:
                    st.session_state.running = True
                    send_telegram("🤖 ALGO STARTED (Manual Mode)")
                    st.success("Started! Algo is now RUNNING")
                else:
                    st.error("❌ Please enter valid 6-digit TOTP code!")
        with col2:
            if st.button("⏹️ STOP", use_container_width=True):
                st.session_state.running = False
                send_telegram("🛑 ALGO STOPPED (Manual Mode)")
                st.warning("Stopped!")
        st.caption("📱 TOTP Code: Google Authenticator app मध्ये Angel One साठी दिसणारा 6 अंकी कोड")
    
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
        st.info("⏰ Stock Options Trading Hours: 9:30 AM - 2:30 PM IST")
    
    st.markdown("---")
    st.markdown("### 📊 Daily Status")
    
    if st.session_state.enable_stocks:
        for stock in FO_STOCKS:
            qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit)
            st.session_state.stock_trades[stock["name"]]["quantity"] = qty
            st.session_state.stock_trades[stock["name"]]["lots"] = lots
        total_stocks_traded = sum([v["trades"] for v in st.session_state.stock_trades.values()])
        st.metric("Stocks Traded", f"{total_stocks_traded}/{st.session_state.max_stocks_per_day}")
    
    loss_color = "red" if st.session_state.daily_loss <= -MAX_DAILY_LOSS else "white"
    st.markdown(f"**Daily Loss:** <span style='color:{loss_color};'>₹{abs(st.session_state.daily_loss):,.0f}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Current Mode")
    if st.session_state.control_mode == "AUTO":
        st.markdown(f"**Mode:** 🤖 AUTO")
        if st.session_state.force_start:
            st.markdown("**Force Start:** ⚠️ ACTIVE")
        else:
            st.markdown("**Force Start:** ❌ OFF")
    else:
        st.markdown("**Mode:** 👆 MANUAL")
        if st.session_state.running:
            st.markdown("**Status:** 🟢 RUNNING")
        else:
            st.markdown("**Status:** 🔴 STOPPED")
    
    st.markdown("---")
    st.markdown("### 🎯 Auto SL/TP Rules")
    st.caption("• TP1 Hit: 50% Profit Book")
    st.caption("• TP2 Hit: 25% Profit Book + SL Shift to TP1")
    st.caption("• TP3 Hit: 25% Auto Exit")

# NIFTY Trend
nifty_trend = get_nifty_trend()
st.markdown("### 🇮🇳 NIFTY TREND (For NIFTY & Stocks Only)")
if nifty_trend == "BULLISH":
    st.success(f"NIFTY TREND: BULLISH 🟢")
elif nifty_trend == "BEARISH":
    st.error(f"NIFTY TREND: BEARISH 🔴")
else:
    st.info(f"NIFTY TREND: SIDEWAYS 🟡")
st.markdown("---")

# ================= NIFTY SECTION =================
if st.session_state.enable_nifty:
    st.markdown("## 📊 NIFTY 50")
    total_qty = st.session_state.nifty_lots * ASSET_LOT_SIZES["NIFTY"]
    display_asset_section("NIFTY", "NIFTY", SYMBOLS["NIFTY"], FIXED_TP_SL["NIFTY"], ASSET_LOT_SIZES["NIFTY"], total_qty, is_commodity=False)

# ================= CRUDE OIL SECTION =================
if st.session_state.enable_crude:
    st.markdown("## 🛢️ CRUDE OIL")
    total_qty = st.session_state.crude_lots * ASSET_LOT_SIZES["CRUDEOIL"]
    display_asset_section("CRUDEOIL", "CRUDE OIL", SYMBOLS["CRUDEOIL"], FIXED_TP_SL["CRUDEOIL"], ASSET_LOT_SIZES["CRUDEOIL"], total_qty, is_commodity=True)

# ================= NATURAL GAS SECTION =================
if st.session_state.enable_ng:
    st.markdown("## 🌿 NATURAL GAS")
    total_qty = st.session_state.ng_lots * ASSET_LOT_SIZES["NATURALGAS"]
    display_asset_section("NATURALGAS", "NATURAL GAS", SYMBOLS["NATURALGAS"], FIXED_TP_SL["NATURALGAS"], ASSET_LOT_SIZES["NATURALGAS"], total_qty, is_commodity=True)

# ================= F&O STOCKS SECTION =================
if st.session_state.enable_stocks and (st.session_state.running if st.session_state.control_mode == "MANUAL" else should_algo_run("STOCKS")):
    st.markdown("## 🔍 SCANNING F&O STOCKS...")
    
    stock_market_open = is_stock_market_open()
    
    if not stock_market_open and not st.session_state.force_start:
        st.info("⏸️ Stock Options Market CLOSED | Trading Hours: 9:30 AM - 2:30 PM IST")
    else:
        if st.session_state.force_start:
            st.warning("⚠️ FORCE START ACTIVE - Scanning stocks outside market hours (Testing Only)")
        
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
                
                # स्टॉक्ससाठी हीच ब्रेकआउट/ब्रेकडाउन कंडिशन (स्टॉकच्या स्वतःच्या डेटावरून)
                stock_high = stock_df['high'] if 'high' in stock_df.columns else pd.Series([current_price])
                stock_low = stock_df['low'] if 'low' in stock_df.columns else pd.Series([current_price])
                res = stock_high.rolling(20).max().iloc[-1]
                sup = stock_low.rolling(20).min().iloc[-1]
                breakout_confirmed = current_price > res
                breakdown_confirmed = current_price < sup
                
                if nifty_trend == "BULLISH" and sector_bullish and stock_bullish and not trade_done and breakout_confirmed:
                    itm_strike = get_stock_itm_strike(current_price, stock, "CE")
                    estimated_premium = get_option_premium(stock["symbol"], itm_strike, "CE")
                    tp_sl_calc = calculate_option_targets(estimated_premium, trade_qty)
                    signals_found.append({"type": "BUY CE", "stock": stock["name"], "price": current_price, "itm_strike": itm_strike, "lots": trade_lots, "quantity": trade_qty, "itm_points": stock["itm"], "estimated_premium": estimated_premium, "tp_sl": tp_sl_calc})
                    if st.session_state.running or st.session_state.force_start:
                        st.session_state.stock_trades[stock["name"]]["trades"] += 1
                        st.session_state.stock_trades[stock["name"]]["buy_done"] = True
                        trades_done += 1
                        send_telegram(f"🔵 REAL AUTO BUY {stock['name']} | {trade_lots} lots ({trade_qty} qty) | Strike: {itm_strike} CE (Breakout Confirmed)")
                elif nifty_trend == "BEARISH" and sector_bearish and stock_bearish and not trade_done and breakdown_confirmed:
                    itm_strike = get_stock_itm_strike(current_price, stock, "PE")
                    estimated_premium = get_option_premium(stock["symbol"], itm_strike, "PE")
                    tp_sl_calc = calculate_option_targets(estimated_premium, trade_qty)
                    signals_found.append({"type": "SELL PE", "stock": stock["name"], "price": current_price, "itm_strike": itm_strike, "lots": trade_lots, "quantity": trade_qty, "itm_points": stock["itm"], "estimated_premium": estimated_premium, "tp_sl": tp_sl_calc})
                    if st.session_state.running or st.session_state.force_start:
                        st.session_state.stock_trades[stock["name"]]["trades"] += 1
                        st.session_state.stock_trades[stock["name"]]["sell_done"] = True
                        trades_done += 1
                        send_telegram(f"🔴 REAL AUTO SELL {stock['name']} | {trade_lots} lots ({trade_qty} qty) | Strike: {itm_strike} PE (Breakdown Confirmed)")
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
                    st.markdown(f"""
                    <div style='background:#1e293b; padding:15px; border-radius:10px; margin:10px 0; border-left:5px solid {color};'>
                        <b>{'🟢' if signal['type'] == 'BUY CE' else '🔴'} {signal['stock']}</b><br>
                        Action: <span style='color:{color};'>{signal['type']}</span><br>
                        ITM Strike: {signal['itm_strike']} ({signal['itm_points']} pts ITM)<br>
                        Est. Premium: ₹{signal['estimated_premium']:.2f}<br>
                        🎯 TP/SL: SL: {tp_sl_calc['sl_points']} pts | TP1: {tp_sl_calc['tp1_points']} pts | TP2: {tp_sl_calc['tp2_points']} pts | TP3: {tp_sl_calc['tp3_points']} pts<br>
                        🛡️ TP2 Hit → SL Shift to TP1 ({tp_sl_calc['tp1_points']} pts)<br>
                        🚪 TP3 Hit → Auto Exit<br>
                        Lots: {signal['lots']} | Qty: {signal['quantity']}<br>
                        🔒 Confirmed {'Breakout' if signal['type'] == 'BUY CE' else 'Breakdown'}<br>
                        ✅ Condition: {'NIFTY Bullish + Sector Bullish + Stock Bullish' if signal['type'] == 'BUY CE' else 'NIFTY Bearish + Sector Bearish + Stock Bearish'}
                    </div>
                    """, unsafe_allow_html=True)
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
elif st.session_state.enable_stocks and not (st.session_state.running if st.session_state.control_mode == "MANUAL" else should_algo_run("STOCKS")):
    if st.session_state.control_mode == "MANUAL" and not st.session_state.running:
        st.info("📈 F&O STOCKS ALGO STOPPED | Press START to begin scanning")
    else:
        st.info("📈 F&O STOCKS ALGO WAITING | Trading Hours: 9:30 AM - 2:30 PM IST")
elif not st.session_state.enable_stocks:
    pass

# ================= Common Status =================
st.markdown("---")
loss_limit_hit = abs(st.session_state.daily_loss) >= MAX_DAILY_LOSS
if loss_limit_hit:
    st.error(f"⚠️ DAILY LOSS LIMIT HIT (₹{MAX_DAILY_LOSS:,.0f})! Trading stopped for today. ⚠️")
else:
    if st.session_state.control_mode == "AUTO":
        if st.session_state.force_start:
            st.warning("⚠️ FORCE START MODE ACTIVE - Trading outside market hours (Testing Only)")
        else:
            st.success("🟢 AUTO MODE ACTIVE - Trading will start/stop automatically as per market hours")
    else:
        if st.session_state.running:
            st.success("🟢 MANUAL MODE ACTIVE - Algo is RUNNING (Press STOP to stop)")
        else:
            st.warning("🔴 MANUAL MODE ACTIVE - Algo is STOPPED (Press START to begin)")

# ================= TP/SL Info =================
st.markdown("---")
st.markdown("### 🎯 Auto SL/TP Rules Summary")
st.markdown("""
| Rule | Action |
|------|--------|
| **TP1 Hit** | 50% Quantity Booked (Profit Locked) |
| **TP2 Hit** | 25% Quantity Booked + **SL Shifted to TP1 Level** (Remaining trade secured) |
| **TP3 Hit** | 25% Quantity **Auto Exit** (Complete Trade Closed) |
""")

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
st.caption(f"🕐 IST: {get_ist_now().strftime('%H:%M:%S')} | Mode: {st.session_state.control_mode} | NIFTY/Stocks: 9:30-2:30 | Commodities: 6:00-10:30 | TP2=SL Shift to TP1 | TP3=Auto Exit | Breakout/Breakdown Confirmation Required")
