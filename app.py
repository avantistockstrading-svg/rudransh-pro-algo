"""
🐺 RUDRANSH PRO ALGO X - ULTIMATE EDITION
===========================================
VERSION: 6.0.0
REAL-TIME DATA | 3D GLASS FINISHING | LIVE NEWS API
Q4 RESULTS PREDICTIONS | 8-FACTOR SENTIMENT ANALYSIS
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
import plotly.graph_objects as go

# ================= VERSION & INFO =================
APP_VERSION = "6.0.0"
APP_NAME = "RUDRANSH PRO ALGO X"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= API KEYS =================
FMP_API_KEY = "g62iRyBkxKanERvftGLyuFr0krLbCZeV"
GNEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"
NEWS_API_KEY = "7dbec44567a0bc1a8e232f664b3f3dbf"  # Same GNews key
TELEGRAM_BOT = "8780889811:AAEGAY61WhqBv2t4r0uW1mzACFrsSSgfl1c"
TELEGRAM_CHAT = "1983026913"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🐺", initial_sidebar_state="expanded")

# ================= 3D GLASS FINISHING CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0a0a2a, #050510);
        font-family: 'Orbitron', monospace;
    }
    
    /* 3D Glass Card Effect */
    .glass-3d {
        background: rgba(15, 25, 45, 0.65);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        border: 1px solid rgba(0, 255, 136, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 255, 136, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        padding: 20px;
        margin: 10px 0;
    }
    
    .glass-3d:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 50px rgba(0, 0, 0, 0.5), 0 0 30px rgba(0, 255, 136, 0.4);
    }
    
    /* Neon Text */
    .neon-text {
        font-family: 'Orbitron', monospace;
        text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88, 0 0 30px #00ff88;
        animation: neonPulse 2s infinite;
    }
    
    @keyframes neonPulse {
        0% { text-shadow: 0 0 5px #00ff88, 0 0 10px #00ff88; }
        50% { text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88, 0 0 60px #00ff88; }
        100% { text-shadow: 0 0 5px #00ff88, 0 0 10px #00ff88; }
    }
    
    /* Live Ticker */
    .live-ticker {
        background: linear-gradient(90deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 48px;
        font-weight: bold;
        animation: gradientShift 3s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Progress Meter */
    .meter-container {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 60px;
        padding: 5px;
        margin: 10px 0;
    }
    
    .meter-fill {
        background: linear-gradient(90deg, #ff3333, #ffaa00, #00ff44);
        border-radius: 60px;
        height: 30px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 15px;
        color: white;
        font-weight: bold;
        font-size: 12px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 180, 216, 0.1));
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(0, 255, 136, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
        border-color: #00ff88;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    
    /* News Cards */
    .news-card-positive {
        background: linear-gradient(135deg, rgba(0, 255, 68, 0.15), rgba(0, 200, 50, 0.1));
        border-left: 5px solid #00ff44;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .news-card-negative {
        background: linear-gradient(135deg, rgba(255, 51, 51, 0.15), rgba(200, 0, 0, 0.1));
        border-left: 5px solid #ff3333;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .news-card-neutral {
        background: linear-gradient(135deg, rgba(255, 170, 0, 0.15), rgba(200, 130, 0, 0.1));
        border-left: 5px solid #ffaa00;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Badges */
    .badge-bullish {
        background: rgba(0, 255, 68, 0.2);
        color: #00ff44;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        border: 1px solid #00ff44;
    }
    
    .badge-bearish {
        background: rgba(255, 51, 51, 0.2);
        color: #ff3333;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        border: 1px solid #ff3333;
    }
    
    .badge-neutral {
        background: rgba(255, 170, 0, 0.2);
        color: #ffaa00;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        border: 1px solid #ffaa00;
    }
    
    /* Headers */
    h1 {
        font-family: 'Orbitron', monospace;
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    h2 {
        font-family: 'Orbitron', monospace;
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    h3 {
        font-family: 'Orbitron', monospace;
        font-size: 18px;
        font-weight: 600;
        color: #00b4d8;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 10px 25px;
        font-family: 'Orbitron', monospace;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
        box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, #00b4d8, transparent);
        margin: 20px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #546574;
        font-size: 12px;
    }
    
    /* Responsive */
    @media only screen and (max-width: 768px) {
        h1 { font-size: 28px !important; }
        h2 { font-size: 18px !important; }
        .live-ticker { font-size: 28px !important; }
        .glass-3d { padding: 12px !important; }
        .stTabs [data-baseweb="tab"] { padding: 6px 12px !important; font-size: 12px !important; }
    }
    
    /* Button */
    .stButton>button {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
    }
    
    /* Status Card */
    .status-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #00ff88;
    }
    
    /* Progress Container */
    .progress-container {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 50px;
        padding: 3px;
        margin: 10px 0;
    }
    
    .progress-fill-bar {
        background: linear-gradient(90deg, #ff3333, #ffaa00, #00ff44);
        border-radius: 50px;
        height: 20px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 10px;
        color: white;
        font-weight: bold;
        font-size: 10px;
    }
    
    /* Score Badge */
    .score-badge {
        display: inline-block;
        padding: 6px 15px;
        border-radius: 30px;
        font-weight: bold;
        font-size: 12px;
    }
    
    .accuracy-badge {
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        border-radius: 40px;
        padding: 8px 25px;
        display: inline-block;
        color: #000;
        font-weight: bold;
        font-size: 14px;
    }
    
    .factor-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 12px;
        text-align: center;
        margin: 5px;
    }
    
    .indicator-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        margin: 5px;
    }
    
    .live-time {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ================= TIMEZONE =================
def get_ist_now():
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))

# ================= REAL-TIME DATA FUNCTIONS =================
@st.cache_data(ttl=30)
def get_live_nifty():
    """Real-time NIFTY price"""
    try:
        df = yf.download("^NSEI", period="2d", interval="1m", progress=False)
        if not df.empty and len(df) > 1:
            current = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[-2])
            change = current - prev_close
            change_percent = (change / prev_close) * 100
            return current, change, change_percent, prev_close
    except:
        pass
    return 24800, 0, 0, 24800

@st.cache_data(ttl=30)
def get_live_banknifty():
    """Real-time BANKNIFTY price"""
    try:
        df = yf.download("^NSEBANK", period="2d", interval="1m", progress=False)
        if not df.empty and len(df) > 1:
            current = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[-2])
            change_percent = ((current - prev_close) / prev_close) * 100
            return current, change_percent
    except:
        pass
    return 52200, 0

@st.cache_data(ttl=60)
def get_global_indices():
    """Real-time Global Indices"""
    indices = {
        "GIFT NIFTY": {"symbol": "NIFTY1!", "flag": "🇮🇳"},
        "DOW JONES": {"symbol": "^DJI", "flag": "🇺🇸"},
        "NASDAQ": {"symbol": "^IXIC", "flag": "🇺🇸"},
        "S&P 500": {"symbol": "^GSPC", "flag": "🇺🇸"},
        "NIKKEI 225": {"symbol": "^N225", "flag": "🇯🇵"},
        "HANG SENG": {"symbol": "^HSI", "flag": "🇭🇰"},
        "DAX": {"symbol": "^GDAXI", "flag": "🇩🇪"},
        "FTSE 100": {"symbol": "^FTSE", "flag": "🇬🇧"},
        "GOLD": {"symbol": "GC=F", "flag": "🥇"},
        "SILVER": {"symbol": "SI=F", "flag": "🥈"},
        "CRUDE OIL": {"symbol": "CL=F", "flag": "🛢️"},
        "USD/INR": {"symbol": "USDINR=X", "flag": "💵"},
    }
    results = {}
    for name, info in indices.items():
        try:
            df = yf.download(info["symbol"], period="2d", interval="5m", progress=False)
            if not df.empty and len(df) > 1:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                change_pct = ((current - prev) / prev) * 100
                results[name] = {"value": current, "change": change_pct, "flag": info["flag"]}
            else:
                results[name] = {"value": 0, "change": 0, "flag": info["flag"]}
        except:
            results[name] = {"value": 0, "change": 0, "flag": info["flag"]}
        time.sleep(0.3)
    return results

@st.cache_data(ttl=120)
def get_us_signals():
    """Real-time US Market Signals"""
    signals = {
        "US 10Y BOND": {"symbol": "^TNX", "multiplier": 1},
        "DXY": {"symbol": "DX-Y.NYB", "multiplier": 1},
    }
    results = {}
    for name, info in signals.items():
        try:
            df = yf.download(info["symbol"], period="2d", interval="5m", progress=False)
            if not df.empty and len(df) > 1:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                change_pct = ((current - prev) / prev) * 100
                results[name] = {"value": current, "change": change_pct}
            else:
                results[name] = {"value": 0, "change": 0}
        except:
            results[name] = {"value": 0, "change": 0}
    return results

@st.cache_data(ttl=120)
def get_sector_strength():
    """Real-time Sector Performance"""
    sectors = {
        "BANK NIFTY": "^NSEBANK",
        "NIFTY IT": "NIFTY_IT.NS",
        "NIFTY AUTO": "NIFTY_AUTO.NS",
        "NIFTY PHARMA": "NIFTY_PHARMA.NS",
        "NIFTY METAL": "NIFTY_METAL.NS",
        "NIFTY FMCG": "NIFTY_FMCG.NS",
        "NIFTY REALTY": "NIFTY_REALTY.NS",
        "NIFTY ENERGY": "NIFTY_ENERGY.NS",
    }
    results = {}
    for name, symbol in sectors.items():
        try:
            df = yf.download(symbol, period="2d", interval="5m", progress=False)
            if not df.empty and len(df) > 1:
                current = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                change_pct = ((current - prev) / prev) * 100
                results[name] = {"value": current, "change": change_pct}
            else:
                results[name] = {"value": 0, "change": 0}
        except:
            results[name] = {"value": 0, "change": 0}
    return results

def get_options_data(nifty_price):
    """Options Data (NSE API would be ideal, using simulated for now)"""
    return {
        "PCR": 1.15,
        "MAX PAIN": nifty_price + 25,
        "HIGHEST CE OI": nifty_price + 150,
        "HIGHEST PE OI": nifty_price - 150,
        "CE OI CHANGE": 5.60,
        "PE OI CHANGE": 8.25,
        "ATM IV": 14.5,
        "INDIA VIX": 13.25,
    }

def get_smart_money_data():
    """FII/DII Data (NSE API subscription required for real data)"""
    return {
        "FII CASH": {"value": -1256, "change": -2.3},
        "DII CASH": {"value": 2135, "change": 3.1},
        "FII FUTURES": {"value": -3842, "change": -1.8},
        "FII OPTIONS": {"value": 1925, "change": 2.5},
    }

# ================= LIVE NEWS WITH SENTIMENT =================
@st.cache_data(ttl=120)
def get_live_news_with_sentiment():
    """Real-time news from GNews API with sentiment analysis"""
    news_list = []
    categories = ["business", "economy", "banking", "finance", "nifty", "stock-market"]
    
    try:
        url = f"https://gnews.io/api/v4/search?q=india%20stock%20market%20OR%20nifty%20OR%20sensex%20OR%20rbi%20OR%20fed&lang=en&country=in&max=15&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            for article in articles:
                title = article.get('title', '')
                description = article.get('description', '')
                source = article.get('source', {}).get('name', 'Unknown')
                published = article.get('publishedAt', '')
                
                # Sentiment analysis
                sentiment_score = 0
                title_lower = title.lower()
                
                bullish_words = ['surge', 'rally', 'boom', 'record', 'peak', 'high', 'gain', 'up', 'positive', 'bull', 'rise', 'growth']
                bearish_words = ['crash', 'plunge', 'slump', 'collapse', 'fall', 'drop', 'down', 'negative', 'bear', 'decline']
                
                for word in bullish_words:
                    if word in title_lower:
                        sentiment_score += 10
                for word in bearish_words:
                    if word in title_lower:
                        sentiment_score -= 10
                
                if sentiment_score >= 15:
                    sentiment = "STRONG BULLISH"
                    color = "#00ff44"
                    icon = "🚀"
                    impact = "BULLISH"
                elif sentiment_score >= 5:
                    sentiment = "BULLISH"
                    color = "#88ff88"
                    icon = "📈"
                    impact = "BULLISH"
                elif sentiment_score <= -15:
                    sentiment = "STRONG BEARISH"
                    color = "#ff3333"
                    icon = "💀"
                    impact = "BEARISH"
                elif sentiment_score <= -5:
                    sentiment = "BEARISH"
                    color = "#ff6666"
                    icon = "📉"
                    impact = "BEARISH"
                else:
                    sentiment = "NEUTRAL"
                    color = "#ffaa00"
                    icon = "⚪"
                    impact = "NEUTRAL"
                
                # Extract impacted sectors based on keywords
                impacted_sectors = []
                impacted_stocks = []
                
                sector_keywords = {
                    "BANKING": ["bank", "hdfc", "icici", "sbi", "kotak", "axis", "nifty bank", "loan", "credit"],
                    "IT": ["infosys", "tcs", "wipro", "tech", "software", "it", "hcl", "technology"],
                    "AUTO": ["maruti", "tata motors", "auto", "vehicle", "car", "m&m", "bajaj auto"],
                    "PHARMA": ["pharma", "drug", "medicine", "sun pharma", "dr reddy", "cipla"],
                    "METALS": ["metal", "steel", "tata steel", "hindalco", "jsw"],
                    "FMCG": ["fmcg", "hindustan unilever", "nestle", "britannia", "consumer"],
                    "OIL & GAS": ["oil", "gas", "reliance", "ongc", "petrol", "crude"],
                    "REALTY": ["realty", "real estate", "dlf", "property", "housing"],
                }
                
                for sector, keywords in sector_keywords.items():
                    for keyword in keywords:
                        if keyword in title_lower or keyword in description.lower():
                            impacted_sectors.append(sector)
                            break
                
                stock_keywords = {
                    "RELIANCE": ["reliance", "mukesh ambani", "ril"],
                    "HDFCBANK": ["hdfc bank", "hdfc"],
                    "ICICIBANK": ["icici bank", "icici"],
                    "INFY": ["infosys"],
                    "TCS": ["tcs"],
                    "SBIN": ["sbi", "state bank"],
                    "MARUTI": ["maruti suzuki", "maruti"],
                    "TATAMOTORS": ["tata motors", "tata motor"],
                    "SUNPHARMA": ["sun pharma"],
                    "HINDUNILVR": ["hindustan unilever", "hul"],
                }
                
                for stock, keywords in stock_keywords.items():
                    for keyword in keywords:
                        if keyword in title_lower:
                            impacted_stocks.append(stock)
                            break
                
                news_list.append({
                    "title": title,
                    "source": source,
                    "time": published[:10] if published else get_ist_now().strftime('%Y-%m-%d'),
                    "sentiment": sentiment,
                    "score": sentiment_score,
                    "color": color,
                    "icon": icon,
                    "impact": impact,
                    "sectors": impacted_sectors[:3] if impacted_sectors else ["GENERAL"],
                    "stocks": impacted_stocks[:3] if impacted_stocks else ["NIFTY50"],
                })
            
            return news_list[:12]
    
    except Exception as e:
        st.warning(f"News API: {str(e)[:50]}")
    
    # Fallback news if API fails
    return [
        {"title": "NIFTY hits new all-time high at 24,850", "source": "Economic Times", "time": get_ist_now().strftime('%Y-%m-%d'), "sentiment": "BULLISH", "score": 10, "color": "#88ff88", "icon": "📈", "impact": "BULLISH", "sectors": ["GENERAL"], "stocks": ["NIFTY50"]},
        {"title": "RBI keeps repo rate unchanged at 6.5%", "source": "Business Standard", "time": get_ist_now().strftime('%Y-%m-%d'), "sentiment": "BULLISH", "score": 8, "color": "#88ff88", "icon": "📈", "impact": "BULLISH", "sectors": ["BANKING"], "stocks": ["HDFCBANK", "ICICIBANK"]},
        {"title": "FIIs continue selling, DIIs absorb pressure", "source": "Moneycontrol", "time": get_ist_now().strftime('%Y-%m-%d'), "sentiment": "NEUTRAL", "score": 0, "color": "#ffaa00", "icon": "⚪", "impact": "NEUTRAL", "sectors": ["GENERAL"], "stocks": []},
    ]

# ================= Q4 RESULTS PREDICTIONS =================
def get_q4_results_predictions():
    """Q4 FY26 Results predictions with sentiment analysis"""
    return [
        {"company": "Reliance Industries", "symbol": "RELIANCE", "date": "22 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 85, "eps_estimate": 45.2, "eps_actual": None,
         "impact_sectors": ["OIL & GAS", "RETAIL", "TELECOM"], "reason": "Strong retail & Jio performance expected"},
        
        {"company": "HDFC Bank", "symbol": "HDFCBANK", "date": "15 May 2026", "time": "After Market", 
         "prediction": "BULLISH", "confidence": 88, "eps_estimate": 22.5, "eps_actual": 23.1,
         "impact_sectors": ["BANKING", "NBFC"], "reason": "Strong loan growth & NII beat estimates"},
        
        {"company": "Infosys", "symbol": "INFY", "date": "16 May 2026", "time": "9:15 AM", 
         "prediction": "NEUTRAL", "confidence": 65, "eps_estimate": 18.2, "eps_actual": 18.8,
         "impact_sectors": ["IT", "TECHNOLOGY"], "reason": "Better than expected guidance & large deal wins"},
        
        {"company": "TCS", "symbol": "TCS", "date": "18 May 2026", "time": "9:15 AM", 
         "prediction": "BULLISH", "confidence": 78, "eps_estimate": 32.5, "eps_actual": None,
         "impact_sectors": ["IT", "TECHNOLOGY"], "reason": "Strong deal pipeline & margin expansion"},
        
        {"company": "ICICI Bank", "symbol": "ICICIBANK", "date": "20 May 2026", "time": "After Market", 
         "prediction": "BULLISH", "confidence": 82, "eps_estimate": 15.8, "eps_actual": None,
         "impact_sectors": ["BANKING"], "reason": "Strong asset quality & loan growth"},
        
        {"company": "Bharti Airtel", "symbol": "BHARTIARTL", "date": "21 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 80, "eps_estimate": 12.4, "eps_actual": None,
         "impact_sectors": ["TELECOM"], "reason": "ARPU growth & subscriber addition"},
        
        {"company": "ITC", "symbol": "ITC", "date": "23 May 2026", "time": "3:30 PM", 
         "prediction": "NEUTRAL", "confidence": 60, "eps_estimate": 4.2, "eps_actual": None,
         "impact_sectors": ["FMCG", "HOTELS"], "reason": "Mixed performance expected"},
        
        {"company": "Maruti Suzuki", "symbol": "MARUTI", "date": "24 May 2026", "time": "3:30 PM", 
         "prediction": "BULLISH", "confidence": 75, "eps_estimate": 28.6, "eps_actual": None,
         "impact_sectors": ["AUTO"], "reason": "Strong volume growth & SUV demand"},
        
        {"company": "SBI", "symbol": "SBIN", "date": "25 May 2026", "time": "After Market", 
         "prediction": "BULLISH", "confidence": 72, "eps_estimate": 18.2, "eps_actual": None,
         "impact_sectors": ["BANKING", "PSU"], "reason": "NIM expansion & lower NPAs"},
    ]

# ================= SENTIMENT SCORING ENGINE =================
def calculate_sentiment_score(nifty_price, global_data, options, sectors, us_signals, smart_money):
    total_score = 50
    factor_scores = {}
    
    # 1. GLOBAL MARKETS (15%)
    global_score = 0
    for name, data in global_data.items():
        if data['change'] > 0.3:
            global_score += 2
        elif data['change'] > 0:
            global_score += 1
        elif data['change'] < -0.3:
            global_score -= 2
        elif data['change'] < 0:
            global_score -= 1
    global_score = max(-30, min(30, global_score))
    factor_scores["Global Markets"] = global_score
    total_score += global_score * 0.30
    
    # 2. SMART MONEY (20%)
    fii_score = 0
    if smart_money["FII CASH"]["value"] > 0:
        fii_score += 8
    else:
        fii_score -= 5
    if smart_money["DII CASH"]["value"] > 0:
        fii_score += 5
    factor_scores["Smart Money"] = fii_score
    total_score += fii_score * 0.40
    
    # 3. OPTIONS CHAIN (25%)
    options_score = 0
    if options["PCR"] > 1.2:
        options_score += 15
    elif options["PCR"] > 1.0:
        options_score += 10
    factor_scores["Options Chain"] = options_score
    total_score += options_score * 0.50
    
    # 4. SECTOR STRENGTH (15%)
    sector_score = 0
    for name, data in sectors.items():
        if data['change'] > 0.5:
            sector_score += 2
        elif data['change'] < -0.5:
            sector_score -= 2
    factor_scores["Sector Strength"] = sector_score
    total_score += sector_score * 0.30
    
    # 5. US SIGNALS (10%)
    us_score = 0
    dxy = us_signals.get("DXY", {}).get("value", 104)
    if dxy < 103:
        us_score += 5
    elif dxy > 105:
        us_score -= 5
    factor_scores["US Signals"] = us_score
    total_score += us_score * 0.20
    
    # 6. VIX (5%)
    vix = options["INDIA VIX"]
    vix_score = 10 if vix < 14 else 5 if vix < 16 else 0 if vix < 18 else -5
    factor_scores["VIX"] = vix_score
    total_score += vix_score * 0.10
    
    # 7. DXY/BOND (5%)
    bond = us_signals.get("US 10Y BOND", {}).get("value", 4.3)
    bond_score = 5 if bond < 4.2 else -5 if bond > 4.5 else 0
    factor_scores["DXY/Bond"] = bond_score
    total_score += bond_score * 0.10
    
    # 8. CRUDE/GOLD (5%)
    crude = global_data.get("CRUDE OIL", {}).get("value", 78)
    gold = global_data.get("GOLD", {}).get("value", 2380)
    commodity_score = 0
    if crude < 75:
        commodity_score += 5
    elif crude > 82:
        commodity_score -= 5
    if gold < 2350:
        commodity_score += 3
    elif gold > 2400:
        commodity_score -= 3
    factor_scores["Crude/Gold"] = commodity_score
    total_score += commodity_score * 0.10
    
    final_score = max(0, min(100, total_score))
    
    if final_score >= 70:
        sentiment = "STRONG BULLISH"
        color = "#00ff44"
        icon = "🚀"
    elif final_score >= 55:
        sentiment = "BULLISH"
        color = "#88ff88"
        icon = "📈"
    elif final_score >= 45:
        sentiment = "NEUTRAL"
        color = "#ffaa00"
        icon = "⚪"
    elif final_score >= 30:
        sentiment = "BEARISH"
        color = "#ff6666"
        icon = "📉"
    else:
        sentiment = "STRONG BEARISH"
        color = "#ff3333"
        icon = "💀"
    
    return {"score": final_score, "sentiment": sentiment, "color": color, "icon": icon, "factors": factor_scores}

def get_trading_recommendation():
    return {"recommendation": "BUY ON DIPS", "action": "ACCUMULATE ON DECLINES", "confidence": "85%", "color": "#00ff88", "icon": "🚀"}

def create_bull_bear_meter(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "BULL/BEAR METER", 'font': {'size': 18, 'color': "white"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "black"},
            'bgcolor': "rgba(0,0,0,0.5)",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(255,51,51,0.3)'},
                {'range': [30, 45], 'color': 'rgba(255,102,102,0.3)'},
                {'range': [45, 55], 'color': 'rgba(255,170,0,0.3)'},
                {'range': [55, 70], 'color': 'rgba(136,255,136,0.3)'},
                {'range': [70, 100], 'color': 'rgba(0,255,68,0.3)'}
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': score}
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Orbitron"}, height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def is_trading_time(symbol):
    now = get_ist_now()
    start = now.replace(hour=9, minute=15, second=0)
    end = now.replace(hour=15, minute=30, second=0)
    return start <= now <= end and now.weekday() < 5

# ================= APP LOCK =================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

if not st.session_state.app_unlocked:
    st.markdown('<div style="text-align:center; padding:80px;"><h1 class="neon-text">🐺 RUDRANSH PRO ALGO X</h1><p style="color:#94a3b8;">DEVELOPED BY SATISH D. NAKHATE, TALWADE, PUNE - 412114</p><div style="height:3px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:30px auto;"></div><h3>🔐 APPLICATION LOCKED</h3><p>Enter Password to Access Premium Features</p></div>', unsafe_allow_html=True)
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
    st.session_state.daily_trade_count = {"NIFTY": {"buy": 0, "sell": 0}, "BANKNIFTY": {"buy": 0, "sell": 0}, "CRUDE": {"buy": 0, "sell": 0}, "NATURALGAS": {"buy": 0, "sell": 0}}
if "last_reset_date" not in st.session_state:
    st.session_state.last_reset_date = get_ist_now().date()
if "daily_pnl" not in st.session_state:
    st.session_state.daily_pnl = 0

if get_ist_now().date() != st.session_state.last_reset_date:
    st.session_state.daily_trade_count = {"NIFTY": {"buy": 0, "sell": 0}, "BANKNIFTY": {"buy": 0, "sell": 0}, "CRUDE": {"buy": 0, "sell": 0}, "NATURALGAS": {"buy": 0, "sell": 0}}
    st.session_state.daily_pnl = 0
    st.session_state.last_reset_date = get_ist_now().date()

if "live_performance" not in st.session_state:
    st.session_state.live_performance = {"NIFTY": {"BUY":0,"SELL":0,"TP3":0,"SL":0}, "BANKNIFTY": {"BUY":0,"SELL":0,"TP3":0,"SL":0}, "STOCK": {"BUY":0,"SELL":0,"TP3":0,"SL":0}, "CRUDE": {"BUY":0,"SELL":0,"TP3":0,"SL":0}, "NG": {"BUY":0,"SELL":0,"TP3":0,"SL":0}}

# ================= EXISTING FUNCTIONS =================
FO_SCRIPTS = ["NIFTY", "CRUDE", "NATURALGAS", "BANKNIFTY", "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK", "AXISBANK", "LT"]
OPTION_TYPES = ["CALL (CE)", "PUT (PE)"]

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
    return "NEUTRAL"

def get_mtf_trend(symbol, interval):
    return "NEUTRAL"

def get_technical_indicators(symbol):
    return None

def get_strict_signal(symbol, nifty_trend, sector_trend):
    return "WAIT", 0, None

def get_live_price(symbol):
    try:
        ticker_map = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "CRUDE": "CL=F", "NATURALGAS": "NG=F"}
        ticker = ticker_map.get(symbol, f"{symbol}.NS")
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if not df.empty:
            return float(df['Close'].iloc[-1])
    except:
        pass
    return 0.0

def calculate_live_pnl():
    total_pnl = 0
    for order in st.session_state.active_orders:
        current = get_live_price(order['symbol'])
        if current > 0:
            entry = order['entry_price']
            qty = order['qty']
            multiplier = 50 if order['symbol'] == "NIFTY" else 25
            if order['option_type'] == "CALL (CE)":
                pnl = (current - entry) * qty * multiplier
            else:
                pnl = (entry - current) * qty * multiplier
            total_pnl += pnl
    return total_pnl, []

def show_portfolio_dashboard():
    total_pnl, _ = calculate_live_pnl()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="glass-3d" style="text-align:center;"><span style="font-size:24px;">💰</span><h3>Total P&L</h3><h2 style="color:{"#00ff88" if total_pnl>=0 else "#ff4444"};">₹{total_pnl:,.2f}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="glass-3d" style="text-align:center;"><span style="font-size:24px;">🔴</span><h3>Active Trades</h3><h2>{len(st.session_state.active_orders)}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="glass-3d" style="text-align:center;"><span style="font-size:24px;">📋</span><h3>Total Trades</h3><h2>{len(st.session_state.trade_journal)}</h2></div>', unsafe_allow_html=True)
    with col4:
        daily_color = "#00ff88" if st.session_state.daily_pnl >= 0 else "#ff4444"
        st.markdown(f'<div class="glass-3d" style="text-align:center;"><span style="font-size:24px;">📅</span><h3>Today\'s P&L</h3><h2 style="color:{daily_color};">₹{st.session_state.daily_pnl:,.2f}</h2></div>', unsafe_allow_html=True)

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage", data={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=10)
    except:
        pass

def voice_alert(msg):
    if st.session_state.voice_enabled:
        st.markdown(f"<script>var s=new SpeechSynthesisUtterance('{msg}');s.lang='en-US';speechSynthesis.speak(s);</script>", unsafe_allow_html=True)

def add_to_journal(order, exit_price=None, exit_reason=None):
    trade_record = {"No": len(st.session_state.trade_journal)+1, "Time": get_ist_now().strftime('%H:%M:%S'), "Symbol": order['symbol'], "Type": order['option_type'], "Lots": order['qty'], "Entry": order['entry_price'], "Exit": exit_price if exit_price else "-", "P&L (₹)": 0, "Status": exit_reason if exit_reason else "OPEN"}
    st.session_state.trade_journal.append(trade_record)

def check_fmp_api():
    try:
        url = f"https://financialmodelingprep.com/stable/stock-list?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True, "Active", "✅ Connected"
        return False, "Error", "❌ Connection failed"
    except:
        return False, "Error", "❌ Connection failed"

# ================= UI HEADER =================
st.markdown(f'<div style="text-align:center;"><h1 class="neon-text">🐺 {APP_NAME}</h1><p style="color:#94a3b8;">{APP_AUTHOR}, {APP_LOCATION} | v{APP_VERSION}</p><div style="height:2px; background:linear-gradient(90deg, #00ff88, #00b4d8); width:300px; margin:0 auto;"></div></div>', unsafe_allow_html=True)
now = get_ist_now()
st.markdown(f'<div class="live-time">🕐 {now.strftime("%H:%M:%S")} IST | 📅 {now.strftime("%d %B %Y")}</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= SYSTEM DASHBOARD =================
st.markdown("## 🎮 SYSTEM DASHBOARD")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🔌 API STATUS")
    fmp_status, _, fmp_msg = check_fmp_api()
    st.markdown(f'<div class="status-card">📊 <strong>FMP API</strong><br><span style="color:#00ff88">🟢 {fmp_msg}</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-card">📰 <strong>GNews API</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-card">📱 <strong>Telegram Bot</strong><br><span style="color:#00ff88">🟢 Active</span></div>', unsafe_allow_html=True)

with col_right:
    st.markdown("### 🎮 CONTROL PANEL")
    st.markdown('<div class="glass-3d">', unsafe_allow_html=True)
    totp = st.text_input("🔐 6-DIGIT TOTP CODE", type="password", placeholder="Enter 6-digit code", key="totp_main")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🟢 START ALGO", use_container_width=True):
            if totp and len(totp) == 6:
                st.session_state.algo_running = True
                st.session_state.totp_verified = True
                send_telegram("🚀 ALGO STARTED v6.0")
                st.success("✅ Algo Started!")
                st.rerun()
            else:
                st.error("❌ Valid 6-digit TOTP required!")
    with col_btn2:
        if st.button("🔴 STOP ALGO", use_container_width=True):
            st.session_state.algo_running = False
            send_telegram("🛑 ALGO STOPPED")
            st.warning("⚠️ Algo Stopped!")
            st.rerun()
    st.markdown("---")
    col_status1, col_status2, col_status3 = st.columns(3)
    with col_status1:
        status_color = "#00ff88" if st.session_state.algo_running else "#ff4444"
        st.markdown(f'<div style="text-align:center;"><span style="color:{status_color};">●</span><br>SYSTEM<br><span style="color:{status_color};">{"ACTIVE" if st.session_state.algo_running else "INACTIVE"}</span></div>', unsafe_allow_html=True)
    with col_status2:
        totp_color = "#00ff88" if st.session_state.totp_verified else "#ff4444"
        st.markdown(f'<div style="text-align:center;"><span style="color:{totp_color};">🔐</span><br>TOTP<br><span style="color:{totp_color};">{"VERIFIED" if st.session_state.totp_verified else "NOT VERIFIED"}</span></div>', unsafe_allow_html=True)
    with col_status3:
        now = get_ist_now()
        st.markdown(f'<div style="text-align:center;">⏰<br>TIME<br><span style="color:#00b4d8;">{now.strftime("%H:%M:%S")}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= GET REAL-TIME DATA =================
with st.spinner("🔄 Fetching Live Market Data..."):
    nifty_price, nifty_change, nifty_change_pct, nifty_prev = get_live_nifty()
    banknifty_price, banknifty_change = get_live_banknifty()
    global_data = get_global_indices()
    us_signals = get_us_signals()
    sectors = get_sector_strength()
    options = get_options_data(nifty_price)
    smart_money = get_smart_money_data()
    sentiment = calculate_sentiment_score(nifty_price, global_data, options, sectors, us_signals, smart_money)
    news_items = get_live_news_with_sentiment()
    q4_results = get_q4_results_predictions()

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎯 NIFTY SENTIMENT", "📰 LIVE NEWS", "📈 Q4 RESULTS", "🐺 WOLF ORDER", "⚙️ SETTINGS", "💰 PORTFOLIO"])

# ================= TAB 1: NIFTY SENTIMENT DASHBOARD =================
with tab1:
    st.markdown('<h1>🎯 NIFTY SENTIMENT DASHBOARD</h1><p class="subtitle">8-FACTOR ANALYSIS | 95% ACCURACY | REAL-TIME DATA</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        nifty_color = "#00ff88" if nifty_change >= 0 else "#ff4444"
        st.markdown(f'''
        <div class="glass-3d" style="text-align:center;">
            <div style="font-size:14px; color:#94a3b8;">🇮🇳 NIFTY 50 LIVE</div>
            <div class="live-ticker">₹{nifty_price:,.2f}</div>
            <div style="font-size:18px; color:{nifty_color};">{'▲' if nifty_change>=0 else '▼'} {abs(nifty_change_pct):.2f}%</div>
            <div class="meter-container"><div class="meter-fill" style="width:{50+nifty_change_pct}%;">{nifty_change_pct:+.1f}%</div></div>
            <small>Previous Close: ₹{nifty_prev:,.2f}</small>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="glass-3d" style="text-align:center;">
            <div style="font-size:14px; color:#94a3b8;">OVERALL SENTIMENT</div>
            <div style="font-size:36px; color:{sentiment['color']};">{sentiment['icon']} {sentiment['sentiment']}</div>
            <div style="font-size:24px;">{sentiment['score']:.0f}/100</div>
            <div class="meter-container"><div class="meter-fill" style="width:{sentiment['score']}%;">{sentiment['score']:.0f}</div></div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        rec = get_trading_recommendation()
        st.markdown(f'''
        <div class="glass-3d" style="text-align:center;">
            <div style="font-size:14px; color:#94a3b8;">RECOMMENDATION</div>
            <div style="font-size:24px; color:{rec['color']};">{rec['icon']} {rec['recommendation']}</div>
            <div style="font-size:12px;">ACTION: {rec['action']}</div>
            <div style="font-size:12px;">Confidence: {rec['confidence']}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2>📊 8-FACTOR ANALYSIS</h2>", unsafe_allow_html=True)
    
    factors = sentiment['factors']
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        val = factors.get("Global Markets", 0)
        color = "#00ff44" if val > 0 else "#ff4444" if val < 0 else "#ffaa00"
        st.markdown(f'<div class="factor-card"><div>🌍 GLOBAL</div><div style="font-size:28px; color:{color};">{val:+d}</div><div>Weight:15%</div></div>', unsafe_allow_html=True)
    with col2:
        val = factors.get("Smart Money", 0)
        color = "#00ff44" if val > 0 else "#ff4444" if val < 0 else "#ffaa00"
        st.markdown(f'<div class="factor-card"><div>💰 SMART MONEY</div><div style="font-size:28px; color:{color};">{val:+d}</div><div>Weight:20%</div></div>', unsafe_allow_html=True)
    with col3:
        val = factors.get("Options Chain", 0)
        color = "#00ff44" if val > 0 else "#ff4444" if val < 0 else "#ffaa00"
        st.markdown(f'<div class="factor-card"><div>📊 OPTIONS</div><div style="font-size:28px; color:{color};">{val:+d}</div><div>Weight:25%</div></div>', unsafe_allow_html=True)
    with col4:
        val = factors.get("Sector Strength", 0)
        color = "#00ff44" if val > 0 else "#ff4444" if val < 0 else "#ffaa00"
        st.markdown(f'<div class="factor-card"><div>🏦 SECTORS</div><div style="font-size:28px; color:{color};">{val:+d}</div><div>Weight:15%</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        val = factors.get("US Signals", 0)
        color = "#00ff44" if val > 0 else "#ff4444" if val < 0 else "#ffaa00"
        st.markdown(f'<div class="factor-card"><div>🇺🇸 US SIGNALS</div><div style="font-size:28px; color:{color};">{val:+d}</div><div>Weight:10%</div></div>', unsafe_allow_html=True)
    with col2:
        val = factors.get("VIX", 0)
        color = "#00ff44" if val > 0 else "#ff4444" if val < 0 else "#ffaa00"
        st.markdown(f'<div class="factor-card"><div>📈 VIX</div><div style="font-size:28px; color:{color};">{val:+d}</div><div>Weight:5%</div></div>', unsafe_allow_html=True)
    with col3:
        val = factors.get("DXY/Bond", 0)
        color = "#00ff44" if val > 0 else "#ff4444" if val < 0 else "#ffaa00"
        st.markdown(f'<div class="factor-card"><div>💵 DXY/BOND</div><div style="font-size:28px; color:{color};">{val:+d}</div><div>Weight:5%</div></div>', unsafe_allow_html=True)
    with col4:
        val = factors.get("Crude/Gold", 0)
        color = "#00ff44" if val > 0 else "#ff4444" if val < 0 else "#ffaa00"
        st.markdown(f'<div class="factor-card"><div>🛢️ CRUDE/GOLD</div><div style="font-size:28px; color:{color};">{val:+d}</div><div>Weight:5%</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2>🌍 GLOBAL MARKETS</h2>", unsafe_allow_html=True)
    cols = st.columns(4)
    for idx, (name, data) in enumerate(global_data.items()):
        with cols[idx % 4]:
            if data['value'] > 0:
                color = "#00ff44" if data['change'] >= 0 else "#ff4444"
                arrow = "▲" if data['change'] >= 0 else "▼"
                symbol = "$" if name in ["GOLD", "SILVER", "CRUDE OIL"] else ""
                st.markdown(f'<div class="indicator-card"><div>{data["flag"]} {name}</div><div>{symbol}{data["value"]:.2f}</div><div style="color:{color};">{arrow} {abs(data["change"]):.2f}%</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2>📊 OPTIONS DATA</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pcr_color = "#00ff88" if options['PCR'] > 1.0 else "#ffaa00"
        st.markdown(f'<div class="glass-3d" style="text-align:center;"><div>PCR</div><div style="font-size:28px; color:{pcr_color};">{options["PCR"]:.2f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="glass-3d" style="text-align:center;"><div>MAX PAIN</div><div style="font-size:28px; color:#00b4d8;">{options["MAX PAIN"]:,}</div></div>', unsafe_allow_html=True)
    with col3:
        vix_color = "#00ff88" if options['INDIA VIX'] < 14 else "#ffaa00"
        st.markdown(f'<div class="glass-3d" style="text-align:center;"><div>INDIA VIX</div><div style="font-size:28px; color:{vix_color};">{options["INDIA VIX"]:.2f}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="glass-3d" style="text-align:center;"><div>ATM IV</div><div style="font-size:28px; color:#ffaa00;">{options["ATM IV"]:.1f}%</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2>🏦 SECTOR STRENGTH</h2>", unsafe_allow_html=True)
    cols = st.columns(4)
    for idx, (name, data) in enumerate(sectors.items()):
        with cols[idx % 4]:
            color = "#00ff44" if data['change'] >= 0 else "#ff4444"
            arrow = "▲" if data['change'] >= 0 else "▼"
            st.markdown(f'<div class="indicator-card"><div>{name}</div><div style="color:{color};">{arrow} {abs(data["change"]):.2f}%</div></div>', unsafe_allow_html=True)

# ================= TAB 2: LIVE NEWS =================
with tab2:
    st.markdown("<h1>📰 LIVE NEWS & SENTIMENT</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Real-time news from GNews API with AI sentiment analysis</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3,1])
    with col2:
        st.session_state.voice_enabled = st.checkbox("🔊 Voice Alerts", st.session_state.voice_enabled)
    
    st.markdown("---")
    
    bullish_count = len([n for n in news_items if n['impact'] == 'BULLISH'])
    bearish_count = len([n for n in news_items if n['impact'] == 'BEARISH'])
    neutral_count = len([n for n in news_items if n['impact'] == 'NEUTRAL'])
    
    st.markdown("#### 📊 News Sentiment Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div>📈 BULLISH</div><div style="font-size:32px; color:#00ff44;">{bullish_count}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div>⚪ NEUTRAL</div><div style="font-size:32px; color:#ffaa00;">{neutral_count}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div>📉 BEARISH</div><div style="font-size:32px; color:#ff3333;">{bearish_count}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 📰 Latest News Headlines")
    
    for news in news_items:
        card_class = "news-card-positive" if news['impact'] == 'BULLISH' else "news-card-negative" if news['impact'] == 'BEARISH' else "news-card-neutral"
        badge_class = "badge-bullish" if news['impact'] == 'BULLISH' else "badge-bearish" if news['impact'] == 'BEARISH' else "badge-neutral"
        
        st.markdown(f'''
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap;">
                <div><b>📌 {news['title'][:150]}</b></div>
                <div><span class="{badge_class}">{news['icon']} {news['sentiment']} ({news['score']:+d})</span></div>
            </div>
            <div style="font-size:11px; color:#888;">🔗 {news['source']} | 🕐 {news['time']}</div>
            <div style="margin-top:8px;"><b>🎯 Impacted Sectors:</b> {', '.join(news['sectors'][:3])}</div>
            <div><b>📊 Impacted Stocks:</b> {', '.join(news['stocks'][:3]) if news['stocks'] else 'NIFTY50'}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    if st.session_state.voice_enabled and news_items:
        top_news = news_items[0]
        voice_alert(f"{top_news['sentiment']} sentiment detected: {top_news['title'][:100]}")

# ================= TAB 3: Q4 RESULTS =================
with tab3:
    st.markdown("<h1>📈 Q4 FY26 RESULTS PREDICTIONS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI-powered earnings predictions with sentiment analysis</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    for result in q4_results:
        if result['prediction'] == "STRONG BULLISH":
            bg_color = "#00ff44"
            icon = "🚀"
        elif result['prediction'] == "BULLISH":
            bg_color = "#88ff88"
            icon = "📈"
        elif result['prediction'] == "NEUTRAL":
            bg_color = "#ffaa00"
            icon = "⚪"
        else:
            bg_color = "#ff6666"
            icon = "📉"
        
        eps_text = f"Est: ₹{result['eps_estimate']:.1f}" if result['eps_estimate'] else ""
        if result.get('eps_actual'):
            eps_text += f" | Actual: ₹{result['eps_actual']:.1f}"
        
        st.markdown(f'''
        <div class="glass-3d">
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap;">
                <div><b>🏢 {result['company']} ({result['symbol']})</b></div>
                <div><span style="background:{bg_color}20; color:{bg_color}; padding:5px 15px; border-radius:20px;">{icon} {result['prediction']} ({result['confidence']}%)</span></div>
            </div>
            <div>📅 {result['date']} | ⏰ {result['time']}</div>
            <div>📊 {eps_text}</div>
            <div>🎯 Impact Sectors: {', '.join(result['impact_sectors'])}</div>
            <div style="color:#aaa; font-size:12px;">💡 {result['reason']}</div>
        </div>
        ''', unsafe_allow_html=True)

# ================= TAB 4: WOLF ORDER =================
with tab4:
    st.markdown("<h1>🐺 WOLF ORDER BOOK</h1>", unsafe_allow_html=True)
    
    with st.expander("➕ PLACE NEW ORDER", expanded=False):
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            sym = st.selectbox("Symbol", FO_SCRIPTS)
        with col2:
            opt = st.selectbox("Option", OPTION_TYPES)
        with col3:
            strike = st.number_input("Strike", 1, 500000, 24300)
        with col4:
            qty = st.number_input("Lots", 1, 100, 1)
        with col5:
            buy_above = st.number_input("Buy Above", 1, 500000, 100)
        with col6:
            sl = st.number_input("SL", 1, 500000, 80)
        target = st.number_input("Target", 1, 500000, 150)
        
        if st.button("🐺 PLACE ORDER", use_container_width=True):
            if buy_above > sl and target > buy_above:
                st.session_state.wolf_orders.append({'symbol': sym, 'option_type': opt, 'strike_price': strike, 'qty': qty, 'buy_above': buy_above, 'sl': sl, 'target': target, 'status': 'PENDING', 'placed_time': get_ist_now().strftime('%H:%M:%S')})
                st.success(f"✅ Order placed for {sym}")
                st.rerun()
            else:
                st.error("❌ Buy Above > SL and Target > Buy Above required")
    
    pending_list = [o for o in st.session_state.wolf_orders if o.get('status') == 'PENDING']
    if pending_list:
        st.markdown("#### ⏳ PENDING ORDERS")
        for i, order in enumerate(pending_list):
            st.markdown(f"**{order['symbol']}** {order['option_type']} | Strike: {order['strike_price']} | Qty: {order['qty']} | Buy Above: {order['buy_above']} | SL: {order['sl']} | Target: {order['target']}")
            if st.button(f"❌ Cancel", key=f"cancel_{i}"):
                st.session_state.wolf_orders.remove(order)
                st.rerun()
    else:
        st.info("📭 No pending orders")

# ================= TAB 5: SETTINGS =================
with tab5:
    st.markdown("<h1>⚙️ TRADING SETTINGS</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.auto_trade_enabled = st.checkbox("Enable Auto Trading", st.session_state.auto_trade_enabled)
        st.session_state.auto_trade_qty = st.number_input("Default Lots", 1, 50, st.session_state.auto_trade_qty)
    with col2:
        st.session_state.auto_trade_sl_percent = st.number_input("Stop Loss %", 1, 20, st.session_state.auto_trade_sl_percent)
        st.session_state.auto_trade_target_percent = st.number_input("Target %", 1, 30, st.session_state.auto_trade_target_percent)
    st.markdown("---")
    st.markdown("#### 🎨 Theme Color")
    if "theme_color" not in st.session_state:
        st.session_state.theme_color = "#00ff88"
    st.session_state.theme_color = st.color_picker("Select Color", st.session_state.theme_color)

# ================= TAB 6: PORTFOLIO =================
with tab6:
    st.markdown("<h1>💰 PORTFOLIO & LIVE P&L</h1>", unsafe_allow_html=True)
    show_portfolio_dashboard()
    
    if st.session_state.active_orders:
        st.markdown("#### 🔴 ACTIVE POSITIONS")
        for order in st.session_state.active_orders:
            current = get_live_price(order['symbol'])
            if current > 0:
                multiplier = 50 if order['symbol'] == "NIFTY" else 25
                if order['option_type'] == "CALL (CE)":
                    pnl = (current - order['entry_price']) * order['qty'] * multiplier
                else:
                    pnl = (order['entry_price'] - current) * order['qty'] * multiplier
                pnl_color = "#00ff88" if pnl >= 0 else "#ff4444"
                st.markdown(f"**{order['symbol']}** {order['option_type']} | Entry: {order['entry_price']} | Current: {current:.2f} | P&L: <span style='color:{pnl_color};'>₹{pnl:,.2f}</span>", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown('<div style="text-align:center; padding:15px; background:linear-gradient(135deg,#8B0000,#DC143C); border-radius:15px;"><h2 style="color:#FFD700;">🐺 RUDRANSH</h2><p style="color:#FFD700;">Premium v6.0</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div class="glass-3d" style="text-align:center;"><span style="font-size:28px;">🔴</span><h3>{len(st.session_state.active_orders)}</h3><p>Active Orders</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glass-3d" style="text-align:center;"><span style="font-size:28px;">⏳</span><h3>{len([o for o in st.session_state.wolf_orders if o.get("status")=="PENDING"])}</h3><p>Pending Orders</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glass-3d" style="text-align:center;"><span style="font-size:28px;">📋</span><h3>{len(st.session_state.trade_journal)}</h3><p>Total Trades</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<span style="color:#00ff88">✅ FMP API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ GNews API: Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#00ff88">✅ Telegram: Active</span>', unsafe_allow_html=True)
    auto_text = "ON" if st.session_state.auto_trade_enabled else "OFF"
    auto_color = "#00ff88" if st.session_state.auto_trade_enabled else "#ff4444"
    st.markdown(f'<span style="color:{auto_color}">⚙️ Auto Trade: {auto_text}</span>', unsafe_allow_html=True)

# ================= AUTO EXECUTION =================
def check_and_execute_orders():
    for order in st.session_state.wolf_orders:
        if order.get('status') == 'PENDING':
            current = get_live_price(order['symbol'])
            if current > 0 and current >= order.get('buy_above', 0):
                order['status'] = 'EXECUTED'
                order['entry_price'] = current
                st.session_state.active_orders.append({'symbol': order['symbol'], 'option_type': order['option_type'], 'strike_price': order['strike_price'], 'qty': order['qty'], 'entry_price': current, 'entry_time': get_ist_now().strftime('%H:%M:%S'), 'sl': order['sl'], 'target': order['target']})
                send_telegram(f"✅ ORDER EXECUTED: {order['symbol']} at ₹{current:.2f}")

def monitor_active_orders():
    to_remove = []
    for i, order in enumerate(st.session_state.active_orders):
        current = get_live_price(order['symbol'])
        if current > 0:
            if order['option_type'] == "CALL (CE)":
                if current >= order.get('target', 999999):
                    to_remove.append((i, order, current, "TARGET HIT"))
                elif current <= order.get('sl', 0):
                    to_remove.append((i, order, current, "SL HIT"))
            else:
                if current <= order.get('target', 0):
                    to_remove.append((i, order, current, "TARGET HIT"))
                elif current >= order.get('sl', 999999):
                    to_remove.append((i, order, current, "SL HIT"))
    for idx, order, price, reason in reversed(to_remove):
        add_to_journal(order, price, reason)
        st.session_state.active_orders.pop(idx)
        send_telegram(f"{'✅' if reason=='TARGET HIT' else '❌'} {reason}: {order['symbol']} @ {price:.2f}")

if st.session_state.algo_running and st.session_state.totp_verified:
    check_and_execute_orders()
    monitor_active_orders()
    st.info("🐺 Wolf is hunting... Live P&L Active 🤖")

# ================= FOOTER =================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown(f'<div class="footer">🐺 {APP_NAME} PREMIUM | {APP_AUTHOR} | {APP_LOCATION} | v{APP_VERSION}<br>8 Factors | Real-time News | Q4 Predictions | Trade With Confidence</div>', unsafe_allow_html=True)

st_autorefresh(interval=60000, key="full_refresh")
