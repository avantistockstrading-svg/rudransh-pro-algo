import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Rudransh Pro-Algo - Multi Stock F&O", layout="wide")

# ================= IST Timezone =================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ================= MAX QUANTITY LIMIT =================
MAX_QTY_LIMIT = 1500  # एकूण कमाल quantity 1500

def calculate_trade_quantity(lot_size):
    """Lot size नुसार 1500 च्या आत किती quantity trade करायची ते calculate करते"""
    max_lots = MAX_QTY_LIMIT // lot_size
    if max_lots < 1:
        max_lots = 1
    quantity = max_lots * lot_size
    return quantity, max_lots

# ================= OPTION TP/SL BASED ON PREMIUM =================
def get_option_tp_sl(entry_premium):
    """Premium नुसार SL आणि TP percentages return करते"""
    
    if entry_premium <= 50:
        return {"sl_percent": 30, "tp1_percent": 20, "tp2_percent": 40, "tp3_percent": 60}
    elif entry_premium <= 150:
        return {"sl_percent": 25, "tp1_percent": 15, "tp2_percent": 30, "tp3_percent": 50}
    elif entry_premium <= 300:
        return {"sl_percent": 20, "tp1_percent": 12, "tp2_percent": 25, "tp3_percent": 40}
    elif entry_premium <= 500:
        return {"sl_percent": 15, "tp1_percent": 10, "tp2_percent": 20, "tp3_percent": 30}
    elif entry_premium <= 1000:
        return {"sl_percent": 12, "tp1_percent": 8, "tp2_percent": 15, "tp3_percent": 25}
    else:
        return {"sl_percent": 10, "tp1_percent": 6, "tp2_percent": 12, "tp3_percent": 20}

def calculate_option_targets(entry_premium, quantity):
    """Option साठी TP, SL, Profit calculate करते"""
    tp_sl = get_option_tp_sl(entry_premium)
    
    sl_price = entry_premium * (1 - tp_sl["sl_percent"] / 100)
    tp1_price = entry_premium * (1 + tp_sl["tp1_percent"] / 100)
    tp2_price = entry_premium * (1 + tp_sl["tp2_percent"] / 100)
    tp3_price = entry_premium * (1 + tp_sl["tp3_percent"] / 100)
    
    # Quantity booking (TP1: 50%, TP2: 25%, TP3: 25%)
    qty_tp1 = quantity // 2
    qty_tp2 = quantity // 4
    qty_tp3 = quantity - qty_tp1 - qty_tp2
    
    tp1_profit = qty_tp1 * (tp1_price - entry_premium)
    tp2_profit = qty_tp2 * (tp2_price - entry_premium)
    tp3_profit = qty_tp3 * (tp3_price - entry_premium)
    sl_loss = quantity * (entry_premium - sl_price)
    
    return {
        "entry": entry_premium,
        "sl": sl_price,
        "sl_loss": sl_loss,
        "tp1": tp1_price,
        "tp1_profit": tp1_profit,
        "tp2": tp2_price,
        "tp2_profit": tp2_profit,
        "tp3": tp3_price,
        "tp3_profit": tp3_profit,
        "total_profit": tp1_profit + tp2_profit + tp3_profit,
        "sl_percent": tp_sl["sl_percent"],
        "tp1_percent": tp_sl["tp1_percent"],
        "tp2_percent": tp_sl["tp2_percent"],
        "tp3_percent": tp_sl["tp3_percent"]
    }

# ================= F&O Stocks List (50+ Stocks) =================
FO_STOCKS = [
    # तुमचे दिलेले stocks
    {"symbol": "ADANIENT.NS", "lot": 250, "itm": 50, "name": "ADANI ENTERPRISES", "sector": "ENERGY"},
    {"symbol": "SOLAR.NS", "lot": 200, "itm": 50, "name": "SOLAR INDUSTRIES", "sector": "CHEMICALS"},
    {"symbol": "MCX.NS", "lot": 150, "itm": 50, "name": "MCX INDIA", "sector": "FINANCE"},
    {"symbol": "HAL.NS", "lot": 150, "itm": 20, "name": "HAL", "sector": "DEFENCE"},
    {"symbol": "M&M.NS", "lot": 500, "itm": 25, "name": "MAHINDRA & MAHINDRA", "sector": "AUTO"},
    {"symbol": "BAJFINANCE.NS", "lot": 250, "itm": 100, "name": "BAJAJ FINANCE", "sector": "FINANCE"},
    {"symbol": "BHARTIARTL.NS", "lot": 700, "itm": 10, "name": "BHARTI AIRTEL", "sector": "TELECOM"},
    {"symbol": "PERSISTENT.NS", "lot": 200, "itm": 100, "name": "PERSISTENT", "sector": "IT"},
    {"symbol": "BSE.NS", "lot": 200, "itm": 50, "name": "BSE INDIA", "sector": "FINANCE"},
    {"symbol": "DIXON.NS", "lot": 150, "itm": 100, "name": "DIXON TECHNOLOGY", "sector": "CONSUMER"},
    {"symbol": "CIPLA.NS", "lot": 400, "itm": 20, "name": "CIPLA LTD", "sector": "PHARMA"},
    {"symbol": "ASIANPAINT.NS", "lot": 300, "itm": 100, "name": "ASIAN PAINTS", "sector": "CONSUMER"},
    {"symbol": "INDIGO.NS", "lot": 200, "itm": 50, "name": "INDIGO", "sector": "AUTO"},
    {"symbol": "ADANIPORTS.NS", "lot": 350, "itm": 25, "name": "ADANI PORTS", "sector": "ENERGY"},
    {"symbol": "HINDUNILVR.NS", "lot": 400, "itm": 100, "name": "HUL", "sector": "FMCG"},
    {"symbol": "ICICIBANK.NS", "lot": 550, "itm": 25, "name": "ICICI BANK", "sector": "BANK"},
    {"symbol": "JSWSTEEL.NS", "lot": 600, "itm": 10, "name": "JSW STEEL", "sector": "METAL"},
    {"symbol": "ULTRACEMCO.NS", "lot": 200, "itm": 100, "name": "ULTRATECH CEMENT", "sector": "INFRA"},
    {"symbol": "COFORGE.NS", "lot": 150, "itm": 100, "name": "COFORGE", "sector": "IT"},
    {"symbol": "APOLLOHOSP.NS", "lot": 200, "itm": 50, "name": "APOLLO HOSPITAL", "sector": "HEALTHCARE"},
    {"symbol": "POLYCAB.NS", "lot": 150, "itm": 50, "name": "POLYCAB", "sector": "INFRA"},
    {"symbol": "KEI.NS", "lot": 200, "itm": 50, "name": "KEI INDUSTRIES", "sector": "INFRA"},
    {"symbol": "MAZDOCK.NS", "lot": 150, "itm": 20, "name": "MAZGOAN DOCKYARD", "sector": "DEFENCE"},
    # Additional NIFTY50 F&O Stocks
    {"symbol": "RELIANCE.NS", "lot": 250, "itm": 50, "name": "RELIANCE", "sector": "ENERGY"},
    {"symbol": "TCS.NS", "lot": 150, "itm": 100, "name": "TCS", "sector": "IT"},
    {"symbol": "HDFCBANK.NS", "lot": 500, "itm": 50, "name": "HDFC BANK", "sector": "BANK"},
    {"symbol": "INFY.NS", "lot": 200, "itm": 100, "name": "INFOSYS", "sector": "IT"},
    {"symbol": "SBIN.NS", "lot": 450, "itm": 25, "name": "SBI", "sector": "BANK"},
    {"symbol": "KOTAKBANK.NS", "lot": 450, "itm": 50, "name": "KOTAK BANK", "sector": "BANK"},
    {"symbol": "ITC.NS", "lot": 800, "itm": 10, "name": "ITC", "sector": "FMCG"},
    {"symbol": "AXISBANK.NS", "lot": 500, "itm": 25, "name": "AXIS BANK", "sector": "BANK"},
    {"symbol": "WIPRO.NS", "lot": 600, "itm": 40, "name": "WIPRO", "sector": "IT"},
    {"symbol": "HCLTECH.NS", "lot": 300, "itm": 100, "name": "HCL TECH", "sector": "IT"},
    {"symbol": "SUNPHARMA.NS", "lot": 400, "itm": 20, "name": "SUN PHARMA", "sector": "PHARMA"},
    {"symbol": "MARUTI.NS", "lot": 150, "itm": 100, "name": "MARUTI SUZUKI", "sector": "AUTO"},
    {"symbol": "TATAMOTORS.NS", "lot": 350, "itm": 10, "name": "TATA MOTORS", "sector": "AUTO"},
    {"symbol": "TATASTEEL.NS", "lot": 600, "itm": 10, "name": "TATA STEEL", "sector": "METAL"},
    {"symbol": "POWERGRID.NS", "lot": 1200, "itm": 10, "name": "POWER GRID", "sector": "ENERGY"},
    {"symbol": "NTPC.NS", "lot": 1500, "itm": 10, "name": "NTPC", "sector": "ENERGY"},
    {"symbol": "ONGC.NS", "lot": 1500, "itm": 10, "name": "ONGC", "sector": "ENERGY"},
    {"symbol": "NESTLEIND.NS", "lot": 100, "itm": 200, "name": "NESTLE", "sector": "FMCG"},
    {"symbol": "TECHM.NS", "lot": 400, "itm": 50, "name": "TECH MAHINDRA", "sector": "IT"},
    {"symbol": "BAJAJFINSV.NS", "lot": 250, "itm": 100, "name": "BAJAJ FINSERV", "sector": "FINANCE"},
    {"symbol": "GRASIM.NS", "lot": 200, "itm": 50, "name": "GRASIM", "sector": "INFRA"},
    {"symbol": "INDUSINDBK.NS", "lot": 350, "itm": 50, "name": "INDUSIND BANK", "sector": "BANK"},
    {"symbol": "BRITANNIA.NS", "lot": 300, "itm": 50, "name": "BRITANNIA", "sector": "FMCG"},
    {"symbol": "HDFCLIFE.NS", "lot": 350, "itm": 50, "name": "HDFC LIFE", "sector": "FINANCE"},
    {"symbol": "SBILIFE.NS", "lot": 300, "itm": 50, "name": "SBI LIFE", "sector": "FINANCE"},
    {"symbol": "DRREDDY.NS", "lot": 200, "itm": 100, "name": "DR REDDY", "sector": "PHARMA"},
    {"symbol": "DIVISLAB.NS", "lot": 200, "itm": 100, "name": "DIVIS LAB", "sector": "PHARMA"},
]

# ================= Sector Mapping for Index =================
SECTOR_INDEX = {
    "BANK": "^NSEBANK",
    "IT": "^CNXIT",
    "AUTO": "^CNXAUTO",
    "PHARMA": "^CNXPHARMA",
    "METAL": "^CNXMETAL",
    "FMCG": "^CNXFMCG",
    "FINANCE": "^CNXFINANCE",
    "ENERGY": "^CNXENERGY",
    "INFRA": "^CNXINFRA",
    "DEFENCE": "^CNXINFRA",
    "HEALTHCARE": "^NIFTY_HEALTHCARE",
    "CONSUMER": "^NIFTY_CONSR_DURBL",
    "TELECOM": "^CNXIT",
    "CHEMICALS": "^CNXINFRA",
}

# ================= Session State =================
if "running" not in st.session_state:
    st.session_state.running = False
if "stock_trades" not in st.session_state:
    st.session_state.stock_trades = {}
    for stock in FO_STOCKS:
        qty, lots = calculate_trade_quantity(stock["lot"])
        st.session_state.stock_trades[stock["name"]] = {
            "buy_done": False,
            "sell_done": False,
            "trades": 0,
            "quantity": qty,
            "lots": lots
        }
if "last_trade_date" not in st.session_state:
    st.session_state.last_trade_date = get_ist_now().date()
if "daily_loss" not in st.session_state:
    st.session_state.daily_loss = 0
if "max_stocks_per_day" not in st.session_state:
    st.session_state.max_stocks_per_day = 10

# Reset daily trades
if get_ist_now().date() != st.session_state.last_trade_date:
    for stock in FO_STOCKS:
        qty, lots = calculate_trade_quantity(stock["lot"])
        st.session_state.stock_trades[stock["name"]] = {
            "buy_done": False,
            "sell_done": False,
            "trades": 0,
            "quantity": qty,
            "lots": lots
        }
    st.session_state.daily_loss = 0
    st.session_state.last_trade_date = get_ist_now().date()

MAX_DAILY_LOSS = 100000

# ================= Helper Functions =================
def get_sector_bullish(sector_name):
    try:
        index_symbol = SECTOR_INDEX.get(sector_name, "^NSEI")
        df = yf.download(index_symbol, period="7d", interval="15m", progress=False)
        if not df.empty and 'Close' in df.columns:
            ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
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
            return current < ema20
    except:
        pass
    return False

def get_stock_trend(symbol):
    try:
        df = yf.download(symbol, period="7d", interval="15m", progress=False)
        if df.empty:
            return "NEUTRAL"
        
        if 'Close' in df.columns:
            close = df['Close']
            ema9 = close.ewm(span=9).mean().iloc[-1]
            ema20 = close.ewm(span=20).mean().iloc[-1]
            
            # Calculate RSI for confirmation
            delta = close.diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1] if not rsi.isna().all() else 50
            
            # Volume filter
            volume = df['Volume'] if 'Volume' in df.columns else pd.Series([1000000])
            volume_sma = volume.rolling(20).mean().iloc[-1] if len(volume) > 20 else 1
            volume_filter = volume.iloc[-1] > volume_sma
            
            if ema9 > ema20 and current_rsi >= 55 and volume_filter:
                return "BULLISH"
            elif ema9 < ema20 and current_rsi <= 45 and volume_filter:
                return "BEARISH"
    except:
        pass
    return "NEUTRAL"

def get_nifty_trend():
    try:
        df = yf.download("^NSEI", period="7d", interval="15m", progress=False)
        if not df.empty and 'Close' in df.columns:
            ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
            if current > ema20:
                return "BULLISH"
            elif current < ema20:
                return "BEARISH"
    except:
        pass
    return "NEUTRAL"

def get_itm_strike(price, stock, option_type="CE"):
    itm_points = stock["itm"]
    if option_type == "CE":
        itm_strike = price - itm_points
    else:
        itm_strike = price + itm_points
    
    # Round to nearest strike based on price
    if itm_strike > 1000:
        itm_strike = round(itm_strike / 50) * 50
    elif itm_strike > 100:
        itm_strike = round(itm_strike / 10) * 10
    else:
        itm_strike = round(itm_strike / 5) * 5
    
    return int(itm_strike)

def get_option_premium(symbol, strike_price, option_type):
    """Option ची current premium मिळवते (approx using stock price)"""
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        if not df.empty and 'Close' in df.columns:
            stock_price = df['Close'].iloc[-1]
            if option_type == "CE":
                intrinsic_value = max(0, stock_price - strike_price)
            else:
                intrinsic_value = max(0, strike_price - stock_price)
            # Time value approx 10% of intrinsic value
            premium = intrinsic_value + (intrinsic_value * 0.1)
            return max(premium, 5)  # Minimum ₹5 premium
    except:
        pass
    return 50  # Default premium if can't fetch

def send_telegram(msg):
    token = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
    chat_id = "1983026913"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg}, timeout=15)
    except:
        pass

# ================= UI =================
st.markdown("<h1>📱 RUDRANSH PRO-ALGO - Multi Stock F&O</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#94a3b8;'>Scanning {len(FO_STOCKS)} F&O Stocks | Max Qty per Trade: {MAX_QTY_LIMIT} | Max Loss: ₹{MAX_DAILY_LOSS:,.0f}</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## 🎮 CONTROLS")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START", use_container_width=True):
            st.session_state.running = True
            send_telegram("🤖 MULTI-STOCK F&O ALGO STARTED")
            st.success("Algo Started!")
    with col2:
        if st.button("⏹️ STOP", use_container_width=True):
            st.session_state.running = False
            send_telegram("🛑 MULTI-STOCK F&O ALGO STOPPED")
            st.warning("Algo Stopped!")
    
    st.markdown("---")
    st.markdown("## ⚙️ SETTINGS")
    
    st.session_state.max_stocks_per_day = st.number_input("Max Stocks per Day", min_value=1, max_value=len(FO_STOCKS), value=10)
    
    st.markdown("---")
    st.markdown("### 📊 Daily Status")
    
    total_trades = sum([v["trades"] for v in st.session_state.stock_trades.values()])
    st.metric("Stocks Traded", f"{total_trades}/{st.session_state.max_stocks_per_day}")
    
    loss_color = "red" if st.session_state.daily_loss <= -MAX_DAILY_LOSS else "white"
    st.markdown(f"**Daily Loss:** <span style='color:{loss_color};'>₹{abs(st.session_state.daily_loss):,.0f}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📦 Auto Quantity (Max 1500)")
    st.caption("Lot size नुसार auto quantity calculate होईल")
    
    st.markdown("### 🎯 Premium Based TP/SL")
    st.caption("Premium नुसार SL/TP percentages auto adjust होतील")

# NIFTY Trend
nifty_trend = get_nifty_trend()
if nifty_trend == "BULLISH":
    st.success(f"🇮🇳 NIFTY TREND: BULLISH 🟢")
elif nifty_trend == "BEARISH":
    st.error(f"🇮🇳 NIFTY TREND: BEARISH 🔴")
else:
    st.info(f"🇮🇳 NIFTY TREND: SIDEWAYS 🟡")

st.markdown("---")

# Scan Stocks
st.markdown("## 🔍 SCANNING STOCKS...")

# Progress
progress_bar = st.progress(0)
status_text = st.empty()
results_container = st.container()

signals_found = []
total_scanned = len(FO_STOCKS)
trades_done = sum([v["trades"] for v in st.session_state.stock_trades.values()])
loss_limit_hit = abs(st.session_state.daily_loss) >= MAX_DAILY_LOSS

if loss_limit_hit:
    st.error(f"⚠️ DAILY LOSS LIMIT HIT (₹{MAX_DAILY_LOSS:,.0f})! Trading stopped for today. ⚠️")

for idx, stock in enumerate(FO_STOCKS):
    progress_bar.progress((idx + 1) / total_scanned)
    status_text.text(f"Scanning {stock['name']}...")
    
    if loss_limit_hit:
        break
    
    try:
        # Check if limit reached
        if trades_done >= st.session_state.max_stocks_per_day:
            status_text.text(f"Daily limit reached ({st.session_state.max_stocks_per_day} stocks)")
            break
        
        # Get stock price
        df = yf.download(stock["symbol"], period="1d", interval="5m", progress=False)
        if df.empty:
            continue
        
        current_price = df['Close'].iloc[-1]
        
        # Get trends
        sector_bullish = get_sector_bullish(stock["sector"])
        sector_bearish = get_sector_bearish(stock["sector"])
        stock_trend = get_stock_trend(stock["symbol"])
        
        stock_bullish = (stock_trend == "BULLISH")
        stock_bearish = (stock_trend == "BEARISH")
        
        trade_done = st.session_state.stock_trades[stock["name"]]["trades"] >= 1
        trade_qty = st.session_state.stock_trades[stock["name"]]["quantity"]
        trade_lots = st.session_state.stock_trades[stock["name"]]["lots"]
        
        # BUY Condition: NIFTY Bullish + Sector Bullish + Stock Bullish
        if nifty_trend == "BULLISH" and sector_bullish and stock_bullish and not trade_done:
            itm_strike = get_itm_strike(current_price, stock, "CE")
            
            # Get estimated premium and calculate TP/SL
            estimated_premium = get_option_premium(stock["symbol"], itm_strike, "CE")
            tp_sl = calculate_option_targets(estimated_premium, trade_qty)
            
            signals_found.append({
                "type": "BUY CE",
                "stock": stock["name"],
                "symbol": stock["symbol"],
                "price": current_price,
                "itm_strike": itm_strike,
                "lot": stock["lot"],
                "lots": trade_lots,
                "quantity": trade_qty,
                "itm_points": stock["itm"],
                "estimated_premium": estimated_premium,
                "tp_sl": tp_sl
            })
            
            if st.session_state.running:
                st.session_state.stock_trades[stock["name"]]["trades"] += 1
                st.session_state.stock_trades[stock["name"]]["buy_done"] = True
                trades_done += 1
                send_telegram(f"🔵 AUTO BUY {stock['name']} | {trade_lots} lots ({trade_qty} qty) | Strike: {itm_strike} CE | Premium: ₹{estimated_premium:.2f} | SL: {tp_sl['sl_percent']}% | TP1: {tp_sl['tp1_percent']}%")
        
        # SELL Condition: NIFTY Bearish + Sector Bearish + Stock Bearish
        elif nifty_trend == "BEARISH" and sector_bearish and stock_bearish and not trade_done:
            itm_strike = get_itm_strike(current_price, stock, "PE")
            
            # Get estimated premium and calculate TP/SL
            estimated_premium = get_option_premium(stock["symbol"], itm_strike, "PE")
            tp_sl = calculate_option_targets(estimated_premium, trade_qty)
            
            signals_found.append({
                "type": "SELL PE",
                "stock": stock["name"],
                "symbol": stock["symbol"],
                "price": current_price,
                "itm_strike": itm_strike,
                "lot": stock["lot"],
                "lots": trade_lots,
                "quantity": trade_qty,
                "itm_points": stock["itm"],
                "estimated_premium": estimated_premium,
                "tp_sl": tp_sl
            })
            
            if st.session_state.running:
                st.session_state.stock_trades[stock["name"]]["trades"] += 1
                st.session_state.stock_trades[stock["name"]]["sell_done"] = True
                trades_done += 1
                send_telegram(f"🔴 AUTO SELL {stock['name']} | {trade_lots} lots ({trade_qty} qty) | Strike: {itm_strike} PE | Premium: ₹{estimated_premium:.2f} | SL: {tp_sl['sl_percent']}% | TP1: {tp_sl['tp1_percent']}%")
                
    except Exception as e:
        continue

progress_bar.empty()
status_text.empty()

# Display Results
with results_container:
    if signals_found:
        st.success(f"✅ Found {len(signals_found)} Trading Opportunities!")
        
        for signal in signals_found:
            tp_sl = signal["tp_sl"]
            if signal["type"] == "BUY CE":
                st.markdown(f"""
                <div style='background:#1e293b; padding:15px; border-radius:10px; margin:10px 0; border-left:5px solid #00ff88;'>
                    <b>🟢 {signal['stock']}</b><br>
                    Action: <span style='color:#00ff88;'>{signal['type']}</span><br>
                    Stock Price: ₹{signal['price']:.2f} | ITM Strike: {signal['itm_strike']} CE ({signal['itm_points']} points ITM)<br>
                    Estimated Premium: ₹{signal['estimated_premium']:.2f}<br>
                    <span style='color:#ffaa00;'>🎯 Premium Based TP/SL:</span><br>
                    &nbsp;&nbsp;• SL: {tp_sl['sl_percent']}% = ₹{tp_sl['sl']:.2f} (Loss: ₹{tp_sl['sl_loss']:.0f})<br>
                    &nbsp;&nbsp;• TP1: {tp_sl['tp1_percent']}% = ₹{tp_sl['tp1']:.2f} (Profit: ₹{tp_sl['tp1_profit']:.0f}) - 50% qty<br>
                    &nbsp;&nbsp;• TP2: {tp_sl['tp2_percent']}% = ₹{tp_sl['tp2']:.2f} (Profit: ₹{tp_sl['tp2_profit']:.0f}) - 25% qty<br>
                    &nbsp;&nbsp;• TP3: {tp_sl['tp3_percent']}% = ₹{tp_sl['tp3']:.2f} (Profit: ₹{tp_sl['tp3_profit']:.0f}) - 25% qty<br>
                    &nbsp;&nbsp;💰 Total Potential Profit: ₹{tp_sl['total_profit']:.0f}<br>
                    Lot Size: {signal['lot']} | <span style='color:#ffaa00;'>Lots: {signal['lots']} | Quantity: {signal['quantity']} (Max {MAX_QTY_LIMIT})</span><br>
                    <span style='color:#00ff88;'>✅ Condition: NIFTY Bullish + {signal['stock'].split()[0]} Sector Bullish + Stock Bullish</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background:#1e293b; padding:15px; border-radius:10px; margin:10px 0; border-left:5px solid #ff4b4b;'>
                    <b>🔴 {signal['stock']}</b><br>
                    Action: <span style='color:#ff4b4b;'>{signal['type']}</span><br>
                    Stock Price: ₹{signal['price']:.2f} | ITM Strike: {signal['itm_strike']} PE ({signal['itm_points']} points ITM)<br>
                    Estimated Premium: ₹{signal['estimated_premium']:.2f}<br>
                    <span style='color:#ffaa00;'>🎯 Premium Based TP/SL:</span><br>
                    &nbsp;&nbsp;• SL: {tp_sl['sl_percent']}% = ₹{tp_sl['sl']:.2f} (Loss: ₹{tp_sl['sl_loss']:.0f})<br>
                    &nbsp;&nbsp;• TP1: {tp_sl['tp1_percent']}% = ₹{tp_sl['tp1']:.2f} (Profit: ₹{tp_sl['tp1_profit']:.0f}) - 50% qty<br>
                    &nbsp;&nbsp;• TP2: {tp_sl['tp2_percent']}% = ₹{tp_sl['tp2']:.2f} (Profit: ₹{tp_sl['tp2_profit']:.0f}) - 25% qty<br>
                    &nbsp;&nbsp;• TP3: {tp_sl['tp3_percent']}% = ₹{tp_sl['tp3']:.2f} (Profit: ₹{tp_sl['tp3_profit']:.0f}) - 25% qty<br>
                    &nbsp;&nbsp;💰 Total Potential Profit: ₹{tp_sl['total_profit']:.0f}<br>
                    Lot Size: {signal['lot']} | <span style='color:#ffaa00;'>Lots: {signal['lots']} | Quantity: {signal['quantity']} (Max {MAX_QTY_LIMIT})</span><br>
                    <span style='color:#ff4b4b;'>✅ Condition: NIFTY Bearish + {signal['stock'].split()[0]} Sector Bearish + Stock Bearish</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📭 No trading opportunities found at this moment.")

# Daily Trades Summary
st.markdown("---")
st.markdown("### 📊 Today's Executed Trades")

trade_data = []
for stock in FO_STOCKS:
    status = st.session_state.stock_trades[stock["name"]]
    if status["trades"] > 0:
        trade_data.append({
            "Stock": stock["name"],
            "Lots": status["lots"],
            "Quantity": status["quantity"],
            "Buy CE": "✅" if status["buy_done"] else "❌",
            "Sell PE": "✅" if status["sell_done"] else "❌"
        })

if trade_data:
    st.dataframe(pd.DataFrame(trade_data), use_container_width=True)
    st.caption(f"📌 Max Quantity Limit: {MAX_QTY_LIMIT} per trade | Lot size नुसार auto quantity calculate केली जाते | SL/TP Premium नुसार auto adjust होते")
else:
    st.info("No trades executed today.")

# Status
st.markdown("---")
if loss_limit_hit:
    st.error(f"⚠️ DAILY LOSS LIMIT HIT (₹{MAX_DAILY_LOSS:,.0f})! Trading stopped for today. ⚠️")
elif st.session_state.running:
    st.success(f"🟢 ALGO RUNNING | Max Stocks: {st.session_state.max_stocks_per_day}/day | Max Qty: {MAX_QTY_LIMIT}")
else:
    st.warning("🔴 ALGO STOPPED")

# Premium Based TP/SL Info
st.markdown("---")
st.markdown("### 🎯 Premium Based TP/SL Table")

premium_table = pd.DataFrame([
    {"Premium Range": "₹10 - ₹50", "SL %": "30%", "TP1 %": "20%", "TP2 %": "40%", "TP3 %": "60%"},
    {"Premium Range": "₹51 - ₹150", "SL %": "25%", "TP1 %": "15%", "TP2 %": "30%", "TP3 %": "50%"},
    {"Premium Range": "₹151 - ₹300", "SL %": "20%", "TP1 %": "12%", "TP2 %": "25%", "TP3 %": "40%"},
    {"Premium Range": "₹301 - ₹500", "SL %": "15%", "TP1 %": "10%", "TP2 %": "20%", "TP3 %": "30%"},
    {"Premium Range": "₹501 - ₹1000", "SL %": "12%", "TP1 %": "8%", "TP2 %": "15%", "TP3 %": "25%"},
    {"Premium Range": "₹1000+", "SL %": "10%", "TP1 %": "6%", "TP2 %": "12%", "TP3 %": "20%"},
])
st.dataframe(premium_table, use_container_width=True)
st.caption("📌 Entry Premium नुसार SL आणि TP percentages auto adjust होतील | Quantity Booking: TP1: 50%, TP2: 25%, TP3: 25%")

# Clock
st.caption(f"🕐 IST: {get_ist_now().strftime('%H:%M:%S')} | Auto Refresh every 60 seconds")
st_autorefresh(interval=60000, key="auto_refresh")
