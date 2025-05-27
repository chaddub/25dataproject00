import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 시가총액 상위 10개 기업 티커 및 이름
companies = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "2222.SR": "Saudi Aramco",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    "NVDA": "NVIDIA",
    "BRK-B": "Berkshire Hathaway",
    "META": "Meta",
    "TSLA": "Tesla",
    "TSM": "TSMC"
}

# 데이터 기간
start_date = "2024-01-01"
end_date = "2025-01-01"

# 주가 데이터 수집
price_data = {}
for ticker in companies:
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if not data.empty:
            price_data[ticker] = data['Adj Close']
        else:
            print(f"[경고] {ticker}의 데이터가 비어 있습니다.")
    except Exception as e:
        print(f"[에러] {ticker} 데이터 수집 실패: {e}")

# 수집된 데이터를 하나의 DataFrame으로 병합
df = pd.DataFrame(price_data)
df.dropna(axis=1, how='all', inplace=True)  # 모든 데이터가 결측인 경우 제거

# 시각화
fig = go.Figure()
for ticker in df.columns:
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[ticker],
        mode='lines',
        name=companies[ticker]
    ))

fig.update_layout(
    title="글로벌 시가총액 상위 10개 기업 주가 추이 (2024년)",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    legend_title="기업명",
    template="plotly_white",
    hovermode="x unified",
    width=1000,
    height=600
)

fig.show()
