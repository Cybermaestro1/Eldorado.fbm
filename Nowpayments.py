import requests
import logging
from bot_config import NOWPAYMENTS_API_KEY

logger = logging.getLogger(__name__)
IPN_URL = "https://YOUR_RENDER_URL/nowpayments-ipn"

def generate_nowpayments_invoice(user_id, amount_usd=5):
    url = "https://api.nowpayments.io/v1/invoice"
    headers = {"x-api-key": NOWPAYMENTS_API_KEY, "Content-Type": "application/json"}
    data = {
        "price_amount": amount_usd,
        "price_currency": "usd",
        "pay_currency": "usd,btc,eth,usdt",
        "order_id": str(user_id),
        "ipn_callback_url": IPN_URL
    }
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        return result.get("invoice_url")
    except Exception as e:
        logger.exception("NowPayments invoice error")
        return None
