import logging
import requests
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
MAX_MESSAGE_LENGTH = 4000

def send_long_message(bot, chat_id, text, markup=None):
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        bot.send_message(chat_id, text[i:i+MAX_MESSAGE_LENGTH], reply_markup=markup if i == 0 else None)

def fetch_news(NEWS_API_KEY, query=None, page_size=7):
    if not NEWS_API_KEY:
        return "⚠️ News API key not configured."
    base = "https://newsapi.org/v2/everything"
    if not query:
        query = "gold OR GC=F OR bitcoin OR btc OR ethereum OR eth OR crypto OR forex OR usd OR eur OR gbp OR jpy OR s&p OR spx OR nasdaq OR dow OR stocks OR equities"
    params = {"q": query,"language":"en","pageSize":page_size,"sortBy":"publishedAt","apiKey":NEWS_API_KEY}
    try:
        resp = requests.get(base, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        lines = ["📰 Top Market News:\n"]
        for i, a in enumerate(articles, 1):
            title = a.get("title","No title")
            source = a.get("source",{}).get("name","Unknown")
            url = a.get("url","")
            published = a.get("publishedAt")
            try:
                ts = datetime.fromisoformat(published.replace("Z","+00:00")).astimezone(timezone.utc)
                published_str = ts.strftime("%Y-%m-%d %H:%M UTC")
            except:
                published_str = published or ""
            lines.append(f"{i}. {title} — {source} ({published_str})\n{url}\n")
        lines.append("\n🔎 Use /news <keyword> to search specific topics.")
        lines.append("\n🔗 Powered by Eldorado.FBM Bot")
        return "\n".join(lines)
    except Exception as e:
        logger.exception("News fetch error")
        return "⚠️ Error fetching news."

def build_gold_report(interval="1d", period="6mo", quick=False):
    try:
        df = yf.download("GC=F", interval=interval, period=period, progress=False, auto_adjust=True)
        if df.empty:
            return "⚠️ No market data available."
        df = df.tail(50)
        df.index = pd.to_datetime(df.index)
        close = df["Close"].astype(float).squeeze()
        high = df["High"].astype(float).squeeze()
        low = df["Low"].astype(float).squeeze()
        ma20 = close.rolling(20, min_periods=1).mean()
        ma50 = close.rolling(50, min_periods=1).mean()
        rsi_series = ta.momentum.RSIIndicator(close, window=14).rsi().squeeze()
        atr_series = ta.volatility.AverageTrueRange(high, low, close, window=14).average_true_range().squeeze()
        last_close = float(close.iloc[-1])
        last_ma20 = float(ma20.iloc[-1])
        last_ma50 = float(ma50.iloc[-1])
        last_rsi = float(rsi_series.iloc[-1])
        last_atr = float(atr_series.iloc[-1])
        forecast_signal = "Neutral 🤔"
        if last_ma20 > last_ma50 and last_rsi < 70:
            forecast_signal = "Bullish 📈"
        elif last_ma20 < last_ma50 and last_rsi > 30:
            forecast_signal = "Bearish 📉"
        last_low_range = low.iloc[-20:] if len(low)>=20 else low
        last_high_range = high.iloc[-20:] if len(high)>=20 else high
        support = float(last_low_range.min())
        resistance = float(last_high_range.max())
        return f"{forecast_signal}\nClose: {last_close:.2f} | Support: {support:.2f} | Resistance: {resistance:.2f}"
    except Exception as e:
        logger.exception("Error generating report")
        return f"⚠️ Error generating report: {str(e)}"
