import os
import requests
import time
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY= os.getenv('COINGECKO_API_KEY')

def save_to_csv(asset, price):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "crypto_history.csv")
    file_exists = os.path.isfile(file_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(file_path, mode="a", newline="") as file:
            writer= csv.writer(file)
            if not file_exists:
                writer.writerow(['Timestamp', 'Asset', 'Price_USD'])
            writer.writerow([timestamp, asset, price])
    except Exception as e:
        print(f"ERROR TRYING TO WRITE: {e}")

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": API_KEY
        }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data[coin_id]['usd']
    except Exception as e:
        print(f'connection error: {e}')
        return None


def monitor(coin_id, limit):
    actual_price = get_price(coin_id)
    if actual_price is not None:
        save_to_csv(coin_id.upper(), actual_price)
        if actual_price <= limit:
            print(f"ALARM! {coin_id.upper()} is at ${actual_price}. Good time to buy.")
        else:
            print(f"Price of {coin_id.upper()}: ${actual_price}. Still above the limit.")

if __name__ == "__main__":
    my_limit = 69300.00
    target_crypto = 'bitcoin'
    
    print(f'--- Crypto Monitor Started for {target_crypto} ---')
    
    try:
        while True:
            monitor(target_crypto, my_limit)
            time.sleep(60)
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        
        input("Press Enter to close...")

input("If you are watching this, the program has ended. Press enter to quit.")
