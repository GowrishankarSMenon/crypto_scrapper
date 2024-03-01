import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_crypto_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table')
            df = pd.DataFrame(columns=['Coin name', 'Price', 'Change(24h)', 'Market cap', 'Volume(24h)'])
            
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    COIN_NAME = columns[0].text.strip()
                    PRICE = columns[1].text.strip()
                    # Use regular expressions to extract numeric values from 'Change(24h)' column
                    CHANGE_24 = re.findall(r'[+-]?\d*\.?\d+', columns[2].text.strip())[0]
                    MARKET_CAP = columns[3].text.strip()
                    VOLUME_24 = columns[4].text.strip()
                    
                    df = df._append({'Coin name': COIN_NAME, 'Price': PRICE, 'Change(24h)': CHANGE_24, 'Market cap': MARKET_CAP, 'Volume(24h)': VOLUME_24}, ignore_index=True)
            
            # Set display width for cleaner output
            pd.set_option('display.max_colwidth', 100)
            # Print the DataFrame after the loop
            #print(df.to_string(index=False))
            return df
        except Exception as e:
            print(e)
    else:
        print("Failed to retrieve data.")

# Example URL of a website with cryptocurrency data
url = "https://www.gadgets360.com/finance/crypto-currency-price-in-india-inr-compare-bitcoin-ether-dogecoin-ripple-litecoin"
scrape_crypto_data(url)
