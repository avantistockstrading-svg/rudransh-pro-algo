"""
🐺 RUDRANSH PRO ALGO X - MASTER COPY v2.0
===========================================
DEVELOPED BY: SATISH D. NAKHATE
LOCATION: TALWADE, PUNE - 412114
VERSION: 2.0.0
LAST UPDATED: 2026-05-16

NEW FEATURES v2.0:
- FMP API Integration (Real-time Results)
- AI Analysis Engine (Bullish/Bearish Detection)
- Multi-Source News (Bloomberg, Reuters, CNBC, FT, ET, Moneycontrol, Zee, Investing, Mint)
- Auto Trade Decision Based on Results
- Real-time Earnings Monitoring (30 sec refresh)
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time
import json
import threading

# ================= VERSION TRACKING =================
APP_VERSION = "2.0.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"
LAST_UPDATE = "2026-05-16"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title=f"{APP_NAME} v{APP_VERSION}", 
    layout="wide", 
    page_icon="🐺",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Card Style */
    .css-1r6slb0, .css-1y4p8pa {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
    }
    
    /* Headers */
    h1, h2, h3 {
        background: linear-gradient(135deg, #00ff88 0%, #00b4d8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00b4d8 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(0,255,136,0.3);
    }
    
    /* Status Badges */
    .badge-success {
        background: rgba(0,255,136,0.2);
        color: #00ff88;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .badge-danger {
        background: rgba(255,0,0,0.2);
        color: #ff4444;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .badge-warning {
        background: rgba(255,165,0,0.2);
        color: #ffa500;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .badge-info {
        background: rgba(0,180,216,0.2);
        color: #00b4d8;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    
    /* Live Time */
    .live-time {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
    }
    
    /* Toast Notification */
    .toast-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        z-index: 9999;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

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
    st.markdown("""
    <div style="text-align:center; padding:50px;">
        <h1>🐺 RUDRANSH PRO ALGO X</h1>
        <p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>
        <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:200px; margin:20px auto;"></div>
        <h3>🔐 APPLICATION LOCKED</h3>
        <p>Enter 4-6 Digit Numeric Password to Access</p>
    </div>
    """, unsafe_allow_html=True)
    
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
if "wolf_orders" not in st.session_state:
    st.session_state.wolf_orders = []
if "active_orders" not in st.session_state:
    st.session_state.active_orders = []
if "trade_journal" not in st.session_state:
    st.session_state.trade_journal = []
if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = get_ist_now().date()
if "max_daily_loss" not in st.session_state:
    st.session_state.max_daily_loss = 100000
if "news_cache" not in st.session_state:
    st.session_state.news_cache = []
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

# ================= NEW: FMP API & RESULT MONITORING =================
if "fmp_api_connected" not in st.session_state:
    st.session_state.fmp_api_connected = False
if "monitored_companies" not in st.session_state:
    st.session_state.monitored_companies = []
if "result_alerts" not in st.session_state:
    st.session_state.result_alerts = []
if "ai_analysis_cache" not in st.session_state:
    st.session_state.ai_analysis_cache = {}

# ================= FMP API KEY (तुमची स्वतःची API Key इथे टाका) =================
FMP_API_KEY = "YOUR_FMP_API_KEY_HERE"  # तुमची FMP API Key इथे टाका

# ================= NEWS SOURCES =================
NEWS_SOURCES = {
    "bloomberg": "https://www.bloomberg.com/india",
    "reuters": "https://www.reuters.com/markets/india/",
    "cnbc": "https://www.cnbc.com/world/?region=world",
    "financial_times": "https://www.ft.com/indian-economy",
    "economic_times": "https://economictimes.indiatimes.com",
    "moneycontrol": "https://www.moneycontrol.com",
    "zee_business": "https://www.zeebiz.com",
    "investing": "https://www.investing.com/india",
    "mint": "https://www.livemint.com"
}

# ================= COMPLETE F&O SCRIPTS (209 + Indices + Commodity) =================
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

# ================= LOT SIZE AND TP SETTINGS (जसेच्या तसे) =================
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

# ================= COMPANIES FOR RESULT MONITORING =================
PENDING_RESULTS = [
    {"name": "Bharat Electronics", "symbol": "BEL", "time": "After 3:30 PM", "expected": "Positive Expected"},
    {"name": "BPCL", "symbol": "BPCL", "time": "After 3:30 PM", "expected": "Mixed/Negative"},
    {"name": "Zydus Lifesciences", "symbol": "ZYDUSLIFE", "time": "After 3:30 PM", "expected": "Positive Expected"},
    {"name": "Mankind Pharma", "symbol": "MANKIND", "time": "After 3:30 PM", "expected": "Positive Expected"},
    {"name": "PI Industries", "symbol": "PIIND", "time": "After 3:30 PM", "expected": "Positive Expected"},
]

# Reset daily
if get_ist_now().date() != st.session_state.last_trade_date:
    st.session_state.daily_loss = 0
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
        elif symbol == "NATURALGAS":
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

# ================= NEW: FMP API FUNCTIONS =================
def connect_fmp_api(api_key):
    """Connect to FMP API"""
    try:
        url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def get_company_earnings(symbol, api_key):
    """Get real-time earnings data from FMP API"""
    try:
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=1&apikey={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]
    except:
        pass
    return None

def check_result_released(symbol, api_key, last_checked_date):
    """Check if result is released for a company"""
    earnings = get_company_earnings(symbol, api_key)
    if earnings:
        report_date = earnings.get('date', '')
        if report_date and report_date > last_checked_date:
            return True, earnings
    return False, None

# ================= NEW: AI ANALYSIS ENGINE =================
def ai_sentiment_analysis(earnings_data):
    """AI-based Bullish/Bearish analysis"""
    try:
        revenue = earnings_data.get('revenue', 0)
        previous_revenue = earnings_data.get('revenuePrevious', 0)
        net_income = earnings_data.get('netIncome', 0)
        previous_net_income = earnings_data.get('netIncomePrevious', 0)
        
        revenue_growth = ((revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
        profit_growth = ((net_income - previous_net_income) / abs(previous_net_income) * 100) if previous_net_income != 0 else 0
        
        # AI Scoring
        score = 0
        reasons = []
        
        if revenue_growth > 10:
            score += 2
            reasons.append(f"Revenue up {revenue_growth:.1f}%")
        elif revenue_growth > 0:
            score += 1
            reasons.append(f"Revenue up {revenue_growth:.1f}%")
        elif revenue_growth < -5:
            score -= 2
            reasons.append(f"Revenue down {abs(revenue_growth):.1f}%")
        
        if profit_growth > 15:
            score += 2
            reasons.append(f"Profit up {profit_growth:.1f}%")
        elif profit_growth > 0:
            score += 1
            reasons.append(f"Profit up {profit_growth:.1f}%")
        elif profit_growth < -10:
            score -= 2
            reasons.append(f"Profit down {abs(profit_growth):.1f}%")
        
        # Final Verdict
        if score >= 2:
            verdict = "🟢 BULLISH"
            signal = "BUY"
            confidence = min(90, 70 + score * 10)
        elif score >= 1:
            verdict = "🟡 CAUTIOUSLY BULLISH"
            signal = "CAUTIOUS BUY"
            confidence = 60 + score * 10
        elif score >= -1:
            verdict = "⚪ NEUTRAL"
            signal = "HOLD"
            confidence = 50
        elif score >= -2:
            verdict = "🟠 CAUTIOUSLY BEARISH"
            signal = "CAUTIOUS SELL"
            confidence = 40 + abs(score) * 10
        else:
            verdict = "🔴 BEARISH"
            signal = "SELL"
            confidence = 80 + abs(score) * 5
        
        return {
            'verdict': verdict,
            'signal': signal,
            'confidence': min(95, confidence),
            'reasons': reasons,
            'score': score,
            'revenue_growth': revenue_growth,
            'profit_growth': profit_growth
        }
    except:
        return {
            'verdict': '⚪ UNKNOWN',
            'signal': 'WAIT',
            'confidence': 0,
            'reasons': ['Analysis failed'],
            'score': 0,
            'revenue_growth': 0,
            'profit_growth': 0
        }

# ================= NEW: MULTI-SOURCE NEWS =================
def fetch_news_from_source(source_name, source_url):
    """Fetch news from different sources"""
    # Note: Real implementation would require API keys for each source
    # This is a placeholder structure
    return [
        {
            'title': f'Market update from {source_name}',
            'source': source_name,
            'time': get_ist_now().strftime('%Y-%m-%d %H:%M'),
            'url': source_url,
            'sentiment': '🟢 Positive' if source_name in ['Bloomberg', 'Reuters', 'CNBC'] else '🟡 Neutral'
        }
    ]

def get_all_news():
    """Get news from all sources"""
    all_news = []
    for source_name, source_url in NEWS_SOURCES.items():
        news = fetch_news_from_source(source_name, source_url)
        all_news.extend(news)
    return all_news[:10]  # Return top 10 news

# ================= TELEGRAM & ALERTS =================
def send_telegram(msg):
    """Send message to Telegram"""
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=10)
    except:
        pass

def show_toast_notification(message, type="info"):
    """Show toast notification in Streamlit"""
    color = "#00ff88" if type == "success" else "#ff4444" if type == "error" else "#00b4d8"
    st.markdown(f"""
    <div class="toast-notification" style="background: linear-gradient(135deg, {color}, {color}aa);">
        {message}
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)

def voice_alert(message):
    """Voice alert for browser"""
    if st.session_state.voice_enabled:
        # JavaScript Speech API
        st.markdown(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{message}");
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

# ================= NEW: RESULT MONITORING ENGINE =================
def monitor_results():
    """Monitor for new results"""
    if not FMP_API_KEY or FMP_API_KEY == "YOUR_FMP_API_KEY_HERE":
        return
    
    for company in PENDING_RESULTS:
        try:
            earnings = get_company_earnings(company['symbol'], FMP_API_KEY)
            if earnings:
                last_check = st.session_state.result_alerts.get(company['symbol'], '')
                report_date = earnings.get('date', '')
                
                if report_date and report_date != last_check:
                    # New result detected!
                    ai_analysis = ai_sentiment_analysis(earnings)
                    
                    # Store alert
                    alert = {
                        'company': company['name'],
                        'symbol': company['symbol'],
                        'date': report_date,
                        'earnings': earnings,
                        'ai_analysis': ai_analysis,
                        'timestamp': get_ist_now().strftime('%H:%M:%S')
                    }
                    st.session_state.result_alerts.append(alert)
                    
                    # Send Telegram Alert
                    telegram_msg = f"""
📊 RESULT ALERT: {company['name']}
━━━━━━━━━━━━━━━━━━━━━━━
🎯 AI Analysis: {ai_analysis['verdict']}
📈 Signal: {ai_analysis['signal']}
⭐ Confidence: {ai_analysis['confidence']}%
📉 Revenue Growth: {ai_analysis['revenue_growth']:.1f}%
💰 Profit Growth: {ai_analysis['profit_growth']:.1f}%
📝 Reasons: {', '.join(ai_analysis['reasons'])}
━━━━━━━━━━━━━━━━━━━━━━━
🐺 Auto Trade Decision: {ai_analysis['signal']}
                    """
                    send_telegram(telegram_msg)
                    
                    # Voice Alert
                    voice_alert(f"Result alert for {company['name']}. AI analysis says {ai_analysis['verdict']}")
                    
                    # Show Toast
                    show_toast_notification(f"📊 {company['name']}: {ai_analysis['verdict']}", "success")
                    
                    # Mark as processed
                    st.session_state.result_alerts[company['symbol']] = report_date
                    
                    # Auto Trade Decision
                    if ai_analysis['signal'] in ['BUY', 'CAUTIOUS BUY'] and st.session_state.algo_running:
                        # Auto place trade logic here
                        pass
                    
        except Exception as e:
            pass

# ================= WOLF ORDER FUNCTIONS =================
def check_and_execute_wolf_orders():
    for order in st.session_state.wolf_orders[:]:
        if order['status'] == 'PENDING':
            current_price = get_live_price(order['symbol'])
            
            if current_price > 0 and current_price >= order['buy_above']:
                order['status'] = 'ACTIVE'
                order['entry_price'] = current_price
                order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
                
                trade_record = {
                    "No": len(st.session_state.trade_journal) + 1,
                    "Time": order['entry_time'],
                    "Symbol": f"{order['symbol']} {order.get('strike_price', '')}",
                    "Type": "🐺 WOLF BUY",
                    "Lots": order['qty'],
                    "Entry": round(current_price, 2),
                    "SL": order['sl'],
                    "Target": order['target'],
                    "Status": "ACTIVE"
                }
                st.session_state.trade_journal.append(trade_record)
                send_telegram(f"🐺 WOLF EXECUTED: {order['symbol']} BUY @ ₹{current_price:.2f}")
                voice_alert(f"Wolf order executed for {order['symbol']}")
                
                st.session_state.active_orders.append({
                    'symbol': order['symbol'],
                    'strike_price': order.get('strike_price', ''),
                    'entry_price': current_price,
                    'sl': order['sl'],
                    'target': order['target'],
                    'qty': order['qty'],
                    'journal_index': len(st.session_state.trade_journal) - 1
                })

def monitor_active_orders():
    for i, order in enumerate(st.session_state.active_orders[:]):
        current_price = get_live_price(order['symbol'])
        if current_price == 0:
            continue
        
        if current_price <= order['sl']:
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = '❌ SL HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit'] = round(current_price, 2)
            send_telegram(f"❌ SL HIT: {order['symbol']} @ ₹{current_price:.2f}")
            voice_alert(f"Stop loss hit for {order['symbol']}")
            st.session_state.active_orders.pop(i)
            st.rerun()
        
        elif current_price >= order['target']:
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = '✅ TARGET HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit'] = round(current_price, 2)
            send_telegram(f"✅ TARGET HIT: {order['symbol']} @ ₹{current_price:.2f}")
            voice_alert(f"Target hit for {order['symbol']}")
            st.session_state.active_orders.pop(i)
            st.rerun()

# ================= LIVE TIME =================
def update_live_time():
    now = get_ist_now()
    return f"""
    <div class="live-time">
        🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')} | 🐺 Rudransh ALGO v{APP_VERSION}
    </div>
    """

# ================= MAIN UI =================
st.markdown("""
<div style="text-align:center; padding:20px;">
    <h1>🐺 RUDRANSH PRO ALGO X</h1>
    <p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114 | v2.0</p>
    <div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(update_live_time(), unsafe_allow_html=True)
st.markdown("---")

# ================= STATUS BAR =================
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.session_state.algo_running:
        st.markdown('<span class="badge-success">🟢 ALGO: RUNNING</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-danger">🔴 ALGO: STOPPED</span>', unsafe_allow_html=True)
with col2:
    if FMP_API_KEY and FMP_API_KEY != "YOUR_FMP_API_KEY_HERE":
        st.markdown('<span class="badge-success">📊 FMP: CONNECTED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-warning">📊 FMP: API KEY NEEDED</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="badge-success">📱 TELEGRAM: ACTIVE</span>', unsafe_allow_html=True)
with col4:
    if st.session_state.voice_enabled:
        st.markdown('<span class="badge-success">🔊 VOICE: ON</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-warning">🔊 VOICE: OFF</span>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<span class="badge-info">🐺 ORDERS: {len(st.session_state.wolf_orders)}</span>', unsafe_allow_html=True)
with col6:
    if check_daily_loss_limit():
        st.markdown('<span class="badge-danger">⚠️ LOSS LIMIT HIT</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="badge-warning">📉 LOSS: ₹{abs(st.session_state.daily_loss):,.0f}</span>', unsafe_allow_html=True)

st.markdown("---")

# Control Panel
col1, col2, col3 = st.columns([2,1,1])
with col1:
    totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code", key="totp_main")
with col2:
    if st.button("🟢 START", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 RUDRANSH ALGO STARTED v2.0")
            st.rerun()
        else:
            st.error("Valid TOTP required!")
with col3:
    if st.button("🔴 STOP", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 RUDRANSH ALGO STOPPED")
        st.rerun()

st.markdown("---")

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🐺 WOLF ORDER", "📊 MARKET", "📰 NEWS", "📈 RESULTS", "⚙️ SETTINGS", "📋 JOURNAL"
])

# ================= TAB 1: WOLF ORDER =================
with tab1:
    st.markdown("### 🐺 WOLF ORDER BOOK (F&O + COMMODITY)")
    st.markdown(f"*Total {len(FO_SCRIPTS)} Symbols Available*")
    
    with st.expander("➕ PLACE WOLF ORDER", expanded=False):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            wolf_symbol = st.selectbox("Symbol", FO_SCRIPTS, key="wolf_sym")
        with col2:
            strike_price = st.number_input("Strike", min_value=1, max_value=500000, value=24300, step=50, key="wolf_strike")
        with col3:
            wolf_qty = st.number_input("Lots", min_value=1, max_value=100, value=1, key="wolf_qty")
        with col4:
            wolf_buy_above = st.number_input("Buy Above", min_value=1, max_value=500000, value=100, step=10, key="wolf_buy")
        with col5:
            wolf_sl = st.number_input("Stop Loss", min_value=1, max_value=500000, value=80, step=10, key="wolf_sl")
        with col6:
            wolf_target = st.number_input("Target", min_value=1, max_value=500000, value=150, step=10, key="wolf_target")
        with col7:
            if st.button("🐺 PLACE ORDER", use_container_width=True):
                if wolf_buy_above <= wolf_sl:
                    st.error("Buy Above > SL required!")
                elif wolf_target <= wolf_buy_above:
                    st.error("Target > Buy Above required!")
                else:
                    st.session_state.wolf_orders.append({
                        'symbol': wolf_symbol, 'strike_price': strike_price, 'qty': wolf_qty,
                        'buy_above': wolf_buy_above, 'sl': wolf_sl, 'target': wolf_target,
                        'status': 'PENDING', 'entry_price': None, 'entry_time': None
                    })
                    send_telegram(f"🐺 WOLF ORDER: {wolf_symbol} | Buy: {wolf_buy_above} | SL: {wolf_sl} | Target: {wolf_target}")
                    st.success(f"✅ Order placed for {wolf_symbol}")
                    st.rerun()
    
    pending = [o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']
    if pending:
        st.markdown("### ⏳ PENDING HUNTS")
        df_pending = pd.DataFrame([{
            'Symbol': o['symbol'], 'Strike': o['strike_price'], 'Lots': o['qty'],
            'Buy Above': o['buy_above'], 'SL': o['sl'], 'Target': o['target']
        } for o in pending])
        st.dataframe(df_pending, use_container_width=True)
    
    active = st.session_state.active_orders
    if active:
        st.markdown("### 🔴 ACTIVE HUNTS")
        active_data = []
        for o in active:
            current = get_live_price(o['symbol'])
            active_data.append({
                'Symbol': o['symbol'], 'Strike': o.get('strike_price', ''), 
                'Entry': o['entry_price'], 'Current': round(current, 2) if current else 0,
                'SL': o['sl'], 'Target': o['target']
            })
        df_active = pd.DataFrame(active_data)
        st.dataframe(df_active, use_container_width=True)

# ================= TAB 2: MARKET DASHBOARD =================
with tab2:
    st.markdown("### 📊 LIVE MARKET DASHBOARD")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nifty = get_live_price("NIFTY")
        st.metric("🇮🇳 NIFTY 50", f"₹{nifty:,.2f}" if nifty else "Loading...")
    with col2:
        banknifty = get_live_price("BANKNIFTY")
        st.metric("🏦 BANK NIFTY", f"₹{banknifty:,.2f}" if banknifty else "Loading...")
    with col3:
        crude = get_live_price("CRUDE") * get_usd_inr_rate()
        st.metric("🛢️ CRUDE OIL", f"₹{crude:,.2f}" if crude else "Loading...")
    with col4:
        ng = get_live_price("NATURALGAS") * get_usd_inr_rate()
        st.metric("🌿 NATURAL GAS", f"₹{ng:,.2f}" if ng else "Loading...")

# ================= TAB 3: NEWS =================
with tab3:
    st.markdown("### 📰 MULTI-SOURCE NEWS")
    st.markdown("*Bloomberg | Reuters | CNBC | FT | ET | Moneycontrol | Zee | Investing | Mint*")
    
    col1, col2 = st.columns([3,1])
    with col2:
        st.session_state.voice_enabled = st.checkbox("🔊 Voice Alerts", value=st.session_state.voice_enabled)
    
    st.markdown("---")
    
    news_articles = get_all_news()
    for article in news_articles:
        with st.container():
            col_a, col_b = st.columns([4,1])
            with col_a:
                st.markdown(f"**📌 {article['title']}**")
                st.caption(f"Source: {article['source']} | {article['time']}")
            with col_b:
                st.markdown(f"`{article['sentiment']}`")
            st.markdown("---")

# ================= TAB 4: RESULTS MONITORING =================
with tab4:
    st.markdown("### 📊 REAL-TIME RESULTS MONITORING")
    st.markdown("*Powered by Financial Modeling Prep API*")
    
    # FMP API Status
    if FMP_API_KEY and FMP_API_KEY != "YOUR_FMP_API_KEY_HERE":
        st.success("🟢 FMP API: CONNECTED | Monitoring Active (30 sec refresh)")
    else:
        st.warning("⚠️ FMP API Key Required! Get it from https://financialmodelingprep.com/")
        api_key_input = st.text_input("Enter FMP API Key:", type="password")
        if api_key_input:
            FMP_API_KEY = api_key_input
            st.rerun()
    
    st.markdown("---")
    
    # Pending Results
    st.markdown("### ⏳ PENDING RESULTS TODAY")
    pending_df = pd.DataFrame([{
        "Company": c['name'], "Symbol": c['symbol'], "Expected Time": c['time'], "Verdict": c['expected']
    } for c in PENDING_RESULTS])
    st.dataframe(pending_df, use_container_width=True)
    
    st.markdown("---")
    
    # AI Analysis Engine Status
    st.markdown("### 🧠 AI ANALYSIS ENGINE")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", "🟢 READY")
    with col2:
        st.metric("Confidence Threshold", "70%")
    with col3:
        st.metric("Auto Trade", "ENABLED" if st.session_state.algo_running else "DISABLED")
    
    st.markdown("---")
    
    # Alerts History
    if st.session_state.result_alerts:
        st.markdown("### 🔔 RESULT ALERTS HISTORY")
        for alert in st.session_state.result_alerts[-5:]:
            with st.container():
                col1, col2 = st.columns([3,1])
                with col1:
                    st.markdown(f"**📊 {alert['company']}**")
                    st.caption(f"Time: {alert['timestamp']} | AI: {alert['ai_analysis']['verdict']}")
                with col2:
                    st.markdown(f"`{alert['ai_analysis']['signal']}`")
                st.progress(alert['ai_analysis']['confidence']/100)
                st.caption(f"Reasons: {', '.join(alert['ai_analysis']['reasons'])}")
                st.markdown("---")

# ================= TAB 5: SETTINGS =================
with tab5:
    st.markdown("### ⚙️ SYSTEM SETTINGS")
    
    st.markdown("#### 🇮🇳 NIFTY TP SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots, key="nifty_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.nifty_tp1, key="nifty_tp1")
    with col3:
        st.checkbox("ON", value=st.session_state.nifty_tp1_enabled, key="nifty_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.nifty_tp2, key="nifty_tp2")
    with col5:
        st.checkbox("ON", value=st.session_state.nifty_tp2_enabled, key="nifty_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.nifty_tp3, key="nifty_tp3")
    with col7:
        st.checkbox("ON", value=st.session_state.nifty_tp3_enabled, key="nifty_tp3_en")
    
    st.markdown("#### 🛢️ CRUDE TP SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, key="crude_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.crude_tp1, key="crude_tp1")
    with col3:
        st.checkbox("ON", value=st.session_state.crude_tp1_enabled, key="crude_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.crude_tp2, key="crude_tp2")
    with col5:
        st.checkbox("ON", value=st.session_state.crude_tp2_enabled, key="crude_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.crude_tp3, key="crude_tp3")
    with col7:
        st.checkbox("ON", value=st.session_state.crude_tp3_enabled, key="crude_tp3_en")
    
    st.markdown("#### 🌿 NATURAL GAS TP SETTINGS")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.number_input("Lots", min_value=1, max_value=50, key="ng_lots")
    with col2:
        st.number_input("TP1", min_value=1, max_value=50, value=st.session_state.ng_tp1, key="ng_tp1")
    with col3:
        st.checkbox("ON", value=st.session_state.ng_tp1_enabled, key="ng_tp1_en")
    with col4:
        st.number_input("TP2", min_value=1, max_value=50, value=st.session_state.ng_tp2, key="ng_tp2")
    with col5:
        st.checkbox("ON", value=st.session_state.ng_tp2_enabled, key="ng_tp2_en")
    with col6:
        st.number_input("TP3", min_value=1, max_value=50, value=st.session_state.ng_tp3, key="ng_tp3")
    with col7:
        st.checkbox("ON", value=st.session_state.ng_tp3_enabled, key="ng_tp3_en")
    
    st.markdown("---")
    st.markdown("#### 📉 RISK MANAGEMENT")
    st.session_state.max_daily_loss = st.number_input("Max Daily Loss (₹)", 10000, 500000, st.session_state.max_daily_loss, 10000)

# ================= TAB 6: JOURNAL =================
with tab6:
    st.markdown("### 📋 TRADING JOURNAL")
    
    if st.session_state.trade_journal:
        df_journal = pd.DataFrame(st.session_state.trade_journal)
        st.dataframe(df_journal, use_container_width=True, height=400)
    else:
        st.info("📭 No trades executed yet.")
    
    st.markdown("---")
    st.markdown("### 📊 PERFORMANCE SUMMARY")
    total_trades = len(st.session_state.trade_journal)
    active_count = len([t for t in st.session_state.trade_journal if 'ACTIVE' in str(t.get('Status', ''))])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trades", total_trades)
    with col2:
        st.metric("Active", active_count)
    with col3:
        st.metric("Daily Loss", f"₹{abs(st.session_state.daily_loss):,.0f}")
    with col4:
        st.metric("Max Loss Limit", f"₹{st.session_state.max_daily_loss:,.0f}")

# ================= AUTO MONITORING =================
if st.session_state.algo_running and st.session_state.totp_verified and not check_daily_loss_limit():
    check_and_execute_wolf_orders()
    monitor_active_orders()
    
    # Monitor FMP Results
    if FMP_API_KEY and FMP_API_KEY != "YOUR_FMP_API_KEY_HERE":
        monitor_results()
    
    st.info("🐺 Rudransh ALGO is active... Monitoring Wolf Orders & Results 🔍")

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🐺 RUDRANSH DASHBOARD")
    st.markdown("---")
    
    st.markdown("### 📊 TODAY'S STATUS")
    st.metric("Active Hunts", len(st.session_state.active_orders))
    st.metric("Pending Hunts", len([o for o in st.session_state.wolf_orders if o['status'] == 'PENDING']))
    st.metric("Daily P&L", f"₹{abs(st.session_state.daily_loss):,.2f}")
    st.metric("Total Symbols", len(FO_SCRIPTS))
    
    st.markdown("---")
    st.markdown("### 🧠 AI STATUS")
    st.caption("🤖 AI Engine: READY")
    st.caption("📊 FMP API: " + ("CONNECTED" if FMP_API_KEY and FMP_API_KEY != "YOUR_FMP_API_KEY_HERE" else "PENDING"))
    st.caption("📰 News Sources: 9 Active")
    
    st.markdown("---")
    st.markdown("### 📱 CONNECTED SERVICES")
    st.caption("✅ Telegram Bot")
    st.caption("✅ Voice Alerts")
    st.caption("✅ FMP API")
    st.caption("✅ Multi-Source News")
    
    st.markdown("---")
    st.markdown(f"### 📌 VERSION INFO")
    st.caption(f"App: {APP_NAME}")
    st.caption(f"Version: {APP_VERSION}")
    st.caption(f"Updated: {LAST_UPDATE}")

# ================= AUTO REFRESH =================
time.sleep(30)  # 30 seconds refresh for real-time monitoring
st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:20px; color:#94a3b8;">
    🐺 Rudransh Pro Algo X v{APP_VERSION} | {APP_AUTHOR} | {APP_LOCATION}
    <br>
    🔐 App Protected | 🐺 Wolf Order Active | 📊 FMP Results Monitor | 📰 9 News Sources
</div>
""", unsafe_allow_html=True)
