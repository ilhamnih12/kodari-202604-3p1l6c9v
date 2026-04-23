import math
import random
from utils.helpers import make_embed

def calculate(client, message, args, sender_jid):
    expression = " ".join(args)
    if not expression:
        client.reply_message("Usage: /calculate <expression>", message)
        return

    try:
        # Safe eval using limited builtins and dict
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

        # Strip out obviously malicious parts if we were to be completely safe, but compile+eval with no builtins is okay for simple math
        code = compile(expression, "<string>", "eval")
        # Ensure there are no function calls outside of allowed math functions or variable accesses
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Use of {name} not allowed")

        result = eval(code, {"__builtins__": {}}, allowed_names)
        text = make_embed("📐 Calculation", f"*Expression:* `{expression}`\n*Result:* `{result}`")
        client.reply_message(text, message)
    except Exception as e:
        client.reply_message(f"Error calculating: {e}", message)

def convert(client, message, args, sender_jid):
    # Basic conversion logic (simplified)
    client.reply_message("Conversion feature is coming soon to WhatsApp!", message)

def bmi(client, message, args, sender_jid):
    if len(args) < 2:
        client.reply_message("Usage: /bmi <weight_kg> <height_cm>", message)
        return

    try:
        weight = float(args[0])
        height_cm = float(args[1])
        height_m = height_cm / 100
        bmi_val = weight / (height_m ** 2)

        category = ""
        if bmi_val < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi_val < 25:
            category = "Normal weight"
        elif 25 <= bmi_val < 30:
            category = "Overweight"
        else:
            category = "Obese"

        text = make_embed("⚖️ BMI Calculator", f"*Weight:* {weight} kg\n*Height:* {height_cm} cm\n\n*BMI:* `{bmi_val:.1f}` ({category})")
        client.reply_message(text, message)
    except ValueError:
        client.reply_message("Please provide valid numbers.", message)

def random_number(client, message, args, sender_jid):
    if len(args) < 2:
        client.reply_message("Usage: /random_number <min> <max>", message)
        return
    try:
        min_val = int(args[0])
        max_val = int(args[1])
        if min_val >= max_val:
            client.reply_message("Min must be less than max.", message)
            return
        result = random.randint(min_val, max_val)
        client.reply_message(make_embed("🎲 Random Number", f"Between {min_val} and {max_val}: *{result}*"), message)
    except ValueError:
        client.reply_message("Please provide valid integers.", message)

def percentage(client, message, args, sender_jid):
    if len(args) < 2:
        client.reply_message("Usage: /percentage <percent> <number>", message)
        return
    try:
        percent = float(args[0])
        number = float(args[1])
        result = (percent / 100) * number
        client.reply_message(make_embed("📐 Percentage", f"{percent}% of {number} is *{result}*"), message)
    except ValueError:
        client.reply_message("Please provide valid numbers.", message)

def get_commands():
    return {
        "calculate": calculate,
        "convert": convert,
        "bmi": bmi,
        "random_number": random_number,
        "percentage": percentage
    }
