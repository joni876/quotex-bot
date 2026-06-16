import streamlit as st
import time
from tradingview_ta import TA_Handler, Interval

# موبائل اور ویب پیج کی سیٹنگز
st.set_page_config(page_title="Quotex VIP Signals", page_icon="📈", layout="centered")

# کسٹم پرو ٹریڈنگ ڈارک تھیم (CSS)
professional_dark_theme = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            button[title="View fullscreen"] {visibility: hidden;}
            
            /* پورا بیک گراؤنڈ بلیک/ڈارک کرنا */
            .stApp {
                background-color: #0b0e14;
                color: #ffffff;
            }
            
            /* ڈراپ ڈاؤن اور ان پٹ بکس کا ڈیزائن */
            div[data-baseweb="select"] > div {
                background-color: #151a24 !important;
                color: white !important;
                border: 1px solid #2a3447 !important;
                border-radius: 8px !important;
            }
            
            /* ریڈیو بٹنز (Timeframe) کا ڈیزائن */
            div[data-testid="stMarkdownContainer"] p {
                color: #e0e3eb !important;
            }
            
            /* جنریٹ سگنل بٹن کو کوٹیکس جیسا گرین بنانا */
            div.stButton > button {
                background-color: #00b050 !important;
                color: white !important;
                font-weight: bold !important;
                font-size: 18px !important;
                border-radius: 8px !important;
                border: none !important;
                padding: 12px 20px !important;
                box-shadow: 0px 4px 15px rgba(0, 176, 80, 0.4) !important;
                transition: all 0.3s ease !important;
            }
            div.stButton > button:hover {
                background-color: #00cd5d !important;
                transform: scale(1.02);
            }
            </style>
            """
st.markdown(professional_dark_theme, unsafe_allow_html=True)

# خوبصورت ہیڈنگ (Quotex VIP اسٹائل)
st.markdown("<h1 style='text-align: center; color: #00e676; font-family: sans-serif; margin-bottom: 0;'>📈 QUOTEX VIP SIGNALS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #707a8a; font-family: sans-serif; font-size: 14px;'>AI-Powered Real-Time Market Analysis Dashboard</p>", unsafe_allow_html=True)
st.markdown("<div style='border-bottom: 2px solid #1f2633; margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# 1. کرنسی پیئر کا انتخاب
pair = st.selectbox(
    "📊 SELECT ASSET / CURRENCY PAIR:",
    ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "BTCUSD", "ETHUSD"]
)

st.write("")

# 2. ٹائم فریم کا انتخاب
timeframe_label = st.radio(
    "⏱️ SELECT EXPIRY TIMEFRAME:",
    ["5 Seconds", "15 Seconds", "30 Seconds", "60 Seconds"],
    horizontal=True
)

st.write("")
st.write("")

# 3. سگنل جنریٹ کرنے کا بٹن
if st.button("🚀 GENERATE INSTANT SIGNAL", use_container_width=True):
    # ٹریڈ کے لیے ریڈی ہونے کا ٹائمر (3 سیکنڈ کاؤنٹ ڈاؤن)
    countdown_placeholder = st.empty()
    for seconds_left in range(3, 0, -1):
        countdown_placeholder.markdown(
            f"<div style='text-align:center; padding:15px; background-color:#1c1901; border: 1px solid #ffea00; border-radius:8px; margin-bottom: 20px;'>"
            f"<h3 style='color:#ffea00; margin:0; font-family: sans-serif;'>⏳ READY YOUR QUOTEX SCREEN... {seconds_left}s</h3>"
            f"</div>", 
            unsafe_allow_html=True
        )
        time.sleep(1)
    
    countdown_placeholder.empty() 

    with st.spinner("Scanning Technical Indicators..."):
        try:
            # TradingView سے لائیو ڈیٹا فیچ کرنا
            handler = TA_Handler(
                symbol=pair,
                screener="forex" if "USD" in pair and pair != "BTCUSD" and pair != "ETHUSD" else "crypto",
                exchange="FX_IDC" if "USD" in pair and pair != "BTCUSD" and pair != "ETHUSD" else "BINANCE",
                interval=Interval.INTERVAL_1_MINUTE 
            )
            
            analysis = handler.get_analysis()
            summary = analysis.summary
            
            buy_score = summary['BUY']
            sell_score = summary['SELL']
            neutral_score = summary['NEUTRAL']
            
            st.markdown("<div style='border-bottom: 1px solid #1f2633; margin: 25px 0;'></div>", unsafe_allow_html=True)
            st.subheader("🎯 LIVE SIGNAL RESULT:")
            
            # سگنل دکھانے کا طریقہ کار
            if buy_score > sell_score and buy_score >= 10:
                st.markdown(
                    f"<div style='background-color:#052e16; padding:25px; border-radius:10px; border:2px solid #00e676; text-align:center; box-shadow: 0px 0px 20px rgba(0,230,118,0.2);'>"
                    f"<h1 style='color:#00e676; margin:0; font-size: 35px; font-weight: bold;'>🟢 UP (CALL)</h1>"
                    f"<p style='color:#a7f3d0; margin:10px 0 0 0; font-size:16px;'><b>Market Sentiment: Strong Bullish Pressure</b></p>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
            elif sell_score > buy_score and sell_score >= 10:
                st.markdown(
                    f"<div style='background-color:#450a0a; padding:25px; border-radius:10px; border:2px solid #ff1744; text-align:center; box-shadow: 0px 0px 20px rgba(255,23,68,0.2);'>"
                    f"<h1 style='color:#ff1744; margin:0; font-size: 35px; font-weight: bold;'>🔴 DOWN (PUT)</h1>"
                    f"<p style='color:#fecaca; margin:10px 0 0 0; font-size:16px;'><b>Market Sentiment: Strong Bearish Pressure</b></p>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color:#1c1c1c; padding:25px; border-radius:10px; border:2px solid #ffea00; text-align:center;'>"
                    f"<h1 style='color:#ffea00; margin:0; font-size:32px;'>⏳ AVOID / NEUTRAL</h1>"
                    f"<p style='color:#fff9db; margin:10px 0 0 0; font-size:16px;'><b>Market is choppy. Wait for clear volume.</b></p>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
            # تکنیکی میٹرکس
            st.write("")
            st.write("")
            col1, col2, col3 = st.columns(3)
            col1.metric("Buy Indicators", buy_score)
            col2.metric("Neutral", neutral_score)
            col3.metric("Sell Indicators", sell_score)
            
        except Exception as e:
            st.error(f"Error connecting to server. Please try again.")
