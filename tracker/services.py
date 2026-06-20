import requests


def send_telegram_message(token, chat_id, message):
    """Sends a text message to a Telegram chat using the Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an exception for HTTP errors
        print("Message sent successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
        return None