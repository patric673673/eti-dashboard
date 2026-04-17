import streamlit as st
import pandas as pd
import numpy as np

# 確保這行在最上面
st.set_page_config(page_title="數據儀表板", layout="wide")

st.header("📊 ETI 核心數據分析")
st.markdown("---")

# 建立模擬數據
data = pd.DataFrame({
    '日期': pd.date_range(start='2024-01-01', periods=10),
    'ETI指數': [102, 105, 103, 110, 108, 115, 112, 118, 120, 125]
})

# 顯示指標
col1, col2 = st.columns(2)
with col1:
    st.metric("當前 ETI", "125", "+5.2%")
with col2:
    st.write("### 趨勢說明")
    st.write("目前市場動能強勁，各項指標顯示穩定成長中。")

# 畫出圖表
st.line_chart(data.set_index('日期'))

st.success("✅ 數據加載完畢")
