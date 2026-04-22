import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from utils.helpers import make_embed, load_feedback, save_feedback, CATEGORY_EMOJIS, COLORS

COMMAND_DATA = {
    "🎮 Games": {
        "description": "Interactive games to play solo or challenge friends",
        "commands": [
            ("/rps", "Play Rock Paper Scissors against the bot"),
            ("/coinflip", "Flip a coin and guess the result"),
            ("/dice", "Roll one or more dice with customizable sides"),
            ("/slots", "Spin the slot machine for prizes!"),
            ("/blackjack", "Play Blackjack against the dealer"),
            ("/numberguess", "Guess the secret number (1–100)"),
            ("/wouldyourather", "React-based Would You Rather question"),
        ],
    },
    "🧠 Trivia": {
        "description": "Test your knowledge across many categories",
        "commands": [
            ("/trivia", "Answer a random multiple-choice trivia question"),
            ("/trivia_category", "Trivia from a specific category"),
            ("/trivia_streak", "5-question streak challenge"),
            ("/quickfire", "Type your answer in 15 seconds"),
            ("/trivia_categories", "List all trivia categories"),
            ("/trivia_scores", "View trivia leaderboard"),
        ],
    },
    "😂 Memes": {
        "description": "Fetch memes, jokes, and roasts",
        "commands": [
            ("/meme", "Fetch a random meme from Reddit"),
            ("/meme_category", "Get a meme from a specific subreddit"),
            ("/meme_top", "Get a top meme from Reddit today"),
            ("/roast", "Roast yourself or another user"),
            ("/joke", "Get a random joke"),
            ("/meme_templates", "List popular meme templates"),
        ],
    },
    "🎉 Fun": {
        "description": "Lighthearted fun commands for everyone",
        "commands": [
            ("/8ball", "Ask the magic 8-ball a yes/no question"),
            ("/fact", "Get a random interesting fact"),
            ("/quote", "Get an inspirational quote"),
            ("/tongue_twister", "Get a tongue twister challenge"),
            ("/pickone", "Let the bot choose between your options"),
            ("/reverse", "Reverse any text"),
            ("/rate", "Rate anything out of 10"),
            ("/countdown", "Start a countdown timer"),
        ],
    },
    "💰 Economy": {
        "description": "Earn, spend, and manage your virtual coins",
        "commands": [
            ("/balance", "Check your coin balance"),
            ("/daily", "Claim your daily 200 🪙 reward"),
            ("/work", "Work to earn coins"),
            ("/pay", "Send coins to another user"),
            ("/shop", "View the item shop"),
            ("/buy", "Purchase an item from the shop"),
            ("/inventory", "View your purchased items"),
            ("/leaderboard", "See the richest users"),
        ],
    },
    "🔧 Utility": {
        "description": "Helpful server and user tools",
        "commands": [
            ("/ping", "Check the bot's latency"),
            ("/serverinfo", "View server details"),
            ("/userinfo", "View user details"),
            ("/avatar", "Get a user's full-size avatar"),
            ("/uptime", "Check bot uptime"),
            ("/poll", "Create a yes/no or multi-option poll"),
            ("/botinfo", "View FunBot stats"),
        ],
    },
    "🛡️ Moderation": {
        "description": "Server moderation tools for staff",
        "commands": [
            ("/kick", "Kick a member from the server"),
            ("/ban", "Ban a member from the server"),
            ("/unban", "Unban a user by ID"),
            ("/timeout", "Temporarily mute a member"),
            ("/warn", "Issue a warning to a member"),
            ("/warnings", "View a member's warnings"),
            ("/clearwarns", "Clear all warnings for a member"),
            ("/purge", "Delete multiple messages at once"),
        ],
    },
    "💞 Social": {
        "description": "Express yourself and interact with others",
        "commands": [
            ("/hug", "Give someone a warm hug"),
            ("/kiss", "Give someone a kiss"),
            ("/slap", "Slap someone"),
            ("/pat", "Give someone a headpat"),
            ("/poke", "Poke someone"),
            ("/highfive", "High five someone"),
            ("/wave", "Wave at someone"),
            ("/ship", "Check compatibility between two users"),
            ("/compliment", "Send a compliment to someone"),
        ],
    },
    "📐 Math": {
        "description": "Math calculations and unit conversions",
        "commands": [
            ("/calculate", "Evaluate a math expression"),
            ("/random_number", "Generate a random number in a range"),
            ("/percentage", "Calculate X% of a number"),
            ("/factor", "Prime factorization of a number"),
            ("/fibonacci", "Generate Fibonacci sequence"),
            ("/convert", "Convert between units (temp, distance, weight)"),
            ("/bmi", "Calculate your Body Mass Index"),
        ],
    },
    "🌸 Anime": {
        "description": "Anime images, GIFs, quotes, and search",
        "commands": [
            ("/waifu", "Get a random waifu image"),
            ("/neko", "Get a random neko image"),
            ("/anime_action", "Get an anime action GIF"),
            ("/anime_quote", "Get a random iconic anime quote"),
            ("/shinobu", "Get a Shinobu image"),
            ("/megumin", "Get a Megumin image"),
            ("/anime_search", "Search for an anime by title"),
        ],
    },
}

class CategorySelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        options = [
            discord.SelectOption(label=cat.split(" ", 1)[1], emoji=cat.split(" ", 1)[0], description=info["description"][:50], value=cat)
            for cat, info in COMMAND_DATA.items()
        ]
        select = discord.ui.Select(placeholder="📂 Choose a category to explore...", options=options)
        select.callback = self.on_select
        self.add_item(select)
        self.selected_category = None

    async def on_select(self, interaction: discord.Interaction):
        cat = interaction.data["values"][0]
        info = COMMAND_DATA[cat]
        desc = "\n".join(f"• `{cmd}` — {desc}" for cmd, desc in info["commands"])
        embed = make_embed(f"{cat} Commands", f"*{info['description']}*\n\n{desc}", "primary")
        embed.set_footer(text="Use /help <command> for detailed usage examples!")
        await interaction.response.edit_message(embed=embed, view=self)

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="menu", description="View all bot commands organized by category")
    async def menu(self, interaction: discord.Interaction):
        total = sum(len(v["commands"]) for v in COMMAND_DATA.values())
        categories = len(COMMAND_DATA)
        lines = [f"{cat} — `{len(info['commands'])} commands`" for cat, info in COMMAND_DATA.items()]
        desc = (
            f"Welcome to **FunBot**! 🎉\n"
            f"**{categories} categories** | **{total} commands**\n\n"
            + "\n".join(lines)
            + "\n\n📂 **Use the dropdown below to explore each category!**"
        )
        embed = make_embed("📋 FunBot — Command Menu", desc, "primary")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url if self.bot.user else discord.Embed.Empty)
        embed.set_footer(text="Use /help <command> for detailed descriptions and examples!")
        await interaction.response.send_message(embed=embed, view=CategorySelectView())

    @app_commands.command(name="help", description="Get detailed help and usage examples for any command")
    @app_commands.describe(command="The command name to get help for (without the slash)")
    async def help(self, interaction: discord.Interaction, command: str = None):
        HELP_DATA = {
            "rps": {
                "desc": "Play Rock Paper Scissors against the bot.\nChoose your move and see who wins!",
                "usage": "/rps choice:Rock",
                "example": "`/rps choice:Paper` — You choose paper, bot picks randomly."
            },
            "coinflip": {
                "desc": "Flip a coin and guess if it lands on heads or tails.",
                "usage": "/coinflip guess:heads",
                "example": "`/coinflip guess:tails` — Guess tails and see if you're right!"
            },
            "dice": {
                "desc": "Roll one or more dice. Customize the number of sides and dice count.",
                "usage": "/dice sides:6 count:2",
                "example": "`/dice sides:20 count:3` — Roll three 20-sided dice."
            },
            "slots": {
                "desc": "Spin the slot machine! Match symbols to win.\n💎 Triple diamonds = JACKPOT!",
                "usage": "/slots",
                "example": "`/slots` — Spin and hope for a match!"
            },
            "blackjack": {
                "desc": "Play Blackjack against the dealer. Try to get as close to 21 without going over.",
                "usage": "/blackjack",
                "example": "`/blackjack` — Start a game and use Hit/Stand buttons."
            },
            "numberguess": {
                "desc": "Guess the secret number between 1 and 100. Get hints after each guess!",
                "usage": "/numberguess guess:50",
                "example": "`/numberguess guess:75` — Guess 75, get told higher/lower."
            },
            "trivia": {
                "desc": "Get a random multiple-choice trivia question. Click the button with the correct answer!",
                "usage": "/trivia",
                "example": "`/trivia` — A question appears with 4 clickable answer buttons."
            },
            "trivia_streak": {
                "desc": "Answer 5 trivia questions in a row without getting one wrong!",
                "usage": "/trivia_streak",
                "example": "`/trivia_streak` — Answer all 5 correctly to complete the streak."
            },
            "quickfire": {
                "desc": "Answer a trivia question by typing in chat. You have 15 seconds!",
                "usage": "/quickfire",
                "example": "`/quickfire` — Type your answer in the chat within 15 seconds."
            },
            "meme": {
                "desc": "Fetch a random meme image from popular Reddit subreddits.",
                "usage": "/meme",
                "example": "`/meme` — Gets a random meme from r/memes, r/dankmemes, etc."
            },
            "meme_top": {
                "desc": "Get a top-rated meme from any subreddit from the past day.",
                "usage": "/meme_top subreddit:ProgrammerHumor",
                "example": "`/meme_top subreddit:wholesomememes` — Top wholesome meme today."
            },
            "8ball": {
                "desc": "Ask the magic 8-ball any yes/no question. Receive a mystical response!",
                "usage": "/8ball question:Will I win today?",
                "example": "`/8ball question:Should I eat pizza?` — The 8-ball will decide."
            },
            "fact": {
                "desc": "Receive a random, fascinating science/world fact.",
                "usage": "/fact",
                "example": "`/fact` — Learn something new every time!"
            },
            "pickone": {
                "desc": "Can't make a decision? Give the bot comma-separated options and it'll pick one!",
                "usage": "/pickone options:pizza, burger, sushi",
                "example": "`/pickone options:coffee, tea, juice` — Bot randomly selects one."
            },
            "calculate": {
                "desc": "Evaluate complex math expressions. Supports trig, log, sqrt, and more.",
                "usage": "/calculate expression:sqrt(144) + 5**2",
                "example": "`/calculate expression:sin(pi/2) * 100` → `100`"
            },
            "balance": {
                "desc": "Check your virtual coin balance or look up another user's balance.",
                "usage": "/balance user:@someone",
                "example": "`/balance` — Check your own coins.\n`/balance user:@friend` — Check a friend's."
            },
            "daily": {
                "desc": "Claim your free 200 🪙 coins every 24 hours!",
                "usage": "/daily",
                "example": "`/daily` — Claim once per day. Shows time remaining if already claimed."
            },
            "work": {
                "desc": "Work a random job to earn between 20–200 coins each time.",
                "usage": "/work",
                "example": "`/work` — 'You delivered pizzas and earned 85 🪙!'"
            },
            "pay": {
                "desc": "Transfer coins from your balance to another user's account.",
                "usage": "/pay user:@friend amount:100",
                "example": "`/pay user:@Alex amount:500` — Send 500 coins to Alex."
            },
            "shop": {
                "desc": "Browse the item shop. Items include Lucky Charm, VIP Badge, Crown, and more!",
                "usage": "/shop",
                "example": "`/shop` — View all items and their prices.\n`/buy item_id:crown` — Purchase the crown (2000 🪙)."
            },
            "poll": {
                "desc": "Create a yes/no poll or multi-option poll with reaction voting.",
                "usage": "/poll question:What's for dinner? options:Pizza, Burgers, Sushi",
                "example": "`/poll question:Favorite season? options:Spring,Summer,Fall,Winter`"
            },
            "ship": {
                "desc": "Check the love compatibility between two users (0–100%).",
                "usage": "/ship user1:@Alice user2:@Bob",
                "example": "`/ship user1:@Alice user2:@Bob` — Shows compatibility bar and ship name."
            },
            "warn": {
                "desc": "Issue a warning to a member. Warnings are tracked per server.",
                "usage": "/warn member:@user reason:Spamming",
                "example": "`/warn member:@Steve reason:Excessive spam in #general`"
            },
            "purge": {
                "desc": "Bulk delete 1–100 messages from a channel.",
                "usage": "/purge amount:50",
                "example": "`/purge amount:10` — Deletes the last 10 messages."
            },
            "anime_search": {
                "desc": "Search for any anime using the Jikan API. Shows score, episodes, genres.",
                "usage": "/anime_search title:Naruto",
                "example": "`/anime_search title:Attack on Titan` — Displays synopsis, score, episode count."
            },
            "convert": {
                "desc": "Convert between temperature, distance, and weight units.",
                "usage": "/convert value:100 from_unit:Celsius to_unit:Fahrenheit",
                "example": "`/convert value:5 from_unit:Miles to_unit:Kilometers` → `8.0467 km`"
            },
            "feedback": {
                "desc": "Submit feedback, suggestions, or bug reports to help improve FunBot.",
                "usage": "/feedback type:Suggestion message:Add more trivia questions",
                "example": "`/feedback type:Bug message:The /slots command shows wrong emoji`"
            },
        }

        if not command:
            embed = make_embed(
                "📖 FunBot Help",
                "Use `/help command:<name>` for detailed info on any command.\n\n"
                "**Quick links:**\n"
                "• `/menu` — Browse all commands by category\n"
                "• `/help command:trivia` — Trivia help\n"
                "• `/help command:balance` — Economy help\n"
                "• `/help command:calculate` — Math help\n\n"
                "**Categories:** Games 🎮 | Trivia 🧠 | Memes 😂 | Fun 🎉 | Economy 💰 | "
                "Utility 🔧 | Moderation 🛡️ | Social 💞 | Math 📐 | Anime 🌸",
                "primary"
            )
            await interaction.response.send_message(embed=embed)
            return

        cmd_lower = command.lower().lstrip("/")
        info = HELP_DATA.get(cmd_lower)
        if not info:
            await interaction.response.send_message(
                embed=make_embed("❓ Command Not Found", f"No help entry for `{command}`.\n\nUse `/menu` to browse all commands.", "warning"),
                ephemeral=True
            )
            return
        embed = make_embed(f"📖 Help: /{cmd_lower}", info["desc"], "info")
        embed.add_field(name="📌 Usage", value=f"`{info['usage']}`", inline=False)
        embed.add_field(name="💡 Example", value=info["example"], inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="feedback", description="Submit feedback, suggestions, or bug reports for FunBot")
    @app_commands.describe(feedback_type="Type of feedback", message="Your feedback message")
    @app_commands.choices(feedback_type=[
        app_commands.Choice(name="💡 Suggestion", value="Suggestion"),
        app_commands.Choice(name="🐛 Bug Report", value="Bug Report"),
        app_commands.Choice(name="⭐ Compliment", value="Compliment"),
        app_commands.Choice(name="❓ Question", value="Question"),
        app_commands.Choice(name="🔧 Feature Request", value="Feature Request"),
    ])
    async def feedback(self, interaction: discord.Interaction, feedback_type: app_commands.Choice[str], message: str):
        if len(message) < 10:
            await interaction.response.send_message(embed=make_embed("Error", "Feedback must be at least 10 characters.", "error"), ephemeral=True)
            return
        if len(message) > 500:
            await interaction.response.send_message(embed=make_embed("Error", "Feedback must be under 500 characters.", "error"), ephemeral=True)
            return
        data = load_feedback()
        entry = {
            "user_id": interaction.user.id,
            "user_name": str(interaction.user),
            "type": feedback_type.value,
            "message": message,
            "guild": interaction.guild.name if interaction.guild else "DM",
            "timestamp": discord.utils.utcnow().isoformat(),
        }
        data.append(entry)
        save_feedback(data)
        type_emojis = {
            "Suggestion": "💡", "Bug Report": "🐛", "Compliment": "⭐",
            "Question": "❓", "Feature Request": "🔧"
        }
        emoji = type_emojis.get(feedback_type.value, "📝")
        embed = make_embed(
            f"{emoji} Feedback Received!",
            f"**Type:** {feedback_type.value}\n**Message:** {message}\n\nThank you for helping improve FunBot! 💖",
            "success"
        )
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="viewfeedback", description="[Admin] View all submitted feedback")
    @app_commands.default_permissions(administrator=True)
    async def viewfeedback(self, interaction: discord.Interaction):
        data = load_feedback()
        if not data:
            await interaction.response.send_message(embed=make_embed("📋 Feedback", "No feedback has been submitted yet.", "warning"), ephemeral=True)
            return
        recent = data[-10:]
        lines = [f"**[{e['type']}]** {e['user_name']}: {e['message'][:80]}" for e in reversed(recent)]
        embed = make_embed(f"📋 Latest Feedback ({len(data)} total)", "\n\n".join(lines), "info")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Menu(bot))