import streamlit as st
import time
from tradingview_ta import TA_Handler, Interval

# موبائل اور ویب پیج کی سیٹنگز
st.set_page_config(page_title="Quotex VIP Signals", page_icon="📈", layout="centered")

# ڈارک تھیم اور پٹی غائب کرنے کا CSS
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

# عارضی ڈیٹا بیس (جب تک ایپ چل رہی ہے ڈیٹا محفوظ رہے گا)
# نوٹ: مستقل اسٹوریج کے لیے مستقبل میں اس میں ڈیٹا بیس لنک کیا جا سکتا ہے
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@bot.com": {
            "name": "Admin", "phone": "0000", "address": "Server", 
            "password": "admin786", "status": "Approved", "role": "admin"
        }
    }

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# لاگ آؤٹ فنکشن
def logout():
    st.session_state.logged_in_user = None
    st.rerun()

# ہیڈنگ
st.markdown("<h1 style='text-align: center; color: #00e676; font-family: sans-serif; margin-bottom: 0;'>📈 QUOTEX VIP SIGNALS</h1>", unsafe_allow_html=True)
st.markdown("<div style='border-bottom: 2px solid #1f2633; margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# اگر صارف لاگ ان نہیں ہے تو لاگ ان/رجسٹریشن اسکرین دکھائیں
if st.session_state.logged_in_user is None:
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
    
    # ---- لاگ ان پینل ----
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
                
    # ---- رجسٹریشن پینل ----
    with tab2:
        st.subheader("Create New Account")
        reg_name = st.text_input("Full Name:")
        reg_phone = st.text_input("Mobile Number:")
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
                # نیا صارف بغیر ایکسیس (Pending) کے سیو ہوگا
                st.session_state.users_db[reg_email] = {
                    "name": reg_name,
                    "phone": reg_phone,
                    "address": reg_address,
                    "password": reg_pass,
                    "status": "Pending",
                    "role": "user"
                }
                st.success("✅ Registered Successfully! Waiting for Admin Approval.")
                st.info("آپ کا اکاؤنٹ بن گیا ہے۔ جیسے ہی ایڈمن آپ کو ایکسیس دیں گے، آپ لاگ ان کر سکیں گے۔")

# اگر لاگ ان ہو چکا ہے
else:
    current_email = st.session_state.logged_in_user
    user_info = st.session_state.users_db[current_email]
    
    # ٹاپ بار (صارف کا نام اور لاگ آؤٹ بٹن)
    col_user, col_out = st.columns([4, 1])
    col_user.markdown(f"👤 **Logged in as:** {user_info['name']} ({user_info['role'].upper()})")
    if col_out.button("LOGOUT", key="logout_btn"):
        logout()
        
    st.write("---")

    # ---- اگر ایڈمن لاگ ان ہے تو ایڈمن پینل دکھائیں ----
    if user_info["role"] == "admin":
        st.subheader("👑 ADMIN CONTROL PANEL")
        st.write("Manage user access and approvals:")
        
        # تمام صارفین کی لسٹ دکھانا
        for email, data in list(st.session_state.users_db.items()):
            if data["role"] == "admin":
                continue
                
            with st.container():
                st.markdown(f"**Name:** {data['name']} | **Email:** {email} | **Phone:** {data['phone']}")
                st.markdown(f"**Address:** {data['address']} | **Status:** `{data['status']}`")
                
                # ایکسیس دینے یا بلاک کرنے کا بٹن
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

    # ---- اگر عام صارف لاگ ان ہے تو اسے بوٹ ڈیش بورڈ دکھائیں ----
    else:
        # یہاں آپ کا اصل سگنل بوٹ والا لاجک چلے گا
        pair = st.selectbox("📊 SELECT ASSET / CURRENCY PAIR:", ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "BTCUSD", "ETHUSD"])
        timeframe_label = st.radio("⏱️ SELECT EXPIRY TIMEFRAME:", ["5 Seconds", "15 Seconds", "30 Seconds", "60 Seconds"], horizontal=True)
        
        if st.button("🚀 GENERATE INSTANT SIGNAL", use_container_width=True):
            with st.spinner("Scanning Technical Indicators..."):
                try:
                    handler = TA_Handler(symbol=pair, screener="forex" if "USD" in pair and pair not in ["BTCUSD", "ETHUSD"] else "crypto", exchange="FX_IDC" if "USD" in pair and pair not in ["BTCUSD", "ETHUSD"] else "BINANCE", interval=Interval.INTERVAL_1_MINUTE)
                    analysis = handler.get_analysis()
                    summary = analysis.summary
                    
                    buy_score = summary['BUY']
                    sell_score = summary['SELL']
                    
                    st.subheader("🎯 LIVE SIGNAL RESULT:")
                    if buy_score > sell_score and buy_score >= 10:
                        st.markdown("<div style='background-color:#052e16; padding:20px; border-radius:10px; border:2px solid #00e676; text-align:center;'><h2 style='color:#00e676; margin:0;'>🟢 UP (CALL)</h2></div>", unsafe_allow_html=True)
                    elif sell_score > buy_score and sell_score >= 10:
                        st.markdown("<div style='background-color:#450a0a; padding:20px; border-radius:10px; border:2px solid #ff1744; text-align:center;'><h2 style='color:#ff1744; margin:0;'>🔴 DOWN (PUT)</h2></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background-color:#1c1c1c; padding:20px; border-radius:10px; border:2px solid #ffea00; text-align:center;'><h2 style='color:#ffea00; margin:0;'>⏳ AVOID / NEUTRAL</h2></div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error("Market data temporarily unavailable.")
