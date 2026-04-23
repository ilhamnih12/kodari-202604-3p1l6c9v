import random
from utils.helpers import make_embed

EIGHT_BALL_RESPONSES = [
    ("It is certain.", "success"), ("It is decidedly so.", "success"), ("Without a doubt.", "success"),
    ("Yes, definitely.", "success"), ("You may rely on it.", "success"), ("As I see it, yes.", "success"),
    ("Most likely.", "success"), ("Outlook good.", "success"), ("Yes.", "success"), ("Signs point to yes.", "success"),
    ("Reply hazy, try again.", "warning"), ("Ask again later.", "warning"), ("Better not tell you now.", "warning"),
    ("Cannot predict now.", "warning"), ("Concentrate and ask again.", "warning"),
    ("Don't count on it.", "error"), ("My reply is no.", "error"), ("My sources say no.", "error"),
    ("Outlook not so good.", "error"), ("Very doubtful.", "error"),
]

FACTS = [
    "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still edible.",
    "A group of flamingos is called a flamboyance.",
    "Octopuses have three hearts and blue blood.",
    "Bananas are berries, but strawberries are not.",
    "The shortest war in history lasted only 38–45 minutes (Anglo-Zanzibar War, 1896).",
    "A day on Venus is longer than a year on Venus.",
    "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid.",
    "The human brain generates about 20 watts of electrical power.",
    "A bolt of lightning is 5 times hotter than the sun's surface.",
    "Crows can recognize human faces and hold grudges.",
    "There are more stars in the universe than grains of sand on all of Earth's beaches.",
    "Sharks are older than trees — they've been around for ~450 million years.",
    "The Eiffel Tower grows about 6 inches taller in summer due to thermal expansion.",
    "Oxford University is older than the Aztec Empire.",
    "Wombats produce cube-shaped poop.",
]

QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("In the middle of every difficulty lies opportunity.", "Albert Einstein"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Life is what happens when you're busy making other plans.", "John Lennon"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("Strive not to be a success, but rather to be of value.", "Albert Einstein"),
    ("You only live once, but if you do it right, once is enough.", "Mae West"),
    ("In order to be irreplaceable one must always be different.", "Coco Chanel"),
    ("Life is not measured by the number of breaths we take, but by the moments that take our breath away.", "Maya Angelou"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
]

TONGUE_TWISTERS = [
    "She sells seashells by the seashore.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "Peter Piper picked a peck of pickled peppers.",
    "Red lorry, yellow lorry.",
    "I saw Susie sitting in a shoeshine shop.",
    "Six sleek swans swam swiftly southwards.",
    "Betty Botter bought some butter, but the butter was bitter.",
    "Can you can a can as a canner can can a can?",
    "Whether the weather be fine or whether the weather be not.",
    "Fred fed Ted bread, and Ted fed Fred bread.",
]

def eight_ball(client, message, args, sender_jid):
    if not args:
        client.reply_message("Please provide a question!", message)
        return
    question = " ".join(args)
    response, _ = random.choice(EIGHT_BALL_RESPONSES)
    text = make_embed("🎱 Magic 8-Ball", f"*Question:* {question}\n\n🎱 *{response}*")
    client.reply_message(text, message)

def fact(client, message, args, sender_jid):
    text = make_embed("💡 Random Fact", random.choice(FACTS))
    client.reply_message(text, message)

def quote(client, message, args, sender_jid):
    text, author = random.choice(QUOTES)
    formatted = make_embed("✨ Inspirational Quote", f"\"{text}\"\n\n— *{author}*")
    client.reply_message(formatted, message)

def tongue_twister(client, message, args, sender_jid):
    text = make_embed("👅 Tongue Twister", f"Try saying this 3 times fast:\n\n*{random.choice(TONGUE_TWISTERS)}*")
    client.reply_message(text, message)

def pickone(client, message, args, sender_jid):
    options_str = " ".join(args)
    choices = [o.strip() for o in options_str.split(",") if o.strip()]
    if len(choices) < 2:
        client.reply_message("Please provide at least 2 comma-separated options. Example: /pickone pizza, burger", message)
        return
    picked = random.choice(choices)
    formatted = make_embed("🎯 Decision Made!", f"From your options:\n{chr(10).join(f'• {c}' for c in choices)}\n\n🎯 *I choose: {picked}*")
    client.reply_message(formatted, message)

def reverse(client, message, args, sender_jid):
    text = " ".join(args)
    if not text:
        client.reply_message("Please provide text to reverse!", message)
        return
    formatted = make_embed("🔄 Reversed Text", f"*Original:* {text}\n*Reversed:* {text[::-1]}")
    client.reply_message(formatted, message)

def rate(client, message, args, sender_jid):
    thing = " ".join(args)
    if not thing:
        client.reply_message("What do you want me to rate?", message)
        return
    score = random.randint(0, 10)
    bars = "█" * score + "░" * (10 - score)
    comment_map = {
        (0, 2): "Absolutely terrible 💀",
        (3, 4): "Not great, not terrible 😐",
        (5, 6): "Pretty average honestly 🤷",
        (7, 8): "Actually pretty good! 👍",
        (9, 9): "Excellent! Nearly perfect! 🌟",
        (10, 10): "PERFECT! 10/10! 🏆",
    }
    comment = next(v for (lo, hi), v in comment_map.items() if lo <= score <= hi)
    formatted = make_embed("⭐ Rating", f"*{thing}*\n\n`[{bars}]` *{score}/10*\n\n{comment}")
    client.reply_message(formatted, message)

def countdown(client, message, args, sender_jid):
    client.reply_message("Countdown is disabled in WhatsApp to prevent spamming.", message)

def get_commands():
    return {
        "8ball": eight_ball,
        "fact": fact,
        "quote": quote,
        "tongue_twister": tongue_twister,
        "pickone": pickone,
        "reverse": reverse,
        "rate": rate,
        "countdown": countdown
    }
