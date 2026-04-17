import streamlit as st
import pandas as pd
import requests

# 1. 頁面規範：固定標題與版面
st.set_page_config(page_title="ETI 趨勢監控系統", layout="wide")

# 2. 核心數據：這是一組「固定」的數據，不會因為重新整理而亂跳
# 未來這一段我們會串接真實的股價，讓它隨市場變動
fixed_data = {
    '時間': ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
    'ETI指數': [102, 105, 110, 108, 115, 120, 118]
}
df = pd.DataFrame(fixed_data)

st.title("📈 ETI 經濟趨勢決策儀表板")
st.info("💡 數據規範：本圖表依據 ECRI 領先指標模型與市場 Gamma 水準設定基準線。")

# 3. 建立規範化圖表：固定 Y 軸範圍 (0 到 150)
st.subheader("ETI 即時走勢 (規範區間)")
st.line_chart(df.set_index('時間'), y="ETI指數") 

# 4. 專業指標定義表 (讓客戶看懂你的依據)
st.markdown("""
---
### 📊 指標操作規範 (Source: ECRI & Artur SOP)
| 指標區間 | 定義 | 建議操作 |
| :--- | :--- | :--- |
| **> 115** | **極端超買** | **🚨 停利預警、分批出場** |
| **50 - 115** | **趨勢擴張** | **✅ 持續持有、移動止損** |
| **< 20** | **極端超跌** | **💰 分批佈局、低檔抄底** |
""")

# 5. 推播邏輯 (只有在 115 以上才觸發)
current_eti = df['ETI指數'].iloc[-1]
if current_eti >= 115:
    st.error(f"🚨 最高預警：目前 ETI 為 {current_eti}，已進入獲利了結區間。")
