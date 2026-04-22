import discord
from discord import app_commands
from discord.ext import commands
import platform
import time
from utils.helpers import make_embed

START_TIME = time.time()

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        color = "success" if latency < 100 else ("warning" if latency < 200 else "error")
        emoji = "🟢" if latency < 100 else ("🟡" if latency < 200 else "🔴")
        embed = make_embed("🏓 Pong!", f"{emoji} **Latency:** `{latency}ms`", color)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Get detailed information about this server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message(embed=make_embed("Error", "This command must be used in a server.", "error"), ephemeral=True)
            return
        bots = sum(1 for m in guild.members if m.bot)
        humans = guild.member_count - bots
        embed = make_embed(f"🏠 {guild.name}", f"**Owner:** {guild.owner.mention if guild.owner else 'Unknown'}", "info")
        embed.add_field(name="👥 Members", value=f"Humans: `{humans}`\nBots: `{bots}`\nTotal: `{guild.member_count}`")
        embed.add_field(name="💬 Channels", value=f"Text: `{len(guild.text_channels)}`\nVoice: `{len(guild.voice_channels)}`\nCategories: `{len(guild.categories)}`")
        embed.add_field(name="📊 Stats", value=f"Roles: `{len(guild.roles)}`\nEmojis: `{len(guild.emojis)}`\nBoosts: `{guild.premium_subscription_count}`")
        embed.add_field(name="📅 Created", value=f"<t:{int(guild.created_at.timestamp())}:F>", inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Get information about a user")
    @app_commands.describe(user="The user to look up (leave blank for yourself)")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        roles = [r.mention for r in target.roles if r.name != "@everyone"]
        embed = make_embed(f"👤 {target.display_name}", "", "primary")
        embed.add_field(name="🆔 User ID", value=f"`{target.id}`")
        embed.add_field(name="🏷️ Tag", value=f"`{target}`")
        embed.add_field(name="🤖 Bot?", value="Yes" if target.bot else "No")
        embed.add_field(name="📅 Joined Server", value=f"<t:{int(target.joined_at.timestamp())}:R>" if target.joined_at else "Unknown")
        embed.add_field(name="📅 Account Created", value=f"<t:{int(target.created_at.timestamp())}:R>")
        embed.add_field(name=f"🎭 Roles ({len(roles)})", value=" ".join(roles[:10]) if roles else "None", inline=False)
        embed.set_thumbnail(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Get a user's full-size avatar")
    @app_commands.describe(user="User to get avatar for (leave blank for yourself)")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        embed = make_embed(f"🖼️ {target.display_name}'s Avatar", "", "primary")
        embed.set_image(url=target.display_avatar.url)
        embed.add_field(name="Download", value=f"[PNG]({target.display_avatar.with_format('png').url}) | [WEBP]({target.display_avatar.with_format('webp').url})")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="uptime", description="Check how long the bot has been running")
    async def uptime(self, interaction: discord.Interaction):
        elapsed = int(time.time() - START_TIME)
        days, rem = divmod(elapsed, 86400)
        hrs, rem = divmod(rem, 3600)
        mins, secs = divmod(rem, 60)
        embed = make_embed("⏰ Bot Uptime", f"**{days}d {hrs}h {mins}m {secs}s**\n\nRunning on Python `{platform.python_version()}` | discord.py", "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="poll", description="Create a simple yes/no or multi-option poll")
    @app_commands.describe(question="The poll question", options="Comma-separated options (leave blank for Yes/No)")
    async def poll(self, interaction: discord.Interaction, question: str, options: str = None):
        if options:
            choices = [o.strip() for o in options.split(",") if o.strip()][:9]
            if len(choices) < 2:
                await interaction.response.send_message(embed=make_embed("Error", "Provide at least 2 options.", "error"), ephemeral=True)
                return
            number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
            desc = "\n".join(f"{number_emojis[i]} {c}" for i, c in enumerate(choices))
            embed = make_embed(f"📊 Poll", f"**{question}**\n\n{desc}", "primary")
            embed.set_footer(text=f"Poll by {interaction.user.display_name}")
            await interaction.response.send_message(embed=embed)
            msg = await interaction.original_response()
            for i in range(len(choices)):
                await msg.add_reaction(number_emojis[i])
        else:
            embed = make_embed(f"📊 Poll", f"**{question}**", "primary")
            embed.set_footer(text=f"Poll by {interaction.user.display_name}")
            await interaction.response.send_message(embed=embed)
            msg = await interaction.original_response()
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

    @app_commands.command(name="botinfo", description="View information about FunBot")
    async def botinfo(self, interaction: discord.Interaction):
        embed = make_embed("🤖 FunBot Info", "A feature-rich Discord bot with 10+ categories of slash commands!", "primary")
        embed.add_field(name="📂 Categories", value="`10` command categories")
        embed.add_field(name="⌨️ Commands", value="`60+` slash commands")
        embed.add_field(name="🏠 Servers", value=f"`{len(self.bot.guilds):,}`")
        embed.add_field(name="👥 Users", value=f"`{sum(g.member_count for g in self.bot.guilds):,}`")
        embed.add_field(name="⚙️ Framework", value="discord.py 2.x")
        embed.add_field(name="🐍 Python", value=f"{platform.python_version()}")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url if self.bot.user else discord.Embed.Empty)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))