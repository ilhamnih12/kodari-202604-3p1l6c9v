import requests
from utils.helpers import make_embed

def meme(client, message, args, sender_jid):
    try:
        resp = requests.get("https://meme-api.com/gimme")
        if resp.status_code == 200:
            data = resp.json()
            title = data.get("title", "Random Meme")
            url = data.get("url", "")

            text = make_embed(f"😂 {title}", f"{url}")
            client.reply_message(text, message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def meme_category(client, message, args, sender_jid):
    if not args:
        client.reply_message("Usage: /meme_category <subreddit>", message)
        return
    subreddit = args[0]
    try:
        resp = requests.get(f"https://meme-api.com/gimme/{subreddit}")
        if resp.status_code == 200:
            data = resp.json()
            title = data.get("title", "Random Meme")
            url = data.get("url", "")

            text = make_embed(f"😂 r/{subreddit}: {title}", f"{url}")
            client.reply_message(text, message)
        else:
            client.reply_message("API Error or subreddit not found.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def meme_top(client, message, args, sender_jid):
    if not args:
        client.reply_message("Usage: /meme_top <subreddit>", message)
        return
    subreddit = args[0]
    try:
        resp = requests.get(f"https://meme-api.com/gimme/{subreddit}")
        if resp.status_code == 200:
            data = resp.json()
            title = data.get("title", "Random Meme")
            url = data.get("url", "")

            text = make_embed(f"🔥 Top in r/{subreddit}: {title}", f"{url}")
            client.reply_message(text, message)
        else:
            client.reply_message("API Error or subreddit not found.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def meme_templates(client, message, args, sender_jid):
    templates = "1. Drake Hotline Bling\n2. Distracted Boyfriend\n3. Two Buttons\n4. Change My Mind\n5. Batman Slapping Robin"
    client.reply_message(make_embed("🖼️ Popular Meme Templates", templates), message)

def joke(client, message, args, sender_jid):
    try:
        resp = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
        if resp.status_code == 200:
            joke_text = resp.json().get("joke", "Error fetching joke.")
            text = make_embed("😂 Random Joke", joke_text)
            client.reply_message(text, message)
        else:
            client.reply_message("API Error.", message)
    except Exception as e:
        client.reply_message(f"Error: {e}", message)

def roast(client, message, args, sender_jid):
    target = " ".join(args) if args else "You"
    roasts = [
        "If laughter is the best medicine, your face must be curing the world.",
        "You bring everyone so much joy... when you leave the room.",
        "I'd agree with you but then we'd both be wrong.",
        "You have miles to go before you reach mediocre.",
        "I’m not insulting you, I’m describing you.",
    ]
    import random
    roast_text = random.choice(roasts)
    client.reply_message(make_embed("🔥 Roast", f"{target}, {roast_text}"), message)


def get_commands():
    return {
        "meme": meme,
        "meme_category": meme_category,
        "meme_top": meme_top,
        "meme_templates": meme_templates,
        "joke": joke,
        "roast": roast
    }
