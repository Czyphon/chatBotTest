import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

def get_stock_data(ticker, timeframe):
    stock = yf.Ticker(ticker)
    data = stock.history(period=timeframe)
    return data

def create_candlestick_chart(data, ticker):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    fig.update_layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price')
    return fig

def display_stock_info(data, selected_point):
    date = data.index[selected_point]
    info = data.iloc[selected_point]
    st.write(f"Date: {date.strftime('%Y-%m-%d')}")
    st.write(f"Open: ${info['Open']:.2f}")
    st.write(f"High: ${info['High']:.2f}")
    st.write(f"Low: ${info['Low']:.2f}")
    st.write(f"Close: ${info['Close']:.2f}")
    st.write(f"Volume: {info['Volume']:,}")
    # Add more info or sentiment analysis here

st.title("Stock Chart Explorer")

ticker = st.text_input("Enter stock ticker:", value="AAPL").upper()
timeframe = st.selectbox("Select timeframe:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"])

if ticker:
    data = get_stock_data(ticker, timeframe)
    fig = create_candlestick_chart(data, ticker)
    
    selected_point = st.plotly_chart(fig, use_container_width=True, key="chart")
    
    if selected_point and selected_point.get("points"):
        point_index = selected_point["points"][0]["pointIndex"]
        with st.expander("Stock Information", expanded=True):
            display_stock_info(data, point_index)
