import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

def get_stock_data(ticker, timeframe, interval):
    stock = yf.Ticker(ticker)
    data = stock.history(period=timeframe, interval=interval)
    return data

def create_candlestick_chart(data, ticker):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    fig.update_layout(
        title=f'{ticker} Stock Price',
        xaxis_title='Date',
        yaxis_title='Price',
        dragmode='pan',
        hovermode='x unified'
    )
    return fig

def display_stock_info(data, selected_date):
    info = data.loc[selected_date]
    st.write(f"Date: {selected_date.strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Open: ${info['Open']:.2f}")
    st.write(f"High: ${info['High']:.2f}")
    st.write(f"Low: ${info['Low']:.2f}")
    st.write(f"Close: ${info['Close']:.2f}")
    st.write(f"Volume: {info['Volume']:,}")
    # Add more info or sentiment analysis here

st.title("Stock Chart Explorer")

ticker = st.text_input("Enter stock ticker:", value="AAPL").upper()

timeframe_options = {
    "1 Day": "1d", "5 Days": "5d", "1 Month": "1mo",
    "3 Months": "3mo", "6 Months": "6mo", "1 Year": "1y",
    "2 Years": "2y", "5 Years": "5y", "Max": "max"
}
timeframe = st.selectbox("Select timeframe:", list(timeframe_options.keys()))

interval_options = {
    "1 Minute": "1m", "5 Minutes": "5m", "15 Minutes": "15m",
    "30 Minutes": "30m", "60 Minutes": "60m", "90 Minutes": "90m",
    "1 Hour": "1h", "1 Day": "1d", "5 Days": "5d",
    "1 Week": "1wk", "1 Month": "1mo", "3 Months": "3mo"
}
interval = st.selectbox("Select interval:", list(interval_options.keys()))

if ticker:
    data = get_stock_data(ticker, timeframe_options[timeframe], interval_options[interval])
    fig = create_candlestick_chart(data, ticker)
    
    selected_point = st.plotly_chart(fig, use_container_width=True)
    
    if selected_point:
        selected_date = selected_point.get('x')
        if selected_date:
            with st.expander("Stock Information", expanded=True):
                display_stock_info(data, pd.Timestamp(selected_date))
