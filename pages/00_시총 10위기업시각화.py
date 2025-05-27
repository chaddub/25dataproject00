import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 상위 10개 기업의 티커 리스트
tickers = ["AAPL", "MSFT", "2222.SR", "GOOGL", "AMZN", "NVDA", "BRK-B", "META", "TSLA", "TSM"]

# 기간 설정
start_date = "2024-01-01"
end_date = "2025-01-01"

# 데이터 프레임 초기화
price_data = {}

# 야후 파이낸스에서 데이터 다운로드
for ticker in tickers:
    try:
        df = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
        price_data[ticker] = df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

# DataFrame으로 변환
df_prices = pd.DataFrame(price_data)

# 시각화
fig = go.Figure()
for ticker in df_prices.columns:
    fig.add_trace(go.Scatter(x=df_prices.index, y=df_prices[ticker], mode='lines', name=ticker))

fig.update_layout(
    title="글로벌 시가총액 상위 10개 기업의 주가 추이 (2024년)",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    legend_title="티커",
    template="plotly_dark"
)

fig.show()
