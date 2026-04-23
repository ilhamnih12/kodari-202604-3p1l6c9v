import random
from datetime import datetime, timedelta
from utils.helpers import make_embed, get_balance, update_user, load_economy

DAILY_AMOUNT = 200
WORK_JOBS = [
    ("🍕 delivered pizzas", 50, 120),
    ("💻 fixed some bugs", 80, 200),
    ("🌿 mowed lawns", 30, 90),
    ("🎨 painted a mural", 70, 180),
    ("📦 sorted packages", 40, 100),
    ("🐾 walked dogs", 35, 85),
    ("🎵 busked on the street", 20, 150),
    ("🍔 flipped burgers", 45, 95),
    ("📚 tutored students", 60, 160),
    ("🔧 repaired appliances", 55, 140),
]

SHOP_ITEMS = {
    "lucky_charm": {"name": "🍀 Lucky Charm", "price": 500, "desc": "Increases your next slot win chance."},
    "vip_badge": {"name": "⭐ VIP Badge", "price": 1000, "desc": "Shows you're a VIP in this server."},
    "golden_dice": {"name": "🎲 Golden Dice", "price": 750, "desc": "A beautiful golden dice for collectors."},
    "mystery_box": {"name": "🎁 Mystery Box", "price": 300, "desc": "Contains a random reward!"},
    "crown": {"name": "👑 Crown", "price": 2000, "desc": "The ultimate status symbol."},
}

def balance(client, message, args, sender_jid):
    # If a number is mentioned, we could parse it, but for simplicity we show the sender's balance
    data = get_balance(sender_jid)
    text = make_embed(
        f"💰 Balance",
        f"*Coins:* `{data['balance']:,} 🪙`\n*Items:* `{len(data.get('inventory', []))}` items in inventory"
    )
    client.reply_message(text, message)

def daily(client, message, args, sender_jid):
    data = get_balance(sender_jid)
    now = datetime.utcnow()
    last = data.get("last_daily")
    if last:
        last_dt = datetime.fromisoformat(last)
        diff = now - last_dt
        if diff < timedelta(hours=24):
            remaining = timedelta(hours=24) - diff
            hrs, rem = divmod(int(remaining.total_seconds()), 3600)
            mins = rem // 60
            text = make_embed("⏰ Daily Reward", f"You already claimed today's reward!\nCome back in *{hrs}h {mins}m*.")
            client.reply_message(text, message)
            return
    new_balance = data["balance"] + DAILY_AMOUNT
    update_user(sender_jid, {"balance": new_balance, "last_daily": now.isoformat()})
    text = make_embed("🎁 Daily Reward", f"You claimed your daily *{DAILY_AMOUNT:,} 🪙*!\n\n💰 *New Balance:* `{new_balance:,} 🪙`")
    client.reply_message(text, message)

def work(client, message, args, sender_jid):
    job, low, high = random.choice(WORK_JOBS)
    earned = random.randint(low, high)
    data = get_balance(sender_jid)
    new_balance = data["balance"] + earned
    update_user(sender_jid, {"balance": new_balance})
    text = make_embed("💼 Work", f"You {job} and earned *{earned} 🪙*!\n\n💰 *New Balance:* `{new_balance:,} 🪙`")
    client.reply_message(text, message)

def pay(client, message, args, sender_jid):
    if len(args) < 2:
        client.reply_message("Usage: /pay <number> <amount>", message)
        return

    target_num = args[0].replace("@", "").replace("+", "").replace("-", "")
    try:
        amount = int(args[1])
    except ValueError:
        client.reply_message("Amount must be a number.", message)
        return

    target_jid = f"{target_num}@s.whatsapp.net"

    if target_jid == sender_jid:
        client.reply_message("You can't pay yourself!", message)
        return

    if amount <= 0:
        client.reply_message("Amount must be positive.", message)
        return

    sender = get_balance(sender_jid)
    if sender["balance"] < amount:
        client.reply_message(f"Insufficient funds. You have `{sender['balance']:,} 🪙`.", message)
        return

    receiver = get_balance(target_jid)
    update_user(sender_jid, {"balance": sender["balance"] - amount})
    update_user(target_jid, {"balance": receiver["balance"] + amount})
    text = make_embed("💸 Payment Sent", f"You sent *{amount:,} 🪙* to {target_num}!\n\n💰 *Your new balance:* `{sender['balance'] - amount:,} 🪙`")
    client.reply_message(text, message)

def shop(client, message, args, sender_jid):
    desc = "\n".join(f"*{v['name']}* — `{v['price']:,} 🪙`\n{v['desc']}\nID: {k}\n" for k, v in SHOP_ITEMS.items())
    text = make_embed("🛒 Item Shop", desc, footer="Use /buy <item_id> to purchase!")
    client.reply_message(text, message)

def buy(client, message, args, sender_jid):
    if not args:
        client.reply_message("Usage: /buy <item_id>", message)
        return

    item_id = args[0].lower()
    item = SHOP_ITEMS.get(item_id)
    if not item:
        client.reply_message(f"Item `{item_id}` not found. Use `/shop` to see available items.", message)
        return

    data = get_balance(sender_jid)
    if data["balance"] < item["price"]:
        client.reply_message(f"You need `{item['price']:,} 🪙` but only have `{data['balance']:,} 🪙`.", message)
        return

    new_balance = data["balance"] - item["price"]
    inventory = data.get("inventory", [])
    inventory.append(item_id)
    update_user(sender_jid, {"balance": new_balance, "inventory": inventory})
    text = make_embed("✅ Purchase Successful", f"You bought *{item['name']}* for `{item['price']:,} 🪙`!\n\n💰 *New Balance:* `{new_balance:,} 🪙`")
    client.reply_message(text, message)

def inventory(client, message, args, sender_jid):
    data = get_balance(sender_jid)
    inv = data.get("inventory", [])
    if not inv:
        client.reply_message(make_embed("🎒 Inventory", "Your inventory is empty! Use `/shop` to buy items."), message)
        return

    counts = {}
    for item_id in inv:
        counts[item_id] = counts.get(item_id, 0) + 1
    desc = "\n".join(f"{SHOP_ITEMS.get(k, {}).get('name', k)} × {v}" for k, v in counts.items())
    text = make_embed("🎒 Your Inventory", desc)
    client.reply_message(text, message)

def leaderboard(client, message, args, sender_jid):
    data = load_economy()
    sorted_users = sorted(data.items(), key=lambda x: x[1].get("balance", 0), reverse=True)[:10]
    if not sorted_users:
        client.reply_message(make_embed("💰 Leaderboard", "No data yet. Use `/daily` and `/work` to earn coins!"), message)
        return

    medals = ["🥇", "🥈", "🥉"] + ["🔹"] * 7
    lines = []
    for i, (uid, udata) in enumerate(sorted_users):
        name = uid.split('@')[0]
        lines.append(f"{medals[i]} *{name}* — `{udata.get('balance', 0):,} 🪙`")
    text = make_embed("💰 Coin Leaderboard", "\n".join(lines))
    client.reply_message(text, message)

def get_commands():
    return {
        "balance": balance,
        "daily": daily,
        "work": work,
        "pay": pay,
        "shop": shop,
        "buy": buy,
        "inventory": inventory,
        "leaderboard": leaderboard
    }
