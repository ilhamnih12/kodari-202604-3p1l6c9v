import random
from utils.helpers import make_embed

SOCIAL_GIFS = {
    "hug": [
        "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
        "https://media.giphy.com/media/3M4NpbLCTxBqU/giphy.gif",
    ],
    "kiss": [
        "https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif",
        "https://media.giphy.com/media/bGm9FEBjB5oX6/giphy.gif",
    ],
    "slap": [
        "https://media.giphy.com/media/xUO4t2gkziBtki2q2U/giphy.gif",
        "https://media.giphy.com/media/cEYFeE4wJ6jdDVBiiIM/giphy.gif",
    ],
    "pat": [
        "https://media.giphy.com/media/5tmRHwTlHAZB/giphy.gif",
        "https://media.giphy.com/media/ARSp9T7wwxNcs/giphy.gif",
    ],
    "poke": [
        "https://media.giphy.com/media/WvVzZ9mCyMjsc/giphy.gif",
        "https://media.giphy.com/media/WvJRPbPxY3i8o/giphy.gif",
    ],
    "highfive": [
        "https://media.giphy.com/media/2Y9OFE20RBHmwSoFnX/giphy.gif",
        "https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif",
    ],
    "wave": [
        "https://media.giphy.com/media/Zb8bZUdrOP7P/giphy.gif",
        "https://media.giphy.com/media/IThjAlJnD9WNO/giphy.gif",
    ],
}

def social_action(action, emoji):
    def wrapper(client, message, args, sender_jid):
        if not args:
            client.reply_message(f"Who do you want to {action}?", message)
            return
        target = " ".join(args)
        gif = random.choice(SOCIAL_GIFS.get(action, []))
        text = make_embed(f"{emoji} {action.capitalize()}", f"*{sender_jid.split('@')[0]}* {action}s *{target}*!\n\n{gif}")
        client.reply_message(text, message)
    return wrapper

hug = social_action("hug", "🤗")
kiss = social_action("kiss", "💋")
slap = social_action("slap", "👋")
pat = social_action("pat", "🫶")
poke = social_action("poke", "👉")
highfive = social_action("highfive", "🙌")
wave = social_action("wave", "👋")

def ship(client, message, args, sender_jid):
    if len(args) < 2:
        client.reply_message("Usage: /ship <person1> <person2>", message)
        return

    person1 = args[0]
    person2 = args[1]

    score = random.randint(0, 100)
    bar_filled = round(score / 10)
    bar = "❤️" * bar_filled + "🖤" * (10 - bar_filled)

    if score >= 90:
        comment = "💍 Soulmates! A match made in heaven!"
    elif score >= 70:
        comment = "💕 Great couple! Very compatible!"
    elif score >= 50:
        comment = "💛 Pretty good! Give it a shot!"
    elif score >= 30:
        comment = "🤷 Eh... could go either way."
    else:
        comment = "💔 Not the best match..."

    ship_name = person1[:len(person1)//2] + person2[len(person2)//2:]

    text = make_embed(f"💘 Ship: {ship_name}", f"{person1} + {person2}\n\n{bar}\n\n*{score}% compatible*\n{comment}")
    client.reply_message(text, message)

def compliment(client, message, args, sender_jid):
    if not args:
        client.reply_message("Who do you want to compliment?", message)
        return
    target = " ".join(args)
    compliments = [
        "You light up every room you walk into! ✨",
        "Your kindness is truly contagious! 💛",
        "You have an amazing sense of humor! 😄",
        "You're incredibly talented and it shows! 🌟",
        "The world is a better place with you in it! 🌍",
        "You always know how to make people smile! 😊",
        "Your creativity is absolutely inspiring! 🎨",
        "You're one of the most genuine people around! 💎",
    ]
    text = make_embed("💌 Compliment", f"{target} — {random.choice(compliments)}\n\n_From {sender_jid.split('@')[0]} with love_ 💝")
    client.reply_message(text, message)

def get_commands():
    return {
        "hug": hug,
        "kiss": kiss,
        "slap": slap,
        "pat": pat,
        "poke": poke,
        "highfive": highfive,
        "wave": wave,
        "ship": ship,
        "compliment": compliment
    }
