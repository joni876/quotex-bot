import streamlit as st
import time
from tradingview_ta import TA_Handler, Interval

# موبائل اور ویب پیج کی سیٹنگز
st.set_page_config(page_title="Quotex VIP Signals", page_icon="📈", layout="centered")

# پٹی غائب کرنے اور ڈارک تھیم کا کسٹم CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden; display: none;}
    footer {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
    .stAppDeployDropdown {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    div[class*="styles_viewerBadge"] {display: none !important;}
    button[title="View fullscreen"] {visibility: hidden; display: none !important;}
    
    .stApp { background-color: #0b0e14; color: #ffffff; }
    div[data-baseweb="select"] > div { background-color: #151a24 !important; color: white !important; border: 1px solid #2a3447 !important; border-radius: 8px !important; }
    div[data-testid="stMarkdownContainer"] p { color: #e0e3eb !important; }
    div.stButton > button { background-color: #00b050 !important; color: white !important; font-weight: bold !important; font-size: 16px !important; border-radius: 8px !important; border: none !important; padding: 10px 20px !important; box-shadow: 0px 4px 15px rgba(0, 176, 80, 0.3) !important; }
    div.stButton > button:hover { background-color: #00cd5d !important; }
    </style>
""", unsafe_allow_html=True)

# سیشن اسٹیٹ میں ڈیٹا بیس بنانا
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@bot.com": {
            "name": "Admin", "phone": "0000", "country": "Pakistan", "address": "Server", 
            "password": "admin786", "status": "Approved", "role": "admin"
        }
    }

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# لاگ آؤٹ فنکشن
def logout():
    st.session_state.logged_in_user = None
    st.rerun()

# ممالک کی لسٹ
countries_list = ["Pakistan", "India", "Bangladesh", "UAE", "Saudi Arabia", "USA", "UK", "Nigeria", "Others"]

# مین ہیڈنگ
st.markdown("<h1 style='text-align: center; color: #00e676; font-family: sans-serif; margin-bottom: 0;'>📈 QUOTEX VIP SIGNALS</h1>", unsafe_allow_html=True)
st.markdown("<div style='border-bottom: 2px solid #1f2633; margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# ---- اگر صارف لاگ ان نہیں ہے ----
if st.session_state.logged_in_user is None:
    tab1, tab2, tab3 = st.tabs(["🔐 LOGIN", "📝 REGISTER", "🔑 FORGOT PASSWORD"])
    
    # 1. لاگ ان پینل
    with tab1:
        st.subheader("Login to Your Account")
        login_email = st.text_input("Email Address:", key="login_email").strip().lower()
        login_pass = st.text_input("Password:", type="password", key="login_pass")
        
        if st.button("SIGN IN", use_container_width=True):
            if login_email in st.session_state.users_db:
                user_data = st.session_state.users_db[login_email]
                if user_data["password"] == login_pass:
                    if user_data["status"] == "Approved":
                        st.session_state.logged_in_user = login_email
                        st.success(f"Welcome back, {user_data['name']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Your account is pending admin approval. Please contact the administrator.")
                else:
                    st.error("❌ Incorrect Password.")
            else:
                st.error("❌ Account not found. Please register first.")
                
    # 2. رجسٹریشن پینل (کنٹری کے ساتھ)
    with tab2:
        st.subheader("Create New Account")
        reg_name = st.text_input("Full Name:")
        reg_phone = st.text_input("Mobile Number:")
        reg_country = st.selectbox("Select Your Country:", countries_list)
        reg_email = st.text_input("Email Address:").strip().lower()
        reg_address = st.text_input("Address:")
        reg_pass = st.text_input("Create Password:", type="password")
        reg_repass = st.text_input("Confirm Password:", type="password")
        
        if st.button("SUBMIT REGISTRATION", use_container_width=True):
            if not (reg_name and reg_phone and reg_email and reg_address and reg_pass and reg_repass):
                st.error("⚠️ All fields are required!")
            elif reg_pass != reg_repass:
                st.error("❌ Passwords do not match!")
            elif reg_email in st.session_state.users_db:
                st.error("❌ This email is already registered!")
            else:
                st.session_state.users_db[reg_email] = {
                    "name": reg_name, "phone": reg_phone, "country": reg_country,
                    "address": reg_address, "password": reg_pass, "status": "Pending", "role": "user"
                }
                st.success("✅ Registered Successfully! Waiting for Admin Approval.")

    # 3. فارگیٹ پاسورڈ پینل
    with tab3:
        st.subheader("Recover Your Password")
        st.write("تصدیق کے لیے اپنی رجسٹرڈ تفصیلات درج کریں:")
        f_email = st.text_input("Enter Registered Email:", key="f_email").strip().lower()
        f_name = st.text_input("Enter Full Name:", key="f_name")
        f_phone = st.text_input("Enter Mobile Number:", key="f_phone")
        
        if st.button("RECOVER PASSWORD", use_container_width=True):
            if f_email in st.session_state.users_db:
                u_data = st.session_state.users_db[f_email]
                if u_data["name"].lower() == f_name.lower() and u_data["phone"] == f_phone:
                    st.success(f"🔑 Your Password is: **{u_data['password']}**")
                else:
                    st.error("❌ معلومات میچ نہیں ہوئیں۔ برائے مہربانی صحیح نام اور موبائل نمبر ڈالیں۔")
            else:
                st.error("❌ یہ ای میل ریکارڈ میں موجود نہیں ہے۔")

# ---- اگر لاگ ان ہو چکا ہے ----
else:
    current_email = st.session_state.logged_in_user
    user_info = st.session_state.users_db[current_email]
    
    # ٹاپ بار
    col_user, col_out = st.columns([4, 1])
    col_user.markdown(f"👤 **Logged in as:** {user_info['name']} ({user_info['country']})")
    if col_out.button("LOGOUT", key="logout_btn"):
        logout()
        
    st.write("---")
    
    # 🔄 پاسورڈ تبدیل کرنے کا آپشن (لاگ ان کے بعد)
    with st.expander("🔄 CHANGE YOUR PASSWORD (پاسورڈ تبدیل کریں)"):
        old_p = st.text_input("Current Password:", type="password", key="old_p")
        new_p = st.text_input("New Password:", type="password", key="new_p")
        confirm_p = st.text_input("Confirm New Password:", type="password", key="confirm_p")
        
        if st.button("UPDATE PASSWORD"):
            if old_p != user_info["password"]:
                st.error("❌ پرانا پاسورڈ غلط ہے!")
            elif new_p != confirm_p:
                st.error("❌ نئے پاسورڈ آپس میں میچ نہیں ہو رہے!")
            elif len(new_p) < 4:
                st.error("⚠️ نیا پاسورڈ کم از کم 4 ہندسوں کا ہونا چاہیے۔")
            else:
                st.session_state.users_db[current_email]["password"] = new_p
                st.success("✅ پاسورڈ کامیابی سے تبدیل ہو گیا ہے!")
                time.sleep(1)
                st.rerun()

    st.write("")

    # ---- ایڈمن پینل لاجک ----
    if user_info["role"] == "admin":
        st.subheader("👑 ADMIN CONTROL PANEL")
        st.write("صارفین کی لسٹ اور منظوری کا پینل:")
        
        for email, data in list(st.session_state.users_db.items()):
            if data["role"] == "admin":
                continue
                
            with st.container():
                st.markdown(f"**Name:** {data['name']} | **Email:** {email} | **Phone:** {data['phone']} | **Country:** {data['country']}")
                st.markdown(f"**Address:** {data['address']} | **Status:** `{data['status']}`")
                
                if data["status"] == "Pending":
                    if st.button(f"Give Access to {data['name']}", key=f"app_{email}"):
                        st.session_state.users_db[email]["status"] = "Approved"
                        st.success(f"Access granted to {data['name']}!")
                        time.sleep(0.5)
                        st.rerun()
                else:
                    if st.button(f"Revoke Access / Block", key=f"rev_{email}"):
                        st.session_state.users_db[email]["status"] = "Pending"
                        st.warning(f"Access revoked for {data['name']}!")
                        time.sleep(0.5)
                        st.rerun()
            st.markdown("<div style='border-bottom: 1px solid #1f2633; margin: 10px 0;'></div>", unsafe_allow_html=True)

    # ---- عام صارف پینل (سگنل بوٹ) ----
    else:
        pair = st.selectbox("📊 SELECT ASSET / CURRENCY PAIR:", ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "BTCUSD", "ETHUSD"])
        timeframe_label = st.radio("⏱️ SELECT EXPIRY TIMEFRAME:", ["5 Seconds", "15 Seconds", "30 Seconds", "60 Seconds"], horizontal=True)
        
        if st.button("🚀 GENERATE INSTANT SIGNAL", use_container_width=True):
            countdown_placeholder = st.empty()
            for seconds_left in range(3, 0, -1):
                countdown_placeholder.markdown(f"<div style='text-align:center; padding:15px; background-color:#1c1901; border: 1px solid #ffea00; border-radius:8px; margin-bottom: 20px;'><h3 style='color:#ffea00; margin:0;'>⏳ READY YOUR SCREEN... {seconds_left}s</h3></div>", unsafe_allow_html=True)
                time.sleep(1)
            countdown_placeholder.empty()

            with st.spinner("Scanning Technical Indicators..."):
                analysis_success = False
                summary = None
                exchanges_to_try = ["FX", "FX_IDC", "OANDA", "BINANCE"] if "USD" in pair and pair not in ["BTCUSD", "ETHUSD"] else ["BINANCE"]
                
                for ex in exchanges_to_try:
                    try:
                        handler = TA_Handler(symbol=pair, screener="crypto" if pair in ["BTCUSD", "ETHUSD"] else "forex", exchange=ex, interval=Interval.INTERVAL_1_MINUTE)
                        analysis = handler.get_analysis()
                        summary = analysis.summary
                        if summary and (summary['BUY'] > 0 or summary['SELL'] > 0):
                            analysis_success = True
                            break
                    except:
                        continue
                        
                if analysis_success and summary:
                    buy_score = summary['BUY']
                    sell_score = summary['SELL']
                    neutral_score = summary['NEUTRAL']
                    
                    st.subheader("🎯 LIVE SIGNAL RESULT:")
                    if buy_score > sell_score and buy_score >= 10:
                        st.markdown("<div style='background-color:#052e16; padding:25px; border-radius:10px; border:2px solid #00e676; text-align:center;'><h1 style='color:#00e676; margin:0; font-size:35px;'>🟢 UP (CALL)</h1></div>", unsafe_allow_html=True)
                    elif sell_score > buy_score and sell_score >= 10:
                        st.markdown("<div style='background-color:#450a0a; padding:25px; border-radius:10px; border:2px solid #ff1744; text-align:center;'><h1 style='color:#ff1744; margin:0; font-size:35px;'>🔴 DOWN (PUT)</h1></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background-color:#1c1c1c; padding:25px; border-radius:10px; border:2px solid #ffea00; text-align:center;'><h1 style='color:#ffea00; margin:0; font-size:32px;'>⏳ AVOID / NEUTRAL</h1></div>", unsafe_allow_html=True)
                    
                    st.write("")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Buy Indicators", buy_score)
                    col2.metric("Neutral", neutral_score)
                    col3.metric("Sell Indicators", sell_score)
                else:
                    st.error("Market data temporarily unavailable.")
