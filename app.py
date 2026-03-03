import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TSMC 金庫", page_icon="💰")
st.title("💰 我的台積電金庫")

@st.cache_data(ttl=300)
def get_finance_data():
    # 抓取台股、ADR、匯率 (抓10天確保穩定)
    tickers = ["TSM", "2330.TW", "TWD=X"]
    df = yf.download(tickers, period="10d", progress=False)['Close']
    return df.ffill().iloc[-1], df['2330.TW'].ffill()

try:
    last_data, tw_hist = get_finance_data()
    tsmc_tw = last_data['2330.TW']
    tsmc_adr = last_data['TSM']
    rate = last_data['TWD=X']
    
    # 計算今日漲跌 (跟昨日收盤比)
    yesterday_close = tw_hist.iloc[-2]
    daily_change = tsmc_tw - yesterday_close
    
    # 計算 ADR 溢價
    adr_converted = (tsmc_adr / 5) * rate
    premium = ((adr_converted - tsmc_tw) / tsmc_tw) * 100

    # --- 顯示介面 ---
    # 1. 顯示現價與今日漲跌 (方案 A)
    st.metric("台積電現價 (2330)", f"{tsmc_tw:.0f} 元", f"{daily_change:+.0f} 今日變動")

    # 2. 自動買進燈號 (存股邏輯)
    if premium < 8:
        st.success(f"🟢 燈號：適合加碼 (溢價僅 {premium:.2f}%)")
        st.info("💡 目前 ADR 溢價低，分批存股很划算！")
    elif 8 <= premium <= 15:
        st.info(f"🟡 燈號：正常存股區 (溢價 {premium:.2f}%)")
        st.write("目前價格合理，可按原計畫小量買進。")
    else:
        st.warning(f"🔴 燈號：建議稍候 (溢價 {premium:.2f}%)")
        st.write("目前 ADR 衝太快，建議等回檔再存。")

    st.divider()
    st.caption(f"ADR 折合台幣合理價：{adr_converted:.2f} 元")
    st.caption(f"即時匯率：{rate:.2f} | 數據每 5 分鐘自動更新")

except Exception as e:
    st.error("數據連線中，請稍後刷新網頁...")
