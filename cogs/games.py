import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
from utils.helpers import make_embed, COLORS

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
               "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}

SLOT_EMOJIS = ["🍒", "🍋", "🍊", "⭐", "💎", "7️⃣", "🍀"]

active_games = {}

def card_value(hand):
    total = sum(RANK_VALUES[r] for r, _ in hand)
    aces = sum(1 for r, _ in hand if r == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def draw_card():
    return (random.choice(RANKS), random.choice(SUITS))

def hand_str(hand):
    return " ".join(f"{r}{s}" for r, s in hand)

class BlackjackView(discord.ui.View):
    def __init__(self, user_id, player_hand, dealer_hand, deck):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.deck = deck
        self.finished = False

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return False
        return True

    def build_embed(self, result=None):
        p_val = card_value(self.player_hand)
        d_val = card_value(self.dealer_hand)
        desc = f"**Your Hand:** {hand_str(self.player_hand)} → `{p_val}`\n"
        if result:
            desc += f"**Dealer Hand:** {hand_str(self.dealer_hand)} → `{d_val}`\n\n"
            desc += result
            color = "success" if "win" in result.lower() or "blackjack" in result.lower() else ("warning" if "tie" in result.lower() else "error")
        else:
            desc += f"**Dealer Hand:** {self.dealer_hand[0][0]}{self.dealer_hand[0][1]} 🂠\n"
            color = "primary"
        return make_embed("🃏 Blackjack", desc, color)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green, emoji="➕")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player_hand.append(draw_card())
        p_val = card_value(self.player_hand)
        if p_val > 21:
            self.finished = True
            self.stop()
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(embed=self.build_embed("💥 **You busted! Dealer wins.**"), view=self)
        elif p_val == 21:
            await self.stand_logic(interaction)
        else:
            await interaction.response.edit_message(embed=self.build_embed(), view=self)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red, emoji="✋")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.stand_logic(interaction)

    async def stand_logic(self, interaction: discord.Interaction):
        while card_value(self.dealer_hand) < 17:
            self.dealer_hand.append(draw_card())
        p_val = card_value(self.player_hand)
        d_val = card_value(self.dealer_hand)
        if d_val > 21 or p_val > d_val:
            result = "🏆 **You win!**"
        elif p_val == d_val:
            result = "🤝 **It's a tie!**"
        else:
            result = "😔 **Dealer wins.**"
        self.finished = True
        self.stop()
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(embed=self.build_embed(result), view=self)

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rps", description="Play Rock Paper Scissors against the bot")
    @app_commands.describe(choice="Your choice: rock, paper, or scissors")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Rock 🪨", value="rock"),
        app_commands.Choice(name="Paper 📄", value="paper"),
        app_commands.Choice(name="Scissors ✂️", value="scissors"),
    ])
    async def rps(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        u = choice.value
        b = bot_choice
        if u == b:
            result = "🤝 It's a tie!"
            color = "warning"
        elif wins[u] == b:
            result = "🏆 You win!"
            color = "success"
        else:
            result = "😔 You lose!"
            color = "error"
        embed = make_embed("🪨 Rock Paper Scissors", f"You chose **{emojis[u]} {u.capitalize()}**\nI chose **{emojis[b]} {b.capitalize()}**\n\n{result}", color)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Flip a coin and guess the result")
    @app_commands.describe(guess="Your guess: heads or tails")
    @app_commands.choices(guess=[
        app_commands.Choice(name="Heads 🪙", value="heads"),
        app_commands.Choice(name="Tails 🔵", value="tails"),
    ])
    async def coinflip(self, interaction: discord.Interaction, guess: app_commands.Choice[str]):
        result = random.choice(["heads", "tails"])
        emojis = {"heads": "🪙", "tails": "🔵"}
        won = guess.value == result
        embed = make_embed(
            "🪙 Coin Flip",
            f"You guessed **{guess.value.capitalize()}**\nThe coin landed on **{emojis[result]} {result.capitalize()}**\n\n{'🏆 Correct!' if won else '😔 Wrong guess!'}",
            "success" if won else "error"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dice", description="Roll one or more dice")
    @app_commands.describe(sides="Number of sides on the dice (default 6)", count="Number of dice to roll (default 1)")
    async def dice(self, interaction: discord.Interaction, sides: int = 6, count: int = 1):
        if sides < 2 or sides > 100:
            await interaction.response.send_message(embed=make_embed("Error", "Sides must be between 2 and 100.", "error"), ephemeral=True)
            return
        if count < 1 or count > 20:
            await interaction.response.send_message(embed=make_embed("Error", "Count must be between 1 and 20.", "error"), ephemeral=True)
            return
        rolls = [random.randint(1, sides) for _ in range(count)]
        desc = f"🎲 **Rolls ({count}d{sides}):** {', '.join(map(str, rolls))}"
        if count > 1:
            desc += f"\n**Total:** `{sum(rolls)}`  |  **Average:** `{sum(rolls)/count:.1f}`"
        await interaction.response.send_message(embed=make_embed("🎲 Dice Roll", desc, "fun"))

    @app_commands.command(name="slots", description="Spin the slot machine!")
    async def slots(self, interaction: discord.Interaction):
        reels = [random.choice(SLOT_EMOJIS) for _ in range(3)]
        display = f"[ {reels[0]} | {reels[1]} | {reels[2]} ]"
        if reels[0] == reels[1] == reels[2]:
            if reels[0] == "💎":
                result = "💎 **JACKPOT! Triple Diamonds!**"
                color = "gold"
            elif reels[0] == "7️⃣":
                result = "7️⃣ **MEGA WIN! Triple Sevens!**"
                color = "gold"
            else:
                result = f"🎉 **You win! Triple {reels[0]}!**"
                color = "success"
        elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
            result = "✨ **Small win! Two of a kind!**"
            color = "warning"
        else:
            result = "😔 **No match. Try again!**"
            color = "error"
        embed = make_embed("🎰 Slot Machine", f"```\n{display}\n```\n{result}", color)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="blackjack", description="Play a game of blackjack against the dealer")
    async def blackjack(self, interaction: discord.Interaction):
        deck = [(r, s) for r in RANKS for s in SUITS]
        random.shuffle(deck)
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]
        view = BlackjackView(interaction.user.id, player, dealer, deck)
        p_val = card_value(player)
        if p_val == 21:
            embed = view.build_embed("🃏 **BLACKJACK! You win instantly!**")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=view.build_embed(), view=view)

    @app_commands.command(name="numberguess", description="Guess the secret number between 1 and 100")
    @app_commands.describe(guess="Your guess (1-100)")
    async def numberguess(self, interaction: discord.Interaction, guess: int):
        uid = interaction.user.id
        if uid not in active_games:
            active_games[uid] = {"number": random.randint(1, 100), "attempts": 0}
        game = active_games[uid]
        game["attempts"] += 1
        secret = game["number"]
        if guess < 1 or guess > 100:
            await interaction.response.send_message(embed=make_embed("Error", "Guess must be between 1 and 100.", "error"), ephemeral=True)
            return
        if guess == secret:
            attempts = game["attempts"]
            del active_games[uid]
            await interaction.response.send_message(embed=make_embed("🎯 Number Guess", f"🏆 **Correct!** The number was **{secret}**!\nYou got it in **{attempts}** attempt(s)!", "success"))
        elif guess < secret:
            await interaction.response.send_message(embed=make_embed("🎯 Number Guess", f"📈 **Too low!** Try a higher number. (Attempt #{game['attempts']})\n*Use `/newgame` to reset.*", "warning"))
        else:
            await interaction.response.send_message(embed=make_embed("🎯 Number Guess", f"📉 **Too high!** Try a lower number. (Attempt #{game['attempts']})\n*Use `/newgame` to reset.*", "warning"))

    @app_commands.command(name="newgame", description="Reset your number guessing game")
    async def newgame(self, interaction: discord.Interaction):
        active_games[interaction.user.id] = {"number": random.randint(1, 100), "attempts": 0}
        await interaction.response.send_message(embed=make_embed("🎯 Number Guess", "A new secret number between **1 and 100** has been chosen!\nUse `/numberguess` to start guessing.", "info"), ephemeral=True)

    @app_commands.command(name="wouldyourather", description="Get a random Would You Rather question")
    async def wouldyourather(self, interaction: discord.Interaction):
        questions = [
            ("be able to fly", "be invisible"),
            ("never eat pizza again", "never eat sweets again"),
            ("lose all your money", "lose all your memories"),
            ("be 10 minutes late every time", "be 20 minutes early every time"),
            ("speak every language", "play every instrument"),
            ("live in the past", "live in the future"),
            ("have super strength", "have super speed"),
            ("know how you die", "know when you die"),
            ("always have to sing", "always have to dance"),
            ("be famous", "be rich but unknown"),
        ]
        a, b = random.choice(questions)
        embed = make_embed("🤔 Would You Rather...", f"🅰️ **{a.capitalize()}**\n\n**— OR —**\n\n🅱️ **{b.capitalize()}**", "fun")
        embed.set_footer(text="React with 🅰️ or 🅱️ to vote!")
        msg = await interaction.response.send_message(embed=embed)
        followup = await interaction.original_response()
        await followup.add_reaction("🅰️")
        await followup.add_reaction("🅱️")

async def setup(bot):
    await bot.add_cog(Games(bot))