import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_crypto_data(crypto_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    data = response.json()
    return data

def plot_price_chart(data, crypto_id):
    df = pd.DataFrame(data['prices'], columns=['Date', 'Price'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Price'])
    plt.title(f"{crypto_id.capitalize()} Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.savefig(f"{crypto_id}_price_chart.png")
    plt.close()

if __name__ == "__main__":
    crypto_id = "ethereum"
    days = 30
    
    data = get_crypto_data(crypto_id, days)
    plot_price_chart(data, crypto_id)
    print(f"Chart saved as {crypto_id}_price_chart.png in the data folder.")