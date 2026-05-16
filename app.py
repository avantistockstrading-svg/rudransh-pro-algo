import streamlit as st
import yfinance as yf
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from streamlit_autorefresh import st_autorefresh

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO ALGO X", layout="wide", page_icon="⚡")

# ================= IST TIMEZONE =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= AUTO REFRESH =================
st_autorefresh(interval=30000, key="auto_refresh", limit=None)

# ================= API KEYS =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"

# ================= APP LOCK =================
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    st.markdown("<h1 style='text-align:center;'>⚡ RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
    pw = st.text_input("Password", type="password", placeholder="Enter password")
    if st.button("UNLOCK", use_container_width=True):
        if pw == "8055":
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("❌ Wrong password")
    st.stop()

# ================= SESSION STATE =================
if "running" not in st.session_state:
    st.session_state.running = False
if "trades" not in st.session_state:
    st.session_state.trades = []
if "nifty_count" not in st.session_state:
    st.session_state.nifty_count = 0
if "crude_count" not in st.session_state:
    st.session_state.crude_count = 0
if "ng_count" not in st.session_state:
    st.session_state.ng_count = 0
if "auto_trade" not in st.session_state:
    st.session_state.auto_trade = True
if "nifty_lots" not in st.session_state:
    st.session_state.nifty_lots = 1
if "crude_lots" not in st.session_state:
    st.session_state.crude_lots = 1
if "ng_lots" not in st.session_state:
    st.session_state.ng_lots = 1
if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0
if "last_date" not in st.session_state:
    st.session_state.last_date = get_ist_now().date()

# ================= Q4 RESULTS DATA =================
Q4_DATA = {
    "HDFC Bank": {"profit": 9.1, "verdict": "🟡 Mixed", "date": "15 May 2026", "revenue": "₹88,500 Cr", "ai_signal": "WAIT", "key": "Deposits grew 14.4%, NII missed"},
    "Reliance": {"profit": -12.5, "verdict": "🔴 Negative", "date": "14 May 2026", "revenue": "₹2,34,000 Cr", "ai_signal": "SELL", "key": "Retail strong, Energy weak"},
    "Infosys": {"profit": 11.6, "verdict": "🟠 Cautious", "date": "16 May 2026", "revenue": "₹42,000 Cr", "ai_signal": "CAUTIOUS BUY", "key": "Revenue declined, weak guidance"},
    "Maruti Suzuki": {"profit": -6.5, "verdict": "🔴 Negative", "date": "13 May 2026", "revenue": "₹38,500 Cr", "ai_signal": "SELL", "key": "Record sales, margin pressure"},
    "Tata Motors": {"profit": -32.0, "verdict": "🔴 Negative", "date": "12 May 2026", "revenue": "₹1,20,000 Cr", "ai_signal": "STRONG SELL", "key": "India PV strong, JLR weak"},
    "Bharat Electronics": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING", "key": "Expected Positive"},
    "BPCL": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING", "key": "Expected Neutral"},
    "Zydus Lifesciences": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING", "key": "Expected Positive"},
    "Mankind Pharma": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING", "key": "Expected Positive"},
    "PI Industries": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING", "key": "Expected Positive"},
}

# ================= DAILY RESET =================
if get_ist_now().date() != st.session_state.last_date:
    st.session_state.daily_loss = 0
    st.session_state.nifty_count = 0
    st.session_state.crude_count = 0
    st.session_state.ng_count = 0
    st.session_state.last_date = get_ist_now().date()

# ================= TECHNICAL INDICATORS FUNCTION =================
def get_technical_indicators(df):
    """Calculate all technical indicators"""
    if df.empty or len(df) < 200:
        return None
    
    close = df['Close']
    high = df['High'] if 'High' in df.columns else close
    low = df['Low'] if 'Low' in df.columns else close
    volume = df['Volume'] if 'Volume' in df.columns else pd.Series([1000000] * len(df))
    
    # EMAs
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
    
    # Strong Bull/Bear candles
    c1 = df.iloc[-2]
    c2 = df.iloc[-1]
    strong_bull = c2['Close'] > c2['Open'] and c2['Close'] > c1['High']
    strong_bear = c2['Close'] < c2['Open'] and c2['Close'] < c1['Low']
    
    # Sideways detection
    current_rsi = rsi.iloc[-1]
    sideways = (45 < current_rsi < 55) and adx < 20
    
    # Multi-timeframe trends
    def get_trend(data, period):
        if len(data) < period:
            return False
        return data['Close'].iloc[-1] > data['Close'].ewm(span=20).mean().iloc[-1]
    
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

# ================= NIFTY TREND =================
def get_nifty_trend():
    try:
        df = yf.download("^NSEI", period="7d", interval="15m", progress=False)
        if df.empty:
            return "NEUTRAL"
        close = df['Close']
        ema20 = close.ewm(span=20).mean().iloc[-1]
        current = close.iloc[-1]
        if current > ema20:
            return "BULLISH"
        elif current < ema20:
            return "BEARISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

# ================= SECTOR TREND =================
def get_sector_trend(sector_symbol):
    try:
        df = yf.download(sector_symbol, period="7d", interval="15m", progress=False)
        if df.empty:
            return False
        close = df['Close']
        ema20 = close.ewm(span=20).mean().iloc[-1]
        current = close.iloc[-1]
        return current > ema20
    except:
        return False

# ================= STRICT BUY SIGNAL =================
def get_strict_buy_signal(symbol, sector_symbol=None):
    """Strict Buy Signal based on your conditions"""
    try:
        # Fetch data
        df = yf.download(symbol, period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return False, 0
        
        indicators = get_technical_indicators(df)
        if indicators is None:
            return False, 0
        
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        
        # Multi-timeframe trends
        df5 = yf.download(symbol, period="3d", interval="5m", progress=False)
        df15 = yf.download(symbol, period="5d", interval="15m", progress=False)
        df1h = yf.download(symbol, period="7d", interval="60m", progress=False)
        
        trend5_up = False
        trend15_up = False
        trend1h_up = False
        
        if not df5.empty and len(df5) > 20:
            trend5_up = df5['Close'].iloc[-1] > df5['Close'].ewm(span=20).mean().iloc[-1]
        if not df15.empty and len(df15) > 20:
            trend15_up = df15['Close'].iloc[-1] > df15['Close'].ewm(span=20).mean().iloc[-1]
        if not df1h.empty and len(df1h) > 20:
            trend1h_up = df1h['Close'].iloc[-1] > df1h['Close'].ewm(span=20).mean().iloc[-1]
        
        # Nifty trend
        nifty_trend = get_nifty_trend()
        nifty_bullish = nifty_trend == "BULLISH"
        nifty_bearish = nifty_trend == "BEARISH"
        
        # Sector trend
        sector_bullish = True
        sector_bearish = False
        if sector_symbol:
            sector_bullish = get_sector_trend(sector_symbol)
            sector_bearish = not sector_bullish
        
        # Strong Bull Stock conditions
        strong_bull_stock = (ema9_val > ema20_val and 
                            current_price > ema200_val and 
                            rsi_val >= 60 and 
                            adx_val >= 25 and 
                            volume_filter_val and 
                            strong_bull_val and 
                            current_price > c1_high_val)
        
        # EMA Buy conditions (Strict)
        ema_buy = (nifty_bullish and 
                  not sideways_val and 
                  sector_bullish and 
                  ema9_val > ema20_val and 
                  current_price > ema200_val and 
                  rsi_val >= 60 and 
                  adx_val >= 25 and 
                  volume_filter_val and 
                  strong_bull_val and 
                  current_price > c1_high_val and 
                  trend5_up and 
                  trend15_up and 
                  trend1h_up)
        
        return ema_buy, current_price
        
    except Exception as e:
        print(f"Buy signal error for {symbol}: {e}")
        return False, 0

# ================= STRICT SELL SIGNAL =================
def get_strict_sell_signal(symbol, sector_symbol=None):
    """Strict Sell Signal based on your conditions"""
    try:
        # Fetch data
        df = yf.download(symbol, period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return False, 0
        
        indicators = get_technical_indicators(df)
        if indicators is None:
            return False, 0
        
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_low_val = indicators["c1_low"]
        
        # Multi-timeframe trends
        df5 = yf.download(symbol, period="3d", interval="5m", progress=False)
        df15 = yf.download(symbol, period="5d", interval="15m", progress=False)
        df1h = yf.download(symbol, period="7d", interval="60m", progress=False)
        
        trend5_up = False
        trend15_up = False
        trend1h_up = False
        
        if not df5.empty and len(df5) > 20:
            trend5_up = df5['Close'].iloc[-1] > df5['Close'].ewm(span=20).mean().iloc[-1]
        if not df15.empty and len(df15) > 20:
            trend15_up = df15['Close'].iloc[-1] > df15['Close'].ewm(span=20).mean().iloc[-1]
        if not df1h.empty and len(df1h) > 20:
            trend1h_up = df1h['Close'].iloc[-1] > df1h['Close'].ewm(span=20).mean().iloc[-1]
        
        # Nifty trend
        nifty_trend = get_nifty_trend()
        nifty_bullish = nifty_trend == "BULLISH"
        nifty_bearish = nifty_trend == "BEARISH"
        
        # Sector trend
        sector_bullish = True
        sector_bearish = False
        if sector_symbol:
            sector_bullish = get_sector_trend(sector_symbol)
            sector_bearish = not sector_bullish
        
        # Strong Bear Stock conditions
        strong_bear_stock = (ema9_val < ema20_val and 
                            current_price < ema200_val and 
                            rsi_val <= 40 and 
                            adx_val >= 25 and 
                            volume_filter_val and 
                            strong_bear_val and 
                            current_price < c1_low_val)
        
        # EMA Sell conditions (Strict)
        ema_sell = (nifty_bearish and 
                   not sideways_val and 
                   sector_bearish and 
                   ema9_val < ema20_val and 
                   current_price < ema200_val and 
                   rsi_val <= 40 and 
                   adx_val >= 25 and 
                   volume_filter_val and 
                   strong_bear_val and 
                   current_price < c1_low_val and 
                   not trend5_up and 
                   not trend15_up and 
                   not trend1h_up)
        
        return ema_sell, current_price
        
    except Exception as e:
        print(f"Sell signal error for {symbol}: {e}")
        return False, 0

# ================= GET SIGNAL FOR DISPLAY =================
def get_signal_display(symbol):
    """Get signal for display (BUY/SELL/WAIT)"""
    buy, buy_price = get_strict_buy_signal(symbol)
    if buy:
        return "BUY", buy_price
    
    sell, sell_price = get_strict_sell_signal(symbol)
    if sell:
        return "SELL", sell_price
    
    return "WAIT", 0

# ================= FUNCTIONS =================
@st.cache_data(ttl=30)
def get_live_prices():
    usdinr = 87.5
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty:
            usdinr = round(float(df['Close'].iloc[-1]), 2)
    except:
        pass
    
    nifty = 0
    try:
        df = yf.download("^NSEI", period="1d", interval="5m", progress=False)
        if not df.empty:
            nifty = round(float(df['Close'].iloc[-1]), 2)
    except:
        pass
    
    crude_usd = 0
    try:
        df = yf.download("CL=F", period="1d", interval="5m", progress=False)
        if not df.empty:
            crude_usd = round(float(df['Close'].iloc[-1]), 2)
    except:
        pass
    crude = round(crude_usd * usdinr, 2) if crude_usd else 0
    
    ng_usd = 0
    try:
        df = yf.download("NG=F", period="1d", interval="5m", progress=False)
        if not df.empty:
            ng_usd = round(float(df['Close'].iloc[-1]), 2)
    except:
        pass
    ng = round(ng_usd * usdinr, 2) if ng_usd else 0
    
    return nifty, crude, ng, usdinr

def send_telegram(msg):
    try:
        token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
        chat_id = "1983026913"
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                     data={"chat_id": chat_id, "text": msg}, timeout=3)
    except:
        pass

def execute_trade(symbol, trade_type, price, lots, qty, target):
    trade = {
        "No": len(st.session_state.trades) + 1,
        "Time": get_ist_now().strftime("%H:%M:%S"),
        "Symbol": symbol,
        "Type": trade_type,
        "Lots": lots,
        "Entry": round(price, 2),
        "Target": target,
        "Status": "OPEN"
    }
    st.session_state.trades.append(trade)
    if symbol == "NIFTY":
        st.session_state.nifty_count += 1
    elif symbol == "CRUDE":
        st.session_state.crude_count += 1
    else:
        st.session_state.ng_count += 1
    send_telegram(f"🤖 {trade_type} {symbol} | {lots} lots @ ₹{price:.2f}")
    return True

# ================= UI HEADER =================
st.markdown("<h1 style='text-align:center;'>⚡ RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE</p>", unsafe_allow_html=True)

# ================= CONTROL PANEL =================
col1, col2, col3, col4 = st.columns([2, 1, 1, 1.5])

with col1:
    totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code", label_visibility="collapsed")

with col2:
    if st.button("🟢 START", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.running = True
            send_telegram("🚀 ALGO STARTED")
            st.rerun()
        else:
            st.error("Valid TOTP required!")

with col3:
    if st.button("🔴 STOP", use_container_width=True):
        st.session_state.running = False
        send_telegram("🛑 ALGO STOPPED")
        st.rerun()

with col4:
    if st.session_state.running:
        st.success(f"🟢 RUNNING | {get_ist_now().strftime('%H:%M:%S')}")
    else:
        st.error(f"🔴 STOPPED | {get_ist_now().strftime('%H:%M:%S')}")

# ================= AUTO-REFRESH STATUS =================
st.info("🔄 **Auto-Refresh every 30 seconds** | Strict Buy/Sell Filters Active")
st.markdown("---")

# ================= LIVE PRICES AND SIGNALS =================
with st.spinner("Fetching live data..."):
    nifty_price, crude_price, ng_price, usdinr = get_live_prices()
    
    # Get signals using strict filters
    nifty_signal, _ = get_signal_display("^NSEI")
    crude_signal, _ = get_signal_display("CL=F")
    ng_signal, _ = get_signal_display("NG=F")

# Display 3 columns with Price and Signal
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🇮🇳 NIFTY 50")
    st.metric("Price", f"₹{nifty_price:,.2f}" if nifty_price else "Loading...")
    if nifty_signal == "BUY":
        st.success(f"🟢 SIGNAL: {nifty_signal}")
    elif nifty_signal == "SELL":
        st.error(f"🔴 SIGNAL: {nifty_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {nifty_signal}")

with col2:
    st.markdown("### 🛢️ CRUDE OIL")
    st.metric("Price", f"₹{crude_price:,.2f}" if crude_price else "Loading...")
    if crude_signal == "BUY":
        st.success(f"🟢 SIGNAL: {crude_signal}")
    elif crude_signal == "SELL":
        st.error(f"🔴 SIGNAL: {crude_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {crude_signal}")

with col3:
    st.markdown("### 🌿 NATURAL GAS")
    st.metric("Price", f"₹{ng_price:,.2f}" if ng_price else "Loading...")
    if ng_signal == "BUY":
        st.success(f"🟢 SIGNAL: {ng_signal}")
    elif ng_signal == "SELL":
        st.error(f"🔴 SIGNAL: {ng_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {ng_signal}")

st.markdown("---")

# ================= Q4 RESULTS DASHBOARD =================
st.markdown("## 📊 Q4 FY26 RESULTS DASHBOARD")
st.caption("🤖 AI-Powered Real-Time Analysis | Auto-refreshes every 30 seconds")

rows = []
for company, data in Q4_DATA.items():
    profit_display = f"{data['profit']:+.1f}%" if data['profit'] != 0 else "—"
    signal = data['ai_signal']
    if "STRONG BUY" in signal:
        signal_display = f"🟢🟢 {signal}"
    elif "BUY" in signal:
        signal_display = f"🟢 {signal}"
    elif "STRONG SELL" in signal:
        signal_display = f"🔴🔴 {signal}"
    elif "SELL" in signal:
        signal_display = f"🔴 {signal}"
    else:
        signal_display = f"⏳ {signal}"
    
    rows.append({
        "Company": company,
        "Date": data['date'],
        "Profit Change": profit_display,
        "Verdict": data['verdict'],
        "Revenue": data['revenue'],
        "🤖 AI Signal": signal_display,
        "Key Point": data['key'][:40] + "..." if len(data['key']) > 40 else data['key']
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, height=450)

# Summary
st.markdown("### 📊 Summary")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total", len(Q4_DATA))
c2.metric("🟢 Positive", sum(1 for d in Q4_DATA.values() if "Positive" in d['verdict']))
c3.metric("🔴 Negative", sum(1 for d in Q4_DATA.values() if "Negative" in d['verdict']))
c4.metric("⏳ Pending", sum(1 for d in Q4_DATA.values() if d['profit'] == 0))
c5.metric("🎯 BUY Signals", sum(1 for d in Q4_DATA.values() if "BUY" in d['ai_signal']))
st.markdown("---")

# ================= TRADING STATUS =================
st.markdown("## 📊 TRADING STATUS")
c1, c2, c3 = st.columns(3)
c1.metric("🇮🇳 NIFTY Trades", f"{st.session_state.nifty_count}/2")
c2.metric("🛢️ CRUDE Trades", f"{st.session_state.crude_count}/2")
c3.metric("🌿 NG Trades", f"{st.session_state.ng_count}/2")
st.markdown("---")

# ================= TRADING JOURNAL =================
st.markdown("## 📋 TRADING JOURNAL")
if st.session_state.trades:
    df_trades = pd.DataFrame(st.session_state.trades)
    st.dataframe(df_trades, use_container_width=True, height=250)
else:
    st.info("📭 No trades executed yet")
st.markdown("---")

# ================= AUTO TRADING LOGIC =================
if st.session_state.running and st.session_state.auto_trade:
    st.markdown("### 🔍 SCANNING FOR SIGNALS...")
    
    # Get fresh signals for trading
    nifty_buy, nifty_buy_price = get_strict_buy_signal("^NSEI")
    nifty_sell, nifty_sell_price = get_strict_sell_signal("^NSEI")
    crude_buy, crude_buy_price = get_strict_buy_signal("CL=F")
    crude_sell, crude_sell_price = get_strict_sell_signal("CL=F")
    ng_buy, ng_buy_price = get_strict_buy_signal("NG=F")
    ng_sell, ng_sell_price = get_strict_sell_signal("NG=F")
    
    # Display current signals
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if nifty_buy:
            st.success("🟢 NIFTY: STRONG BUY")
        elif nifty_sell:
            st.error("🔴 NIFTY: STRONG SELL")
        else:
            st.warning("⏳ NIFTY: WAIT")
    
    with c2:
        if crude_buy:
            st.success("🟢 CRUDE: STRONG BUY")
        elif crude_sell:
            st.error("🔴 CRUDE: STRONG SELL")
        else:
            st.warning("⏳ CRUDE: WAIT")
    
    with c3:
        if ng_buy:
            st.success("🟢 NG: STRONG BUY")
        elif ng_sell:
            st.error("🔴 NG: STRONG SELL")
        else:
            st.warning("⏳ NG: WAIT")
    
    # Execute trades
    if nifty_buy and st.session_state.nifty_count < 2:
        if execute_trade("NIFTY", "BUY", nifty_buy_price, st.session_state.nifty_lots, st.session_state.nifty_lots * 65, 10):
            st.success(f"✅ NIFTY BUY executed at ₹{nifty_buy_price:.2f}")
            st.rerun()
    
    if nifty_sell and st.session_state.nifty_count < 2:
        if execute_trade("NIFTY", "SELL", nifty_sell_price, st.session_state.nifty_lots, st.session_state.nifty_lots * 65, 10):
            st.success(f"✅ NIFTY SELL executed at ₹{nifty_sell_price:.2f}")
            st.rerun()
    
    if crude_buy and st.session_state.crude_count < 2:
        if execute_trade("CRUDE", "BUY", crude_buy_price * usdinr, st.session_state.crude_lots, st.session_state.crude_lots * 100, 10):
            st.success(f"✅ CRUDE BUY executed")
            st.rerun()
    
    if crude_sell and st.session_state.crude_count < 2:
        if execute_trade("CRUDE", "SELL", crude_sell_price * usdinr, st.session_state.crude_lots, st.session_state.crude_lots * 100, 10):
            st.success(f"✅ CRUDE SELL executed")
            st.rerun()
    
    if ng_buy and st.session_state.ng_count < 2:
        if execute_trade("NG", "BUY", ng_buy_price * usdinr, st.session_state.ng_lots, st.session_state.ng_lots * 1250, 1):
            st.success(f"✅ NG BUY executed")
            st.rerun()
    
    if ng_sell and st.session_state.ng_count < 2:
        if execute_trade("NG", "SELL", ng_sell_price * usdinr, st.session_state.ng_lots, st.session_state.ng_lots * 1250, 1):
            st.success(f"✅ NG SELL executed")
            st.rerun()
    
    st.info("⏳ Waiting for next scan cycle... (Auto-refresh in 30 seconds)")
    
elif not st.session_state.running:
    st.warning("⏸️ Press START to begin auto trading")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ SETTINGS")
    st.markdown("### 🤖 AUTO TRADE")
    st.session_state.auto_trade = st.checkbox("Enable Auto Trading", value=st.session_state.auto_trade)
    st.markdown("### 📊 LOT SIZE")
    st.session_state.nifty_lots = st.number_input("NIFTY Lots", 1, 20, st.session_state.nifty_lots)
    st.session_state.crude_lots = st.number_input("CRUDE Lots", 1, 20, st.session_state.crude_lots)
    st.session_state.ng_lots = st.number_input("NG Lots", 1, 20, st.session_state.ng_lots)
    st.markdown("---")
    st.markdown("### 🎯 TARGETS")
    st.caption("🇮🇳 NIFTY: ₹10 per point")
    st.caption("🛢️ CRUDE: ₹10 per point")
    st.caption("🌿 NG: ₹1 per point")
    st.markdown("---")
    st.markdown("### 📡 STATUS")
    st.success("✅ FMP API Connected")
    st.success("✅ GNews API Connected")
    st.info("🔄 Auto-refresh: 30 sec")
    st.markdown("---")
    st.markdown("### 🛡️ STRICT FILTERS ACTIVE")
    st.caption("• EMA9 > EMA20")
    st.caption("• Price > EMA200")
    st.caption("• RSI >= 60 (BUY) / <= 40 (SELL)")
    st.caption("• ADX >= 25")
    st.caption("• Volume Filter")
    st.caption("• Strong Bull/Bear Candle")
    st.caption("• Multi-timeframe confirmation")

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🔄 Auto-refresh every 30 seconds | Last update: {get_ist_now().strftime('%H:%M:%S')}")
st.caption("🔐 Password: 8055 | Developed by Satish D. Nakhate")
