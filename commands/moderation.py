from utils.helpers import make_embed

# Since we are not using full WhatsApp group admin APIs at this moment, we mock these for completeness.
def warn(client, message, args, sender_jid):
    if len(args) < 1:
        client.reply_message("Usage: /warn <user> [reason]", message)
        return
    target = args[0]
    reason = " ".join(args[1:]) if len(args) > 1 else "No reason provided."
    text = make_embed("⚠️ Warning Issued", f"*User:* {target}\n*Reason:* {reason}")
    client.reply_message(text, message)

def warnings(client, message, args, sender_jid):
    if len(args) < 1:
        client.reply_message("Usage: /warnings <user>", message)
        return
    target = args[0]
    text = make_embed("⚠️ Warnings", f"*User:* {target}\n*Total Warnings:* 1 (Mocked)")
    client.reply_message(text, message)

def clearwarns(client, message, args, sender_jid):
    if len(args) < 1:
        client.reply_message("Usage: /clearwarns <user>", message)
        return
    target = args[0]
    text = make_embed("✅ Warnings Cleared", f"Cleared all warnings for *{target}*.")
    client.reply_message(text, message)

def kick(client, message, args, sender_jid):
    client.reply_message("Group admin features (like Kick) must be explicitly managed by group admins via Baileys API. (Mocked response)", message)

def ban(client, message, args, sender_jid):
    client.reply_message("Group admin features (like Ban) must be explicitly managed by group admins via Baileys API. (Mocked response)", message)

def unban(client, message, args, sender_jid):
    client.reply_message("Group admin features (like Unban) must be explicitly managed by group admins via Baileys API. (Mocked response)", message)

def timeout(client, message, args, sender_jid):
    client.reply_message("Group admin features (like Timeout/Mute) must be explicitly managed by group admins via Baileys API. (Mocked response)", message)

def purge(client, message, args, sender_jid):
    client.reply_message("Deleting multiple messages simultaneously isn't natively supported in standard WhatsApp simple APIs. (Mocked response)", message)

def get_commands():
    return {
        "warn": warn,
        "warnings": warnings,
        "clearwarns": clearwarns,
        "kick": kick,
        "ban": ban,
        "unban": unban,
        "timeout": timeout,
        "purge": purge
    }
