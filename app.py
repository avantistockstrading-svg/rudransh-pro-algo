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

# ================= WOLF ORDER BOOK SESSION STATE =================
if "wolf_orders" not in st.session_state:
    st.session_state.wolf_orders = []
if "active_orders" not in st.session_state:
    st.session_state.active_orders = []

# ================= COMPLETE F&O SCRIPTS LIST =================
FO_SCRIPTS = [
    # NIFTY & BANKNIFTY (Index)
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY",
    
    # TOP BLUECHIP STOCKS
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", 
    "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
    "AXISBANK", "LT", "DMART", "SUNPHARMA", "BAJFINANCE",
    "TITAN", "MARUTI", "TATAMOTORS", "TATASTEEL", "WIPRO",
    "HCLTECH", "ONGC", "NTPC", "POWERGRID", "ULTRACEMCO",
    "ADANIPORTS", "ADANIENT", "ASIANPAINT", "BAJAJFINSV",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY",
    "EICHERMOT", "GRASIM", "HDFC", "HDFCLIFE", "HEROMOTOCO",
    "HINDALCO", "HINDZINC", "IBULHSGFIN", "IOC", "INDUSINDBK",
    "JSWSTEEL", "JUBLFOOD", "M&M", "MCDOWELL-N", "MUTHOOTFIN",
    "NAUKRI", "NESTLEIND", "PIDILITIND", "PEL", "PFC",
    "PNB", "RECLTD", "SAIL", "SHREECEM", "SIEMENS",
    "TATACONSUM", "TATAPOWER", "TECHM", "TORNTPHARM", "UPL",
    "VEDL", "YESBANK", "ZEEL"
]

# ================= LOT SIZE AND TP SETTINGS =================
# NIFTY
if "nifty_lots" not in st.session_state:
    st.session_state.nifty_lots = 1
if "nifty_tp1" not in st.session_state:
    st.session_state.nifty_tp1 = 10
if "nifty_tp2" not in st.session_state:
    st.session_state.nifty_tp2 = 20
if "nifty_tp3" not in st.session_state:
    st.session_state.nifty_tp3 = 30
if "nifty_tp1_enabled" not in st.session_state:
    st.session_state.nifty_tp1_enabled = True
if "nifty_tp2_enabled" not in st.session_state:
    st.session_state.nifty_tp2_enabled = True
if "nifty_tp3_enabled" not in st.session_state:
    st.session_state.nifty_tp3_enabled = False

# CRUDE
if "crude_lots" not in st.session_state:
    st.session_state.crude_lots = 1
if "crude_tp1" not in st.session_state:
    st.session_state.crude_tp1 = 10
if "crude_tp2" not in st.session_state:
    st.session_state.crude_tp2 = 20
if "crude_tp3" not in st.session_state:
    st.session_state.crude_tp3 = 30
if "crude_tp1_enabled" not in st.session_state:
    st.session_state.crude_tp1_enabled = True
if "crude_tp2_enabled" not in st.session_state:
    st.session_state.crude_tp2_enabled = True
if "crude_tp3_enabled" not in st.session_state:
    st.session_state.crude_tp3_enabled = False

# NG
if "ng_lots" not in st.session_state:
    st.session_state.ng_lots = 1
if "ng_tp1" not in st.session_state:
    st.session_state.ng_tp1 = 1
if "ng_tp2" not in st.session_state:
    st.session_state.ng_tp2 = 2
if "ng_tp3" not in st.session_state:
    st.session_state.ng_tp3 = 3
if "ng_tp1_enabled" not in st.session_state:
    st.session_state.ng_tp1_enabled = True
if "ng_tp2_enabled" not in st.session_state:
    st.session_state.ng_tp2_enabled = True
if "ng_tp3_enabled" not in st.session_state:
    st.session_state.ng_tp3_enabled = False

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

# Reset daily trades
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
        if symbol == "NIFTY":
            ticker = "^NSEI"
        elif symbol == "BANKNIFTY":
            ticker = "^NSEBANK"
        elif symbol == "FINNIFTY":
            ticker = "^NIFTY_FIN_SERVICE"
        elif symbol == "MIDCPNIFTY":
            ticker = "^NSE_MIDCAP_100"
        elif symbol == "CRUDE":
            ticker = "CL=F"
        elif symbol == "NG":
            ticker = "NG=F"
        else:
            ticker = f"{symbol}.NS"
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

# ================= WOLF ORDER FUNCTIONS =================
def check_and_execute_wolf_orders():
    """Check if any wolf order conditions are met and execute"""
    for order in st.session_state.wolf_orders[:]:
        if order['status'] == 'PENDING':
            current_price = get_live_price(order['symbol'])
            
            if current_price > 0 and current_price >= order['buy_above']:
                order['status'] = 'ACTIVE'
                order['entry_price'] = current_price
                order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
                
                qty_multiplier = 65 if order['symbol'] in ['NIFTY', 'FINNIFTY', 'MIDCPNIFTY'] else 25
                
                trade_record = {
                    "No": len(st.session_state.trade_journal) + 1,
                    "Time": order['entry_time'],
                    "Symbol": f"{order['symbol']} {order['strike_price']}",
                    "Type": "WOLF BUY",
                    "Lots": order['qty'],
                    "Qty": order['qty'] * qty_multiplier,
                    "Entry Price": round(current_price, 2),
                    "SL": order['sl'],
                    "Target": order['target'],
                    "Status": "ACTIVE"
                }
                st.session_state.trade_journal.append(trade_record)
                send_telegram(f"🐺 WOLF ORDER: {order['symbol']} {order['strike_price']} BUY @ ₹{current_price:.2f} | SL: ₹{order['sl']} | Target: ₹{order['target']}")
                
                st.session_state.active_orders.append({
                    'symbol': order['symbol'],
                    'strike_price': order['strike_price'],
                    'entry_price': current_price,
                    'sl': order['sl'],
                    'target': order['target'],
                    'qty': order['qty'],
                    'journal_index': len(st.session_state.trade_journal) - 1
                })

def monitor_active_orders():
    """Monitor active orders for SL and Target hits"""
    for i, order in enumerate(st.session_state.active_orders[:]):
        current_price = get_live_price(order['symbol'])
        if current_price == 0:
            continue
        
        qty_multiplier = 65 if order['symbol'] in ['NIFTY', 'FINNIFTY', 'MIDCPNIFTY'] else 25
        
        if current_price <= order['sl']:
            loss_amount = (order['entry_price'] - current_price) * (order['qty'] * qty_multiplier)
            st.session_state.daily_loss += loss_amount
            
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = 'SL HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit Price'] = round(current_price, 2)
                st.session_state.trade_journal[order['journal_index']]['PNL'] = round(loss_amount, 2)
            
            send_telegram(f"❌ SL HIT: {order['symbol']} {order.get('strike_price', '')} @ ₹{current_price:.2f} | Loss: ₹{abs(loss_amount):,.2f}")
            st.session_state.active_orders.pop(i)
            st.rerun()
        
        elif current_price >= order['target']:
            profit_amount = (current_price - order['entry_price']) * (order['qty'] * qty_multiplier)
            
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = 'TARGET HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit Price'] = round(current_price, 2)
                st.session_state.trade_journal[order['journal_index']]['PNL'] = round(profit_amount, 2)
            
            send_telegram(f"✅ TARGET HIT: {order['symbol']} {order.get('strike_price', '')} @ ₹{current_price:.2f} | Profit: ₹{profit_amount:,.2f}")
            st.session_state.active_orders.pop(i)
            st.rerun()

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

# ================= DAILY LOSS =================
if check_daily_loss_limit():
    st.error(f"🚨 DAILY LOSS LIMIT HIT: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{st.session_state.max_daily_loss:,.0f}")
else:
    st.info(f"📉 Daily Loss: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{st.session_state.max_daily_loss:,.0f}")

st.markdown("---")

# ================= LIVE PRICES =================
usd_inr = get_usd_inr_rate()
nifty_price = get_live_price("NIFTY")
crude_price_usd = get_live_price("CRUDE")
crude_price_inr = crude_price_usd * usd_inr if crude_price_usd else 0
ng_price_usd = get_live_price("NG")
ng_price_inr = ng_price_usd * usd_inr if ng_price_usd else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🇮🇳 NIFTY 50", f"₹{nifty_price:,.2f}" if nifty_price else "Loading...")
with col2:
    st.metric("🛢️ CRUDE OIL", f"₹{crude_price_inr:,.2f}" if crude_price_inr else "Loading...")
with col3:
    st.metric("🌿 NATURAL GAS", f"₹{ng_price_inr:,.2f}" if ng_price_inr else "Loading...")

st.markdown("---")

# ================= WOLF ORDER BOOK (F&O) =================
st.markdown("## 🐺 WOLF ORDER BOOK (F&O)")
st.markdown("*Set Strike Price, Buy Above, Stop Loss, Target, Quantity - Auto execute when price hits your level*")

with st.expander("➕ ADD WOLF ORDER", expanded=False):
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        wolf_symbol = st.selectbox("Symbol", FO_SCRIPTS, key="wolf_symbol")
    with col2:
        strike_price = st.number_input("Strike Price (₹)", min_value=1, max_value=500000, value=24300, step=50, key="strike_price")
    with col3:
        wolf_qty = st.number_input("Quantity (Lots)", min_value=1, max_value=100, value=1, step=1, key="wolf_qty")
    with col4:
        wolf_buy_above = st.number_input("Buy Above (₹)", min_value=1, max_value=500000, value=100, step=10, key="wolf_buy_above")
    with col5:
        wolf_sl = st.number_input("Stop Loss (₹)", min_value=1, max_value=500000, value=80, step=10, key="wolf_sl")
    with col6:
        wolf_target = st.number_input("Target (₹)", min_value=1, max_value=500000, value=150, step=10, key="wolf_target")
    
    if st.button("🐺 PLACE WOLF ORDER", use_container_width=True):
        if wolf_buy_above <= wolf_sl:
            st.error("❌ Buy Above must be greater than Stop Loss!")
        elif wolf_target <= wolf_buy_above:
            st.error("❌ Target must be greater than Buy Above!")
        else:
            st.session_state.wolf_orders.append({
                'symbol': wolf_symbol,
                'strike_price': strike_price,
                'qty': wolf_qty,
                'buy_above': wolf_buy_above,
                'sl': wolf_sl,
                'target': wolf_target,
                'status': 'PENDING',
                'entry_price': None,
                'entry_time': None
            })
            send_telegram(f"🐺 WOLF ORDER PLACED: {wolf_symbol} {strike_price} | Buy: ₹{wolf_buy_above} | SL: ₹{wolf_sl} | Target: ₹{wolf_target} | Qty: {wolf_qty} lots")
            st.success(f"✅ Wolf Order placed for {wolf_symbol} {strike_price}")
            st.rerun()

# Display Pending Wolf Orders
st.markdown("### ⏳ PENDING WOLF ORDERS")
pending_orders = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
if pending_orders:
    pending_df = pd.DataFrame([{
        'Symbol': o['symbol'], 'Strike': f"₹{o['strike_price']:,.0f}", 'Qty': f"{o['qty']} lots",
        'Buy Above': f"₹{o['buy_above']:,.2f}", 'SL': f"₹{o['sl']:,.2f}", 'Target': f"₹{o['target']:,.2f}", 
        'Status': '⏳ PENDING'
    } for o in pending_orders])
    st.dataframe(pending_df, use_container_width=True)
    
    for idx, order in enumerate(pending_orders):
        if st.button(f"❌ Cancel {order['symbol']} {order['strike_price']}", key=f"cancel_wolf_{idx}"):
            st.session_state.wolf_orders.remove(order)
            st.rerun()
else:
    st.info("📭 No pending wolf orders")

# Display Active Wolf Orders
st.markdown("### 🔴 ACTIVE WOLF ORDERS (SL/Target Monitoring)")
active_orders_list = [o for o in st.session_state.active_orders]
if active_orders_list:
    active_df_data = []
    for o in active_orders_list:
        current_price = get_live_price(o['symbol'])
        pnl = (current_price - o['entry_price']) * (o['qty'] * (65 if o['symbol'] in ['NIFTY', 'FINNIFTY', 'MIDCPNIFTY'] else 25))
        active_df_data.append({
            'Symbol': o['symbol'], 'Strike': f"₹{o.get('strike_price', 0):,.0f}", 'Entry': f"₹{o['entry_price']:,.2f}",
            'SL': f"₹{o['sl']:,.2f}", 'Target': f"₹{o['target']:,.2f}", 'Current P/L': f"₹{pnl:,.2f}"
        })
    active_df = pd.DataFrame(active_df_data)
    st.dataframe(active_df, use_container_width=True)
else:
    st.info("📭 No active wolf orders")

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

# ================= LOT SIZE & TP SETTINGS (नवीन व्यवस्था: Lots → TP1 → TP1 ON → TP2 → TP2 ON → TP3 → TP3 ON) =================
with st.expander("⚙️ LOT SIZE & TARGET PROFIT SETTINGS"):
    
    st.markdown("### 🇮🇳 NIFTY SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots, key="nifty_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.nifty_tp1, key="nifty_tp1")
    with col3:
        st.checkbox("TP1 ON", value=st.session_state.nifty_tp1_enabled, key="nifty_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.nifty_tp2, key="nifty_tp2")
    with col5:
        st.checkbox("TP2 ON", value=st.session_state.nifty_tp2_enabled, key="nifty_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.nifty_tp3, key="nifty_tp3")
    with col7:
        st.checkbox("TP3 ON", value=st.session_state.nifty_tp3_enabled, key="nifty_tp3_en")
    
    st.markdown("### 🛢️ CRUDE SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, key="crude_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.crude_tp1, key="crude_tp1")
    with col3:
        st.checkbox("TP1 ON", value=st.session_state.crude_tp1_enabled, key="crude_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.crude_tp2, key="crude_tp2")
    with col5:
        st.checkbox("TP2 ON", value=st.session_state.crude_tp2_enabled, key="crude_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.crude_tp3, key="crude_tp3")
    with col7:
        st.checkbox("TP3 ON", value=st.session_state.crude_tp3_enabled, key="crude_tp3_en")
    
    st.markdown("### 🌿 NATURAL GAS SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, key="ng_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=50, value=st.session_state.ng_tp1, key="ng_tp1")
    with col3:
        st.checkbox("TP1 ON", value=st.session_state.ng_tp1_enabled, key="ng_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=50, value=st.session_state.ng_tp2, key="ng_tp2")
    with col5:
        st.checkbox("TP2 ON", value=st.session_state.ng_tp2_enabled, key="ng_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=50, value=st.session_state.ng_tp3, key="ng_tp3")
    with col7:
        st.checkbox("TP3 ON", value=st.session_state.ng_tp3_enabled, key="ng_tp3_en")

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
    check_and_execute_wolf_orders()
    monitor_active_orders()
    st.info("🐺 Wolf is watching the market...")
elif not st.session_state.algo_running:
    st.warning("⏸️ ALGO IS STOPPED. Press START to begin.")
elif not st.session_state.totp_verified:
    st.warning("🔐 Please enter valid 6-digit TOTP code.")
elif check_daily_loss_limit():
    st.error(f"🚨 DAILY LOSS LIMIT HIT! Trading stopped.")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ GENERAL SETTINGS")
    st.session_state.max_daily_loss = st.number_input("📉 Max Daily Loss (₹)", 10000, 500000, st.session_state.max_daily_loss, 10000)
    st.markdown("---")
    st.markdown("### 📌 ASSETS")
    st.session_state.enable_nifty = st.checkbox("🇮🇳 NIFTY", st.session_state.enable_nifty)
    st.session_state.enable_crude = st.checkbox("🛢️ CRUDE", st.session_state.enable_crude)
    st.session_state.enable_ng = st.checkbox("🌿 NATURAL GAS", st.session_state.enable_ng)
    st.markdown("---")
    st.markdown("### 📊 TODAY'S STATUS")
    st.metric("Active Orders", len(st.session_state.active_orders))
    st.metric("Wolf Orders", len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']))
    st.metric("Daily Loss", f"₹{abs(st.session_state.daily_loss):,.2f}")
    st.markdown("---")
    st.markdown("### 🐺 WOLF ORDER FORM")
    st.caption("Symbol → Strike → Qty → Buy Above → SL → Target")

# ================= AUTO REFRESH =================
time.sleep(5)
st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.caption("🔐 App Protected | Developed by Satish D. Nakhate, Talwade, Pune - 412114")
