import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Rudransh Pro-Algo", layout="wide")

# ================= IST Timezone =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= CSS =================
st.markdown("""
<style>
.main { padding: 0rem 0.5rem; }
.stButton button { background: linear-gradient(90deg, #00ff88, #00cc66); color: black; font-weight: bold; border-radius: 30px; padding: 12px; width: 100%; border: none; }
div[data-testid="column"]:nth-child(2) button { background: linear-gradient(90deg, #ff4b4b, #cc0000); color: white; }
.status-running { background: #00ff88; color: black; padding: 8px; border-radius: 30px; text-align: center; font-weight: bold; }
.status-stopped { background: #ff4b4b; color: white; padding: 8px; border-radius: 30px; text-align: center; font-weight: bold; }
.pnl-positive { color: #00ff88; font-size: 24px; font-weight: bold; text-align: center; }
.pnl-negative { color: #ff4b4b; font-size: 24px; font-weight: bold; text-align: center; }
.price { font-size: 32px; font-weight: bold; text-align: center; background: linear-gradient(90deg, #00ff88, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.loss-limit-hit { background: #ff0000; color: white; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ================= Telegram Alert =================
def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
    except:
        pass

# ================= Session State =================
if "running" not in st.session_state:
    st.session_state.running = False
if "pnl" not in st.session_state:
    st.session_state.pnl = 0
if "quantity" not in st.session_state:
    st.session_state.quantity = 65
if "asset" not in st.session_state:
    st.session_state.asset = "NIFTY"
if "last_trade_side" not in st.session_state:
    st.session_state.last_trade_side = ""
if "last_trade_time" not in st.session_state:
    st.session_state.last_trade_time = get_ist_now() - timedelta(minutes=10)
if "nifty_trades" not in st.session_state:
    st.session_state.nifty_trades = 0
if "nifty_buy_done" not in st.session_state:
    st.session_state.nifty_buy_done = False
if "nifty_sell_done" not in st.session_state:
    st.session_state.nifty_sell_done = False
if "crude_trades" not in st.session_state:
    st.session_state.crude_trades = 0
if "crude_buy_done" not in st.session_state:
    st.session_state.crude_buy_done = False
if "crude_sell_done" not in st.session_state:
    st.session_state.crude_sell_done = False
if "ng_trades" not in st.session_state:
    st.session_state.ng_trades = 0
if "ng_buy_done" not in st.session_state:
    st.session_state.ng_buy_done = False
if "ng_sell_done" not in st.session_state:
    st.session_state.ng_sell_done = False
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = get_ist_now().date()
if "signal_mode" not in st.session_state:
    st.session_state.signal_mode = "STRICT"
if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0

# Reset daily trades (IST मध्ये)
if get_ist_now().date() != st.session_state.last_trade_date:
    st.session_state.nifty_trades = 0
    st.session_state.nifty_buy_done = False
    st.session_state.nifty_sell_done = False
    st.session_state.crude_trades = 0
    st.session_state.crude_buy_done = False
    st.session_state.crude_sell_done = False
    st.session_state.ng_trades = 0
    st.session_state.ng_buy_done = False
    st.session_state.ng_sell_done = False
    st.session_state.daily_loss = 0
    st.session_state.pnl = 0
    st.session_state.last_trade_date = get_ist_now().date()

# ================= Settings as per your requirement =================
MAX_DAILY_LOSS = 100000  # ₹1,00,000

# ITM Settings
ITM_SETTINGS = {
    "NIFTY": {"itm_points": 100},
    "CRUDEOIL": {"itm_points": 100},
    "NATURALGAS": {"itm_points": 10}
}

# TP Booking Percentages
TP_BOOKING = {
    "tp1_percent": 50,
    "tp2_percent": 25,
    "tp3_percent": 25
}

# TP/SL Points
TP_SL_POINTS = {
    "NIFTY": {"sl": 20, "tp1": 10, "tp2": 20, "tp3": 30, "lot": 65},
    "CRUDEOIL": {"sl": 30, "tp1": 15, "tp2": 10, "tp3": 20, "lot": 100},
    "NATURALGAS": {"sl": 1.50, "tp1": 1, "tp2": 1.5, "tp3": 2, "lot": 1250}
}

def get_tp_sl(asset):
    return TP_SL_POINTS.get(asset, TP_SL_POINTS["NIFTY"])

def get_itm_strike(price, asset):
    """Calculate ITM strike price for options"""
    itm_points = ITM_SETTINGS[asset]["itm_points"]
    if asset == "NATURALGAS":
        return round(price - itm_points, 1)
    else:
        return int(price - itm_points)

# ================= Title =================
st.markdown("<h1>📱 RUDRANSH PRO-ALGO</h1>", unsafe_allow_html=True)
st.markdown("---")

# ================= Sidebar =================
with st.sidebar:
    st.markdown("## 🎮 CONTROLS")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START", use_container_width=True):
            st.session_state.running = True
            send_telegram("🤖 ALGO STARTED")
    with col2:
        if st.button("⏹️ STOP", use_container_width=True):
            st.session_state.running = False
            send_telegram("🛑 ALGO STOPPED")
    
    st.markdown("---")
    
    st.markdown("## 🎯 SIGNAL MODE")
    
    signal_mode = st.radio(
        "Select Trading Mode",
        ["🟢 EARLY Mode (Fast Signals)", "🔴 STRICT Mode (Safe Signals)", "🟣 BOTH Mode (Combined)"],
        index=1
    )
    st.session_state.signal_mode = signal_mode
    
    st.markdown("---")
    
    asset = st.selectbox("Asset", ["NIFTY", "CRUDEOIL", "NATURALGAS"])
    st.session_state.asset = asset
    
    tp_sl = get_tp_sl(asset)
    lot_sizes = {"NIFTY": 65, "CRUDEOIL": 100, "NATURALGAS": 1250}
    lots = st.number_input("Lots", min_value=1, max_value=10, value=1)
    st.session_state.quantity = lots * lot_sizes[asset]
    
    st.markdown(f"<p style='text-align:center; color:#00ff88;'>📦 Qty: {st.session_state.quantity}</p>", unsafe_allow_html=True)

# ================= Status =================
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.running:
        st.markdown("<div class='status-running'>🟢 RUNNING</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-stopped'>🔴 STOPPED</div>", unsafe_allow_html=True)
with col2:
    color = "pnl-positive" if st.session_state.pnl >= 0 else "pnl-negative"
    st.markdown(f"<div style='text-align:center;'>P&L<br><span class='{color}'>₹{st.session_state.pnl:,.0f}</span></div>", unsafe_allow_html=True)
with col3:
    loss_color = "red" if st.session_state.daily_loss <= -MAX_DAILY_LOSS else "white"
    st.markdown(f"<div style='text-align:center;'>Daily Loss<br><span style='color:{loss_color}; font-weight:bold;'>₹{abs(st.session_state.daily_loss):,.0f} / ₹{MAX_DAILY_LOSS:,.0f}</span></div>", unsafe_allow_html=True)

# Loss Limit Check
loss_limit_hit = abs(st.session_state.daily_loss) >= MAX_DAILY_LOSS

if loss_limit_hit:
    st.markdown(f"<div class='loss-limit-hit'>⚠️ DAILY LOSS LIMIT HIT (₹{MAX_DAILY_LOSS:,.0f})! TRADING STOPPED FOR TODAY ⚠️</div>", unsafe_allow_html=True)

st.markdown("---")

# ================= Get Live Price =================
symbols = {"NIFTY": "^NSEI", "CRUDEOIL": "CL=F", "NATURALGAS": "NG=F"}
price = 23500.0

try:
    df_price = yf.download(symbols[asset], period="1d", interval="5m", progress=False)
    if not df_price.empty and 'Close' in df_price.columns:
        price = float(df_price['Close'].iloc[-1])
except:
    pass

# ITM Strike Price
itm_strike = get_itm_strike(price, asset)

st.markdown(f"<div class='price'>₹{price:,.2f}</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#ffaa00;'>🎯 ITM Strike: {itm_strike} (ITM: {ITM_SETTINGS[asset]['itm_points']} points)</p>", unsafe_allow_html=True)
st.markdown("---")

# ================= Sector Detection =================
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

# ================= Signal Calculation =================
def calculate_signals():
    symbol = symbols[asset]
    
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
    
    # Strict Strong Bull/Bear Stock
    strong_bull_stock = (current_ema9 > current_ema20 and current_price > current_ema200 and current_rsi >= 60 and adx >= 25 and volume_filter and strong_bull and current_price > c1['high'])
    strong_bear_stock = (current_ema9 < current_ema20 and current_price < current_ema200 and current_rsi <= 40 and adx >= 25 and volume_filter and strong_bear and current_price < c1['low'])
    
    # Early Conditions
    early_buy = (current_ema9 > current_ema20 and current_price > current_ema20 and strong_bull and current_rsi > 55 and nifty_positive)
    early_sell = (current_ema9 < current_ema20 and current_price < current_ema20 and strong_bear and current_rsi < 45 and nifty_negative)
    
    # Strict Conditions
    strict_buy = (nifty_positive and not nifty_negative and not sideways and sector_bullish and strong_bull_stock and trend5_up and trend15_up and trend1h_up and current_price > current_ema20)
    strict_sell = (nifty_negative and not nifty_positive and not sideways and sector_bearish and strong_bear_stock and not trend5_up and not trend15_up and not trend1h_up and current_price < current_ema20)
    
    # Mode based signal
    mode = st.session_state.signal_mode
    
    if "EARLY" in mode and "STRICT" not in mode and "BOTH" not in mode:
        buy_condition = early_buy
        sell_condition = early_sell
    elif "STRICT" in mode and "EARLY" not in mode:
        buy_condition = strict_buy
        sell_condition = strict_sell
    else:
        buy_condition = early_buy or strict_buy
        sell_condition = early_sell or strict_sell
    
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
        "early_buy": early_buy,
        "strict_buy": strict_buy
    }

# ================= Calculate Signals =================
signals = calculate_signals()
tp_sl = get_tp_sl(asset)

# ================= Display Metrics =================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Price", f"₹{signals['price']:,.2f}")
col2.metric("Signal", signals['signal'])
col3.metric("RSI", f"{signals['rsi']:.1f}")
col4.metric("Trend", signals['trend'])

st.markdown("---")
st.markdown("### 🎯 TP/SL & Booking Settings")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Stop Loss", f"{tp_sl['sl']}")
col2.metric("TP1", f"{tp_sl['tp1']} ({TP_BOOKING['tp1_percent']}%)")
col3.metric("TP2", f"{tp_sl['tp2']} ({TP_BOOKING['tp2_percent']}%)")
col4.metric("TP3", f"{tp_sl['tp3']} ({TP_BOOKING['tp3_percent']}%)")
col5.metric("ITM", f"{ITM_SETTINGS[asset]['itm_points']} pts")

st.markdown("---")

# ================= Control Buttons =================
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 BUY", use_container_width=True):
        st.success(f"BUY {st.session_state.quantity} qty")
        st.session_state.pnl += 500
        st.session_state.daily_loss += 500
        send_telegram(f"🔵 MANUAL BUY {st.session_state.asset} | Qty: {st.session_state.quantity}")
with col2:
    if st.button("🔴 SELL", use_container_width=True):
        st.error(f"SELL {st.session_state.quantity} qty")
        st.session_state.pnl -= 500
        st.session_state.daily_loss -= 500
        send_telegram(f"🔴 MANUAL SELL {st.session_state.asset} | Qty: {st.session_state.quantity}")
with col3:
    if st.button("🔲 SQ OFF", use_container_width=True):
        st.session_state.pnl = 0
        st.warning("Squared off!")
        send_telegram(f"🔲 SQUARE OFF {st.session_state.asset}")

st.markdown("---")

# ================= Trading Hours Check =================
market_hours = False
now = get_ist_now()

if st.session_state.asset == "NIFTY":
    # NIFTY: 9:30 AM to 2:30 PM IST
    if 9 <= now.hour <= 14:
        market_hours = True
    max_trades = 2
    buy_done = st.session_state.nifty_buy_done
    sell_done = st.session_state.nifty_sell_done
    trades_today = st.session_state.nifty_trades
else:
    # CRUDE/NG: 6:00 PM to 10:30 PM IST
    if 18 <= now.hour <= 22:
        market_hours = True
    max_trades = 2
    buy_done = st.session_state.crude_buy_done if st.session_state.asset == "CRUDEOIL" else st.session_state.ng_buy_done
    sell_done = st.session_state.crude_sell_done if st.session_state.asset == "CRUDEOIL" else st.session_state.ng_sell_done
    trades_today = st.session_state.crude_trades if st.session_state.asset == "CRUDEOIL" else st.session_state.ng_trades

# ================= Auto Trade Execution =================
if st.session_state.running and market_hours and not loss_limit_hit and trades_today < max_trades:
    
    # BUY Signal - only if buy not done yet
    if signals['buy'] and not buy_done and st.session_state.last_trade_side != "BUY":
        st.success(f"🚀 BUY SIGNAL at ₹{signals['price']:.2f}")
        send_telegram(f"🔵 AUTO BUY {st.session_state.asset} | Qty: {st.session_state.quantity} | Price: ₹{signals['price']:.2f} | ITM Strike: {itm_strike}")
        
        if st.session_state.asset == "NIFTY":
            st.session_state.nifty_trades += 1
            st.session_state.nifty_buy_done = True
        elif st.session_state.asset == "CRUDEOIL":
            st.session_state.crude_trades += 1
            st.session_state.crude_buy_done = True
        else:
            st.session_state.ng_trades += 1
            st.session_state.ng_buy_done = True
        
        st.session_state.last_trade_side = "BUY"
        st.session_state.last_trade_time = get_ist_now()
        st.balloons()
    
    # SELL Signal - only if sell not done yet
    elif signals['sell'] and not sell_done and st.session_state.last_trade_side != "SELL":
        st.error(f"🔻 SELL SIGNAL at ₹{signals['price']:.2f}")
        send_telegram(f"🔴 AUTO SELL {st.session_state.asset} | Qty: {st.session_state.quantity} | Price: ₹{signals['price']:.2f} | ITM Strike: {itm_strike}")
        
        if st.session_state.asset == "NIFTY":
            st.session_state.nifty_trades += 1
            st.session_state.nifty_sell_done = True
        elif st.session_state.asset == "CRUDEOIL":
            st.session_state.crude_trades += 1
            st.session_state.crude_sell_done = True
        else:
            st.session_state.ng_trades += 1
            st.session_state.ng_sell_done = True
        
        st.session_state.last_trade_side = "SELL"
        st.session_state.last_trade_time = get_ist_now()

# ================= Status =================
st.markdown("---")
if loss_limit_hit:
    st.error(f"⚠️ DAILY LOSS LIMIT HIT (₹{MAX_DAILY_LOSS:,.0f})! Trading stopped for today. ⚠️")
elif st.session_state.running and market_hours:
    st.success(f"🟢 ALGO RUNNING | {st.session_state.signal_mode} | IST: {now.strftime('%H:%M:%S')}")
elif not market_hours:
    if st.session_state.asset == "NIFTY":
        st.info("⏰ NIFTY Market closed (IST: 9:30 AM - 2:30 PM)")
    else:
        st.info("⏰ Commodity Market closed (IST: 6:00 PM - 10:30 PM)")
else:
    st.warning("🔴 ALGO STOPPED")

# ================= Daily Trades Status =================
st.markdown("---")
st.markdown("### 📊 Daily Trades Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**NIFTY**")
    st.markdown(f"- Total Trades: {st.session_state.nifty_trades}/2")
    st.markdown(f"- Buy Done: {'✅' if st.session_state.nifty_buy_done else '❌'}")
    st.markdown(f"- Sell Done: {'✅' if st.session_state.nifty_sell_done else '❌'}")

with col2:
    st.markdown("**CRUDE OIL**")
    st.markdown(f"- Total Trades: {st.session_state.crude_trades}/2")
    st.markdown(f"- Buy Done: {'✅' if st.session_state.crude_buy_done else '❌'}")
    st.markdown(f"- Sell Done: {'✅' if st.session_state.crude_sell_done else '❌'}")

with col3:
    st.markdown("**NATURAL GAS**")
    st.markdown(f"- Total Trades: {st.session_state.ng_trades}/2")
    st.markdown(f"- Buy Done: {'✅' if st.session_state.ng_buy_done else '❌'}")
    st.markdown(f"- Sell Done: {'✅' if st.session_state.ng_sell_done else '❌'}")

# ================= Clock =================
st.markdown("---")
st.caption(f"🕐 IST: {get_ist_now().strftime('%H:%M:%S')} | Auto Refresh every 60 seconds | Max Daily Loss: ₹{MAX_DAILY_LOSS:,.0f}")
st_autorefresh(interval=60000, key="auto_refresh")
