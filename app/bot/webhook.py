import os
import time
import requests
from aiogram.loggers import webhook
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_BOT_TOKEN")
NGROK_API = "http://ngrok:4040/api/tunnels"
ENV_PATH = ".env"

def get_ngrok_url():
    for _ in range(10):
        try:
            response = requests.get(NGROK_API).json()
            for tunnel in response["tunnels"]:
                if tunnel["proto"] == "https":
                    return tunnel["public_url"]
        except Exception:
            time.sleep(2)
    raise Exception("Ngrok URL not found")

def update_env(ngrok_url):
    lines = []
    with open(ENV_PATH, "r") as file:
        for line in file:
            if line.startswith("BASE_URL="):
                lines.append(f"BASE_URL={ngrok_url}\n")
            else:
                lines.append(line)
    with open(ENV_PATH, "w") as file:
        file.writelines(lines)


def webhook_update():
    ngrok_url = get_ngrok_url()
    print("NGROK URL:", ngrok_url)
    update_env(ngrok_url)
    return ngrok_url
