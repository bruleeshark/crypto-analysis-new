import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import WeekdayLocator, DateFormatter
import mplfinance as mpf

def get_crypto_data(crypto_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    data = response.json()
    return data

def plot_price_and_volume_chart(data, crypto_id):
    # Prepare the data
    df = pd.DataFrame(data['prices'], columns=['Date', 'Price'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True)
    
    # Add volume data
    volume_df = pd.DataFrame(data['total_volumes'], columns=['Date', 'Volume'])
    volume_df['Date'] = pd.to_datetime(volume_df['Date'], unit='ms')
    volume_df.set_index('Date', inplace=True)
    df['Volume'] = volume_df['Volume']
    
    # Add necessary OHLC data (Open, High, Low, Close)
    df['Open'] = df['Price']
    df['High'] = df['Price']
    df['Low'] = df['Price']
    df['Close'] = df['Price']
    
    # Create the plot
    fig, axes = mpf.plot(df, type='line', volume=True, figsize=(12, 8),
                         style='yahoo', title=f'\n{crypto_id.capitalize()} Price and Volume Over Time',
                         ylabel='Price (USD)',
                         ylabel_lower='Volume',
                         returnfig=True)
    
    ax_main = axes[0]
    ax_volume = axes[2]
    
    # Add grid lines at one-week intervals
    ax_main.xaxis.set_major_locator(WeekdayLocator(byweekday=0, interval=1))  # Every Monday
    ax_main.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax_main.grid(True, which='major', axis='x', linestyle='--', alpha=0.7)
    
    # Rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    
    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig(f"{crypto_id}_price_volume_chart.png")
    plt.close()

if __name__ == "__main__":
    crypto_id = "ethereum"
    days = 30
    
    data = get_crypto_data(crypto_id, days)
    plot_price_and_volume_chart(data, crypto_id)
    print(f"Chart saved as {crypto_id}_price_volume_chart.png in the current directory.")