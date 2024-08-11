import requests
import pandas as pd
import mplfinance as mpf
from matplotlib.dates import WeekdayLocator, DateFormatter

def get_crypto_data(crypto_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    data = response.json()
    return data

def prepare_data(data):
    df = pd.DataFrame(data['prices'], columns=['Date', 'Close'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True)
    
    volume_df = pd.DataFrame(data['total_volumes'], columns=['Date', 'Volume'])
    volume_df['Date'] = pd.to_datetime(volume_df['Date'], unit='ms')
    volume_df.set_index('Date', inplace=True)
    df['Volume'] = volume_df['Volume']
    
    df['Open'] = df['Close'].shift(1)
    df['High'] = df['Close']
    df['Low'] = df['Close']
    
    df = df.dropna()
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    return df

def plot_candlestick_chart(df, crypto_id):
    mc = mpf.make_marketcolors(up='g', down='r', volume='b')
    s = mpf.make_mpf_style(marketcolors=mc)
    
    # Create a WeekdayLocator for Mondays
    week_locator = WeekdayLocator(byweekday=0, interval=1)
    
    # Create custom x-axis formatter
    date_formatter = DateFormatter('%Y-%m-%d')
    
    # Additional style for grid
    s.update({'xaxis': {'major_locator': week_locator,
                       'major_formatter': date_formatter},
             'xtick': {'rotation': 45, 'ha': 'right'},
             'grid': {'alpha': 0.5}})

    # Create the plot
    mpf.plot(df, type='candle', style=s, volume=True, 
             title=f'\n{crypto_id.capitalize()} Price and Volume Over Time',
             ylabel='Price (USD)',
             ylabel_lower='Volume',
             figratio=(12,8),
             figscale=1.1,
             axtitle='Date',
             savefig=f"{crypto_id}_candlestick_chart.png",
             show_nontrading=True,
             tight_layout=True)

if __name__ == "__main__":
    crypto_id = "ethereum"
    days = 30
    
    data = get_crypto_data(crypto_id, days)
    df = prepare_data(data)
    plot_candlestick_chart(df, crypto_id)
    print(f"Chart saved as {crypto_id}_candlestick_chart.png in the current directory.")