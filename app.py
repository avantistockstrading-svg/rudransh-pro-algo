""")

# ================= REFRESH BUTTON =================
if st.button("🔄 Force Refresh Now", use_container_width=True):
    st.rerun()

st.caption(f"⏰ Last auto-refresh: {get_ist_now().strftime('%H:%M:%S')} | Next refresh in 30 seconds")

# ================= TABS =================
st.markdown("---")
tab1, tab2 = st.tabs(["📈 ALGO TRADING", "📰 LIVE NEWS"])

# ================= TAB 1: ALGO TRADING =================
with tab1:
    # Control Panel
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1.5])
    with col1:
        totp = st.text_input("🔐 TOTP", type="password", placeholder="6-digit code", label_visibility="collapsed")
    with col2:
        if st.button("🟢 START", use_container_width=True):
            if totp and len(totp) == 6:
                st.session_state.running = True
                send_telegram("🚀 ALGO STARTED")
                st.rerun()
            else:
                st.error("Valid TOTP required!")
    with col3:
        if st.button("🔴 STOP", use_container_width=True):
            st.session_state.running = False
            send_telegram("🛑 ALGO STOPPED")
            st.rerun()
    with col4:
        if st.session_state.running:
            st.success(f"🟢 RUNNING | {get_ist_now().strftime('%H:%M:%S')}")
        else:
            st.error(f"🔴 STOPPED | {get_ist_now().strftime('%H:%M:%S')}")

    st.markdown("---")

    # Live Prices
    usdinr = get_usd_inr()
    nifty_price = get_price("^NSEI")
    crude_usd = get_price("CL=F")
    crude_price = round(crude_usd * usdinr, 2) if crude_usd else 0
    ng_usd = get_price("NG=F")
    ng_price = round(ng_usd * usdinr, 2) if ng_usd else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("🇮🇳 NIFTY 50", f"₹{nifty_price:,.2f}" if nifty_price else "Loading...")
    col2.metric("🛢️ CRUDE OIL", f"₹{crude_price:,.2f}" if crude_price else "Loading...")
    col3.metric("🌿 NATURAL GAS", f"₹{ng_price:,.2f}" if ng_price else "Loading...")

    st.markdown("---")

    # Fund & Trade Status
    available_funds = st.session_state.capital - st.session_state.daily_loss
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Available", f"₹{available_funds:,.0f}")
    col2.metric("📉 Daily Loss", f"₹{abs(st.session_state.daily_loss):,.0f}")
    col3.metric("🇮🇳 NIFTY", f"{st.session_state.nifty_count}/2")
    col4.metric("🛢️ CRUDE", f"{st.session_state.crude_count}/2")

    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ SETTINGS")
        st.markdown("### 🤖 AUTO TRADE")
        st.session_state.auto_trade = st.checkbox("Enable Auto Trading", value=st.session_state.auto_trade)
        st.markdown("### 💰 CAPITAL")
        st.session_state.capital = st.number_input("Initial Capital (₹)", 50000, 10000000, st.session_state.capital, 50000)
        st.markdown("### 📊 LOT SIZE")
        st.session_state.nifty_lots = st.number_input("NIFTY Lots", 1, 20, st.session_state.nifty_lots)
        st.caption(f"Qty: {st.session_state.nifty_lots * 65}")
        st.session_state.crude_lots = st.number_input("CRUDE Lots", 1, 20, st.session_state.crude_lots)
        st.caption(f"Qty: {st.session_state.crude_lots * 100}")
        st.session_state.ng_lots = st.number_input("NG Lots", 1, 20, st.session_state.ng_lots)
        st.caption(f"Qty: {st.session_state.ng_lots * 1250}")
        st.markdown("---")
        st.markdown("### 🎯 TARGETS")
        st.caption("🇮🇳 NIFTY: ₹10 per point")
        st.caption("🛢️ CRUDE: ₹10 per point")
        st.caption("🌿 NG: ₹1 per point")

    # Trading Journal
    st.markdown("## 📋 TRADING JOURNAL")
    if st.session_state.trades:
        df_trades = pd.DataFrame(st.session_state.trades)
        st.dataframe(df_trades, use_container_width=True, height=300)
        st.caption(f"📊 Total Trades: {len(st.session_state.trades)}")
    else:
        st.info("📭 No trades executed yet")

    # Main Trading Logic
    if st.session_state.running:
        if st.session_state.daily_loss >= 100000:
            st.error(f"🚨 DAILY LOSS LIMIT HIT: ₹{st.session_state.daily_loss:,.0f} / ₹1,00,000")
        else:
            placeholder = st.empty()
            nifty_signal = get_signal("^NSEI") if st.session_state.nifty_count < 2 else "WAIT"
            crude_signal = get_signal("CL=F") if st.session_state.crude_count < 2 else "WAIT"
            ng_signal = get_signal("NG=F") if st.session_state.ng_count < 2 else "WAIT"
            
            with placeholder.container():
                st.markdown("### 🔍 LIVE SIGNALS")
                col1, col2, col3 = st.columns(3)
                col1.metric("🇮🇳 NIFTY Signal", nifty_signal)
                col2.metric("🛢️ CRUDE Signal", crude_signal)
                col3.metric("🌿 NG Signal", ng_signal)
            
            if st.session_state.auto_trade:
                if nifty_signal != "WAIT" and st.session_state.nifty_count < 2:
                    price = get_price("^NSEI")
                    if price:
                        execute_trade("NIFTY", nifty_signal, price, st.session_state.nifty_lots, st.session_state.nifty_lots * 65, 10)
                        st.rerun()
                if crude_signal != "WAIT" and st.session_state.crude_count < 2:
                    price = get_price("CL=F") * usdinr
                    if price:
                        execute_trade("CRUDE", crude_signal, price, st.session_state.crude_lots, st.session_state.crude_lots * 100, 10)
                        st.rerun()
                if ng_signal != "WAIT" and st.session_state.ng_count < 2:
                    price = get_price("NG=F") * usdinr
                    if price:
                        execute_trade("NG", ng_signal, price, st.session_state.ng_lots, st.session_state.ng_lots * 1250, 1)
                        st.rerun()
            time.sleep(10)
            st.rerun()
    else:
        st.info("⏸️ Press START to begin auto trading")

# ================= TAB 2: LIVE NEWS =================
with tab2:
    st.markdown("## 📰 LIVE MARKET NEWS")
    
    try:
        url = f"https://gnews.io/api/v4/search?q=stock%20market%20india%20NIFTY&lang=en&max=10&apikey={GNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            for article in articles[:10]:
                title = article.get("title", "No Title")
                source = article.get("source", {}).get("name", "News")
                published = article.get("publishedAt", "")
                st.markdown(f"""
                <div style='background:rgba(0,255,136,0.05); padding:10px; border-radius:8px; margin:5px 0; border-left:3px solid #00ff88;'>
                    <b>📌 {title}</b><br>
                    <span style='color:#94a3b8; font-size:12px'>{source}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 News API limit reached. Try after some time.")
    except:
        st.info("📭 Unable to fetch news. Please check internet connection.")

# ================= FOOTER =================
st.markdown("---")
st.caption(f"🔄 Auto-refresh every 30 seconds | Last update: {get_ist_now().strftime('%d %b %Y, %I:%M:%S %p')} IST")
st.caption("🔐 App Protected | Developed by Satish D. Nakhate")
