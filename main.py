import threading
from flask import Flask
from bot_config import bot
from callbacks import register_callbacks
from vip_handler import vip_users, save_vip_users

app = Flask(__name__)
register_callbacks(bot)  # set up Telegram callbacks

@app.route("/nowpayments-ipn", methods=["POST"])
def nowpayments_ipn():
    from flask import request
    data = request.json
    if not data:
        return "No data", 400
    order_id = data.get("order_id")
    payment_status = data.get("payment_status")
    if order_id and payment_status in ["finished","confirmed"]:
        user_id = int(order_id)
        vip_users.add(user_id)
        save_vip_users()
        try:
            bot.send_message(user_id, "🎉 Your VIP Upgrade is confirmed! Enjoy premium features.")
        except:
            pass
    return "OK", 200

def run_flask():
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def run_bot():
    bot.infinity_polling(timeout=60,long_polling_timeout=60)

threading.Thread(target=run_flask).start()
threading.Thread(target=run_bot).start()
