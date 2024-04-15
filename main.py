import asyncio
import requests
import sched
import sqlite3
import time
from telegram import Bot


bot_token = '6428194229:AAGRdb2z9197-zz9zdWXZfus8HMfhsoUWYk'
chat_id = '925553030'

# Replace 'YOUR_API_KEY' with your actual CoinMarketCap API key
api_key = '5f5739a1-661b-4a8e-bab2-a6fbac4caa52'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key
}

# bot = Bot(token=bot_token)

# Connect to the SQLite database
conn = sqlite3.connect('prices.db')
cursor = conn.cursor()

# Create the 'prices' table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS prices
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   bitcoin_price REAL,
                   ethereum_price REAL,
                   solana_price REAL)''')

def send_price_message():
    # Get the latest prices of Bitcoin, Ethereum and Solana from CoinMarketCap API
    response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,ETH,SOL', headers=headers)

    if response.status_code == 200:
        data = response.json()
        bitcoin_price = data['data']['BTC']['quote']['USD']['price']
        ethereum_price = data['data']['ETH']['quote']['USD']['price']
        solana_price = data['data']['SOL']['quote']['USD']['price']
        message = f'Current prices:\nBitcoin: ${bitcoin_price:.2f}\nEthereum: ${ethereum_price:.2f}\nSolana: ${solana_price:.2f}'

        # Insert the prices into the 'prices' table
        cursor.execute('''INSERT INTO prices(bitcoin_price, ethereum_price, solana_price) VALUES(?,?,?)''', (bitcoin_price, ethereum_price, solana_price))
        conn.commit()

        # Print the latest price
        cursor.execute('SELECT * FROM prices ORDER BY id DESC LIMIT 1')
        latest_price = cursor.fetchone()
        print(latest_price)

        # Send the message using the Telegram bot
        # await bot.send_message(chat_id=chat_id, text=message)
    else:
        print(f'Error: {response.status_code}')


scheduler = sched.scheduler(time.time, time.sleep)
def repeat_task():
    scheduler.enter(5, 1, send_price_message, ())
    scheduler.enter(5, 1, repeat_task, ())
repeat_task()
scheduler.run()
    