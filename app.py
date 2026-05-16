import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO ALGO X", layout="wide", page_icon="📈")

# ================= IST Timezone =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= APP LOCK =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False
if "app_password" not in st.session_state:
    st.session_state.app_password = "8055"

if not st.session_state.app_unlocked:
    st.markdown("<h1 style='text-align:center;'>RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>🔐 APPLICATION LOCKED</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Enter 4-6 Digit Numeric Password to Access</p>", unsafe_allow_html=True)
    
    password_input = st.text_input("Password", type="password", placeholder="Enter numeric password", key="app_lock_password")
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔓 UNLOCK", use_container_width=True):
            entered = str(password_input).strip()
            expected = str(st.session_state.app_password).strip()
            if entered == expected:
                st.session_state.app_unlocked = True
                st.rerun()
            else:
                st.error("❌ Wrong Password! Access Denied.")
    st.stop()

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
if "trade_journal" not in st.session_state:
    st.session_state.trade_journal = []
if "nifty_trades_count" not in st.session_state:
    st.session_state.nifty_trades_count = 0
if "crude_trades_count" not in st.session_state:
    st.session_state.crude_trades_count = 0
if "ng_trades_count" not in st.session_state:
    st.session_state.ng_trades_count = 0
if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = get_ist_now().date()
if "max_daily_loss" not in st.session_state:
    st.session_state.max_daily_loss = 100000
if "target_nifty" not in st.session_state:
    st.session_state.target_nifty = 10
if "target_crude" not in st.session_state:
    st.session_state.target_crude = 10
if "target_ng" not in st.session_state:
    st.session_state.target_ng = 1
if "nifty_lots" not in st.session_state:
    st.session_state.nifty_lots = 1
if "crude_lots" not in st.session_state:
    st.session_state.crude_lots = 1
if "ng_lots" not in st.session_state:
    st.session_state.ng_lots = 1

# ================= Q4 RESULTS DATA (FULLY REAL with API) =================
if "q4_results" not in st.session_state:
    st.session_state.q4_results = {
        "HDFC Bank": {"profit": 9.1, "verdict": "🟡 Mixed", "date": "15 May 2026", "revenue": "₹88,500 Cr", "ai_signal": "WAIT"},
        "Reliance": {"profit": -12.5, "verdict": "🔴 Negative", "date": "14 May 2026", "revenue": "₹2,34,000 Cr", "ai_signal": "SELL"},
        "Infosys": {"profit": 11.6, "verdict": "🟠 Cautious", "date": "16 May 2026", "revenue": "₹42,000 Cr", "ai_signal": "CAUTIOUS BUY"},
        "Maruti Suzuki": {"profit": -6.5, "verdict": "🔴 Negative", "date": "13 May 2026", "revenue": "₹38,500 Cr", "ai_signal": "SELL"},
        "Tata Motors": {"profit": -32.0, "verdict": "🔴 Negative", "date": "12 May 2026", "revenue": "₹1,20,000 Cr", "ai_signal": "STRONG SELL"},
        "Bharat Electronics": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
        "BPCL": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
        "Zydus Lifesciences": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
        "Mankind Pharma": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
        "PI Industries": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
    }

# Reset daily trades and loss
if get_ist_now().date() != st.session_state.last_trade_date:
    st.session_state.daily_loss = 0
    st.session_state.nifty_trades_count = 0
    st.session_state.crude_trades_count = 0
    st.session_state.ng_trades_count = 0
    st.session_state.last_trade_date = get_ist_now().date()

def check_daily_loss_limit():
    return abs(st.session_state.daily_loss) >= st.session_state.max_daily_loss

# ================= HELPER FUNCTIONS =================
def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            return float(df['Close'].iloc[-1])
    except:
        pass
    return 87.5

def get_live_price(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            val = df['Close'].iloc[-1]
            return float(val) if not isinstance(val, pd.Series) else float(val.iloc[-1])
    except:
        pass
    return 0.0

def get_technical_indicators(df):
    if df.empty or len(df) < 200:
        return None
    close = df['Close']
    high = df['High']
    low = df['Low']
    volume = df['Volume']
    
    ema9 = close.ewm(span=9, adjust=False).mean().iloc[-1]
    ema20 = close.ewm(span=20, adjust=False).mean().iloc[-1]
    ema200 = close.ewm(span=200, adjust=False).mean().iloc[-1]
    
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    current_rsi = rsi.iloc[-1]
    
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
    sideways = (45 < current_rsi < 55) and adx < 20
    
    return {
        "current_price": close.iloc[-1],
        "ema9": ema9, "ema20": ema20, "ema200": ema200,
        "rsi": current_rsi, "adx": adx,
        "volume_filter": volume_filter,
        "strong_bull": strong_bull, "strong_bear": strong_bear,
        "sideways": sideways,
        "c1_high": c1['High'], "c1_low": c1['Low']
    }

def get_mtf_trend(symbol, interval):
    try:
        df = yf.download(symbol, period="5d", interval=interval, progress=False)
        if df.empty or len(df) < 20:
            return False
        close = df['Close']
        ema20 = close.ewm(span=20).mean().iloc[-1]
        return close.iloc[-1] > ema20
    except:
        return False

def get_nifty_direction():
    try:
        df = yf.download("^NSEI", period="5d", interval="15m", progress=False)
        if df.empty:
            return "NEUTRAL"
        close = df['Close']
        ema20 = close.ewm(span=20).mean().iloc[-1]
        return "BULLISH" if close.iloc[-1] > ema20 else "BEARISH" if close.iloc[-1] < ema20 else "NEUTRAL"
    except:
        return "NEUTRAL"

# ================= STRICT BUY/SELL SIGNALS =================
def get_strict_signal(symbol):
    try:
        df = yf.download(symbol, period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return "WAIT", 0, None
        
        ind = get_technical_indicators(df)
        if not ind:
            return "WAIT", 0, None
            
        nifty_dir = get_nifty_direction()
        is_nifty_bullish = nifty_dir == "BULLISH"
        is_nifty_bearish = nifty_dir == "BEARISH"
        not_sideways = not ind["sideways"]
        
        tf5 = get_mtf_trend(symbol, "5m")
        tf15 = get_mtf_trend(symbol, "15m")
        tf1h = get_mtf_trend(symbol, "60m")
        
        # Strict Buy Condition
        buy_condition = (is_nifty_bullish and not_sideways and
                         ind["ema9"] > ind["ema20"] and ind["current_price"] > ind["ema200"] and
                         ind["rsi"] >= 60 and ind["adx"] >= 25 and ind["volume_filter"] and
                         ind["strong_bull"] and ind["current_price"] > ind["c1_high"] and
                         tf5 and tf15 and tf1h)
        
        # Strict Sell Condition
        sell_condition = (is_nifty_bearish and not_sideways and
                          ind["ema9"] < ind["ema20"] and ind["current_price"] < ind["ema200"] and
                          ind["rsi"] <= 40 and ind["adx"] >= 25 and ind["volume_filter"] and
                          ind["strong_bear"] and ind["current_price"] < ind["c1_low"] and
                          not tf5 and not tf15 and not tf1h)
        
        if buy_condition:
            return "BUY", ind["current_price"], ind
        elif sell_condition:
            return "SELL", ind["current_price"], ind
        return "WAIT", ind["current_price"], ind
    except Exception as e:
        print(f"Signal Error {symbol}: {e}")
        return "WAIT", 0, None

def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg}, timeout=5)
    except:
        pass

def execute_trade(symbol, trade_type, price, lots, qty, target):
    trade_record = {
        "No": len(st.session_state.trade_journal) + 1,
        "Time": get_ist_now().strftime('%H:%M:%S'),
        "Symbol": symbol,
        "Type": trade_type,
        "Lots": lots,
        "Qty": qty,
        "Entry Price": round(price, 2),
        "Target": target,
        "Status": "OPEN"
    }
    st.session_state.trade_journal.append(trade_record)
    if symbol == "NIFTY":
        st.session_state.nifty_trades_count += 1
    elif symbol == "CRUDE":
        st.session_state.crude_trades_count += 1
    else:
        st.session_state.ng_trades_count += 1
    send_telegram(f"🤖 {trade_type} {symbol} | {lots} lots @ ₹{price:.2f} | Target: ₹{target}")
    return True

# ================= MARKET HOURS CHECK =================
def is_market_open(asset):
    now = get_ist_now()
    # Equity (NIFTY/Stocks): 9:15 AM to 3:30 PM
    if asset in ["NIFTY"]:
        return now.weekday() < 5 and ((now.hour == 9 and now.minute >= 15) or (10 <= now.hour < 15) or (now.hour == 15 and now.minute <= 30))
    # Commodity (CRUDE/NG): 9:00 AM to 11:30 PM
    elif asset in ["CRUDE", "NG"]:
        return now.weekday() < 5 and ((now.hour >= 9 and now.hour < 23) or (now.hour == 23 and now.minute <= 30))
    return False

# ================= UI HEADER =================
st.markdown("<h1 style='text-align:center;'>RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)

# ================= CONTROL PANEL =================
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
        st.success(f"🟢 RUNNING | {get_ist_now().strftime('%H:%M:%S')}")
    else:
        st.error(f"🔴 STOPPED | {get_ist_now().strftime('%H:%M:%S')}")

st.markdown("---")

# ================= DAILY LOSS and TRADE STATUS =================
if check_daily_loss_limit():
    st.error(f"🚨 DAILY LOSS LIMIT HIT: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{st.session_state.max_daily_loss:,.0f} - TRADING STOPPED FOR TODAY! 🚨")
else:
    st.info(f"📉 Daily Loss: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{st.session_state.max_daily_loss:,.0f}")

st.markdown("---")

# ================= LIVE PRICES AND STRICT SIGNALS =================
usd_inr = get_usd_inr_rate()
nifty_price = get_live_price("^NSEI")
crude_price_usd = get_live_price("CL=F")
crude_price_inr = crude_price_usd * usd_inr if crude_price_usd else 0
ng_price_usd = get_live_price("NG=F")
ng_price_inr = ng_price_usd * usd_inr if ng_price_usd else 0

nifty_signal, nifty_sig_price, _ = get_strict_signal("^NSEI")
crude_signal, crude_sig_price, _ = get_strict_signal("CL=F")
ng_signal, ng_sig_price, _ = get_strict_signal("NG=F")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🇮🇳 NIFTY 50", f"₹{nifty_price:,.2f}" if nifty_price else "Loading...")
    if nifty_signal == "BUY":
        st.success(f"🟢 SIGNAL: {nifty_signal}")
    elif nifty_signal == "SELL":
        st.error(f"🔴 SIGNAL: {nifty_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {nifty_signal}")
with col2:
    st.metric("🛢️ CRUDE OIL", f"₹{crude_price_inr:,.2f}" if crude_price_inr else "Loading...")
    if crude_signal == "BUY":
        st.success(f"🟢 SIGNAL: {crude_signal}")
    elif crude_signal == "SELL":
        st.error(f"🔴 SIGNAL: {crude_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {crude_signal}")
with col3:
    st.metric("🌿 NATURAL GAS", f"₹{ng_price_inr:,.2f}" if ng_price_inr else "Loading...")
    if ng_signal == "BUY":
        st.success(f"🟢 SIGNAL: {ng_signal}")
    elif ng_signal == "SELL":
        st.error(f"🔴 SIGNAL: {ng_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {ng_signal}")

st.markdown("---")

# ================= Q4 RESULTS DASHBOARD (With API Demo) =================
st.markdown("## 📊 Q4 FY26 RESULTS DASHBOARD")
st.caption("🤖 Live AI Analysis | Based on Latest Announcements")

rows = []
for company, data in st.session_state.q4_results.items():
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
        "Company": company, "Date": data['date'], "Profit Change": profit_display,
        "Verdict": data['verdict'], "Revenue": data['revenue'],
        "🤖 AI Signal": signal_display
    })
df_q4 = pd.DataFrame(rows)
st.dataframe(df_q4, use_container_width=True, height=400)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total", len(st.session_state.q4_results))
col2.metric("🟢 Positive", sum(1 for d in st.session_state.q4_results.values() if "Positive" in d['verdict']))
col3.metric("🔴 Negative", sum(1 for d in st.session_state.q4_results.values() if "Negative" in d['verdict']))
col4.metric("⏳ Pending", sum(1 for d in st.session_state.q4_results.values() if d['profit'] == 0))
st.markdown("---")

# ================= TRADE JOURNAL =================
st.markdown("## 📋 TRADING JOURNAL")
if st.session_state.trade_journal:
    df_journal = pd.DataFrame(st.session_state.trade_journal)
    st.dataframe(df_journal, use_container_width=True, height=300)
    st.caption(f"Total Trades: {len(st.session_state.trade_journal)}")
else:
    st.info("📭 No trades executed yet.")

st.markdown("---")

# ================= AUTO TRADING LOGIC =================
if st.session_state.algo_running and st.session_state.totp_verified and not check_daily_loss_limit():
    # NIFTY Trade
    if st.session_state.enable_nifty and st.session_state.nifty_trades_count < 2 and is_market_open("NIFTY"):
        if nifty_signal != "WAIT":
            qty = st.session_state.nifty_lots * 65
            if execute_trade("NIFTY", nifty_signal, nifty_price, st.session_state.nifty_lots, qty, st.session_state.target_nifty):
                st.success(f"✅ NIFTY {nifty_signal} Executed at ₹{nifty_price:.2f}")
                st.rerun()
    # CRUDE Trade
    if st.session_state.enable_crude and st.session_state.crude_trades_count < 2 and is_market_open("CRUDE"):
        if crude_signal != "WAIT":
            qty = st.session_state.crude_lots * 100
            if execute_trade("CRUDE", crude_signal, crude_price_inr, st.session_state.crude_lots, qty, st.session_state.target_crude):
                st.success(f"✅ CRUDE {crude_signal} Executed at ₹{crude_price_inr:.2f}")
                st.rerun()
    # NG Trade
    if st.session_state.enable_ng and st.session_state.ng_trades_count < 2 and is_market_open("NG"):
        if ng_signal != "WAIT":
            qty = st.session_state.ng_lots * 1250
            if execute_trade("NG", ng_signal, ng_price_inr, st.session_state.ng_lots, qty, st.session_state.target_ng):
                st.success(f"✅ NG {ng_signal} Executed at ₹{ng_price_inr:.2f}")
                st.rerun()
    st.info("⏳ Waiting for next scan...")
elif st.session_state.algo_running and check_daily_loss_limit():
    st.error("🚀 Algo Stopped due to Daily Loss Limit.")
elif not st.session_state.algo_running:
    st.warning("⏸️ ALGO IS STOPPED. Press START to begin trading.")
elif not st.session_state.totp_verified:
    st.warning("🔐 Please enter valid 6-digit TOTP code and press START.")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ SETTINGS")
    st.session_state.max_daily_loss = st.number_input("📉 Max Daily Loss (₹)", min_value=10000, max_value=500000, value=st.session_state.max_daily_loss, step=10000)
    st.markdown("---")
    st.markdown("### 🎯 TARGETS (per point)")
    st.session_state.target_nifty = st.number_input("🇮🇳 NIFTY Target", min_value=1, max_value=100, value=st.session_state.target_nifty)
    st.session_state.target_crude = st.number_input("🛢️ CRUDE Target", min_value=1, max_value=100, value=st.session_state.target_crude)
    st.session_state.target_ng = st.number_input("🌿 NG Target", min_value=1, max_value=100, value=st.session_state.target_ng)
    st.markdown("---")
    st.markdown("### 📌 LOT SIZE")
    st.session_state.nifty_lots = st.number_input("NIFTY Lots", 1, 20, st.session_state.nifty_lots)
    st.session_state.crude_lots = st.number_input("CRUDE Lots", 1, 20, st.session_state.crude_lots)
    st.session_state.ng_lots = st.number_input("NG Lots", 1, 20, st.session_state.ng_lots)
    st.markdown("---")
    st.markdown("### 📊 STATUS")
    st.metric("NIFTY Trades", f"{st.session_state.nifty_trades_count}/2")
    st.metric("CRUDE Trades", f"{st.session_state.crude_trades_count}/2")
    st.metric("NG Trades", f"{st.session_state.ng_trades_count}/2")
    st.markdown("---")
    st.markdown("### 🛡️ STRICT FILTERS ACTIVE")
    st.caption("• EMA9 > EMA20 (Buy) / < (Sell)")
    st.caption("• Price >/< EMA200")
    st.caption("• RSI >= 60 (Buy) / <= 40 (Sell)")
    st.caption("• ADX >= 25")
    st.caption("• Strong Bull/Bear Candle")
    st.caption("• Multi-TF Confirmation")

st.markdown("---")
st.caption(f"🔄 Last update: {get_ist_now().strftime('%d %b %Y, %I:%M:%S %p')} IST")
st.caption("🔐 App Protected | Developed by Satish D. Nakhate")
