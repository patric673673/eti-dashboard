import streamlit as st

# 1. 基礎設定
st.set_page_config(
    page_title="ETI 市場微調關預警系統",
    page_icon="📈",
    layout="wide"
)

# 2. 側邊欄隱藏多餘內容
st.markdown("""
    <style>
        .reportview-container { margin-top: -2em; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. 主頁面內容
st.title("🚀 ETI 市場預警系統 - 即時推送通知")
st.write(f"歡迎回來，**敏雄**！這是您的個人化金融決策儀表板。")

st.info("💡 請從左側選單選擇 **「01_儀表板」** 查看最新市場數據分析。")

# 4. 建立一些快速指標
col1, col2, col3 = st.columns(3)
col1.metric("市場情緒", "穩定", "Normal")
col2.metric("推播狀態", "已連線", "Active")
col3.metric("系統版本", "v1.0.0", "Stable")
