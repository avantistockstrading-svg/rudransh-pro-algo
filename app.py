import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
import time
import threading

# ================= पेज कॉन्फिग =================
st.set_page_config(page_title="RUDRANSH PRO ALGO X", layout="wide", page_icon="📈")

# ================= IST टाइमझोन =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= अॅप लॉक =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False
if "app_password" not in st.session_state:
    st.session_state.app_password = "8055"

if not st.session_state.app_unlocked:
    st.markdown("<h1 style='text-align:center;'>RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>🔐 अॅप्लिकेशन लॉक आहे</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>प्रवेशासाठी 4-6 अंकी पासवर्ड टाका</p>", unsafe_allow_html=True)
    
    password_input = st.text_input("पासवर्ड", type="password", placeholder="अंकी पासवर्ड टाका", key="app_lock_password")
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔓 अनलॉक करा", use_container_width=True):
            entered = str(password_input).strip()
            expected = str(st.session_state.app_password).strip()
            if entered == expected:
                st.session_state.app_unlocked = True
                st.rerun()
            else:
                st.error("❌ चुकीचा पासवर्ड! प्रवेश नाकारला.")
    st.stop()

# ================= लाइव्ह वेळ दाखवण्यासाठी =================
def update_live_time():
    """जावास्क्रिप्ट वापरून सतत वेळ अपडेट"""
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
    
# ================= सेशन स्टेट =================
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

# ================= लॉट साइज आणि TP सेटिंग्ज =================
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

# ================= Q4 निकाल डेटा =================
if "q4_results" not in st.session_state:
    st.session_state.q4_results = {
        "HDFC Bank": {"profit": 9.1, "verdict": "🟡 मिश्र", "date": "15 May 2026", "revenue": "₹88,500 Cr", "ai_signal": "WAIT"},
        "Reliance": {"profit": -12.5, "verdict": "🔴 नकारात्मक", "date": "14 May 2026", "revenue": "₹2,34,000 Cr", "ai_signal": "SELL"},
        "Infosys": {"profit": 11.6, "verdict": "🟠 सावधान", "date": "16 May 2026", "revenue": "₹42,000 Cr", "ai_signal": "CAUTIOUS BUY"},
        "Maruti Suzuki": {"profit": -6.5, "verdict": "🔴 नकारात्मक", "date": "13 May 2026", "revenue": "₹38,500 Cr", "ai_signal": "SELL"},
        "Tata Motors": {"profit": -32.0, "verdict": "🔴 नकारात्मक", "date": "12 May 2026", "revenue": "₹1,20,000 Cr", "ai_signal": "STRONG SELL"},
        "Bharat Electronics": {"profit": 0, "verdict": "⏳ प्रलंबित", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
        "BPCL": {"profit": 0, "verdict": "⏳ प्रलंबित", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
        "Zydus Lifesciences": {"profit": 0, "verdict": "⏳ प्रलंबित", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
        "Mankind Pharma": {"profit": 0, "verdict": "⏳ प्रलंबित", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
        "PI Industries": {"profit": 0, "verdict": "⏳ प्रलंबित", "date": "19 May 2026", "revenue": "—", "ai_signal": "PENDING"},
    }

# दररोज ट्रेड रीसेट
if get_ist_now().date() != st.session_state.last_trade_date:
    st.session_state.daily_loss = 0
    st.session_state.nifty_trades_count = 0
    st.session_state.crude_trades_count = 0
    st.session_state.ng_trades_count = 0
    st.session_state.last_trade_date = get_ist_now().date()

def check_daily_loss_limit():
    return abs(st.session_state.daily_loss) >= st.session_state.max_daily_loss

# ================= हेल्पर फंक्शन्स =================
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
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            val = df['Close'].iloc[-1]
            return float(val) if not isinstance(val, pd.Series) else float(val.iloc[-1])
    except:
        pass
    return 0.0

# ================= ट्रेडिंग सिग्नल लॉजिक =================
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

# ================= UI हेडर =================
st.markdown("<h1 style='text-align:center;'>RUDRANSH PRO ALGO X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p>", unsafe_allow_html=True)

# ================= लाइव्ह वेळ दाखवा =================
st.markdown(update_live_time(), unsafe_allow_html=True)
st.markdown("---")

# ================= कंट्रोल पॅनेल =================
col_a, col_b, col_c, col_d = st.columns([2.2, 1, 1, 1.2])
with col_a:
    totp = st.text_input("🔐 TOTP कोड", type="password", placeholder="6 अंकी कोड", key="totp_main", label_visibility="collapsed")
with col_b:
    if st.button("🟢 सुरू करा", use_container_width=True):
        if totp and len(totp) == 6:
            st.session_state.algo_running = True
            st.session_state.totp_verified = True
            send_telegram("🚀 ALGO STARTED")
            st.rerun()
        else:
            st.error("❌ योग्य TOTP आवश्यक आहे!")
with col_c:
    if st.button("🔴 थांबवा", use_container_width=True):
        st.session_state.algo_running = False
        send_telegram("🛑 ALGO STOPPED")
        st.rerun()
with col_d:
    if st.session_state.algo_running:
        st.success(f"🟢 चालू आहे | {get_ist_now().strftime('%H:%M:%S')}")
    else:
        st.error(f"🔴 थांबवले आहे | {get_ist_now().strftime('%H:%M:%S')}")

st.markdown("---")

# ================= दररोजचा तोटा =================
if check_daily_loss_limit():
    st.error(f"🚨 दररोजची तोटा मर्यादा पूर्ण झाली: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{st.session_state.max_daily_loss:,.0f}")
else:
    st.info(f"📉 आजचा तोटा: ₹{abs(st.session_state.daily_loss):,.0f} / ₹{st.session_state.max_daily_loss:,.0f}")

st.markdown("---")

# ================= लाइव्ह किमती आणि सिग्नल =================
usd_inr = get_usd_inr_rate()
nifty_price = get_live_price("^NSEI")
crude_price_usd = get_live_price("CL=F")
crude_price_inr = crude_price_usd * usd_inr if crude_price_usd else 0
ng_price_usd = get_live_price("NG=F")
ng_price_inr = ng_price_usd * usd_inr if ng_price_usd else 0

nifty_signal, nifty_price_sig = get_nifty_signal()
crude_signal, crude_price_sig = get_crude_signal()
ng_signal, ng_price_sig = get_ng_signal()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🇮🇳 निफ्टी 50", f"₹{nifty_price:,.2f}" if nifty_price else "लोड होत आहे...")
    if nifty_signal == "BUY":
        st.success(f"🟢 सिग्नल: {nifty_signal}")
    elif nifty_signal == "SELL":
        st.error(f"🔴 सिग्नल: {nifty_signal}")
    else:
        st.warning(f"⏳ सिग्नल: {nifty_signal}")
with col2:
    st.metric("🛢️ क्रूड ऑइल", f"₹{crude_price_inr:,.2f}" if crude_price_inr else "लोड होत आहे...")
    if crude_signal == "BUY":
        st.success(f"🟢 सिग्नल: {crude_signal}")
    elif crude_signal == "SELL":
        st.error(f"🔴 सिग्नल: {crude_signal}")
    else:
        st.warning(f"⏳ सिग्नल: {crude_signal}")
with col3:
    st.metric("🌿 नॅचरल गॅस", f"₹{ng_price_inr:,.2f}" if ng_price_inr else "लोड होत आहे...")
    if ng_signal == "BUY":
        st.success(f"🟢 सिग्नल: {ng_signal}")
    elif ng_signal == "SELL":
        st.error(f"🔴 सिग्नल: {ng_signal}")
    else:
        st.warning(f"⏳ सिग्नल: {ng_signal}")

st.markdown("---")

# ================= Q4 निकाल डॅशबोर्ड =================
st.markdown("## 📊 Q4 FY26 निकाल डॅशबोर्ड")
rows = []
for company, data in st.session_state.q4_results.items():
    profit_display = f"{data['profit']:+.1f}%" if data['profit'] != 0 else "—"
    rows.append({
        "कंपनी": company, "तारीख": data['date'], "नफा बदल": profit_display,
        "निकाल": data['verdict'], "महसूल": data['revenue'], "🤖 AI सिग्नल": data['ai_signal']
    })
df_q4 = pd.DataFrame(rows)
st.dataframe(df_q4, use_container_width=True, height=300)
st.markdown("---")

# ================= लॉट साइज आणि TP सेटिंग्ज (सुधारित) =================
with st.expander("⚙️ लॉट साइज आणि टार्गेट प्रॉफिट सेटिंग्ज"):
    
    st.markdown("### 🇮🇳 निफ्टी सेटिंग्ज")
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1:
        st.number_input("लॉट", min_value=1, max_value=50, value=st.session_state.nifty_lots, key="nifty_lots")
    with c2:
        st.checkbox("TP1 चालू", value=st.session_state.nifty_tp1_enabled, key="nifty_tp1_en")
    with c3:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.nifty_tp1, 
                       disabled=not st.session_state.nifty_tp1_enabled, key="nifty_tp1")
    with c4:
        st.checkbox("TP2 चालू", value=st.session_state.nifty_tp2_enabled, key="nifty_tp2_en")
    with c5:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.nifty_tp2, 
                       disabled=not st.session_state.nifty_tp2_enabled, key="nifty_tp2")
    with c6:
        st.checkbox("TP3 चालू", value=st.session_state.nifty_tp3_enabled, key="nifty_tp3_en")
    with c7:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.nifty_tp3, 
                       disabled=not st.session_state.nifty_tp3_enabled, key="nifty_tp3")
    
    st.markdown("### 🛢️ क्रूड सेटिंग्ज")
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1:
        # ✅ योग्य - assignment काढून टाकला
        st.number_input("लॉट", min_value=1, max_value=50, key="crude_lots")
    with c2:
        st.checkbox("TP1 चालू", value=st.session_state.crude_tp1_enabled, key="crude_tp1_en")
    with c3:
        st.number_input("TP1", min_value=1, max_value=100, value=st.session_state.crude_tp1, 
                       disabled=not st.session_state.crude_tp1_enabled, key="crude_tp1")
    with c4:
        st.checkbox("TP2 चालू", value=st.session_state.crude_tp2_enabled, key="crude_tp2_en")
    with c5:
        st.number_input("TP2", min_value=1, max_value=100, value=st.session_state.crude_tp2, 
                       disabled=not st.session_state.crude_tp2_enabled, key="crude_tp2")
    with c6:
        st.checkbox("TP3 चालू", value=st.session_state.crude_tp3_enabled, key="crude_tp3_en")
    with c7:
        st.number_input("TP3", min_value=1, max_value=100, value=st.session_state.crude_tp3, 
                       disabled=not st.session_state.crude_tp3_enabled, key="crude_tp3")
    
    st.markdown("### 🌿 नॅचरल गॅस सेटिंग्ज")
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1:
        # ✅ योग्य - assignment काढून टाकला
        st.number_input("लॉट", min_value=1, max_value=50, key="ng_lots")
    with c2:
        st.checkbox("TP1 चालू", value=st.session_state.ng_tp1_enabled, key="ng_tp1_en")
    with c3:
        st.number_input("TP1", min_value=1, max_value=50, value=st.session_state.ng_tp1, 
                       disabled=not st.session_state.ng_tp1_enabled, key="ng_tp1")
    with c4:
        st.checkbox("TP2 चालू", value=st.session_state.ng_tp2_enabled, key="ng_tp2_en")
    with c5:
        st.number_input("TP2", min_value=1, max_value=50, value=st.session_state.ng_tp2, 
                       disabled=not st.session_state.ng_tp2_enabled, key="ng_tp2")
    with c6:
        st.checkbox("TP3 चालू", value=st.session_state.ng_tp3_enabled, key="ng_tp3_en")
    with c7:
        st.number_input("TP3", min_value=1, max_value=50, value=st.session_state.ng_tp3, 
                       disabled=not st.session_state.ng_tp3_enabled, key="ng_tp3")

st.markdown("---")

# ================= ट्रेडिंग जर्नल =================
st.markdown("## 📋 ट्रेडिंग जर्नल")
if st.session_state.trade_journal:
    df_journal = pd.DataFrame(st.session_state.trade_journal)
    st.dataframe(df_journal, use_container_width=True, height=300)
else:
    st.info("📭 अजून कोणतेही ट्रेड झाले नाहीत.")

st.markdown("---")

# ================= ऑटो ट्रेडिंग लॉजिक =================
if st.session_state.algo_running and st.session_state.totp_verified and not check_daily_loss_limit():
    
    # टार्गेट लिस्ट बनवा
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
    
    # निफ्टी
    if st.session_state.enable_nifty and st.session_state.nifty_trades_count < 2:
        if is_nifty_market_open():
            signal, price = get_nifty_signal()
            if signal != "WAIT":
                qty = st.session_state.nifty_lots * 65
                if execute_trade("NIFTY", signal, price, st.session_state.nifty_lots, qty, nifty_targets):
                    st.success(f"✅ निफ्टी {signal} ₹{price:.2f} ला कार्यान्वित झाला")
                    st.rerun()
    
    # क्रूड
    if st.session_state.enable_crude and st.session_state.crude_trades_count < 2:
        if is_commodity_market_open():
            signal, price_usd = get_crude_signal()
            if signal != "WAIT":
                price_inr = price_usd * get_usd_inr_rate()
                qty = st.session_state.crude_lots * 100
                if execute_trade("CRUDE", signal, price_inr, st.session_state.crude_lots, qty, crude_targets):
                    st.success(f"✅ क्रूड {signal} ₹{price_inr:.2f} ला कार्यान्वित झाला")
                    st.rerun()
    
    # एनजी
    if st.session_state.enable_ng and st.session_state.ng_trades_count < 2:
        if is_commodity_market_open():
            signal, price_usd = get_ng_signal()
            if signal != "WAIT":
                price_inr = price_usd * get_usd_inr_rate()
                qty = st.session_state.ng_lots * 1250
                if execute_trade("NG", signal, price_inr, st.session_state.ng_lots, qty, ng_targets):
                    st.success(f"✅ एनजी {signal} ₹{price_inr:.2f} ला कार्यान्वित झाला")
                    st.rerun()
    
    st.info("⏳ पुढील स्कॅनची प्रतीक्षा करत आहे...")
    
elif not st.session_state.algo_running:
    st.warning("⏸️ ALGO थांबवले आहे. ट्रेडिंग सुरू करण्यासाठी START दाबा.")
elif not st.session_state.totp_verified:
    st.warning("🔐 कृपया योग्य 6-अंकी TOTP कोड टाका आणि START दाबा.")
elif check_daily_loss_limit():
    st.error(f"🚨 दररोजची तोटा मर्यादा (₹{st.session_state.max_daily_loss:,.0f}) पूर्ण झाली! ट्रेडिंग थांबवले.")

# ================= साइडबार =================
with st.sidebar:
    st.markdown("## ⚙️ सामान्य सेटिंग्ज")
    st.session_state.max_daily_loss = st.number_input("📉 कमाल दररोज तोटा (₹)", 10000, 500000, st.session_state.max_daily_loss, 10000)
    st.markdown("---")
    st.markdown("### 📌 मालमत्ता")
    st.session_state.enable_nifty = st.checkbox("🇮🇳 निफ्टी", st.session_state.enable_nifty)
    st.session_state.enable_crude = st.checkbox("🛢️ क्रूड ऑइल", st.session_state.enable_crude)
    st.session_state.enable_ng = st.checkbox("🌿 नॅचरल गॅस", st.session_state.enable_ng)
    st.markdown("---")
    st.markdown("### 📊 आजची स्थिती")
    st.metric("निफ्टी ट्रेड", f"{st.session_state.nifty_trades_count}/2")
    st.metric("क्रूड ट्रेड", f"{st.session_state.crude_trades_count}/2")
    st.metric("एनजी ट्रेड", f"{st.session_state.ng_trades_count}/2")
    st.markdown("---")
    st.markdown("### 🛡️ सक्रिय अटी")
    st.caption("• EMA9 >/ < EMA20")
    st.caption("• किंमत >/< EMA200")
    st.caption("• RSI >= 55 (खरेदी) / <= 45 (विक्री)")
    st.caption("• ADX >= 22")
    st.caption("• मजबूत बुल/बेअर मेणबत्ती")
    st.caption("• मल्टी-टीएफ (5m, 15m, 1h)")

# ================= लाइव्ह वेळेसाठी ऑटो रिफ्रेश =================
time.sleep(1)
st.rerun()

# ================= फूटर =================
st.markdown("---")
st.caption("🔐 अॅप संरक्षित | विकसक: सतीश डी. नाखाते, तळवडे, पुणे - 412114")
