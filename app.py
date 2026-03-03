import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TSMC 金庫", page_icon="💰")
st.title("💰 我的台積電金庫")

@st.cache_data(ttl=600)
def get_finance_data():
    # 同時抓取 ADR(TSM)、台股(2330.TW)、匯率(TWD=X)
    tickers = ["TSM", "2330.TW", "TWD=X"]
    # 抓取 5 天數據確保即便美股休市也能拿到最近一天的收盤價
    df = yf.download(tickers, period="5d")['Close']
    return df.iloc[-1].ffill() 

try:
    data = get_finance_data()
    tsmc_tw = data['2330.TW']
    tsmc_adr = data['TSM']
    rate = data['TWD=X']
    
    # 計算 ADR 換算台幣價與溢價
    adr_converted = (tsmc_adr / 5) * rate
    premium = ((adr_converted - tsmc_tw) / tsmc_tw) * 100

    # 顯示數據
    st.metric("台積電現價 (2330)", f"{tsmc_tw:.0f} 元", "成本 1985")
    
    # 判斷溢價是否有效
    if str(premium) != 'nan':
        st.metric("ADR 溢價率", f"{premium:.2f}%")
        st.info(f"💡 ADR 折合台幣價：**{adr_converted:.2f}** 元")
    else:
        st.warning("⚠️ 目前美股休市中，請參考昨日數據")

    st.write(f"匯率參考：{rate:.2f}")

except Exception as e:
    st.error("數據更新中，請稍候重新整理網頁...")
