import random
from utils.helpers import make_embed, get_balance, update_user

def rps(client, message, args, sender_jid):
    if not args:
        client.reply_message("Usage: /rps <rock|paper|scissors>", message)
        return

    user_choice = args[0].lower()
    choices = ["rock", "paper", "scissors"]

    if user_choice not in choices:
        client.reply_message("Please choose rock, paper, or scissors.", message)
        return

    bot_choice = random.choice(choices)

    if user_choice == bot_choice:
        result = "It's a tie!"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        result = "You win! 🎉"
    else:
        result = "I win! 🤖"

    text = make_embed("🎮 Rock Paper Scissors", f"You chose: *{user_choice}*\nI chose: *{bot_choice}*\n\n{result}")
    client.reply_message(text, message)

def coinflip(client, message, args, sender_jid):
    if not args:
        client.reply_message("Usage: /coinflip <heads|tails>", message)
        return

    guess = args[0].lower()
    if guess not in ["heads", "tails"]:
        client.reply_message("Please guess heads or tails.", message)
        return

    result = random.choice(["heads", "tails"])
    if guess == result:
        text = make_embed("🪙 Coin Flip", f"It landed on *{result}*!\nYou won! 🎉")
    else:
        text = make_embed("🪙 Coin Flip", f"It landed on *{result}*...\nYou lost! 😢")

    client.reply_message(text, message)

def dice(client, message, args, sender_jid):
    sides = 6
    count = 1

    if len(args) > 0:
        try:
            sides = int(args[0])
        except ValueError:
            pass

    if len(args) > 1:
        try:
            count = int(args[1])
        except ValueError:
            pass

    if count > 10:
        client.reply_message("Maximum of 10 dice allowed.", message)
        return

    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)

    text = make_embed("🎲 Dice Roll", f"Rolling {count}d{sides}...\n\nResults: {rolls}\n*Total:* {total}")
    client.reply_message(text, message)

def slots(client, message, args, sender_jid):
    emojis = ["🍒", "🍋", "🍊", "🍉", "🍇", "💎"]
    weights = [30, 25, 20, 15, 8, 2] # Probabilities

    data = get_balance(sender_jid)
    if data["balance"] < 10:
        client.reply_message("You need at least 10 🪙 to play slots.", message)
        return

    # Cost to play
    update_user(sender_jid, {"balance": data["balance"] - 10})

    result = random.choices(emojis, weights=weights, k=3)

    winnings = 0
    if result[0] == result[1] == result[2]:
        if result[0] == "💎":
            winnings = 1000
        elif result[0] == "🍇":
            winnings = 500
        else:
            winnings = 100

    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        winnings = 20

    msg = f"🎰 *SLOTS* 🎰\n\n[{result[0]} | {result[1]} | {result[2]}]\n\n"

    if winnings > 0:
        data = get_balance(sender_jid)
        update_user(sender_jid, {"balance": data["balance"] + winnings})
        msg += f"You won *{winnings} 🪙*! 🎉"
    else:
        msg += "You lost 10 🪙. Better luck next time!"

    client.reply_message(make_embed("🎰 Slot Machine", msg), message)

def blackjack(client, message, args, sender_jid):
    # Very simplified Blackjack that draws cards instantly instead of interactive UI
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    player_hand = [random.choice(cards), random.choice(cards)]
    dealer_hand = [random.choice(cards), random.choice(cards)]

    player_total = sum(player_hand)
    dealer_total = sum(dealer_hand)

    # Adjust for aces
    if player_total > 21 and 11 in player_hand:
        player_total -= 10
    if dealer_total > 21 and 11 in dealer_hand:
        dealer_total -= 10

    result = ""
    if player_total == 21:
        result = "Blackjack! You win!"
    elif player_total > 21:
        result = "Bust! You lose."
    elif dealer_total > 21:
        result = "Dealer busts! You win!"
    elif player_total > dealer_total:
        result = "You win!"
    elif dealer_total > player_total:
        result = "Dealer wins!"
    else:
        result = "It's a push! (Tie)"

    msg = f"Your Hand: {player_hand} (*{player_total}*)\nDealer's Hand: {dealer_hand} (*{dealer_total}*)\n\n*{result}*"
    client.reply_message(make_embed("🃏 Blackjack (Quick Match)", msg), message)

def numberguess(client, message, args, sender_jid):
    if not args:
        client.reply_message("Usage: /numberguess <guess 1-100>", message)
        return

    try:
        guess = int(args[0])
    except ValueError:
        client.reply_message("Please provide a valid number.", message)
        return

    target = random.randint(1, 100)

    if guess == target:
        msg = f"Wow! You guessed the exact number: *{target}*!"
    elif abs(guess - target) <= 5:
        msg = f"So close! The number was *{target}*. You guessed *{guess}*."
    else:
        msg = f"Not quite! The number was *{target}*. You guessed *{guess}*."

    client.reply_message(make_embed("🔢 Number Guessing", msg), message)

def get_commands():
    return {
        "rps": rps,
        "coinflip": coinflip,
        "dice": dice,
        "slots": slots,
        "blackjack": blackjack,
        "numberguess": numberguess
    }
