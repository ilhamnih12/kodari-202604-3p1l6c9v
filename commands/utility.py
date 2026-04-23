import time
from utils.helpers import make_embed

start_time = time.time()

def ping(client, message, args, sender_jid):
    client.reply_message("Pong!", message)

def uptime(client, message, args, sender_jid):
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)

    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    client.reply_message(f"Bot Uptime: {hours}h {minutes}m {seconds}s", message)

def serverinfo(client, message, args, sender_jid):
    # In WhatsApp, group info can be seen but requires API requests. Here's a mocked summary or simplified logic.
    if message.info.messageSource.chat.endswith("@g.us"):
        client.reply_message("This command works best in Discord. For WhatsApp groups, group metadata will be fetched in future updates.", message)
    else:
        client.reply_message("You are not in a group.", message)

def userinfo(client, message, args, sender_jid):
    target = args[0] if args else sender_jid.split('@')[0]
    client.reply_message(make_embed("👤 User Info", f"*User:* {target}\n*Platform:* WhatsApp"), message)

def avatar(client, message, args, sender_jid):
    client.reply_message("Avatar fetching is not directly supported via simple text messages without Baileys profile picture API.", message)

def poll(client, message, args, sender_jid):
    if len(args) < 2:
        client.reply_message("Usage: /poll <question>, <option1>, <option2>...", message)
        return
    parts = " ".join(args).split(",")
    if len(parts) < 2:
        client.reply_message("Please provide a question and at least one option, separated by commas.", message)
        return
    question = parts[0].strip()
    options = [opt.strip() for opt in parts[1:] if opt.strip()]

    opts_text = "\n".join([f"{i+1}️⃣ {opt}" for i, opt in enumerate(options)])
    text = make_embed(f"📊 Poll: {question}", f"{opts_text}\n\n_Reply with the number of your choice._")
    client.reply_message(text, message)

def botinfo(client, message, args, sender_jid):
    desc = "A lightweight WhatsApp bot running on Neonize.\n\n" \
           "*Version:* 1.0.0\n" \
           "*Library:* neonize\n" \
           "*Platform:* Koyeb Free Tier Compatible"
    client.reply_message(make_embed("🤖 Bot Info", desc), message)

def get_commands():
    return {
        "ping": ping,
        "uptime": uptime,
        "serverinfo": serverinfo,
        "userinfo": userinfo,
        "avatar": avatar,
        "poll": poll,
        "botinfo": botinfo
    }
