import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
log = logging.getLogger("FunBot")

COGS = [
    "cogs.games",
    "cogs.trivia",
    "cogs.memes",
    "cogs.fun",
    "cogs.economy",
    "cogs.utility",
    "cogs.moderation",
    "cogs.social",
    "cogs.math",
    "cogs.anime",
    "cogs.menu",
]

class FunBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        for cog in COGS:
            try:
                await self.load_extension(cog)
                log.info(f"Loaded cog: {cog}")
            except Exception as e:
                log.error(f"Failed to load cog {cog}: {e}")
        synced = await self.tree.sync()
        log.info(f"Synced {len(synced)} slash commands.")

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="/menu for commands"
            )
        )
        log.info(f"Logged in as {self.user} ({self.user.id})")

    async def on_command_error(self, ctx, error):
        log.error(f"Command error: {error}")

bot = FunBot()
bot.run(os.getenv("DISCORD_TOKEN"))