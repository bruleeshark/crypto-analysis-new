import requests
import pandas as pd
import mplfinance as mpf
from matplotlib.dates import WeekdayLocator, DateFormatter
import matplotlib.pyplot as plt

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
    # Set up the style
    mc = mpf.make_marketcolors(up='g', down='r', volume='b')
    s = mpf.make_mpf_style(marketcolors=mc, rc={'font.size': 8})

    # Create a WeekdayLocator for Mondays
    week_locator = WeekdayLocator(byweekday=0, interval=1)
    
    # Create custom x-axis formatter
    date_formatter = DateFormatter('%Y-%m-%d')

    # Create the plot
    fig, axes = mpf.plot(df, type='candle', style=s, volume=True, 
                         ylabel='Price (USD)',
                         ylabel_lower='Volume',
                         figratio=(16,9),
                         figscale=1.2,
                         returnfig=True,
                         show_nontrading=True,
                         tight_layout=True)

    # Customize the plot after it's created
    ax_main = axes[0]
    ax_main.set_title(f"{crypto_id.capitalize()} Price and Volume Over Time", fontsize=16, pad=20)
    ax_main.xaxis.set_major_locator(week_locator)
    ax_main.xaxis.set_major_formatter(date_formatter)
    ax_main.grid(True, which='major', axis='x', linestyle='--', alpha=0.5)
    
    # Rotate x-axis labels
    plt.setp(ax_main.get_xticklabels(), rotation=45, ha='right')

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(f"{crypto_id}_candlestick_chart.png", dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == "__main__":
    crypto_id = "ethereum"
    days = 30
    
    data = get_crypto_data(crypto_id, days)
    df = prepare_data(data)
    plot_candlestick_chart(df, crypto_id)
    print(f"Chart saved as {crypto_id}_candlestick_chart.png in the current directory.")