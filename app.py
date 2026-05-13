import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Rudransh Remote", layout="wide", page_icon="📱")

st.title("📱 RUDRANSH REMOTE CONTROL")
st.markdown("### Mobile Trading Controller")

# ===== Session State for Demo =====
if "running" not in st.session_state:
    st.session_state.running = False
if "pnl" not in st.session_state:
    st.session_state.pnl = 0
if "position" not in st.session_state:
    st.session_state.position = None
if "entry_price" not in st.session_state:
    st.session_state.entry_price = 0
if "quantity" not in st.session_state:
    st.session_state.quantity = 65

# ===== Sidebar - Controls =====
with st.sidebar:
    st.markdown("## 🎮 MAIN CONTROLS")
    
    # START / STOP buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START ALGO", use_container_width=True):
            st.session_state.running = True
            st.success("✅ Algo Started!")
            st.toast("Algo is now RUNNING", icon="🟢")
    
    with col2:
        if st.button("🛑 STOP ALGO", use_container_width=True):
            st.session_state.running = False
            st.warning("⏸️ Algo Stopped!")
            st.toast("Algo is STOPPED", icon="🔴")
    
    st.markdown("---")
    
    # Quantity Selection
    st.markdown("### 📊 POSITION SIZE")
    asset = st.selectbox("Select Asset", ["NIFTY", "BANK NIFTY", "CRUDEOIL", "NATURALGAS"])
    
    lot_sizes = {
        "NIFTY": 65,
        "BANK NIFTY": 25,
        "CRUDEOIL": 100,
        "NATURALGAS": 1250
    }
    
    lots = st.number_input("Number of Lots", min_value=1, max_value=10, value=1)
    quantity = lots * lot_sizes[asset]
    st.session_state.quantity = quantity
    
    st.metric("📦 Total Quantity", quantity)
    
    st.markdown("---")
    
    # SQUARE OFF button
    st.markdown("### 🔴 TRADE CONTROL")
    if st.button("🔴 SQUARE OFF ALL", use_container_width=True):
        st.session_state.position = None
        st.session_state.entry_price = 0
        st.session_state.pnl = 0
        st.error("✅ All positions SQUARED OFF!")
        st.toast("All trades closed!", icon="🔴")

# ===== Main Panel =====
st.markdown("---")

# Status Card
col1, col2, col3 = st.columns(3)

with col1:
    status_color = "🟢" if st.session_state.running else "🔴"
    status_text = "RUNNING" if st.session_state.running else "STOPPED"
    st.markdown(f"""
    <div style='background:#1e293b; padding:20px; border-radius:15px; text-align:center;'>
        <span style='font-size:14px; color:#94a3b8;'>ALGO STATUS</span><br>
        <span style='font-size:28px; font-weight:bold;'>{status_color} {status_text}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    pnl_color = "#00ff88" if st.session_state.pnl >= 0 else "#ff4b4b"
    st.markdown(f"""
    <div style='background:#1e293b; padding:20px; border-radius:15px; text-align:center;'>
        <span style='font-size:14px; color:#94a3b8;'>TODAY'S P&L</span><br>
        <span style='font-size:28px; font-weight:bold; color:{pnl_color};'>₹{st.session_state.pnl:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    position_text = "NO POSITION" if st.session_state.position is None else f"{st.session_state.position} @ ₹{st.session_state.entry_price}"
    st.markdown(f"""
    <div style='background:#1e293b; padding:20px; border-radius:15px; text-align:center;'>
        <span style='font-size:14px; color:#94a3b8;'>CURRENT POSITION</span><br>
        <span style='font-size:16px; font-weight:bold;'>{position_text}</span>
    </div>
    """, unsafe_allow_html=True)

# ===== Current Market Price =====
st.markdown("---")
st.markdown("### 📈 LIVE MARKET DATA")

try:
    import yfinance as yf
    
    symbols = {
        "NIFTY": "^NSEI",
        "BANK NIFTY": "^NSEBANK",
        "CRUDEOIL": "CL=F",
        "NATURALGAS": "NG=F"
    }
    
    ticker = yf.Ticker(symbols[asset])
    data = ticker.history(period="1d")
    
    if not data.empty:
        current_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
        change = ((current_price - prev_close) / prev_close) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Current Price", f"₹{current_price:.2f}")
        c2.metric("Change", f"{change:+.2f}%")
        c3.metric("Asset", asset)
        
        # Auto P&L update (demo)
        if st.session_state.position == "BUY" and st.session_state.entry_price > 0:
            st.session_state.pnl = (current_price - st.session_state.entry_price) * quantity
        elif st.session_state.position == "SELL" and st.session_state.entry_price > 0:
            st.session_state.pnl = (st.session_state.entry_price - current_price) * quantity
except:
    st.info("📡 Waiting for market data...")

# ===== Quick Actions =====
st.markdown("---")
st.markdown("### ⚡ QUICK ACTIONS")

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 BUY (Market)", use_container_width=True):
        st.session_state.position = "BUY"
        st.session_state.entry_price = current_price if 'current_price' in locals() else 24500
        st.success(f"✅ BUY order placed for {quantity} qty!")
        st.toast(f"BUY {quantity} @ ₹{st.session_state.entry_price:.2f}", icon="🟢")

with col2:
    if st.button("🔴 SELL (Market)", use_container_width=True):
        st.session_state.position = "SELL"
        st.session_state.entry_price = current_price if 'current_price' in locals() else 24500
        st.success(f"✅ SELL order placed for {quantity} qty!")
        st.toast(f"SELL {quantity} @ ₹{st.session_state.entry_price:.2f}", icon="🔴")

# ===== Live Trade Log =====
st.markdown("---")
st.markdown("### 📋 TRADE LOG")

if st.session_state.position:
    st.info(f"📊 ACTIVE: {st.session_state.position} {quantity} qty @ ₹{st.session_state.entry_price:.2f}")
else:
    st.info("📭 No active trades")

# ===== Instructions =====
st.markdown("---")
st.markdown("""
### 📱 HOW TO USE:

1. **START ALGO** - Algorithm शिकवण्यास सुरुवात करेल
2. **STOP ALGO** - Algorithm थांबवेल
3. **BUY/SELL** - Manual trade करायचे असेल तर
4. **SQUARE OFF** - सर्व पोझिशन बंद करेल
5. **PNL** - तुमचा नफा/तोटा दिसेल

🔄 **Auto Refresh every 10 seconds**
""")

st.caption(f"🕐 Last Updated: {datetime.now().strftime('%H:%M:%S')}")
st_autorefresh = st.empty()
