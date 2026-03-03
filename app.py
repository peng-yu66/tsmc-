import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TSMC 金庫", page_icon="💰")
st.title("💰 我的台積電金庫")

@st.cache_data(ttl=300)
def get_finance_data():
    # 抓取台股、ADR、匯率
    # 增加抓取天數到 10 天，確保能抓到上一個交易日的收盤價
    tickers = ["TSM", "2330.TW", "TWD=X"]
    df = yf.download(tickers, period="10d", progress=False)['Close']
    
    # 用最後一行有效數據填補空值
    last_data = df.ffill().iloc[-1]
    return last_data

try:
    data = get_finance_data()
    tsmc_tw = data['2330.TW']
    tsmc_adr = data['TSM']
    rate = data['TWD=X']
    
    # 計算 ADR 換算台幣價 (1股 ADR = 5股台股)
    adr_converted = (tsmc_adr / 5) * rate
    premium = ((adr_converted - tsmc_tw) / tsmc_tw) * 100

    # 介面顯示
    st.metric("台積電現價 (2330)", f"{tsmc_tw:.0f} 元", "成本 1985")
    
    # 增加顏色顯示：溢價過高提醒
    if premium > 15:
        st.warning(f"🚩 目前溢價率：{premium:.2f}% (溢價偏高，請留意風險)")
    else:
        st.success(f"✅ 目前溢價率：{premium:.2f}%")
        
    st.info(f"💡 ADR 折合台幣合理價：**{adr_converted:.2f}** 元")
    st.caption(f"匯率參考：{rate:.2f} | 數據每 5 分鐘自動更新")

except Exception as e:
    st.error("數據連接中，請稍後刷新頁面...")
