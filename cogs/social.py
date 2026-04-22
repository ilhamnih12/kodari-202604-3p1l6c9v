import discord
from discord import app_commands
from discord.ext import commands
import random
from utils.helpers import make_embed

SOCIAL_GIFS = {
    "hug": [
        "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
        "https://media.giphy.com/media/3M4NpbLCTxBqU/giphy.gif",
    ],
    "kiss": [
        "https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif",
        "https://media.giphy.com/media/bGm9FEBjB5oX6/giphy.gif",
    ],
    "slap": [
        "https://media.giphy.com/media/xUO4t2gkziBtki2q2U/giphy.gif",
        "https://media.giphy.com/media/cEYFeE4wJ6jdDVBiiIM/giphy.gif",
    ],
    "pat": [
        "https://media.giphy.com/media/5tmRHwTlHAZB/giphy.gif",
        "https://media.giphy.com/media/ARSp9T7wwxNcs/giphy.gif",
    ],
    "poke": [
        "https://media.giphy.com/media/WvVzZ9mCyMjsc/giphy.gif",
        "https://media.giphy.com/media/WvJRPbPxY3i8o/giphy.gif",
    ],
    "highfive": [
        "https://media.giphy.com/media/2Y9OFE20RBHmwSoFnX/giphy.gif",
        "https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif",
    ],
    "wave": [
        "https://media.giphy.com/media/Zb8bZUdrOP7P/giphy.gif",
        "https://media.giphy.com/media/IThjAlJnD9WNO/giphy.gif",
    ],
}

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def social_embed(self, action: str, emoji: str, sender: discord.Member, receiver: discord.Member, color="fun") -> discord.Embed:
        embed = make_embed(f"{emoji} {action}", f"**{sender.display_name}** {action.lower()}s **{receiver.display_name}**!", color)
        gif = random.choice(SOCIAL_GIFS.get(action.lower(), []))
        if gif:
            embed.set_image(url=gif)
        return embed

    @app_commands.command(name="hug", description="Give someone a warm hug!")
    @app_commands.describe(user="Who to hug")
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.social_embed("Hug", "🤗", interaction.user, user, "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kiss", description="Give someone a kiss!")
    @app_commands.describe(user="Who to kiss")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.social_embed("Kiss", "💋", interaction.user, user, "fun")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="slap", description="Slap someone!")
    @app_commands.describe(user="Who to slap")
    async def slap(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.social_embed("Slap", "👋", interaction.user, user, "error")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pat", description="Give someone a headpat!")
    @app_commands.describe(user="Who to pat")
    async def pat(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.social_embed("Pat", "🫶", interaction.user, user, "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="poke", description="Poke someone!")
    @app_commands.describe(user="Who to poke")
    async def poke(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.social_embed("Poke", "👉", interaction.user, user, "warning")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="highfive", description="High five someone!")
    @app_commands.describe(user="Who to high five")
    async def highfive(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.social_embed("Highfive", "🙌", interaction.user, user, "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="wave", description="Wave at someone!")
    @app_commands.describe(user="Who to wave at")
    async def wave(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.social_embed("Wave", "👋", interaction.user, user, "info")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ship", description="Check the compatibility between two users!")
    @app_commands.describe(user1="First user", user2="Second user")
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
        seed = user1.id + user2.id
        random.seed(seed)
        score = random.randint(0, 100)
        random.seed()
        bar_filled = round(score / 10)
        bar = "❤️" * bar_filled + "🖤" * (10 - bar_filled)
        if score >= 90:
            comment = "💍 Soulmates! A match made in heaven!"
        elif score >= 70:
            comment = "💕 Great couple! Very compatible!"
        elif score >= 50:
            comment = "💛 Pretty good! Give it a shot!"
        elif score >= 30:
            comment = "🤷 Eh... could go either way."
        else:
            comment = "💔 Not the best match..."
        name1 = user1.display_name[:len(user1.display_name)//2]
        name2 = user2.display_name[len(user2.display_name)//2:]
        ship_name = name1 + name2
        embed = make_embed(f"💘 Ship: {ship_name}", f"{user1.mention} + {user2.mention}\n\n{bar}\n\n**{score}% compatible**\n{comment}", "fun")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="compliment", description="Send a compliment to someone!")
    @app_commands.describe(user="Who to compliment")
    async def compliment(self, interaction: discord.Interaction, user: discord.Member):
        compliments = [
            "You light up every room you walk into! ✨",
            "Your kindness is truly contagious! 💛",
            "You have an amazing sense of humor! 😄",
            "You're incredibly talented and it shows! 🌟",
            "The world is a better place with you in it! 🌍",
            "You always know how to make people smile! 😊",
            "Your creativity is absolutely inspiring! 🎨",
            "You're one of the most genuine people around! 💎",
        ]
        embed = make_embed("💌 Compliment", f"{user.mention} — {random.choice(compliments)}\n\n*From {interaction.user.display_name} with love* 💝", "success")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Social(bot))