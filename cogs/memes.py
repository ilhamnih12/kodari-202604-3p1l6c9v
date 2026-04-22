import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import random
from utils.helpers import make_embed

MEME_SUBREDDITS = ["memes", "dankmemes", "me_irl", "wholesomememes", "ProgrammerHumor"]

MEME_TEMPLATES = {
    "drake": ("Drake Approves/Disapproves", "drake_hotline_bling"),
    "distracted": ("Distracted Boyfriend", "distracted_boyfriend"),
    "two_buttons": ("Two Buttons", "two_buttons"),
    "expanding_brain": ("Expanding Brain", "expanding_brain"),
    "change_my_mind": ("Change My Mind", "change-my-mind"),
}

ROASTS = [
    "You're not stupid; you just have bad luck thinking.",
    "I'd agree with you but then we'd both be wrong.",
    "You have your entire life to be an idiot. Why not take today off?",
    "You're proof that evolution can go in reverse.",
    "If laughter is the best medicine, your face must be curing diseases.",
    "You're like a cloud. When you disappear, it's a beautiful day.",
    "I'd insult you, but nature already did a great job.",
    "You're not the dumbest person alive, but you better hope they don't die.",
    "Somewhere out there, a tree is working overtime producing oxygen for you.",
    "You have the right to remain silent because whatever you say will probably be dumb anyway.",
]

DARK_JOKES = [
    "Why don't scientists trust atoms? Because they make up everything.",
    "I told my doctor I broke my arm in two places. He told me to stop going to those places.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
    "Why don't eggs tell jokes? They'd crack each other up.",
    "I would tell you a joke about time travel, but you didn't like it.",
    "I asked the librarian if they had books about paranoia. She whispered: 'They're right behind you!'",
    "What did the ocean say to the beach? Nothing, it just waved.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
]

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="meme", description="Fetch a random meme from Reddit")
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        subreddit = random.choice(MEME_SUBREDDITS)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://www.reddit.com/r/{subreddit}/random.json?limit=1",
                    headers={"User-Agent": "FunBot/1.0"}
                ) as resp:
                    if resp.status != 200:
                        raise Exception("Reddit API error")
                    data = await resp.json()
                    post = data[0]["data"]["children"][0]["data"]
                    if post.get("over_18"):
                        await interaction.followup.send(embed=make_embed("⚠️ NSFW", "This meme was NSFW. Try again!", "warning"))
                        return
                    embed = make_embed(f"😂 r/{subreddit}", f"**{post['title']}**", "fun")
                    embed.set_image(url=post.get("url", ""))
                    embed.set_footer(text=f"👍 {post.get('ups', 0):,} upvotes • r/{subreddit}")
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", "Could not fetch a meme right now. Try again later!", "error"))

    @app_commands.command(name="meme_category", description="Get a meme from a specific subreddit")
    @app_commands.describe(category="Choose a meme category")
    @app_commands.choices(category=[
        app_commands.Choice(name="Classic Memes", value="memes"),
        app_commands.Choice(name="Dank Memes", value="dankmemes"),
        app_commands.Choice(name="Wholesome Memes", value="wholesomememes"),
        app_commands.Choice(name="Me IRL", value="me_irl"),
        app_commands.Choice(name="Programmer Humor", value="ProgrammerHumor"),
    ])
    async def meme_category(self, interaction: discord.Interaction, category: app_commands.Choice[str]):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://www.reddit.com/r/{category.value}/random.json?limit=1",
                    headers={"User-Agent": "FunBot/1.0"}
                ) as resp:
                    if resp.status != 200:
                        raise Exception("error")
                    data = await resp.json()
                    post = data[0]["data"]["children"][0]["data"]
                    if post.get("over_18"):
                        await interaction.followup.send(embed=make_embed("⚠️ NSFW", "NSFW meme filtered. Try again!", "warning"))
                        return
                    embed = make_embed(f"😂 r/{category.value}", f"**{post['title']}**", "fun")
                    embed.set_image(url=post.get("url", ""))
                    embed.set_footer(text=f"👍 {post.get('ups', 0):,} upvotes")
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", "Could not fetch meme. Try again!", "error"))

    @app_commands.command(name="roast", description="Get a roast for yourself or another user")
    @app_commands.describe(user="The user to roast (leave blank to roast yourself)")
    async def roast(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        roast_text = random.choice(ROASTS)
        embed = make_embed("🔥 Roast", f"{target.mention} — {roast_text}", "error")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="joke", description="Get a random programming or dad joke")
    async def joke(self, interaction: discord.Interaction):
        jokes = DARK_JOKES
        embed = make_embed("😄 Joke", random.choice(jokes), "fun")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="meme_top", description="Get a top meme from Reddit right now")
    @app_commands.describe(subreddit="Subreddit to pull from (default: memes)")
    async def meme_top(self, interaction: discord.Interaction, subreddit: str = "memes"):
        await interaction.response.defer()
        safe_sub = subreddit.strip().replace(" ", "")[:50]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://www.reddit.com/r/{safe_sub}/top.json?limit=10&t=day",
                    headers={"User-Agent": "FunBot/1.0"}
                ) as resp:
                    if resp.status != 200:
                        raise Exception("bad subreddit")
                    data = await resp.json()
                    posts = [p["data"] for p in data["data"]["children"] if not p["data"].get("over_18") and p["data"].get("url", "").endswith((".jpg", ".png", ".gif", ".jpeg", ".webp"))]
                    if not posts:
                        raise Exception("no posts")
                    post = random.choice(posts[:5])
                    embed = make_embed(f"🔝 Top Meme from r/{safe_sub}", f"**{post['title']}**", "gold")
                    embed.set_image(url=post["url"])
                    embed.set_footer(text=f"👍 {post.get('ups', 0):,} upvotes")
                    await interaction.followup.send(embed=embed)
        except Exception:
            await interaction.followup.send(embed=make_embed("Error", f"Could not fetch top memes from r/{safe_sub}.", "error"))

    @app_commands.command(name="meme_templates", description="List popular meme template names")
    async def meme_templates(self, interaction: discord.Interaction):
        desc = "\n".join(f"• **{name}** — `{key}`" for key, (name, _) in MEME_TEMPLATES.items())
        embed = make_embed("🖼️ Meme Templates", f"Popular meme formats:\n\n{desc}\n\n*More features coming soon!*", "info")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Memes(bot))