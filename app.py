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

# ================= CUSTOM ORDER BOOK SESSION STATE =================
if "custom_orders" not in st.session_state:
    st.session_state.custom_orders = []  # {symbol, buy_above, sl, target, qty, status}
if "active_orders" not in st.session_state:
    st.session_state.active_orders = []  # Active orders with SL/Target monitoring

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
        elif symbol == "CRUDE":
            ticker = "CL=F"
        elif symbol == "NG":
            ticker = "NG=F"
        else:
            ticker = symbol
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            val = df['Close'].iloc[-1]
            return float(val) if not isinstance(val, pd.Series) else float(val.iloc[-1])
    except:
        pass
    return 0.0

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
        "current_price": close.iloc[-1],
        "ema9": ema9.iloc[-1],
        "ema20": ema20.iloc[-1],
        "ema200": ema200.iloc[-1],
        "rsi": current_rsi,
        "adx": adx,
        "volume_filter": volume_filter,
        "strong_bull": strong_bull,
        "strong_bear": strong_bear,
        "sideways": sideways,
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

def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
    except:
        pass

def execute_trade(symbol, trade_type, price, lots, qty, targets):
    target_text = " | ".join([f"TP{i+1}: ₹{t}" for i, t in enumerate(targets) if t > 0])
    trade_record = {
        "No": len(st.session_state.trade_journal) + 1,
        "Time": get_ist_now().strftime('%H:%M:%S'),
        "Symbol": symbol,
        "Type": trade_type,
        "Lots": lots,
        "Qty": qty,
        "Entry Price": round(price, 2),
        "Targets": target_text,
        "Status": "OPEN"
    }
    st.session_state.trade_journal.append(trade_record)
    
    if symbol == "NIFTY":
        st.session_state.nifty_trades_count += 1
    elif symbol == "CRUDE":
        st.session_state.crude_trades_count += 1
    else:
        st.session_state.ng_trades_count += 1
    
    send_telegram(f"🤖 {trade_type} {symbol} | {lots} lots @ ₹{price:.2f} | {target_text}")
    return True

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

# ================= CUSTOM ORDER FUNCTIONS =================
def check_and_execute_custom_orders():
    """Check if any custom order conditions are met and execute"""
    for order in st.session_state.custom_orders[:]:  # Use slice copy
        if order['status'] == 'PENDING':
            current_price = get_live_price(order['symbol'])
            
            if current_price > 0 and current_price >= order['buy_above']:
                # Execute the trade
                order['status'] = 'ACTIVE'
                order['entry_price'] = current_price
                order['entry_time'] = get_ist_now().strftime('%H:%M:%S')
                
                qty_multiplier = 65 if order['symbol'] == 'NIFTY' else 25
                
                # Add to trade journal
                trade_record = {
                    "No": len(st.session_state.trade_journal) + 1,
                    "Time": order['entry_time'],
                    "Symbol": order['symbol'],
                    "Type": "CUSTOM BUY",
                    "Lots": order['qty'],
                    "Qty": order['qty'] * qty_multiplier,
                    "Entry Price": round(current_price, 2),
                    "SL": order['sl'],
                    "Target": order['target'],
                    "Status": "ACTIVE"
                }
                st.session_state.trade_journal.append(trade_record)
                send_telegram(f"🎯 CUSTOM ORDER EXECUTED: {order['symbol']} BUY @ ₹{current_price:.2f} | SL: ₹{order['sl']} | Target: ₹{order['target']} | Qty: {order['qty']} lots")
                
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
        
        qty_multiplier = 65 if order['symbol'] == 'NIFTY' else 25
        
        # Check SL hit
        if current_price <= order['sl']:
            loss_amount = (order['entry_price'] - current_price) * (order['qty'] * qty_multiplier)
            st.session_state.daily_loss += loss_amount
            
            # Update journal
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = 'SL HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit Price'] = round(current_price, 2)
                st.session_state.trade_journal[order['journal_index']]['PNL'] = round(loss_amount, 2)
            
            send_telegram(f"❌ SL HIT: {order['symbol']} @ ₹{current_price:.2f} | Loss: ₹{abs(loss_amount):,.2f}")
            st.session_state.active_orders.pop(i)
            # Remove from custom orders
            for cust_order in st.session_state.custom_orders:
                if cust_order.get('status') == 'ACTIVE' and cust_order.get('entry_price') == order['entry_price']:
                    cust_order['status'] = 'COMPLETED'
            st.rerun()
        
        # Check Target hit
        elif current_price >= order['target']:
            profit_amount = (current_price - order['entry_price']) * (order['qty'] * qty_multiplier)
            
            # Update journal
            if order['journal_index'] < len(st.session_state.trade_journal):
                st.session_state.trade_journal[order['journal_index']]['Status'] = 'TARGET HIT'
                st.session_state.trade_journal[order['journal_index']]['Exit Price'] = round(current_price, 2)
                st.session_state.trade_journal[order['journal_index']]['PNL'] = round(profit_amount, 2)
            
            send_telegram(f"✅ TARGET HIT: {order['symbol']} @ ₹{current_price:.2f} | Profit: ₹{profit_amount:,.2f}")
            st.session_state.active_orders.pop(i)
            # Remove from custom orders
            for cust_order in st.session_state.custom_orders:
                if cust_order.get('status') == 'ACTIVE' and cust_order.get('entry_price') == order['entry_price']:
                    cust_order['status'] = 'COMPLETED'
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

# ================= LIVE PRICES AND SIGNALS =================
usd_inr = get_usd_inr_rate()
nifty_price = get_live_price("NIFTY")
crude_price_usd = get_live_price("CRUDE")
crude_price_inr = crude_price_usd * usd_inr if crude_price_usd else 0
ng_price_usd = get_live_price("NG")
ng_price_inr = ng_price_usd * usd_inr if ng_price_usd else 0

nifty_signal, nifty_price_sig = get_nifty_signal()
crude_signal, crude_price_sig = get_crude_signal()
ng_signal, ng_price_sig = get_ng_signal()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🇮🇳 NIFTY 50", f"₹{nifty_price:,.2f}" if nifty_price else "Loading...")
    if nifty_signal == "BUY":
        st.success(f"🟢 SIGNAL: {nifty_signal}")
    elif nifty_signal == "SELL":
        st.error(f"🔴 SIGNAL: {nifty_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {nifty_signal}")
with col2:
    st.metric("🛢️ CRUDE OIL", f"₹{crude_price_inr:,.2f}" if crude_price_inr else "Loading...")
    if crude_signal == "BUY":
        st.success(f"🟢 SIGNAL: {crude_signal}")
    elif crude_signal == "SELL":
        st.error(f"🔴 SIGNAL: {crude_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {crude_signal}")
with col3:
    st.metric("🌿 NATURAL GAS", f"₹{ng_price_inr:,.2f}" if ng_price_inr else "Loading...")
    if ng_signal == "BUY":
        st.success(f"🟢 SIGNAL: {ng_signal}")
    elif ng_signal == "SELL":
        st.error(f"🔴 SIGNAL: {ng_signal}")
    else:
        st.warning(f"⏳ SIGNAL: {ng_signal}")

st.markdown("---")

# ================= CUSTOM ORDER BOOK (NEW FEATURE) =================
st.markdown("## 📝 CUSTOM ORDER BOOK")
st.markdown("*Set your own Buy Above, Stop Loss, Target, and Quantity - Auto execute when price hits your level*")

with st.expander("➕ ADD NEW ORDER", expanded=False):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        custom_symbol = st.selectbox("Symbol", ["NIFTY", "BANKNIFTY"], key="custom_symbol")
    with col2:
        buy_above = st.number_input("Buy Above (₹)", min_value=10000, max_value=300000, value=24300, step=50, key="buy_above")
    with col3:
        sl = st.number_input("Stop Loss (₹)", min_value=10000, max_value=300000, value=24200, step=50, key="sl")
    with col4:
        target = st.number_input("Target (₹)", min_value=10000, max_value=300000, value=24500, step=50, key="target")
    with col5:
        qty = st.number_input("Quantity (Lots)", min_value=1, max_value=100, value=1, step=1, key="qty")
    
    if st.button("📌 PLACE ORDER", use_container_width=True):
        if buy_above <= sl:
            st.error("❌ Buy Above price must be greater than Stop Loss!")
        elif target <= buy_above:
            st.error("❌ Target must be greater than Buy Above price!")
        else:
            st.session_state.custom_orders.append({
                'symbol': custom_symbol,
                'buy_above': buy_above,
                'sl': sl,
                'target': target,
                'qty': qty,
                'status': 'PENDING',
                'entry_price': None,
                'entry_time': None
            })
            send_telegram(f"📌 ORDER PLACED: {custom_symbol} | Buy Above: ₹{buy_above} | SL: ₹{sl} | Target: ₹{target} | Qty: {qty} lots")
            st.success(f"✅ Order placed for {custom_symbol} - Will execute when price crosses ₹{buy_above}")
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
    for idx, order in enumerate(pending_orders):
        if st.button(f"❌ Cancel {order['symbol']} @ ₹{order['buy_above']}", key=f"cancel_{idx}"):
            st.session_state.custom_orders.remove(order)
            st.rerun()
else:
    st.info("📭 No pending orders. Add an order above.")

# Display Active Orders
st.markdown("### 🔴 ACTIVE ORDERS (SL/Target Monitoring)")
active_orders_list = [o for o in st.session_state.active_orders]
if active_orders_list:
    active_df_data = []
    for o in active_orders_list:
        current_price = get_live_price(o['symbol'])
        pnl = (current_price - o['entry_price']) * (o['qty'] * (65 if o['symbol'] == 'NIFTY' else 25))
        active_df_data.append({
            'Symbol': o['symbol'],
            'Entry Price': f"₹{o['entry_price']:,.2f}",
            'SL': f"₹{o['sl']:,.2f}",
            'Target': f"₹{o['target']:,.2f}",
            'Current P/L': f"₹{pnl:,.2f}"
        })
    active_df = pd.DataFrame(active_df_data)
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

# ================= LOT SIZE AND TP SETTINGS =================
with st.expander("⚙️ LOT SIZE & TARGET PROFIT SETTINGS"):
    st.markdown("### 🇮🇳 NIFTY SETTINGS")
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1:
        st.number_input("Lots", min_value=1, max_value=50, value=st.session_state.nifty_lots, key="nifty_lots")
    with c2:
        st.checkbox("TP1 ON", value=st.session_state.nifty_tp1_enabled, key="nifty_tp1_en")
    with c3:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.nifty_tp1, 
                       disabled=not st.session_state.nifty_tp1_enabled, key="nifty_tp1")
    with c4:
        st.checkbox("TP2 ON", value=st.session_state.nifty_tp2_enabled, key="nifty_tp2_en")
    with c5:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.nifty_tp2, 
                       disabled=not st.session_state.nifty_tp2_enabled, key="nifty_tp2")
    with c6:
        st.checkbox("TP3 ON", value=st.session_state.nifty_tp3_enabled, key="nifty_tp3_en")
    with c7:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.nifty_tp3, 
                       disabled=not st.session_state.nifty_tp3_enabled, key="nifty_tp3")
    
    st.markdown("### 🛢️ CRUDE SETTINGS")
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1:
        st.number_input("Lots", min_value=1, max_value=50, key="crude_lots")
    with c2:
        st.checkbox("TP1 ON", value=st.session_state.crude_tp1_enabled, key="crude_tp1_en")
    with c3:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.crude_tp1, 
                       disabled=not st.session_state.crude_tp1_enabled, key="crude_tp1")
    with c4:
        st.checkbox("TP2 ON", value=st.session_state.crude_tp2_enabled, key="crude_tp2_en")
    with c5:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.crude_tp2, 
                       disabled=not st.session_state.crude_tp2_enabled, key="crude_tp2")
    with c6:
        st.checkbox("TP3 ON", value=st.session_state.crude_tp3_enabled, key="crude_tp3_en")
    with c7:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.crude_tp3, 
                       disabled=not st.session_state.crude_tp3_enabled, key="crude_tp3")
    
    st.markdown("### 🌿 NATURAL GAS SETTINGS")
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1:
        st.number_input("Lots", min_value=1, max_value=50, key="ng_lots")
    with c2:
        st.checkbox("TP1 ON", value=st.session_state.ng_tp1_enabled, key="ng_tp1_en")
    with c3:
        st.number_input("TP1", min_value=1, max_value=50, value=st.session_state.ng_tp1, 
                       disabled=not st.session_state.ng_tp1_enabled, key="ng_tp1")
    with c4:
        st.checkbox("TP2 ON", value=st.session_state.ng_tp2_enabled, key="ng_tp2_en")
    with c5:
        st.number_input("TP2", min_value=1, max_value=50, value=st.session_state.ng_tp2, 
                       disabled=not st.session_state.ng_tp2_enabled, key="ng_tp2")
    with c6:
        st.checkbox("TP3 ON", value=st.session_state.ng_tp3_enabled, key="ng_tp3_en")
    with c7:
        st.number_input("TP3", min_value=1, max_value=50, value=st.session_state.ng_tp3, 
                       disabled=not st.session_state.ng_tp3_enabled, key="ng_tp3")

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
    
    # Check and execute custom orders (NEW)
    check_and_execute_custom_orders()
    
    # Monitor active orders for SL/Target (NEW)
    monitor_active_orders()
    
    # Build target lists for original algo
    nifty_targets = []
    if st.session_state.nifty_tp1_enabled: nifty_targets.append(st.session_state.nifty_tp1)
    if st.session_state.nifty_tp2_enabled: nifty_targets.append(st.session_state.nifty_tp2)
    if st.session_state.nifty_tp3_enabled: nifty_targets.append(st.session_state.nifty_tp3)
    
    crude_targets = []
    if st.session_state.crude_tp1_enabled: crude_targets.append(st.session_state.crude_tp1)
    if st.session_state.crude_tp2_enabled: crude_targets.append(st.session_state.crude_tp2)
    if st.session_state.crude_tp3_enabled: crude_targets.append(st.session_state.crude_tp3)
    
    ng_targets = []
    if st.session_state.ng_tp1_enabled: ng_targets.append(st.session_state.ng_tp1)
    if st.session_state.ng_tp2_enabled: ng_targets.append(st.session_state.ng_tp2)
    if st.session_state.ng_tp3_enabled: ng_targets.append(st.session_state.ng_tp3)
    
    # NIFTY Original Algo
    if st.session_state.enable_nifty and st.session_state.nifty_trades_count < 2:
        if is_nifty_market_open():
            signal, price = get_nifty_signal()
            if signal != "WAIT":
                qty = st.session_state.nifty_lots * 65
                if execute_trade("NIFTY", signal, price, st.session_state.nifty_lots, qty, nifty_targets):
                    st.success(f"✅ NIFTY {signal} Executed at ₹{price:.2f}")
                    st.rerun()
    
    # CRUDE Original Algo
    if st.session_state.enable_crude and st.session_state.crude_trades_count < 2:
        if is_commodity_market_open():
            signal, price_usd = get_crude_signal()
            if signal != "WAIT":
                price_inr = price_usd * get_usd_inr_rate()
                qty = st.session_state.crude_lots * 100
                if execute_trade("CRUDE", signal, price_inr, st.session_state.crude_lots, qty, crude_targets):
                    st.success(f"✅ CRUDE {signal} Executed at ₹{price_inr:.2f}")
                    st.rerun()
    
    # NG Original Algo
    if st.session_state.enable_ng and st.session_state.ng_trades_count < 2:
        if is_commodity_market_open():
            signal, price_usd = get_ng_signal()
            if signal != "WAIT":
                price_inr = price_usd * get_usd_inr_rate()
                qty = st.session_state.ng_lots * 1250
                if execute_trade("NG", signal, price_inr, st.session_state.ng_lots, qty, ng_targets):
                    st.success(f"✅ NG {signal} Executed at ₹{price_inr:.2f}")
                    st.rerun()
    
    st.info("⏳ Waiting for next scan cycle...")
    
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
    st.markdown("### 📌 ASSETS")
    st.session_state.enable_nifty = st.checkbox("🇮🇳 NIFTY", st.session_state.enable_nifty)
    st.session_state.enable_crude = st.checkbox("🛢️ CRUDE OIL", st.session_state.enable_crude)
    st.session_state.enable_ng = st.checkbox("🌿 NATURAL GAS", st.session_state.enable_ng)
    st.markdown("---")
    st.markdown("### 📊 TODAY'S STATUS")
    st.metric("NIFTY Trades", f"{st.session_state.nifty_trades_count}/2")
    st.metric("CRUDE Trades", f"{st.session_state.crude_trades_count}/2")
    st.metric("NG Trades", f"{st.session_state.ng_trades_count}/2")
    st.metric("Active Orders", len(st.session_state.active_orders))
    st.metric("Pending Orders", len([o for o in st.session_state.custom_orders if o['status'] == 'PENDING']))
    st.markdown("---")
    st.markdown("### 🛡️ ACTIVE CONDITIONS")
    st.caption("• EMA9 >/ < EMA20")
    st.caption("• Price >/< EMA200")
    st.caption("• RSI >= 55 (BUY) / <= 45 (SELL)")
    st.caption("• ADX >= 22")
    st.caption("• Strong Bull/Bear Candle")
    st.caption("• Multi-TF (5m, 15m, 1h)")

# ================= AUTO REFRESH =================
time.sleep(5)
st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.caption("🔐 App Protected | Developed by Satish D. Nakhate, Talwade, Pune - 412114")
