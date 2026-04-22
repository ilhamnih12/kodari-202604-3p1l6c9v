import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import make_embed

warnings_db = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_mod_perms(self, interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.manage_messages or interaction.user.guild_permissions.administrator

    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.describe(member="Member to kick", reason="Reason for kick")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(embed=make_embed("Error", "You cannot kick someone with an equal or higher role.", "error"), ephemeral=True)
            return
        try:
            await member.kick(reason=reason)
            embed = make_embed("👢 Member Kicked", f"**{member}** has been kicked.\n**Reason:** {reason}", "warning")
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(embed=make_embed("Error", "I don't have permission to kick that member.", "error"), ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.describe(member="Member to ban", reason="Reason for ban", delete_days="Days of messages to delete (0-7)")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided", delete_days: int = 0):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(embed=make_embed("Error", "You cannot ban someone with an equal or higher role.", "error"), ephemeral=True)
            return
        try:
            await member.ban(reason=reason, delete_message_days=min(delete_days, 7))
            embed = make_embed("🔨 Member Banned", f"**{member}** has been banned.\n**Reason:** {reason}", "error")
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(embed=make_embed("Error", "I don't have permission to ban that member.", "error"), ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user by their ID")
    @app_commands.describe(user_id="The ID of the user to unban")
    @app_commands.default_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            embed = make_embed("✅ User Unbanned", f"**{user}** has been unbanned.", "success")
            await interaction.response.send_message(embed=embed)
        except Exception:
            await interaction.response.send_message(embed=make_embed("Error", "Could not unban that user. Check the ID.", "error"), ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout (mute) a member temporarily")
    @app_commands.describe(member="Member to timeout", minutes="Timeout duration in minutes", reason="Reason")
    @app_commands.default_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int = 5, reason: str = "No reason provided"):
        import datetime
        if minutes < 1 or minutes > 40320:
            await interaction.response.send_message(embed=make_embed("Error", "Duration must be between 1 and 40320 minutes.", "error"), ephemeral=True)
            return
        try:
            until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
            await member.timeout(until, reason=reason)
            embed = make_embed("🔇 Member Timed Out", f"**{member}** has been timed out for **{minutes} minutes**.\n**Reason:** {reason}", "warning")
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(embed=make_embed("Error", "I don't have permission to timeout that member.", "error"), ephemeral=True)

    @app_commands.command(name="warn", description="Issue a warning to a member")
    @app_commands.describe(member="Member to warn", reason="Reason for the warning")
    @app_commands.default_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        uid = str(member.id)
        gid = str(interaction.guild.id)
        if gid not in warnings_db:
            warnings_db[gid] = {}
        if uid not in warnings_db[gid]:
            warnings_db[gid][uid] = []
        warnings_db[gid][uid].append({"reason": reason, "by": str(interaction.user)})
        count = len(warnings_db[gid][uid])
        embed = make_embed("⚠️ Warning Issued", f"**{member}** has been warned.\n**Reason:** {reason}\n**Total Warnings:** `{count}`", "warning")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warnings", description="View warnings for a member")
    @app_commands.describe(member="Member to check warnings for")
    @app_commands.default_permissions(manage_messages=True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        uid = str(member.id)
        gid = str(interaction.guild.id)
        warns = warnings_db.get(gid, {}).get(uid, [])
        if not warns:
            await interaction.response.send_message(embed=make_embed("⚠️ Warnings", f"**{member}** has no warnings.", "success"))
            return
        lines = [f"`{i+1}.` {w['reason']} — by {w['by']}" for i, w in enumerate(warns)]
        embed = make_embed(f"⚠️ Warnings for {member}", "\n".join(lines), "warning")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clearwarns", description="Clear all warnings for a member")
    @app_commands.describe(member="Member to clear warnings for")
    @app_commands.default_permissions(administrator=True)
    async def clearwarns(self, interaction: discord.Interaction, member: discord.Member):
        uid = str(member.id)
        gid = str(interaction.guild.id)
        if gid in warnings_db and uid in warnings_db[gid]:
            del warnings_db[gid][uid]
        embed = make_embed("✅ Warnings Cleared", f"All warnings for **{member}** have been removed.", "success")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="purge", description="Delete multiple messages at once")
    @app_commands.describe(amount="Number of messages to delete (1-100)")
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message(embed=make_embed("Error", "Amount must be between 1 and 100.", "error"), ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(embed=make_embed("🗑️ Messages Purged", f"Successfully deleted **{len(deleted)}** messages.", "success"), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))