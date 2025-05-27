import yfinance as yf
import plotly.graph_objects as go

# 글로벌 시총 상위 10개 기업 (2024년 기준, 시총 순위는 약간 변동 가능)
top_10_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Nvidia": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Eli Lilly": "LLY"
}

# 주가 데이터 다운로드 (최근 6개월)
data = yf.download(list(top_10_tickers.values()), period="6mo")["Adj Close"]

# Plotly 그래프 생성
fig = go.Figure()

for company, ticker in top_10_tickers.items():
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[ticker],
        mode='lines',
        name=company
    ))

# 그래프 레이아웃 설정
fig.update_layout(
    title="글로벌 시가총액 상위 10개 기업 주가 (최근 6개월)",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    template="plotly_dark",
    hovermode="x unified"
)

fig.show()
