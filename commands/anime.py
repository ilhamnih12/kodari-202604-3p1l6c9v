import requests
from utils.helpers import make_embed

def anime_search(client, message, args, sender_jid):
    query = " ".join(args)
    if not query:
        client.reply_message("Usage: /anime_search <title>", message)
        return

    try:
        resp = requests.get(f"https://api.jikan.moe/v4/anime?q={query}&limit=1")
        if resp.status_code == 200:
            data = resp.json().get("data")
            if data:
                anime = data[0]
                title = anime.get("title", "Unknown")
                score = anime.get("score", "N/A")
                episodes = anime.get("episodes", "N/A")
                synopsis = anime.get("synopsis", "No synopsis available.")[:200] + "..."
                url = anime.get("url", "")

                text = make_embed(f"🌸 {title}", f"*Score:* {score} | *Episodes:* {episodes}\n\n{synopsis}\n\n[More Info]({url})")
                client.reply_message(text, message)
            else:
                client.reply_message("Anime not found.", message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def waifu(client, message, args, sender_jid):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/waifu")
        if resp.status_code == 200:
            url = resp.json().get("url")
            client.reply_message(make_embed("🌸 Random Waifu", f"{url}"), message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def neko(client, message, args, sender_jid):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/neko")
        if resp.status_code == 200:
            url = resp.json().get("url")
            client.reply_message(make_embed("🐱 Random Neko", f"{url}"), message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def anime_action(client, message, args, sender_jid):
    try:
        actions = ["hug", "kiss", "pat", "slap", "poke"]
        import random
        action = random.choice(actions)
        resp = requests.get(f"https://api.waifu.pics/sfw/{action}")
        if resp.status_code == 200:
            url = resp.json().get("url")
            client.reply_message(make_embed(f"🌸 Anime Action ({action.title()})", f"{url}"), message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def anime_quote(client, message, args, sender_jid):
    try:
        resp = requests.get("https://animechan.xyz/api/random")
        if resp.status_code == 200:
            data = resp.json()
            quote = data.get("quote", "No quote found.")
            character = data.get("character", "Unknown")
            anime = data.get("anime", "Unknown")
            client.reply_message(make_embed("🌸 Anime Quote", f"\"{quote}\"\n\n— *{character}* ({anime})"), message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def shinobu(client, message, args, sender_jid):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/shinobu")
        if resp.status_code == 200:
            url = resp.json().get("url")
            client.reply_message(make_embed("🦋 Shinobu", f"{url}"), message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def megumin(client, message, args, sender_jid):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/megumin")
        if resp.status_code == 200:
            url = resp.json().get("url")
            client.reply_message(make_embed("💥 Megumin", f"{url}"), message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def get_commands():
    return {
        "anime_search": anime_search,
        "waifu": waifu,
        "neko": neko,
        "anime_action": anime_action,
        "anime_quote": anime_quote,
        "shinobu": shinobu,
        "megumin": megumin
    }
