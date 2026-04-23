import json
import os

ECONOMY_FILE = "data/economy.json"
FEEDBACK_FILE = "data/feedback.json"

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

def get_balance(user_id: str):
    data = load_economy()
    if user_id not in data:
        data[user_id] = {"balance": 0, "last_daily": None, "inventory": []}
        save_economy(data)
    return data[user_id]

def update_user(user_id: str, updates: dict):
    data = load_economy()
    if user_id not in data:
        data[user_id] = {"balance": 0, "last_daily": None, "inventory": []}
    data[user_id].update(updates)
    save_economy(data)

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)

def save_feedback(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

def make_embed(title: str, description: str = "", color_key: str = "primary", footer: str = "FunBot") -> str:
    """
    Since WhatsApp does not support rich embeds, we format it as a clean text block.
    """
    lines = []
    lines.append(f"*{title}*")
    lines.append("────────────────")
    if description:
        lines.append(description)
        lines.append("────────────────")
    if footer:
        lines.append(f"_{footer}_")

    return "\n".join(lines)

def load_trivia():
    with open("data/trivia.json", "r") as f:
        return json.load(f)
