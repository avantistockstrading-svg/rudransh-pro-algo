# ============================================================
# RUDRANSH PRO ALGO X - COMPLETE AUTO TRADING ECOSYSTEM
# With Fund Management, Dynamic Lot Sizing, AI Auto Trade
# And Live Market Dashboard with Sliding News Ticker
# DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114
# ============================================================

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time
from streamlit_autorefresh import st_autorefresh

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RUDRANSH PRO ALGO X", layout="wide", page_icon="🤖")

# ================= FMP API CONFIGURATION =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"

# ================= IST Timezone =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= APP LOCK =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False
if "app_password" not in st.session_state:
    st.session_state.app_password = "8055"

# ================= FUND MANAGEMENT SYSTEM =================
if "initial_capital" not in st.session_state:
    st.session_state.initial_capital = 1000000
if "premium_estimate" not in st.session_state:
    st.session_state.premium_estimate = 30
if "max_capital_per_trade" not in st.session_state:
    st.session_state.max_capital_per_trade = 20

def get_available_funds():
    total_pnl = 0
    for trade in st.session_state.trade_journal:
        if 'Profit/Loss' in trade:
            total_pnl += trade.get('Profit/Loss', 0)
    available = st.session_state.initial_capital + total_pnl
    return max(available, 0)

def calculate_dynamic_quantity(lot_size, max_qty_limit, enable_big_lot_mode, big_lot_qty, available_funds, entry_premium_estimate=30):
    if enable_big_lot_mode and big_lot_qty:
        suggested_qty = big_lot_qty
        suggested_lots = big_lot_qty // lot_size
    else:
        max_lots = max_qty_limit // lot_size
        if max_lots < 1:
            max_lots = 1
        suggested_qty = max_lots * lot_size
        suggested_lots = max_lots
    
    max_capital_this_trade = (available_funds * st.session_state.max_capital_per_trade) / 100
    max_qty_by_capital = max_capital_this_trade // entry_premium_estimate
    required_funds = suggested_qty * entry_premium_estimate
    min_required = lot_size * entry_premium_estimate
    
    if available_funds >= required_funds and suggested_qty <= max_qty_by_capital:
        return suggested_qty, suggested_lots, None, required_funds
    elif available_funds >= min_required:
        max_possible_qty = min(max_qty_by_capital, available_funds // entry_premium_estimate)
        max_possible_lots = max_possible_qty // lot_size
        if max_possible_lots < 1:
            max_possible_lots = 1
        final_qty = max_possible_lots * lot_size
        final_lots = max_possible_lots
        final_required = final_qty * entry_premium_estimate
        warning = f"⚠️ Fund limit! Reduced from {suggested_lots} lots to {final_lots} lots"
        return final_qty, final_lots, warning, final_required
    else:
        warning = f"❌ Insufficient funds! Required: ₹{min_required:,.0f}, Available: ₹{available_funds:,.0f}"
        return 0, 0, warning, 0

# ================= COMPANY SYMBOLS =================
COMPANY_SYMBOLS = {
    "HDFC Bank": "HDFCBANK",
    "Reliance Industries": "RELIANCE",
    "Infosys": "INFY",
    "Maruti Suzuki": "MARUTI",
    "Tata Motors": "TATAMOTORS",
    "Bharat Electronics": "BEL",
    "BPCL": "BPCL",
    "Zydus Lifesciences": "ZYDUSLIFE",
    "Mankind Pharma": "MANKIND",
    "PI Industries": "PIIND",
}

# ================= Q4 RESULTS =================
if "q4_results" not in st.session_state:
    st.session_state.q4_results = {
        "HDFC Bank": {"profit": 9.1, "verdict": "Mixed", "date": "15 May 2026", "revenue": 88500, "key": "Deposits grew 14.4%, but NII missed estimates", "announced": True, "alert_sent": True},
        "Reliance Industries": {"profit": -12.5, "verdict": "Negative", "date": "14 May 2026", "revenue": 234000, "key": "Retail strong, Energy business weak", "announced": True, "alert_sent": True},
        "Infosys": {"profit": 11.6, "verdict": "Cautious", "date": "16 May 2026", "revenue": 42000, "key": "Revenue declined 1.3% QoQ, weak guidance", "announced": True, "alert_sent": True},
        "Maruti Suzuki": {"profit": -6.5, "verdict": "Negative", "date": "13 May 2026", "revenue": 38500, "key": "Record sales but margin pressure", "announced": True, "alert_sent": True},
        "Tata Motors": {"profit": -32.0, "verdict": "Negative", "date": "12 May 2026", "revenue": 120000, "key": "India PV strong, JLR weak", "announced": True, "alert_sent": True},
        "Bharat Electronics": {"profit": 0, "verdict": "Pending", "date": "19 May 2026", "revenue": 0, "key": "Expected Positive", "announced": False, "alert_sent": False},
        "BPCL": {"profit": 0, "verdict": "Pending", "date": "19 May 2026", "revenue": 0, "key": "Expected Neutral/Negative", "announced": False, "alert_sent": False},
        "Zydus Lifesciences": {"profit": 0, "verdict": "Pending", "date": "19 May 2026", "revenue": 0, "key": "Expected Positive", "announced": False, "alert_sent": False},
        "Mankind Pharma": {"profit": 0, "verdict": "Pending", "date": "19 May 2026", "revenue": 0, "key": "Expected Positive", "announced": False, "alert_sent": False},
        "PI Industries": {"profit": 0, "verdict": "Pending", "date": "19 May 2026", "revenue": 0, "key": "Expected Positive", "announced": False, "alert_sent": False},
    }

if "last_earnings_check" not in st.session_state:
    st.session_state.last_earnings_check = get_ist_now()
if "alert_history" not in st.session_state:
    st.session_state.alert_history = []
if "latest_alert" not in st.session_state:
    st.session_state.latest_alert = None
if "voice_alert" not in st.session_state:
    st.session_state.voice_alert = None
if "auto_trade_enabled" not in st.session_state:
    st.session_state.auto_trade_enabled = True
if "selected_timeframe" not in st.session_state:
    st.session_state.selected_timeframe = "15m"

# ================= FIXED TARGETS =================
FIXED_TARGETS = {
    "NIFTY": 10,
    "CRUDEOIL": 10,
    "NATURALGAS": 1,
}

# ================= TRADE COUNTERS =================
if "nifty_trades_count" not in st.session_state:
    st.session_state.nifty_trades_count = 0
if "crude_trades_count" not in st.session_state:
    st.session_state.crude_trades_count = 0
if "ng_trades_count" not in st.session_state:
    st.session_state.ng_trades_count = 0

# ================= MAX QUANTITY LIMIT =================
MAX_QTY_OPTIONS = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]

def calculate_trade_quantity(lot_size, max_qty_limit, enable_big_lot_mode=False, big_lot_qty=None):
    available_funds = get_available_funds()
    premium_estimate = st.session_state.get("premium_estimate", 30)
    final_qty, final_lots, warning, required = calculate_dynamic_quantity(
        lot_size, max_qty_limit, enable_big_lot_mode, big_lot_qty,
        available_funds, premium_estimate
    )
    if warning:
        st.warning(warning)
    return final_qty, final_lots

# ================= SYMBOLS =================
SYMBOLS = {"NIFTY": "^NSEI", "CRUDEOIL": "CL=F", "NATURALGAS": "NG=F"}

# ================= USD/INR RATE =================
def get_usd_inr_rate():
    try:
        df = yf.download("USDINR=X", period="1d", interval="5m", progress=False)
        if df.empty:
            df = yf.download("INR=X", period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            rate = df['Close'].iloc[-1]
            if isinstance(rate, pd.Series):
                rate = float(rate.iloc[-1])
            return rate
    except:
        pass
    return 87.5

def get_live_price(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            val = df['Close'].iloc[-1]
            if isinstance(val, pd.Series):
                val = float(val.iloc[-1]) if not val.empty else 0.0
            return float(val)
    except:
        pass
    return 0.0

def get_stock_itm_strike_auto(price, stock, option_type="CE", strike_offset=2):
    if price <= 0:
        return 0, 0, 50
    if price < 100:
        strike_interval = 2.5
    elif price < 250:
        strike_interval = 5
    elif price < 500:
        strike_interval = 10
    elif price < 1000:
        strike_interval = 20
    elif price < 2000:
        strike_interval = 50
    elif price < 5000:
        strike_interval = 100
    else:
        strike_interval = 200
    atm_strike = round(price / strike_interval) * strike_interval
    if option_type == "CE":
        itm_strike = atm_strike - (strike_offset * strike_interval)
        actual_itm = price - itm_strike
    else:
        itm_strike = atm_strike + (strike_offset * strike_interval)
        actual_itm = itm_strike - price
    if itm_strike <= 0:
        itm_strike = strike_interval
    return int(itm_strike), round(actual_itm, 2), strike_interval

# ================= LIVE MARKET DATA FUNCTIONS (NEW) =================

@st.cache_data(ttl=60)
def get_live_market_indices():
    """Get live NIFTY, BANK NIFTY, etc. data"""
    indices = {
        "NIFTY 50": {"symbol": "^NSEI", "name": "🇮🇳 NIFTY 50"},
        "BANK NIFTY": {"symbol": "^NSEBANK", "name": "🏦 BANK NIFTY"},
        "NIFTY IT": {"symbol": "^CNXIT", "name": "💻 NIFTY IT"},
        "NIFTY PHARMA": {"symbol": "^CNXPHARMA", "name": "💊 NIFTY PHARMA"},
    }
    
    result = {}
    for key, value in indices.items():
        try:
            df = yf.download(value["symbol"], period="1d", interval="5m", progress=False)
            if not df.empty:
                current = df['Close'].iloc[-1]
                prev_close = df['Close'].iloc[0] if len(df) > 1 else current
                change = current - prev_close
                change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
                result[key] = {
                    "price": round(current, 2),
                    "change": round(change, 2),
                    "change_percent": round(change_percent, 2),
                    "name": value["name"]
                }
        except:
            result[key] = {"price": 0, "change": 0, "change_percent": 0, "name": value["name"]}
    return result

@st.cache_data(ttl=120)
def get_top_movers():
    """Get top gainers and losers"""
    nifty50_symbols = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "HINDUNILVR.NS", "TATAMOTORS.NS"
    ]
    
    gainers = []
    losers = []
    
    for symbol in nifty50_symbols:
        try:
            df = yf.download(symbol, period="2d", progress=False)
            if len(df) >= 2:
                current = df['Close'].iloc[-1]
                prev = df['Close'].iloc[-2]
                change_percent = ((current - prev) / prev) * 100
                name = symbol.replace(".NS", "")
                
                if change_percent > 0:
                    gainers.append({"name": name, "change": round(change_percent, 2)})
                else:
                    losers.append({"name": name, "change": round(change_percent, 2)})
        except:
            pass
    
    gainers = sorted(gainers, key=lambda x: x["change"], reverse=True)[:5]
    losers = sorted(losers, key=lambda x: x["change"])[:5]
    
    return gainers, losers

@st.cache_data(ttl=60)
def get_live_news():
    """Get live market news - Free API"""
    news_items = []
    
    # Free News API (GNews)
    try:
        url = "https://gnews.io/api/v4/search?q=stock%20market%20india&lang=en&max=10&apikey=YOUR_API_KEY"
        # Note: Get free API key from https://gnews.io/
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for article in data.get("articles", [])[:10]:
                news_items.append({
                    "title": article.get("title", "No Title"),
                    "time": article.get("publishedAt", "Just now")[:16],
                    "source": article.get("source", {}).get("name", "News")
                })
    except:
        # Fallback news
        news_items = [
            {"title": "NIFTY hits fresh record high above 25,000", "time": "Just now", "source": "Market Update"},
            {"title": "RBI announces ₹50,000 cr OMO purchase", "time": "5 mins ago", "source": "Policy News"},
            {"title": "FIIs turn net buyers in Indian equities", "time": "15 mins ago", "source": "FII/DII"},
            {"title": "Crude oil prices steady above $85", "time": "25 mins ago", "source": "Commodity"},
            {"title": "Q4 Results: Multiple companies beat estimates", "time": "35 mins ago", "source": "Earnings"},
            {"title": "Rupee strengthens against US dollar", "time": "45 mins ago", "source": "Forex"},
            {"title": "Gold prices rise on weak dollar", "time": "55 mins ago", "source": "Commodity"},
            {"title": "IT sector leads rally, NIFTY IT up 2%", "time": "1 hour ago", "source": "Sector Update"},
        ]
    
    return news_items

def get_stock_chart(symbol, timeframe):
    """Get stock chart data for selected timeframe"""
    interval_map = {
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1H": "60m",
        "4H": "1h",
        "1D": "1d",
        "1W": "1wk",
        "1M": "1mo"
    }
    
    period_map = {
        "1m": "1d", "5m": "5d", "15m": "5d", "30m": "1mo",
        "1H": "1mo", "4H": "3mo", "1D": "3mo", "1W": "6mo", "1M": "1y"
    }
    
    interval = interval_map.get(timeframe, "15m")
    period = period_map.get(timeframe, "5d")
    
    try:
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        if not df.empty:
            return df
    except:
        pass
    return None

# ================= AUTO TRADE EXECUTION ENGINE =================

def auto_execute_trade(symbol, trade_type, lot_size=0):
    if symbol == "NIFTY":
        current_price = get_live_price("^NSEI")
        if current_price <= 0:
            return False, "Unable to get NIFTY price"
        fixed_target = FIXED_TARGETS["NIFTY"]
        trade_counter = st.session_state.nifty_trades_count
        max_trades = 2
        qty = st.session_state.nifty_lots * 65
        lots = st.session_state.nifty_lots
    elif symbol == "CRUDEOIL":
        current_price = get_live_price("CL=F") * get_usd_inr_rate()
        if current_price <= 0:
            return False, "Unable to get CRUDE price"
        fixed_target = FIXED_TARGETS["CRUDEOIL"]
        trade_counter = st.session_state.crude_trades_count
        max_trades = 2
        qty = st.session_state.crude_lots * 100
        lots = st.session_state.crude_lots
    elif symbol == "NATURALGAS":
        current_price = get_live_price("NG=F") * get_usd_inr_rate()
        if current_price <= 0:
            return False, "Unable to get NG price"
        fixed_target = FIXED_TARGETS["NATURALGAS"]
        trade_counter = st.session_state.ng_trades_count
        max_trades = 2
        qty = st.session_state.ng_lots * 1250
        lots = st.session_state.ng_lots
    else:
        stock_data = next((s for s in FO_STOCKS if s["name"] == symbol), None)
        if not stock_data:
            return False, f"Stock {symbol} not found"
        current_price = get_live_price(stock_data["symbol"])
        if current_price <= 0:
            return False, f"Unable to get {symbol} price"
        fixed_target = stock_data["tp1"]
        trade_counter = st.session_state.stock_trades.get(symbol, {}).get("trades", 0)
        max_trades = 1
        qty, lots = calculate_trade_quantity(
            stock_data["lot"], 
            st.session_state.max_qty_limit,
            st.session_state.enable_big_lot_mode,
            stock_data.get("big_lot_qty")
        )
    
    if qty <= 0:
        return False, "Insufficient funds for trade"
    if trade_counter >= max_trades:
        return False, f"Max trades ({max_trades}) reached for {symbol}"
    
    trade_record = {
        "No": len(st.session_state.trade_journal) + 1,
        "Symbol": symbol,
        "Type": trade_type,
        "Qty": qty,
        "Lots": lots,
        "Entry Price": round(current_price, 2),
        "Target": fixed_target,
        "Status": "OPEN",
        "Entry Time": get_ist_now().strftime('%H:%M:%S'),
        "Source": "🤖 AI AUTO"
    }
    
    st.session_state.trade_journal.append(trade_record)
    
    if symbol == "NIFTY":
        st.session_state.nifty_trades_count += 1
    elif symbol == "CRUDEOIL":
        st.session_state.crude_trades_count += 1
    elif symbol == "NATURALGAS":
        st.session_state.ng_trades_count += 1
    else:
        if symbol not in st.session_state.stock_trades:
            st.session_state.stock_trades[symbol] = {"trades": 0, "buy_done": False, "sell_done": False, "quantity": qty, "lots": lots}
        st.session_state.stock_trades[symbol]["trades"] += 1
    
    send_telegram(f"""
🤖 *AUTO TRADE EXECUTED*

{symbol} | {trade_type}
📊 Lots: {lots} | Qty: {qty}
💰 Entry: ₹{current_price:.2f}
🎯 Target: ₹{fixed_target}
💵 Funds: ₹{get_available_funds():,.0f}

-- RUDRANSH PRO ALGO X --
""")
    
    return True, f"✅ Auto {trade_type} executed for {symbol}"

def process_ai_trade_signal(company_name, verdict, trade_signal):
    if not st.session_state.get("auto_trade_enabled", False):
        return False, "Auto trading disabled"
    if check_daily_loss_limit():
        return False, "Daily loss limit hit"
    
    if "STRONG BUY" in trade_signal or trade_signal == "BUY":
        success, msg = auto_execute_trade("NIFTY", "BUY")
        if success:
            st.toast(f"🤖 AUTO BUY: NIFTY executed based on {company_name} result!", icon="🟢")
            return True, msg
    elif "STRONG SELL" in trade_signal or trade_signal == "SELL":
        success, msg = auto_execute_trade("NIFTY", "SELL")
        if success:
            st.toast(f"🤖 AUTO SELL: NIFTY executed based on {company_name} result!", icon="🔴")
            return True, msg
    return False, "No strong signal"

# ================= AI ANALYSIS ENGINE =================

def ai_analyze_earnings(company_name, eps_actual, eps_estimated, revenue_actual=None, revenue_estimated=None):
    if eps_actual is None or eps_estimated is None or eps_estimated == 0:
        return "Pending", 0, "No data available", "WAIT"
    
    surprise_percent = ((eps_actual - eps_estimated) / abs(eps_estimated)) * 100
    
    if surprise_percent >= 10:
        verdict = "Strong Positive 🟢🟢"
        bullish_score = 90
        reasoning = f"Strong earnings beat! EPS surprise +{surprise_percent:.1f}%"
        trade_signal = "STRONG BUY"
    elif surprise_percent >= 3:
        verdict = "Positive 🟢"
        bullish_score = 70
        reasoning = f"Positive earnings surprise of {surprise_percent:.1f}%"
        trade_signal = "BUY"
    elif surprise_percent >= 0:
        verdict = "Slightly Positive 🟢"
        bullish_score = 55
        reasoning = f"Marginal beat of {surprise_percent:.1f}%"
        trade_signal = "CAUTIOUS BUY"
    elif surprise_percent >= -3:
        verdict = "Slightly Negative 🟡"
        bullish_score = 45
        reasoning = f"Marginal miss of {abs(surprise_percent):.1f}%"
        trade_signal = "WAIT"
    elif surprise_percent >= -10:
        verdict = "Negative 🔴"
        bullish_score = 30
        reasoning = f"Earnings miss of {abs(surprise_percent):.1f}%"
        trade_signal = "SELL"
    else:
        verdict = "Strong Negative 🔴🔴"
        bullish_score = 10
        reasoning = f"Major earnings miss of {abs(surprise_percent):.1f}%"
        trade_signal = "STRONG SELL"
    
    return verdict, bullish_score, reasoning, trade_signal

# ================= CHECK FOR NEW EARNINGS (FMP API) =================

def check_for_new_earnings():
    try:
        today = get_ist_now().date()
        from_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")
        
        url = f"https://financialmodelingprep.com/api/v3/earnings-calendar"
        params = {"apikey": FMP_API_KEY, "from": from_date, "to": to_date}
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code != 200:
            return False
        
        earnings_data = response.json()
        new_alerts = []
        
        for company_name, fmp_symbol in COMPANY_SYMBOLS.items():
            matching = [e for e in earnings_data if e.get('symbol') == fmp_symbol]
            if matching:
                earnings = matching[0]
                eps_actual = earnings.get('epsActual')
                eps_estimated = earnings.get('epsEstimated')
                if eps_actual is not None and eps_estimated is not None:
                    current_data = st.session_state.q4_results[company_name]
                    if current_data.get('eps_actual') != eps_actual and not current_data.get('alert_sent', False):
                        surprise_percent = ((eps_actual - eps_estimated) / abs(eps_estimated)) * 100
                        verdict, bullish_score, reasoning, trade_signal = ai_analyze_earnings(company_name, eps_actual, eps_estimated)
                        
                        st.session_state.q4_results[company_name].update({
                            "profit": surprise_percent, "verdict": verdict,
                            "date": earnings.get('date', get_ist_now().strftime("%d %b %Y")),
                            "eps_actual": eps_actual, "eps_estimated": eps_estimated,
                            "surprise_percent": surprise_percent, "key": reasoning,
                            "trade_signal": trade_signal, "bullish_score": bullish_score,
                            "announced": True, "alert_sent": True
                        })
                        new_alerts.append({
                            "company": company_name, "verdict": verdict,
                            "surprise_percent": surprise_percent, "reasoning": reasoning,
                            "trade_signal": trade_signal, "bullish_score": bullish_score,
                            "time": get_ist_now().strftime("%H:%M:%S")
                        })
        
        for alert in new_alerts:
            send_comprehensive_alert(alert)
            st.session_state.alert_history.insert(0, alert)
        return len(new_alerts) > 0
    except:
        return False

def send_comprehensive_alert(alert):
    company = alert['company']
    verdict = alert['verdict']
    surprise = alert['surprise_percent']
    reasoning = alert['reasoning']
    trade_signal = alert['trade_signal']
    
    send_telegram_alert(company, verdict, surprise, reasoning, trade_signal)
    st.session_state.latest_alert = alert
    voice_msg = f"Alert for {company}. {verdict} with {abs(surprise):.1f} percent surprise. {trade_signal} signal."
    st.session_state.voice_alert = voice_msg
    
    if st.session_state.get("auto_trade_enabled", False):
        trade_executed, msg = process_ai_trade_signal(company, verdict, trade_signal)
        if trade_executed:
            st.toast(f"🤖 {msg}", icon="🤖")

def send_telegram_alert(company, verdict, surprise, reasoning, trade_signal):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    if "Positive" in verdict:
        emoji = "🟢✅"
        direction = "BULLISH"
    elif "Negative" in verdict:
        emoji = "🔴❌"
        direction = "BEARISH"
    else:
        emoji = "🟡📊"
        direction = "NEUTRAL"
    
    msg = f"""🤖 *AI EARNINGS ALERT* 🤖

🏢 *Company:* {company}
{emoji} *Verdict:* {verdict}
📊 *EPS Surprise:* {surprise:+.1f}%
🧠 *AI Analysis:* {reasoning}
🎯 *Trade Signal:* {trade_signal}
⏰ *Time:* {get_ist_now().strftime('%I:%M:%S %p')}"""
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except:
        pass

def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
    except:
        pass

# ================= VOICE ALERT =================
def get_voice_alert_js():
    return """
    <script>
    function speakAlert(message) {
        if ('speechSynthesis' in window) {
            var utterance = new SpeechSynthesisUtterance(message);
            utterance.rate = 0.9;
            utterance.pitch = 1.1;
            utterance.lang = 'en-IN';
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }
    }
    const voiceAlertDiv = document.getElementById('voice-alert-trigger');
    if (voiceAlertDiv && voiceAlertDiv.innerText) {
        speakAlert(voiceAlertDiv.innerText);
    }
    </script>
    """

# ================= GLOBAL TREND FUNCTIONS =================

def get_us_market_trend():
    try:
        spx = yf.download("^GSPC", period="7d", interval="15m", progress=False)
        nasdaq = yf.download("^IXIC", period="7d", interval="15m", progress=False)
        dow = yf.download("^DJI", period="7d", interval="15m", progress=False)
        trends = []
        if not spx.empty and 'Close' in spx.columns:
            ema20_spx = spx['Close'].ewm(span=20).mean().iloc[-1]
            current_spx = spx['Close'].iloc[-1]
            trends.append("BULLISH" if current_spx > ema20_spx else "BEARISH")
        if not nasdaq.empty and 'Close' in nasdaq.columns:
            ema20_nasdaq = nasdaq['Close'].ewm(span=20).mean().iloc[-1]
            current_nasdaq = nasdaq['Close'].iloc[-1]
            trends.append("BULLISH" if current_nasdaq > ema20_nasdaq else "BEARISH")
        if not dow.empty and 'Close' in dow.columns:
            ema20_dow = dow['Close'].ewm(span=20).mean().iloc[-1]
            current_dow = dow['Close'].iloc[-1]
            trends.append("BULLISH" if current_dow > ema20_dow else "BEARISH")
        if not trends:
            return "NEUTRAL"
        bullish_count = trends.count("BULLISH")
        if bullish_count >= 2:
            return "BULLISH"
        elif bullish_count <= 1:
            return "BEARISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_asia_market_trend():
    try:
        nikkei = yf.download("^N225", period="7d", interval="15m", progress=False)
        hangseng = yf.download("^HSI", period="7d", interval="15m", progress=False)
        shanghai = yf.download("000001.SS", period="7d", interval="15m", progress=False)
        trends = []
        if not nikkei.empty and 'Close' in nikkei.columns:
            ema20_nikkei = nikkei['Close'].ewm(span=20).mean().iloc[-1]
            current_nikkei = nikkei['Close'].iloc[-1]
            trends.append("BULLISH" if current_nikkei > ema20_nikkei else "BEARISH")
        if not hangseng.empty and 'Close' in hangseng.columns:
            ema20_hangseng = hangseng['Close'].ewm(span=20).mean().iloc[-1]
            current_hangseng = hangseng['Close'].iloc[-1]
            trends.append("BULLISH" if current_hangseng > ema20_hangseng else "BEARISH")
        if not shanghai.empty and 'Close' in shanghai.columns:
            ema20_shanghai = shanghai['Close'].ewm(span=20).mean().iloc[-1]
            current_shanghai = shanghai['Close'].iloc[-1]
            trends.append("BULLISH" if current_shanghai > ema20_shanghai else "BEARISH")
        if not trends:
            return "NEUTRAL"
        bullish_count = trends.count("BULLISH")
        if bullish_count >= 2:
            return "BULLISH"
        elif bullish_count <= 1:
            return "BEARISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_dxy_trend():
    try:
        dxy = yf.download("DX-Y.NYB", period="7d", interval="15m", progress=False)
        if dxy.empty or 'Close' not in dxy.columns:
            return "NEUTRAL"
        ema20_dxy = dxy['Close'].ewm(span=20).mean().iloc[-1]
        current_dxy = dxy['Close'].iloc[-1]
        if current_dxy > ema20_dxy:
            return "BEARISH"
        elif current_dxy < ema20_dxy:
            return "BULLISH"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_global_trend():
    us_trend = get_us_market_trend()
    asia_trend = get_asia_market_trend()
    dxy_trend = get_dxy_trend()
    scores = []
    scores.append(1 if us_trend == "BULLISH" else -1 if us_trend == "BEARISH" else 0)
    scores.append(1 if asia_trend == "BULLISH" else -1 if asia_trend == "BEARISH" else 0)
    scores.append(1 if dxy_trend == "BULLISH" else -1 if dxy_trend == "BEARISH" else 0)
    total_score = sum(scores)
    if total_score >= 2:
        return "BULLISH", us_trend, asia_trend, dxy_trend
    elif total_score <= -2:
        return "BEARISH", us_trend, asia_trend, dxy_trend
    else:
        return "NEUTRAL", us_trend, asia_trend, dxy_trend

# ================= COMPLETE 69 F&O STOCKS =================
FO_STOCKS = [
    {"symbol": "RELIANCE.NS", "lot": 500, "name": "RELIANCE", "sector": "ENERGY", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "TCS.NS", "lot": 174, "name": "TCS", "sector": "IT", "tp1": 4, "tp2": 4, "big_lot_qty": 5220, "big_lot_lots": 30},
    {"symbol": "HDFCBANK.NS", "lot": 550, "name": "HDFC BANK", "sector": "BANK", "tp1": 3, "tp2": 3, "big_lot_qty": 7700, "big_lot_lots": 14},
    {"symbol": "INFY.NS", "lot": 400, "name": "INFOSYS", "sector": "IT", "tp1": 3, "tp2": 3, "big_lot_qty": 7200, "big_lot_lots": 18},
    {"symbol": "ICICIBANK.NS", "lot": 700, "name": "ICICI BANK", "sector": "BANK", "tp1": 2, "tp2": 2, "big_lot_qty": 11200, "big_lot_lots": 16},
    {"symbol": "SBIN.NS", "lot": 750, "name": "SBI", "sector": "BANK", "tp1": 3, "tp2": 2, "big_lot_qty": 9000, "big_lot_lots": 12},
    {"symbol": "BHARTIARTL.NS", "lot": 476, "name": "BHARTI AIRTEL", "sector": "TELECOM", "tp1": 3, "tp2": 3, "big_lot_qty": 7616, "big_lot_lots": 16},
    {"symbol": "KOTAKBANK.NS", "lot": 2000, "name": "KOTAK BANK", "sector": "BANK", "tp1": 3, "tp2": 3, "big_lot_qty": 8000, "big_lot_lots": 4},
    {"symbol": "BAJFINANCE.NS", "lot": 750, "name": "BAJAJ FINANCE", "sector": "FINANCE", "tp1": 3, "tp2": 3, "big_lot_qty": 7500, "big_lot_lots": 10},
    {"symbol": "ITC.NS", "lot": 1600, "name": "ITC", "sector": "FMCG", "tp1": 1, "tp2": 1, "big_lot_qty": 22400, "big_lot_lots": 14},
    {"symbol": "HINDUNILVR.NS", "lot": 300, "name": "HUL", "sector": "FMCG", "tp1": 3, "tp2": 3, "big_lot_qty": 7200, "big_lot_lots": 24},
    {"symbol": "TATAMOTORS.NS", "lot": 800, "name": "TMPV", "sector": "AUTO", "tp1": 0.75, "tp2": 0.75, "big_lot_qty": 27200, "big_lot_lots": 34},
    {"symbol": "TATASTEEL.NS", "lot": 600, "name": "TATA STEEL", "sector": "METAL", "tp1": 1, "tp2": 1, "big_lot_qty": 20400, "big_lot_lots": 34},
    {"symbol": "AXISBANK.NS", "lot": 624, "name": "AXIS BANK", "sector": "BANK", "tp1": 3, "tp2": 3, "big_lot_qty": 7488, "big_lot_lots": 12},
    {"symbol": "MARUTI.NS", "lot": 50, "name": "MARUTI", "sector": "AUTO", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 80},
    {"symbol": "SUNPHARMA.NS", "lot": 350, "name": "SUN PHARMA", "sector": "PHARMA", "tp1": 3, "tp2": 3, "big_lot_qty": 7000, "big_lot_lots": 20},
    {"symbol": "WIPRO.NS", "lot": 3000, "name": "WIPRO", "sector": "IT", "tp1": 0.50, "tp2": 0.50, "big_lot_qty": 42000, "big_lot_lots": 14},
    {"symbol": "HCLTECH.NS", "lot": 350, "name": "HCL TECH", "sector": "IT", "tp1": 3, "tp2": 3, "big_lot_qty": 7000, "big_lot_lots": 20},
    {"symbol": "NTPC.NS", "lot": 1500, "name": "NTPC", "sector": "ENERGY", "tp1": 0.50, "tp2": 0.50, "big_lot_qty": 42000, "big_lot_lots": 28},
    {"symbol": "POWERGRID.NS", "lot": 1900, "name": "POWER GRID", "sector": "ENERGY", "tp1": 0.75, "tp2": 0.75, "big_lot_qty": 30400, "big_lot_lots": 16},
    {"symbol": "ONGC.NS", "lot": 2250, "name": "ONGC", "sector": "ENERGY", "tp1": 0.50, "tp2": 0.50, "big_lot_qty": 40500, "big_lot_lots": 18},
    {"symbol": "M&M.NS", "lot": 200, "name": "M&M", "sector": "AUTO", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 10},
    {"symbol": "ULTRACEMCO.NS", "lot": 50, "name": "ULTRATECH", "sector": "INFRA", "tp1": 20, "tp2": 20, "big_lot_qty": 1000, "big_lot_lots": 20},
    {"symbol": "NESTLEIND.NS", "lot": 500, "name": "NESTLE", "sector": "FMCG", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "JSWSTEEL.NS", "lot": 674, "name": "JSW STEEL", "sector": "METAL", "tp1": 5, "tp2": 5, "big_lot_qty": 4044, "big_lot_lots": 6},
    {"symbol": "TECHM.NS", "lot": 600, "name": "TECH MAHINDRA", "sector": "IT", "tp1": 5, "tp2": 5, "big_lot_qty": 4800, "big_lot_lots": 8},
    {"symbol": "BAJAJFINSV.NS", "lot": 250, "name": "BAJAJ FINSERV", "sector": "FINANCE", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 16},
    {"symbol": "ASIANPAINT.NS", "lot": 250, "name": "ASIAN PAINTS", "sector": "CONSUMER", "tp1": 4, "tp2": 4, "big_lot_qty": 5000, "big_lot_lots": 20},
    {"symbol": "GRASIM.NS", "lot": 250, "name": "GRASIM", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 16},
    {"symbol": "INDUSINDBK.NS", "lot": 700, "name": "INDUSIND BANK", "sector": "BANK", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 6},
    {"symbol": "BRITANNIA.NS", "lot": 124, "name": "BRITANNIA", "sector": "FMCG", "tp1": 5, "tp2": 5, "big_lot_qty": 4216, "big_lot_lots": 34},
    {"symbol": "DRREDDY.NS", "lot": 624, "name": "DR REDDY", "sector": "PHARMA", "tp1": 5, "tp2": 5, "big_lot_qty": 4992, "big_lot_lots": 8},
    {"symbol": "DIVISLAB.NS", "lot": 100, "name": "DIVIS LAB", "sector": "PHARMA", "tp1": 15, "tp2": 15, "big_lot_qty": 1400, "big_lot_lots": 14},
    {"symbol": "HAL.NS", "lot": 150, "name": "HAL", "sector": "DEFENCE", "tp1": 10, "tp2": 10, "big_lot_qty": 2100, "big_lot_lots": 14},
    {"symbol": "ADANIENT.NS", "lot": 308, "name": "ADANI ENTERPRISES", "sector": "ENERGY", "tp1": 5, "tp2": 5, "big_lot_qty": 4312, "big_lot_lots": 14},
    {"symbol": "ADANIPORTS.NS", "lot": 476, "name": "ADANI PORTS", "sector": "ENERGY", "tp1": 3, "tp2": 3, "big_lot_qty": 7616, "big_lot_lots": 16},
    {"symbol": "HEROMOTOCO.NS", "lot": 150, "name": "HERO MOTOCORP", "sector": "AUTO", "tp1": 10, "tp2": 10, "big_lot_qty": 2100, "big_lot_lots": 14},
    {"symbol": "EICHERMOT.NS", "lot": 100, "name": "EICHER MOTORS", "sector": "AUTO", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 20},
    {"symbol": "PIDILITIND.NS", "lot": 500, "name": "PIDILITE", "sector": "CONSUMER", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 8},
    {"symbol": "DABUR.NS", "lot": 1250, "name": "DABUR", "sector": "FMCG", "tp1": 2, "tp2": 2, "big_lot_qty": 10000, "big_lot_lots": 8},
    {"symbol": "HAVELLS.NS", "lot": 500, "name": "HAVELLS", "sector": "CONSUMER", "tp1": 3, "tp2": 3, "big_lot_qty": 7000, "big_lot_lots": 14},
    {"symbol": "UPL.NS", "lot": 1356, "name": "UPL", "sector": "CHEMICAL", "tp1": 3, "tp2": 3, "big_lot_qty": 8136, "big_lot_lots": 6},
    {"symbol": "LT.NS", "lot": 174, "name": "LT", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4176, "big_lot_lots": 24},
    {"symbol": "ADANIGREEN.NS", "lot": 600, "name": "ADANI GREEN", "sector": "ENERGY", "tp1": 5, "tp2": 5, "big_lot_qty": 4800, "big_lot_lots": 8},
    {"symbol": "VEDANTA.NS", "lot": 1150, "name": "VEDANTA", "sector": "METAL", "tp1": 3, "tp2": 3, "big_lot_qty": 6900, "big_lot_lots": 6},
    {"symbol": "ABB.NS", "lot": 125, "name": "ABB", "sector": "INFRA", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 16},
    {"symbol": "TITAN.NS", "lot": 175, "name": "TITAN", "sector": "CONSUMER", "tp1": 10, "tp2": 10, "big_lot_qty": 2100, "big_lot_lots": 12},
    {"symbol": "INDIGO.NS", "lot": 150, "name": "INDIGO", "sector": "TRAVEL", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 28},
    {"symbol": "BAJAJ-AUTO.NS", "lot": 50, "name": "BAJAJAUTO", "sector": "AUTO", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 40},
    {"symbol": "TVSMOTOR.NS", "lot": 175, "name": "TVSMOTOR", "sector": "AUTO", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 24},
    {"symbol": "COFORGE.NS", "lot": 375, "name": "COFORGE", "sector": "IT", "tp1": 5, "tp2": 5, "big_lot_qty": 4500, "big_lot_lots": 12},
    {"symbol": "PERSISTENT.NS", "lot": 100, "name": "PERSISTENT", "sector": "IT", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 20},
    {"symbol": "LUPIN.NS", "lot": 425, "name": "LUPIN", "sector": "PHARMA", "tp1": 5, "tp2": 5, "big_lot_qty": 4250, "big_lot_lots": 10},
    {"symbol": "AUROPHARMA.NS", "lot": 550, "name": "AUROPHARMA", "sector": "PHARMA", "tp1": 5, "tp2": 5, "big_lot_qty": 4400, "big_lot_lots": 8},
    {"symbol": "HINDALCO.NS", "lot": 700, "name": "HINDALCO", "sector": "METAL", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 6},
    {"symbol": "DMART.NS", "lot": 150, "name": "DMART", "sector": "CONSUMER", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 28},
    {"symbol": "GODREJPROP.NS", "lot": 275, "name": "GODREJPROP", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4400, "big_lot_lots": 16},
    {"symbol": "JSWENERGY.NS", "lot": 1000, "name": "JSWENERGY", "sector": "ENERGY", "tp1": 3, "tp2": 3, "big_lot_qty": 8000, "big_lot_lots": 8},
    {"symbol": "CHOLAFIN.NS", "lot": 625, "name": "CHOLAFIN", "sector": "FINANCE", "tp1": 5, "tp2": 5, "big_lot_qty": 5000, "big_lot_lots": 8},
    {"symbol": "SHRIRAMFIN.NS", "lot": 825, "name": "SHRIRAMFIN", "sector": "FINANCE", "tp1": 5, "tp2": 5, "big_lot_qty": 4950, "big_lot_lots": 6},
    {"symbol": "SIEMENS.NS", "lot": 175, "name": "SIEMENS", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 24},
    {"symbol": "KEI.NS", "lot": 175, "name": "KEI", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 24},
    {"symbol": "POLYCAB.NS", "lot": 125, "name": "POLYCAB", "sector": "INFRA", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 32},
    {"symbol": "APOLLOHOSP.NS", "lot": 125, "name": "APOLLOHOSP", "sector": "HEALTHCARE", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 32},
    {"symbol": "MAXHEALTH.NS", "lot": 525, "name": "MAXHEALTH", "sector": "HEALTHCARE", "tp1": 5, "tp2": 5, "big_lot_qty": 4200, "big_lot_lots": 8},
    {"symbol": "AMBER.NS", "lot": 100, "name": "AMBER", "sector": "CONSUMER", "tp1": 10, "tp2": 10, "big_lot_qty": 2000, "big_lot_lots": 20},
    {"symbol": "VOLTAS.NS", "lot": 375, "name": "VOLTAS", "sector": "CONSUMER", "tp1": 10, "tp2": 10, "big_lot_qty": 2250, "big_lot_lots": 6},
    {"symbol": "MCX.NS", "lot": 225, "name": "MCX", "sector": "FINANCE", "tp1": 5, "tp2": 5, "big_lot_qty": 4050, "big_lot_lots": 18},
    {"symbol": "TRENT.NS", "lot": 100, "name": "TRENT", "sector": "CONSUMER", "tp1": 5, "tp2": 5, "big_lot_qty": 4000, "big_lot_lots": 40},
]

# ================= SECTOR MAPPING =================
SECTOR_INDEX = {
    "BANK": "^NSEBANK", "IT": "^CNXIT", "AUTO": "^CNXAUTO", "PHARMA": "^CNXPHARMA",
    "METAL": "^CNXMETAL", "FMCG": "^CNXFMCG", "FINANCE": "^CNXFINANCE", "ENERGY": "^CNXENERGY",
    "INFRA": "^CNXINFRA", "DEFENCE": "^CNXINFRA", "CONSUMER": "^NIFTY_CONSR_DURBL", 
    "TELECOM": "^CNXIT", "CHEMICAL": "^NIFTY_CHEMICAL", "HEALTHCARE": "^NIFTY_HEALTHCARE",
    "TRAVEL": "^CNXSERVICE",
}

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
if "enable_stocks" not in st.session_state:
    st.session_state.enable_stocks = True
if "nifty_lots" not in st.session_state:
    st.session_state.nifty_lots = 1
if "crude_lots" not in st.session_state:
    st.session_state.crude_lots = 1
if "ng_lots" not in st.session_state:
    st.session_state.ng_lots = 1
if "max_qty_limit" not in st.session_state:
    st.session_state.max_qty_limit = 1500
if "enable_big_lot_mode" not in st.session_state:
    st.session_state.enable_big_lot_mode = False
if "trade_journal" not in st.session_state:
    st.session_state.trade_journal = []
if "stock_trades" not in st.session_state:
    st.session_state.stock_trades = {}
    for stock in FO_STOCKS:
        qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit, False, stock.get("big_lot_qty"))
        st.session_state.stock_trades[stock["name"]] = {"buy_done": False, "sell_done": False, "trades": 0, "quantity": qty, "lots": lots}
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = get_ist_now().date()
if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0
if "max_stocks_per_day" not in st.session_state:
    st.session_state.max_stocks_per_day = 10

# Reset daily trades
if get_ist_now().date() != st.session_state.last_trade_date:
    for stock in FO_STOCKS:
        qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit, st.session_state.enable_big_lot_mode, stock.get("big_lot_qty"))
        st.session_state.stock_trades[stock["name"]] = {"buy_done": False, "sell_done": False, "trades": 0, "quantity": qty, "lots": lots}
    st.session_state.daily_loss = 0
    st.session_state.nifty_trades_count = 0
    st.session_state.crude_trades_count = 0
    st.session_state.ng_trades_count = 0
    st.session_state.last_trade_date = get_ist_now().date()

MAX_DAILY_LOSS = 100000

def check_daily_loss_limit():
    return abs(st.session_state.daily_loss) >= MAX_DAILY_LOSS

# ================= TECHNICAL INDICATORS =================
def get_technical_indicators(df):
    if df.empty or len(df) < 200:
        return None
    close = df['Close']
    high = df['High'] if 'High' in df.columns else close
    low = df['Low'] if 'Low' in df.columns else close
    volume = df['Volume'] if 'Volume' in df.columns else pd.Series([1000000] * len(df))
    
    ema9 = close.ewm(span=9, adjust=False).mean()
    ema20 = close.ewm(span=20, adjust=False).mean()
    ema200 = close.ewm(span=200, adjust=False).mean()
    
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
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
    
    current_rsi = rsi.iloc[-1]
    sideways = (45 < current_rsi < 55) and adx < 20
    
    return {
        "current_price": close.iloc[-1], "ema9": ema9.iloc[-1], "ema20": ema20.iloc[-1],
        "ema200": ema200.iloc[-1], "rsi": current_rsi, "adx": adx,
        "volume_filter": volume_filter, "strong_bull": strong_bull,
        "strong_bear": strong_bear, "sideways": sideways,
        "c1_high": c1['High'] if 'High' in df.columns else close.iloc[-2],
        "c1_low": c1['Low'] if 'Low' in df.columns else close.iloc[-2]
    }

def get_mtf_trend(symbol, timeframe):
    try:
        df = yf.download(symbol, period="7d", interval=timeframe, progress=False)
        if df.empty or len(df) < 20:
            return "NEUTRAL"
        close = df['Close']
        ema20 = close.ewm(span=20).mean().iloc[-1]
        current = close.iloc[-1]
        if current > ema20:
            return "UP"
        elif current < ema20:
            return "DOWN"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_nifty_trend():
    try:
        df = yf.download("^NSEI", period="7d", interval="15m", progress=False)
        if not df.empty and 'Close' in df.columns:
            ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
            if isinstance(current, pd.Series):
                current = float(current.iloc[-1])
            if isinstance(ema20, pd.Series):
                ema20 = float(ema20.iloc[-1])
            if current > ema20:
                return "BULLISH"
            elif current < ema20:
                return "BEARISH"
    except:
        pass
    return "NEUTRAL"

def get_sector_bullish(sector_name):
    try:
        index_symbol = SECTOR_INDEX.get(sector_name, "^NSEI")
        df = yf.download(index_symbol, period="7d", interval="15m", progress=False)
        if not df.empty and 'Close' in df.columns:
            ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
            if isinstance(current, pd.Series):
                current = float(current.iloc[-1])
            if isinstance(ema20, pd.Series):
                ema20 = float(ema20.iloc[-1])
            return current > ema20
    except:
        pass
    return False

def get_sector_bearish(sector_name):
    try:
        index_symbol = SECTOR_INDEX.get(sector_name, "^NSEI")
        df = yf.download(index_symbol, period="7d", interval="15m", progress=False)
        if not df.empty and 'Close' in df.columns:
            ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
            if isinstance(current, pd.Series):
                current = float(current.iloc[-1])
            if isinstance(ema20, pd.Series):
                ema20 = float(ema20.iloc[-1])
            return current < ema20
    except:
        pass
    return False

# ================= TRADING HOURS =================
def is_nifty_market_open():
    now = get_ist_now()
    if now.hour == 9 and now.minute >= 30:
        return True
    elif 10 <= now.hour < 14:
        return True
    elif now.hour == 14 and now.minute <= 30:
        return True
    return False

def is_commodity_market_open():
    now = get_ist_now()
    if now.hour == 18 and now.minute >= 0:
        return True
    elif 19 <= now.hour < 22:
        return True
    elif now.hour == 22 and now.minute <= 15:
        return True
    return False

def is_stock_market_open():
    now = get_ist_now()
    if now.hour == 9 and now.minute >= 30:
        return True
    elif 10 <= now.hour < 14:
        return True
    elif now.hour == 14 and now.minute <= 30:
        return True
    return False

def get_nifty_signal():
    try:
        df = yf.download("^NSEI", period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return "WAIT", 0
        indicators = get_technical_indicators(df)
        if indicators is None:
            return "WAIT", 0
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        c1_low_val = indicators["c1_low"]
        
        trend5_up = get_mtf_trend("^NSEI", "5m") == "UP"
        trend15_up = get_mtf_trend("^NSEI", "15m") == "UP"
        trend1h_up = get_mtf_trend("^NSEI", "60m") == "UP"
        
        buy_conditions = (not sideways_val and ema9_val > ema20_val and current_price > ema200_val and
            rsi_val >= 55 and adx_val >= 22 and volume_filter_val and 
            strong_bull_val and current_price > c1_high_val and
            trend5_up and trend15_up and trend1h_up)
        sell_conditions = (not sideways_val and ema9_val < ema20_val and current_price < ema200_val and
            rsi_val <= 45 and adx_val >= 22 and volume_filter_val and 
            strong_bear_val and current_price < c1_low_val and
            not trend5_up and not trend15_up and not trend1h_up)
        
        if buy_conditions:
            return "BUY", current_price
        elif sell_conditions:
            return "SELL", current_price
        return "WAIT", current_price
    except:
        return "WAIT", 0

def get_crude_signal():
    try:
        df = yf.download("CL=F", period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return "WAIT", 0
        indicators = get_technical_indicators(df)
        if indicators is None:
            return "WAIT", 0
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        c1_low_val = indicators["c1_low"]
        
        trend5_up = get_mtf_trend("CL=F", "5m") == "UP"
        trend15_up = get_mtf_trend("CL=F", "15m") == "UP"
        trend1h_up = get_mtf_trend("CL=F", "60m") == "UP"
        
        buy_conditions = (not sideways_val and ema9_val > ema20_val and current_price > ema200_val and
            rsi_val >= 55 and adx_val >= 22 and volume_filter_val and 
            strong_bull_val and current_price > c1_high_val and
            trend5_up and trend15_up and trend1h_up)
        sell_conditions = (not sideways_val and ema9_val < ema20_val and current_price < ema200_val and
            rsi_val <= 45 and adx_val >= 22 and volume_filter_val and 
            strong_bear_val and current_price < c1_low_val and
            not trend5_up and not trend15_up and not trend1h_up)
        
        if buy_conditions:
            return "BUY", current_price
        elif sell_conditions:
            return "SELL", current_price
        return "WAIT", current_price
    except:
        return "WAIT", 0

def get_ng_signal():
    try:
        df = yf.download("NG=F", period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return "WAIT", 0
        indicators = get_technical_indicators(df)
        if indicators is None:
            return "WAIT", 0
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        c1_low_val = indicators["c1_low"]
        
        trend5_up = get_mtf_trend("NG=F", "5m") == "UP"
        trend15_up = get_mtf_trend("NG=F", "15m") == "UP"
        trend1h_up = get_mtf_trend("NG=F", "60m") == "UP"
        
        buy_conditions = (not sideways_val and ema9_val > ema20_val and current_price > ema200_val and
            rsi_val >= 55 and adx_val >= 22 and volume_filter_val and 
            strong_bull_val and current_price > c1_high_val and
            trend5_up and trend15_up and trend1h_up)
        sell_conditions = (not sideways_val and ema9_val < ema20_val and current_price < ema200_val and
            rsi_val <= 45 and adx_val >= 22 and volume_filter_val and 
            strong_bear_val and current_price < c1_low_val and
            not trend5_up and not trend15_up and not trend1h_up)
        
        if buy_conditions:
            return "BUY", current_price
        elif sell_conditions:
            return "SELL", current_price
        return "WAIT", current_price
    except:
        return "WAIT", 0

def calculate_signals_stock(symbol, stock_name, sector_name):
    try:
        df = yf.download(symbol, period="10d", interval="5m", progress=False)
        if df.empty or len(df) < 200:
            return None
        df.columns = [str(c).lower() for c in df.columns]
        indicators = get_technical_indicators(df)
        if indicators is None:
            return None
        current_price = indicators["current_price"]
        ema9_val = indicators["ema9"]
        ema20_val = indicators["ema20"]
        ema200_val = indicators["ema200"]
        rsi_val = indicators["rsi"]
        adx_val = indicators["adx"]
        volume_filter_val = indicators["volume_filter"]
        strong_bull_val = indicators["strong_bull"]
        strong_bear_val = indicators["strong_bear"]
        sideways_val = indicators["sideways"]
        c1_high_val = indicators["c1_high"]
        c1_low_val = indicators["c1_low"]
        
        nifty_trend = get_nifty_trend()
        nifty_bullish = nifty_trend == "BULLISH"
        nifty_bearish = nifty_trend == "BEARISH"
        sector_bullish = get_sector_bullish(sector_name)
        sector_bearish = get_sector_bearish(sector_name)
        trend5_up = get_mtf_trend(symbol, "5m") == "UP"
        trend15_up = get_mtf_trend(symbol, "15m") == "UP"
        trend1h_up = get_mtf_trend(symbol, "60m") == "UP"
        
        buy_conditions = (nifty_bullish and not sideways_val and sector_bullish and
            ema9_val > ema20_val and current_price > ema200_val and
            rsi_val >= 55 and adx_val >= 22 and volume_filter_val and 
            strong_bull_val and current_price > c1_high_val and
            trend5_up and trend15_up and trend1h_up)
        sell_conditions = (nifty_bearish and not sideways_val and sector_bearish and
            ema9_val < ema20_val and current_price < ema200_val and
            rsi_val <= 45 and adx_val >= 22 and volume_filter_val and 
            strong_bear_val and current_price < c1_low_val and
            not trend5_up and not trend15_up and not trend1h_up)
        
        return {
            "signal": "BUY" if buy_conditions else "SELL" if sell_conditions else "WAIT",
            "buy": buy_conditions, "sell": sell_conditions, "price": current_price,
            "rsi": rsi_val, "adx": adx_val, "strong_bull": strong_bull_val,
            "strong_bear": strong_bear_val, "nifty_bullish": nifty_bullish,
            "sector_bullish": sector_bullish
        }
    except Exception as e:
        return None

# ================= Q4 DASHBOARD =================

def show_q4_dashboard():
    st.markdown("## 📊 Q4 FY26 RESULTS DASHBOARD")
    st.caption("🤖 AI-Powered Real-Time Earnings Analysis | Auto-refresh every 30 seconds | Auto Trading ACTIVE")
    
    try:
        new_earnings = check_for_new_earnings()
        if new_earnings:
            st.toast("📢 New earnings data detected! Auto trade may execute.", icon="🔔")
    except Exception as e:
        pass
    
    if st.session_state.latest_alert:
        alert = st.session_state.latest_alert
        if "Positive" in alert['verdict']:
            bg_color = "rgba(0,255,136,0.2)"
            border_color = "#00ff88"
        else:
            bg_color = "rgba(255,68,68,0.2)"
            border_color = "#ff4444"
        
        st.markdown(f"""
        <div style='background:{bg_color}; padding:15px; border-radius:10px; margin:10px 0; border:2px solid {border_color};'>
            <b>🚨 NEW AI ALERT</b><br>
            <b>{alert['company']}</b> → {alert['verdict']}<br>
            📊 Surprise: {alert['surprise_percent']:+.1f}%<br>
            🧠 {alert['reasoning']}<br>
            🎯 Trade Signal: <b>{alert['trade_signal']}</b><br>
            ⏰ {alert['time']}
        </div>
        """, unsafe_allow_html=True)
    
    rows = []
    for company, data in st.session_state.q4_results.items():
        if "Strong Positive" in str(data["verdict"]) or "Positive" in str(data["verdict"]):
            verdict_display = data["verdict"]
        elif "Negative" in str(data["verdict"]):
            verdict_display = data["verdict"]
        else:
            verdict_display = data["verdict"] if data["verdict"] else "⏳ Pending"
        profit_display = f"{data.get('surprise_percent', data.get('profit', 0)):+.1f}%" if data.get('profit') != 0 else "—"
        rows.append({
            "Company": company, "Result Date": data.get("date", "Pending"),
            "EPS Surprise": profit_display, "Verdict": verdict_display,
            "AI Signal": data.get("trade_signal", "WAIT"),
            "AI Analysis": data.get("key", "Waiting for data...")[:60] + "..."
        })
    
    df_q4 = pd.DataFrame(rows)
    st.dataframe(df_q4, use_container_width=True, height=400)
    
    st.markdown("### 📊 AI Summary")
    col1, col2, col3, col4 = st.columns(4)
    total = len(st.session_state.q4_results)
    positive = sum(1 for d in st.session_state.q4_results.values() if "Positive" in str(d.get("verdict", "")))
    negative = sum(1 for d in st.session_state.q4_results.values() if "Negative" in str(d.get("verdict", "")))
    bullish_signals = sum(1 for d in st.session_state.q4_results.values() if d.get("trade_signal") in ["BUY", "STRONG BUY"])
    
    with col1:
        st.metric("Total Companies", total)
    with col2:
        st.metric("🟢 Positive/Bullish", positive)
    with col3:
        st.metric("🔴 Negative/Bearish", negative)
    with col4:
        st.metric("🎯 AI Buy Signals", bullish_signals)
    
    available_funds = get_available_funds()
    st.markdown(f"### 💰 Fund Status: ₹{available_funds:,.0f} available | Max {st.session_state.max_capital_per_trade}% per trade")
    
    if st.session_state.auto_trade_enabled:
        st.success("🤖 **AUTO TRADING ACTIVE** - AI signals will automatically execute BUY/SELL orders")
    else:
        st.info("⏸️ **AUTO TRADING DISABLED** - Enable in Settings to auto trade")
    
    st.info("🔄 Dashboard auto-refreshes every 30 seconds | AI alerts on Telegram + Voice + Popup + Auto Trade")
    
    if st.session_state.voice_alert:
        st.markdown(f'<div id="voice-alert-trigger" style="display:none;">{st.session_state.voice_alert}</div>', unsafe_allow_html=True)
        st.session_state.voice_alert = None
    st.markdown(get_voice_alert_js(), unsafe_allow_html=True)

# ================= LIVE MARKET DASHBOARD (NEW TAB) =================

def show_live_market_dashboard():
    st.markdown("## 📰 LIVE MARKET DASHBOARD")
    st.caption("Real-time Market Data | News Ticker | Top Movers | Live Charts")
    
    # Timeframe Slider
    st.markdown("### 🎚️ TIME FRAME SELECTOR")
    timeframes = ["1m", "5m", "15m", "30m", "1H", "4H", "1D", "1W", "1M"]
    selected_tf = st.select_slider(
        "Select Time Frame",
        options=timeframes,
        value=st.session_state.selected_timeframe,
        key="tf_slider"
    )
    st.session_state.selected_timeframe = selected_tf
    st.caption(f"Selected: {selected_tf} | Charts and data will update based on this timeframe")
    
    st.markdown("---")
    
    # Sliding News Ticker (CSS Animation)
    st.markdown("""
    <style>
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .ticker-container {
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        border-radius: 10px;
        padding: 12px;
        margin: 10px 0;
        border: 1px solid #00ff88;
        overflow: hidden;
        white-space: nowrap;
    }
    .ticker-wrapper {
        display: inline-block;
        animation: ticker 25s linear infinite;
        white-space: nowrap;
    }
    .ticker-item {
        display: inline-block;
        margin-right: 50px;
        font-size: 16px;
        font-weight: bold;
    }
    .ticker-item-positive { color: #00ff88; }
    .ticker-item-negative { color: #ff4444; }
    .ticker-item-neutral { color: #ffaa00; }
    </style>
    """, unsafe_allow_html=True)
    
    # Get live news
    news_items = get_live_news()
    indices = get_live_market_indices()
    
    # Create ticker HTML
    ticker_html = '<div class="ticker-container"><div class="ticker-wrapper">'
    for name, data in indices.items():
        color_class = "ticker-item-positive" if data['change_percent'] > 0 else "ticker-item-negative" if data['change_percent'] < 0 else "ticker-item-neutral"
        ticker_html += f'<span class="ticker-item {color_class}">{data["name"]}: {data["price"]:,.2f} ({data["change_percent"]:+.2f}%)</span>'
    
    for news in news_items[:5]:
        ticker_html += f'<span class="ticker-item ticker-item-neutral">📰 {news["title"][:50]}...</span>'
    
    ticker_html += '</div></div>'
    st.markdown(ticker_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Market Indices Cards
    st.markdown("### 📈 MARKET INDICES")
    cols = st.columns(4)
    for idx, (name, data) in enumerate(indices.items()):
        with cols[idx % 4]:
            color = "🟢" if data['change_percent'] > 0 else "🔴" if data['change_percent'] < 0 else "🟡"
            st.metric(
                label=f"{color} {data['name']}",
                value=f"{data['price']:,.2f}",
                delta=f"{data['change_percent']:+.2f}%"
            )
    
    st.markdown("---")
    
    # Top Gainers and Losers
    gainers, losers = get_top_movers()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🟢 TOP GAINERS")
        for g in gainers:
            st.markdown(f"<div style='background:rgba(0,255,136,0.1); padding:8px; margin:5px 0; border-radius:8px;'>📈 {g['name']} <span style='color:#00ff88; float:right'>+{g['change']}%</span></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔴 TOP LOSERS")
        for l in losers:
            st.markdown(f"<div style='background:rgba(255,68,68,0.1); padding:8px; margin:5px 0; border-radius:8px;'>📉 {l['name']} <span style='color:#ff4444; float:right'>{l['change']}%</span></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Live Charts Section
    st.markdown("### 📊 LIVE CHARTS")
    chart_options = ["NIFTY 50", "BANK NIFTY", "RELIANCE", "HDFC BANK", "INFOSYS", "TCS"]
    selected_chart = st.selectbox("Select Stock/Index for Chart", chart_options)
    
    symbol_map = {
        "NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK",
        "RELIANCE": "RELIANCE.NS", "HDFC BANK": "HDFCBANK.NS",
        "INFOSYS": "INFY.NS", "TCS": "TCS.NS"
    }
    
    symbol = symbol_map.get(selected_chart, "^NSEI")
    df = get_stock_chart(symbol, st.session_state.selected_timeframe)
    
    if df is not None:
        st.line_chart(df['Close'], use_container_width=True)
        
        # Additional stats
        current_price = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2] if len(df) > 1 else current_price
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"₹{current_price:,.2f}", f"{change_percent:+.2f}%")
        col2.metric("Day High", f"₹{df['High'].max():,.2f}")
        col3.metric("Day Low", f"₹{df['Low'].min():,.2f}")
        col4.metric("Volume", f"{df['Volume'].iloc[-1]:,.0f}")
    else:
        st.warning("Chart data not available")
    
    st.markdown("---")
    
    # Latest News Section
    st.markdown("### 📰 LATEST MARKET NEWS")
    for news in news_items:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin:5px 0; border-left:3px solid #00ff88;'>
            <b>📌 {news['title']}</b><br>
            <span style='color:#94a3b8; font-size:12px'>{news['time']} | {news.get('source', 'Market Update')}</span>
        </div>
        """, unsafe_allow_html=True)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .stButton > button {
        background: linear-gradient(90deg, #00ff88, #00bcd4);
        color: black;
        font-weight: bold;
        border-radius: 30px;
        padding: 8px 20px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,255,136,0.3);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,255,136,0.5);
    }
    h1 {
        background: linear-gradient(135deg, #ffd89b, #19547b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-align: center;
        font-size: 2.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 8px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00ff88, #00bcd4);
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1>RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)

# ================= APP LOCK =================
if not st.session_state.app_unlocked:
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>🔐 APPLICATION LOCKED</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Enter 4-6 Digit Numeric Password to Access</p>", unsafe_allow_html=True)
    
    password_input = st.text_input("Password", type="password", placeholder="Enter numeric password", key="app_lock_password", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔓 UNLOCK", use_container_width=True):
            if str(password_input).strip() == str(st.session_state.app_password).strip():
                st.session_state.app_unlocked = True
                st.rerun()
            else:
                st.error("❌ Wrong Password! Access Denied.")
    st.stop()

# ================= AUTO-REFRESH =================
st_autorefresh(interval=30000, key="q4_auto_refresh", limit=None)

# ================= TABS =================
tab1, tab2, tab3 = st.tabs(["📈 ALGO TRADING", "🤖 AI EARNINGS DASHBOARD", "📰 LIVE MARKET"])

# ================= TAB 1: ALGO TRADING =================
with tab1:
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
            st.markdown(f"""
            <div style="background:linear-gradient(90deg,#00c853,#69f0ae); padding:10px; border-radius:18px; text-align:center; font-weight:bold; color:black; box-shadow:0 0 12px #00ff88; font-size:14px;">
                🟢 RUNNING<br>{get_ist_now().strftime('%H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:linear-gradient(90deg,#d50000,#ff5252); padding:10px; border-radius:18px; text-align:center; font-weight:bold; color:white; box-shadow:0 0 12px #ff0000; font-size:14px;">
                🔴 STOPPED<br>{get_ist_now().strftime('%H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    if check_daily_loss_limit():
        st.error(f"🚨 DAILY LOSS LIMIT HIT: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{MAX_DAILY_LOSS:,.0f} - TRADING STOPPED FOR TODAY! 🚨")
    else:
        st.info(f"📉 Daily Loss: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{MAX_DAILY_LOSS:,.0f} (Limit: ₹1,00,000)")

    st.markdown("---")

    st.markdown("### 🎯 FIXED TARGETS")
    col1, col2, col3 = st.columns(3)
    col1.metric("🇮🇳 NIFTY", "Target ₹10", delta="per point")
    col2.metric("🛢️ CRUDE OIL", "Target ₹10", delta="per point")
    col3.metric("🌿 NATURAL GAS", "Target ₹1", delta="per point")

    st.markdown("---")

    st.markdown("### 🌍 GLOBAL MARKET TREND")
    global_trend, us_trend, asia_trend, dxy_trend = get_global_trend()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if global_trend == "BULLISH":
            st.success(f"🌏 GLOBAL\n🟢 {global_trend}")
        elif global_trend == "BEARISH":
            st.error(f"🌏 GLOBAL\n🔴 {global_trend}")
        else:
            st.warning(f"🌏 GLOBAL\n🟡 {global_trend}")
    with col2:
        if us_trend == "BULLISH":
            st.success(f"🇺🇸 US MARKET\n🟢 {us_trend}")
        elif us_trend == "BEARISH":
            st.error(f"🇺🇸 US MARKET\n🔴 {us_trend}")
        else:
            st.warning(f"🇺🇸 US MARKET\n🟡 {us_trend}")
    with col3:
        if asia_trend == "BULLISH":
            st.success(f"🌏 ASIA MARKET\n🟢 {asia_trend}")
        elif asia_trend == "BEARISH":
            st.error(f"🌏 ASIA MARKET\n🔴 {asia_trend}")
        else:
            st.warning(f"🌏 ASIA MARKET\n🟡 {asia_trend}")
    with col4:
        if dxy_trend == "BULLISH":
            st.success(f"💵 DOLLAR INDEX\n🟢 {dxy_trend} (Weak $)")
        elif dxy_trend == "BEARISH":
            st.error(f"💵 DOLLAR INDEX\n🔴 {dxy_trend} (Strong $)")
        else:
            st.warning(f"💵 DOLLAR INDEX\n🟡 {dxy_trend}")

    st.markdown("---")

    nifty_trend = get_nifty_trend()
    st.markdown("### 🇮🇳 NIFTY TREND")
    if nifty_trend == "BULLISH":
        st.success("🟢 BULLISH")
    elif nifty_trend == "BEARISH":
        st.error("🔴 BEARISH")
    else:
        st.warning("🟡 SIDEWAYS")

    st.markdown("---")

    st.markdown("### 📊 DAILY TRADE COUNTERS (Max 2 per asset)")
    col1, col2, col3 = st.columns(3)
    col1.metric("🇮🇳 NIFTY Trades", f"{st.session_state.nifty_trades_count}/2")
    col2.metric("🛢️ CRUDE Trades", f"{st.session_state.crude_trades_count}/2")
    col3.metric("🌿 NG Trades", f"{st.session_state.ng_trades_count}/2")
    st.markdown("---")

    with st.sidebar:
        st.markdown("## ⚙️ SETTINGS")
        
        st.markdown("### 💰 FUND MANAGEMENT")
        st.session_state.initial_capital = st.number_input("💰 Initial Capital (₹)", min_value=50000, max_value=10000000, value=st.session_state.initial_capital, step=50000, format="%d")
        st.session_state.max_capital_per_trade = st.slider("📊 Max Capital per Trade (%)", min_value=5, max_value=50, value=st.session_state.max_capital_per_trade, step=5)
        st.session_state.premium_estimate = st.number_input("🎯 Estimated Premium per Share (₹)", min_value=5, max_value=200, value=st.session_state.premium_estimate, step=5)
        available_funds = get_available_funds()
        st.metric("💵 Available Funds", f"₹{available_funds:,.0f}")
        if available_funds < 100000:
            st.warning("⚠️ Low funds! Auto lot size will reduce automatically.")
        else:
            st.success(f"✅ Sufficient funds")
        
        st.markdown("---")
        st.markdown("### 🤖 AUTO TRADE")
        st.session_state.auto_trade_enabled = st.checkbox("🔮 Enable AI Auto Trading", value=st.session_state.auto_trade_enabled)
        if st.session_state.auto_trade_enabled:
            st.success("✅ AUTO TRADING ACTIVE")
        else:
            st.info("⏸️ Manual mode")
        
        st.markdown("---")
        st.markdown("### 📌 ASSETS")
        st.session_state.enable_nifty = st.checkbox("🇮🇳 NIFTY", value=st.session_state.enable_nifty)
        if st.session_state.enable_nifty:
            st.session_state.nifty_lots = st.number_input("NIFTY Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots, step=1)
            st.caption(f"📦 Qty: {st.session_state.nifty_lots * 65}")
        
        st.session_state.enable_crude = st.checkbox("🛢️ CRUDE OIL", value=st.session_state.enable_crude)
        if st.session_state.enable_crude:
            st.session_state.crude_lots = st.number_input("CRUDE Lots", min_value=1, max_value=50, value=st.session_state.crude_lots, step=1)
            st.caption(f"📦 Qty: {st.session_state.crude_lots * 100}")
        
        st.session_state.enable_ng = st.checkbox("🌿 NATURAL GAS", value=st.session_state.enable_ng)
        if st.session_state.enable_ng:
            st.session_state.ng_lots = st.number_input("NG Lots", min_value=1, max_value=50, value=st.session_state.ng_lots, step=1)
            st.caption(f"📦 Qty: {st.session_state.ng_lots * 1250}")
        
        st.session_state.enable_stocks = st.checkbox("📈 F&O STOCKS (69)", value=st.session_state.enable_stocks)
        
        if st.session_state.enable_stocks:
            st.markdown("---")
            st.markdown("### 📊 STOCK SETTINGS")
            st.session_state.max_stocks_per_day = st.number_input("Max Stocks/Day", 1, 69, 10)
            st.session_state.max_qty_limit = st.selectbox("Max Qty per Trade", MAX_QTY_OPTIONS, index=14)
            st.session_state.enable_big_lot_mode = st.checkbox("🔥 BIG LOT MODE", value=st.session_state.enable_big_lot_mode)
            if st.session_state.enable_big_lot_mode:
                st.success("✅ BIG LOT ACTIVE - Auto reduces if funds low")
        
        st.markdown("---")
        st.markdown("### 📊 DAILY STATUS")
        total_stocks_traded = sum(v["trades"] for v in st.session_state.stock_trades.values())
        st.metric("Stocks Traded", f"{total_stocks_traded}/{st.session_state.max_stocks_per_day}")
        st.metric("Daily Loss", f"₹{abs(st.session_state.daily_loss):,.0f} / ₹{MAX_DAILY_LOSS:,.0f}")
        
        st.markdown("---")
        st.markdown("### 🎯 RULES")
        st.caption("NIFTY/CRUDE/NG: Max 2 trades/day")
        st.caption("Stocks: Max stocks/day limit")
        st.caption("Daily Loss Limit: ₹1,00,000")
        st.caption("🔐 App Protected with Password")

    st.markdown("## 📋 TRADING JOURNAL")

    if st.session_state.trade_journal:
        df_journal = pd.DataFrame(st.session_state.trade_journal)
        st.dataframe(df_journal, use_container_width=True, height=400)
        
        if 'Profit/Loss' in df_journal.columns:
            total_profit = df_journal[df_journal['Profit/Loss'] > 0]['Profit/Loss'].sum() if len(df_journal[df_journal['Profit/Loss'] > 0]) > 0 else 0
            total_loss = df_journal[df_journal['Profit/Loss'] < 0]['Profit/Loss'].sum() if len(df_journal[df_journal['Profit/Loss'] < 0]) > 0 else 0
            win_trades = len(df_journal[df_journal['Profit/Loss'] > 0])
            loss_trades = len(df_journal[df_journal['Profit/Loss'] < 0])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📊 Total Trades", len(df_journal))
            col2.metric("✅ Win Trades", win_trades)
            col3.metric("❌ Loss Trades", loss_trades)
            col4.metric("💰 Net P&L", f"₹{total_profit + total_loss:,.2f}")
    else:
        st.info("📭 No trades executed yet.")

    st.markdown("---")

    if st.session_state.algo_running and st.session_state.totp_verified and not check_daily_loss_limit():
        if st.session_state.enable_nifty and st.session_state.nifty_trades_count < 2:
            if is_nifty_market_open():
                signal, price = get_nifty_signal()
                if signal != "WAIT":
                    trade_type = "BUY" if signal == "BUY" else "SELL"
                    qty = st.session_state.nifty_lots * 65
                    trade_record = {
                        "No": len(st.session_state.trade_journal) + 1, "Symbol": "NIFTY",
                        "Type": trade_type, "Qty": qty, "Lots": st.session_state.nifty_lots,
                        "Entry Price": round(price, 2), "Target": FIXED_TARGETS["NIFTY"],
                        "Status": "OPEN", "Entry Time": get_ist_now().strftime('%H:%M:%S')
                    }
                    st.session_state.trade_journal.append(trade_record)
                    st.session_state.nifty_trades_count += 1
                    send_telegram(f"🇮🇳 NIFTY {trade_type} | {st.session_state.nifty_lots} lots | Entry: ₹{price:.2f}")
                    st.success(f"✅ NIFTY {trade_type} Executed!")
                    st.rerun()
        
        if st.session_state.enable_crude and st.session_state.crude_trades_count < 2:
            if is_commodity_market_open():
                signal, price = get_crude_signal()
                if signal != "WAIT":
                    trade_type = "BUY" if signal == "BUY" else "SELL"
                    qty = st.session_state.crude_lots * 100
                    price_inr = price * get_usd_inr_rate()
                    trade_record = {
                        "No": len(st.session_state.trade_journal) + 1, "Symbol": "CRUDE OIL",
                        "Type": trade_type, "Qty": qty, "Lots": st.session_state.crude_lots,
                        "Entry Price": round(price_inr, 2), "Target": FIXED_TARGETS["CRUDEOIL"],
                        "Status": "OPEN", "Entry Time": get_ist_now().strftime('%H:%M:%S')
                    }
                    st.session_state.trade_journal.append(trade_record)
                    st.session_state.crude_trades_count += 1
                    send_telegram(f"🛢️ CRUDE {trade_type} | {st.session_state.crude_lots} lots")
                    st.success(f"✅ CRUDE {trade_type} Executed!")
                    st.rerun()
        
        if st.session_state.enable_ng and st.session_state.ng_trades_count < 2:
            if is_commodity_market_open():
                signal, price = get_ng_signal()
                if signal != "WAIT":
                    trade_type = "BUY" if signal == "BUY" else "SELL"
                    qty = st.session_state.ng_lots * 1250
                    price_inr = price * get_usd_inr_rate()
                    trade_record = {
                        "No": len(st.session_state.trade_journal) + 1, "Symbol": "NATURAL GAS",
                        "Type": trade_type, "Qty": qty, "Lots": st.session_state.ng_lots,
                        "Entry Price": round(price_inr, 2), "Target": FIXED_TARGETS["NATURALGAS"],
                        "Status": "OPEN", "Entry Time": get_ist_now().strftime('%H:%M:%S')
                    }
                    st.session_state.trade_journal.append(trade_record)
                    st.session_state.ng_trades_count += 1
                    send_telegram(f"🌿 NG {trade_type} | {st.session_state.ng_lots} lots")
                    st.success(f"✅ NG {trade_type} Executed!")
                    st.rerun()
        
        if st.session_state.enable_stocks:
            st.markdown("## 🔍 SCANNING F&O STOCKS")
            if not is_stock_market_open():
                st.info("⏸️ Market Closed | 9:30 AM - 2:30 PM IST")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                signals_found = []
                trades_done = sum(v["trades"] for v in st.session_state.stock_trades.values())
                
                for idx, stock in enumerate(FO_STOCKS[:20]):
                    progress_bar.progress((idx+1)/20)
                    status_text.text(f"Scanning {stock['name']}...")
                    if trades_done >= st.session_state.max_stocks_per_day:
                        break
                    sig = calculate_signals_stock(stock["symbol"], stock["name"], stock["sector"])
                    if sig and (sig["buy"] or sig["sell"]):
                        trade_done = st.session_state.stock_trades[stock["name"]]["trades"] >= 1
                        if not trade_done:
                            qty, lots = calculate_trade_quantity(stock["lot"], st.session_state.max_qty_limit, 
                                                                  st.session_state.enable_big_lot_mode, stock.get("big_lot_qty"))
                            if qty > 0:
                                buy_price = sig["price"]
                                option_type = "CE" if sig["buy"] else "PE"
                                itm_strike, actual_itm, _ = get_stock_itm_strike_auto(buy_price, stock, option_type)
                                trade_record = {
                                    "No": len(st.session_state.trade_journal) + 1, "Symbol": stock["name"],
                                    "Type": f"BUY {option_type}" if sig["buy"] else f"SELL {option_type}",
                                    "Qty": qty, "Lots": lots, "Entry Price": round(buy_price, 2),
                                    "ITM Strike": itm_strike, "Status": "OPEN",
                                    "Entry Time": get_ist_now().strftime('%H:%M:%S')
                                }
                                st.session_state.trade_journal.append(trade_record)
                                st.session_state.stock_trades[stock["name"]]["trades"] += 1
                                trades_done += 1
                                send_telegram(f"{'BUY' if sig['buy'] else 'SELL'} {stock['name']} {option_type} | Strike: {itm_strike}")
                
                progress_bar.empty()
                status_text.empty()
                
                if signals_found:
                    st.success(f"✅ Signals Found!")
                else:
                    st.info("📭 No signals found")
        
    elif not st.session_state.algo_running:
        st.warning("⏸️ ALGO IS STOPPED. Press START to begin trading.")
    elif not st.session_state.totp_verified:
        st.warning("🔐 Please enter valid 6-digit TOTP code and press START.")
    elif check_daily_loss_limit():
        st.error(f"🚨 DAILY LOSS LIMIT HIT! Trading stopped for today. 🚨")

    st.markdown("---")
    st.caption(f"📊 Trading Journal | NIFTY: {st.session_state.nifty_trades_count}/2 | CRUDE: {st.session_state.crude_trades_count}/2 | NG: {st.session_state.ng_trades_count}/2")
    st.caption("🔐 App Protected | Developed by Satish D. Nakhate")

# ================= TAB 2: AI EARNINGS DASHBOARD =================
with tab2:
    show_q4_dashboard()

# ================= TAB 3: LIVE MARKET DASHBOARD =================
with tab3:
    show_live_market_dashboard()
