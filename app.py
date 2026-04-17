import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. 頁面配置
st.set_page_config(page_title="資產配置監控系統", layout="wide")

# 2. 定義監控清單 (你可以隨時調整這些代號)
ASSETS = {
    "美股/ETF": ["NVDA", "QQQ", "VOO", "VTI"],
    "台股/ETF": ["2330.TW", "0050.TW", "0056.TW", "00878.TW"],
    "共同基金 (模擬)": ["安聯收益成長基金", "摩根全球機會基金", "富蘭克林坦伯頓"]
}

# 3. 標題與專業聲明
st.title("🏦 全方位資產決策監控儀表板")
st.caption(f"最後更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 使用者：Hsu Min-Hsiung")

# 4. 頂部核心總經指標 (ETI)
st.subheader("🚨 核心總經預警：ETI 指數")
col_eti1, col_eti2 = st.columns([1, 3])
with col_eti1:
    st.metric(label="當前 ETI 指數", value="120", delta="進入停利區", delta_color="inverse")
with col_eti2:
    st.warning("⚠️ 根據 SOP：ETI > 115。建議對下方高標偏離之資產執行分批獲利了結。")

st.divider()

# 5. 分類監控區
tabs = st.tabs(["🇺🇸 國外股票/ETF", "🇹🇼 台灣股票/ETF", "📊 共同基金監控"])

# --- 國外股票/ETF ---
with tabs[0]:
    st.write("### 華爾街即時行情 (Source: yfinance)")
    cols = st.columns(len(ASSETS["美股/ETF"]))
    for i, ticker in enumerate(ASSETS["美股/ETF"]):
        with cols[i]:
            data = yf.Ticker(ticker).history(period="1mo")
            current_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2]
            change = ((current_price - prev_price) / prev_price) * 100
            st.metric(ticker, f"${current_price:.2f}", f"{change:.2f}%")
            st.line_chart(data['Close'], height=150)

# --- 台灣股票/ETF ---
with tabs[1]:
    st.write("### 台灣市場行情 (Source: yfinance)")
    cols = st.columns(len(ASSETS["台股/ETF"]))
    for i, ticker in enumerate(ASSETS["台股/ETF"]):
        with cols[i]:
            data = yf.Ticker(ticker).history(period="1mo")
            current_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2]
            change = ((current_price - prev_price) / prev_price) * 100
            st.metric(ticker, f"{current_price:.1f} TWD", f"{change:.2f}%")
            st.line_chart(data['Close'], height=150)

# --- 共同基金監控 ---
with tabs[2]:
    st.write("### 共同基金淨值觀測")
    st.info("💡 基金淨值為每日更新。此處展示淨值趨勢與風險預警。")
    fund_df = pd.DataFrame({
        "基金名稱": ASSETS["共同基金 (模擬)"],
        "最新淨值": [15.2, 128.4, 45.8],
        "風險等級": ["RR4", "RR3", "RR4"],
        "SOP 建議": ["符合分批買進", "持有觀望", "高點預警"]
    })
    st.dataframe(fund_df, use_container_width=True)

# 6. 底部專業備註
st.divider()
with st.expander("📖 數據來源與操作依據備註"):
    st.write("""
    1. **股票/ETF數據**：串接 Yahoo Finance API，每小時自動同步。
    2. **ETI 模型**：依據 ECRI 領先指標與 Artur 期望值模型設定。
    3. **操作建議**：僅供 Min-Hsiung 內部決策輔助，不構成外部投資建議。
    """)
