import discord
from discord import app_commands
from discord.ext import commands
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

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Check your or another user's coin balance")
    @app_commands.describe(user="User to check (leave blank for yourself)")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        data = get_balance(target.id)
        embed = make_embed(
            f"💰 {target.display_name}'s Balance",
            f"**Coins:** `{data['balance']:,} 🪙`\n**Items:** `{len(data.get('inventory', []))}` items in inventory",
            "gold"
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="Claim your daily coin reward")
    async def daily(self, interaction: discord.Interaction):
        data = get_balance(interaction.user.id)
        now = datetime.utcnow()
        last = data.get("last_daily")
        if last:
            last_dt = datetime.fromisoformat(last)
            diff = now - last_dt
            if diff < timedelta(hours=24):
                remaining = timedelta(hours=24) - diff
                hrs, rem = divmod(int(remaining.total_seconds()), 3600)
                mins = rem // 60
                await interaction.response.send_message(
                    embed=make_embed("⏰ Daily Reward", f"You already claimed today's reward!\nCome back in **{hrs}h {mins}m**.", "warning"),
                    ephemeral=True
                )
                return
        new_balance = data["balance"] + DAILY_AMOUNT
        update_user(interaction.user.id, {"balance": new_balance, "last_daily": now.isoformat()})
        embed = make_embed("🎁 Daily Reward", f"You claimed your daily **{DAILY_AMOUNT:,} 🪙**!\n\n💰 **New Balance:** `{new_balance:,} 🪙`", "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="work", description="Work to earn some coins")
    async def work(self, interaction: discord.Interaction):
        job, low, high = random.choice(WORK_JOBS)
        earned = random.randint(low, high)
        data = get_balance(interaction.user.id)
        new_balance = data["balance"] + earned
        update_user(interaction.user.id, {"balance": new_balance})
        embed = make_embed("💼 Work", f"You {job} and earned **{earned} 🪙**!\n\n💰 **New Balance:** `{new_balance:,} 🪙`", "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pay", description="Send coins to another user")
    @app_commands.describe(user="Who to pay", amount="Amount to send")
    async def pay(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if user.id == interaction.user.id:
            await interaction.response.send_message(embed=make_embed("Error", "You can't pay yourself!", "error"), ephemeral=True)
            return
        if amount <= 0:
            await interaction.response.send_message(embed=make_embed("Error", "Amount must be positive.", "error"), ephemeral=True)
            return
        sender = get_balance(interaction.user.id)
        if sender["balance"] < amount:
            await interaction.response.send_message(embed=make_embed("Error", f"Insufficient funds. You have `{sender['balance']:,} 🪙`.", "error"), ephemeral=True)
            return
        receiver = get_balance(user.id)
        update_user(interaction.user.id, {"balance": sender["balance"] - amount})
        update_user(user.id, {"balance": receiver["balance"] + amount})
        embed = make_embed("💸 Payment Sent", f"You sent **{amount:,} 🪙** to {user.mention}!\n\n💰 **Your new balance:** `{sender['balance'] - amount:,} 🪙`", "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shop", description="View the item shop")
    async def shop(self, interaction: discord.Interaction):
        desc = "\n".join(f"**{v['name']}** — `{v['price']:,} 🪙`\n{v['desc']}\n" for v in SHOP_ITEMS.values())
        embed = make_embed("🛒 Item Shop", desc, "gold")
        embed.set_footer(text="Use /buy <item_id> to purchase!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Buy an item from the shop")
    @app_commands.describe(item_id="Item ID (lucky_charm, vip_badge, golden_dice, mystery_box, crown)")
    async def buy(self, interaction: discord.Interaction, item_id: str):
        item = SHOP_ITEMS.get(item_id.lower())
        if not item:
            await interaction.response.send_message(embed=make_embed("Error", f"Item `{item_id}` not found. Use `/shop` to see available items.", "error"), ephemeral=True)
            return
        data = get_balance(interaction.user.id)
        if data["balance"] < item["price"]:
            await interaction.response.send_message(embed=make_embed("Error", f"You need `{item['price']:,} 🪙` but only have `{data['balance']:,} 🪙`.", "error"), ephemeral=True)
            return
        new_balance = data["balance"] - item["price"]
        inventory = data.get("inventory", [])
        inventory.append(item_id)
        update_user(interaction.user.id, {"balance": new_balance, "inventory": inventory})
        embed = make_embed("✅ Purchase Successful", f"You bought **{item['name']}** for `{item['price']:,} 🪙`!\n\n💰 **New Balance:** `{new_balance:,} 🪙`", "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory", description="View your purchased items")
    async def inventory(self, interaction: discord.Interaction):
        data = get_balance(interaction.user.id)
        inv = data.get("inventory", [])
        if not inv:
            await interaction.response.send_message(embed=make_embed("🎒 Inventory", "Your inventory is empty! Use `/shop` to buy items.", "warning"))
            return
        counts = {}
        for item_id in inv:
            counts[item_id] = counts.get(item_id, 0) + 1
        desc = "\n".join(f"{SHOP_ITEMS.get(k, {}).get('name', k)} × {v}" for k, v in counts.items())
        embed = make_embed("🎒 Your Inventory", desc, "gold")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="View the richest users on the server")
    async def leaderboard(self, interaction: discord.Interaction):
        data = load_economy()
        sorted_users = sorted(data.items(), key=lambda x: x[1].get("balance", 0), reverse=True)[:10]
        if not sorted_users:
            await interaction.response.send_message(embed=make_embed("💰 Leaderboard", "No data yet. Use `/daily` and `/work` to earn coins!", "warning"))
            return
        medals = ["🥇", "🥈", "🥉"] + ["🔹"] * 7
        lines = []
        for i, (uid, udata) in enumerate(sorted_users):
            try:
                user = await interaction.client.fetch_user(int(uid))
                name = user.display_name
            except Exception:
                name = f"User#{uid[:4]}"
            lines.append(f"{medals[i]} **{name}** — `{udata.get('balance', 0):,} 🪙`")
        embed = make_embed("💰 Coin Leaderboard", "\n".join(lines), "gold")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))