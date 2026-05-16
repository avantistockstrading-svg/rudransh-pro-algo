# ============================================================
# RUDRANSH PRO ALGO X
# DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114
# ============================================================

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO ALGO X", layout="wide", page_icon="📊")

# ================= IST Timezone =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= APP LOCK SESSION STATE =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False
if "app_password" not in st.session_state:
    st.session_state.app_password = "8055"

# ================= Q4 RESULT DATA WITH DATES =================
if "q4_results" not in st.session_state:
    st.session_state.q4_results = {
        "HDFC Bank": {"profit": 9.1, "verdict": "Mixed", "date": "15 May 2026", "revenue": 88500, "key": "Deposits grew 14.4%, but NII missed estimates"},
        "Reliance Industries": {"profit": -12.5, "verdict": "Negative", "date": "14 May 2026", "revenue": 234000, "key": "Retail strong, Energy business weak"},
        "Infosys": {"profit": 11.6, "verdict": "Cautious", "date": "16 May 2026", "revenue": 42000, "key": "Revenue declined 1.3% QoQ, weak guidance"},
        "Maruti Suzuki": {"profit": -6.5, "verdict": "Negative", "date": "13 May 2026", "revenue": 38500, "key": "Record sales but margin pressure"},
        "Tata Motors": {"profit": -32.0, "verdict": "Negative", "date": "12 May 2026", "revenue": 120000, "key": "India PV strong, JLR weak"},
        "Bharat Electronics": {"profit": 0, "verdict": "Pending", "date": "19 May 2026 (Today)", "revenue": 0, "key": "Expected Positive"},
        "BPCL": {"profit": 0, "verdict": "Pending", "date": "19 May 2026 (Today)", "revenue": 0, "key": "Expected Neutral/Negative"},
        "Zydus Lifesciences": {"profit": 0, "verdict": "Pending", "date": "19 May 2026 (Today)", "revenue": 0, "key": "Expected Positive"},
        "Mankind Pharma": {"profit": 0, "verdict": "Pending", "date": "19 May 2026 (Today)", "revenue": 0, "key": "Expected Positive"},
        "PI Industries": {"profit": 0, "verdict": "Pending", "date": "19 May 2026 (Today)", "revenue": 0, "key": "Expected Positive"},
    }

# ================= FIXED TARGETS =================
FIXED_TARGETS = {
    "NIFTY": 10,
    "CRUDEOIL": 10,
    "NATURALGAS": 1,
}

# ================= TRADE COUNTERS =================
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

# ================= 69 F&O STOCKS (Shortened for brevity) =================
FO_STOCKS = [
    {"symbol": "RELIANCE.NS", "lot": 500, "name": "RELIANCE", "sector": "ENERGY", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "TCS.NS", "lot": 174, "name": "TCS", "sector": "IT", "tp1": 4, "tp2": 4, "big_lot_qty": 5220, "big_lot_lots": 30},
    {"symbol": "HDFCBANK.NS", "lot": 550, "name": "HDFC BANK", "sector": "BANK", "tp1": 3, "tp2": 3, "big_lot_qty": 7700, "big_lot_lots": 14},
    {"symbol": "INFY.NS", "lot": 400, "name": "INFOSYS", "sector": "IT", "tp1": 3, "tp2": 3, "big_lot_qty": 7200, "big_lot_lots": 18},
    {"symbol": "ICICIBANK.NS", "lot": 700, "name": "ICICI BANK", "sector": "BANK", "tp1": 2, "tp2": 2, "big_lot_qty": 11200, "big_lot_lots": 16},
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

MAX_DAILY_LOSS = 100000

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

# ================= Q4 RESULTS DASHBOARD FUNCTION (FIXED) =================
def show_q4_dashboard():
    st.markdown("## 📊 Q4 FY26 RESULTS DASHBOARD")
    
    # Create list for display (rows as list of dicts)
    rows = []
    for company, data in st.session_state.q4_results.items():
        if data["verdict"] == "Positive":
            verdict_display = "🟢 Positive"
        elif data["verdict"] == "Negative":
            verdict_display = "🔴 Negative"
        elif data["verdict"] == "Mixed":
            verdict_display = "🟡 Mixed"
        elif data["verdict"] == "Cautious":
            verdict_display = "🟠 Cautious"
        else:
            verdict_display = "⏳ Pending"
        
        profit_display = f"{data['profit']:+.1f}%" if data['profit'] != 0 else "—"
        revenue_display = f"₹{data['revenue']:,} Cr" if data['revenue'] > 0 else "—"
        
        rows.append({
            "Company": company,
            "Result Date": data["date"],
            "Profit Change": profit_display,
            "Verdict": verdict_display,
            "Revenue": revenue_display,
            "Key Point": data["key"]
        })
    
    # Convert to DataFrame for table display
    df_q4 = pd.DataFrame(rows)
    st.dataframe(df_q4, use_container_width=True, height=400)
    
    # Color coded cards - Iterate through rows list correctly
    st.markdown("### 📈 Company-wise Performance")
    
    for row in rows:  # FIXED: rows list वरून iterate करा
        if "Negative" in row["Verdict"]:
            color = "#ff4444"
            bg = "rgba(255,68,68,0.1)"
            icon = "🔴"
        elif "Mixed" in row["Verdict"] or "Cautious" in row["Verdict"]:
            color = "#ffaa00"
            bg = "rgba(255,170,0,0.1)"
            icon = "🟡"
        elif "Positive" in row["Verdict"]:
            color = "#00ff88"
            bg = "rgba(0,255,136,0.1)"
            icon = "🟢"
        else:
            color = "#888888"
            bg = "rgba(136,136,136,0.1)"
            icon = "⏳"
        
        if "Today" in row["Result Date"] and row["Profit Change"] != "—":
            live_badge = "<span style='background:#00ff88; color:black; padding:2px 8px; border-radius:12px; font-size:12px; margin-left:10px;'>🔴 LIVE UPDATE</span>"
        else:
            live_badge = ""
        
        st.markdown(f"""
        <div style='background:{bg}; padding:15px; border-radius:10px; margin:10px 0; border-left:4px solid {color};'>
            <div style='display:flex; align-items:center;'>
                <b style='color:{color}; font-size:18px;'>{icon} {row['Company']}</b>
                {live_badge}
            </div>
            📅 Date: <b>{row['Result Date']}</b><br>
            📊 Profit Change: <b>{row['Profit Change']}</b> | Verdict: {row['Verdict']}<br>
            💰 Revenue: {row['Revenue']}<br>
            📌 {row['Key Point']}
        </div>
        """, unsafe_allow_html=True)
    
    # Summary Stats
    st.markdown("### 📊 Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(st.session_state.q4_results)
    positive = sum(1 for d in st.session_state.q4_results.values() if d["verdict"] == "Positive")
    negative = sum(1 for d in st.session_state.q4_results.values() if d["verdict"] == "Negative")
    pending = sum(1 for d in st.session_state.q4_results.values() if d["verdict"] == "Pending")
    
    with col1:
        st.metric("Total Companies", total)
    with col2:
        st.metric("🟢 Positive", positive)
    with col3:
        st.metric("🔴 Negative", negative)
    with col4:
        st.metric("⏳ Pending", pending)
    
    st.info("🔄 Manual refresh using button below. Live results will appear when announced.")
    
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

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
    h1 {
        background: linear-gradient(135deg, #ffd89b, #19547b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-align: center;
        font-size: 2.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 8px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00ff88, #00bcd4);
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1>RUDRANSH PRO ALGO X</h1>, unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)

# ================= APP LOCK SCREEN =================
if not st.session_state.app_unlocked:
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>🔐 APPLICATION LOCKED</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Enter 4-6 Digit Numeric Password to Access</p>", unsafe_allow_html=True)
    
    password_input = st.text_input("Password", type="password", placeholder="Enter numeric password", key="app_lock_password", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔓 UNLOCK", use_container_width=True):
            if str(password_input).strip() == str(st.session_state.app_password).strip():
                st.session_state.app_unlocked = True
                st.rerun()
            else:
                st.error("❌ Wrong Password! Access Denied.")
    st.stop()

# ================= TABS =================
tab1, tab2 = st.tabs(["📈 ALGO TRADING", "📊 Q4 RESULTS"])

# ================= TAB 1: ALGO TRADING (Simplified) =================
with tab1:
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
    
    if not st.session_state.algo_running:
        st.warning("⏸️ ALGO IS STOPPED. Press START to begin trading.")
    elif not st.session_state.totp_verified:
        st.warning("🔐 Please enter valid 6-digit TOTP code and press START.")
    else:
        st.success("✅ Algo is running. Check Sidebar for settings and Trading Journal for trades.")

    with st.sidebar:
        st.markdown("## ⚙️ SETTINGS")
        st.markdown("### 📌 ASSETS")
        st.session_state.enable_nifty = st.checkbox("🇮🇳 NIFTY", value=st.session_state.enable_nifty)
        if st.session_state.enable_nifty:
            st.session_state.nifty_lots = st.number_input("NIFTY Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots, step=1)
        
        st.session_state.enable_crude = st.checkbox("🛢️ CRUDE OIL", value=st.session_state.enable_crude)
        if st.session_state.enable_crude:
            st.session_state.crude_lots = st.number_input("CRUDE Lots", min_value=1, max_value=50, value=st.session_state.crude_lots, step=1)
        
        st.session_state.enable_ng = st.checkbox("🌿 NATURAL GAS", value=st.session_state.enable_ng)
        if st.session_state.enable_ng:
            st.session_state.ng_lots = st.number_input("NG Lots", min_value=1, max_value=50, value=st.session_state.ng_lots, step=1)
        
        st.session_state.enable_stocks = st.checkbox("📈 F&O STOCKS", value=st.session_state.enable_stocks)
        
        st.markdown("---")
        st.markdown("### 📊 DAILY STATUS")
        st.metric("NIFTY Trades", f"{st.session_state.nifty_trades_count}/2")
        st.metric("CRUDE Trades", f"{st.session_state.crude_trades_count}/2")
        st.metric("NG Trades", f"{st.session_state.ng_trades_count}/2")

# ================= TAB 2: Q4 RESULTS =================
with tab2:
    show_q4_dashboard()
