import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. 頁面配置
st.set_page_config(page_title="ETI 專業預警系統", layout="wide")

# ================== OneSignal 推送函數 (您的原始邏輯) ==================
def send_onesignal_notification(title: str, message: str, player_ids: list = None):
    """透過 OneSignal API 發送後端推送"""
    # 檢查 secrets 是否已設定，避免程式崩潰
    if 'ONESIGNAL_REST_API_KEY' not in st.secrets:
        st.warning("請在 Streamlit Secrets 中設定 ONESIGNAL 金鑰")
        return

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {st.secrets['ONESIGNAL_REST_API_KEY']}"
    }
    payload = {
        "app_id": st.secrets['ONESIGNAL_APP_ID'],
        "headings": {"en": title, "zh-Hant": title},      
        "contents": {"en": message, "zh-Hant": message},    
        "url": "https://your-app.streamlit.app"   # 記得換成您的實際網址
    }
    try:
        response = requests.post("https://api.onesignal.com/notifications", 
                                 headers=headers, json=payload)
        if response.status_code == 200:
            st.success("✅ OneSignal 預警推送已成功發送")
        else:
            st.error(f"推送失敗: {response.text}")
    except Exception as e:
        st.error(f"推送異常: {e}")

# ================== 主程式介面 ==================

st.header("🚀 ETI 核心趨勢與 OneSignal 預警")

# 這裡設定當前 ETI (設定為 120 進行測試)
eti_total = 120 

# 使用者訂閱按鈕
if st.button("🔔 開啟 ETI 即時推送通知 (OneSignal)", use_container_width=True, type="primary"):
    st.markdown("""
    <script>
        if (window.OneSignal) {
            OneSignal.showSlidedownPrompt();
        } else {
            alert("OneSignal 尚未初始化，請確認 static 資料夾內的 SDK 檔案");
        }
    </script>
    """, unsafe_allow_html=True)
    st.info("請在彈出的視窗中點選「允許通知」")

st.markdown("---")

# 🚦 自動推送邏輯 (依照您的 120 最高標)
if eti_total >= 115:
    status_msg = "🚨 【最高警戒：獲利了結】"
    status_type = "error"
    
    # 自動推送範例：1小時內不重複發送
    last_push = st.session_state.get("last_high_eti_push", 0)
    current_time = datetime.now().timestamp()
    
    if (current_time - last_push) > 3600:
        send_onesignal_notification(
            title="🚨 ETI 最高預警！",
            message=f"目前 ETI 達 {eti_total} → 進入最高壓力區，建議執行獲利了結。"
        )
        st.session_state.last_high_eti_push = current_time

elif eti_total <= 85:
    status_msg = "✅ 【建議分批進場】"
    status_type = "success"
else:
    status_msg = "💡 【暫時觀望】"
    status_type = "info"

# 顯示視覺看板
col1, col2 = st.columns([1, 2])
with col1:
    st.metric(label="當前 ETI 指數", value=eti_total, delta="最高點")
with col2:
    if status_type == "error":
        st.error(f"### {status_msg}")
    elif status_type == "success":
        st.success(f"### {status_msg}")
    else:
        st.info(f"### {status_msg}")

# 趨勢圖表
st.write("### 歷史趨勢參考")
chart_data = pd.DataFrame(np.random.randn(20, 1) + (eti_total/100), columns=['ETI 指數'])
st.line_chart(chart_data)
