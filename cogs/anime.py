import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import random
from utils.helpers import make_embed

WAIFU_CATEGORIES = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "kiss", "pat", "smug", "bonk", "blush", "smile", "wave", "poke", "dance", "cringe"]
SFW_CATEGORIES = ["waifu", "neko", "shinobu", "megumin"]

ANIME_QUOTES = [
    ("A dropout will beat a genius through hard work.", "Rock Lee, Naruto"),
    ("Whatever you lose, you'll find it again. But what you throw away you'll never get back.", "Himura Kenshin, Rurouni Kenshin"),
    ("The world isn't perfect. But it's there for us, doing the best it can.", "Roy Mustang, FMA"),
    ("People's lives don't end when they die. It ends when they lose faith.", "Itachi Uchiha, Naruto"),
    ("Hard work is worthless for those that don't believe in themselves.", "Naruto Uzumaki, Naruto"),
    ("If you don't take risks, you can't create a future.", "Monkey D. Luffy, One Piece"),
    ("There will always be people who can't understand until they experience something themselves.", "Levi Ackerman, AoT"),
    ("I am the hope of the universe. I am the answer to all living things that cry out for peace.", "Goku, Dragon Ball Z"),
    ("Even if I'm worthless and carry demon blood... I want to be the best person I can be.", "Inuyasha"),
    ("Don't give up, there's no shame in falling down! True shame is to not stand up again!", "Shintaro Midorima, KnB"),
]

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="waifu", description="Get a random waifu image")
    async def waifu(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/sfw/waifu") as resp:
                    data = await resp.json()
                    embed = make_embed("🌸 Random Waifu", "", "fun")
                    embed.set_image(url=data["url"])
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", "Could not fetch waifu image. Try again!", "error"))

    @app_commands.command(name="neko", description="Get a random neko (cat girl) image")
    async def neko(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/sfw/neko") as resp:
                    data = await resp.json()
                    embed = make_embed("🐱 Neko", "", "fun")
                    embed.set_image(url=data["url"])
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", "Could not fetch neko image.", "error"))

    @app_commands.command(name="anime_action", description="Get an anime action GIF")
    @app_commands.describe(action="Type of anime action")
    @app_commands.choices(action=[
        app_commands.Choice(name="Hug 🤗", value="hug"),
        app_commands.Choice(name="Kiss 💋", value="kiss"),
        app_commands.Choice(name="Pat 🫶", value="pat"),
        app_commands.Choice(name="Bonk 🔨", value="bonk"),
        app_commands.Choice(name="Smug 😏", value="smug"),
        app_commands.Choice(name="Cry 😢", value="cry"),
        app_commands.Choice(name="Dance 💃", value="dance"),
        app_commands.Choice(name="Poke 👉", value="poke"),
        app_commands.Choice(name="Blush 😊", value="blush"),
        app_commands.Choice(name="Wave 👋", value="wave"),
    ])
    async def anime_action(self, interaction: discord.Interaction, action: app_commands.Choice[str]):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.waifu.pics/sfw/{action.value}") as resp:
                    data = await resp.json()
                    action_labels = {"hug": "🤗 Anime Hug", "kiss": "💋 Anime Kiss", "pat": "🫶 Anime Pat",
                                     "bonk": "🔨 Anime Bonk", "smug": "😏 Smug", "cry": "😢 Anime Cry",
                                     "dance": "💃 Anime Dance", "poke": "👉 Anime Poke",
                                     "blush": "😊 Blushing", "wave": "👋 Anime Wave"}
                    embed = make_embed(action_labels.get(action.value, action.value), "", "fun")
                    embed.set_image(url=data["url"])
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", "Could not fetch GIF. Try again!", "error"))

    @app_commands.command(name="anime_quote", description="Get a random iconic anime quote")
    async def anime_quote(self, interaction: discord.Interaction):
        quote, source = random.choice(ANIME_QUOTES)
        embed = make_embed("📜 Anime Quote", f"*\"{quote}\"*\n\n— **{source}**", "primary")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shinobu", description="Get a Shinobu image")
    async def shinobu(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/sfw/shinobu") as resp:
                    data = await resp.json()
                    embed = make_embed("🦋 Shinobu", "", "fun")
                    embed.set_image(url=data["url"])
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", "Could not fetch image.", "error"))

    @app_commands.command(name="megumin", description="Get a Megumin image")
    async def megumin(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/sfw/megumin") as resp:
                    data = await resp.json()
                    embed = make_embed("💥 Megumin", "", "fun")
                    embed.set_image(url=data["url"])
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", "Could not fetch image.", "error"))

    @app_commands.command(name="anime_search", description="Search for an anime by name (via Jikan API)")
    @app_commands.describe(title="Anime title to search for")
    async def anime_search(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.jikan.moe/v4/anime?q={title}&limit=1") as resp:
                    data = await resp.json()
                    anime = data["data"][0]
                    embed = make_embed(anime["title"], anime.get("synopsis", "No synopsis available.")[:500] + "...", "primary")
                    embed.add_field(name="⭐ Score", value=str(anime.get("score", "N/A")))
                    embed.add_field(name="📺 Episodes", value=str(anime.get("episodes", "N/A")))
                    embed.add_field(name="📊 Status", value=anime.get("status", "N/A"))
                    embed.add_field(name="🎭 Genre", value=", ".join(g["name"] for g in anime.get("genres", [])[:3]) or "N/A")
                    embed.set_thumbnail(url=anime["images"]["jpg"]["image_url"])
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", f"No anime found for `{title}`.", "error"))

async def setup(bot):
    await bot.add_cog(Anime(bot))