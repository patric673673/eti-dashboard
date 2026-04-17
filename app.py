import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import numpy as np

# 1. 頁面基礎設定
st.set_page_config(page_title="ETI 專業預警系統", layout="wide")

# 初始化 session_state，避免重複發送推播
if "last_high_eti_push" not in st.session_state:
    st.session_state.last_high_eti_push = 0

# ================== OneSignal 推送函數 ==================
def send_onesignal_notification(title: str, message: str):
    """透過 OneSignal API 發送推送給所有訂閱者"""
    try:
        app_id = st.secrets["ONESIGNAL_APP_ID"]
        api_key = st.secrets["ONESIGNAL_REST_API_KEY"]
        
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {api_key}"
        }
        
        # 這裡就是你剛才說沒看到的 Payload 區塊
        payload = {
            "app_id": app_id,
            "headings": {"en": title, "zh-Hant": title},
            "contents": {"en": message, "zh-Hant": message},
            "included_segments": ["Total Subscriptions"], # 發給所有人
            "url": "https://share.streamlit.io/patric673673/eti-dashboard/main"
        }
        
        response = requests.post("https://api.onesignal.com/notifications", 
                                 headers=headers, json=payload)
        
        if response.status_code == 200:
            st.success("✅ OneSignal 預警推送已成功發送！")
        else:
            st.error(f"推送失敗，請檢查金鑰或訂閱人數。代碼：{response.status_code}")
    except Exception as e:
        st.error(f"系統錯誤: {e}")

# ================== 主畫面呈現 ==================
st.header("🚀 ETI 核心趨勢與 OneSignal 預警")

# 這裡設定目前的 ETI 數值
eti_total = 120 

# 🔔 訂閱按鈕 (這一步一定要點，否則收不到)
if st.button("🔔 點此開啟行動端即時通知", use_container_width=True, type="primary"):
    st.markdown("""
    <script>
        if (window.OneSignal) {
            OneSignal.showSlidedownPrompt();
        } else {
            alert("OneSignal 正在初始化，請稍候再試");
        }
    </script>
    """, unsafe_allow_html=True)
    st.info("請在彈出的視窗中點選「允許通知」")

st.markdown("---")

# 🚦 您的操作原則：120 最高標自動推播
if eti_total >= 115:
    st.error(f"### 🚨 【最高警戒：獲利了結】\n目前 ETI 已達 {eti_total}。建議紀律執行賣出。")
    
    # 檢查是否一小時內已經推過，避免重複干擾
    current_time = datetime.now().timestamp()
    if (current_time - st.session_state.last_high_eti_push) > 3600:
        send_onesignal_notification(
            title="🚨 ETI 最高預警！",
            message=f"目前 ETI 達 {eti_total}，已進入最高壓力區，建議執行獲利了結。"
        )
        st.session_state.last_high_eti_push = current_time

# 繪製圖表
chart_data = pd.DataFrame(np.random.randn(20, 1) + (eti_total/100), columns=['ETI 指數'])
st.line_chart(chart_data)
