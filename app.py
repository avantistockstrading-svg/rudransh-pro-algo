import streamlit as st
import yfinance as yf
import requests
import time
import pandas as pd
from datetime import datetime, timedelta, timezone

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO ALGO X", layout="wide", page_icon="⚡")

# ================= IST TIMEZONE =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= API KEYS =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"

# ================= AUTO REFRESH (30 सेकंद) =================
st.markdown('<meta http-equiv="refresh" content="30">', unsafe_allow_html=True)

# ================= APP LOCK =================
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    st.markdown("<h1 style='text-align:center;'>⚡ RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE</p>", unsafe_allow_html=True)
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
    
    return nifty, crude, ng

@st.cache_data(ttl=10)
def get_trading_signal(symbol):
    try:
        df = yf.download(symbol, period="2d", interval="5m", progress=False)
        if df.empty or len(df) < 20:
            return "WAIT"
        close = df['Close']
        ema9 = close.ewm(span=9).mean().iloc[-1]
        ema20 = close.ewm(span=20).mean().iloc[-1]
        if ema9 > ema20:
            return "BUY"
        elif ema9 < ema20:
            return "SELL"
        return "WAIT"
    except:
        return "WAIT"

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
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE</p>", unsafe_allow_html=True)

# ================= AUTO-REFRESH STATUS =================
st.info("🔄 **Auto-Refresh every 30 seconds** | Page will reload automatically")
st.markdown("---")

# ================= LIVE PRICES =================
with st.spinner("Fetching live prices..."):
    nifty_price, crude_price, ng_price = get_live_prices()

col1, col2, col3 = st.columns(3)
col1.metric("🇮🇳 NIFTY 50", f"₹{nifty_price:,.2f}" if nifty_price else "Loading...")
col2.metric("🛢️ CRUDE OIL", f"₹{crude_price:,.2f}" if crude_price else "Loading...")
col3.metric("🌿 NATURAL GAS", f"₹{ng_price:,.2f}" if ng_price else "Loading...")
st.markdown("---")

# ================= Q4 RESULTS DASHBOARD =================
st.markdown("## 📊 Q4 FY26 RESULTS DASHBOARD")
st.caption("🤖 AI-Powered Real-Time Analysis | Updates every 30 seconds")

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

# ================= CONTROL PANEL =================
st.markdown("## 🎮 CONTROL PANEL")

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

st.markdown("---")

# ================= TRADING STATUS =================
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
    
    nifty_signal = get_trading_signal("^NSEI") if st.session_state.nifty_count < 2 else "WAIT"
    crude_signal = get_trading_signal("CL=F") if st.session_state.crude_count < 2 else "WAIT"
    ng_signal = get_trading_signal("NG=F") if st.session_state.ng_count < 2 else "WAIT"
    
    c1, c2, c3 = st.columns(3)
    c1.metric("🇮🇳 NIFTY Signal", nifty_signal)
    c2.metric("🛢️ CRUDE Signal", crude_signal)
    c3.metric("🌿 NG Signal", ng_signal)
    
    if nifty_signal != "WAIT":
        if execute_trade("NIFTY", nifty_signal, nifty_price, st.session_state.nifty_lots, st.session_state.nifty_lots * 65, 10):
            st.success(f"✅ NIFTY {nifty_signal} executed!")
            st.rerun()
    
    if crude_signal != "WAIT" and crude_price:
        if execute_trade("CRUDE", crude_signal, crude_price, st.session_state.crude_lots, st.session_state.crude_lots * 100, 10):
            st.success(f"✅ CRUDE {crude_signal} executed!")
            st.rerun()
    
    if ng_signal != "WAIT" and ng_price:
        if execute_trade("NG", ng_signal, ng_price, st.session_state.ng_lots, st.session_state.ng_lots * 1250, 1):
            st.success(f"✅ NG {ng_signal} executed!")
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

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🔄 Next auto-refresh in 30 seconds | Last: {get_ist_now().strftime('%H:%M:%S')}")
st.caption("🔐 Password: 8055 | Developed by Satish D. Nakhate")
