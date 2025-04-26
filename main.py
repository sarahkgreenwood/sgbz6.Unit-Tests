'''
This code is directly taken and modified with all credientials to Michael McClanahan and Sarah Greenwood of 4320 Team 15.
It was posted to Github at: https://github.com/sarahkgreenwood/Team15.3/blob/main/main.py
'''

from datetime import datetime
from input_handler import get_stock_symbol, get_chart_type, get_time_series
from visualizer import fetch_stock_data, plot_stock_chart

def date_check(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])

    if not (2005 <= year <= 2025):
        print("No data available.")
        return False

    if month not in range(1, 13):
        print("Month is invalid.")
        return False

    if month in [1, 3, 5, 7, 8, 10, 12]:
        if day > 31:
            print("Day is invalid.")
            return False
    elif month in [4, 6, 9, 11]:
        if day > 30:
            print("Day is invalid.")
            return False
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            if day > 29:
                print("Day is invalid.")
                return False
        else:
            if day > 28:
                print("Day is invalid.")
                return False
    return True

def calculate_days(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return f"{abs((end - start).days)}day"
    except ValueError:
        print("Invalid date format. Please enter YYYY-MM-DD.")
        return None

def calculate_weeks(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        weeks = abs((end - start).days / 7)
        return f"{weeks:.2f}week"
    except ValueError:
        print("Invalid date format. Please enter YYYY-MM-DD.")
        return None

def calculate_months(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        months = (end.year - start.year) * 12 + (end.month - start.month)
        return f"{abs(months)}month"
    except ValueError:
        print("Invalid date format. Please enter YYYY-MM-DD.")
        return None

def build_alphavantage_url(symbols, time_series, interval, apikey):
    base_url = "https://www.alphavantage.co/query?"

    if time_series == "1":
        function_name = "TIME_SERIES_INTRADAY"
    elif time_series == "2":
        function_name = "TIME_SERIES_DAILY"
    elif time_series == "3":
        function_name = "TIME_SERIES_WEEKLY"
    else:
        function_name = "TIME_SERIES_MONTHLY"

    params = {
        "function": function_name,
        "symbol": symbols,
        "apikey": apikey
    }

    if function_name in ["TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"]:
        params["outputsize"] = "full"

    if function_name == "TIME_SERIES_INTRADAY" and interval:
        params["interval"] = interval

    url_parts = [f"{key}={value}" for key, value in params.items()]
    return base_url + "&".join(url_parts)

def get_user_input_and_build_url():
    stock_symbol = get_stock_symbol()
    chart_type = get_chart_type()
    time_series = get_time_series()

    interval = None

    if time_series == "1":
        # Retry until valid date is entered
        while True:
            start_date = input("Please enter the day (YYYY-MM-DD): ")
            if date_check(start_date):
                break
            print("Please enter a valid date.")
        interval = "60min"
        end_date = None
    else:
        # Retry until valid start date
        while True:
            start_date = input("Please enter the start date (YYYY-MM-DD): ")
            if date_check(start_date):
                break
            print("Invalid start date. Please try again.")

        # Retry until valid end date
        while True:
            end_date = input("Please enter the end date (YYYY-MM-DD): ")
            if date_check(end_date):
                break
            print("Invalid end date. Please try again.")

        # Ensure end date is not before start date
        while end_date < start_date:
            print("Error: End date cannot be before start date.")
            end_date = input("Please enter the end date (YYYY-MM-DD): ")

        # Display duration info
        if time_series == "2":
            print(calculate_days(start_date, end_date))
        elif time_series == "3":
            print(calculate_weeks(start_date, end_date))
        else:
            print(calculate_months(start_date, end_date))

    url = build_alphavantage_url(stock_symbol, time_series, interval, "19Z62OVAZ1XYL8JR")
    print(f"Generated API URL: {url}")

    data = fetch_stock_data(url)
    plot_stock_chart(data, chart_type, stock_symbol)

def main():
    get_user_input_and_build_url()
    while True:
        again = input("Would you like to view more stock data? Press 'y' to continue: ").lower()
        if again != "y":
            print("Goodbye!")
            break
        get_user_input_and_build_url()

if __name__ == "__main__":
    main()