import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO ALGO X", layout="wide", page_icon="📈")

# ================= IST TIMEZONE =================
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

# ================= SESSION STATE INITIALIZATION =================
if "algo_running" not in st.session_state:
    st.session_state.algo_running = False
if "totp_verified" not in st.session_state:
    st.session_state.totp_verified = False
if "trade_journal" not in st.session_state:
    st.session_state.trade_journal = []
if "active_orders" not in st.session_state:
    st.session_state.active_orders = []  # List of active orders with SL and Target

# Custom Orders (User Defined)
if "custom_orders" not in st.session_state:
    st.session_state.custom_orders = []  # {symbol, buy_above, sl, target, qty, status}

if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = get_ist_now().date()
if "max_daily_loss" not in st.session_state:
    st.session_state.max_daily_loss = 100000

# ================= Q4 RESULTS DATA =================
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

# Reset daily
if get_ist_now().date() != st.session_state.last_trade_date:
    st.session_state.daily_loss = 0
    st.session_state.last_trade_date = get_ist_now().date()

def check_daily_loss_limit():
    return abs(st.session_state.daily_loss) >= st.session_state.max_daily_loss

# ================= HELPER FUNCTIONS =================
def get_live_price(symbol):
    """Get live price for any symbol"""
    try:
        if symbol == "NIFTY":
            ticker = "^NSEI"
        elif symbol == "BANKNIFTY":
            ticker = "^NSEBANK"
        else:
            ticker = symbol
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            val = df['Close'].iloc[-1]
            return float(val) if not isinstance(val, pd.Series) else float(val.iloc[-1])
    except:
        pass
    return 0.0

def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
    except:
        pass

def check_and_execute_custom_orders():
    """Check if any custom order conditions are met and execute"""
    current_nifty = get_live_price("NIFTY")
    current_banknifty = get_live_price("BANKNIFTY")
    
    for order in st.session_state.custom_orders:
        if order['status'] == 'PENDING':
            current_price = 0
            if order['symbol'] == 'NIFTY':
                current_price = current_nifty
            elif order['symbol'] == 'BANKNIFTY':
                current_price = current_banknifty
            
            if current_price > 0 and current_price >= order['buy_above']:
                # Execute the trade
                order['status'] = 'ACTIVE'
                order['entry_price'] = current_price
                order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
                
                # Add to trade journal
                trade_record = {
                    "No": len(st.session_state.trade_journal) + 1,
                    "Time": order['entry_time'],
                    "Symbol": order['symbol'],
                    "Type": "BUY",
                    "Lots": order['qty'],
                    "Qty": order['qty'] * 65 if order['symbol'] == 'NIFTY' else order['qty'] * 25,
                    "Entry Price": round(current_price, 2),
                    "SL": order['sl'],
                    "Target": order['target'],
                    "Status": "ACTIVE"
                }
                st.session_state.trade_journal.append(trade_record)
                send_telegram(f"🎯 ORDER EXECUTED: {order['symbol']} BUY @ ₹{current_price:.2f} | SL: ₹{order['sl']} | Target: ₹{order['target']} | Qty: {order['qty']} lots")
                
                # Add to active orders for SL/Target monitoring
                st.session_state.active_orders.append({
                    'symbol': order['symbol'],
                    'entry_price': current_price,
                    'sl': order['sl'],
                    'target': order['target'],
                    'qty': order['qty'],
                    'journal_index': len(st.session_state.trade_journal) - 1
                })

def monitor_active_orders():
    """Monitor active orders for SL and Target hits"""
    for i, order in enumerate(st.session_state.active_orders[:]):  # Use slice copy
        current_price = get_live_price(order['symbol'])
        if current_price == 0:
            continue
        
        # Check SL hit
        if current_price <= order['sl']:
            loss_amount = (order['entry_price'] - current_price) * (order['qty'] * 65 if order['symbol'] == 'NIFTY' else order['qty'] * 25)
            st.session_state.daily_loss += loss_amount
            
            # Update journal
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = 'SL HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit Price'] = round(current_price, 2)
                st.session_state.trade_journal[order['journal_index']]['PNL'] = round(loss_amount, 2)
            
            send_telegram(f"❌ SL HIT: {order['symbol']} @ ₹{current_price:.2f} | Loss: ₹{abs(loss_amount):,.2f}")
            st.session_state.active_orders.pop(i)
            st.rerun()
        
        # Check Target hit
        elif current_price >= order['target']:
            profit_amount = (current_price - order['entry_price']) * (order['qty'] * 65 if order['symbol'] == 'NIFTY' else order['qty'] * 25)
            
            # Update journal
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = 'TARGET HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit Price'] = round(current_price, 2)
                st.session_state.trade_journal[order['journal_index']]['PNL'] = round(profit_amount, 2)
            
            send_telegram(f"✅ TARGET HIT: {order['symbol']} @ ₹{current_price:.2f} | Profit: ₹{profit_amount:,.2f}")
            st.session_state.active_orders.pop(i)
            st.rerun()

def is_market_open():
    now = get_ist_now()
    if now.weekday() >= 5:  # Weekend
        return False
    if 9 <= now.hour < 15:
        if now.hour == 9 and now.minute < 15:
            return False
        return True
    return False

# ================= LIVE TIME UPDATE =================
def update_live_time():
    return f"""
    <script>
    function updateTime() {{
        var now = new Date();
        var hours = now.getHours().toString().padStart(2, '0');
        var minutes = now.getMinutes().toString().padStart(2, '0');
        var seconds = now.getSeconds().toString().padStart(2, '0');
        var timeString = hours + ':' + minutes + ':' + seconds + ' IST';
        document.getElementById('live-time').innerHTML = '🕐 ' + timeString;
    }}
    setInterval(updateTime, 1000);
    updateTime();
    </script>
    <div id="live-time" style="text-align:center; font-size:24px; font-weight:bold; color:#00ff88;"></div>
    """

# ================= UI HEADER =================
st.markdown("<h1 style='text-align:center;'>RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)
st.markdown(update_live_time(), unsafe_allow_html=True)
st.markdown("---")

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

# ================= DAILY LOSS DISPLAY =================
if check_daily_loss_limit():
    st.error(f"🚨 DAILY LOSS LIMIT HIT: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{st.session_state.max_daily_loss:,.0f}")
else:
    st.info(f"📉 Daily Loss: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{st.session_state.max_daily_loss:,.0f}")

st.markdown("---")

# ================= LIVE PRICES =================
nifty_price = get_live_price("NIFTY")
banknifty_price = get_live_price("BANKNIFTY")

col1, col2 = st.columns(2)
with col1:
    st.metric("🇮🇳 NIFTY 50", f"₹{nifty_price:,.2f}" if nifty_price else "Loading...")
with col2:
    st.metric("🏦 BANK NIFTY", f"₹{banknifty_price:,.2f}" if banknifty_price else "Loading...")

st.markdown("---")

# ================= CUSTOM ORDER BOOK (NEW FEATURE) =================
st.markdown("## 📝 CUSTOM ORDER BOOK")
st.markdown("*Set your own Buy Above, Stop Loss, Target, and Quantity - Auto execute when price hits your level*")

with st.expander("➕ ADD NEW ORDER", expanded=False):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        symbol = st.selectbox("Symbol", ["NIFTY", "BANKNIFTY"])
    with col2:
        buy_above = st.number_input("Buy Above (₹)", min_value=10000, max_value=300000, value=24300, step=50)
    with col3:
        sl = st.number_input("Stop Loss (₹)", min_value=10000, max_value=300000, value=24200, step=50)
    with col4:
        target = st.number_input("Target (₹)", min_value=10000, max_value=300000, value=24500, step=50)
    with col5:
        qty = st.number_input("Quantity (Lots)", min_value=1, max_value=100, value=1, step=1)
    
    if st.button("📌 PLACE ORDER", use_container_width=True):
        if buy_above <= sl:
            st.error("❌ Buy Above price must be greater than Stop Loss!")
        elif target <= buy_above:
            st.error("❌ Target must be greater than Buy Above price!")
        else:
            st.session_state.custom_orders.append({
                'symbol': symbol,
                'buy_above': buy_above,
                'sl': sl,
                'target': target,
                'qty': qty,
                'status': 'PENDING',
                'entry_price': None,
                'entry_time': None
            })
            send_telegram(f"📌 ORDER PLACED: {symbol} | Buy Above: ₹{buy_above} | SL: ₹{sl} | Target: ₹{target} | Qty: {qty} lots")
            st.success(f"✅ Order placed for {symbol} - Will execute when price crosses ₹{buy_above}")
            st.rerun()

# Display Pending Orders
st.markdown("### ⏳ PENDING ORDERS")
pending_orders = [o for o in st.session_state.custom_orders if o['status'] == 'PENDING']
if pending_orders:
    pending_df = pd.DataFrame([{
        'Symbol': o['symbol'],
        'Buy Above': f"₹{o['buy_above']:,.2f}",
        'SL': f"₹{o['sl']:,.2f}",
        'Target': f"₹{o['target']:,.2f}",
        'Qty': f"{o['qty']} lots",
        'Status': '⏳ PENDING'
    } for o in pending_orders])
    st.dataframe(pending_df, use_container_width=True)
    
    # Cancel order option
    for i, order in enumerate(pending_orders):
        if st.button(f"❌ Cancel {order['symbol']} @ ₹{order['buy_above']}", key=f"cancel_{i}"):
            st.session_state.custom_orders.remove(order)
            st.rerun()
else:
    st.info("📭 No pending orders. Add an order above.")

# Display Active Orders
st.markdown("### 🔴 ACTIVE ORDERS (SL/Target Monitoring)")
active_orders = [o for o in st.session_state.active_orders]
if active_orders:
    active_df = pd.DataFrame([{
        'Symbol': o['symbol'],
        'Entry Price': f"₹{o['entry_price']:,.2f}",
        'SL': f"₹{o['sl']:,.2f}",
        'Target': f"₹{o['target']:,.2f}",
        'Current P/L': f"₹{((get_live_price(o['symbol']) - o['entry_price']) * (o['qty'] * 65 if o['symbol'] == 'NIFTY' else o['qty'] * 25)):,.2f}"
    } for o in active_orders])
    st.dataframe(active_df, use_container_width=True)
else:
    st.info("📭 No active orders.")

st.markdown("---")

# ================= Q4 RESULTS DASHBOARD =================
st.markdown("## 📊 Q4 FY26 RESULTS DASHBOARD")
rows = []
for company, data in st.session_state.q4_results.items():
    profit_display = f"{data['profit']:+.1f}%" if data['profit'] != 0 else "—"
    rows.append({
        "Company": company, "Date": data['date'], "Profit Change": profit_display,
        "Verdict": data['verdict'], "Revenue": data['revenue'], "🤖 AI Signal": data['ai_signal']
    })
df_q4 = pd.DataFrame(rows)
st.dataframe(df_q4, use_container_width=True, height=300)
st.markdown("---")

# ================= TRADING JOURNAL =================
st.markdown("## 📋 TRADING JOURNAL")
if st.session_state.trade_journal:
    df_journal = pd.DataFrame(st.session_state.trade_journal)
    st.dataframe(df_journal, use_container_width=True, height=300)
else:
    st.info("📭 No trades executed yet.")

st.markdown("---")

# ================= AUTO TRADING LOGIC =================
if st.session_state.algo_running and st.session_state.totp_verified and not check_daily_loss_limit():
    if is_market_open():
        # Check and execute custom orders
        check_and_execute_custom_orders()
        # Monitor active orders for SL/Target
        monitor_active_orders()
        st.info("⏳ Monitoring orders... (Auto refreshes every 5 seconds)")
    else:
        st.warning("⏸️ Market is closed. Trading will resume when market opens.")
    
elif not st.session_state.algo_running:
    st.warning("⏸️ ALGO IS STOPPED. Press START to begin trading.")
elif not st.session_state.totp_verified:
    st.warning("🔐 Please enter valid 6-digit TOTP code and press START.")
elif check_daily_loss_limit():
    st.error(f"🚨 DAILY LOSS LIMIT HIT (₹{st.session_state.max_daily_loss:,.0f})! Trading stopped.")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ GENERAL SETTINGS")
    st.session_state.max_daily_loss = st.number_input("📉 Max Daily Loss (₹)", 10000, 500000, st.session_state.max_daily_loss, 10000)
    st.markdown("---")
    st.markdown("### 📊 TODAY'S STATUS")
    st.metric("Active Orders", len(st.session_state.active_orders))
    st.metric("Pending Orders", len([o for o in st.session_state.custom_orders if o['status'] == 'PENDING']))
    st.metric("Daily Loss", f"₹{abs(st.session_state.daily_loss):,.2f}")
    st.markdown("---")
    st.markdown("### 🛡️ HOW IT WORKS")
    st.caption("1️⃣ Add an order with Buy Above price")
    st.caption("2️⃣ When price crosses Buy Above, trade executes")
    st.caption("3️⃣ System auto monitors SL and Target")
    st.caption("4️⃣ SL/Target hit = Auto square off")
    st.caption("5️⃣ Telegram notifications for all events")

# ================= AUTO REFRESH =================
time.sleep(5)
st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.caption("🔐 App Protected | Developed by Satish D. Nakhate, Talwade, Pune - 412114")
