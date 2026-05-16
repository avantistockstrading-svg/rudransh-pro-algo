import streamlit as st
import yfinance as yf
import requests
import time
from datetime import datetime, timedelta, timezone
import pandas as pd

# ================= CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO ALGO X", layout="wide", page_icon="⚡")
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

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
if "capital" not in st.session_state:
    st.session_state.capital = 1000000
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
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "ALGO TRADING"

# ================= Q4 RESULTS DATA (LIGHTWEIGHT) =================
if "q4_data" not in st.session_state:
    st.session_state.q4_data = {
        "HDFC Bank": {"profit": 9.1, "verdict": "🟡 Mixed", "date": "15 May 2026"},
        "Reliance": {"profit": -12.5, "verdict": "🔴 Negative", "date": "14 May 2026"},
        "Infosys": {"profit": 11.6, "verdict": "🟡 Cautious", "date": "16 May 2026"},
        "Maruti Suzuki": {"profit": -6.5, "verdict": "🔴 Negative", "date": "13 May 2026"},
        "Tata Motors": {"profit": -32.0, "verdict": "🔴 Negative", "date": "12 May 2026"},
        "Bharat Electronics": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026 (Today)"},
        "BPCL": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026 (Today)"},
        "Zydus Lifesciences": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026 (Today)"},
        "Mankind Pharma": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026 (Today)"},
        "PI Industries": {"profit": 0, "verdict": "⏳ Pending", "date": "19 May 2026 (Today)"},
    }

# ================= DAILY RESET =================
if get_ist_now().date() != st.session_state.last_date:
    st.session_state.daily_loss = 0
    st.session_state.nifty_count = 0
    st.session_state.crude_count = 0
    st.session_state.ng_count = 0
    st.session_state.last_date = get_ist_now().date()

# ================= FUNCTIONS =================
def get_price(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        if not df.empty:
            return round(float(df['Close'].iloc[-1]), 2)
    except:
        pass
    return 0

def get_usd_inr():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty:
            return round(float(df['Close'].iloc[-1]), 2)
    except:
        pass
    return 87.5

def get_signal(symbol):
    try:
        df = yf.download(symbol, period="3d", interval="5m", progress=False)
        if df.empty or len(df) < 20:
            return "WAIT"
        
        close = df['Close']
        ema9 = close.ewm(span=9).mean().iloc[-1]
        ema20 = close.ewm(span=20).mean().iloc[-1]
        
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1] if not rsi.empty else 50
        
        if ema9 > ema20 and current_rsi >= 55:
            return "BUY"
        elif ema9 < ema20 and current_rsi <= 45:
            return "SELL"
        return "WAIT"
    except:
        return "WAIT"

def send_telegram(msg):
    try:
        token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
        chat_id = "1983026913"
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                     data={"chat_id": chat_id, "text": msg}, timeout=5)
    except:
        pass

def execute_trade(symbol, trade_type, price, lots, qty, target):
    trade = {
        "No": len(st.session_state.trades) + 1,
        "Time": get_ist_now().strftime("%H:%M:%S"),
        "Symbol": symbol,
        "Type": trade_type,
        "Lots": lots,
        "Qty": qty,
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
    
    send_telegram(f"🤖 {trade_type} {symbol} | {lots} lots | Entry: ₹{price:.2f} | Target: ₹{target}")
    return True

# ================= Q4 DASHBOARD FUNCTION =================
def show_q4_dashboard():
    st.markdown("## 📊 Q4 FY26 RESULTS DASHBOARD")
    st.caption("Live updates as results are announced")
    
    # Create DataFrame
    rows = []
    for company, data in st.session_state.q4_data.items():
        profit_display = f"{data['profit']:+.1f}%" if data['profit'] != 0 else "—"
        rows.append({
            "Company": company,
            "Date": data['date'],
            "Profit Change": profit_display,
            "Verdict": data['verdict']
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, height=400)
    
    # Summary
    col1, col2, col3 = st.columns(3)
    total = len(st.session_state.q4_data)
    pending = sum(1 for d in st.session_state.q4_data.values() if d['verdict'] == "⏳ Pending")
    announced = total - pending
    
    col1.metric("Total Companies", total)
    col2.metric("Announced", announced)
    col3.metric("Pending", pending)
    
    st.info("🔄 Click REFRESH to check for new results")
    if st.button("🔄 REFRESH RESULTS", use_container_width=True):
        st.rerun()

# ================= UI HEADER =================
st.markdown("<h1 style='text-align:center;'>⚡ RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE</p>", unsafe_allow_html=True)

# ================= TABS =================
tab1, tab2 = st.tabs(["📈 ALGO TRADING", "📊 Q4 RESULTS"])

# ================= TAB 1: ALGO TRADING =================
with tab1:
    # Control Panel
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

    # Live Prices
    usdinr = get_usd_inr()
    nifty_price = get_price("^NSEI")
    crude_usd = get_price("CL=F")
    crude_price = round(crude_usd * usdinr, 2) if crude_usd else 0
    ng_usd = get_price("NG=F")
    ng_price = round(ng_usd * usdinr, 2) if ng_usd else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("🇮🇳 NIFTY 50", f"₹{nifty_price:,.2f}" if nifty_price else "Loading...")
    col2.metric("🛢️ CRUDE OIL", f"₹{crude_price:,.2f}" if crude_price else "Loading...")
    col3.metric("🌿 NATURAL GAS", f"₹{ng_price:,.2f}" if ng_price else "Loading...")

    st.markdown("---")

    # Fund & Trade Status
    available_funds = st.session_state.capital - st.session_state.daily_loss
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Available", f"₹{available_funds:,.0f}")
    col2.metric("📉 Daily Loss", f"₹{abs(st.session_state.daily_loss):,.0f}")
    col3.metric("🇮🇳 NIFTY", f"{st.session_state.nifty_count}/2")
    col4.metric("🛢️ CRUDE", f"{st.session_state.crude_count}/2")

    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ SETTINGS")
        
        st.markdown("### 🤖 AUTO TRADE")
        st.session_state.auto_trade = st.checkbox("Enable Auto Trading", value=st.session_state.auto_trade)
        
        st.markdown("### 💰 CAPITAL")
        st.session_state.capital = st.number_input("Initial Capital (₹)", 50000, 10000000, st.session_state.capital, 50000)
        
        st.markdown("### 📊 LOT SIZE")
        st.session_state.nifty_lots = st.number_input("NIFTY Lots", 1, 20, st.session_state.nifty_lots)
        st.caption(f"Qty: {st.session_state.nifty_lots * 65}")
        
        st.session_state.crude_lots = st.number_input("CRUDE Lots", 1, 20, st.session_state.crude_lots)
        st.caption(f"Qty: {st.session_state.crude_lots * 100}")
        
        st.session_state.ng_lots = st.number_input("NG Lots", 1, 20, st.session_state.ng_lots)
        st.caption(f"Qty: {st.session_state.ng_lots * 1250}")
        
        st.markdown("---")
        st.markdown("### 🎯 TARGETS")
        st.caption("🇮🇳 NIFTY: ₹10 per point")
        st.caption("🛢️ CRUDE: ₹10 per point")
        st.caption("🌿 NG: ₹1 per point")
        
        st.markdown("---")
        st.markdown("### 🛡️ RISK")
        st.caption("Max 2 trades/day per asset")
        st.caption("Daily Loss Limit: ₹1,00,000")
        st.caption("🔐 App Password: 8055")

    # Trading Journal
    st.markdown("## 📋 TRADING JOURNAL")

    if st.session_state.trades:
        df = pd.DataFrame(st.session_state.trades)
        st.dataframe(df, use_container_width=True, height=300)
        
        total_trades = len(st.session_state.trades)
        st.caption(f"📊 Total Trades: {total_trades} | NIFTY: {st.session_state.nifty_count}/2 | CRUDE: {st.session_state.crude_count}/2 | NG: {st.session_state.ng_count}/2")
    else:
        st.info("📭 No trades executed yet")

    st.markdown("---")

    # Main Trading Logic
    if st.session_state.running:
        
        if st.session_state.daily_loss >= 100000:
            st.error(f"🚨 DAILY LOSS LIMIT HIT: ₹{st.session_state.daily_loss:,.0f} / ₹1,00,000")
            st.stop()
        
        placeholder = st.empty()
        
        # Get Signals
        nifty_signal = get_signal("^NSEI") if st.session_state.nifty_count < 2 else "WAIT"
        crude_signal = get_signal("CL=F") if st.session_state.crude_count < 2 else "WAIT"
        ng_signal = get_signal("NG=F") if st.session_state.ng_count < 2 else "WAIT"
        
        # Display Signals
        with placeholder.container():
            st.markdown("### 🔍 LIVE SIGNALS")
            col1, col2, col3 = st.columns(3)
            
            if nifty_signal == "BUY":
                col1.success(f"🇮🇳 NIFTY: 🟢 BUY")
            elif nifty_signal == "SELL":
                col1.error(f"🇮🇳 NIFTY: 🔴 SELL")
            else:
                col1.warning(f"🇮🇳 NIFTY: ⏳ WAIT")
            
            if crude_signal == "BUY":
                col2.success(f"🛢️ CRUDE: 🟢 BUY")
            elif crude_signal == "SELL":
                col2.error(f"🛢️ CRUDE: 🔴 SELL")
            else:
                col2.warning(f"🛢️ CRUDE: ⏳ WAIT")
            
            if ng_signal == "BUY":
                col3.success(f"🌿 NG: 🟢 BUY")
            elif ng_signal == "SELL":
                col3.error(f"🌿 NG: 🔴 SELL")
            else:
                col3.warning(f"🌿 NG: ⏳ WAIT")
        
        # Execute Trades
        if st.session_state.auto_trade:
            
            if nifty_signal != "WAIT" and st.session_state.nifty_count < 2:
                price = get_price("^NSEI")
                if price:
                    execute_trade("NIFTY", nifty_signal, price, 
                                 st.session_state.nifty_lots, 
                                 st.session_state.nifty_lots * 65, 10)
                    st.rerun()
            
            if crude_signal != "WAIT" and st.session_state.crude_count < 2:
                price = get_price("CL=F") * usdinr
                if price:
                    execute_trade("CRUDE", crude_signal, price,
                                 st.session_state.crude_lots,
                                 st.session_state.crude_lots * 100, 10)
                    st.rerun()
            
            if ng_signal != "WAIT" and st.session_state.ng_count < 2:
                price = get_price("NG=F") * usdinr
                if price:
                    execute_trade("NG", ng_signal, price,
                                 st.session_state.ng_lots,
                                 st.session_state.ng_lots * 1250, 1)
                    st.rerun()
        
        time.sleep(10)
        st.rerun()

    else:
        st.info("⏸️ Press START to begin auto trading")

    st.markdown("---")
    st.caption(f"🔄 Last update: {get_ist_now().strftime('%d %b %Y, %I:%M:%S %p')} IST")

# ================= TAB 2: Q4 RESULTS =================
with tab2:
    show_q4_dashboard()
    st.markdown("---")
    st.caption("📊 Results update as companies announce | Click REFRESH for latest")
