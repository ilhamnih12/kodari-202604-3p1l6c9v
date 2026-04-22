import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
from utils.helpers import make_embed, load_trivia, COLORS

active_trivia = {}

class TriviaAnswerView(discord.ui.View):
    def __init__(self, correct: str, options: list, user_id: int):
        super().__init__(timeout=30)
        self.correct = correct
        self.user_id = user_id
        self.answered = False
        styles = [discord.ButtonStyle.blurple, discord.ButtonStyle.green,
                  discord.ButtonStyle.red, discord.ButtonStyle.grey]
        for i, opt in enumerate(options):
            btn = discord.ui.Button(label=opt, style=styles[i % len(styles)], custom_id=f"trivia_{i}")
            btn.callback = self.make_callback(opt)
            self.add_item(btn)

    def make_callback(self, option):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This is not your trivia question!", ephemeral=True)
                return
            if self.answered:
                await interaction.response.send_message("Already answered!", ephemeral=True)
                return
            self.answered = True
            self.stop()
            correct = option == self.correct
            for child in self.children:
                child.disabled = True
                if child.label == self.correct:
                    child.style = discord.ButtonStyle.green
                elif child.label == option and not correct:
                    child.style = discord.ButtonStyle.red
            result = f"✅ **Correct!** Well done!" if correct else f"❌ **Wrong!** The correct answer was **{self.correct}**."
            embed = make_embed("🧠 Trivia", result, "success" if correct else "error")
            await interaction.response.edit_message(embed=embed, view=self)
        return callback

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = load_trivia()

    def get_random(self, category=None):
        pool = [q for q in self.questions if not category or q["category"].lower() == category.lower()]
        return random.choice(pool) if pool else None

    @app_commands.command(name="trivia", description="Answer a random trivia question")
    async def trivia(self, interaction: discord.Interaction):
        q = self.get_random()
        options = q["options"][:]
        random.shuffle(options)
        embed = make_embed(
            f"🧠 Trivia — {q['category']}",
            f"**{q['question']}**\n\nSelect your answer below:",
            "info"
        )
        view = TriviaAnswerView(q["answer"], options, interaction.user.id)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="trivia_category", description="Answer a trivia question from a specific category")
    @app_commands.describe(category="Category: Geography, Science, History, Math, Literature, Technology, Animals, Art, Food, Biology, Language")
    async def trivia_category(self, interaction: discord.Interaction, category: str):
        q = self.get_random(category)
        if not q:
            await interaction.response.send_message(embed=make_embed("Error", f"No questions found for category **{category}**.", "error"), ephemeral=True)
            return
        options = q["options"][:]
        random.shuffle(options)
        embed = make_embed(f"🧠 Trivia — {q['category']}", f"**{q['question']}**\n\nSelect your answer below:", "info")
        view = TriviaAnswerView(q["answer"], options, interaction.user.id)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="trivia_streak", description="Start a trivia streak — answer 5 questions in a row!")
    async def trivia_streak(self, interaction: discord.Interaction):
        uid = interaction.user.id
        if uid in active_trivia:
            await interaction.response.send_message(embed=make_embed("Error", "You already have an active streak game!", "error"), ephemeral=True)
            return
        active_trivia[uid] = {"score": 0, "round": 1, "total": 5}
        q = self.get_random()
        options = q["options"][:]
        random.shuffle(options)
        embed = make_embed(
            f"🧠 Streak Trivia — Round 1/5",
            f"**{q['question']}**\n\nAnswer correctly to continue your streak!",
            "info"
        )
        await interaction.response.send_message(embed=embed, view=StreakView(q["answer"], options, interaction.user.id, self, active_trivia))

    @app_commands.command(name="trivia_scores", description="View your trivia stats")
    async def trivia_scores(self, interaction: discord.Interaction):
        embed = make_embed(
            "🏆 Trivia Leaderboard",
            "Use `/trivia` and `/trivia_streak` to earn points and compete!\n\n*Full leaderboard coming soon — keep playing!*",
            "gold"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="trivia_categories", description="List all available trivia categories")
    async def trivia_categories(self, interaction: discord.Interaction):
        categories = sorted(set(q["category"] for q in self.questions))
        desc = "\n".join(f"• **{c}**" for c in categories)
        embed = make_embed("🧠 Trivia Categories", desc, "info")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quickfire", description="Answer a trivia question without buttons — type your answer!")
    async def quickfire(self, interaction: discord.Interaction):
        q = self.get_random()
        embed = make_embed("⚡ Quick Fire Trivia", f"**{q['question']}**\n\nType your answer in chat! You have **15 seconds**.", "warning")
        await interaction.response.send_message(embed=embed)
        def check(m):
            return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id
        try:
            msg = await self.bot.wait_for("message", timeout=15.0, check=check)
            if msg.content.strip().lower() == q["answer"].lower():
                await msg.reply(embed=make_embed("⚡ Quick Fire", f"✅ **Correct!** Great job!", "success"))
            else:
                await msg.reply(embed=make_embed("⚡ Quick Fire", f"❌ **Wrong!** The answer was **{q['answer']}**.", "error"))
        except asyncio.TimeoutError:
            await interaction.followup.send(embed=make_embed("⚡ Quick Fire", f"⏰ **Time's up!** The answer was **{q['answer']}**.", "error"))

class StreakView(discord.ui.View):
    def __init__(self, correct, options, user_id, cog, active_trivia_ref):
        super().__init__(timeout=30)
        self.correct = correct
        self.user_id = user_id
        self.cog = cog
        self.active_trivia_ref = active_trivia_ref
        styles = [discord.ButtonStyle.blurple, discord.ButtonStyle.green,
                  discord.ButtonStyle.red, discord.ButtonStyle.grey]
        for i, opt in enumerate(options):
            btn = discord.ui.Button(label=opt, style=styles[i % len(styles)])
            btn.callback = self.make_callback(opt)
            self.add_item(btn)

    def make_callback(self, option):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("Not your game!", ephemeral=True)
                return
            self.stop()
            for child in self.children:
                child.disabled = True
            uid = self.user_id
            game = self.active_trivia_ref.get(uid)
            if not game:
                return
            correct = option == self.correct
            if correct:
                game["score"] += 1
            if not correct or game["round"] >= game["total"]:
                del self.active_trivia_ref[uid]
                if correct:
                    embed = make_embed("🧠 Streak Complete!", f"🏆 You completed the streak with **{game['score']}/{game['total']}** correct!", "gold")
                else:
                    embed = make_embed("🧠 Streak Ended", f"❌ Wrong! The answer was **{self.correct}**.\nFinal score: **{game['score']}/{game['total']}**", "error")
                await interaction.response.edit_message(embed=embed, view=self)
            else:
                game["round"] += 1
                q = self.cog.get_random()
                opts = q["options"][:]
                random.shuffle(opts)
                embed = make_embed(
                    f"🧠 Streak Trivia — Round {game['round']}/{game['total']}",
                    f"✅ Correct! Keep going!\n\n**{q['question']}**",
                    "info"
                )
                await interaction.response.edit_message(embed=embed, view=StreakView(q["answer"], opts, self.user_id, self.cog, self.active_trivia_ref))
        return callback

async def setup(bot):
    await bot.add_cog(Trivia(bot))