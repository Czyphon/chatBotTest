import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Function to fetch stock data
def get_stock_data(symbol, period="1mo"):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data

# Function to create candlestick chart
def create_candlestick_chart(data, name):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    fig.update_layout(title=f'{name} Stock Price',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_rangeslider_visible=False)
    return fig

# Function to display educational content
def display_education(date, open_price, high, low, close):
    st.subheader("Candlestick Analysis")
    st.write(f"Date: {date.strftime('%Y-%m-%d')}")
    st.write(f"Open: ${open_price:.4f}")
    st.write(f"High: ${high:.4f}")
    st.write(f"Low: ${low:.4f}")
    st.write(f"Close: ${close:.4f}")
    
    body = close - open_price
    if body >= 0:
        candle_type = "Bullish (Green) Candle"
        interpretation = "The stock price increased during this trading day. This might indicate buying pressure."
    else:
        candle_type = "Bearish (Red) Candle"
        interpretation = "The stock price decreased during this trading day. This might indicate selling pressure."
    
    st.write(f"Candle Type: {candle_type}")
    st.write(f"Interpretation: {interpretation}")
    
    wick_up = high - max(open_price, close)
    wick_down = min(open_price, close) - low
    st.write(f"Upper Wick: ${wick_up:.4f}")
    st.write(f"Lower Wick: ${wick_down:.4f}")
    st.write("The wicks (shadows) represent the price extremes for the day. Long wicks might indicate indecision or reversal.")
    
    st.write("Remember: A single candlestick provides limited information. Always consider the broader context and use multiple indicators for investment decisions.")

# Main Streamlit app
st.title("Interactive AAPL Stock Candlestick Chart")
st.write("Click on any candle to learn more about candlestick analysis!")

# Fetch AAPL stock data
data = get_stock_data("AAPL")
data2 = get_stock_data("NVDA")
data3 = get_stock_data("MSFT")

# Create candlestick chart
fig = create_candlestick_chart(data, "AAPL")
fig2 = create_candlestick_chart(data2, "NVDA")
fig3 = create_candlestick_chart(data3, "MSFT")

# Use Streamlit's plotly_chart with click event handling
selected_points = st.plotly_chart(fig, use_container_width=True, key="candlestick_chart")
second_chart = st.plotly_chart(fig2, use_container_width=True, key="candlestick_chart")
third_chart = st.plotly_chart(fig3, use_container_width=True, key="candlestick_chart")

# Check if a candle was clicked
if selected_points:
    point = selected_points["points"][0]
    date = datetime.utcfromtimestamp(point["x"] / 1000)
    open_price, high, low, close = point["open"], point["high"], point["low"], point["close"]
    display_education(date, open_price, high, low, close)
else:
    st.write("Click on a candle to see detailed information and learn about candlestick analysis.")

st.sidebar.header("About This Tool")
st.sidebar.write("This interactive chart helps beginner investors learn about candlestick analysis using AAPL stock data. Click on any candle to get detailed information and educational content.")
st.sidebar.write("Data provided by Yahoo Finance via yfinance.")
