import streamlit as st
import time
import json
import os
from tradingview_ta import TA_Handler, Interval

# پیج سیٹنگز
st.set_page_config(page_title="VIP Trading Terminal", page_icon="📈", layout="centered")

# مستقل فائل کا نام جہاں صارفین کا ڈیٹا سیو رہے گا
DB_FILE = "users_db.json"

# ڈیٹا بیس کو فائل سے لوڈ کرنے اور سیو کرنے کے فنکشنز
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    # ڈیفالٹ ایڈمن اکاؤنٹ
    return {
        "admin@bot.com": {
            "name": "Admin", "phone": "0000", "country": "Pakistan", "address": "Server", 
            "password": "admin786", "status": "Approved", "role": "admin"
        }
    }

def save_db(db_data):
    with open(DB_FILE, "w") as f:
        json.dump(db_data, f, indent=4)

# سیشن اسٹیٹ میں ڈیٹا لوڈ کرنا
if "users_db" not in st.session_state:
    st.session_state.users_db = load_db()

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# کسٹم اسٹائلنگ - پٹی غائب کرنے اور چمکدار سفید ٹیکسٹ کے لیے
st.markdown("""
    <style>
    #MainMenu {visibility: hidden; display: none;}
    footer {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
    .stAppDeployDropdown {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    button[title="View fullscreen"] {visibility: hidden; display: none !important;}
    
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* لیبلز کو بالکل سفید اور واضح کرنے کے لیے */
    div[data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    input { color: #ffffff !important; background-color: #151a24 !important; }
    div[data-baseweb="select"] > div { background-color: #151a24 !important; color: white !important; border: 1px solid #2a3447 !important; border-radius: 8px !important; }
    
    div.stButton > button { 
        background-color: #00b050 !important; color: white !important; font-weight: bold; font-size: 16px !important;
        border-radius: 8px !important; width: 100%; border: none !important;
        box-shadow: 0px 4px 15px rgba(0, 176, 80, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

countries_list = ["Pakistan", "India", "Bangladesh", "UAE", "Saudi Arabia", "USA", "UK", "Others"]

st.markdown("<h1 style='text-align: center; color: #00e676;'>📈 VIP SIGNAL CONTROLLER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a3b1cc; font-size: 14px;'>Secure Financial Analysis Interface</p>", unsafe_allow_html=True)
st.markdown("<div style='border-bottom: 2px solid #1f2633; margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# لاگ ان اور رجسٹریشن سسٹم
if st.session_state.logged_in_user is None:
    tab1, tab2, tab3 = st.tabs(["🔐 MEMBER ACCESS", "📝 REQUEST ACCESS", "🔑 RECOVERY"])
    
    with tab1:
        st.markdown("<h4 style='color:#00e676;'>Enter your registered credentials:</h4>", unsafe_allow_html=True)
        login_email = st.text_input("User ID (Email):", key="l_email").strip().lower()
        login_pass = st.text_input("Access Key (Password):", type="password", key="l_pass")
        
        if st.button("VERIFY & ENTER", key="btn_login"):
            # فائل سے تازہ ترین ڈیٹا لوڈ کریں
            st.session_state.users_db = load_db()
            
            if login_email in st.session_state.users_db:
                user_data = st.session_state.users_db[login_email]
                if user_data["password"] == login_pass:
                    if user_data["status"] == "Approved":
                        st.session_state.logged_in_user = login_email
                        st.success("Access Granted!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Your account is pending admin verification.")
                else:
                    st.error("❌ Invalid Access Key.")
            else:
                st.error("❌ ID not registered.")
                
    with tab2:
        st.subheader("Account Application")
        reg_name = st.text_input("Your Full Name:")
        reg_phone = st.text_input("Mobile Number:")
        reg_country = st.selectbox("Your Country:", countries_list)
        reg_email = st.text_input("Email ID:").strip().lower()
        reg_address = st.text_input("Postal Address:")
        reg_pass = st.text_input("Choose Password:", type="password")
        reg_repass = st.text_input("Retype Password:", type="password")
        
        if st.button("SUBMIT APPLICATION", key="btn_reg"):
            st.session_state.users_db = load_db()
            
            if not (reg_name and reg_phone and reg_email and reg_address and reg_pass and reg_repass):
                st.error("⚠️ All fields are mandatory!")
            elif reg_pass != reg_repass:
                st.error("❌ Passwords do not match!")
            elif reg_email in st.session_state.users_db:
                st.error("❌ This ID is already in use.")
            else:
                # نئے صارف کو شامل کریں اور فائل میں محفوظ کریں
                st.session_state.users_db[reg_email] = {
                    "name": reg_name, "phone": reg_phone, "country": reg_country,
                    "address": reg_address, "password": reg_pass, "status": "Pending", "role": "user"
                }
                save_db(st.session_state.users_db)
                st.success("✅ Application submitted! Please ask Admin to approve your ID.")

    with tab3:
        st.subheader("Credential Recovery")
        f_email = st.text_input("Registered Email:", key="f_email").strip().lower()
        f_name = st.text_input("Full Name:", key="f_name")
        f_phone = st.text_input("Mobile Number:", key="f_phone")
        
        if st.button("RETRIEVE ACCESS KEY", key="btn_forgot"):
            st.session_state.users_db = load_db()
            if f_email in st.session_state.users_db:
                u_data = st.session_state.users_db[f_email]
                if u_data["name"].lower() == f_name.lower() and u_data["phone"] == f_phone:
                    st.success(f"🔑 Your Access Key is: **{u_data['password']}**")
                else:
                    st.error("❌ Identity check failed. Incorrect details.")
            else:
                st.error("❌ No such ID found.")

else:
    current_email = st.session_state.logged_in_user
    user_info = st.session_state.users_db[current_email]
    
    col_user, col_out = st.columns([4, 1])
    col_user.markdown(f"👤 **Active Session:** {user_info['name']} ({user_info['country']})")
    if col_out.button("DISCONNECT", key="logout_btn"):
        st.session_state.logged_in_user = None
        st.rerun()
        
    st.write("---")
    
    with st.expander("🔄 MODIFY ACCESS KEY"):
        old_p = st.text_input("Old Password:", type="password", key="old_p")
        new_p = st.text_input("New Password:", type="password", key="new_p")
        confirm_p = st.text_input("Confirm Password:", type="password", key="confirm_p")
        
        if st.button("SAVE CHANGES"):
            st.session_state.users_db = load_db()
            if old_p != user_info["password"]:
                st.error("❌ Incorrect old password.")
            elif new_p != confirm_p:
                st.error("❌ New passwords mismatch.")
            elif len(new_p) < 4:
                st.error("⚠️ Must be at least 4 characters.")
            else:
                st.session_state.users_db[current_email]["password"] = new_p
                save_db(st.session_state.users_db)
                st.success("✅ Password updated successfully!")
                time.sleep(1)
                st.rerun()

    st.write("")

    if user_info["role"] == "admin":
        st.subheader("👑 TERMINAL CONTROLLER PANEL")
        st.session_state.users_db = load_db()
        
        for email, data in list(st.session_state.users_db.items()):
            if data["role"] == "admin":
                continue
                
            with st.container():
                st.markdown(f"**Name:** {data['name']} | **Country:** {data['country']} | **Phone:** {data['phone']}")
                st.markdown(f"**Email:** {email} | **Status:** `{data['status']}`")
                
                if data["status"] == "Pending":
                    if st.button(f"Approve Account", key=f"app_{email}"):
                        st.session_state.users_db[email]["status"] = "Approved"
                        save_db(st.session_state.users_db)
                        st.success("Approved!")
                        time.sleep(0.5)
                        st.rerun()
                else:
                    if st.button(f"Revoke Access / Block ID", key=f"rev_{email}"):
                        st.session_state.users_db[email]["status"] = "Pending"
                        save_db(st.session_state.users_db)
                        st.warning("Blocked!")
                        time.sleep(0.5)
                        st.rerun()
            st.markdown("<div style='border-bottom: 1px solid #1f2633; margin: 10px 0;'></div>", unsafe_allow_html=True)

    else:
        # بائنری سگنل بوٹ لاجک
        pair = st.selectbox("📊 SELECT ASSET / CURRENCY PAIR:", ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "BTCUSD", "ETHUSD"])
        timeframe_label = st.radio("⏱️ SELECT EXPIRY TIMEFRAME:", ["5 Seconds", "15 Seconds", "30 Seconds", "60 Seconds"], horizontal=True)
        
        if st.button("🚀 GENERATE INSTANT SIGNAL", use_container_width=True):
            countdown_placeholder = st.empty()
            for seconds_left in range(3, 0, -1):
                countdown_placeholder.markdown(f"<div style='text-align:center; padding:15px; background-color:#1c1901; border: 1px solid #ffea00; border-radius:8px; margin-bottom: 20px;'><h3 style='color:#ffea00; margin:0;'>⏳ READY YOUR SCREEN... {seconds_left}s</h3></div>", unsafe_allow_html=True)
                time.sleep(1)
            countdown_placeholder.empty()

            with st.spinner("Analyzing Market Flow..."):
                analysis_success = False
                summary = None
                
                exchanges_to_try = ["FX_IDC", "OANDA", "FOREXCOM", "SAXO"] if "USD" in pair and pair not in ["BTCUSD", "ETHUSD"] else ["BINANCE"]
                
                for ex in exchanges_to_try:
                    try:
                        handler = TA_Handler(
                            symbol=pair,
                            screener="crypto" if pair in ["BTCUSD", "ETHUSD"] else "forex",
                            exchange=ex,
                            interval=Interval.INTERVAL_1_MINUTE
                        )
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
                    st.error("Market data server timed out. Please click generate again.")
