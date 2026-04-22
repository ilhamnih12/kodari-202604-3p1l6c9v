import discord
import json
import os

ECONOMY_FILE = "data/economy.json"
FEEDBACK_FILE = "data/feedback.json"

COLORS = {
    "primary": 0x5865F2,
    "success": 0x57F287,
    "error": 0xED4245,
    "warning": 0xFEE75C,
    "info": 0x5DADE2,
    "fun": 0xFF79C6,
    "gold": 0xF1C40F,
}

CATEGORY_EMOJIS = {
    "Games": "🎮",
    "Trivia": "🧠",
    "Memes": "😂",
    "Fun": "🎉",
    "Economy": "💰",
    "Utility": "🔧",
    "Moderation": "🛡️",
    "Social": "💞",
    "Math": "📐",
    "Anime": "🌸",
    "Menu": "📋",
}

def load_economy():
    if not os.path.exists(ECONOMY_FILE):
        return {}
    with open(ECONOMY_FILE, "r") as f:
        return json.load(f)

def save_economy(data):
    with open(ECONOMY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_balance(user_id: int):
    data = load_economy()
    key = str(user_id)
    if key not in data:
        data[key] = {"balance": 0, "last_daily": None, "inventory": []}
        save_economy(data)
    return data[key]

def update_user(user_id: int, updates: dict):
    data = load_economy()
    key = str(user_id)
    if key not in data:
        data[key] = {"balance": 0, "last_daily": None, "inventory": []}
    data[key].update(updates)
    save_economy(data)

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)

def save_feedback(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

def make_embed(title: str, description: str = "", color_key: str = "primary", footer: str = "FunBot") -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=COLORS.get(color_key, COLORS["primary"])
    )
    embed.set_footer(text=footer)
    return embed

def load_trivia():
    with open("data/trivia.json", "r") as f:
        return json.load(f)