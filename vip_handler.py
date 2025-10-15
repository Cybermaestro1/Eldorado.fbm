import os, json
from bot_config import VIP_FILE

if os.path.exists(VIP_FILE):
    with open(VIP_FILE, "r") as f:
        vip_users = set(json.load(f))
else:
    vip_users = set()

def save_vip_users():
    with open(VIP_FILE, "w") as f:
        json.dump(list(vip_users), f)
