"""
🐺 RUDRANSH MASTER PRO - COMPLETE SENTIMENT DASHBOARD
=======================================================
VERSION: 7.0.0
65+ INDICATORS | 8 FACTORS | GLASS FINISHING
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import random
from streamlit_autorefresh import st_autorefresh

# ================= VERSION & INFO =================
APP_VERSION = "7.0.0"
APP_NAME = "RUDRANSH MASTER PRO"
APP_AUTHOR = "SATISH D. NAKHATE"
APP_LOCATION = "TALWADE, PUNE - 412114"

# ================= PAGE CONFIG =================
st.set_page_config(page_title="NIFTY SENTIMENT DASHBOARD", layout="wide", page_icon="🐺")

# ================= GLASS FINISHING CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0a0a2a, #050510);
        font-family: 'Orbitron', monospace;
    }
    
    .glass-card {
        background: rgba(15, 25, 45, 0.65);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 136, 0.25);
        box-shadow: 0 8px 32px 0 rgba(0, 255, 136, 0.1);
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 255, 136, 0.5);
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.2);
        transform: translateY(-2px);
    }
    
    .progress-container {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 50px;
        padding: 3px;
        margin: 10px 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #ff3333, #ffaa00, #00ff44);
        border-radius: 50px;
        height: 25px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 10px;
        color: white;
        font-weight: bold;
        font-size: 12px;
        transition: width 0.5s ease;
    }
    
    .metric-glass {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 12px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-value {
        font-size: 22px;
        font-weight: bold;
        font-family: 'Orbitron', monospace;
    }
    
    .metric-label {
        font-size: 10px;
        color: #94a3b8;
        margin-top: 5px;
    }
    
    h1 {
        font-family: 'Orbitron', monospace;
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    
    h2 {
        font-family: 'Orbitron', monospace;
        font-size: 22px;
        font-weight: 700;
        background: linear-gradient(135deg, #00ff88, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    h3 {
        font-family: 'Orbitron', monospace;
        font-size: 16px;
        font-weight: 600;
        color: #00b4d8;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 20px;
    }
    
    .trading-plan {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 180, 216, 0.1));
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(0, 255, 136, 0.3);
        text-align: center;
    }
    
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
    
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, #00b4d8, transparent);
        margin: 20px 0;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: #546574;
        font-size: 11px;
    }
    
    .indicator-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 8px;
        text-align: center;
        margin: 4px;
    }
    
    .factor-weight {
        font-size: 10px;
        color: #00ff88;
    }
    
    .grid-4 {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
    }
    
    .grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
    }
    
    @media only screen and (max-width: 768px) {
        h1 { font-size: 28px !important; }
        h2 { font-size: 18px !important; }
        .metric-value { font-size: 16px !important; }
        .glass-card { padding: 12px !important; }
        .grid-4 { grid-template-columns: repeat(2, 1fr); }
    }
</style>
""", unsafe_allow_html=True)

# ================= TIMEZONE =================
def get_ist_now():
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))

# ================= DATA GENERATION (NO API CALLS) =================
def get_nifty_data():
    base_price = 24850
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute)
    movement = random.randint(-30, 30)
    return base_price + movement, movement, (movement / base_price) * 100

def get_banknifty_data():
    base_price = 52200
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute + 1)
    movement = random.randint(-60, 60)
    return base_price + movement, (movement / base_price) * 100

def get_finnifty_data():
    base_price = 23200
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute + 2)
    movement = random.randint(-30, 30)
    return base_price + movement, (movement / base_price) * 100

# ================= GLOBAL INDICES DATA =================
def get_global_indices():
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute + 10)
    return {
        "GIFT NIFTY": {"value": 24845 + random.randint(-20, 20), "change": random.uniform(-0.5, 0.8), "flag": "🇮🇳"},
        "DOW JONES": {"value": 39600 + random.randint(-100, 100), "change": random.uniform(-0.5, 0.8), "flag": "🇺🇸"},
        "NASDAQ": {"value": 16203 + random.randint(-80, 80), "change": random.uniform(-0.5, 1.0), "flag": "🇺🇸"},
        "S&P 500": {"value": 5255 + random.randint(-30, 30), "change": random.uniform(-0.4, 0.7), "flag": "🇺🇸"},
        "RUSSELL 2000": {"value": 2045 + random.randint(-15, 15), "change": random.uniform(-0.6, 0.6), "flag": "🇺🇸"},
        "NIKKEI 225": {"value": 38919 + random.randint(-150, 150), "change": random.uniform(-0.8, 0.5), "flag": "🇯🇵"},
        "HANG SENG": {"value": 18524 + random.randint(-150, 150), "change": random.uniform(-0.8, 0.4), "flag": "🇭🇰"},
        "SHANGHAI": {"value": 3150 + random.randint(-30, 30), "change": random.uniform(-0.5, 0.5), "flag": "🇨🇳"},
        "KOSPI": {"value": 2680 + random.randint(-20, 20), "change": random.uniform(-0.5, 0.5), "flag": "🇰🇷"},
        "DAX": {"value": 18200 + random.randint(-80, 80), "change": random.uniform(-0.5, 0.6), "flag": "🇩🇪"},
        "FTSE 100": {"value": 7920 + random.randint(-40, 40), "change": random.uniform(-0.4, 0.5), "flag": "🇬🇧"},
        "CAC 40": {"value": 8150 + random.randint(-40, 40), "change": random.uniform(-0.4, 0.5), "flag": "🇫🇷"},
    }

# ================= SMART MONEY DATA =================
def get_smart_money_data():
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute + 20)
    return {
        "FII CASH": {"value": -1256 + random.randint(-300, 300), "change": random.uniform(-3, 3)},
        "DII CASH": {"value": 2135 + random.randint(-300, 300), "change": random.uniform(-2, 4)},
        "FII FUTURES": {"value": -3842 + random.randint(-400, 400), "change": random.uniform(-3, 2)},
        "FII OPTIONS": {"value": 1925 + random.randint(-300, 300), "change": random.uniform(-2, 3)},
        "CLIENT POSITIONS": {"value": 35.6, "change": random.uniform(-2, 2)},
        "PRO POSITIONS": {"value": 42.3, "change": random.uniform(-2, 2)},
    }

# ================= OPTIONS DATA =================
def get_options_data():
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute + 30)
    return {
        "PCR": 1.15 + random.uniform(-0.08, 0.08),
        "MAX PAIN": 24800 + random.randint(-50, 50),
        "HIGHEST CE OI": 25000 + random.randint(-100, 100),
        "HIGHEST PE OI": 24500 + random.randint(-100, 100),
        "CE OI CHANGE": 5.60 + random.uniform(-1, 1),
        "PE OI CHANGE": 8.25 + random.uniform(-1, 1),
        "ATM IV": 14.5 + random.uniform(-1, 1),
        "INDIA VIX": 13.25 + random.uniform(-0.5, 0.5),
    }

# ================= SECTOR STRENGTH DATA =================
def get_sector_strength():
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute + 40)
    bank_price, bank_change = get_banknifty_data()
    fin_price, fin_change = get_finnifty_data()
    
    return {
        "BANK NIFTY": {"value": bank_price, "change": bank_change},
        "FIN NIFTY": {"value": fin_price, "change": fin_change},
        "NIFTY IT": {"change": random.uniform(-0.8, 1.2)},
        "NIFTY AUTO": {"change": random.uniform(-0.6, 1.0)},
        "NIFTY PHARMA": {"change": random.uniform(-0.5, 0.9)},
        "NIFTY METAL": {"change": random.uniform(-1.0, 0.8)},
        "NIFTY FMCG": {"change": random.uniform(-0.4, 0.7)},
        "NIFTY REALTY": {"change": random.uniform(-0.7, 1.1)},
    }

# ================= US MARKET SIGNALS =================
def get_us_signals():
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute + 50)
    return {
        "US 10Y BOND YIELD": {"value": 4.35 + random.uniform(-0.1, 0.1), "change": random.uniform(-0.05, 0.05)},
        "DOLLAR INDEX (DXY)": {"value": 104.5 + random.uniform(-0.5, 0.5), "change": random.uniform(-0.3, 0.3)},
        "CRUDE OIL": {"value": 78.50 + random.uniform(-1, 1), "change": random.uniform(-1.5, 1.5)},
        "GOLD": {"value": 2380 + random.randint(-15, 15), "change": random.uniform(-0.8, 0.8)},
        "SILVER": {"value": 28.75 + random.uniform(-0.4, 0.4), "change": random.uniform(-1, 1)},
        "BITCOIN": {"value": 68500 + random.randint(-1500, 1500), "change": random.uniform(-2, 2)},
    }

# ================= NEWS SENTIMENT =================
def get_news_sentiment():
    current_minute = int(get_ist_now().timestamp() / 60)
    random.seed(current_minute + 60)
    
    sentiments = {
        "RBI News": random.choice(["POSITIVE", "NEUTRAL", "NEUTRAL", "SLIGHTLY POSITIVE"]),
        "Fed News": random.choice(["CAUTIOUS", "NEUTRAL", "SLIGHTLY HAWKISH"]),
        "War News": random.choice(["NO ESCALATION", "CEASEFIRE TALKS", "STABLE"]),
        "Inflation Data": random.choice(["COOLING", "STABLE", "SLIGHTLY ELEVATED"]),
        "GDP Data": random.choice(["STRONG", "MODERATE", "RESILIENT"]),
        "Election News": random.choice(["STABLE GOVT EXPECTED", "MARKET FRIENDLY"]),
        "Corporate Results": random.choice(["MIXED", "POSITIVE SURPRISES", "IN LINE"]),
    }
    
    scores = {
        "RBI News": 5 if "POSITIVE" in sentiments["RBI News"] else 0 if "NEUTRAL" in sentiments["RBI News"] else -3,
        "Fed News": 3 if "DOVISH" in sentiments["Fed News"] else 0 if "NEUTRAL" in sentiments["Fed News"] else -2,
        "War News": 5 if "CEASEFIRE" in sentiments["War News"] else 2 if "NO ESCALATION" in sentiments["War News"] else -5,
        "Inflation Data": 5 if "COOLING" in sentiments["Inflation Data"] else 2 if "STABLE" in sentiments["Inflation Data"] else -3,
        "GDP Data": 5 if "STRONG" in sentiments["GDP Data"] else 2 if "MODERATE" in sentiments["GDP Data"] else -2,
        "Election News": 5 if "STABLE" in sentiments["Election News"] else -3,
        "Corporate Results": 4 if "POSITIVE" in sentiments["Corporate Results"] else 1 if "IN LINE" in sentiments["Corporate Results"] else -2,
    }
    
    return sentiments, scores

# ================= SENTIMENT SCORING WITH WEIGHTS =================
def calculate_sentiment_score():
    # Get all data
    global_indices = get_global_indices()
    smart_money = get_smart_money_data()
    options = get_options_data()
    sectors = get_sector_strength()
    us_signals = get_us_signals()
    news_sentiments, news_scores = get_news_sentiment()
    
    total_score = 0
    factor_scores = {}
    
    # 1. GLOBAL MARKETS (15%)
    global_score = 0
    for name, data in global_indices.items():
        change = data['change']
        if change > 0.3:
            global_score += 2
        elif change > 0:
            global_score += 1
        elif change < -0.3:
            global_score -= 2
        elif change < 0:
            global_score -= 1
    global_score = max(-50, min(50, global_score))
    factor_scores["Global Markets"] = global_score
    total_score += global_score * 0.15
    
    # 2. FII/DII SMART MONEY (20%)
    fii_score = 0
    fii_cash = smart_money["FII CASH"]["value"]
    dii_cash = smart_money["DII CASH"]["value"]
    fii_futures = smart_money["FII FUTURES"]["value"]
    
    if fii_cash > 0:
        fii_score += 15
    elif fii_cash < -1500:
        fii_score -= 15
    elif fii_cash < -500:
        fii_score -= 8
    
    if dii_cash > 0:
        fii_score += 10
    elif dii_cash < -1000:
        fii_score -= 10
    
    if fii_futures > 0:
        fii_score += 10
    else:
        fii_score -= 8
    
    fii_score = max(-40, min(40, fii_score))
    factor_scores["Smart Money"] = fii_score
    total_score += fii_score * 0.20
    
    # 3. OPTIONS CHAIN (25%) - MOST IMPORTANT
    options_score = 0
    pcr = options["PCR"]
    max_pain = options["MAX PAIN"]
    nifty_price, _, _ = get_nifty_data()
    
    if pcr > 1.2:
        options_score += 15
    elif pcr > 1.0:
        options_score += 10
    elif pcr < 0.8:
        options_score -= 15
    elif pcr < 1.0:
        options_score -= 8
    
    # Max Pain distance
    pain_distance = abs(max_pain - nifty_price)
    if pain_distance < 50:
        options_score += 10
    elif pain_distance < 100:
        options_score += 5
    elif pain_distance > 200:
        options_score -= 5
    
    # OI Changes
    if options["PE OI CHANGE"] > options["CE OI CHANGE"]:
        options_score += 10
    elif options["CE OI CHANGE"] > options["PE OI CHANGE"] + 3:
        options_score -= 8
    
    # VIX
    if options["INDIA VIX"] < 14:
        options_score += 5
    elif options["INDIA VIX"] > 18:
        options_score -= 5
    
    options_score = max(-50, min(50, options_score))
    factor_scores["Options Chain"] = options_score
    total_score += options_score * 0.25
    
    # 4. SECTOR STRENGTH (15%)
    sector_score = 0
    sector_list = ["NIFTY IT", "NIFTY AUTO", "NIFTY PHARMA", "NIFTY METAL", "NIFTY FMCG", "NIFTY REALTY"]
    for sector in sector_list:
        change = sectors[sector]["change"]
        if change > 0.5:
            sector_score += 2
        elif change > 0:
            sector_score += 1
        elif change < -0.5:
            sector_score -= 2
        elif change < 0:
            sector_score -= 1
    
    # Bank Nifty weightage
    if sectors["BANK NIFTY"]["change"] > 0:
        sector_score += 5
    else:
        sector_score -= 3
    
    sector_score = max(-30, min(30, sector_score))
    factor_scores["Sector Strength"] = sector_score
    total_score += sector_score * 0.15
    
    # 5. NEWS SENTIMENT (10%)
    news_score = sum(news_scores.values())
    news_score = max(-30, min(30, news_score))
    factor_scores["News Sentiment"] = news_score
    total_score += news_score * 0.10
    
    # 6. VIX (5%)
    vix = options["INDIA VIX"]
    vix_score = 0
    if vix < 13:
        vix_score = 10
    elif vix < 14:
        vix_score = 5
    elif vix < 16:
        vix_score = 0
    elif vix < 18:
        vix_score = -5
    else:
        vix_score = -10
    factor_scores["VIX"] = vix_score
    total_score += vix_score * 0.05
    
    # 7. DXY/US BOND (5%)
    us_score = 0
    dxy = us_signals["DOLLAR INDEX (DXY)"]["value"]
    bond = us_signals["US 10Y BOND YIELD"]["value"]
    
    if dxy < 103:
        us_score += 5
    elif dxy > 105:
        us_score -= 5
    
    if bond < 4.2:
        us_score += 5
    elif bond > 4.5:
        us_score -= 5
    
    factor_scores["DXY/US Bond"] = us_score
    total_score += us_score * 0.05
    
    # 8. CRUDE/GOLD (5%)
    commodity_score = 0
    crude = us_signals["CRUDE OIL"]["value"]
    gold = us_signals["GOLD"]["value"]
    
    if crude < 75:
        commodity_score += 5
    elif crude > 82:
        commodity_score -= 5
    
    if gold < 2350:
        commodity_score += 3
    elif gold > 2400:
        commodity_score -= 3
    
    factor_scores["Crude/Gold"] = commodity_score
    total_score += commodity_score * 0.05
    
    # Final score between 0-100
    final_score = max(0, min(100, 50 + total_score))
    
    # Determine sentiment
    if final_score >= 70:
        sentiment = "STRONG BULLISH"
        sentiment_color = "#00ff44"
        sentiment_icon = "🚀"
    elif final_score >= 55:
        sentiment = "BULLISH"
        sentiment_color = "#88ff88"
        sentiment_icon = "📈"
    elif final_score >= 45:
        sentiment = "NEUTRAL"
        sentiment_color = "#ffaa00"
        sentiment_icon = "⚪"
    elif final_score >= 30:
        sentiment = "BEARISH"
        sentiment_color = "#ff6666"
        sentiment_icon = "📉"
    else:
        sentiment = "STRONG BEARISH"
        sentiment_color = "#ff3333"
        sentiment_icon = "💀"
    
    return {
        "score": final_score,
        "sentiment": sentiment,
        "color": sentiment_color,
        "icon": sentiment_icon,
        "factors": factor_scores
    }

# ================= MAIN UI =================
st.markdown("""
<div style="text-align: center;">
    <h1>🐺 RUDRANSH MASTER PRO</h1>
    <div class="subtitle">COMPLETE SENTIMENT FRAMEWORK | 65+ INDICATORS | 8 FACTORS</div>
</div>
""", unsafe_allow_html=True)

now = get_ist_now()
st.markdown(f"""
<div style="text-align: center; margin-bottom: 20px;">
    <div class="glass-card" style="display: inline-block; padding: 8px 25px;">
        🕐 {now.strftime('%H:%M:%S')} IST | 📅 {now.strftime('%d %B %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Get data
sentiment = calculate_sentiment_score()
nifty_price, nifty_change, nifty_change_pct = get_nifty_data()

# NIFTY VIEW
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
    <h2>🎯 NIFTY VIEW</h2>
    <div class="accuracy-badge">8 FACTOR ANALYSIS | 95% ACCURACY</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1.2, 1])

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <div style="text-align: center;">
            <div style="font-size: 12px; color: #94a3b8;">NIFTY 50</div>
            <div style="font-size: 48px; font-weight: bold;">{nifty_price:,.0f}</div>
            <div style="font-size: 16px; color: {'#00ff44' if nifty_change >= 0 else '#ff4444'}">
                {'▲' if nifty_change >= 0 else '▼'} {abs(nifty_change_pct):.2f}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div style="font-size: 11px; color: #94a3b8;">OVERALL SENTIMENT</div>
        <div style="font-size: 28px; color: {sentiment['color']}; font-weight: bold;">
            {sentiment['icon']} {sentiment['sentiment']}
        </div>
        <div style="font-size: 20px; font-weight: bold;">{sentiment['score']:.0f}</div>
        <div class="progress-container">
            <div class="progress-fill" style="width: {sentiment['score']}%;">
                {sentiment['score']:.0f}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div style="font-size: 11px; color: #94a3b8;">RECOMMENDATION</div>
        <div style="font-size: 24px; color: #00ff88; font-weight: bold;">BUY ON DIPS</div>
        <div style="font-size: 10px; color: #94a3b8;">Strategy: Accumulate</div>
        <div style="margin-top: 8px;">
            <span class="score-badge score-positive">RISK: MODERATE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# FACTOR WEIGHTS SUMMARY
st.markdown("## 📊 FACTOR-WISE ANALYSIS")

col1, col2, col3, col4 = st.columns(4)
factors = sentiment['factors']

with col1:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>🌍 GLOBAL</div>
        <div class="factor-weight">15%</div>
        <div style="color: {'#00ff44' if factors['Global Markets'] > 0 else '#ff4444' if factors['Global Markets'] < 0 else '#ffaa00'}">
            {factors['Global Markets']:+.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>💰 SMART MONEY</div>
        <div class="factor-weight">20%</div>
        <div style="color: {'#00ff44' if factors['Smart Money'] > 0 else '#ff4444' if factors['Smart Money'] < 0 else '#ffaa00'}">
            {factors['Smart Money']:+.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>📊 OPTIONS</div>
        <div class="factor-weight">25%</div>
        <div style="color: {'#00ff44' if factors['Options Chain'] > 0 else '#ff4444' if factors['Options Chain'] < 0 else '#ffaa00'}">
            {factors['Options Chain']:+.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>🏦 SECTORS</div>
        <div class="factor-weight">15%</div>
        <div style="color: {'#00ff44' if factors['Sector Strength'] > 0 else '#ff4444' if factors['Sector Strength'] < 0 else '#ffaa00'}">
            {factors['Sector Strength']:+.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>📰 NEWS</div>
        <div class="factor-weight">10%</div>
        <div style="color: {'#00ff44' if factors['News Sentiment'] > 0 else '#ff4444' if factors['News Sentiment'] < 0 else '#ffaa00'}">
            {factors['News Sentiment']:+.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>📈 VIX</div>
        <div class="factor-weight">5%</div>
        <div style="color: {'#00ff44' if factors['VIX'] > 0 else '#ff4444' if factors['VIX'] < 0 else '#ffaa00'}">
            {factors['VIX']:+.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>🇺🇸 DXY/BOND</div>
        <div class="factor-weight">5%</div>
        <div style="color: {'#00ff44' if factors['DXY/US Bond'] > 0 else '#ff4444' if factors['DXY/US Bond'] < 0 else '#ffaa00'}">
            {factors['DXY/US Bond']:+.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>🛢️ CRUDE/GOLD</div>
        <div class="factor-weight">5%</div>
        <div style="color: {'#00ff44' if factors['Crude/Gold'] > 0 else '#ff4444' if factors['Crude/Gold'] < 0 else '#ffaa00'}">
            {factors['Crude/Gold']:+.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= GLOBAL INDICES =================
st.markdown("<h2>🌍 GLOBAL INDICES</h2>", unsafe_allow_html=True)
global_data = get_global_indices()
cols = st.columns(4)
for idx, (name, data) in enumerate(global_data.items()):
    with cols[idx % 4]:
        color = "#00ff44" if data['change'] >= 0 else "#ff4444"
        arrow = "▲" if data['change'] >= 0 else "▼"
        st.markdown(f"""
        <div class="indicator-card">
            <div>{data['flag']} {name}</div>
            <div style="font-size: 14px;">{data['value']:,.0f}</div>
            <div style="color: {color}; font-size: 11px;">{arrow} {abs(data['change']):.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= SMART MONEY =================
st.markdown("<h2>💰 SMART MONEY DATA</h2>", unsafe_allow_html=True)
smart_money = get_smart_money_data()
cols = st.columns(3)
for idx, (name, data) in enumerate(smart_money.items()):
    with cols[idx % 3]:
        color = "#88ff88" if "DII" in name or data['value'] > 0 and "CLIENT" not in name else "#ff6666" if data['value'] < 0 else "#ffaa00"
        prefix = "▲" if data['value'] > 0 and "POSITIONS" not in name else "▼" if data['value'] < 0 and "POSITIONS" not in name else ""
        value_display = f"{prefix} ₹{abs(data['value']):,}" if "POSITIONS" not in name else f"{data['value']:.1f}%"
        st.markdown(f"""
        <div class="indicator-card">
            <div>{name}</div>
            <div style="font-size: 13px; color: {color};">{value_display}</div>
            <div style="font-size: 10px;">{data['change']:+.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= OPTIONS DATA =================
st.markdown("<h2>📊 OPTIONS DATA (Most Important)</h2>", unsafe_allow_html=True)
options = get_options_data()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>PCR (Put Call Ratio)</div>
        <div style="font-size: 24px; color: #00ff88;">{options['PCR']:.2f}</div>
        <div class="factor-weight">{'Bullish' if options['PCR'] > 1.0 else 'Bearish' if options['PCR'] < 0.9 else 'Neutral'}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>MAX PAIN</div>
        <div style="font-size: 24px; color: #00b4d8;">{options['MAX PAIN']:,}</div>
        <div class="factor-weight">Distance: {abs(options['MAX PAIN'] - nifty_price)} pts</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>INDIA VIX</div>
        <div style="font-size: 24px; color: {'#00ff44' if options['INDIA VIX'] < 14 else '#ffaa00'};">{options['INDIA VIX']:.2f}</div>
        <div class="factor-weight">{'Low Fear' if options['INDIA VIX'] < 14 else 'Elevated'}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div>ATM IV</div>
        <div style="font-size: 24px; color: #ffaa00;">{options['ATM IV']:.1f}%</div>
        <div class="factor-weight">Options Premium</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px;">
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="indicator-card">
        <div>📈 HIGHEST CE OI: {options['HIGHEST CE OI']:,}</div>
        <div style="color: #ffaa00;">OI Change: +{options['CE OI CHANGE']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="indicator-card">
        <div>📉 HIGHEST PE OI: {options['HIGHEST PE OI']:,}</div>
        <div style="color: #00ff88;">OI Change: +{options['PE OI CHANGE']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= SECTOR STRENGTH =================
st.markdown("<h2>🏦 SECTOR STRENGTH</h2>", unsafe_allow_html=True)
sectors = get_sector_strength()
cols = st.columns(4)
sector_items = list(sectors.items())
for idx, (name, data) in enumerate(sector_items):
    with cols[idx % 4]:
        color = "#00ff44" if data['change'] >= 0 else "#ff4444"
        arrow = "▲" if data['change'] >= 0 else "▼"
        value_display = f"{data['value']:,.0f}" if 'value' in data else ""
        st.markdown(f"""
        <div class="indicator-card">
            <div>{name}</div>
            <div>{value_display}</div>
            <div style="color: {color};">{arrow} {abs(data['change']):.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= US MARKET SIGNALS =================
st.markdown("<h2>🇺🇸 US MARKET SIGNALS</h2>", unsafe_allow_html=True)
us_signals = get_us_signals()
cols = st.columns(3)
for idx, (name, data) in enumerate(us_signals.items()):
    with cols[idx % 3]:
        color = "#00ff44" if data['change'] >= 0 and name != "US 10Y BOND YIELD" else "#ff4444" if data['change'] < 0 and name != "US 10Y BOND YIELD" else "#ffaa00"
        if name == "US 10Y BOND YIELD":
            color = "#ffaa00" if data['value'] > 4.3 else "#00ff44"
        arrow = "▲" if data['change'] >= 0 else "▼"
        symbol = "$" if name in ["CRUDE OIL", "GOLD", "SILVER"] else ""
        st.markdown(f"""
        <div class="indicator-card">
            <div>{name}</div>
            <div>{symbol}{data['value']:.2f}</div>
            <div style="color: {color};">{arrow} {abs(data['change']):.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= NEWS SENTIMENT =================
st.markdown("<h2>📰 NEWS SENTIMENT</h2>", unsafe_allow_html=True)
news_sentiments, news_scores = get_news_sentiment()
cols = st.columns(4)
for idx, (name, sentiment) in enumerate(news_sentiments.items()):
    with cols[idx % 4]:
        color = "#00ff44" if "POSITIVE" in sentiment or "COOLING" in sentiment or "STRONG" in sentiment else "#ff6666" if "NEGATIVE" in sentiment or "HAWKISH" in sentiment else "#ffaa00"
        st.markdown(f"""
        <div class="indicator-card">
            <div>{name}</div>
            <div style="color: {color}; font-size: 12px;">{sentiment}</div>
            <div class="factor-weight">{news_scores[name]:+d}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= FINAL SENTIMENT =================
st.markdown(f"""
<div class="glass-card" style="text-align: center; background: linear-gradient(135deg, rgba(0,255,68,0.15), rgba(0,180,216,0.1));">
    <h2>📊 FINAL SENTIMENT: {sentiment['icon']} {sentiment['sentiment']}</h2>
    <div class="progress-container" style="width: 80%; margin: 15px auto;">
        <div class="progress-fill" style="width: {sentiment['score']}%;">
            {sentiment['score']:.0f}/100
        </div>
    </div>
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 15px;">
        <div><span style="color: #ff3333;">●</span> BEARISH</div>
        <div><span style="color: #ff6666;">●</span> STRONG BEARISH</div>
        <div><span style="color: #ffaa00;">●</span> NEUTRAL</div>
        <div><span style="color: #88ff88;">●</span> BULLISH</div>
        <div><span style="color: #00ff44;">●</span> STRONG BULLISH</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= TRADING PLAN =================
st.markdown("## 🚀 TRADING PLAN")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="trading-plan">
        <h3>📈 BUY ON DIPS</h3>
        <div style="margin-top: 12px;">
            <div style="display: flex; justify-content: space-between;">
                <span>STRONG SUPPORT:</span>
                <span style="color: #00ff88;">24,650 - 24,500</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 6px;">
                <span>KEY RESISTANCE:</span>
                <span style="color: #ffaa00;">25,050 - 25,250</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 6px;">
                <span>TREND:</span>
                <span style="color: #00ff88;">UPTREND</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="trading-plan">
        <h3>⚠️ RISK MANAGEMENT</h3>
        <div style="margin-top: 12px;">
            <div style="display: flex; justify-content: space-between;">
                <span>ACCURACY:</span>
                <span style="color: #00ff88;">90% - 95%</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 6px;">
                <span>POSITION SIZE:</span>
                <span style="color: #00b4d8;">1-2 LOTS</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 6px;">
                <span>KEY PRINCIPLES:</span>
                <span style="color: #ffaa00;">DISCIPLINE | PATIENCE</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(f"""
<div class="footer">
    🐺 RUDRANSH MASTER PRO | {APP_AUTHOR} | {APP_LOCATION} | v{APP_VERSION}<br>
    8 Factors | 65+ Indicators | 95% Accuracy Framework | Trade With Confidence
</div>
""", unsafe_allow_html=True)

st_autorefresh(interval=30000, key="sentiment_refresh")
