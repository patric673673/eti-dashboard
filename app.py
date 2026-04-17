import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="專業自定義資產監控系統", layout="wide")

# --- 側邊欄：動態自定義輸入區 ---
st.sidebar.header("⚙️ 資產清單自定義")
st.sidebar.info("請輸入 Yahoo Finance 代號 (多筆請用逗號隔開)")

# 1. 國外資產設定
us_stocks_input = st.sidebar.text_input("國外股票 (例如: NVDA, AAPL, MSFT)", "NVDA, AAPL")
us_etfs_input = st.sidebar.text_input("國外 ETF (例如: QQQ, VOO, ARKK)", "QQQ, VOO")

# 2. 台灣資產設定
tw_stocks_input = st.sidebar.text_input("台灣股票 (例如: 2330.TW, 2454.TW)", "2330.TW, 2454.TW")
tw_etfs_input = st.sidebar.text_input("台灣指數型 ETF (例如: 0050.TW, 006208.TW)", "0050.TW, 006208.TW")

# 3. 共同基金設定
intl_funds_input = st.sidebar.text_input("海外共同基金 (例如: AZALX, JPMGX)", "AZALX, JPMGX")
tw_funds_input = st.sidebar.text_input("國內共同基金 (例如: 0056.TW, 00878.TW)", "0056.TW, 00878.TW")

# 4. 時間區間控制
time_range = st.sidebar.selectbox(
    "觀察區間", ["1d", "5d", "1mo", "6mo", "1y", "5y", "max"], index=2,
    format_func=lambda x: {"1d":"1天", "5d":"5天", "1mo":"1個月", "6mo":"6個月", "1y":"1年", "5y":"5年", "max":"歷史最久"}[x]
)

# --- 繪圖工具函數 ---
def draw_pro_chart(ticker, color="#1f77b4"):
    try:
        data = yf.Ticker(ticker.strip()).history(period=time_range)
        if data.empty:
            st.warning(f"找不到代號: {ticker}")
            return
        
        prices = data['Close']
        current_p = prices.iloc[-1]
        prev_p = prices.iloc[0]
        change = ((current_p - prev_p) / prev_p) * 100
        
        st.metric(ticker.strip(), f"{current_p:.2f}", f"{change:.2f}%")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=prices, mode='lines', fill='tozeroy', line=dict(color=color, width=2)))
        fig.update_layout(
            height=200, margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(autorange=True, fixedrange=False, showgrid=True, side="right"),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error(f"讀取 {ticker} 出錯")

# --- 主畫面顯示 ---
st.title("📈 全方位自定義資產決策儀表板")
st.caption(f"指標規範：動態數據抓取 | 觀察區間：{time_range}")

# 核心 ETI 指標 (維持模擬以確保預警邏輯)
st.subheader("🚨 總經預警：ETI 指數")
st.metric("當前 ETI", "120", delta="過熱預警", delta_color="inverse")
st.divider()

# 分類呈現區
tabs = st.tabs(["🇺🇸 國外股票/ETF", "🇹🇼 台灣市場", "📊 國內外共同基金"])

with tabs[0]:
    st.write("### 國外股票")
    tickers = us_stocks_input.split(",")
    cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        with cols[i]: draw_pro_chart(t, "#1f77b4")
    
    st.write("### 國外 ETF")
    tickers_etf = us_etfs_input.split(",")
    cols_etf = st.columns(len(tickers_etf))
    for i, t in enumerate(tickers_etf):
        with cols_etf[i]: draw_pro_chart(t, "#17becf")

with tabs[1]:
    st.write("### 台灣一般股票")
    tickers_tw = tw_stocks_input.split(",")
    cols_tw = st.columns(len(tickers_tw))
    for i, t in enumerate(tickers_tw):
        with cols_tw[i]: draw_pro_chart(t, "#2ca02c")

    st.write("### 台灣指數型基金 (ETF)")
    tickers_tw_etf = tw_etfs_input.split(",")
    cols_tw_etf = st.columns(len(tickers_tw_etf))
    for i, t in enumerate(tickers_tw_etf):
        with cols_tw_etf[i]: draw_pro_chart(t, "#bcbd22")

with tabs[2]:
    st.write("### 海外共同基金淨值觀測")
    tickers_int_f = intl_funds_input.split(",")
    cols_int_f = st.columns(len(tickers_int_f))
    for i, t in enumerate(tickers_int_f):
        with cols_int_f[i]: draw_pro_chart(t, "#9467bd")

    st.write("### 國內共同基金淨值觀測")
    tickers_tw_f = tw_funds_input.split(",")
    cols_tw_f = st.columns(len(tickers_tw_f))
    for i, t in enumerate(tickers_tw_f):
        with cols_tw_f[i]: draw_pro_chart(t, "#e377c2")
