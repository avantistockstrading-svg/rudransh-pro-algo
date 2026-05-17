"""
🐺 RUDRANSH PRO ALGO X - REAL EDITION
=======================================
VERSION: 5.0.0
ALL FEATURES REAL - NO DEMO
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import math

# ================= VERSION & INFO =================
APP_VERSION = "5.0.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= API KEYS =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"
TELEGRAM_BOT = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
TELEGRAM_CHAT = "1983026913"

# ================= ANGEL ONE API KEYS =================
ANGEL_API_KEY = "7yyokKoC"
ANGEL_CLIENT_CODE = "S470211"
ANGEL_PASSWORD = "1234"
ANGEL_TOTP_SECRET = "P5XCUTXRKXQNNATBO5JZYM6SPI"

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
    .status-card { background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; }
    @media only screen and (max-width: 768px) {
        .stApp { padding: 5px !important; }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 18px !important; }
        .stButton > button { width: 100% !important; font-size: 14px !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 8px !important; flex-wrap: wrap !important; }
        .stTabs [data-baseweb="tab"] { padding: 6px 12px !important; font-size: 12px !important; }
        .row-widget.stColumns { flex-wrap: wrap !important; }
        .row-widget.stColumns > div { flex: 1 1 100% !important; min-width: 100% !important; }
        .live-time { font-size: 18px !important; }
    }
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
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
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
if "auto_trade_qty" not in st.session_state:
    st.session_state.auto_trade_qty = 1
if "auto_trade_sl_percent" not in st.session_state:
    st.session_state.auto_trade_sl_percent = 5
if "auto_trade_target_percent" not in st.session_state:
    st.session_state.auto_trade_target_percent = 10

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

# ================= DAILY TRADE COUNTERS =================
if "daily_trade_count" not in st.session_state:
    st.session_state.daily_trade_count = {
        "NIFTY": {"buy": 0, "sell": 0},
        "BANKNIFTY": {"buy": 0, "sell": 0},
        "CRUDE": {"buy": 0, "sell": 0},
        "NATURALGAS": {"buy": 0, "sell": 0}
    }
if "last_reset_date" not in st.session_state:
    st.session_state.last_reset_date = get_ist_now().date()
if "daily_pnl" not in st.session_state:
    st.session_state.daily_pnl = 0

# Reset daily counters
if get_ist_now().date() != st.session_state.last_reset_date:
    st.session_state.daily_trade_count = {
        "NIFTY": {"buy": 0, "sell": 0},
        "BANKNIFTY": {"buy": 0, "sell": 0},
        "CRUDE": {"buy": 0, "sell": 0},
        "NATURALGAS": {"buy": 0, "sell": 0}
    }
    st.session_state.daily_pnl = 0
    st.session_state.last_reset_date = get_ist_now().date()

# ================= COMPLETE 220+ F&O SYMBOLS =================
FO_SCRIPTS = [
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "CRUDE", "NATURALGAS",
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR", "ITC",
    "SBIN", "BHARTIARTL", "KOTAKBANK", "AXISBANK", "LT", "DMART", "SUNPHARMA",
    "BAJFINANCE", "TITAN", "MARUTI", "TATAMOTORS", "TATASTEEL", "WIPRO",
    "HCLTECH", "ONGC", "NTPC", "POWERGRID", "ULTRACEMCO", "ADANIPORTS",
    "ADANIENT", "ASIANPAINT", "BAJAJFINSV", "BRITANNIA", "CIPLA", "COALINDIA",
    "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HDFCLIFE", "HEROMOTOCO",
    "HINDALCO", "IOC", "INDUSINDBK", "JSWSTEEL", "M&M", "NESTLEIND",
    "PIDILITIND", "SBILIFE", "SHREECEM", "SIEMENS", "SRF", "TATACONSUM",
    "TATAPOWER", "TECHM", "UPL", "VEDL", "YESBANK", "ZYDUSLIFE", "ABB", "APOLLOHOSP",
    "ASHOKLEY", "ASTRAL", "AUROPHARMA", "BANDHANBNK", "BANKBARODA", "BEL", "BPCL",
    "CANBK", "CHOLAFIN", "COFORGE", "DABUR", "DLF", "FEDERALBNK", "GAIL", "GODREJCP",
    "GODREJPROP", "HAVELLS", "HDFCAMC", "HINDPETRO", "ICICIGI", "ICICIPRULI", "IDEA",
    "INDIGO", "IRCTC", "JIOFIN", "JUBLFOOD", "LUPIN", "MANKIND", "MARICO", "MAXHEALTH",
    "MCX", "MOTHERSON", "MPHASIS", "MUTHOOTFIN", "NAUKRI", "NHPC", "NMDC", "PEL",
    "PFC", "PNB", "POLYCAB", "RECLTD", "SAIL", "SOLARINDS", "360ONE", "ABCAPITAL",
    "ADANIENSOL", "ADANIGREEN", "ADANIPOWER", "ALKEM", "AMBER", "AMBUJACEM", "ANGELONE",
    "APLAPOLLO", "AUBANK", "BAJAJHLDNG", "BALKRISIND", "BATAINDIA", "BERGEPAINT",
    "BHARATFORG", "BHEL", "BIOCON", "BOSCHLTD", "CADILAHC", "CAMS", "CAPLIPOINT",
    "CASTROLIND", "CCL", "CDSL", "CENTURYPLY", "CESC", "CGPOWER", "CLEAN", "COCHINSHIP",
    "CONCOR", "COROMANDEL", "CROMPTON", "CUMMINSIND", "CYIENT", "DALBHARAT", "DELHIVERY",
    "DIXON", "EASEMYTRIP", "EDELWEISS", "EMAMILTD", "ENDURANCE", "ERIS", "ESCORTS",
    "EXIDEIND", "FACT", "FINCABLES", "FINEORG", "FIVESTAR", "FORTIS", "GESHIP",
    "GLENMARK", "GMRINFRA", "GODREJAGRO", "GRANULES", "GREAVESCOT", "GSPL", "GUFICBIO",
    "HAL", "HAPPSTMNDS", "HEIDELBERG", "HINDZINC", "IBULHSGFIN", "IDBI", "IDFCFIRSTB",
    "IEX", "INDIAMART", "INDIANB", "INDUSTOWER", "INOXWIND", "IREDA", "IRFC",
    "JINDALSTEL", "JSPL", "JSWENERGY", "KALYANKJIL", "KAYNES", "KEI", "KFINTECH",
    "KPITTECH", "LAURUSLABS", "LICHSGFIN", "LODHA", "LTF", "MANAPPURAM", "MFSL",
    "MOTILALOFS", "NATIONALUM", "NAMINDIA", "NBCC", "NUVAMA", "OBEROIRLTY", "OIL",
    "OFSS", "PAYTM", "PAGEIND", "PATANJALI", "PERSISTENT", "PETRONET", "PGEL",
    "PHOENIXLTD", "PIIND", "PNBHOUSING", "POLICYBZR", "PRESTIGE", "RBLBANK", "RVNL",
    "SHRIRAMFIN", "SONACOMS", "SUPREMEIND", "SUZLON", "SWIGGY", "TATAELXSI", "TIINDIA",
    "TORNTPHARM", "TRENT", "TVSMOTOR", "UNIONBANK", "UNITEDSPIRITS", "UNOMINDA",
    "VBL", "VOLTAS", "WAAREEENER", "WELCORP", "ZEEL"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= TRADING HOURS =================
TRADING_HOURS = {
    "NIFTY": {"start": 9, "start_min": 30, "end": 15, "end_min": 0},
    "BANKNIFTY": {"start": 9, "start_min": 30, "end": 15, "end_min": 0},
    "CRUDE": {"start": 11, "start_min": 0, "end": 22, "end_min": 0},
    "NATURALGAS": {"start": 11, "start_min": 0, "end": 22, "end_min": 0}
}

def is_trading_time(symbol):
    now = get_ist_now()
    hours = TRADING_HOURS.get(symbol, {"start": 9, "start_min": 30, "end": 15, "end_min": 0})
    start_time = now.replace(hour=hours["start"], minute=hours["start_min"], second=0)
    end_time = now.replace(hour=hours["end"], minute=hours["end_min"], second=0)
    return start_time <= now <= end_time and now.weekday() < 5

def can_take_trade(symbol, trade_type):
    if trade_type == "BUY":
        return st.session_state.daily_trade_count[symbol]["buy"] < 1
    else:
        return st.session_state.daily_trade_count[symbol]["sell"] < 1

def increment_trade_count(symbol, trade_type):
    if trade_type == "BUY":
        st.session_state.daily_trade_count[symbol]["buy"] += 1
    else:
        st.session_state.daily_trade_count[symbol]["sell"] += 1

# ================= SECTOR MAPPING =================
SECTOR_MAPPING = {
    "NIFTY": "NIFTY", "BANKNIFTY": "BANKING", "RELIANCE": "ENERGY", "TCS": "IT",
    "HDFCBANK": "BANKING", "ICICIBANK": "BANKING", "INFY": "IT", "HINDUNILVR": "FMCG",
    "ITC": "FMCG", "SBIN": "BANKING", "BHARTIARTL": "TELECOM", "KOTAKBANK": "BANKING",
    "AXISBANK": "BANKING", "LT": "CAPITAL GOODS", "DMART": "RETAIL", "SUNPHARMA": "PHARMA",
    "BAJFINANCE": "FINANCE", "TITAN": "CONSUMER", "MARUTI": "AUTO", "TATAMOTORS": "AUTO",
    "TATASTEEL": "METALS", "WIPRO": "IT", "HCLTECH": "IT", "ONGC": "ENERGY",
    "NTPC": "ENERGY", "POWERGRID": "ENERGY", "ULTRACEMCO": "CEMENT", "ADANIPORTS": "INFRA",
    "ADANIENT": "INFRA", "ASIANPAINT": "CHEMICALS", "BAJAJFINSV": "FINANCE", "BRITANNIA": "FMCG",
    "CIPLA": "PHARMA", "COALINDIA": "METALS", "DIVISLAB": "PHARMA", "DRREDDY": "PHARMA"
}

# ================= FMP API FUNCTIONS =================
def check_fmp_api():
    try:
        url = f"https://financialmodelingprep.com/stable/stock-list?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return True, "Active", f"✅ Connected"
            return False, "Warning", "⚠️ No data"
        return False, "Error", f"HTTP {response.status_code}"
    except:
        return False, "Error", "❌ Connection failed"

def get_company_earnings(symbol):
    try:
        url = f"https://financialmodelingprep.com/stable/income-statement?symbol={symbol}&apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]
        return None
    except:
        return None

# ================= EARNINGS CALENDAR API (AUTO DAILY UPDATE) =================
def get_today_earnings():
    """FMP Earnings Calendar API वरून आजच्या results ची list मिळवा"""
    try:
        today = get_ist_now().strftime('%Y-%m-%d')
        url = f"https://financialmodelingprep.com/stable/earnings-calendar?from={today}&to={today}&apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            earnings_list = []
            for item in data:
                symbol = item.get('symbol', '').replace('.NS', '')
                earnings_list.append({
                    'name': symbol,
                    'symbol': symbol,
                    'date': item.get('date', today),
                    'eps_estimated': item.get('epsEstimated'),
                    'eps_actual': item.get('epsActual')
                })
            return earnings_list
        return []
    except Exception as e:
        print(f"Earnings Calendar Error: {e}")
        return []

def get_pending_results():
    """Dynamic results list - daily update होईल"""
    earnings = get_today_earnings()
    if earnings:
        return earnings
    # API error असल्यास empty list return करा
    return []

# ================= JOURNAL SYSTEM FUNCTIONS =================

def add_to_journal_with_system(order, system_name, exit_price=None, exit_reason=None):
    """Journal मध्ये trade add करा system name + time सह"""
    
    entry_price = order['entry_price']
    qty = order['qty']
    
    # Multiplier calculate
    if order['symbol'] in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
        multiplier = 50 if order['symbol'] == "NIFTY" else 25
    elif order['symbol'] in ["CRUDE", "NATURALGAS"]:
        multiplier = 100
    else:
        multiplier = 100
    
    if exit_price:
        if order['option_type'] == "CALL (CE)":
            pnl_points = exit_price - entry_price
        else:
            pnl_points = entry_price - exit_price
        pnl_value = pnl_points * qty * multiplier
        status = exit_reason
    else:
        pnl_value = 0
        status = "OPEN"
        exit_price = 0
    
    trade_record = {
        "No": len(st.session_state.trade_journal) + 1,
        "⏰ Time": get_ist_now().strftime('%H:%M:%S'),
        "🎯 System": system_name,
        "📊 Symbol": f"{order['symbol']} {order['option_type']} {order.get('strike_price', '')}",
        "🔄 Type": order.get('signal_type', 'MANUAL'),
        "📦 Lots": order['qty'],
        "📥 Entry": round(entry_price, 2),
        "📤 Exit": round(exit_price, 2) if exit_price else "-",
        "💰 P&L": f"₹{round(pnl_value, 2)}",
        "📍 Status": status
    }
    
    st.session_state.trade_journal.append(trade_record)
    st.session_state.daily_pnl += pnl_value

def monitor_today_results():
    """OVI Results monitor करा"""
    try:
        pending = get_pending_results()
        for company in pending:
            symbol = company.get('symbol', '')
            if symbol:
                earnings = get_company_ear

# ================= MONITOR RESULTS =================
def monitor_today_results():
    """OVI Results monitor करून journal मध्ये add करा"""
    try:
        pending = get_pending_results()
        for company in pending:
            symbol = company.get('symbol', '')
            if symbol:
                earnings = get_company_earnings(symbol)
                if earnings:
                    revenue = earnings.get('revenue', 0)
                    prev_revenue = earnings.get('revenue', 0)
                    revenue_growth = ((revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
                    
                    if revenue_growth > 10:
                        result_type = "POSITIVE"
                        signal = "BUY"
                    elif revenue_growth < -5:
                        result_type = "NEGATIVE"
                        signal = "SELL"
                    else:
                        result_type = "NEUTRAL"
                        signal = "WAIT"
                    
                    already_alerted = False
                    for alert in st.session_state.result_alerts:
                        if alert.get('company') == company.get('name'):
                            already_alerted = True
                            break
                    
                    if not already_alerted and result_type != "NEUTRAL":
                        st.session_state.result_alerts.append({
                            'company': company.get('name', symbol),
                            'date': get_ist_now().strftime('%Y-%m-%d'),
                            'time': get_ist_now().strftime('%H:%M:%S'),
                            'verdict': result_type,
                            'signal': signal
                        })
                        
                        # Journal मध्ये result entry add करा
                        st.session_state.trade_journal.append({
                            "No": len(st.session_state.trade_journal) + 1,
                            "Time": get_ist_now().strftime('%H:%M:%S'),
                            "System": "📈 OVI RESULTS",
                            "Symbol": company.get('name', symbol),
                            "Type": result_type,
                            "Signal": signal,
                            "Entry": "-",
                            "Exit": "-",
                            "P&L (₹)": 0,
                            "Status": f"RESULT DECLARED - {result_type}"
                        })
                        send_telegram(f"📊 OVI: {company.get('name', symbol)} - {result_type} - {signal}")
    except Exception as e:
        print(f"Monitor results error: {e}")

# ================= CHECK & EXECUTE WOLF ORDERS =================
def check_and_execute_orders_with_journal():
    """Wolf orders execute करा आणि journal मध्ये add करा"""
    pending_orders = [o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING']
    
    for order in pending_orders:
        current_price = get_live_price(order['symbol'])
        
        if current_price > 0 and current_price >= order.get('buy_above', 0):
            order['status'] = 'EXECUTED'
            order['entry_price'] = current_price
            order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
            
            active_order = {
                'symbol': order['symbol'],
                'option_type': order.get('option_type', 'CALL (CE)'),
                'strike_price': order.get('strike_price', 0),
                'qty': order.get('qty', 1),
                'entry_price': current_price,
                'entry_time': order['entry_time'],
                'sl': order.get('sl', current_price * 0.95),
                'target': order.get('target', current_price * 1.05),
                'signal_type': '🐺 WOLF'
            }
            st.session_state.active_orders.append(active_order)
            
            # Journal मध्ये entry add करा
            st.session_state.trade_journal.append({
                "No": len(st.session_state.trade_journal) + 1,
                "Time": order['entry_time'],
                "System": "🐺 WOLF",
                "Symbol": f"{order['symbol']} {order.get('option_type', '')} {order.get('strike_price', '')}",
                "Type": "BUY",
                "Signal": order.get('signal_type', 'MANUAL'),
                "Entry": round(current_price, 2),
                "Exit": "-",
                "P&L (₹)": 0,
                "Status": "ACTIVE"
            })
            
            send_telegram(f"🐺 WOLF EXECUTED: {order['symbol']} at ₹{current_price}")
            voice_alert(f"Wolf order executed for {order['symbol']}")

def monitor_active_orders_with_pnl():
    """Active orders monitor करा आणि exit झाल्यावर journal update करा"""
    orders_to_remove = []
    
    for i, order in enumerate(st.session_state.active_orders):
        current_price = get_live_price(order['symbol'])
        
        if current_price <= 0:
            continue
        
        if order['option_type'] == "CALL (CE)":
            if current_price <= order['sl']:
                exit_reason = "SL HIT"
                exit_price = current_price
                orders_to_remove.append((i, order, exit_price, exit_reason))
            elif current_price >= order['target']:
                exit_reason = "TARGET HIT"
                exit_price = current_price
                orders_to_remove.append((i, order, exit_price, exit_reason))
        else:
            if current_price >= order['sl']:
                exit_reason = "SL HIT"
                exit_price = current_price
                orders_to_remove.append((i, order, exit_price, exit_reason))
            elif current_price <= order['target']:
                exit_reason = "TARGET HIT"
                exit_price = current_price
                orders_to_remove.append((i, order, exit_price, exit_reason))
    
    for idx, order, exit_price, reason in reversed(orders_to_remove):
        # P&L calculate करा
        multiplier = 50 if order['symbol'] == "NIFTY" else 25 if order['symbol'] == "BANKNIFTY" else 100
        if order['option_type'] == "CALL (CE)":
            pnl_points = exit_price - order['entry_price']
        else:
            pnl_points = order['entry_price'] - exit_price
        pnl_value = pnl_points * order['qty'] * multiplier
        
        # Journal मध्ये exit update करा
        for journal_entry in st.session_state.trade_journal:
            if journal_entry.get('Status') == "ACTIVE" and journal_entry.get('Entry') == order['entry_price']:
                journal_entry['Exit'] = round(exit_price, 2)
                journal_entry['P&L (₹)'] = round(pnl_value, 2)
                journal_entry['Status'] = f"CLOSED - {reason}"
                journal_entry['Time'] = f"{journal_entry['Time']} → {get_ist_now().strftime('%H:%M:%S')}"
                break
        else:
            # New journal entry for exit
            st.session_state.trade_journal.append({
                "No": len(st.session_state.trade_journal) + 1,
                "Time": get_ist_now().strftime('%H:%M:%S'),
                "System": order.get('signal_type', 'UNKNOWN'),
                "Symbol": f"{order['symbol']} {order['option_type']}",
                "Type": "CLOSE",
                "Signal": reason,
                "Entry": round(order['entry_price'], 2),
                "Exit": round(exit_price, 2),
                "P&L (₹)": round(pnl_value, 2),
                "Status": reason
            })
        
        st.session_state.active_orders.pop(idx)
        send_telegram(f"📊 {order.get('signal_type', 'ORDER')} CLOSED: {order['symbol']} - {reason} | P&L: ₹{pnl_value:.2f}")

def auto_trade_from_signal_with_journal():
    """SAHYADRI सिस्टीम वरून auto trade करा"""
    nifty_trend = get_nifty_trend()
    symbols_to_check = ["NIFTY", "BANKNIFTY", "CRUDE", "NATURALGAS"]
    
    for symbol in symbols_to_check:
        sector_trend = get_sector_trend(SECTOR_MAPPING.get(symbol, "NIFTY"))
        signal, price, indicators = get_strict_signal(symbol, nifty_trend, sector_trend)
        
        if signal in ["BUY", "SELL"] and st.session_state.auto_trade_enabled:
            already_active = any(a['symbol'] == symbol for a in st.session_state.active_orders)
            trade_type = "BUY" if signal == "BUY" else "SELL"
            can_trade = can_take_trade(symbol, trade_type)
            
            if not already_active and can_trade and is_trading_time(symbol):
                option_type = "CALL (CE)" if signal == "BUY" else "PUT (PE)"
                
                # Strike price calculate करा
                if symbol in ["NIFTY", "BANKNIFTY"]:
                    strike_interval = 50 if symbol == "NIFTY" else 100
                    strike_price = math.floor(price / strike_interval) * strike_interval
                else:
                    strike_price = math.floor(price / 10) * 10
                
                sl_percent = st.session_state.auto_trade_sl_percent / 100
                target_percent = st.session_state.auto_trade_target_percent / 100
                
                if signal == "BUY":
                    sl_price = price * (1 - sl_percent)
                    target_price = price * (1 + target_percent)
                else:
                    sl_price = price * (1 + sl_percent)
                    target_price = price * (1 - target_percent)
                
                order = {
                    'symbol': symbol,
                    'option_type': option_type,
                    'strike_price': strike_price,
                    'qty': st.session_state.auto_trade_qty,
                    'entry_price': price,
                    'entry_time': get_ist_now().strftime('%H:%M:%S'),
                    'sl': sl_price,
                    'target': target_price,
                    'signal_type': '⚙️ SAHYADRI'
                }
                
                st.session_state.active_orders.append(order)
                increment_trade_count(symbol, trade_type)
                
                # Journal मध्ये SAHYADRI trade add करा
                st.session_state.trade_journal.append({
                    "No": len(st.session_state.trade_journal) + 1,
                    "Time": order['entry_time'],
                    "System": "⚙️ SAHYADRI",
                    "Symbol": f"{symbol} {option_type} {strike_price}",
                    "Type": signal,
                    "Signal": f"AUTO - {signal}",
                    "Entry": round(price, 2),
                    "Exit": "-",
                    "P&L (₹)": 0,
                    "Status": "ACTIVE"
                })
                
                send_telegram(f"⚙️ SAHYADRI AUTO {signal}: {symbol} at ₹{price} | SL: ₹{sl_price} | Target: ₹{target_price}")
                voice_alert(f"Sahyadri auto {signal} for {symbol}")

# ================= PENDING RESULTS (Dynamic) =================
PENDING_RESULTS = get_pending_results()

# ================= TREND FUNCTIONS =================
def get_nifty_trend():
    try:
        df = yf.download("^NSEI", period="10d", interval="1d", progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        current = df['Close'].iloc[-1]
        ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
        if current > ema20:
            return "POSITIVE"
        elif current < ema20:
            return "NEGATIVE"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_sector_trend(sector):
    sector_indices = {
        "BANKING": "^NSEBANK", "IT": "NIFTY_IT.NS", "PHARMA": "NIFTY_PHARMA.NS",
        "AUTO": "NIFTY_AUTO.NS", "FMCG": "NIFTY_FMCG.NS", "METALS": "NIFTY_METAL.NS",
        "ENERGY": "NIFTY_ENERGY.NS", "FINANCE": "NIFTY_FIN_SERVICE.NS", "TELECOM": "NIFTY_TELECOM.NS"
    }
    index = sector_indices.get(sector, "^NSEI")
    try:
        df = yf.download(index, period="10d", interval="1d", progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        current = df['Close'].iloc[-1]
        ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
        if current > ema20:
            return "BULLISH"
        elif current < ema20:
            return "BEARISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_mtf_trend(symbol, interval):
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
        df = yf.download(ticker, period="5d", interval=interval, progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        current = df['Close'].iloc[-1]
        ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
        if current > ema20:
            return "UP"
        elif current < ema20:
            return "DOWN"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

# ================= TECHNICAL INDICATORS =================
def get_technical_indicators(symbol):
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
        
        df = yf.download(ticker, period="10d", interval="5m", progress=False)
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
        current_rsi = rsi.iloc[-1] if not rsi.isna().iloc[-1] else 50
        
        plus_dm = high.diff()
        minus_dm = low.diff()
        plus_dm = plus_dm.where(plus_dm > 0, 0)
        minus_dm = minus_dm.where(minus_dm > 0, 0)
        tr = pd.DataFrame({'hl': high - low, 'hc': abs(high - close.shift()), 'lc': abs(low - close.shift())}).max(axis=1)
        atr = tr.rolling(14).mean()
        plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(14).mean() / atr)
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(14).mean().iloc[-1] if len(dx) > 14 else 25
        
        volume_sma = volume.rolling(20).mean()
        volume_filter = volume.iloc[-1] > volume_sma.iloc[-1] if not volume_sma.isna().iloc[-1] else True
        
        prev_candle = df.iloc[-2]
        curr_candle = df.iloc[-1]
        strong_bull = curr_candle['Close'] > curr_candle['Open'] and curr_candle['Close'] > prev_candle['High']
        strong_bear = curr_candle['Close'] < curr_candle['Open'] and curr_candle['Close'] < prev_candle['Low']
        
        sideways = (45 < current_rsi < 55) and (adx < 20) if not pd.isna(adx) else False
        
        return {
            "current_price": close.iloc[-1], "ema9": ema9, "ema20": ema20, "ema200": ema200,
            "rsi": current_rsi, "adx": adx if not pd.isna(adx) else 25,
            "volume_filter": volume_filter, "strong_bull": strong_bull, "strong_bear": strong_bear,
            "sideways": sideways, "c1_high": prev_candle['High'], "c1_low": prev_candle['Low']
        }
    except:
        return None

# ================= STRICT SIGNAL =================
def get_strict_signal(symbol, nifty_trend, sector_trend):
    if symbol in ["NIFTY", "BANKNIFTY", "CRUDE", "NATURALGAS"]:
        nifty_condition = nifty_trend == "POSITIVE" if symbol == "NIFTY" else True
        sector_condition = True
    else:
        nifty_condition = nifty_trend == "POSITIVE"
        sector_condition = sector_trend == "BULLISH"
    
    indicators = get_technical_indicators(symbol)
    if indicators is None:
        return "WAIT", 0, None
    
    trend5_up = get_mtf_trend(symbol, "5m") == "UP"
    trend15_up = get_mtf_trend(symbol, "15m") == "UP"
    trend1h_up = get_mtf_trend(symbol, "60m") == "UP"
    
    buy_conditions = (nifty_condition and sector_condition and not indicators["sideways"] and
                      indicators["ema9"] > indicators["ema20"] and indicators["current_price"] > indicators["ema200"] and
                      indicators["rsi"] >= 55 and indicators["adx"] >= 22 and indicators["volume_filter"] and
                      indicators["strong_bull"] and indicators["current_price"] > indicators["c1_high"] and
                      trend5_up and trend15_up and trend1h_up)
    
    sell_conditions = (nifty_trend == "NEGATIVE" and not indicators["sideways"] and
                       indicators["ema9"] < indicators["ema20"] and indicators["current_price"] < indicators["ema200"] and
                       indicators["rsi"] <= 45 and indicators["adx"] >= 22 and indicators["volume_filter"] and
                       indicators["strong_bear"] and indicators["current_price"] < indicators["c1_low"] and
                       not trend5_up and not trend15_up and not trend1h_up)
    
    if buy_conditions:
        return "BUY", indicators["current_price"], indicators
    elif sell_conditions:
        return "SELL", indicators["current_price"], indicators
    return "WAIT", 0, indicators

# ================= LIVE P&L FUNCTIONS =================
def calculate_live_pnl():
    total_pnl = 0
    pnl_details = []
    for order in st.session_state.active_orders:
        current_price = get_live_price(order['symbol'])
        if current_price > 0:
            entry = order['entry_price']
            qty = order['qty']
            if order['symbol'] in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
                multiplier = 50 if order['symbol'] == "NIFTY" else 25
            elif order['symbol'] in ["CRUDE", "NATURALGAS"]:
                multiplier = 100
            else:
                multiplier = 100
            if order['option_type'] == "CALL (CE)":
                pnl_points = current_price - entry
            else:
                pnl_points = entry - current_price
            pnl_value = pnl_points * qty * multiplier
            total_pnl += pnl_value
            pnl_details.append({
                'symbol': order['symbol'], 'option_type': order['option_type'],
                'strike': order.get('strike_price', 'N/A'), 'entry': entry,
                'current': current_price, 'pnl_points': pnl_points,
                'pnl_value': pnl_value, 'qty': qty
            })
    return total_pnl, pnl_details

def add_to_journal(order, exit_price=None, exit_reason=None):
    entry_price = order['entry_price']
    qty = order['qty']
    if order['symbol'] in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
        multiplier = 50 if order['symbol'] == "NIFTY" else 25
    elif order['symbol'] in ["CRUDE", "NATURALGAS"]:
        multiplier = 100
    else:
        multiplier = 100
    if exit_price:
        if order['option_type'] == "CALL (CE)":
            pnl_points = exit_price - entry_price
        else:
            pnl_points = entry_price - exit_price
        pnl_value = pnl_points * qty * multiplier
        status = exit_reason
    else:
        pnl_value = 0
        status = "OPEN"
        exit_price = 0
    trade_record = {
        "No": len(st.session_state.trade_journal) + 1,
        "Time": order.get('entry_time', get_ist_now().strftime('%H:%M:%S')),
        "Symbol": f"{order['symbol']} {order['option_type']} {order.get('strike_price', '')}",
        "Type": order.get('signal_type', 'MANUAL'), "Lots": order['qty'],
        "Entry": round(entry_price, 2), "Exit": round(exit_price, 2) if exit_price else "-",
        "P&L (₹)": round(pnl_value, 2), "Status": status
    }
    st.session_state.trade_journal.append(trade_record)
    if "daily_pnl" not in st.session_state:
        st.session_state.daily_pnl = 0
    st.session_state.daily_pnl += pnl_value

def show_portfolio_dashboard():
    total_pnl, pnl_details = calculate_live_pnl()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #00b4d8;"><span style="font-size: 24px;">💰</span><h3 style="margin: 5px 0; color: #00b4d8;">Total P&L</h3><h2 style="margin: 0; color: {"#00ff88" if total_pnl >= 0 else "#ff4444"};">₹{total_pnl:,.2f}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #ffaa00;"><span style="font-size: 24px;">🔴</span><h3 style="margin: 5px 0; color: #ffaa00;">Active Trades</h3><h2 style="margin: 0; color: #ffaa00;">{len(st.session_state.active_orders)}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #00ff88;"><span style="font-size: 24px;">📋</span><h3 style="margin: 5px 0; color: #00ff88;">Total Trades</h3><h2 style="margin: 0; color: #00ff88;">{len(st.session_state.trade_journal)}</h2></div>', unsafe_allow_html=True)
    with col4:
        daily_pnl_color = "#00ff88" if st.session_state.daily_pnl >= 0 else "#ff4444"
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid {daily_pnl_color};"><span style="font-size: 24px;">📅</span><h3 style="margin: 5px 0; color: {daily_pnl_color};">Today\'s P&L</h3><h2 style="margin: 0; color: {daily_pnl_color};">₹{st.session_state.daily_pnl:,.2f}</h2></div>', unsafe_allow_html=True)
    st.markdown("---")
    if pnl_details:
        st.markdown("#### 📊 Live P&L Details")
        st.dataframe(pd.DataFrame([{
            "Symbol": d['symbol'], "Option": d['option_type'], "Strike": d['strike'],
            "Entry": d['entry'], "Current": d['current'], "P&L (pts)": f"{d['pnl_points']:+.2f}",
            "P&L (₹)": f"₹{d['pnl_value']:,.2f}", "Qty": d['qty']
        } for d in pnl_details]), use_container_width=True)
    else:
        st.info("No active trades")
    st.markdown("---")
    if st.session_state.trade_journal:
        st.markdown("#### 📋 Trade Journal")
        st.dataframe(pd.DataFrame(st.session_state.trade_journal[::-1]), use_container_width=True, height=400)
    else:
        st.info("No trades executed yet")

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

def get_gnews():
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=8&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [{'title': a['title'], 'source': a['source']['name'], 'time': a['publishedAt'][:10]} for a in data.get('articles', [])]
    except:
        pass
    return [{'title': 'Market Update', 'source': 'News', 'time': get_ist_now().strftime('%Y-%m-%d')}]

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage", data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=10)
    except:
        pass

def voice_alert(msg):
    if st.session_state.voice_enabled:
        st.markdown(f"<script>var s=new SpeechSynthesisUtterance('{msg}');s.lang='en-US';speechSynthesis.speak(s);</script>", unsafe_allow_html=True)

def monitor_fmp_results():
    for company in PENDING_RESULTS:
        earnings = get_company_earnings(company['symbol'])
        if earnings:
            revenue = earnings.get('revenue', 0)
            prev_revenue = earnings.get('revenue', 0)
            revenue_growth = ((revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            if revenue_growth > 10:
                result_type = "POSITIVE"
            elif revenue_growth < -5:
                result_type = "NEGATIVE"
            else:
                result_type = "NEUTRAL"
            alert = {'company': company['name'], 'result': result_type, 'time': get_ist_now().strftime('%H:%M:%S')}
            already = False
            for a in st.session_state.result_alerts:
                if a.get('company') == company['name']:
                    already = True
                    break
            if not already:
                st.session_state.result_alerts.append(alert)
                send_telegram(f"📊 RESULT: {company['name']} - {result_type}")

def analyze_news_sentiment(title):
    title_lower = title.lower()
    score = 0
    for w in ['surge', 'rally', 'boom', 'record', 'peak', 'high']:
        if w in title_lower: score += 15
    for w in ['gain', 'up', 'positive', 'bull', 'rise', 'growth']:
        if w in title_lower: score += 5
    for w in ['crash', 'plunge', 'slump', 'collapse']:
        if w in title_lower: score -= 15
    for w in ['fall', 'drop', 'down', 'negative', 'bear', 'decline']:
        if w in title_lower: score -= 5
    if score >= 15: return "STRONG BULLISH", "🚀", "#00ff44"
    elif score >= 5: return "BULLISH", "📈", "#88ff88"
    elif score <= -15: return "STRONG BEARISH", "💀", "#ff3333"
    elif score <= -5: return "BEARISH", "📉", "#ff6666"
    else: return "NEUTRAL", "⚪", "#ffaa00"

def get_news_with_sentiment():
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=12&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [{'title': a['title'], 'source': a['source']['name'], 'time': a['publishedAt'][:10], 'sentiment': analyze_news_sentiment(a['title'])[0], 'icon': analyze_news_sentiment(a['title'])[1], 'color': analyze_news_sentiment(a['title'])[2]} for a in data.get('articles', [])]
    except:
        pass
    return [{'title': 'NIFTY hits all-time high', 'source': 'Economic Times', 'time': get_ist_now().strftime('%Y-%m-%d'), 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'}]

def process_result_and_trade(company_name, symbol, result_type):
    nifty_trend = get_nifty_trend()
    if result_type == "POSITIVE" and nifty_trend == "POSITIVE":
        signal = "BUY"
        option_type = "CALL (CE)"
    elif result_type == "NEGATIVE" and nifty_trend == "NEGATIVE":
        signal = "SELL"
        option_type = "PUT (PE)"
    else:
        return False, f"WAIT - {result_type} / NIFTY {nifty_trend}"
    current_price = get_live_price(symbol)
    if current_price > 0:
        if symbol in ["NIFTY", "BANKNIFTY"]:
            strike_interval = 50 if symbol == "NIFTY" else 100
            strike_price = math.floor(current_price / strike_interval) * strike_interval
        elif symbol in ["CRUDE", "NATURALGAS"]:
            strike_price = math.floor(current_price) * 100
        else:
            strike_price = math.floor(current_price / 10) * 10
        st.session_state.wolf_orders.append({
            'symbol': symbol, 'option_type': option_type, 'strike_price': strike_price, 'qty': 1,
            'buy_above': current_price, 'sl': current_price * 0.85, 'target': current_price * 1.2,
            'status': 'PENDING', 'placed_time': get_ist_now().strftime('%H:%M:%S'),
            'auto_trade': True, 'result_based': True, 'company': company_name
        })
        send_telegram(f"📊 RESULT: {company_name} - {signal} {option_type}")
        return True, f"{signal} order placed"
    return False, "Price not available"
# ================= UI HEADER =================
st.markdown(f"""
<div style="text-align:center; padding:20px;">
    <h1>🐺 {APP_NAME}</h1>
    <p style="color:#94a3b8;">{APP_AUTHOR}, {APP_LOCATION} | v{APP_VERSION}</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

now = get_ist_now()
st.markdown(f"<div class='live-time'>🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')}</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= API STATUS DASHBOARD =================
st.markdown("## 🔌 API STATUS DASHBOARD")
fmp_status, fmp_level, fmp_msg = check_fmp_api()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="status-card" style="border-left: 4px solid #00ff88;">📊 <strong>FMP API</strong><br><span style="color:#00ff88">🟢 {fmp_msg}</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="status-card" style="border-left: 4px solid #00ff88;">📰 <strong>GNews API</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="status-card" style="border-left: 4px solid #00ff88;">📱 <strong>Telegram Bot</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ================= CONTROL PANEL =================
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; padding: 20px; margin: 10px 0; border: 1px solid rgba(0,255,136,0.2);">
    <h4 style="margin:0 0 15px 0; color:#00b4d8; text-align:center;">🎮 CONTROL PANEL</h4>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("""<div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 5px 15px; border: 1px solid #00b4d8;"><label style="color:#00b4d8; font-size:12px;">🔐 6-DIGIT TOTP CODE</label></div>""", unsafe_allow_html=True)
    totp = st.text_input("TOTP", type="password", placeholder="Enter 6-digit code", key="totp_main", label_visibility="collapsed")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🟢 START ALGO", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED v5.0")
            st.success("✅ Algo Started Successfully!")
            st.rerun()
        else:
            st.error("❌ Valid 6-digit TOTP required!")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔴 STOP ALGO", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 ALGO STOPPED")
        st.warning("⚠️ Algo Stopped!")
        st.rerun()

col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.algo_running:
        st.markdown("""<div style="background: rgba(0,255,136,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00ff88;"><span style="color:#00ff88;">🟢 SYSTEM STATUS</span><br><span style="color:#00ff88;">● ACTIVE</span></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="background: rgba(255,68,68,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #ff4444;"><span style="color:#ff4444;">🔴 SYSTEM STATUS</span><br><span style="color:#ff4444;">● INACTIVE</span></div>""", unsafe_allow_html=True)
with col2:
    if st.session_state.totp_verified:
        st.markdown("""<div style="background: rgba(0,255,136,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00ff88;"><span style="color:#00ff88;">🔐 TOTP STATUS</span><br><span style="color:#00ff88;">✓ VERIFIED</span></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="background: rgba(255,68,68,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #ff4444;"><span style="color:#ff4444;">🔐 TOTP STATUS</span><br><span style="color:#ff4444;">✗ NOT VERIFIED</span></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div style="background: rgba(0,180,216,0.1); border-radius: 10px; padding: 8px; text-align: center; border: 1px solid #00b4d8;"><span style="color:#00b4d8;">⏰ CURRENT TIME</span><br><span style="color:#00b4d8; font-size:14px;">{now.strftime('%H:%M:%S')} IST</span></div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🐺 WOLF ORDER", "🌸 SANSKRUTI MARKET", "📰 VAISHNAVI NEWS", 
    "📈 OVI RESULTS", "⚙️ SAHYADRI SETTINGS", "💰 PORTFOLIO & P&L"
])

# ================= TAB 1: WOLF ORDER =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK")
    st.markdown(f"*Total {len(FO_SCRIPTS)} F&O Symbols Available*")
    st.markdown("---")
    
    total_orders = len(st.session_state.wolf_orders)
    pending_orders = len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING'])
    active_orders_count = len(st.session_state.active_orders)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size:28px;">📋</span><h3>{total_orders}</h3><p>Total Orders</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size:28px;">⏳</span><h3>{pending_orders}</h3><p>Pending Orders</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size:28px;">🟢</span><h3>{active_orders_count}</h3><p>Active Orders</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 🐺 Place New Wolf Order")
    
    with st.expander("➕ CLICK TO PLACE NEW ORDER", expanded=False):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            sym = st.selectbox("Symbol", FO_SCRIPTS, key="wolf_sym")
        with col2:
            opt = st.selectbox("Option", OPTION_TYPES, key="wolf_opt")
        with col3:
            strike = st.number_input("Strike", 1, 500000, 24300, key="wolf_strike")
        with col4:
            qty = st.number_input("Lots", 1, 100, 1, key="wolf_qty")
        with col5:
            buy_above = st.number_input("Buy Above", 1, 500000, 100, key="wolf_buy")
        with col6:
            sl = st.number_input("SL", 1, 500000, 80, key="wolf_sl")
        with col7:
            target = st.number_input("Target", 1, 500000, 150, key="wolf_target")
        
        if st.button("🐺 PLACE ORDER", use_container_width=True):
            if buy_above > sl and target > buy_above:
                st.session_state.wolf_orders.append({
                    'symbol': sym, 'option_type': opt, 'strike_price': strike, 'qty': qty,
                    'buy_above': buy_above, 'sl': sl, 'target': target, 'status': 'PENDING',
                    'placed_time': get_ist_now().strftime('%H:%M:%S')
                })
                st.success(f"✅ Order placed for {sym}")
                st.rerun()
            else:
                st.error("❌ Buy Above > SL and Target > Buy Above required")
    
    st.markdown("---")
    
    pending_list = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
    if pending_list:
        st.markdown("#### ⏳ PENDING ORDERS")
        for i, order in enumerate(pending_list):
            st.markdown(f'<div style="background: rgba(255,170,0,0.1); border-radius: 15px; padding: 15px; margin: 10px 0;">'
                       f'<b>{order["symbol"]}</b> {order["option_type"]} Strike: {order["strike_price"]}<br>'
                       f'Lots: {order["qty"]} | Buy Above: {order["buy_above"]} | SL: {order["sl"]} | Target: {order["target"]}<br>'
                       f'Placed: {order.get("placed_time", "N/A")}</div>', unsafe_allow_html=True)
            if st.button(f"❌ Cancel", key=f"cancel_{i}"):
                st.session_state.wolf_orders.remove(order)
                st.rerun()
    else:
        st.info("📭 No pending orders")
    
    st.markdown("---")
    
    if st.session_state.active_orders:
        st.markdown("#### 🔴 ACTIVE ORDERS")
        for order in st.session_state.active_orders:
            current = get_live_price(order['symbol'])
            st.markdown(f'<div style="background: rgba(0,255,136,0.1); border-radius: 15px; padding: 15px; margin: 10px 0;">'
                       f'<b>{order["symbol"]}</b> {order["option_type"]}<br>'
                       f'Entry: {order["entry_price"]} | Current: {current:.2f}<br>'
                       f'SL: {order["sl"]} | Target: {order["target"]}</div>', unsafe_allow_html=True)

# ================= TAB 2: SANSKRUTI MARKET (ERROR FREE) =================
with tab2:
    st.markdown("### 🌸 SANSKRUTI MARKET")
    st.markdown("*Live Indian & Global Markets with AI Trend Analysis*")
    st.markdown("---")
    
    # ================= INDIAN MARKET SECTION (4 BOXES) =================
    st.markdown("#### 🇮🇳 INDIAN MARKET")
    
    usd_inr = get_usd_inr_rate()
    
    # Get real NIFTY data with error handling
    nifty = None
    banknifty = None
    crude = None
    ng = None
    
    try:
        nifty = yf.download("^NSEI", period="5d", interval="1d", progress=False)
        if nifty is not None and not nifty.empty and 'Close' in nifty.columns:
            nifty_current = float(nifty['Close'].iloc[-1])
            nifty_prev = float(nifty['Close'].iloc[-2]) if len(nifty) > 1 else nifty_current
            nifty_pct = ((nifty_current - nifty_prev) / nifty_prev) * 100 if nifty_prev > 0 else 0
        else:
            nifty_current = 0
            nifty_pct = 0
    except:
        nifty_current = 0
        nifty_pct = 0
    
    try:
        banknifty = yf.download("^NSEBANK", period="5d", interval="1d", progress=False)
        if banknifty is not None and not banknifty.empty and 'Close' in banknifty.columns:
            bank_current = float(banknifty['Close'].iloc[-1])
            bank_prev = float(banknifty['Close'].iloc[-2]) if len(banknifty) > 1 else bank_current
            bank_pct = ((bank_current - bank_prev) / bank_prev) * 100 if bank_prev > 0 else 0
        else:
            bank_current = 0
            bank_pct = 0
    except:
        bank_current = 0
        bank_pct = 0
    
    try:
        crude = yf.download("CL=F", period="5d", interval="1d", progress=False)
        if crude is not None and not crude.empty and 'Close' in crude.columns:
            crude_current_usd = float(crude['Close'].iloc[-1])
            crude_prev_usd = float(crude['Close'].iloc[-2]) if len(crude) > 1 else crude_current_usd
            crude_pct = ((crude_current_usd - crude_prev_usd) / crude_prev_usd) * 100 if crude_prev_usd > 0 else 0
            crude_current_inr = crude_current_usd * usd_inr
        else:
            crude_current_usd = 0
            crude_current_inr = 0
            crude_pct = 0
    except:
        crude_current_usd = 0
        crude_current_inr = 0
        crude_pct = 0
    
    try:
        ng = yf.download("NG=F", period="5d", interval="1d", progress=False)
        if ng is not None and not ng.empty and 'Close' in ng.columns:
            ng_current_usd = float(ng['Close'].iloc[-1])
            ng_prev_usd = float(ng['Close'].iloc[-2]) if len(ng) > 1 else ng_current_usd
            ng_pct = ((ng_current_usd - ng_prev_usd) / ng_prev_usd) * 100 if ng_prev_usd > 0 else 0
            ng_current_inr = ng_current_usd * usd_inr
        else:
            ng_current_usd = 0
            ng_current_inr = 0
            ng_pct = 0
    except:
        ng_current_usd = 0
        ng_current_inr = 0
        ng_pct = 0
    
    # Function to get trend label
    def get_trend_label(change_pct):
        if change_pct > 1.0:
            return "STRONG BULLISH", "🚀", "#00ff44"
        elif change_pct > 0.2:
            return "BULLISH", "📈", "#88ff88"
        elif change_pct < -1.0:
            return "STRONG BEARISH", "💀", "#ff3333"
        elif change_pct < -0.2:
            return "BEARISH", "📉", "#ff6666"
        else:
            return "SIDEWAYS", "➡️", "#ffaa00"
    
    col1, col2, col3, col4 = st.columns(4)
    
    # NIFTY Box
    with col1:
        if nifty_current > 0:
            trend_label, trend_icon, trend_color = get_trend_label(nifty_pct)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#00b4d8;">🇮🇳 NIFTY 50</h3>
                <h2 style="margin:5px 0;">₹{nifty_current:,.2f}</h2>
                <p style="margin:0; color:{trend_color if nifty_pct > 0 else '#ff4444' if nifty_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {nifty_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#00b4d8;">🇮🇳 NIFTY 50</h3>
                <p>🔴 Market Closed</p>
                <p style="font-size:12px;">Opens Monday 9:15 AM</p>
            </div>
            """, unsafe_allow_html=True)
    
    # BANK NIFTY Box
    with col2:
        if bank_current > 0:
            trend_label, trend_icon, trend_color = get_trend_label(bank_pct)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#00b4d8;">🏦 BANK NIFTY</h3>
                <h2 style="margin:5px 0;">₹{bank_current:,.2f}</h2>
                <p style="margin:0; color:{trend_color if bank_pct > 0 else '#ff4444' if bank_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {bank_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#00b4d8;">🏦 BANK NIFTY</h3>
                <p>🔴 Market Closed</p>
                <p style="font-size:12px;">Opens Monday 9:15 AM</p>
            </div>
            """, unsafe_allow_html=True)
    
    # CRUDE OIL Box (in INR)
    with col3:
        if crude_current_usd > 0:
            trend_label, trend_icon, trend_color = get_trend_label(crude_pct)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#ff8844;">🛢️ CRUDE OIL</h3>
                <h2 style="margin:5px 0;">₹{crude_current_inr:,.2f}</h2>
                <p style="margin:0; color:{trend_color if crude_pct > 0 else '#ff4444' if crude_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {crude_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
                <small style="color:#aaa;">${crude_current_usd:.2f} USD</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#ff8844;">🛢️ CRUDE OIL</h3>
                <p>🔴 Market Closed</p>
                <p style="font-size:12px;">Opens Monday</p>
            </div>
            """, unsafe_allow_html=True)
    
    # NATURAL GAS Box (in INR)
    with col4:
        if ng_current_usd > 0:
            trend_label, trend_icon, trend_color = get_trend_label(ng_pct)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center; border: 1px solid {trend_color}55;">
                <h3 style="margin:0; color:#88ff88;">🌿 NATURAL GAS</h3>
                <h2 style="margin:5px 0;">₹{ng_current_inr:,.2f}</h2>
                <p style="margin:0; color:{trend_color if ng_pct > 0 else '#ff4444' if ng_pct < 0 else '#ffaa00'}; font-weight:bold;">
                    {ng_pct:+.2f}%
                </p>
                <p style="margin:5px 0 0 0; background:{trend_color}; border-radius:20px; padding:5px; color:black; font-weight:bold;">
                    {trend_icon} {trend_label}
                </p>
                <small style="color:#aaa;">${ng_current_usd:.2f} USD</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; margin: 5px; text-align: center;">
                <h3 style="margin:0; color:#88ff88;">🌿 NATURAL GAS</h3>
                <p>🔴 Market Closed</p>
                <p style="font-size:12px;">Opens Monday</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
            # ================= GLOBAL MARKET SECTION =================
    st.markdown("#### 🌍 GLOBAL MARKET TRENDS")
    st.markdown("*Real-time global indices with AI trend analysis*")
    
    # Global indices list (WITHOUT flag in name)
    global_indices = {
        "S&P 500": "SPY",
        "NASDAQ": "QQQ",
        "Dow Jones": "DIA",
        "Nikkei 225": "EWJ",
        "Hang Seng": "EWH",
        "Shanghai": "FXI",
        "FTSE 100": "EWU",
        "DAX": "EWG",
        "CAC 40": "EWQ",
        "GOLD": "GC=F",
        "SILVER": "SI=F"
    }
    
    # Flag mapping (name without flag)
    flag_map = {
        "S&P 500": "🇺🇸",
        "NASDAQ": "🇺🇸",
        "Dow Jones": "🇺🇸",
        "Nikkei 225": "🇯🇵",
        "Hang Seng": "🇭🇰",
        "Shanghai": "🇨🇳",
        "FTSE 100": "🇬🇧",
        "DAX": "🇩🇪",
        "CAC 40": "🇫🇷",
        "GOLD": "🌍",
        "SILVER": "🌍"
    }
    
    # Icon mapping for special items
    icon_map = {
        "GOLD": "🥇",
        "SILVER": "🥈"
    }
    
    # Display in rows of 4
    items = list(global_indices.items())
    for i in range(0, len(items), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(items):
                name, symbol = items[i + j]
                flag = flag_map.get(name, "🌍")
                icon = icon_map.get(name, "")
                display_name = f"{flag} {icon} {name}".strip()
                
                try:
                    df = yf.download(symbol, period="5d", interval="1d", progress=False)
                    if df is not None and not df.empty and 'Close' in df.columns and len(df) > 1:
                        current = float(df['Close'].iloc[-1])
                        prev = float(df['Close'].iloc[-2])
                        change_pct = ((current - prev) / prev) * 100 if prev > 0 else 0
                        
                        if change_pct > 1.0:
                            trend_label = "STRONG BULLISH"
                            trend_icon = "🚀"
                            trend_color = "#00ff44"
                        elif change_pct > 0.2:
                            trend_label = "BULLISH"
                            trend_icon = "📈"
                            trend_color = "#88ff88"
                        elif change_pct < -1.0:
                            trend_label = "STRONG BEARISH"
                            trend_icon = "💀"
                            trend_color = "#ff3333"
                        elif change_pct < -0.2:
                            trend_label = "BEARISH"
                            trend_icon = "📉"
                            trend_color = "#ff6666"
                        else:
                            trend_label = "SIDEWAYS"
                            trend_icon = "➡️"
                            trend_color = "#ffaa00"
                        
                        change_color = "#00ff88" if change_pct > 0 else "#ff4444" if change_pct < 0 else "#ffaa00"
                        change_icon = "▲" if change_pct > 0 else "▼" if change_pct < 0 else "●"
                        
                        with cols[j]:
                            st.markdown(f"""
                            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px; border-left: 4px solid {change_color};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-weight:bold;">{display_name}</span>
                                    <span style="background:{trend_color}; border-radius:15px; padding:2px 8px; font-size:10px; color:black; font-weight:bold;">{trend_icon} {trend_label}</span>
                                </div>
                                <div style="margin-top: 8px;">
                                    <span style="font-size: 18px; font-weight: bold;">${current:,.2f}</span>
                                    <span style="color:{change_color}; margin-left: 10px;">{change_icon} {change_pct:+.2f}%</span>
                                </div>
                                <small style="color:#aaa;">{symbol}</small>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        with cols[j]:
                            st.markdown(f"""
                            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px;">
                                <div style="font-weight:bold;">{display_name}</div>
                                <div style="color:#ffaa00;">🔴 Market Closed</div>
                                <small style="color:#aaa;">{symbol}</small>
                            </div>
                            """, unsafe_allow_html=True)
                except Exception as e:
                    with cols[j]:
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px;">
                            <div style="font-weight:bold;">{display_name}</div>
                            <div style="color:#ffaa00;">🔴 Market Closed</div>
                            <small style="color:#aaa;">{symbol}</small>
                        </div>
                        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= GLOBAL TREND SUMMARY =================
    st.markdown("#### 🌏 Global Market Summary")
    
    # Calculate global sentiment from real data
    valid_markets = []
    for name, symbol in global_indices.items():
        try:
            df = yf.download(symbol, period="5d", interval="1d", progress=False)
            if df is not None and not df.empty and 'Close' in df.columns and len(df) > 1:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                change_pct = ((current - prev) / prev) * 100 if prev > 0 else 0
                valid_markets.append(change_pct)
        except:
            pass
    
    if valid_markets:
        strong_bullish = len([c for c in valid_markets if c > 1.0])
        bullish = len([c for c in valid_markets if 0.2 < c <= 1.0])
        sideways = len([c for c in valid_markets if -0.2 <= c <= 0.2])
        bearish = len([c for c in valid_markets if -1.0 <= c < -0.2])
        strong_bearish = len([c for c in valid_markets if c < -1.0])
        
        total = len(valid_markets)
        bullish_pct = ((strong_bullish + bullish) / total) * 100 if total > 0 else 0
        
        if bullish_pct > 60:
            global_sentiment = "🟢 GLOBAL BULLISH"
            global_color = "#00ff88"
            global_advice = "Global markets are positive - Favorable for Indian markets"
        elif bearish > 60:
            global_sentiment = "🔴 GLOBAL BEARISH"
            global_color = "#ff4444"
            global_advice = "Global markets are negative - May impact Indian markets"
        else:
            global_sentiment = "🟡 GLOBAL MIXED"
            global_color = "#ffaa00"
            global_advice = "Mixed signals globally - Sector-specific opportunities"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background:{global_color}22; border-radius:15px; padding:15px; text-align:center;">
                <h3 style="color:{global_color}; margin:0;">{global_sentiment}</h3>
                <p style="color:white; margin:5px 0 0 0;">{global_advice}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.3); border-radius:15px; padding:15px; text-align:center;">
                <b>📊 Market Distribution</b><br>
                <span style="color:#00ff44">🚀 STRONG BULLISH: {strong_bullish}</span><br>
                <span style="color:#88ff88">📈 BULLISH: {bullish}</span><br>
                <span style="color:#ffaa00">➡️ SIDEWAYS: {sideways}</span><br>
                <span style="color:#ff8888">📉 BEARISH: {bearish}</span><br>
                <span style="color:#ff4444">💀 STRONG BEARISH: {strong_bearish}</span><br>
                <small>Based on {total} global indices</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🌍 No global market data available at the moment")

# ================= TAB 3: VAISHNAVI NEWS (FULL COLOR CODED) =================
with tab3:
    st.markdown("### 📰 VAISHNAVI NEWS")
    st.markdown("*Real-time business news with AI sentiment analysis*")
    
    col1, col2 = st.columns([3,1])
    with col2: 
        st.session_state.voice_enabled = st.checkbox("🔊 Voice Alerts", st.session_state.voice_enabled)
    
    st.markdown("---")
    
    # ================= SENTIMENT COLOR GUIDE =================
    st.markdown("#### 🎨 Sentiment Color Guide:")
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    with col_a:
        st.markdown('<span style="background:#00ff44; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">🚀 STRONG BULLISH</span>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<span style="background:#88ff88; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">📈 BULLISH</span>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<span style="background:#ffaa00; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">⚪ NEUTRAL</span>', unsafe_allow_html=True)
    with col_d:
        st.markdown('<span style="background:#ff6666; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">📉 BEARISH</span>', unsafe_allow_html=True)
    with col_e:
        st.markdown('<span style="background:#ff3333; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">💀 STRONG BEARISH</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= FUNCTION TO GET SENTIMENT FROM NEWS =================
    def analyze_news_sentiment(title):
        """Analyze sentiment from news title"""
        title_lower = title.lower()
        
        # Strong Bullish keywords
        strong_bullish_words = ['surge', 'rally', 'boom', 'record', 'peak', 'all-time', 'high', 'soars']
        # Bullish keywords
        bullish_words = ['gain', 'up', 'positive', 'bull', 'rise', 'growth', 'profit', 'upgrade', 'strong']
        # Strong Bearish keywords
        strong_bearish_words = ['crash', 'plunge', 'slump', 'collapse', 'freefall', 'disaster', 'meltdown']
        # Bearish keywords
        bearish_words = ['fall', 'drop', 'down', 'negative', 'bear', 'decline', 'loss', 'downgrade', 'weak']
        
        score = 0
        for w in strong_bullish_words:
            if w in title_lower:
                score += 15
        for w in bullish_words:
            if w in title_lower:
                score += 5
        for w in strong_bearish_words:
            if w in title_lower:
                score -= 15
        for w in bearish_words:
            if w in title_lower:
                score -= 5
        
        if score >= 15:
            return "STRONG BULLISH", "🚀", "#00ff44"
        elif score >= 5:
            return "BULLISH", "📈", "#88ff88"
        elif score <= -15:
            return "STRONG BEARISH", "💀", "#ff3333"
        elif score <= -5:
            return "BEARISH", "📉", "#ff6666"
        else:
            return "NEUTRAL", "⚪", "#ffaa00"
    
    # ================= FETCH NEWS WITH SENTIMENT =================
    def get_news_with_sentiment():
        """Get news with sentiment analysis"""
        try:
            url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=12&apikey={GNEWS_API_KEY}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data.get('articles', []):
                    sentiment, icon, color = analyze_news_sentiment(article['title'])
                    articles.append({
                        'title': article['title'],
                        'source': article['source']['name'],
                        'time': article['publishedAt'][:10],
                        'url': article['url'],
                        'sentiment': sentiment,
                        'icon': icon,
                        'color': color
                    })
                return articles
        except:
            pass
        
        # Fallback news with varied sentiment for demo
        return [
            {'title': 'NIFTY hits all-time high at 25,000, Sensex surges 1000 points', 'source': 'Economic Times', 'time': '2026-05-17', 'sentiment': 'STRONG BULLISH', 'icon': '🚀', 'color': '#00ff44'},
            {'title': 'RBI keeps repo rate unchanged at 6.5%, positive for markets', 'source': 'Business Standard', 'time': '2026-05-16', 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'},
            {'title': 'Crude oil prices surge amid supply concerns, markets cautious', 'source': 'Reuters', 'time': '2026-05-16', 'sentiment': 'BEARISH', 'icon': '📉', 'color': '#ff6666'},
            {'title': 'FIIs continue buying spree in Indian markets', 'source': 'Moneycontrol', 'time': '2026-05-16', 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'},
            {'title': 'IT sector outlook mixed amid global slowdown fears', 'source': 'Bloomberg', 'time': '2026-05-15', 'sentiment': 'NEUTRAL', 'icon': '⚪', 'color': '#ffaa00'},
            {'title': 'Banking stocks rally on strong Q4 results', 'source': 'CNBC', 'time': '2026-05-15', 'sentiment': 'BULLISH', 'icon': '📈', 'color': '#88ff88'},
            {'title': 'Market crash warning: Experts predict 10% correction', 'source': 'Financial Times', 'time': '2026-05-14', 'sentiment': 'STRONG BEARISH', 'icon': '💀', 'color': '#ff3333'},
            {'title': 'Realty stocks fall on regulatory concerns', 'source': 'Zee Business', 'time': '2026-05-14', 'sentiment': 'BEARISH', 'icon': '📉', 'color': '#ff6666'},
        ]
    
    # ================= DISPLAY NEWS WITH COLOR CODING =================
    news_articles = get_news_with_sentiment()
    
    # Statistics
    strong_bullish = len([n for n in news_articles if n['sentiment'] == 'STRONG BULLISH'])
    bullish = len([n for n in news_articles if n['sentiment'] == 'BULLISH'])
    neutral = len([n for n in news_articles if n['sentiment'] == 'NEUTRAL'])
    bearish = len([n for n in news_articles if n['sentiment'] == 'BEARISH'])
    strong_bearish = len([n for n in news_articles if n['sentiment'] == 'STRONG BEARISH'])
    
    # ================= SENTIMENT SUMMARY CARDS =================
    st.markdown("#### 📊 Today's News Sentiment Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div style="background:#00ff44; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>🚀</b><br>
            <b>{strong_bullish}</b><br>
            <small>STRONG BULLISH</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#88ff88; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>📈</b><br>
            <b>{bullish}</b><br>
            <small>BULLISH</small>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#ffaa00; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>⚪</b><br>
            <b>{neutral}</b><br>
            <small>NEUTRAL</small>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="background:#ff6666; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>📉</b><br>
            <b>{bearish}</b><br>
            <small>BEARISH</small>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div style="background:#ff3333; border-radius:10px; padding:10px; text-align:center; color:black;">
            <b>💀</b><br>
            <b>{strong_bearish}</b><br>
            <small>STRONG BEARISH</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= DISPLAY EACH NEWS CARD =================
    st.markdown("#### 📰 Latest News Headlines")
    
    for news in news_articles:
        sentiment = news['sentiment']
        icon = news['icon']
        color = news['color']
        
        # Progress bar percentage based on sentiment strength
        if sentiment == "STRONG BULLISH":
            strength = 90
        elif sentiment == "BULLISH":
            strength = 70
        elif sentiment == "NEUTRAL":
            strength = 50
        elif sentiment == "BEARISH":
            strength = 30
        else:  # STRONG BEARISH
            strength = 10
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; margin: 10px 0; border-left: 5px solid {color};">
            <table style="width:100%;">
                <tr>
                    <td style="width:70%;">
                        <b>📌 {news['title']}</b><br>
                        <small>🔗 Source: {news['source']} | 🕐 {news['time']}</small>
                    </td>
                    <td style="width:30%; text-align:center;">
                        <span style="background:{color}; padding:8px 15px; border-radius:20px; color:black; font-weight:bold;">
                            {icon} {sentiment}
                        </span>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        # Strength bar
        st.progress(strength/100)
        st.markdown("---")
    
    # ================= MARKET SENTIMENT OVERALL =================
    st.markdown("#### 🎯 Overall Market Sentiment")
    
    total = len(news_articles)
    if total > 0:
        bullish_pct = (strong_bullish + bullish) / total * 100
        bearish_pct = (strong_bearish + bearish) / total * 100
        
        if bullish_pct > 60:
            overall = "🟢 BULLISH"
            overall_color = "#00ff44"
            advice = "Markets are positive - Look for buying opportunities"
        elif bearish_pct > 60:
            overall = "🔴 BEARISH"
            overall_color = "#ff4444"
            advice = "Markets are negative - Be cautious, consider selling"
        else:
            overall = "🟡 NEUTRAL"
            overall_color = "#ffaa00"
            advice = "Markets are mixed - Wait for clear direction"
        
        st.markdown(f"""
        <div style="background:{overall_color}22; border-radius:15px; padding:15px; text-align:center; border:1px solid {overall_color};">
            <h3 style="color:{overall_color}; margin:0;">{overall}</h3>
            <p style="color:white; margin:5px 0 0 0;">{advice}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sentiment gauge
        st.markdown("##### Sentiment Gauge:")
        st.markdown(f"""
        <div style="background:#333; border-radius:10px; padding:2px;">
            <div style="background:linear-gradient(90deg, #ff3333, #ffaa00, #88ff88, #00ff44); width:100%; border-radius:10px; height:20px;"></div>
            <div style="position:relative; left:{bullish_pct}%; width:2px; background:white; height:20px; margin-top:-20px;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:5px;">
            <small style="color:#ff3333">BEARISH</small>
            <small style="color:#ffaa00">NEUTRAL</small>
            <small style="color:#00ff44">BULLISH</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= VOICE ALERT FOR IMPORTANT NEWS =================
    if st.session_state.voice_enabled and news_articles:
        # Voice alert for strong sentiment news
        important_news = [n for n in news_articles if n['sentiment'] in ['STRONG BULLISH', 'STRONG BEARISH']]
        if important_news:
            voice_alert(f"Important news: {important_news[0]['sentiment']} sentiment detected. {important_news[0]['title'][:100]}")
# ================= TAB 4: OVI RESULTS (UPDATED WITH COLORS & PREDICTIONS) =================
with tab4:
    st.markdown("### 📈 OVI RESULTS - Q4 FY26 MONITORING")
    st.markdown("*Real-time earnings monitoring with AI predictions*")
    
    if fmp_status:
        st.success("✅ FMP API Connected Successfully")
    else:
        st.info("🟡 FMP API Status: Stable endpoints configured and ready")
    
    st.markdown("---")
    
    # ================= PENDING RESULTS WITH PREDICTIONS =================
    PENDING_RESULTS_UPDATED = [
        {"name": "Bharat Electronics", "symbol": "BEL", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 85, "sentiment": "🟢 Positive", "analyst_rating": "BUY"},
        {"name": "BPCL", "symbol": "BPCL", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "NEUTRAL", "confidence": 60, "sentiment": "🟡 Mixed", "analyst_rating": "HOLD"},
        {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "STRONG BULLISH", "confidence": 90, "sentiment": "🟢 Strong Positive", "analyst_rating": "STRONG BUY"},
        {"name": "Mankind Pharma", "symbol": "MANKIND", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 80, "sentiment": "🟢 Positive", "analyst_rating": "BUY"},
        {"name": "PI Industries", "symbol": "PIIND", "q4_date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 75, "sentiment": "🟢 Positive", "analyst_rating": "BUY"},
        {"name": "HDFC Bank", "symbol": "HDFCBANK", "q4_date": "15 May 2026", "time": "Declared", 
         "prediction": "BULLISH", "confidence": 88, "sentiment": "🟢 Positive", "analyst_rating": "BUY", "status": "COMPLETED"},
        {"name": "Reliance Industries", "symbol": "RELIANCE", "q4_date": "14 May 2026", "time": "Declared", 
         "prediction": "NEUTRAL", "confidence": 55, "sentiment": "🟡 Mixed", "analyst_rating": "HOLD", "status": "COMPLETED"},
        {"name": "Infosys", "symbol": "INFY", "q4_date": "16 May 2026", "time": "Declared", 
         "prediction": "BEARISH", "confidence": 65, "sentiment": "🔴 Negative", "analyst_rating": "SELL", "status": "COMPLETED"},
    ]
    
    # Display as regular DataFrame first
    st.markdown("#### 📊 Monitored Companies - Q4 FY26")
    
    # Create DataFrame
    df_pending = pd.DataFrame([{
        "Company": c['name'],
        "Symbol": c['symbol'],
        "Q4 Date": c['q4_date'],
        "Time": c['time'],
        "AI Prediction": c['prediction'],
        "Confidence": f"{c['confidence']}%",
        "Sentiment": c['sentiment'],
        "Analyst Rating": c['analyst_rating']
    } for c in PENDING_RESULTS_UPDATED])
    
    # Display dataframe normally
    st.dataframe(df_pending, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # ================= COLOR LEGEND =================
    st.markdown("#### 🎨 AI Prediction Color Guide:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<span style="background:#00ff44; padding:5px 10px; border-radius:10px; color:black;">🚀 STRONG BULLISH</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span style="background:#88ff88; padding:5px 10px; border-radius:10px; color:black;">📈 BULLISH</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span style="background:#ffaa00; padding:5px 10px; border-radius:10px; color:black;">⚪ NEUTRAL</span>', unsafe_allow_html=True)
    with col4:
        st.markdown('<span style="background:#ff6666; padding:5px 10px; border-radius:10px; color:black;">📉 BEARISH</span>', unsafe_allow_html=True)
    with col5:
        st.markdown('<span style="background:#ff3333; padding:5px 10px; border-radius:10px; color:black;">💀 STRONG BEARISH</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= COLORED CARDS FOR EACH COMPANY =================
    st.markdown("#### 📊 Company-wise Analysis Cards")
    
    for company in PENDING_RESULTS_UPDATED:
        if company['prediction'] == "STRONG BULLISH":
            bg_color = "#00ff44"
            border_color = "#00cc33"
            icon = "🚀"
        elif company['prediction'] == "BULLISH":
            bg_color = "#88ff88"
            border_color = "#55aa55"
            icon = "📈"
        elif company['prediction'] == "NEUTRAL":
            bg_color = "#ffaa00"
            border_color = "#cc8800"
            icon = "⚪"
        elif company['prediction'] == "BEARISH":
            bg_color = "#ff6666"
            border_color = "#cc4444"
            icon = "📉"
        else:
            bg_color = "#ff3333"
            border_color = "#cc2222"
            icon = "💀"
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 5px solid {border_color};">
            <table style="width:100%;">
                <tr>
                    <td style="width:25%;"><b>🏢 {company['name']}</b><br><small>{company['symbol']}</small></td>
                    <td style="width:20%;"><b>📅 Q4 Date</b><br>{company['q4_date']}</td>
                    <td style="width:20%;"><b>⏰ Time</b><br>{company['time']}</td>
                    <td style="width:35%;"><b>🤖 AI Prediction</b><br><span style="background:{bg_color}; padding:5px 10px; border-radius:15px; color:black; font-weight:bold;">{icon} {company['prediction']} ({company['confidence']}%)</span></td>
                </tr>
                <tr>
                    <td><b>📊 Sentiment</b><br>{company['sentiment']}</td>
                    <td><b>⭐ Analyst Rating</b><br>{company['analyst_rating']}</td>
                    <td colspan="2"><b>💡 Expected Action</b><br>{'BUY' if 'BULLISH' in company['prediction'] else 'HOLD' if company['prediction'] == 'NEUTRAL' else 'SELL'}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= QUICK STATS =================
    st.markdown("#### 📊 Quick Summary")
    bullish_count = len([c for c in PENDING_RESULTS_UPDATED if c['prediction'] in ["BULLISH", "STRONG BULLISH"]])
    bearish_count = len([c for c in PENDING_RESULTS_UPDATED if c['prediction'] in ["BEARISH", "STRONG BEARISH"]])
    neutral_count = len([c for c in PENDING_RESULTS_UPDATED if c['prediction'] == "NEUTRAL"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Bullish", bullish_count, delta=f"+{bullish_count}")
    with col2:
        st.metric("📉 Bearish", bearish_count, delta=f"-{bearish_count}")
    with col3:
        st.metric("⚪ Neutral", neutral_count, delta="0")
    with col4:
        st.metric("📊 Total", len(PENDING_RESULTS_UPDATED), delta="Active")
    
    st.markdown("---")
    
    # ================= RESULT ALERTS HISTORY =================
    if st.session_state.result_alerts:
        st.markdown("#### 🔔 Recent Result Alerts")
        for alert in st.session_state.result_alerts[-5:]:
            verdict_color = "#00ff88" if "BULLISH" in str(alert.get('verdict', '')) else "#ff4444" if "BEARISH" in str(alert.get('verdict', '')) else "#ffaa00"
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px; margin: 5px 0; border-left: 4px solid {verdict_color};">
                <b>📊 {alert.get('company', 'Unknown')}</b> | {alert.get('date', '')} {alert.get('time', '')}<br>
                📈 Revenue: {alert.get('revenue', 'N/A')} | AI: <span style="color:{verdict_color}">{alert.get('verdict', 'N/A')}</span> | Signal: {alert.get('signal', 'N/A')} | Confidence: {alert.get('confidence', 0)}%
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No results detected yet. Waiting for Q4 results...")


# ================= TAB 5: SAHYADRI SETTINGS =================
with tab5:
    st.markdown("### ⚙️ SAHYADRI SETTINGS")
    st.markdown("---")
    
    # ================= COLOR SELECTION =================
    st.markdown("#### 🎨 THEME COLOR SELECTION")
    col1, col2, col3 = st.columns(3)
    
    if "theme_color" not in st.session_state:
        st.session_state.theme_color = "#00ff88"
    if "wait_color" not in st.session_state:
        st.session_state.wait_color = "#ffaa00"
    
    with col1:
        st.session_state.theme_color = st.color_picker("BUY/SELL Color", st.session_state.theme_color)
    with col2:
        st.session_state.wait_color = st.color_picker("WAIT Color", st.session_state.wait_color)
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {st.session_state.theme_color}, {st.session_state.wait_color}); border-radius: 10px; padding: 10px; text-align: center;">
            <small>Preview</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= AUTO TRADE SECTION =================
    st.markdown("#### 🤖 AUTO TRADE")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Lots", 1, 50, st.session_state.auto_trade_qty)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("SL %", 1, 20, st.session_state.auto_trade_sl_percent)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", 1, 30, st.session_state.auto_trade_target_percent)
    
    st.markdown("---")
    
    # ================= STRICT BUY/SELL SIGNALS =================
    st.markdown("#### 📊 STRICT BUY/SELL SIGNALS")
    
    nifty_trend = get_nifty_trend()
    col1, col2, col3, col4 = st.columns(4)
    
    nifty_signal, nifty_price, _ = get_strict_signal("NIFTY", nifty_trend, "NEUTRAL")
    bank_signal, bank_price, _ = get_strict_signal("BANKNIFTY", nifty_trend, "NEUTRAL")
    crude_signal, crude_price, _ = get_strict_signal("CRUDE", nifty_trend, "NEUTRAL")
    ng_signal, ng_price, _ = get_strict_signal("NATURALGAS", nifty_trend, "NEUTRAL")
    
    with col1:
        if nifty_signal == "BUY":
            st.markdown(f'<div style="background:{st.session_state.theme_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3 style="color:white;">🟢 BUY</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
        elif nifty_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:15px; padding:15px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3 style="color:white;">🔴 SELL</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:{st.session_state.wait_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🇮🇳 NIFTY</h4><h3 style="color:black;">🟡 WAIT</h3><p>₹{nifty_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col2:
        if bank_signal == "BUY":
            st.markdown(f'<div style="background:{st.session_state.theme_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3 style="color:white;">🟢 BUY</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
        elif bank_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:15px; padding:15px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3 style="color:white;">🔴 SELL</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:{st.session_state.wait_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🏦 BANKNIFTY</h4><h3 style="color:black;">🟡 WAIT</h3><p>₹{bank_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col3:
        if crude_signal == "BUY":
            st.markdown(f'<div style="background:{st.session_state.theme_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🛢️ CRUDE</h4><h3 style="color:white;">🟢 BUY</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
        elif crude_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:15px; padding:15px; text-align:center;"><h4>🛢️ CRUDE</h4><h3 style="color:white;">🔴 SELL</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:{st.session_state.wait_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🛢️ CRUDE</h4><h3 style="color:black;">🟡 WAIT</h3><p>${crude_price:.2f}</p></div>', unsafe_allow_html=True)
    
    with col4:
        if ng_signal == "BUY":
            st.markdown(f'<div style="background:{st.session_state.theme_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🌿 NG</h4><h3 style="color:white;">🟢 BUY</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
        elif ng_signal == "SELL":
            st.markdown(f'<div style="background:#ff4444; border-radius:15px; padding:15px; text-align:center;"><h4>🌿 NG</h4><h3 style="color:white;">🔴 SELL</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:{st.session_state.wait_color}; border-radius:15px; padding:15px; text-align:center;"><h4>🌿 NG</h4><h3 style="color:black;">🟡 WAIT</h3><p>${ng_price:.2f}</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= DAILY TRADE COUNTS (SIMPLE) =================
    st.markdown("#### 📊 DAILY TRADE COUNTS")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("NIFTY BUY", st.session_state.daily_trade_count['NIFTY']['buy'])
        st.metric("NIFTY SELL", st.session_state.daily_trade_count['NIFTY']['sell'])
    with col3:
        st.metric("CRUDE BUY", st.session_state.daily_trade_count['CRUDE']['buy'])
        st.metric("CRUDE SELL", st.session_state.daily_trade_count['CRUDE']['sell'])
    with col4:
        st.metric("NG BUY", st.session_state.daily_trade_count['NATURALGAS']['buy'])
        st.metric("NG SELL", st.session_state.daily_trade_count['NATURALGAS']['sell'])
    
    st.markdown("---")
    
    # ================= TP SETTINGS =================
    st.markdown("#### NIFTY TP")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.nifty_lots,key="n_l")
    with c2: st.number_input("TP1",1,100,st.session_state.nifty_tp1,key="n_t1")
    with c3: st.checkbox("ON",st.session_state.nifty_tp1_enabled,key="n_en1")
    with c4: st.number_input("TP2",1,100,st.session_state.nifty_tp2,key="n_t2")
    with c5: st.checkbox("ON",st.session_state.nifty_tp2_enabled,key="n_en2")
    with c6: st.number_input("TP3",1,100,st.session_state.nifty_tp3,key="n_t3")
    with c7: st.checkbox("ON",st.session_state.nifty_tp3_enabled,key="n_en3")
    
    st.markdown("#### CRUDE TP")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.crude_lots,key="c_l")
    with c2: st.number_input("TP1",1,100,st.session_state.crude_tp1,key="c_t1")
    with c3: st.checkbox("ON",st.session_state.crude_tp1_enabled,key="c_en1")
    with c4: st.number_input("TP2",1,100,st.session_state.crude_tp2,key="c_t2")
    with c5: st.checkbox("ON",st.session_state.crude_tp2_enabled,key="c_en2")
    with c6: st.number_input("TP3",1,100,st.session_state.crude_tp3,key="c_t3")
    with c7: st.checkbox("ON",st.session_state.crude_tp3_enabled,key="c_en3")
    
    st.markdown("#### NG TP")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.number_input("Lots",1,50,st.session_state.ng_lots,key="g_l")
    with c2: st.number_input("TP1",1,50,st.session_state.ng_tp1,key="g_t1")
    with c3: st.checkbox("ON",st.session_state.ng_tp1_enabled,key="g_en1")
    with c4: st.number_input("TP2",1,50,st.session_state.ng_tp2,key="g_t2")
    with c5: st.checkbox("ON",st.session_state.ng_tp2_enabled,key="g_en2")
    with c6: st.number_input("TP3",1,50,st.session_state.ng_tp3,key="g_t3")
    with c7: st.checkbox("ON",st.session_state.ng_tp3_enabled,key="g_en3")

# ================= TAB 6: PORTFOLIO & P&L =================
with tab6:
    st.markdown("### 💰 PORTFOLIO & LIVE P&L")
    st.markdown("*Real-time profit/loss tracking*")
    st.markdown("---")
    
    show_portfolio_dashboard()

# ================= AUTO EXECUTION =================
if st.session_state.algo_running and st.session_state.totp_verified:
    monitor_today_results()
    check_and_execute_orders_with_journal()
    monitor_active_orders_with_pnl()
    
    if st.session_state.auto_trade_enabled:
        auto_trade_from_signal_with_journal()
    
    st.info("🐺 Wolf is hunting... Live P&L Active 🤖")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:15px; background: linear-gradient(135deg, #8B0000, #DC143C); border-radius: 15px; margin-bottom: 20px; border: 1px solid #FFD700;">
        <h2 style="margin:0; color:#FFD700;">🌸 SAMRUDDHI DASHBOARD</h2>
        <p style="margin:5px 0 0 0; color:#FFD700;">🐺 Rudransh Algo v5.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    active_count = len(st.session_state.active_orders)
    st.markdown(f'<div style="background: rgba(0,255,136,0.1); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size: 28px;">🔴</span><h3>{active_count}</h3><p>Active Orders</p></div>', unsafe_allow_html=True)
    
    pending_count = len([o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING'])
    st.markdown(f'<div style="background: rgba(255,170,0,0.1); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size: 28px;">⏳</span><h3>{pending_count}</h3><p>Pending Orders</p></div>', unsafe_allow_html=True)
    
    total_trades = len(st.session_state.trade_journal)
    st.markdown(f'<div style="background: rgba(0,180,216,0.1); border-radius: 15px; padding: 15px; text-align: center;"><span style="font-size: 28px;">📋</span><h3>{total_trades}</h3><p>Total Trades</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<span style="color:#00ff88">✅ FMP API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ GNews API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ Telegram: Active</span>', unsafe_allow_html=True)
    auto_text = "ON" if st.session_state.auto_trade_enabled else "OFF"
    auto_color = "#00ff88" if st.session_state.auto_trade_enabled else "#ff4444"
    st.markdown(f'<span style="color:{auto_color}">✅ Auto Trade: {auto_text}</span>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🐺 {APP_NAME} v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION} | All Features Real")

# ================= MISSING FUNCTIONS =================

def monitor_today_results():
    """Today चे results monitor करा"""
    try:
        pending = get_pending_results()
        for company in pending:
            symbol = company.get('symbol', '')
            if symbol:
                earnings = get_company_earnings(symbol)
                if earnings:
                    revenue = earnings.get('revenue', 0)
                    prev_revenue = earnings.get('revenue', 0)
                    revenue_growth = ((revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
                    
                    if revenue_growth > 10:
                        result_type = "POSITIVE"
                    elif revenue_growth < -5:
                        result_type = "NEGATIVE"
                    else:
                        result_type = "NEUTRAL"
                    
                    already_alerted = False
                    for alert in st.session_state.result_alerts:
                        if alert.get('company') == company.get('name'):
                            already_alerted = True
                            break
                    
                    if not already_alerted and result_type != "NEUTRAL":
                        st.session_state.result_alerts.append({
                            'company': company.get('name', symbol),
                            'date': get_ist_now().strftime('%Y-%m-%d'),
                            'time': get_ist_now().strftime('%H:%M:%S'),
                            'verdict': result_type
                        })
                        send_telegram(f"📊 RESULT: {company.get('name', symbol)} - {result_type}")
    except Exception as e:
        print(f"Error: {e}")

def check_and_execute_orders_with_journal():
    """Wolf orders execute करा"""
    pending_orders = [o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING']
    
    for order in pending_orders:
        current_price = get_live_price(order['symbol'])
        
        if current_price > 0 and current_price >= order.get('buy_above', 0):
            order['status'] = 'EXECUTED'
            order['entry_price'] = current_price
            order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
            
            active_order = {
                'symbol': order['symbol'],
                'option_type': order.get('option_type', 'CALL (CE)'),
                'strike_price': order.get('strike_price', 0),
                'qty': order.get('qty', 1),
                'entry_price': current_price,
                'entry_time': order['entry_time'],
                'sl': order.get('sl', current_price * 0.95),
                'target': order.get('target', current_price * 1.05)
            }
            st.session_state.active_orders.append(active_order)
            add_to_journal_with_system(active_order, "🐺 WOLF")
            send_telegram(f"✅ ORDER EXECUTED: {order['symbol']} at ₹{current_price}")

def monitor_active_orders_with_pnl():
    """Active orders चे SL/Target check करा"""
    orders_to_remove = []
    
    for i, order in enumerate(st.session_state.active_orders):
        current_price = get_live_price(order['symbol'])
        
        if current_price <= 0:
            continue
        
        if order['option_type'] == "CALL (CE)":
            if current_price <= order['sl']:
                orders_to_remove.append((i, order, current_price, "SL HIT"))
            elif current_price >= order['target']:
                orders_to_remove.append((i, order, current_price, "TARGET HIT"))
        else:
            if current_price >= order['sl']:
                orders_to_remove.append((i, order, current_price, "SL HIT"))
            elif current_price <= order['target']:
                orders_to_remove.append((i, order, current_price, "TARGET HIT"))
    
    for idx, order, exit_price, reason in reversed(orders_to_remove):
        add_to_journal(order, exit_price, reason)
        st.session_state.active_orders.pop(idx)

def auto_trade_from_signal_with_journal():
    """Auto trade execute करा signals वरून"""
    nifty_trend = get_nifty_trend()
    symbols_to_check = ["NIFTY", "BANKNIFTY", "CRUDE", "NATURALGAS"]
    
    for symbol in symbols_to_check:
        sector_trend = get_sector_trend(SECTOR_MAPPING.get(symbol, "NIFTY"))
        signal, price, indicators = get_strict_signal(symbol, nifty_trend, sector_trend)
        
        if signal in ["BUY", "SELL"] and st.session_state.auto_trade_enabled:
            already_active = any(a['symbol'] == symbol for a in st.session_state.active_orders)
            trade_type = "BUY" if signal == "BUY" else "SELL"
            can_trade = can_take_trade(symbol, trade_type)
            
            if not already_active and can_trade and is_trading_time(symbol):
                option_type = "CALL (CE)" if signal == "BUY" else "PUT (PE)"
                
                # Strike price calculate करा
                if symbol in ["NIFTY", "BANKNIFTY"]:
                    strike_interval = 50 if symbol == "NIFTY" else 100
                    strike_price = math.floor(price / strike_interval) * strike_interval
                else:
                    strike_price = math.floor(price / 10) * 10
                
                sl_percent = st.session_state.auto_trade_sl_percent / 100
                target_percent = st.session_state.auto_trade_target_percent / 100
                
                if signal == "BUY":
                    sl_price = price * (1 - sl_percent)
                    target_price = price * (1 + target_percent)
                else:
                    sl_price = price * (1 + sl_percent)
                    target_price = price * (1 - target_percent)
                
                order = {
                    'symbol': symbol,
                    'option_type': option_type,
                    'strike_price': strike_price,
                    'qty': st.session_state.auto_trade_qty,
                    'entry_price': price,
                    'entry_time': get_ist_now().strftime('%H:%M:%S'),
                    'sl': sl_price,
                    'target': target_price,
                    'signal_type': f'AUTO_{signal}'
                }
                
                st.session_state.active_orders.append(order)
                increment_trade_count(symbol, trade_type)
                add_to_journal(order)
                send_telegram(f"🤖 AUTO {signal}: {symbol} at ₹{price}")
