'''
This code is directly taken and modified with all credientials to Michael McClanahan with aid of Sarah Greenwood of 4320 Team 15.
It was posted to Github at: https://github.com/sarahkgreenwood/Team15.3/blob/main/visualizer.py
'''
import requests
import plotly.express as px
import pandas as pd

def fetch_stock_data(url):
    try:
        response = requests.get(url)
        data = response.json()

        time_series_keys = [
            "Time Series (60min)",
            "Time Series (Daily)",
            "Weekly Time Series",
            "Monthly Time Series"
        ]

        for key in time_series_keys:
            if key in data:
                return data[key]

        print("Error: Time series data not found in response.")
        return None

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def plot_stock_chart(time_series_data, chart_type="Line", symbol="N/A"):
    if not time_series_data:
        print("No data to plot.")
        return

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(time_series_data, orient='index')
    df = df.sort_index()  # Ensure dates are in order
    df["date"] = df.index
    df["close"] = df["4. close"].astype(float)

    # Last 20 records for cleaner plot
    df = df.tail(20)

    fig = None
    if chart_type == "Bar":
        fig = px.bar(df, x="date", y="close", title=f"{symbol} - Last 20 Closing Prices")
    else:
        fig = px.line(df, x="date", y="close", title=f"{symbol} - Last 20 Closing Prices")

    fig.update_layout(xaxis_title="Date", yaxis_title="Closing Price", xaxis_tickangle=-45)
    fig.show()