import streamlit as st
import pandas as pd
import numpy as np

# 1. 頁面基礎設定
st.set_page_config(page_title="ETI 決策儀表板", layout="wide")

# ================== 您的通知函數 (保持原樣) ==================
def request_notification_permission():
    st.markdown("""
    <script>
    function requestPushPermission() {
        if (!("Notification" in window)) {
            alert("您的瀏覽器不支援通知");
            return;
        }
        if (Notification.permission === "granted") {
            alert("通知權限已開啟！");
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    new Notification("✅ ETI 通知已啟用", {
                        body: "當 ETI 達到關鍵數值時，您將收到即時提醒。",
                        icon: "https://cdn-icons-png.flaticon.com/512/1055/1055644.png"
                    });
                }
            });
        }
    }
    </script>
    """, unsafe_allow_html=True)
    
    if st.button("🔔 開啟行動端通知權限", use_container_width=True):
        st.markdown('<script>requestPushPermission();</script>', unsafe_allow_html=True)

def send_browser_notification(title, body, tag="eti_alert"):
    st.markdown(f"""
    <script>
    if (Notification.permission === "granted") {{
        new Notification("{title}", {{
            body: "{body}",
            icon: "https://cdn-icons-png.flaticon.com/512/1055/1055644.png",
            tag: "{tag}",
            requireInteraction: true
        }});
    }}
    </script>
    """, unsafe_allow_html=True)

# ================== 主程式邏輯 ==================

st.header("📊 ETI 核心趨勢與即時預警")

# 這裡設定當前 ETI (您可以手動改這個數字測試效果)
eti_total = 120 

# 顯示權限按鈕
request_notification_permission()
st.markdown("---")

# 🚦 您的操作原則邏輯 (最高 120)
if eti_total >= 115:
    status_msg = "🚨 【最高警戒：獲利了結】"
    status_detail = f"目前 ETI 已達 {eti_total}。進入最高壓力區，建議執行獲利了結。"
    status_type = "error"
    # 自動發送通知
    send_browser_notification("🚨 ETI 最高預警！", f"目前 ETI {eti_total} 達最高標，建議立即評估獲利了結。", "eti_high")
    
elif eti_total <= 85:
    status_msg = "✅ 【建議分批進場】"
    status_detail = "目前指數處於低位，市場恐慌正是佈局良機。"
    status_type = "success"
    send_browser_notification("✅ ETI 低位訊號", "目前處於相對低點，適合分批佈局。", "eti_low")
    
else:
    status_msg = "💡 【暫時觀望】"
    status_detail = "目前處於震盪區間，建議保留現金，靜待信號。"
    status_type = "info"

# 顯示看板
col1, col2 = st.columns([1, 2])
with col1:
    st.metric(label="當前 ETI 總分", value=eti_total, delta="最高點")

with col2:
    if status_type == "error":
        st.error(f"### {status_msg}\n{status_detail}")
    elif status_type == "success":
        st.success(f"### {status_msg}\n{status_detail}")
    else:
        st.info(f"### {status_msg}\n{status_detail}")

# 趨勢圖表
st.write("### 歷史趨勢圖")
chart_data = pd.DataFrame(np.random.randn(20, 1) + (eti_total/100), columns=['ETI 指數'])
st.line_chart(chart_data)

# 紀錄狀態防止重複通知
st.session_state.last_eti = eti_total
