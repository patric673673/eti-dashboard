import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import numpy as np

# 1. 頁面基礎設定
st.set_page_config(page_title="ETI 專業預警系統", layout="wide")

# 初始化 session_state
if "last_high_eti_push" not in st.session_state:
    st.session_state.last_high_eti_push = 0

# ================== OneSignal 推送函數 ==================
def send_onesignal_notification(title: str, message: str):
    try:
        app_id = st.secrets["ONESIGNAL_APP_ID"]
        api_key = st.secrets["ONESIGNAL_REST_API_KEY"]
        
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {api_key}"
        }
        
        # 這就是你剛才說沒看到的 Payload 區塊
        payload = {
            "app_id": app_id,
            "headings": {"en": title, "zh-Hant": title},
            "contents": {"en": message, "zh-Hant": message},
            "included_segments": ["Total Subscriptions"], 
            "url": "https://share.streamlit.io/patric673673/eti-dashboard/main"
        }
        
        response = requests.post("https://api.onesignal.com/notifications", 
                                 headers=headers, json=payload)
        
        if response.status_code == 200:
            st.success("✅ OneSignal 預警推送已成功發送！")
        else:
            st.error(f"推送失敗。代碼：{response.status_code}")
    except Exception as e:
        st.error(f"系統錯誤: {e}")

# ================== 主畫面呈現 ==================
st.header("📈 ETI 核心分析 - 決策儀表板")

eti_total = 120 # 設定為 120 進行測試

# 🔔 訂閱按鈕
if st.button("🔔 點此開啟行動端即時通知", use_container_width=True, type="primary"):
    st.markdown("""
    <script>
        if (window.OneSignal) { window.OneSignal.showSlidedownPrompt(); }
        else { alert("OneSignal 初始化中..."); }
    </script>
    """, unsafe_allow_html=True)

# 🚦 120 最高標邏輯
if eti_total >= 115:
    st.error(f"### 🚨 【最高警戒：獲利了結】\n目前 ETI：{eti_total}")
    
    current_time = datetime.now().timestamp()
    if (current_time - st.session_state.last_high_eti_push) > 3600:
        send_onesignal_notification("🚨 ETI 最高預警！", f"目前 ETI 達 {eti_total}，建議執行獲利了結。")
        st.session_state.last_high_eti_push = current_time

st.line_chart(pd.DataFrame(np.random.randn(20, 1) + (eti_total/100)))
