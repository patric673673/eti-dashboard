import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. 頁面基礎規範設定
st.set_page_config(page_title="專業資產配置監控系統", layout="wide")

# 2. 側邊欄：時間區間控制 (影響所有座標軸)
st.sidebar.header("📊 全球市場規範設定")
time_range = st.sidebar.selectbox(
    "選擇觀察區間",
    ["1d", "5d", "1mo", "6mo", "1y", "5y", "max"],
    index=2,
    format_func=lambda x: {"1d":"1天", "5d":"5天", "1mo":"1個月", "6mo":"6個月", "1y":"1年", "5y":"5年", "max":"歷史最久"}[x]
)

# 3. 資產清單設定
ASSETS = {
    "美股/ETF": ["NVDA", "QQQ", "VOO"],
    "台股/ETF": ["2330.TW", "0050.TW", "0056.TW"],
    "共同基金": ["安聯收益成長", "摩根全球機會", "富蘭克林"]
}

# 繪圖函數：專門處理「緊縮座標軸」與「專業比例」
def draw_professional_chart(ticker, data, color="#1f77b4"):
    if data.empty:
        st.warning(f"無法取得 {ticker} 數據")
        return

    prices = data['Close']
    fig = go.Figure()
    
    # 畫出走勢線
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=prices, 
        mode='lines', 
        fill='tozeroy', 
        line=dict(color=color, width=2),
        name=ticker
    ))

    # 專業座標軸設定：不從 0 開始，鎖定波動區間
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, tickformat='%m/%d'),
        yaxis=dict(
            autorange=True, 
            fixedrange=False, 
            showgrid=True, 
            gridcolor='rgba(200, 200, 200, 0.2)',
            side="right" # 座標軸放在右邊，符合交易軟體習慣
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# 4. 主畫面呈現
st.title("🏦 全方位資產決策儀表板")
st.caption(f"指標規範：依據 ECRI 與 Artur SOP 建立 | 當前時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- ETI 核心預警區 ---
st.subheader("🚨 核心總經指標：ETI 指數")
col_e1, col_e2 = st.columns([1, 4])
with col_e1:
    st.metric("當前 ETI 指數", "120", delta="最高警戒區", delta_color="inverse")
with col_e2:
    # 模擬 ETI 趨勢圖 (固定區間)
    eti_mock = pd.DataFrame({
        'Close': [105, 108, 112, 115, 118, 120, 119, 120]
    }, index=pd.date_range(end=datetime.now(), periods=8, freq='D'))
    draw_professional_chart("ETI 指標", eti_mock, color="#d62728")

st.divider()

# --- 分類監控區 ---
tabs = st.tabs(["🇺🇸 國外股票/ETF", "🇹🇼 台灣股票/ETF", "📊 共同基金走勢"])

with tabs[0]:
    st.write(f"### 華爾街即時監控 ({time_range})")
    cols = st.columns(len(ASSETS["美股/ETF"]))
    for i, ticker in enumerate(ASSETS["美股/ETF"]):
        data = yf.Ticker(ticker).history(period=time_range)
        with cols[i]:
            if not data.empty:
                current_p = data['Close'].iloc[-1]
                st.metric(ticker, f"${current_p:.2f}")
                draw_professional_chart(ticker, data)

with tabs[1]:
    st.write(f"### 台灣市場監控 ({time_range})")
    cols = st.columns(len(ASSETS["台股/ETF"]))
    for i, ticker in enumerate(ASSETS["台股/ETF"]):
        data = yf.Ticker(ticker).history(period=time_range)
        with cols[i]:
            if not data.empty:
                current_p = data['Close'].iloc[-1]
                st.metric(ticker, f"{current_p:.1f} TWD")
                draw_professional_chart(ticker, data, color="#2ca02c")

with tabs[2]:
    st.write(f"### 共同基金淨值觀測 ({time_range})")
    st.info("基金走勢依據每日淨值計算，旨在觀察長期複利斜率。")
    fund_cols = st.columns(3)
    # 為基金建立模擬但規範的淨值圖
    periods_map = {"1d": 24, "5d": 5, "1mo": 30, "6mo": 180, "1y": 365, "5y": 1825, "max": 2500}
    num_days = periods_map[time_range]
    for i, name in enumerate(ASSETS["共同基金"]):
        with fund_cols[i]:
            mock_nav = pd.DataFrame({
                'Close': [15 + (x * 0.01) for x in range(num_days)]
            }, index=pd.date_range(end=datetime.now(), periods=num_days))
            st.metric(name, f"NAV {mock_nav['Close'].iloc[-1]:.2f}")
            draw_professional_chart(name, mock_nav, color="#9467bd")

# 5. 專業備註
st.divider()
with st.expander("📖 專業指標來源與操作規範"):
    st.markdown("""
    * **數據來源**：美股/台股由 Yahoo Finance API 提供；基金淨值由系統模擬淨值軌跡。
    * **指標定義**：ETI > 115 定義為「極端超買區」，結合 Gamma 指標與期望值理論。
    * **座標規範**：圖表採緊縮 Y 軸設計 (Autorange)，旨在放大波動視角，利於觀察趨勢拐點。
    """)
