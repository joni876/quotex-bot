import streamlit as st
import time
import json
import os
from tradingview_ta import TA_Handler, Interval

# पेज सेटिंग्स
st.set_page_config(page_title="VIP Trading Terminal", page_icon="📈", layout="centered")

DB_FILE = "users_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "admin@bot.com": {
            "name": "Admin", "phone": "0000", "country": "Pakistan", "address": "Server", 
            "password": "admin786", "status": "Approved", "role": "admin"
        }
    }

def save_db(db_data):
    with open(DB_FILE, "w") as f:
        json.dump(db_data, f, indent=4)

if "users_db" not in st.session_state:
    st.session_state.users_db = load_db()

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# कस्टम डार्क थीम स्टाइलिंग
st.markdown("""
    <style>
    #MainMenu {visibility: hidden; display: none;}
    footer {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none;}
    .stApp { background-color: #0b0e14; color: #ffffff; }
    div[data-testid="stWidgetLabel"] p { color: #ffffff !important; font-size: 16px !important; font-weight: 600 !important; }
    div.stButton > button { background-color: #00b050 !important; color: white !important; font-weight: bold; font-size: 16px !important; border-radius: 8px !important; width: 100%; border: none !important; box-shadow: 0px 4px 15px rgba(0, 176, 80, 0.4) !important;}
    .price-box { background-color: #151a24; padding: 15px; border-radius: 8px; border-left: 4px solid #00e676; margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

countries_list = ["Pakistan", "India", "Bangladesh", "UAE", "Saudi Arabia", "USA", "UK", "Others"]

st.markdown("<h1 style='text-align: center; color: #00e676;'>📈 VIP SIGNAL CONTROLLER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a3b1cc; font-size: 14px;'>Real-Time Market Rate & Analysis Dashboard</p>", unsafe_allow_html=True)
st.markdown("<div style='border-bottom: 2px solid #1f2633; margin-bottom: 25px;'></div>", unsafe_allow_html=True)

if st.session_state.logged_in_user is None:
    tab1, tab2 = st.tabs(["🔐 MEMBER ACCESS", "📝 REQUEST ACCESS"])
    with tab1:
        login_email = st.text_input("User ID (Email):", key="l_email").strip().lower()
        login_pass = st.text_input("Access Key (Password):", type="password", key="l_pass")
        if st.button("VERIFY & ENTER"):
            if login_email in st.session_state.users_db and st.session_state.users_db[login_email]["password"] == login_pass:
                if st.session_state.users_db[login_email]["status"] == "Approved":
                    st.session_state.logged_in_user = login_email
                    st.success("Access Granted!")
                    st.rerun()
                else:
                    st.error("❌ Your account is pending admin verification.")
            else:
                st.error("❌ Invalid Credentials.")
    with tab2:
        reg_name = st.text_input("Your Full Name:")
        reg_phone = st.text_input("Mobile Number:")
        reg_country = st.selectbox("Your Country:", countries_list)
        reg_email = st.text_input("Email ID:").strip().lower()
        reg_address = st.text_input("Postal Address:")
        reg_pass = st.text_input("Choose Password:", type="password")
        if st.button("SUBMIT APPLICATION"):
            if reg_name and reg_phone and reg_email and reg_pass:
                st.session_state.users_db[reg_email] = {
                    "name": reg_name, "phone": reg_phone, "country": reg_country,
                    "address": reg_address, "password": reg_pass, "status": "Pending", "role": "user"
                }
                save_db(st.session_state.users_db)
                st.success("✅ Application submitted!")
else:
    current_email = st.session_state.logged_in_user
    user_info = st.session_state.users_db[current_email]
    
    if st.button("DISCONNECT Session"):
        st.session_state.logged_in_user = None
        st.rerun()
        
    st.write("---")
        
    if user_info["role"] == "admin":
        st.subheader("👑 ADMIN CONTROL PANEL")
        for email, data in list(st.session_state.users_db.items()):
            if data["role"] == "admin": continue
            st.write(f"**{data['name']}** ({email}) - Status: `{data['status']}`")
            if data["status"] == "Pending" and st.button(f"Approve {data['name']}", key=f"app_{email}"):
                st.session_state.users_db[email]["status"] = "Approved"
                save_db(st.session_state.users_db)
                st.rerun()
    else:
        # यूजर के लिए सिग्नल पैनल
        pair = st.selectbox("📊 SELECT ASSET / CURRENCY PAIR:", ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "BTCUSD", "ETHUSD"])
        timeframe = st.radio("⏱️ SELECT EXPIRY TIMEFRAME:", ["5 Seconds", "15 Seconds", "30 Seconds", "60 Seconds"], horizontal=True)
        
        # लाइव रेट फ़ेच करने की लॉजिक
        screener_type = "crypto" if pair in ["BTCUSD", "ETHUSD"] else "forex"
        exchange_type = "BINANCE" if screener_type == "crypto" else "FX_IDC"
        
        current_price = "Fetching..."
        try:
            handler_price = TA_Handler(
                symbol=pair,
                screener=screener_type,
                exchange=exchange_type,
                interval=Interval.INTERVAL_1_MINUTE,
                timeout=5
            )
            analysis_p = handler_price.get_analysis()
            if analysis_p and analysis_p.indicators:
                # क्लोजिंग प्राइस ही लाइव करंट रेट होता है
                current_price = analysis_p.indicators.get("close", "N/A")
        except:
            current_price = "Market Live (Click Generate to refresh)"

        # लाइव रेट को स्क्रीन पर सुंदर बॉक्स में दिखाना
        st.markdown(f"""
            <div class='price-box'>
                <span style='color: #a3b1cc; font-size: 14px; font-weight: bold;'>CURRENT LIVE RATE FOR {pair}:</span><br>
                <span style='color: #00e676; font-size: 26px; font-weight: 800;'>{current_price}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 GENERATE INSTANT SIGNAL", use_container_width=True):
            with st.spinner("Analyzing Live Indicators & Price Action..."):
                try:
                    handler = TA_Handler(
                        symbol=pair,
                        screener=screener_type,
                        exchange=exchange_type,
                        interval=Interval.INTERVAL_1_MINUTE,
                        timeout=8
                    )
                    analysis = handler.get_analysis()
                    summary = analysis.summary
                    
                    buy = summary.get('BUY', 0)
                    sell = summary.get('SELL', 0)
                    neutral = summary.get('NEUTRAL', 0)
                    
                    st.subheader("🎯 LIVE SIGNAL RESULT:")
                    if buy > sell and buy >= 12:
                        st.markdown("<div style='background-color:#052e16; padding:25px; border-radius:10px; border:2px solid #00e676; text-align:center;'><h1 style='color:#00e676; margin:0; font-size:35px;'>🟢 UP (CALL)</h1><p style='color:#ffffff; margin:5px 0 0 0;'>Strong Technical Buying Pressure</p></div>", unsafe_allow_html=True)
                    elif sell > buy and sell >= 12:
                        st.markdown("<div style='background-color:#450a0a; padding:25px; border-radius:10px; border:2px solid #ff1744; text-align:center;'><h1 style='color:#ff1744; margin:0; font-size:35px;'>🔴 DOWN (PUT)</h1><p style='color:#ffffff; margin:5px 0 0 0;'>Strong Technical Selling Pressure</p></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background-color:#1c1c1c; padding:25px; border-radius:10px; border:2px solid #ffea00; text-align:center;'><h1 style='color:#ffea00; margin:0; font-size:32px;'>⏳ AVOID / NEUTRAL</h1><p style='color:#ffffff; margin:5px 0 0 0;'>Market is Sideways / Unstable</p></div>", unsafe_allow_html=True)
                        
                    st.write("")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Buy Indicators", buy)
                    col2.metric("Neutral", neutral)
                    col3.metric("Sell Indicators", sell)
                except Exception as e:
                    st.error("⚠️ Server data busy. Please click the button again to reload.")
