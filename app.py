import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
import requests

st.set_page_config(page_title="Rudransh Pro-Algo", layout="wide")

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
    st.session_state.last_trade_time = datetime.now() - timedelta(minutes=10)
if "nifty_trades" not in st.session_state:
    st.session_state.nifty_trades = 0
if "crude_trades" not in st.session_state:
    st.session_state.crude_trades = 0
if "ng_trades" not in st.session_state:
    st.session_state.ng_trades = 0
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = datetime.now().date()

# Reset daily trades
if datetime.now().date() != st.session_state.last_trade_date:
    st.session_state.nifty_trades = 0
    st.session_state.crude_trades = 0
    st.session_state.ng_trades = 0
    st.session_state.last_trade_date = datetime.now().date()

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
    
    asset = st.selectbox("Asset", ["NIFTY", "CRUDEOIL", "NATURALGAS"])
    st.session_state.asset = asset
    
    lot_sizes = {"NIFTY": 65, "CRUDEOIL": 100, "NATURALGAS": 1250}
    lots = st.number_input("Lots", min_value=1, max_value=10, value=1)
    st.session_state.quantity = lots * lot_sizes[asset]
    
    st.markdown(f"<p style='text-align:center; color:#00ff88;'>📦 Qty: {st.session_state.quantity}</p>", unsafe_allow_html=True)

# ================= Status =================
col1, col2 = st.columns(2)
with col1:
    if st.session_state.running:
        st.markdown("<div class='status-running'>🟢 RUNNING</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-stopped'>🔴 STOPPED</div>", unsafe_allow_html=True)
with col2:
    color = "pnl-positive" if st.session_state.pnl >= 0 else "pnl-negative"
    st.markdown(f"<div style='text-align:center;'>P&L<br><span class='{color}'>₹{st.session_state.pnl:,.0f}</span></div>", unsafe_allow_html=True)

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

st.markdown(f"<div class='price'>₹{price:,.2f}</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= BUY/SELL Signal Function (5 मिनिटे Timeframe) =================
def calculate_signals():
    symbol = symbols[asset]
    
    # Get NIFTY data for trend filter
    nifty_df = yf.download("^NSEI", period="7d", interval="5m", progress=False)
    nifty_df.columns = [str(c).lower() for c in nifty_df.columns]
    
    # Get stock/commodity data - 5 MINUTE TIMEFRAME
    stock_df = yf.download(symbol, period="7d", interval="5m", progress=False)
    
    if stock_df.empty or len(stock_df) < 30:
        return {"signal": "WAIT", "buy": False, "sell": False, "price": price, "trend": "NEUTRAL", "rsi": 50, "adx": 0}
    
    # Clean column names
    stock_df.columns = [str(c).lower() for c in stock_df.columns]
    if 'close' not in stock_df.columns:
        return {"signal": "WAIT", "buy": False, "sell": False, "price": price, "trend": "NEUTRAL", "rsi": 50, "adx": 0}
    
    # ================= NIFTY Trend =================
    nifty_positive = False
    nifty_negative = False
    
    if not nifty_df.empty and 'close' in nifty_df.columns:
        nifty_ema20 = nifty_df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
        nifty_current = nifty_df['close'].iloc[-1]
        nifty_positive = nifty_current > nifty_ema20
        nifty_negative = nifty_current < nifty_ema20
    
    # ================= Sideways Condition =================
    nifty_high = nifty_df['high'].iloc[-20:].max() if 'high' in nifty_df.columns else 0
    nifty_low = nifty_df['low'].iloc[-20:].min() if 'low' in nifty_df.columns else 0
    nifty_current = nifty_df['close'].iloc[-1] if 'close' in nifty_df.columns else 23500
    nifty_range = (nifty_high - nifty_low) / nifty_current if nifty_current > 0 else 0
    sideways = nifty_range < 0.005
    
    # ================= Stock Calculations =================
    close = stock_df['close']
    
    # Calculate EMAs
    ema9 = close.ewm(span=9, adjust=False).mean()
    ema20 = close.ewm(span=20, adjust=False).mean()
    ema200 = close.ewm(span=200, adjust=False).mean()
    
    # Calculate RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Volume filter
    volume = stock_df['volume'] if 'volume' in stock_df.columns else pd.Series([1000000] * len(stock_df))
    volume_sma = volume.rolling(20).mean()
    volume_filter = volume.iloc[-1] > volume_sma.iloc[-1] if not volume_sma.isna().iloc[-1] else True
    
    # ADX calculation
    high = stock_df['high'] if 'high' in stock_df.columns else close
    low = stock_df['low'] if 'low' in stock_df.columns else close
    
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
    
    # ADX approximation
    plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(14).mean() / atr)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(14).mean().iloc[-1] if len(dx) > 14 else 25
    
    # ================= Strong Bull/Bear Conditions =================
    c1 = stock_df.iloc[-2]
    c2 = stock_df.iloc[-1]
    
    strong_bull = c2['close'] > c2['open'] and c2['close'] > c1['high']
    strong_bear = c2['close'] < c2['open'] and c2['close'] < c1['low']
    
    # Current values
    current_price = close.iloc[-1]
    current_ema20 = ema20.iloc[-1]
    current_rsi = rsi.iloc[-1]
    current_ema200 = ema200.iloc[-1] if not ema200.isna().all() else current_price
    
    # Trends across timeframes (5m, 15m, 1h using 5m data)
    trend5_up = ema9.iloc[-1] > ema20.iloc[-1]
    trend15_up = ema9.iloc[-3] > ema20.iloc[-3] if len(ema9) > 3 else trend5_up
    trend1h_up = ema9.iloc[-12] > ema20.iloc[-12] if len(ema9) > 12 else trend5_up
    
    # ================= Strong Bull/Bear Stock =================
    strong_bull_stock = (
        ema9.iloc[-1] > ema20.iloc[-1] and
        current_price > current_ema200 and
        current_rsi >= 60 and
        adx >= 25 and
        volume_filter and
        strong_bull and
        current_price > c1['high']
    )
    
    strong_bear_stock = (
        ema9.iloc[-1] < ema20.iloc[-1] and
        current_price < current_ema200 and
        current_rsi <= 40 and
        adx >= 25 and
        volume_filter and
        strong_bear and
        current_price < c1['low']
    )
    
    # Sector trend
    sector_bullish = nifty_positive
    sector_bearish = nifty_negative
    
    # ================= FINAL BUY/SELL CONDITIONS =================
    buy_condition = (
        nifty_positive and
        not nifty_negative and
        not sideways and
        sector_bullish and
        strong_bull_stock and
        trend5_up and
        trend15_up and
        trend1h_up and
        current_price > current_ema20
    )
    
    sell_condition = (
        nifty_negative and
        not nifty_positive and
        not sideways and
        sector_bearish and
        strong_bear_stock and
        not trend5_up and
        not trend15_up and
        not trend1h_up and
        current_price < current_ema20
    )
    
    # Cooldown check
    cooldown_ok = (datetime.now() - st.session_state.last_trade_time).seconds > 300
    
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
        "ema20": current_ema20
    }

# ================= Calculate Signals =================
signals = calculate_signals()

# ================= Display Metrics =================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Price", f"₹{signals['price']:,.2f}")
col2.metric("Signal", signals['signal'])
col3.metric("RSI", f"{signals['rsi']:.1f}")
col4.metric("Trend", signals['trend'])

st.markdown("---")

# ================= Control Buttons =================
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 BUY", use_container_width=True):
        st.success(f"BUY {st.session_state.quantity} qty")
        st.session_state.pnl += 500
        send_telegram(f"🔵 MANUAL BUY {st.session_state.asset} | Qty: {st.session_state.quantity}")
with col2:
    if st.button("🔴 SELL", use_container_width=True):
        st.error(f"SELL {st.session_state.quantity} qty")
        st.session_state.pnl -= 500
        send_telegram(f"🔴 MANUAL SELL {st.session_state.asset} | Qty: {st.session_state.quantity}")
with col3:
    if st.button("🔲 SQ OFF", use_container_width=True):
        st.session_state.pnl = 0
        st.warning("Squared off!")
        send_telegram(f"🔲 SQUARE OFF {st.session_state.asset}")

st.markdown("---")

# ================= Auto Trade Execution =================
market_hours = False
now = datetime.now()

if st.session_state.asset == "NIFTY":
    if 9 <= now.hour <= 15:
        market_hours = True
    max_trades = 2
    trades_today = st.session_state.nifty_trades
else:
    if 18 <= now.hour <= 23:
        market_hours = True
    max_trades = 2
    trades_today = st.session_state.crude_trades if st.session_state.asset == "CRUDEOIL" else st.session_state.ng_trades

if st.session_state.running and market_hours and trades_today < max_trades:
    if signals['buy']:
        st.success(f"🚀 BUY SIGNAL at ₹{signals['price']:.2f}")
        send_telegram(f"🔵 AUTO BUY {st.session_state.asset} | Qty: {st.session_state.quantity} | Price: ₹{signals['price']:.2f}")
        
        if st.session_state.asset == "NIFTY":
            st.session_state.nifty_trades += 1
        elif st.session_state.asset == "CRUDEOIL":
            st.session_state.crude_trades += 1
        else:
            st.session_state.ng_trades += 1
        
        st.session_state.last_trade_side = "BUY"
        st.session_state.last_trade_time = datetime.now()
        st.balloons()
    
    elif signals['sell']:
        st.error(f"🔻 SELL SIGNAL at ₹{signals['price']:.2f}")
        send_telegram(f"🔴 AUTO SELL {st.session_state.asset} | Qty: {st.session_state.quantity} | Price: ₹{signals['price']:.2f}")
        
        if st.session_state.asset == "NIFTY":
            st.session_state.nifty_trades += 1
        elif st.session_state.asset == "CRUDEOIL":
            st.session_state.crude_trades += 1
        else:
            st.session_state.ng_trades += 1
        
        st.session_state.last_trade_side = "SELL"
        st.session_state.last_trade_time = datetime.now()

# ================= Status =================
st.markdown("---")
if st.session_state.running and market_hours:
    st.success("🟢 ALGO RUNNING (5 min timeframe)")
elif not market_hours:
    st.info("⏰ Market closed. Algo will run during trading hours.")
else:
    st.warning("🔴 ALGO STOPPED")

# ================= Daily Trades =================
st.markdown("---")
st.markdown("### 📊 Daily Trades")
col1, col2, col3 = st.columns(3)
col1.metric("NIFTY", f"{st.session_state.nifty_trades}/2")
col2.metric("CRUDE", f"{st.session_state.crude_trades}/2")
col3.metric("NG", f"{st.session_state.ng_trades}/2")

# ================= Timeframe Info =================
st.info("⏱️ Signal check every 1 minutes")

# ================= Clock =================
st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')} | Auto Refresh")
time.sleep(1)
st.rerun()
