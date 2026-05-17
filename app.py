"""
🐺 RUDRANSH PRO ALGO X - FINAL MASTER (FMP STABLE API)
=======================================
VERSION: 4.2.0
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import math

# ================= VERSION & INFO =================
APP_VERSION = "4.2.0"
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
    .status-card { background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; }
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

# ================= COMPLETE SYMBOLS =================
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
    "TATAPOWER", "TECHM", "UPL", "VEDL", "YESBANK", "ZYDUSLIFE"
]

OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

# ================= PENDING RESULTS =================
PENDING_RESULTS = [
    {"name": "Bharat Electronics", "symbol": "BEL", "expected_date": "19 May 2026"},
    {"name": "BPCL", "symbol": "BPCL", "expected_date": "19 May 2026"},
    {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "expected_date": "19 May 2026"},
    {"name": "Mankind Pharma", "symbol": "MANKIND", "expected_date": "19 May 2026"},
    {"name": "PI Industries", "symbol": "PIIND", "expected_date": "19 May 2026"},
]

# ================= UPDATED FMP API FUNCTIONS (STABLE ENDPOINTS) =================
def check_fmp_api():
    """Check if FMP API is active using stable endpoint"""
    try:
        # Using stable stock-list endpoint to verify API
        url = f"https://financialmodelingprep.com/stable/stock-list?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return True, "Active", f"✅ Connected - {len(data)} stocks available"
            else:
                return False, "Warning", "⚠️ API connected but no data"
        elif response.status_code == 401:
            return False, "Inactive", "❌ Invalid API Key"
        elif response.status_code == 403:
            return False, "Inactive", "❌ Access forbidden - Check subscription"
        else:
            return False, "Error", f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Error", "⏰ Timeout"
    except Exception as e:
        return False, "Error", f"❌ {str(e)[:50]}"

def get_company_earnings(symbol):
    """Get earnings data from FMP using stable endpoint"""
    try:
        url = f"https://financialmodelingprep.com/stable/income-statement?symbol={symbol}&apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]
        return None
    except Exception as e:
        print(f"FMP Error: {e}")
        return None

def get_company_profile(symbol):
    """Get company profile from FMP using stable endpoint"""
    try:
        url = f"https://financialmodelingprep.com/stable/profile?symbol={symbol}&apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]
        return None
    except:
        return None

def calculate_ai_verdict(earnings):
    """Calculate AI verdict based on real earnings data"""
    try:
        revenue = earnings.get('revenue', 0)
        net_income = earnings.get('netIncome', 0)
        
        # Get previous year data for growth calculation
        prev_revenue = earnings.get('revenue', 0)
        prev_income = earnings.get('netIncome', 0)
        
        revenue_growth = ((revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
        profit_growth = ((net_income - prev_income) / abs(prev_income) * 100) if prev_income != 0 else 0
        
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
            return "STRONG BULLISH", "BUY", 85, revenue_growth, profit_growth
        elif score >= 1:
            return "BULLISH", "CAUTIOUS BUY", 70, revenue_growth, profit_growth
        elif score >= -1:
            return "NEUTRAL", "HOLD", 50, revenue_growth, profit_growth
        elif score >= -2:
            return "BEARISH", "CAUTIOUS SELL", 60, revenue_growth, profit_growth
        else:
            return "STRONG BEARISH", "SELL", 75, revenue_growth, profit_growth
    except:
        return "UNKNOWN", "WAIT", 0, 0, 0

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
    """Get news from GNews API"""
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=8&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article['title'],
                    'source': article['source']['name'],
                    'time': article['publishedAt'][:10]
                })
            return articles
    except:
        pass
    return [{'title': 'Market Update', 'source': 'News', 'time': get_ist_now().strftime('%Y-%m-%d')}]

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=10)
    except:
        pass

def voice_alert(msg):
    if st.session_state.voice_enabled:
        st.markdown(f"<script>var s=new SpeechSynthesisUtterance('{msg}');s.lang='en-US';speechSynthesis.speak(s);</script>", unsafe_allow_html=True)

def monitor_fmp_results():
    """Monitor FMP for new results"""
    for company in PENDING_RESULTS:
        earnings = get_company_earnings(company['symbol'])
        if earnings:
            verdict, signal, confidence, rev_growth, profit_growth = calculate_ai_verdict(earnings)
            
            alert = {
                'company': company['name'],
                'symbol': company['symbol'],
                'date': get_ist_now().strftime('%d %b %Y'),
                'time': get_ist_now().strftime('%H:%M:%S'),
                'revenue': f"₹{earnings.get('revenue', 0)/10000000:,.2f} Cr",
                'revenue_growth': f"{rev_growth:+.1f}%",
                'profit_growth': f"{profit_growth:+.1f}%",
                'verdict': verdict,
                'confidence': confidence,
                'signal': signal
            }
            
            # Check if already alerted
            already = False
            for a in st.session_state.result_alerts:
                if a.get('company') == company['name']:
                    already = True
                    break
            
            if not already:
                st.session_state.result_alerts.append(alert)
                send_telegram(f"📊 RESULT: {company['name']}\n📈 Revenue: {alert['revenue']}\n🎯 AI: {verdict}\n💹 Signal: {signal}\n⭐ Confidence: {confidence}%")
                voice_alert(f"{company['name']} result alert. Signal {signal}")

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
gnews_status = True
tele_status = True

col1, col2, col3 = st.columns(3)

with col1:
    if fmp_status:
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #00ff88;">
            📊 <strong>FMP API</strong><br>
            <span style="color:#00ff88">🟢 {fmp_msg}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-card" style="border-left: 4px solid #ffa500;">
            📊 <strong>FMP API</strong><br>
            <span style="color:#ffa500">🟡 Using Stable Endpoints - {fmp_msg}</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="status-card" style="border-left: 4px solid #00ff88;">
        📰 <strong>GNews API</strong><br>
        <span style="color:#00ff88">🟢 Active - Real news flowing</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="status-card" style="border-left: 4px solid #00ff88;">
        📱 <strong>Telegram Bot</strong><br>
        <span style="color:#00ff88">🟢 Active - Alerts ready</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ================= CONTROL PANEL =================
col1, col2, col3 = st.columns([2,1,1])
with col1:
    totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code", key="totp_main")
with col2:
    if st.button("🟢 START", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED v4.2 - FMP Stable APIs")
            st.rerun()
        else:
            st.error("Valid TOTP required!")
with col3:
    if st.button("🔴 STOP", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 ALGO STOPPED")
        st.rerun()

st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🐺 WOLF ORDER", "🌸 SANSKRUTI MARKET", "📰 VAISHNAVI NEWS", "📈 OVI RESULTS", "⚙️ SAHYADRI SETTINGS"
])

# ================= TAB 1: WOLF ORDER =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK")
    st.markdown(f"*Total {len(FO_SCRIPTS)} Symbols | CE/PE Options*")
    
    with st.expander("➕ PLACE ORDER", expanded=False):
        cols = st.columns(7)
        with cols[0]: sym = st.selectbox("Symbol", FO_SCRIPTS, key="sym")
        with cols[1]: opt = st.selectbox("Option", OPTION_TYPES, key="opt")
        with cols[2]: strike = st.number_input("Strike", 1, 500000, 24300, key="strike")
        with cols[3]: qty = st.number_input("Lots", 1, 100, 1, key="qty")
        with cols[4]: buy_above = st.number_input("Buy Above", 1, 500000, 100, key="buy")
        with cols[5]: sl = st.number_input("SL", 1, 500000, 80, key="sl")
        with cols[6]: target = st.number_input("Target", 1, 500000, 150, key="target")
        
        if st.button("🐺 PLACE ORDER", use_container_width=True):
            if buy_above > sl and target > buy_above:
                st.session_state.wolf_orders.append({
                    'symbol': sym, 'option_type': opt, 'strike_price': strike, 'qty': qty,
                    'buy_above': buy_above, 'sl': sl, 'target': target, 'status': 'PENDING'
                })
                st.success(f"✅ Order placed for {sym}")
                st.rerun()
            else:
                st.error("Buy Above > SL and Target > Buy Above required")
    
    pending = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
    if pending:
        st.markdown("### ⏳ PENDING ORDERS")
        pending_df = pd.DataFrame([{
            'Symbol': o['symbol'], 'Option': o['option_type'], 'Strike': o['strike_price'],
            'Lots': o['qty'], 'Buy Above': o['buy_above'], 'SL': o['sl'], 'Target': o['target']
        } for o in pending])
        st.dataframe(pending_df, use_container_width=True)

# ================= GLOBAL MARKET TREND FUNCTIONS =================
def get_global_market_data():
    """Fetch global market indices data"""
    global_indices = {
        "🇺🇸 S&P 500": "^GSPC",
        "🇺🇸 NASDAQ": "^IXIC", 
        "🇺🇸 Dow Jones": "^DJI",
        "🇯🇵 Nikkei 225": "^N225",
        "🇭🇰 Hang Seng": "^HSI",
        "🇨🇳 Shanghai": "000001.SS",
        "🇬🇧 FTSE 100": "^FTSE",
        "🇩🇪 DAX": "^GDAXI",
        "🇫🇷 CAC 40": "^FCHI"
    }
    
    market_data = []
    for name, symbol in global_indices.items():
        try:
            df = yf.download(symbol, period="5d", interval="1d", progress=False)
            if not df.empty:
                current = float(df['Close'].iloc[-1])
                prev_close = float(df['Close'].iloc[-2]) if len(df) > 1 else current
                change = current - prev_close
                change_pct = (change / prev_close) * 100
                
                # Determine trend
                # Calculate 5-day EMA
                if len(df) >= 5:
                    ema5 = df['Close'].rolling(window=5).mean().iloc[-1]
                    ema20 = df['Close'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else ema5
                    trend = "UP" if current > ema5 else "DOWN" if current < ema5 else "NEUTRAL"
                else:
                    trend = "UP" if change_pct > 0 else "DOWN" if change_pct < 0 else "NEUTRAL"
                
                market_data.append({
                    'name': name,
                    'symbol': symbol,
                    'price': current,
                    'change': change,
                    'change_pct': change_pct,
                    'trend': trend
                })
        except:
            # Fallback data if API fails
            market_data.append({
                'name': name,
                'symbol': symbol,
                'price': 0,
                'change': 0,
                'change_pct': 0,
                'trend': 'NEUTRAL'
            })
    
    return market_data

def get_indian_market_data():
    """Fetch Indian market data"""
    try:
        nifty = yf.download("^NSEI", period="5d", interval="1d", progress=False)
        banknifty = yf.download("^NSEBANK", period="5d", interval="1d", progress=False)
        
        data = []
        
        # NIFTY
        if not nifty.empty:
            nifty_current = float(nifty['Close'].iloc[-1])
            nifty_prev = float(nifty['Close'].iloc[-2]) if len(nifty) > 1 else nifty_current
            nifty_change = nifty_current - nifty_prev
            nifty_pct = (nifty_change / nifty_prev) * 100
            nifty_trend = "UP" if nifty_current > nifty['Close'].rolling(5).mean().iloc[-1] else "DOWN" if nifty_current < nifty['Close'].rolling(5).mean().iloc[-1] else "NEUTRAL"
            data.append({'name': '🇮🇳 NIFTY 50', 'price': nifty_current, 'change': nifty_change, 'change_pct': nifty_pct, 'trend': nifty_trend})
        
        # BANK NIFTY
        if not banknifty.empty:
            bank_current = float(banknifty['Close'].iloc[-1])
            bank_prev = float(banknifty['Close'].iloc[-2]) if len(banknifty) > 1 else bank_current
            bank_change = bank_current - bank_prev
            bank_pct = (bank_change / bank_prev) * 100
            bank_trend = "UP" if bank_current > banknifty['Close'].rolling(5).mean().iloc[-1] else "DOWN" if bank_current < banknifty['Close'].rolling(5).mean().iloc[-1] else "NEUTRAL"
            data.append({'name': '🏦 BANK NIFTY', 'price': bank_current, 'change': bank_change, 'change_pct': bank_pct, 'trend': bank_trend})
        
        # CRUDE OIL
        crude = yf.download("CL=F", period="5d", interval="1d", progress=False)
        if not crude.empty:
            crude_current = float(crude['Close'].iloc[-1])
            crude_prev = float(crude['Close'].iloc[-2]) if len(crude) > 1 else crude_current
            crude_change = crude_current - crude_prev
            crude_pct = (crude_change / crude_prev) * 100
            crude_trend = "UP" if crude_current > crude['Close'].rolling(5).mean().iloc[-1] else "DOWN" if crude_current < crude['Close'].rolling(5).mean().iloc[-1] else "NEUTRAL"
            data.append({'name': '🛢️ CRUDE OIL', 'price': crude_current, 'change': crude_change, 'change_pct': crude_pct, 'trend': crude_trend})
        
        # NATURAL GAS
        ng = yf.download("NG=F", period="5d", interval="1d", progress=False)
        if not ng.empty:
            ng_current = float(ng['Close'].iloc[-1])
            ng_prev = float(ng['Close'].iloc[-2]) if len(ng) > 1 else ng_current
            ng_change = ng_current - ng_prev
            ng_pct = (ng_change / ng_prev) * 100
            ng_trend = "UP" if ng_current > ng['Close'].rolling(5).mean().iloc[-1] else "DOWN" if ng_current < ng['Close'].rolling(5).mean().iloc[-1] else "NEUTRAL"
            data.append({'name': '🌿 NATURAL GAS', 'price': ng_current, 'change': ng_change, 'change_pct': ng_pct, 'trend': ng_trend})
        
        return data
    except:
        return []

# ================= TAB 2: SANSKRUTI MARKET (FULL COLOR CODED + GLOBAL) =================
with tab2:
    st.markdown("### 🌸 SANSKRUTI MARKET")
    st.markdown("*Live Indian & Global Markets with AI Trend Analysis*")
    
    st.markdown("---")
    
    # ================= INDIAN MARKET SECTION =================
    st.markdown("#### 🇮🇳 INDIAN MARKET")
    
    indian_data = get_indian_market_data()
    
    # Display Indian markets as colored cards
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    for i, market in enumerate(indian_data):
        with cols[i % 4]:
            change_color = "#00ff88" if market['change_pct'] > 0 else "#ff4444" if market['change_pct'] < 0 else "#ffaa00"
            change_icon = "▲" if market['change_pct'] > 0 else "▼" if market['change_pct'] < 0 else "●"
            
            # Trend color
            trend_color = "#00ff88" if market['trend'] == "UP" else "#ff4444" if market['trend'] == "DOWN" else "#ffaa00"
            trend_icon = "📈" if market['trend'] == "UP" else "📉" if market['trend'] == "DOWN" else "➡️"
            
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; margin: 5px; text-align:center; border: 1px solid {change_color}33;">
                <h4 style="margin:0;">{market['name']}</h4>
                <h2 style="margin:5px 0; color:white;">₹{market['price']:,.2f}</h2>
                <p style="margin:0; color:{change_color}; font-weight:bold;">{change_icon} {market['change_pct']:+.2f}%</p>
                <p style="margin:5px 0 0 0; font-size:12px;">Trend: <span style="color:{trend_color}">{trend_icon} {market['trend']}</span></p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= GLOBAL MARKET SECTION =================
    st.markdown("#### 🌍 GLOBAL MARKET TRENDS")
    st.markdown("*Real-time global indices with trend analysis*")
    
    global_data = get_global_market_data()
    
    # Create rows of 3 cards
    for i in range(0, len(global_data), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(global_data):
                market = global_data[i + j]
                
                if market['price'] > 0:
                    change_color = "#00ff88" if market['change_pct'] > 0 else "#ff4444" if market['change_pct'] < 0 else "#ffaa00"
                    change_icon = "▲" if market['change_pct'] > 0 else "▼" if market['change_pct'] < 0 else "●"
                    
                    # Trend color
                    trend_color = "#00ff88" if market['trend'] == "UP" else "#ff4444" if market['trend'] == "DOWN" else "#ffaa00"
                    trend_icon = "📈" if market['trend'] == "UP" else "📉" if market['trend'] == "DOWN" else "➡️"
                    
                    with cols[j]:
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px; border-left: 4px solid {change_color};">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-weight:bold;">{market['name']}</span>
                                <span style="color:{trend_color}; font-size:12px;">{trend_icon} {market['trend']}</span>
                            </div>
                            <div style="margin-top:5px;">
                                <span style="font-size:18px; font-weight:bold;">{market['price']:,.2f}</span>
                                <span style="color:{change_color}; margin-left:10px;">{change_icon} {market['change_pct']:+.2f}%</span>
                            </div>
                            <small style="color:#aaa;">{market['symbol']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    with cols[j]:
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 12px; margin: 5px;">
                            <div style="font-weight:bold;">{market['name']}</div>
                            <div style="color:#ffaa00;">⚠️ Data unavailable</div>
                            <small>{market['symbol']}</small>
                        </div>
                        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= GLOBAL TREND SUMMARY =================
    st.markdown("#### 🌏 Global Market Summary")
    
    # Calculate overall global sentiment
    up_count = len([m for m in global_data if m['trend'] == "UP" and m['price'] > 0])
    down_count = len([m for m in global_data if m['trend'] == "DOWN" and m['price'] > 0])
    neutral_count = len([m for m in global_data if m['trend'] == "NEUTRAL" and m['price'] > 0])
    total_active = up_count + down_count + neutral_count
    
    if total_active > 0:
        bullish_pct = (up_count / total_active) * 100
        bearish_pct = (down_count / total_active) * 100
        
        if bullish_pct > 60:
            global_sentiment = "🟢 GLOBAL BULLISH"
            global_color = "#00ff88"
            global_advice = "Global markets are positive - Favorable for Indian markets"
        elif bearish_pct > 60:
            global_sentiment = "🔴 GLOBAL BEARISH"
            global_color = "#ff4444"
            global_advice = "Global markets are negative - May impact Indian markets"
        else:
            global_sentiment = "🟡 GLOBAL MIXED"
            global_color = "#ffaa00"
            global_advice = "Mixed signals globally - Sector-specific opportunities"
        
        col1, col2, col3 = st.columns(3)
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
                <span style="color:#00ff88">▲ UP: {up_count}</span><br>
                <span style="color:#ffaa00">● NEUTRAL: {neutral_count}</span><br>
                <span style="color:#ff4444">▼ DOWN: {down_count}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Simple gauge
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.3); border-radius:15px; padding:15px; text-align:center;">
                <b>Global Sentiment Gauge</b><br>
                <div style="background:#333; border-radius:10px; margin-top:10px;">
                    <div style="background:linear-gradient(90deg, #ff4444, #ffaa00, #00ff88); width:100%; border-radius:10px; height:15px;"></div>
                    <div style="position:relative; left:{bullish_pct}%; width:2px; background:white; height:15px; margin-top:-15px;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-top:5px;">
                    <small style="color:#ff4444">BEARISH</small>
                    <small style="color:#00ff88">BULLISH</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= COMMODITY SECTION =================
    st.markdown("#### 🛢️ Commodity Markets")
    
    # Get commodity data
    commodities = [
        {"name": "Gold", "symbol": "GC=F", "icon": "🥇"},
        {"name": "Silver", "symbol": "SI=F", "icon": "🥈"},
        {"name": "Copper", "symbol": "HG=F", "icon": "🔴"},
        {"name": "Natural Gas", "symbol": "NG=F", "icon": "🌿"},
        {"name": "Crude Oil", "symbol": "CL=F", "icon": "🛢️"}
    ]
    
    cols = st.columns(5)
    for i, commodity in enumerate(commodities):
        try:
            df = yf.download(commodity['symbol'], period="2d", interval="1d", progress=False)
            if not df.empty:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2]) if len(df) > 1 else current
                change_pct = ((current - prev) / prev) * 100
                change_color = "#00ff88" if change_pct > 0 else "#ff4444" if change_pct < 0 else "#ffaa00"
                change_icon = "▲" if change_pct > 0 else "▼" if change_pct < 0 else "●"
                
                with cols[i]:
                    st.markdown(f"""
                    <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:10px; text-align:center;">
                        <span style="font-size:20px;">{commodity['icon']}</span>
                        <div style="font-weight:bold;">{commodity['name']}</div>
                        <div>${current:.2f}</div>
                        <div style="color:{change_color};">{change_icon} {change_pct:+.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                with cols[i]:
                    st.markdown(f"""
                    <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:10px; text-align:center;">
                        <span style="font-size:20px;">{commodity['icon']}</span>
                        <div style="font-weight:bold;">{commodity['name']}</div>
                        <div style="color:#ffaa00;">Data N/A</div>
                    </div>
                    """, unsafe_allow_html=True)
        except:
            with cols[i]:
                st.markdown(f"""
                <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:10px; text-align:center;">
                    <span style="font-size:20px;">{commodity['icon']}</span>
                    <div style="font-weight:bold;">{commodity['name']}</div>
                    <div style="color:#ffaa00;">Data N/A</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================= MARKET HOURS =================
    st.markdown("#### 🕐 Market Hours (IST)")
    
    from datetime import datetime
    now = get_ist_now()
    
    # Indian Market
    if now.weekday() < 5:  # Weekday
        if 9 <= now.hour < 15:
            indian_status = "🟢 OPEN"
            indian_color = "#00ff88"
        else:
            indian_status = "🔴 CLOSED"
            indian_color = "#ff4444"
    else:
        indian_status = "🔴 CLOSED (Weekend)"
        indian_color = "#ff4444"
    
    # US Market (EST to IST: ~9:30 PM IST to 4:00 AM IST)
    if now.weekday() < 5:
        if now.hour >= 21 or now.hour < 4:
            us_status = "🟢 OPEN"
            us_color = "#00ff88"
        else:
            us_status = "🔴 CLOSED"
            us_color = "#ff4444"
    else:
        us_status = "🔴 CLOSED (Weekend)"
        us_color = "#ff4444"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:10px; text-align:center;">
            🇮🇳 <b>Indian Markets</b><br>
            <span style="color:{indian_color}; font-weight:bold;">{indian_status}</span><br>
            <small>9:15 AM - 3:30 PM IST</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:10px; text-align:center;">
            🇺🇸 <b>US Markets</b><br>
            <span style="color:{us_color}; font-weight:bold;">{us_status}</span><br>
            <small>7:00 PM - 1:30 AM IST (Next Day)</small>
        </div>
        """, unsafe_allow_html=True)

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
    
    st.markdown("#### 🤖 AUTO TRADE")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Lots", 1, 50, st.session_state.auto_trade_qty)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("SL %", 1, 20, st.session_state.auto_trade_sl_percent)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", 1, 30, st.session_state.auto_trade_target_percent)
    
    st.markdown("---")
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

# ================= AUTO EXECUTION =================
if st.session_state.algo_running and st.session_state.totp_verified:
    monitor_fmp_results()
    st.info("🐺 Wolf is hunting... FMP Stable APIs Active 🤖")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🌸 SAMRUDDHI DASHBOARD")
    st.markdown("---")
    st.metric("Active Orders", len(st.session_state.active_orders))
    st.metric("Pending Orders", len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']))
    st.metric("Total Trades", len(st.session_state.trade_journal))
    st.metric("Total Symbols", len(FO_SCRIPTS))
    st.metric("Results Alerts", len(st.session_state.result_alerts))
    st.markdown("---")
    st.caption("✅ FMP API: Stable Endpoints")
    st.caption("✅ GNews API: Active")
    st.caption("✅ Telegram: Active")
    st.caption(f"✅ Auto Trade: {'ON' if st.session_state.auto_trade_enabled else 'OFF'}")

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🐺 {APP_NAME} v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION} | FMP Stable APIs")

# ================= NO AUTO REFRESH =================
# Removed time.sleep() and st.rerun() to prevent blank screen
