import streamlit as st
import yfinance as yf

st.title("💰 我的台積電金庫")
data = yf.download(["TSM", "2330.TW", "TWD=X"], period="5d")['Close'].iloc[-1]

tw_price = data['2330.TW']
adr_now = (data['TSM'] / 5) * data['TWD=X']
premium = ((adr_now - tw_price) / tw_price) * 100

st.metric("台積電現價", f"{tw_price:.0f} 元", "成本 1985")
st.metric("ADR 溢價率", f"{premium:.2f}%")
