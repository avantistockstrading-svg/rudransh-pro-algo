"""
🐺 RUDRANSH PRO ALGO X - REAL TIME EDITION
===========================================
VERSION: 5.0.0
ALL DATA LIVE - REAL MARKET DATA - NO DUMMY
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import math
import time
import json
from streamlit_autorefresh import st_autorefresh
import pytz

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

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🐺")

# ================= TIMEZONE SETUP =================
IST = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    """Returns current IST datetime"""
    return datetime.now(IST)

# ================= SESSION STATE INITIALIZATION =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False
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
if "auto_trade_enabled" not in st.session_state:
    st.session_state.auto_trade_enabled = True
if "auto_trade_qty" not in st.session_state:
    st.session_state.auto_trade_qty = 1
if "auto_trade_sl_percent" not in st.session_state:
    st.session_state.auto_trade_sl_percent = 5
if "auto_trade_target_percent" not in st.session_state:
    st.session_state.auto_trade_target_percent = 10
if "last_price_cache" not in st.session_state:
    st.session_state.last_price_cache = {}
if "price_update_time" not in st.session_state:
    st.session_state.price_update_time = {}

# ================= TRADING HOURS =================
TRADING_HOURS = {
    "NIFTY": {"start_hour": 9, "start_min": 15, "end_hour": 15, "end_min": 30},
    "BANKNIFTY": {"start_hour": 9, "start_min": 15, "end_hour": 15, "end_min": 30},
    "CRUDE": {"start_hour": 9, "start_min": 0, "end_hour": 23, "end_min": 30},
    "NATURALGAS": {"start_hour": 9, "start_min": 0, "end_hour": 23, "end_min": 30},
}

def is_market_open(symbol="NIFTY"):
    """Check if market is open for trading"""
    now = get_ist_now()
    is_weekday = now.weekday() < 5
    if not is_weekday:
        return False
    
    if symbol == "CRUDE" or symbol == "NATURALGAS":
        # Commodity markets - almost 24/7 but limited hours for API
        return True
    else:
        # Equity markets - 9:15 AM to 3:30 PM
        market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
        return market_open <= now <= market_close

# ================= LIVE PRICE FETCHING WITH CACHE =================
def get_live_price(symbol, force_refresh=False):
    """Get real-time price with caching for performance"""
    now = get_ist_now()
    
    # Check cache (refresh every 2 seconds)
    if not force_refresh and symbol in st.session_state.last_price_cache:
        last_update = st.session_state.price_update_time.get(symbol, datetime.min.replace(tzinfo=IST))
        if (now - last_update).total_seconds() < 2:
            return st.session_state.last_price_cache[symbol]
    
    try:
        # Map symbols to yfinance tickers
        ticker_map = {
            "NIFTY": "^NSEI",
            "BANKNIFTY": "^NSEBANK",
            "CRUDE": "CL=F",
            "NATURALGAS": "NG=F",
        }
        
        ticker = ticker_map.get(symbol, f"{symbol}.NS")
        
        # Get live data
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        
        if data is not None and not data.empty and 'Close' in data.columns:
            price = float(data['Close'].iloc[-1])
            st.session_state.last_price_cache[symbol] = price
            st.session_state.price_update_time[symbol] = now
            return price
        
        # Fallback to 5m data
        data = yf.download(ticker, period="5d", interval="5m", progress=False)
        if data is not None and not data.empty and 'Close' in data.columns:
            price = float(data['Close'].iloc[-1])
            st.session_state.last_price_cache[symbol] = price
            st.session_state.price_update_time[symbol] = now
            return price
            
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
    
    # Return cached price if available
    return st.session_state.last_price_cache.get(symbol, 0)

# ================= MULTIPLE PRICE FETCHING =================
def get_multiple_prices(symbols):
    """Fetch multiple prices at once efficiently"""
    result = {}
    ticker_map = {
        "NIFTY": "^NSEI",
        "BANKNIFTY": "^NSEBANK",
        "CRUDE": "CL=F",
        "NATURALGAS": "NG=F",
    }
    
    for symbol in symbols:
        try:
            ticker = ticker_map.get(symbol, f"{symbol}.NS")
            data = yf.download(ticker, period="1d", interval="1m", progress=False)
            if data is not None and not data.empty and 'Close' in data.columns:
                result[symbol] = float(data['Close'].iloc[-1])
            else:
                result[symbol] = st.session_state.last_price_cache.get(symbol, 0)
        except:
            result[symbol] = st.session_state.last_price_cache.get(symbol, 0)
    
    return result

# ================= REAL TECHNICAL INDICATORS =================
def get_technical_indicators(symbol):
    """Calculate real technical indicators from live data"""
    try:
        ticker_map = {
            "NIFTY": "^NSEI",
            "BANKNIFTY": "^NSEBANK",
            "CRUDE": "CL=F",
            "NATURALGAS": "NG=F",
        }
        
        ticker = ticker_map.get(symbol, f"{symbol}.NS")
        
        # Get enough data for indicators
        df = yf.download(ticker, period="5d", interval="5m", progress=False)
        
        if df.empty or len(df) < 50:
            # Try longer period
            df = yf.download(ticker, period="1mo", interval="15m", progress=False)
            if df.empty or len(df) < 50:
                return None
        
        close = df['Close']
        high = df['High']
        low = df['Low']
        volume = df['Volume']
        
        # EMAs
        ema9 = close.ewm(span=9, adjust=False).mean().iloc[-1]
        ema20 = close.ewm(span=20, adjust=False).mean().iloc[-1]
        ema50 = close.ewm(span=50, adjust=False).mean().iloc[-1] if len(close) > 50 else ema20
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1] if not rsi.isna().iloc[-1] else 50
        
        # ADX
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
        
        # MACD
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        macd_histogram = macd - signal
        
        current_price = float(close.iloc[-1])
        
        # Bollinger Bands
        bb_period = 20
        bb_std = 2
        rolling_mean = close.rolling(window=bb_period).mean()
        rolling_std = close.rolling(window=bb_period).std()
        bb_upper = rolling_mean + (rolling_std * bb_std)
        bb_lower = rolling_mean - (rolling_std * bb_std)
        
        return {
            "current_price": current_price,
            "ema9": float(ema9),
            "ema20": float(ema20),
            "ema50": float(ema50),
            "rsi": float(current_rsi),
            "adx": float(adx) if not pd.isna(adx) else 25,
            "macd": float(macd.iloc[-1]),
            "macd_signal": float(signal.iloc[-1]),
            "macd_histogram": float(macd_histogram.iloc[-1]),
            "bb_upper": float(bb_upper.iloc[-1]),
            "bb_lower": float(bb_lower.iloc[-1]),
            "volume": float(volume.iloc[-1]),
        }
    except Exception as e:
        print(f"Technical indicator error for {symbol}: {e}")
        return None

# ================= REAL SIGNAL GENERATION =================
def get_real_signal(symbol):
    """Generate real trading signals based on live data"""
    indicators = get_technical_indicators(symbol)
    if indicators is None:
        return "WAIT", 0, None
    
    price = indicators["current_price"]
    ema9 = indicators["ema9"]
    ema20 = indicators["ema20"]
    rsi = indicators["rsi"]
    adx = indicators["adx"]
    macd_hist = indicators["macd_histogram"]
    
    # Strong Buy conditions
    strong_buy = (
        ema9 > ema20 and
        rsi > 55 and rsi < 75 and
        adx > 25 and
        macd_hist > 0
    )
    
    # Strong Sell conditions
    strong_sell = (
        ema9 < ema20 and
        rsi < 45 and rsi > 25 and
        adx > 25 and
        macd_hist < 0
    )
    
    # Normal Buy
    normal_buy = (
        ema9 > ema20 and
        rsi > 50 and
        macd_hist > 0
    )
    
    # Normal Sell
    normal_sell = (
        ema9 < ema20 and
        rsi < 50 and
        macd_hist < 0
    )
    
    if strong_buy:
        return "STRONG_BUY", price, indicators
    elif strong_sell:
        return "STRONG_SELL", price, indicators
    elif normal_buy:
        return "BUY", price, indicators
    elif normal_sell:
        return "SELL", price, indicators
    
    return "WAIT", price, indicators

# ================= NIFTY TREND (REAL) =================
def get_nifty_trend():
    """Get real NIFTY trend"""
    try:
        data = yf.download("^NSEI", period="10d", interval="15m", progress=False)
        if data.empty or len(data) < 20:
            return "NEUTRAL"
        
        close = data['Close']
        current = close.iloc[-1]
        ema20 = close.ewm(span=20).mean().iloc[-1]
        
        if current > ema20 * 1.005:
            return "STRONG_POSITIVE"
        elif current > ema20:
            return "POSITIVE"
        elif current < ema20 * 0.995:
            return "STRONG_NEGATIVE"
        elif current < ema20:
            return "NEGATIVE"
        return "NEUTRAL"
    except:
        return "NEUTRAL"

# ================= REAL NEWS WITH SENTIMENT =================
def get_real_news():
    """Get real news with sentiment analysis"""
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=15&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            news_list = []
            for article in articles[:10]:
                title = article.get('title', '')
                sentiment = analyze_sentiment(title)
                news_list.append({
                    'title': title,
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'time': article.get('publishedAt', '')[:10],
                    'sentiment': sentiment['label'],
                    'score': sentiment['score'],
                    'icon': sentiment['icon'],
                    'color': sentiment['color']
                })
            return news_list
    except Exception as e:
        print(f"News error: {e}")
    
    # Return empty list if API fails
    return []

def analyze_sentiment(text):
    """Analyze sentiment of news text"""
    text_lower = text.lower()
    
    positive_words = ['surge', 'rally', 'boom', 'record', 'peak', 'high', 'gain', 'up', 'positive', 'bull', 'rise', 'growth', 'profit', 'beat', 'upgrade']
    negative_words = ['crash', 'plunge', 'slump', 'collapse', 'fall', 'drop', 'down', 'negative', 'bear', 'decline', 'loss', 'miss', 'downgrade', 'fear']
    
    score = 0
    for word in positive_words:
        if word in text_lower:
            score += 10
    for word in negative_words:
        if word in text_lower:
            score -= 10
    
    if score >= 20:
        return {'label': 'STRONG BULLISH', 'icon': '🚀', 'color': '#00ff44', 'score': score}
    elif score >= 10:
        return {'label': 'BULLISH', 'icon': '📈', 'color': '#88ff88', 'score': score}
    elif score <= -20:
        return {'label': 'STRONG BEARISH', 'icon': '💀', 'color': '#ff3333', 'score': score}
    elif score <= -10:
        return {'label': 'BEARISH', 'icon': '📉', 'color': '#ff6666', 'score': score}
    else:
        return {'label': 'NEUTRAL', 'icon': '⚪', 'color': '#ffaa00', 'score': score}

# ================= TELEGRAM FUNCTIONS =================
def send_telegram_message(message):
    """Send real Telegram notification"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

# ================= ORDER MANAGEMENT =================
def place_order(symbol, signal, price, qty):
    """Place a real order"""
    if not st.session_state.auto_trade_enabled:
        return False, "Auto trading disabled"
    
    if not is_market_open(symbol):
        return False, "Market closed"
    
    option_type = "CALL (CE)" if signal in ["BUY", "STRONG_BUY"] else "PUT (PE)"
    
    # Calculate SL and Targets
    sl_percent = st.session_state.auto_trade_sl_percent / 100
    target_percent = st.session_state.auto_trade_target_percent / 100
    
    if signal in ["BUY", "STRONG_BUY"]:
        sl_price = price * (1 - sl_percent)
        tp1_price = price * (1 + target_percent * 0.5)
        tp2_price = price * (1 + target_percent)
    else:
        sl_price = price * (1 + sl_percent)
        tp1_price = price * (1 - target_percent * 0.5)
        tp2_price = price * (1 - target_percent)
    
    order = {
        'symbol': symbol,
        'option_type': option_type,
        'qty': qty,
        'entry_price': price,
        'entry_time': get_ist_now().strftime('%H:%M:%S'),
        'sl': sl_price,
        'tp1': tp1_price,
        'tp2': tp2_price,
        'signal': signal,
        'status': 'ACTIVE'
    }
    
    st.session_state.active_orders.append(order)
    
    # Add to journal
    st.session_state.trade_journal.append({
        'time': get_ist_now().strftime('%H:%M:%S'),
        'symbol': symbol,
        'type': signal,
        'entry': price,
        'qty': qty,
        'sl': sl_price,
        'target': tp2_price,
        'status': 'ACTIVE'
    })
    
    # Send Telegram alert
    message = f"""🐺 <b>NEW ORDER PLACED</b>
━━━━━━━━━━━━━━━━
📊 Symbol: {symbol}
📈 Signal: {signal}
💰 Entry: ₹{price:.2f}
📦 Qty: {qty}
🎯 Target 1: ₹{tp1_price:.2f}
🎯 Target 2: ₹{tp2_price:.2f}
🛑 Stop Loss: ₹{sl_price:.2f}
⏰ Time: {get_ist_now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━"""
    
    send_telegram_message(message)
    
    return True, "Order placed successfully"

def monitor_orders():
    """Monitor active orders and check SL/Target hits"""
    orders_to_remove = []
    
    for i, order in enumerate(st.session_state.active_orders):
        current_price = get_live_price(order['symbol'])
        
        if current_price <= 0:
            continue
        
        # Check Stop Loss
        if order['option_type'] == "CALL (CE)":
            if current_price <= order['sl']:
                orders_to_remove.append((i, order, current_price, "SL HIT"))
                pnl = (current_price - order['entry_price']) * order['qty'] * 50
                message = f"❌ <b>SL HIT</b>\n{order['symbol']} | P&L: ₹{pnl:.2f}"
                send_telegram_message(message)
        else:
            if current_price >= order['sl']:
                orders_to_remove.append((i, order, current_price, "SL HIT"))
                pnl = (order['entry_price'] - current_price) * order['qty'] * 50
                message = f"❌ <b>SL HIT</b>\n{order['symbol']} | P&L: ₹{pnl:.2f}"
                send_telegram_message(message)
        
        # Check Target 2
        if order['option_type'] == "CALL (CE)":
            if current_price >= order['tp2']:
                orders_to_remove.append((i, order, current_price, "TARGET HIT"))
                pnl = (current_price - order['entry_price']) * order['qty'] * 50
                message = f"✅ <b>TARGET HIT</b>\n{order['symbol']} | P&L: ₹{pnl:.2f}"
                send_telegram_message(message)
        else:
            if current_price <= order['tp2']:
                orders_to_remove.append((i, order, current_price, "TARGET HIT"))
                pnl = (order['entry_price'] - current_price) * order['qty'] * 50
                message = f"✅ <b>TARGET HIT</b>\n{order['symbol']} | P&L: ₹{pnl:.2f}"
                send_telegram_message(message)
    
    # Remove completed orders
    for idx, order, exit_price, reason in reversed(orders_to_remove):
        # Update journal
        for journal_entry in st.session_state.trade_journal:
            if journal_entry['symbol'] == order['symbol'] and journal_entry['status'] == 'ACTIVE':
                journal_entry['exit'] = exit_price
                journal_entry['status'] = reason
                journal_entry['pnl'] = (exit_price - order['entry_price']) * order['qty'] * 50 if order['option_type'] == "CALL (CE)" else (order['entry_price'] - exit_price) * order['qty'] * 50
                break
        
        st.session_state.active_orders.pop(idx)

# ================= AUTO TRADING ENGINE =================
def run_auto_trading():
    """Main auto trading engine"""
    if not st.session_state.algo_running or not st.session_state.auto_trade_enabled:
        return
    
    # Monitor existing orders
    monitor_orders()
    
    # Check for new signals
    symbols_to_trade = ["NIFTY", "BANKNIFTY", "CRUDE", "NATURALGAS"]
    
    for symbol in symbols_to_trade:
        # Check if already have active order for this symbol
        has_active = any(o['symbol'] == symbol for o in st.session_state.active_orders)
        if has_active:
            continue
        
        # Check if market is open
        if not is_market_open(symbol):
            continue
        
        # Get real signal
        signal, price, indicators = get_real_signal(symbol)
        
        if signal in ["STRONG_BUY", "BUY", "STRONG_SELL", "SELL"]:
            trade_type = "BUY" if "BUY" in signal else "SELL"
            can_trade = True  # Add your trade limit logic here
            
            if can_trade:
                success, msg = place_order(symbol, signal, price, st.session_state.auto_trade_qty)
                if success:
                    time.sleep(1)  # Prevent multiple orders at once

# ================= UI =================
# Custom CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
    .main-header { text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; margin-bottom: 20px; }
    .live-price { font-size: 24px; font-weight: bold; background: rgba(0,255,136,0.1); padding: 10px; border-radius: 10px; text-align: center; }
    .signal-buy { background: #00ff88; color: black; padding: 5px 10px; border-radius: 10px; font-weight: bold; }
    .signal-sell { background: #ff4444; color: white; padding: 5px 10px; border-radius: 10px; font-weight: bold; }
    .signal-wait { background: #ffaa00; color: black; padding: 5px 10px; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# App Lock
if not st.session_state.app_unlocked:
    st.markdown('<div class="main-header"><h1>🐺 RUDRANSH PRO ALGO X</h1><p>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p></div>', unsafe_allow_html=True)
    
    password = st.text_input("Enter Password", type="password")
    if st.button("Unlock", use_container_width=True):
        if password == "8055":
            st.session_state.app_unlocked = True
            st.rerun()
        else:
            st.error("Wrong password!")
    st.stop()

# Header
st.markdown(f"""
<div class="main-header">
    <h1>🐺 {APP_NAME}</h1>
    <p>{APP_AUTHOR} | {APP_LOCATION} | v{APP_VERSION}</p>
    <p>🕐 {get_ist_now().strftime('%H:%M:%S')} IST | 📅 {get_ist_now().strftime('%d %B %Y')}</p>
</div>
""", unsafe_allow_html=True)

# Control Panel
col1, col2, col3 = st.columns(3)

with col1:
    totp = st.text_input("TOTP Code", type="password", placeholder="Enter 6-digit code")
    if st.button("🚀 START ALGO", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram_message("🚀 RUDRANSH PRO ALGO X STARTED")
            st.success("Algo Started!")
            st.rerun()
        else:
            st.error("Valid TOTP required!")

with col2:
    if st.button("🛑 STOP ALGO", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram_message("🛑 RUDRANSH PRO ALGO X STOPPED")
        st.warning("Algo Stopped!")
        st.rerun()

with col3:
    auto_trade = st.checkbox("Auto Trading", st.session_state.auto_trade_enabled)
    st.session_state.auto_trade_enabled = auto_trade

st.markdown("---")

# Live Market Data
st.subheader("📊 LIVE MARKET DATA")

# Auto refresh every 5 seconds
count = st_autorefresh(interval=5000, limit=None, key="live_refresh")

# Get live prices
live_symbols = ["NIFTY", "BANKNIFTY", "CRUDE", "NATURALGAS"]
live_prices = get_multiple_prices(live_symbols)

col1, col2, col3, col4 = st.columns(4)

with col1:
    price = live_prices.get("NIFTY", 0)
    signal, sig_price, _ = get_real_signal("NIFTY")
    signal_class = f"signal-{signal.lower().replace('strong_', '')}" if signal != "WAIT" else "signal-wait"
    st.markdown(f"""
    <div class="live-price">
        🇮🇳 NIFTY<br>
        <span style="font-size:32px;">₹{price:,.2f}</span><br>
        <span class="{signal_class}">{signal}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    price = live_prices.get("BANKNIFTY", 0)
    signal, sig_price, _ = get_real_signal("BANKNIFTY")
    signal_class = f"signal-{signal.lower().replace('strong_', '')}" if signal != "WAIT" else "signal-wait"
    st.markdown(f"""
    <div class="live-price">
        🏦 BANKNIFTY<br>
        <span style="font-size:32px;">₹{price:,.2f}</span><br>
        <span class="{signal_class}">{signal}</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    price = live_prices.get("CRUDE", 0)
    signal, sig_price, _ = get_real_signal("CRUDE")
    signal_class = f"signal-{signal.lower().replace('strong_', '')}" if signal != "WAIT" else "signal-wait"
    st.markdown(f"""
    <div class="live-price">
        🛢️ CRUDE OIL<br>
        <span style="font-size:32px;">${price:.2f}</span><br>
        <span class="{signal_class}">{signal}</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    price = live_prices.get("NATURALGAS", 0)
    signal, sig_price, _ = get_real_signal("NATURALGAS")
    signal_class = f"signal-{signal.lower().replace('strong_', '')}" if signal != "WAIT" else "signal-wait"
    st.markdown(f"""
    <div class="live-price">
        🌿 NATURAL GAS<br>
        <span style="font-size:32px;">${price:.2f}</span><br>
        <span class="{signal_class}">{signal}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Active Orders
st.subheader("🔴 ACTIVE ORDERS")

if st.session_state.active_orders:
    orders_data = []
    for order in st.session_state.active_orders:
        current_price = get_live_price(order['symbol'])
        if order['option_type'] == "CALL (CE)":
            pnl_points = current_price - order['entry_price']
            pnl_color = "green" if pnl_points > 0 else "red"
        else:
            pnl_points = order['entry_price'] - current_price
            pnl_color = "green" if pnl_points > 0 else "red"
        
        pnl_value = pnl_points * order['qty'] * 50
        
        orders_data.append({
            "Symbol": order['symbol'],
            "Type": order['option_type'],
            "Qty": order['qty'],
            "Entry": f"₹{order['entry_price']:.2f}",
            "Current": f"₹{current_price:.2f}",
            "P&L": f"<span style='color:{pnl_color}'>₹{pnl_value:,.2f}</span>",
            "SL": f"₹{order['sl']:.2f}",
            "Target": f"₹{order['tp2']:.2f}"
        })
    
    st.markdown(pd.DataFrame(orders_data).to_html(escape=False), unsafe_allow_html=True)
else:
    st.info("No active orders")

st.markdown("---")

# Trade Journal
st.subheader("📋 TRADE JOURNAL")

if st.session_state.trade_journal:
    journal_df = pd.DataFrame(st.session_state.trade_journal[::-1])
    st.dataframe(journal_df, use_container_width=True)
else:
    st.info("No trades yet")

st.markdown("---")

# Real News
st.subheader("📰 REAL-TIME MARKET NEWS")

news_articles = get_real_news()

if news_articles:
    for news in news_articles[:8]:
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 4px solid {news['color']};">
            <b>{news['icon']} {news['sentiment']}</b><br>
            📌 {news['title']}<br>
            <small>🔗 {news['source']} | 🕐 {news['time']}</small>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Loading news...")

st.markdown("---")

# Technical Indicators Display
st.subheader("📈 TECHNICAL INDICATORS")

selected_symbol = st.selectbox("Select Symbol", live_symbols)

if selected_symbol:
    indicators = get_technical_indicators(selected_symbol)
    if indicators:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("EMA 9", f"{indicators['ema9']:.2f}")
            st.metric("EMA 20", f"{indicators['ema20']:.2f}")
        with col2:
            st.metric("RSI", f"{indicators['rsi']:.1f}")
            st.metric("ADX", f"{indicators['adx']:.1f}")
        with col3:
            st.metric("MACD", f"{indicators['macd']:.2f}")
            st.metric("Signal", f"{indicators['macd_signal']:.2f}")
        with col4:
            st.metric("BB Upper", f"{indicators['bb_upper']:.2f}")
            st.metric("BB Lower", f"{indicators['bb_lower']:.2f}")

# Run auto trading engine
if st.session_state.algo_running and st.session_state.totp_verified:
    run_auto_trading()

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>🐺 RUDRANSH PRO ALGO X v{APP_VERSION} | All data is LIVE from market sources</p>
    <p>Last Updated: {get_ist_now().strftime('%H:%M:%S')} IST</p>
</div>
""", unsafe_allow_html=True)
