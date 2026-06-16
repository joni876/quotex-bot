import streamlit as st
import time
from tradingview_ta import TA_Handler, Interval

# موبائل اور ویب پیج کی سیٹنگز
st.set_page_config(page_title="Quotex Signal Bot", page_icon="📈", layout="centered")

# خوبصورت ہیڈنگ
st.markdown("<h1 style='text-align: center; color: #00e676;'>Quotex Fast Signals</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Select pair and timeframe to get instant signal</p>", unsafe_allow_html=True)
st.write("---")

# 1. کرنسی پیئر کا انتخاب
pair = st.selectbox(
    "📊 Select Currency Pair / Asset:",
    ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "BTCUSD", "ETHUSD"]
)

# 2. ٹائم فریم کا انتخاب
timeframe_label = st.radio(
    "⏱️ Select Expiry / Analyze Timeframe:",
    ["5 Seconds", "15 Seconds", "30 Seconds", "60 Seconds"],
    horizontal=True
)

st.write("")

# 3. سگنل جنریٹ کرنے کا بٹن
if st.button("🚀 GENERATE SIGNAL", use_container_width=True):
    # ٹریڈ کے لیے ریڈی ہونے کا ٹائمر (3 سیکنڈ کاؤنٹ ڈاؤن)
    countdown_placeholder = st.empty()
    for seconds_left in range(3, 0, -1):
        countdown_placeholder.markdown(
            f"<div style='text-align:center; padding:10px; background-color:#111; border-radius:5px;'>"
            f"<h3 style='color:#ffea00; margin:0;'>⏳ Get Ready! Opening Trade in {seconds_left}s...</h3>"
            f"</div>", 
            unsafe_allow_html=True
        )
        time.sleep(1)
    
    countdown_placeholder.empty() # ٹائمر ختم ہونے پر اسے صاف کریں

    with st.spinner("Analyzing market indicators..."):
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
            
            st.write("---")
            st.subheader("Signal Result:")
            
            # سگنل دکھانے کا طریقہ کار
            if buy_score > sell_score and buy_score >= 10:
                st.markdown(
                    f"<div style='background-color:#003311; padding:20px; border-radius:10px; border:2px solid #00e676; text-align:center;'> "
                    f"<h2 style='color:#00e676; margin:0;'>🟢 UP (CALL)</h2>"
                    f"<p style='color:white; margin:10px 0 0 0;'><b>Strong Buyers Momentum</b></p>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
            elif sell_score > buy_score and sell_score >= 10:
                st.markdown(
                    f"<div style='background-color:#330000; padding:20px; border-radius:10px; border:2px solid #ff1744; text-align:center;'> "
                    f"<h2 style='color:#ff1744; margin:0;'>🔴 DOWN (PUT)</h2>"
                    f"<p style='color:white; margin:10px 0 0 0;'><b>Strong Sellers Momentum</b></p>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color:#222; padding:20px; border-radius:10px; border:2px solid #ffea00; text-align:center;'> "
                    f"<h2 style='color:#ffea00; margin:0;'>⏳ AVOID / NEUTRAL</h2>"
                    f"<p style='color:white; margin:10px 0 0 0;'><b>Market is choppy. Wait for clear trend.</b></p>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
            # تکنیکی تفصیلات
            st.write("")
            col1, col2, col3 = st.columns(3)
            col1.metric("Buy Indicators", buy_score)
            col2.metric("Neutral", neutral_score)
            col3.metric("Sell Indicators", sell_score)
            
        except Exception as e:
            st.error(f"Error fetching data: {e}. Please try again.")
