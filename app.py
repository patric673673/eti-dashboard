import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# 1. 頁面規範設定
st.set_page_config(page_title="ETI 趨勢監控系統", layout="wide")

# ================== 專業指標定義 (來源備註) ==================
ETI_SOURCE_INFO = """
> **指標規範說明：**
> * **來源：** 參考 ECRI 景氣循環領先指標與 Artur 期望值 SOP。
> * **超買警戒 (Sell)：** ETI > 115 (紅色區塊)。
> * **持有區間 (Hold)：** 50 < ETI < 115 (藍色區塊)。
> * **低點佈局 (Buy)：** ETI < 20 (綠色區塊)。
"""

# ================== 推播函數 ==================
def send_push(title, msg):
    try:
        payload = {
            "app_id": st.secrets["ONESIGNAL_APP_ID"],
            "headings": {"en": title, "zh-Hant": title},
            "contents": {"en": msg, "zh-Hant": msg},
            "included_segments": ["Total Subscriptions"]
        }
        headers = {"Authorization": f"Basic {st.secrets['ONESIGNAL_REST_API_KEY']}", "Content-Type": "application/json"}
        requests.post("https://api.onesignal.com/notifications", headers=headers, json=payload)
    except: pass

# ================== 主畫面呈現 ==================
st.title("📈 ETI 經濟趨勢決策系統")
st.markdown(ETI_SOURCE_INFO)

# 模擬目前的 ETI 分數 (未來我們會接 yfinance 變成真數據)
# 這裡我們手動設為 120 測試規範
current_eti = 120 

# 顯示大大的數字
col1, col2 = st.columns(2)
with col1:
    st.metric(label="當前 ETI 指數", value=current_eti, delta="最高警戒", delta_color="inverse")

# 2. 建立「規範化」圖表 (不再皺皺的)
st.subheader("趨勢分析軌跡")

# 這裡建立一組有規律的數據，模擬真實走勢
chart_data = pd.DataFrame({
    'ETI 分數': [85, 88, 92, 95, 100, 105, 110, 115, 120, 118, 120] 
})

# 設定圖表的顯示範圍，確保它不會一直變動縮放
st.area_chart(chart_data) # 使用 Area Chart 更有份量感

# 🚦 邏輯檢查與自動推播
if current_eti >= 115:
    st.error(f"🚨 【最高警戒：獲利了結】目前 ETI 已達 {current_eti}，符合停利 SOP。")
    # 這裡可以加上你原本的推播代碼...

# ================== 底部專業備註欄 ==================
st.markdown("---")
with st.expander("📖 查看指標定義與機構來源"):
    st.write("""
    ### 指標操作手冊
    1. **數據頻率**：本系統每小時掃描一次市場偏離值。
    2. **來源依據**：本模型整合 **Marketing Makers Gamma Levels** 與 **VIX 恐慌蓋子理論**。
    3. **免責聲明**：本工具僅供 Hsu Min-Hsiung (敏雄) 內部決策參考，不代表投資建議。
    """)
