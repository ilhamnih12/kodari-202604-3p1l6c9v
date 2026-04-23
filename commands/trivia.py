import random
from utils.helpers import make_embed, load_trivia

def trivia(client, message, args, sender_jid):
    try:
        data = load_trivia()
        q = random.choice(data)

        options = q["options"]
        random.shuffle(options)

        opts_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])

        text = make_embed(
            "🧠 Trivia Time!",
            f"*{q['question']}*\n\n{opts_text}\n\n_Wait a few seconds to see the answer... (Interactive buttons not supported on this version)_"
        )
        client.reply_message(text, message)

        # In a real async WhatsApp bot, we'd sleep and send answer.
        # But `neonize` events are synchronous blocks right now in our setup unless we use threading/async.
        # For simplicity, we just send the answer together with spoiler or separate message.
        client.reply_message(f"The correct answer is: *{q['answer']}*", message)

    except Exception as e:
        client.reply_message(f"Error loading trivia: {e}", message)

def get_commands():
    return {
        "trivia": trivia
    }
