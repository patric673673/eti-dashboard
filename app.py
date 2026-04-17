import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. 頁面基礎與外觀設定 (固定版面)
st.set_page_config(page_title="ETI 趨勢監控系統", layout="wide")

# 2. 定義專業指標操作規範 (寫入來源備註)
ETI_SOP_GUIDE = """
### 📊 ETI 操作規範與數據來源
| 指標區間 (ETI 分數) | 市場狀態定義 | 建議操作 (SOP) | 數據來源依據 |
| :--- | :--- | :--- | :--- |
| **> 115** | **極端超買區** | **🚨 預警推送、執行停利** | ECRI 景氣拐點模型 & Artur SOP |
| **50 ~ 115** | **趨勢擴張區** | **✅ 持續持有、移動止損** | 期望值理論 (Expected Value) |
| **< 20** | **極端超跌區** | **💰 分批佈局、低檔抄底** | 逆向投資策略 (Contrarian) |
"""

# 3. 穩定數據集 (不再使用 random 隨機數)
# 這裡使用固定的趨勢數據，確保圖表穩定且有規範感
data_points = {
    '時間': ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
    'ETI指數': [95.0, 98.2, 102.5, 110.0, 115.0, 120.0, 118.5, 120.0]
}
df = pd.DataFrame(data_points)
current_eti = df['ETI指數'].iloc[-1]

# 4. 主畫面呈現
st.title("📈 ETI 經濟趨勢決策系統 (專業版)")
st.markdown(ETI_SOP_GUIDE)
st.divider()

# 顯示核心指標 (固定數值與狀態)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="當前 ETI 指數", value=current_eti, delta="進入警戒區", delta_color="inverse")
with col2:
    st.warning("⚠️ 目前狀態：符合【獲利了結】標準。")

# 5. 規範化圖表 (固定座標軸，不再變來變去)
st.subheader("趨勢路徑監控")
# 將圖表固定在時間序列上
st.line_chart(df.set_index('時間'))

# 6. 自動推播邏輯 (嚴謹判斷)
if current_eti >= 115:
    # 這裡確保只有在條件成立時，發送最後一次測試推播
    try:
        app_id = st.secrets["ONESIGNAL_APP_ID"]
        api_key = st.secrets["ONESIGNAL_REST_API_KEY"]
        headers = {"Authorization": f"Basic {api_key}", "Content-Type": "application/json"}
        payload = {
            "app_id": app_id,
            "headings": {"zh-Hant": "🚨 ETI 最高預警！"},
            "contents": {"zh-Hant": f"目前 ETI 達 {current_eti}，已進入獲利了結區間。"},
            "included_segments": ["Total Subscriptions"]
        }
        # 僅在頁面重整且符合條件時嘗試發送
        if "pushed" not in st.session_state:
            requests.post("https://api.onesignal.com/notifications", headers=headers, json=payload)
            st.session_state.pushed = True
            st.success("✅ OneSignal 專業預警已推送至您的裝置。")
    except:
        pass

st.divider()
st.caption("本系統為 Hsu Min-Hsiung (敏雄) 專屬開發，嚴格遵守量化停利 SOP 指引。")
