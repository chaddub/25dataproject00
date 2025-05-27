import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="도지코인 가격 변화", layout="wide")

st.title("🐶 도지코인(DOGE) 전체 가격 변화 시각화")

# CoinGecko API를 사용하여 도지코인 가격 데이터 가져오기
@st.cache_data
def load_doge_data():
    url = "https://api.coingecko.com/api/v3/coins/dogecoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "max",
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("date", inplace=True)
    df.drop("timestamp", axis=1, inplace=True)
    return df

with st.spinner("도지코인 가격 데이터를 불러오는 중..."):
    df = load_doge_data()

st.success("데이터 로딩 완료!")

# 가격 차트 시각화
st.subheader("📊 도지코인 가격 추이")
st.line_chart(df["price"])

# 가격 요약 정보
st.subheader("📌 주요 가격 정보")
col1, col2, col3 = st.columns(3)
col1.metric("최초 가격", f"${df['price'].iloc[0]:.4f}")
col2.metric("최고가", f"${df['price'].max():.4f}")
col3.metric("현재가", f"${df['price'].iloc[-1]:.4f}")

# 데이터 다운로드 옵션
st.download_button(
    label="📥 CSV로 데이터 다운로드",
    data=df.to_csv().encode("utf-8"),
    file_name="dogecoin_price_history.csv",
    mime="text/csv"
)
