from bot_config import bot, NEWS_API_KEY
from helpers import send_long_message, fetch_news, build_gold_report
from content import get_random_lesson, get_random_quiz
from vip_handler import vip_users, save_vip_users
from nowpayments import generate_nowpayments_invoice

from telebot import types

def register_callbacks(bot):
    @bot.message_handler(commands=["start","help"])
    def handle_start(message):
        chat_id = message.chat.id
        markup = types.InlineKeyboardMarkup()
        if chat_id in vip_users:
            markup.row(
                types.InlineKeyboardButton("📊 Daily", callback_data="daily"),
                types.InlineKeyboardButton("⏳ 4H", callback_data="4h")
            )
            markup.row(
                types.InlineKeyboardButton("📑 Combined", callback_data="combined"),
                types.InlineKeyboardButton("⚡ Quick Signal", callback_data="signal")
            )
        markup.row(
            types.InlineKeyboardButton("📖 Learn", callback_data="learn"),
            types.InlineKeyboardButton("❓ Quiz", callback_data="quiz")
        )
        markup.row(
            types.InlineKeyboardButton("📰 News", callback_data="news"),
            types.InlineKeyboardButton("💎 Upgrade to VIP", callback_data="upgrade_vip")
        )
        bot.reply_to(message, "🤖 Gold Signal Bot\nChoose an option or use commands.", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        chat_id = call.message.chat.id
        try:
            bot.answer_callback_query(call.id,"Generating...")
            if call.data=="upgrade_vip":
                invoice_url = generate_nowpayments_invoice(chat_id)
                if invoice_url:
                    bot.send_message(chat_id,f"💳 Upgrade to VIP:\nPay here → {invoice_url}")
                else:
                    bot.send_message(chat_id,"⚠️ Failed to generate payment link.")
                return

            if call.data in ["daily","4h","combined","signal"] and chat_id not in vip_users:
                bot.send_message(chat_id,"💎 This is a VIP feature. Upgrade to access!")
                return

            if call.data=="daily":
                send_long_message(chat_id,"📊 Daily Report\n\n"+build_gold_report("1d","6mo"))
            elif call.data=="4h":
                send_long_message(chat_id,"⏳ 4H Report\n\n"+build_gold_report("4h","60d"))
            elif call.data=="combined":
                daily = build_gold_report("1d","6mo")
                h4 = build_gold_report("4h","60d")
                send_long_message(chat_id,"📊 Combined Report\n\n"+daily+"\n"+h4)
            elif call.data=="signal":
                bot.send_message(chat_id,build_gold_report("4h","60d",quick=True))
            elif call.data=="learn":
                bot.send_message(chat_id,f"📖 Lesson:\n{get_random_lesson()}")
            elif call.data=="quiz":
                q = get_random_quiz()
                markup = types.InlineKeyboardMarkup()
                for opt in q["options"]:
                    markup.add(types.InlineKeyboardButton(opt, callback_data=f"quiz_{opt}_{q['answer']}"))
                bot.send_message(chat_id,f"❓ {q['q']}",reply_markup=markup)
            elif call.data.startswith("quiz_"):
                _, choice, answer = call.data.split("_",2)
                bot.send_message(chat_id,"✅ Correct!" if choice==answer else f"❌ Wrong. Correct: {answer}")
            elif call.data=="news":
                send_long_message(chat_id, fetch_news(NEWS_API_KEY))
        except:
            import logging; logging.exception("Callback query error")
            bot.send_message(chat_id,"⚠️ Failed to process request.")
