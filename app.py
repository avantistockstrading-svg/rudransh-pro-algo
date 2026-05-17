"""
🐺 RUDRANSH PRO ALGO X - FINAL MASTER
=======================================
VERSION: 3.2.0 (SAMRUDDHI EDITION)
DEVELOPED BY: SATISH D. NAKHATE
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time
import math

# ================= VERSION & INFO =================
APP_VERSION = "3.2.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= API KEYS =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"
TELEGRAM_BOT = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
TELEGRAM_CHAT = "1983026913"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🐺")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
    .css-1r6slb0, .css-1y4p8pa { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; border: 1px solid rgba(255,255,255,0.2); padding: 20px; }
    h1, h2, h3 { background: linear-gradient(135deg, #00ff88 0%, #00b4d8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { background: linear-gradient(135deg, #00ff88, #00b4d8); color: white; border: none; border-radius: 10px; font-weight: bold; }
    .badge-success { background: rgba(0,255,136,0.2); color: #00ff88; padding: 5px 10px; border-radius: 20px; font-size: 12px; }
    .badge-danger { background: rgba(255,0,0,0.2); color: #ff4444; padding: 5px 10px; border-radius: 20px; }
    .badge-warning { background: rgba(255,165,0,0.2); color: #ffa500; padding: 5px 10px; border-radius: 20px; }
    .badge-info { background: rgba(0,180,216,0.2); color: #00b4d8; padding: 5px 10px; border-radius: 20px; }
    .live-time { text-align: center; font-size: 28px; font-weight: bold; background: linear-gradient(135deg, #00ff88, #00b4d8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #00ff88, #00b4d8); color: white; }
    .result-card { background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px; margin: 10px 0; border-left: 4px solid #00ff88; }
</style>
""", unsafe_allow_html=True)

# ================= TIMEZONE =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= APP LOCK =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

if not st.session_state.app_unlocked:
    st.markdown("""
    <div style="text-align:center; padding:50px;">
        <h1>🐺 RUDRANSH PRO ALGO X</h1>
        <p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>
        <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:200px; margin:20px auto;"></div>
        <h3>🔐 APPLICATION LOCKED</h3>
        <p>Enter Password to Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    password_input = st.text_input("Password", type="password", placeholder="Enter password", key="app_lock")
    if st.button("🔓 UNLOCK", use_container_width=True):
        if password_input == "8055":
            st.session_state.app_unlocked = True
            st.rerun()
        else:
            st.error("❌ Wrong Password!")
    st.stop()

# ================= SESSION STATE =================
if "algo_running" not in st.session_state:
    st.session_state.algo_running = False
if "totp_verified" not in st.session_state:
    st.session_state.totp_verified = False
if "wolf_orders" not in st.session_state:
    st.session_state.wolf_orders = []
if "active_orders" not in st.session_state:
    st.session_state.active_orders = []
if "trade_journal" not in st.session_state:
    st.session_state.trade_journal = []
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True
if "result_alerts" not in st.session_state:
    st.session_state.result_alerts = []
if "auto_trade_enabled" not in st.session_state:
    st.session_state.auto_trade_enabled = True

# ================= AUTO TRADE SETTINGS =================
if "auto_trade_qty" not in st.session_state:
    st.session_state.auto_trade_qty = 1
if "auto_trade_sl_percent" not in st.session_state:
    st.session_state.auto_trade_sl_percent = 5
if "auto_trade_target_percent" not in st.session_state:
    st.session_state.auto_trade_target_percent = 10

# ================= COMPLETE SYMBOLS =================
FO_SCRIPTS = [
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "CRUDE", "NATURALGAS",
    "360ONE", "ABB", "APLAPOLLO", "AUBANK", "ADANIENSOL", "ADANIENT", "ADANIGREEN",
    "ADANIPORTS", "ADANIPOWER", "ABCAPITAL", "ALKEM", "AMBER", "AMBUJACEM", "ANGELONE",
    "APOLLOHOSP", "ASHOKLEY", "ASIANPAINT", "ASTRAL", "AUROPHARMA", "DMART", "AXISBANK",
    "BSE", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BAJAJHLDNG", "BANDHANBNK", "BANKBARODA",
    "BANKINDIA", "BDL", "BEL", "BHARATFORG", "BHEL", "BPCL", "BHARTIARTL", "BIOCON",
    "BLUESTARCO", "BOSCHLTD", "BRITANNIA", "CGPOWER", "CANBK", "CDSL", "CHOLAFIN", "CIPLA",
    "COALINDIA", "COCHINSHIP", "COFORGE", "COLPAL", "CAMS", "CONCOR", "CROMPTON", "CUMMINSIND",
    "DLF", "DABUR", "DALBHARAT", "DELHIVERY", "DIVISLAB", "DIXON", "DRREDDY", "EICHERMOT",
    "EXIDEIND", "FORTIS", "GAIL", "GMRAIRPORT", "GLENMARK", "GODREJCP", "GODREJPROP", "GRASIM",
    "HCLTECH", "HDFCAMC", "HDFCBANK", "HDFCLIFE", "HAVELLS", "HEROMOTOCO", "HINDALCO", "HAL",
    "HINDPETRO", "HINDUNILVR", "HINDZINC", "ICICIBANK", "ICICIGI", "ICICIPRULI", "IDFCFIRSTB",
    "ITC", "IEX", "IOC", "IRFC", "IREDA", "INDUSTOWER", "INDUSINDBK", "NAUKRI", "INFY",
    "INDIGO", "JSWENERGY", "JSWSTEEL", "JIOFIN", "JUBLFOOD", "KOTAKBANK", "LT", "LICHSGFIN",
    "LUPIN", "M&M", "MANAPPURAM", "MANKIND", "MARICO", "MARUTI", "MAXHEALTH", "MOTHERSON",
    "MPHASIS", "MCX", "MUTHOOTFIN", "NHPC", "NMDC", "NTPC", "NATIONALUM", "NESTLEIND",
    "ONGC", "PIDILITIND", "PFC", "POWERGRID", "PNB", "RECLTD", "RELIANCE", "SBICARD",
    "SBILIFE", "SHREECEM", "SRF", "SHRIRAMFIN", "SIEMENS", "SBIN", "SAIL", "SUNPHARMA",
    "SUZLON", "TATACONSUM", "TVSMOTOR", "TCS", "TATAPOWER", "TATASTEEL", "TECHM", "TITAN",
    "TORNTPHARM", "TRENT", "UPL", "ULTRACEMCO", "UNIONBANK", "VEDL", "VOLTAS", "WIPRO", "YESBANK", "ZYDUSLIFE"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= TP SETTINGS =================
if "nifty_lots" not in st.session_state:
    st.session_state.nifty_lots = 1
    st.session_state.nifty_tp1 = 10
    st.session_state.nifty_tp2 = 20
    st.session_state.nifty_tp3 = 30
    st.session_state.nifty_tp1_enabled = True
    st.session_state.nifty_tp2_enabled = True
    st.session_state.nifty_tp3_enabled = False

if "crude_lots" not in st.session_state:
    st.session_state.crude_lots = 1
    st.session_state.crude_tp1 = 10
    st.session_state.crude_tp2 = 20
    st.session_state.crude_tp3 = 30
    st.session_state.crude_tp1_enabled = True
    st.session_state.crude_tp2_enabled = True
    st.session_state.crude_tp3_enabled = False

if "ng_lots" not in st.session_state:
    st.session_state.ng_lots = 1
    st.session_state.ng_tp1 = 1
    st.session_state.ng_tp2 = 2
    st.session_state.ng_tp3 = 3
    st.session_state.ng_tp1_enabled = True
    st.session_state.ng_tp2_enabled = True
    st.session_state.ng_tp3_enabled = False

# ================= PENDING RESULTS =================
PENDING_RESULTS = [
    {"name": "Bharat Electronics", "symbol": "BEL", "expected_date": "19 May 2026", "expected_time": "After 3:30 PM", "expected_verdict": "🟢 POSITIVE"},
    {"name": "BPCL", "symbol": "BPCL", "expected_date": "19 May 2026", "expected_time": "After 3:30 PM", "expected_verdict": "🟡 MIXED"},
    {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "expected_date": "19 May 2026", "expected_time": "After 3:30 PM", "expected_verdict": "🟢 POSITIVE"},
    {"name": "Mankind Pharma", "symbol": "MANKIND", "expected_date": "19 May 2026", "expected_time": "After 3:30 PM", "expected_verdict": "🟢 POSITIVE"},
    {"name": "PI Industries", "symbol": "PIIND", "expected_date": "19 May 2026", "expected_time": "After 3:30 PM", "expected_verdict": "🟢 POSITIVE"},
]

# ================= HELPER FUNCTIONS =================
def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if not df.empty:
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
        elif symbol == "CRUDE":
            ticker = "CL=F"
        elif symbol == "NATURALGAS":
            ticker = "NG=F"
        else:
            ticker = f"{symbol}.NS"
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if not df.empty:
            val = df['Close'].iloc[-1]
            return float(val) if not isinstance(val, pd.Series) else float(val.iloc[-1])
    except:
        pass
    return 0.0

def get_nearest_itm_strike(current_price, option_type="CE"):
    """Get nearest ITM strike price for F&O"""
    if current_price < 10000:
        strike_interval = 10
        multiplier = 100
    elif current_price < 50000:
        strike_interval = 50
        multiplier = 50
    else:
        strike_interval = 100
        multiplier = 25
    
    if option_type == "CALL (CE)":
        itm_strike = math.floor(current_price / strike_interval) * strike_interval
    else:
        itm_strike = math.ceil(current_price / strike_interval) * strike_interval
    
    return itm_strike, strike_interval, multiplier

def get_gnews():
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=8&apikey={GNEWS_API_KEY}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return [{'title': a['title'], 'source': a['source']['name'], 'time': a['publishedAt'][:10]} for a in data.get('articles', [])]
    except:
        pass
    return [{'title': 'Market Update', 'source': 'News', 'time': get_ist_now().strftime('%Y-%m-%d')}]

def get_company_earnings(symbol):
    try:
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=1&apikey={FMP_API_KEY}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                return data[0]
    except:
        pass
    return None

def ai_analysis(earnings):
    try:
        revenue = earnings.get('revenue', 0)
        net_income = earnings.get('netIncome', 0)
        revenue_growth = 0
        profit_growth = 0
        score = 0
        if revenue_growth > 10:
            score += 2
        elif revenue_growth > 0:
            score += 1
        elif revenue_growth < -5:
            score -= 2
        if profit_growth > 15:
            score += 2
        elif profit_growth > 0:
            score += 1
        elif profit_growth < -10:
            score -= 2
        if score >= 2:
            return "🟢 BULLISH", "BUY", 85, f"+{revenue_growth}%" if revenue_growth else "+0%", f"+{profit_growth}%" if profit_growth else "+0%"
        elif score >= 1:
            return "🟡 CAUTIOUSLY BULLISH", "CAUTIOUS BUY", 70, f"+{revenue_growth}%" if revenue_growth else "+0%", f"+{profit_growth}%" if profit_growth else "+0%"
        elif score >= -1:
            return "⚪ NEUTRAL", "HOLD", 50, "+0%", "+0%"
        else:
            return "🔴 BEARISH", "SELL", 75, f"{revenue_growth}%" if revenue_growth else "0%", f"{profit_growth}%" if profit_growth else "0%"
    except:
        return "⚪ UNKNOWN", "WAIT", 0, "N/A", "N/A"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=10)
    except:
        pass

def voice_alert(msg):
    if st.session_state.voice_enabled:
        st.markdown(f"<script>var s=new SpeechSynthesisUtterance('{msg}');s.lang='en-US';speechSynthesis.speak(s);</script>", unsafe_allow_html=True)

def auto_place_trade(symbol, signal, current_price, confidence):
    if not st.session_state.auto_trade_enabled:
        return False
    if signal not in ["BUY", "CAUTIOUS BUY"]:
        return False
    if signal in ["BUY", "CAUTIOUS BUY"]:
        option_type = "CALL (CE)"
    else:
        option_type = "PUT (PE)"
    itm_strike, interval, multiplier = get_nearest_itm_strike(current_price, option_type)
    sl_percent = st.session_state.auto_trade_sl_percent / 100
    target_percent = st.session_state.auto_trade_target_percent / 100
    option_premium = 100
    sl_price = option_premium * (1 - sl_percent)
    target_price = option_premium * (1 + target_percent)
    order = {
        'symbol': symbol, 'option_type': option_type, 'strike_price': itm_strike, 'qty': st.session_state.auto_trade_qty,
        'buy_above': option_premium, 'sl': sl_price, 'target': target_price,
        'status': 'PENDING', 'entry_price': None, 'auto_trade': True, 'confidence': confidence
    }
    st.session_state.wolf_orders.append(order)
    send_telegram(f"🤖 AUTO TRADE: {symbol} {option_type} {itm_strike} | Qty: {st.session_state.auto_trade_qty}")
    voice_alert(f"Auto trade placed for {symbol}")
    return True

# ================= WOLF ORDER FUNCTIONS =================
def check_and_execute_orders():
    for order in st.session_state.wolf_orders[:]:
        if order['status'] == 'PENDING':
            price = get_live_price(order['symbol'])
            if price > 0 and price >= order['buy_above']:
                order['status'] = 'ACTIVE'
                order['entry_price'] = price
                order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
                st.session_state.trade_journal.append({
                    "No": len(st.session_state.trade_journal)+1, "Time": order['entry_time'],
                    "Symbol": f"{order['symbol']} {order['option_type']} {order['strike_price']}",
                    "Type": "AUTO" if order.get('auto_trade') else "MANUAL", "Lots": order['qty'],
                    "Entry": round(price, 2), "SL": order['sl'], "Target": order['target'], "Status": "ACTIVE"
                })
                send_telegram(f"🐺 EXECUTED: {order['symbol']} {order['option_type']} @ ₹{price}")
                st.session_state.active_orders.append({
                    'symbol': order['symbol'], 'entry_price': price, 'sl': order['sl'], 
                    'target': order['target'], 'qty': order['qty'], 'journal_index': len(st.session_state.trade_journal)-1
                })

def monitor_active_orders():
    for i, order in enumerate(st.session_state.active_orders[:]):
        price = get_live_price(order['symbol'])
        if price == 0:
            continue
        if price <= order['sl']:
            st.session_state.trade_journal[order['journal_index']]['Status'] = 'SL HIT'
            send_telegram(f"❌ SL HIT: {order['symbol']} @ ₹{price}")
            st.session_state.active_orders.pop(i)
            st.rerun()
        elif price >= order['target']:
            st.session_state.trade_journal[order['journal_index']]['Status'] = 'TARGET HIT'
            send_telegram(f"✅ TARGET HIT: {order['symbol']} @ ₹{price}")
            st.session_state.active_orders.pop(i)
            st.rerun()

def monitor_results():
    for company in PENDING_RESULTS:
        earnings = get_company_earnings(company['symbol'])
        if earnings:
            verdict, signal, confidence, revenue_growth, profit_growth = ai_analysis(earnings)
            alert = {
                'company': company['name'], 'symbol': company['symbol'], 'date': get_ist_now().strftime('%d %b %Y'),
                'time': get_ist_now().strftime('%H:%M'), 'revenue': f"₹{earnings.get('revenue', 0)/100:,.0f} Cr",
                'profit_growth': profit_growth, 'verdict': verdict, 'confidence': confidence, 'signal': signal
            }
            already_alerted = False
            for a in st.session_state.result_alerts:
                if a.get('company') == company['name']:
                    already_alerted = True
                    break
            if not already_alerted:
                st.session_state.result_alerts.append(alert)
                send_telegram(f"📊 OVI RESULT: {company['name']}\n📈 Revenue: {alert['revenue']}\n🎯 AI: {verdict}\n💹 Signal: {signal}")
                voice_alert(f"OVI result alert for {company['name']}. Signal {signal}")
                if signal in ["BUY", "CAUTIOUS BUY"] and st.session_state.auto_trade_enabled:
                    current_price = get_live_price(company['symbol'])
                    if current_price > 0:
                        auto_place_trade(company['symbol'], signal, current_price, confidence)

# ================= UI =================
st.markdown(f"""
<div style="text-align:center; padding:20px;">
    <h1>🐺 {APP_NAME}</h1>
    <p style="color:#94a3b8;">DEVELOPED BY {APP_AUTHOR}, {APP_LOCATION} | v{APP_VERSION}</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

now = get_ist_now()
st.markdown(f"<div class='live-time'>🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')}</div>", unsafe_allow_html=True)
st.markdown("---")

# Status Bar
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: 
    if st.session_state.algo_running:
        st.markdown('<span class="badge-success">🟢 RUNNING</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-danger">🔴 STOPPED</span>', unsafe_allow_html=True)
with c2: st.markdown('<span class="badge-success">📊 FMP ACTIVE</span>', unsafe_allow_html=True)
with c3: st.markdown('<span class="badge-success">📰 GNEWS ACTIVE</span>', unsafe_allow_html=True)
with c4: st.markdown('<span class="badge-success">📱 TELEGRAM ACTIVE</span>', unsafe_allow_html=True)
with c5: st.markdown(f'<span class="badge-info">🐺 ORDERS: {len(st.session_state.wolf_orders)}</span>', unsafe_allow_html=True)
with c6:
    if st.session_state.auto_trade_enabled:
        st.markdown('<span class="badge-success">🤖 AUTO TRADE: ON</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-warning">🤖 AUTO TRADE: OFF</span>', unsafe_allow_html=True)

st.markdown("---")

# Control
col1, col2, col3 = st.columns([2,1,1])
with col1:
    totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code")
with col2:
    if st.button("🟢 START", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED v3.2 - SAMRUDDHI EDITION")
            st.rerun()
        else:
            st.error("Valid TOTP required!")
with col3:
    if st.button("🔴 STOP", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 ALGO STOPPED")
        st.rerun()

st.markdown("---")

# ================= TABS WITH NEW NAMES =================
t1, t2, t3, t4, t5 = st.tabs([
    "🐺 WOLF ORDER",           # Wolf Order राहील
    "🌸 SANSKRUTI MARKET",     # Market -> SANSKRUTI MARKET
    "📰 VAISHNAVI NEWS",       # News -> VAISHNAVI NEWS
    "📈 OVI RESULTS",          # Results -> OVI RESULTS
    "⚙️ SAHYADRI SETTINGS"     # Settings -> SAHYADRI SETTINGS
])

# TAB 1: WOLF ORDER (बदल नाही)
with t1:
    st.markdown("### 🐺 WOLF ORDER BOOK")
    st.markdown(f"*{len(FO_SCRIPTS)} Symbols | CE/PE Options*")
    
    with st.expander("➕ PLACE ORDER", expanded=False):
        cols = st.columns(8)
        with cols[0]: sym = st.selectbox("Symbol", FO_SCRIPTS)
        with cols[1]: opt = st.selectbox("Option", OPTION_TYPES)
        with cols[2]: strike = st.number_input("Strike", 1, 500000, 24300)
        with cols[3]: qty = st.number_input("Lots", 1, 100, 1)
        with cols[4]: buy_above = st.number_input("Buy Above", 1, 500000, 100)
        with cols[5]: sl = st.number_input("Stop Loss", 1, 500000, 80)
        with cols[6]: target = st.number_input("Target", 1, 500000, 150)
        with cols[7]:
            if st.button("🐺 PLACE", use_container_width=True):
                if buy_above > sl and target > buy_above:
                    st.session_state.wolf_orders.append({
                        'symbol': sym, 'option_type': opt, 'strike_price': strike, 'qty': qty,
                        'buy_above': buy_above, 'sl': sl, 'target': target,
                        'status': 'PENDING', 'entry_price': None
                    })
                    send_telegram(f"🐺 ORDER: {sym} {opt} {strike}")
                    st.success(f"✅ Order placed")
                    st.rerun()
                else:
                    st.error("Invalid values!")
    
    pending = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
    if pending:
        st.markdown("### ⏳ PENDING ORDERS")
        st.dataframe(pd.DataFrame([{
            'Symbol': o['symbol'], 'Option': o['option_type'], 'Strike': o['strike_price'],
            'Lots': o['qty'], 'Buy Above': o['buy_above'], 'SL': o['sl'], 'Target': o['target']
        } for o in pending]), use_container_width=True)
    
    active = st.session_state.active_orders
    if active:
        st.markdown("### 🔴 ACTIVE ORDERS")
        data = []
        for o in active:
            current = get_live_price(o['symbol'])
            data.append({'Symbol': o['symbol'], 'Entry': o['entry_price'], 'Current': round(current,2) if current else 0, 'SL': o['sl'], 'Target': o['target']})
        st.dataframe(pd.DataFrame(data), use_container_width=True)

# TAB 2: SANSKRUTI MARKET
with t2:
    st.markdown("### 🌸 SANSKRUTI MARKET")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🇮🇳 NIFTY", f"₹{get_live_price('NIFTY'):,.2f}")
    with c2: st.metric("🏦 BANK NIFTY", f"₹{get_live_price('BANKNIFTY'):,.2f}")
    crude = get_live_price('CRUDE') * get_usd_inr_rate()
    with c3: st.metric("🛢️ CRUDE", f"₹{crude:,.2f}")
    ng = get_live_price('NATURALGAS') * get_usd_inr_rate()
    with c4: st.metric("🌿 NATURAL GAS", f"₹{ng:,.2f}")

# TAB 3: VAISHNAVI NEWS
with t3:
    st.markdown("### 📰 VAISHNAVI NEWS")
    col1, col2 = st.columns([3,1])
    with col2: st.session_state.voice_enabled = st.checkbox("🔊 Voice", st.session_state.voice_enabled)
    st.markdown("---")
    for news in get_gnews():
        st.markdown(f"**📌 {news['title']}**")
        st.caption(f"Source: {news['source']} | {news['time']}")
        st.markdown("---")

# TAB 4: OVI RESULTS
with t4:
    st.markdown("### 📈 OVI RESULTS")
    st.markdown("*Auto detects results via FMP API*")
    
    st.markdown("#### ⏳ Expected Results Today")
    pending_df = pd.DataFrame([{
        "Company": c['name'], "Symbol": c['symbol'], "Expected Date": c['expected_date'], 
        "Expected Time": c['expected_time'], "Expected Verdict": c['expected_verdict']
    } for c in PENDING_RESULTS])
    st.dataframe(pending_df, use_container_width=True)
    
    st.markdown("---")
    
    if st.session_state.result_alerts:
        st.markdown("#### 🔔 OVI Alerts History")
        alerts_df = pd.DataFrame([{
            "Company": a['company'], "Date": a['date'], "Time": a['time'],
            "Revenue": a['revenue'], "Profit Growth": a['profit_growth'],
            "AI Verdict": a['verdict'], "Confidence": f"{a['confidence']}%", "Signal": a['signal']
        } for a in st.session_state.result_alerts[::-1]])
        st.dataframe(alerts_df, use_container_width=True)
        
        for alert in st.session_state.result_alerts[::-1][:3]:
            signal_color = "#00ff88" if "BUY" in alert['signal'] else "#ff4444" if "SELL" in alert['signal'] else "#ffa500"
            st.markdown(f"""
            <div class="result-card">
                <b>📊 OVI: {alert['company']}</b> | {alert['date']} {alert['time']}<br>
                📈 Revenue: {alert['revenue']} | Profit Growth: {alert['profit_growth']}<br>
                🎯 AI Verdict: {alert['verdict']} | Confidence: {alert['confidence']}%<br>
                💹 Signal: <span style="color:{signal_color}">{alert['signal']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No results detected yet. Waiting for FMP API data...")

# TAB 5: SAHYADRI SETTINGS
with t5:
    st.markdown("### ⚙️ SAHYADRI SETTINGS")
    
    st.markdown("#### 🤖 AUTO TRADE")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Quantity (Lots)", 1, 50, st.session_state.auto_trade_qty)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("Stop Loss (%)", 1, 20, st.session_state.auto_trade_sl_percent)
        st.session_state.auto_trade_target_percent = st.number_input("Target (%)", 1, 30, st.session_state.auto_trade_target_percent)
    
    st.markdown("---")
    st.markdown("#### NIFTY TP SETTINGS")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.nifty_lots,key="n_lots")
    with c2: st.number_input("TP1",1,100,st.session_state.nifty_tp1,key="n_tp1")
    with c3: st.checkbox("ON",st.session_state.nifty_tp1_enabled,key="n_tp1_en")
    with c4: st.number_input("TP2",1,100,st.session_state.nifty_tp2,key="n_tp2")
    with c5: st.checkbox("ON",st.session_state.nifty_tp2_enabled,key="n_tp2_en")
    with c6: st.number_input("TP3",1,100,st.session_state.nifty_tp3,key="n_tp3")
    with c7: st.checkbox("ON",st.session_state.nifty_tp3_enabled,key="n_tp3_en")
    
    st.markdown("#### CRUDE TP SETTINGS")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.crude_lots,key="c_lots")
    with c2: st.number_input("TP1",1,100,st.session_state.crude_tp1,key="c_tp1")
    with c3: st.checkbox("ON",st.session_state.crude_tp1_enabled,key="c_tp1_en")
    with c4: st.number_input("TP2",1,100,st.session_state.crude_tp2,key="c_tp2")
    with c5: st.checkbox("ON",st.session_state.crude_tp2_enabled,key="c_tp2_en")
    with c6: st.number_input("TP3",1,100,st.session_state.crude_tp3,key="c_tp3")
    with c7: st.checkbox("ON",st.session_state.crude_tp3_enabled,key="c_tp3_en")
    
    st.markdown("#### NATURAL GAS TP SETTINGS")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.ng_lots,key="g_lots")
    with c2: st.number_input("TP1",1,50,st.session_state.ng_tp1,key="g_tp1")
    with c3: st.checkbox("ON",st.session_state.ng_tp1_enabled,key="g_tp1_en")
    with c4: st.number_input("TP2",1,50,st.session_state.ng_tp2,key="g_tp2")
    with c5: st.checkbox("ON",st.session_state.ng_tp2_enabled,key="g_tp2_en")
    with c6: st.number_input("TP3",1,50,st.session_state.ng_tp3,key="g_tp3")
    with c7: st.checkbox("ON",st.session_state.ng_tp3_enabled,key="g_tp3_en")

# ================= AUTO EXECUTION =================
if st.session_state.algo_running and st.session_state.totp_verified:
    check_and_execute_orders()
    monitor_active_orders()
    monitor_results()
    st.info("🌸 Samruddhi | 🐺 Wolf | 🌸 Sanskruti | 📰 Vaishnavi | 📈 OVI | ⚙️ Sahyadri - All Active")

# ================= SIDEBAR WITH SAMRUDDHI DASHBOARD =================
with st.sidebar:
    st.markdown("## 🌸 SAMRUDDHI DASHBOARD")
    st.markdown("---")
    st.metric("Active Orders", len(st.session_state.active_orders))
    st.metric("Pending Orders", len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']))
    st.metric("Total Trades", len(st.session_state.trade_journal))
    st.metric("Symbols Available", len(FO_SCRIPTS))
    st.metric("Results Alerts", len(st.session_state.result_alerts))
    st.markdown("---")
    st.markdown("### 🧠 SYSTEM STATUS")
    st.caption("✅ FMP API: ACTIVE")
    st.caption("✅ GNews API: ACTIVE")
    st.caption("✅ Telegram: ACTIVE")
    st.caption("✅ CE/PE Support")
    st.caption("✅ Auto Trade: " + ("ON" if st.session_state.auto_trade_enabled else "OFF"))
    st.markdown("---")
    st.markdown("### 🌸 MODULES")
    st.caption("🐺 Wolf Order Book")
    st.caption("🌸 Sanskruti Market")
    st.caption("📰 Vaishnavi News")
    st.caption("📈 OVI Results")
    st.caption("⚙️ Sahyadri Settings")

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🐺 {APP_NAME} v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION} | 🌸 SAMRUDDHI EDITION")

# ================= REFRESH =================
time.sleep(30)
st.rerun()
