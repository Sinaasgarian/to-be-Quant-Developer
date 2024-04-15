import asyncio
from telegram import Bot

bot_token = '6428194229:AAGRdb2z9197-zz9zdWXZfus8HMfhsoUWYk'
chat_id = '@sinaasgarian'
message = 'This is a test message'


async def send_message():
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

# اجرای کوروتین
asyncio.run(send_message())