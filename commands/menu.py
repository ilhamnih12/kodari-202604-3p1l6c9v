from utils.helpers import make_embed, load_feedback, save_feedback

COMMAND_DATA = {
    "🎮 Games": {
        "description": "Interactive games to play solo or challenge friends",
        "commands": [
            ("/rps", "Play Rock Paper Scissors against the bot"),
            ("/coinflip", "Flip a coin and guess the result"),
            ("/dice", "Roll one or more dice with customizable sides"),
            ("/slots", "Spin the slot machine for prizes!"),
            ("/blackjack", "Play Blackjack against the dealer"),
            ("/numberguess", "Guess the secret number (1–100)"),
        ],
    },
    "🧠 Trivia": {
        "description": "Test your knowledge across many categories",
        "commands": [
            ("/trivia", "Answer a random multiple-choice trivia question"),
        ],
    },
    "🎉 Fun": {
        "description": "Lighthearted fun commands for everyone",
        "commands": [
            ("/8ball", "Ask the magic 8-ball a yes/no question"),
            ("/fact", "Get a random interesting fact"),
            ("/quote", "Get an inspirational quote"),
            ("/tongue_twister", "Get a tongue twister challenge"),
            ("/pickone", "Let the bot choose between your options"),
            ("/reverse", "Reverse any text"),
            ("/rate", "Rate anything out of 10"),
        ],
    },
    "💰 Economy": {
        "description": "Earn, spend, and manage your virtual coins",
        "commands": [
            ("/balance", "Check your coin balance"),
            ("/daily", "Claim your daily 200 🪙 reward"),
            ("/work", "Work to earn coins"),
            ("/pay", "Send coins to another user"),
            ("/shop", "View the item shop"),
            ("/buy", "Purchase an item from the shop"),
            ("/inventory", "View your purchased items"),
            ("/leaderboard", "See the richest users"),
        ],
    },
    "🔧 Utility": {
        "description": "Helpful server and user tools",
        "commands": [
            ("/ping", "Check the bot's latency"),
            ("/feedback", "Send feedback to bot owner"),
        ],
    },
}

def menu(client, message, args, sender_jid):
    total = sum(len(v["commands"]) for v in COMMAND_DATA.values())
    categories = len(COMMAND_DATA)

    lines = []
    for cat, info in COMMAND_DATA.items():
        lines.append(f"*{cat}*")
        lines.append(f"_{info['description']}_")
        for cmd, desc in info['commands']:
            lines.append(f"  {cmd} - {desc}")
        lines.append("")

    desc = (
        f"Welcome to *FunBot*! 🎉\n"
        f"*{categories} categories* | *{total} commands*\n\n"
        + "\n".join(lines)
    )
    text = make_embed("📋 FunBot — Command Menu", desc)
    client.reply_message(text, message)

def help_command(client, message, args, sender_jid):
    client.reply_message("Please use /menu to see the list of all commands.", message)

def feedback(client, message, args, sender_jid):
    msg = " ".join(args)
    if len(msg) < 10:
        client.reply_message("Feedback must be at least 10 characters. Usage: /feedback <message>", message)
        return

    data = load_feedback()
    entry = {
        "user_id": sender_jid,
        "message": msg,
    }
    data.append(entry)
    save_feedback(data)

    text = make_embed("⭐ Feedback Received!", f"*Message:* {msg}\n\nThank you for helping improve FunBot! 💖")
    client.reply_message(text, message)

def get_commands():
    return {
        "menu": menu,
        "help": help_command,
        "feedback": feedback
    }
