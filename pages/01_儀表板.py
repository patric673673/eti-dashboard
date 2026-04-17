import streamlit as st
import pandas as pd
import numpy as np

# 1. 頁面配置
st.set_page_config(page_title="ETI 決策儀表板", layout="wide")

# 2. 標題
st.header("📈 ETI 核心趨勢與操作建議")
st.markdown("---")

# 💡 模擬當前數據（未來可改為自動抓取）
current_eti = 125 
prev_eti = 118
change_pct = round(((current_eti - prev_eti) / prev_eti) * 100, 1)

# 🚦 智能策略邏輯判斷
if current_eti >= 120:
    status_msg = "⚠️ 【建議獲利了結】"
    status_detail = "目前指數已進入過熱區（>120），建議分批賣出獲利，入袋為安，避免回檔風險。"
    status_type = "error" # 紅色提示
elif current_eti <= 80:
    status_msg = "✅ 【建議分批進場】"
    status_detail = "目前指數處於低估區（<80），市場恐慌正是佈局良機，建議開始分批買進。"
    status_type = "success" # 綠色提示
else:
    status_msg = "💡 【建議暫時觀望】"
    status_detail = "目前指數在 80-120 區間震盪，方向不明確。建議保留現金，靜待明確信號出現。"
    status_type = "info" # 藍色提示

# 3. 顯示視覺化看板
col1, col2 = st.columns([1, 2])

with col1:
    st.metric(label="當前 ETI 指數", value=current_eti, delta=f"{change_pct}%")

with col2:
    # 根據判斷結果顯示變色提示框
    if status_type == "error":
        st.error(f"### {status_msg}\n{status_detail}")
    elif status_type == "success":
        st.success(f"### {status_msg}\n{status_detail}")
    else:
        st.info(f"### {status_msg}\n{status_detail}")

# 4. 趨勢圖表
st.write("### 歷史走勢參考")
chart_data = pd.DataFrame({
    '日期': pd.date_range(start='2024-04-01', periods=10),
    'ETI 指數': [110, 112, 115, 113, 117, 119, 118, 122, 124, 125]
})
st.line_chart(chart_data.set_index('日期'))

# 5. 操作原則小筆記
with st.expander("📌 查看 ETI 操作原則"):
    st.write("""
    * **紅色警告**：指數 > 120。代表市場太樂觀，你要反向思考，準備獲利。
    * **綠色信心**：指數 < 80。代表市場太悲觀，你要勇敢進場。
    * **藍色觀望**：指數在中間。代表目前是常態，不需要頻繁操作。
    """)
