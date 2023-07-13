import requests
import pandas as pd
import os

def get_price_history(token_id, days, vs_currency='usd'):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart"
    params = {
        'vs_currency': vs_currency,
        'days': days,
    }
    result = requests.get(url, params=params)
    result.raise_for_status()

    data = result.json()

    # Convert timestamps to datetime and prices to a list to resolve float typeError
    times = [x[0] for x in data['prices']]
    prices = [x[1] for x in data['prices']]
    market_caps = [x[1] for x in data['market_caps']]
    total_volumes = [x[1] for x in data['total_volumes']]

    # Create DataFrame
    df = pd.DataFrame({'time': pd.to_datetime(times, unit='ms'), 'price': prices, 'market_cap':market_caps, 'total_volume': total_volumes})

    # Calculate moving average
    N = 5
    df['price_ma'] = df['price'].rolling(window=N).mean()

    df['price_change'] = df['price'].diff().round(5)
    df['price_change'] = df['price_change'].apply('{:.5f}'.format)

    df.set_index('time', inplace=True, drop=False)

    return df

# request token id from user
token_id = input("Enter desired token ID: ")
days = int(input("Enter range of sample in days: "))


# replace 'bitcoin' with your token_id
df = get_price_history(token_id, days)
df.to_csv('price_history.csv')

os.system('py candlestick.py')