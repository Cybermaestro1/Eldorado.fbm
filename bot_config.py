import os
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")
NOWPAYMENTS_API_KEY = os.environ.get("NOWPAYMENTS_API_KEY", "")
VIP_FILE = "vip_users.json"

bot = telebot.TeleBot(BOT_TOKEN)
