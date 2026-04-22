import discord
from discord import app_commands
from discord.ext import commands
import math
import random
from utils.helpers import make_embed

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="calculate", description="Evaluate a math expression")
    @app_commands.describe(expression="Math expression to calculate (e.g. 2 + 2, sqrt(16), 5**3)")
    async def calculate(self, interaction: discord.Interaction, expression: str):
        safe_names = {
            "sqrt": math.sqrt, "abs": abs, "round": round, "pow": pow,
            "log": math.log, "log10": math.log10, "log2": math.log2,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "ceil": math.ceil, "floor": math.floor,
            "pi": math.pi, "e": math.e, "inf": math.inf,
        }
        try:
            cleaned = expression.replace("^", "**")
            result = eval(cleaned, {"__builtins__": {}}, safe_names)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            embed = make_embed("🧮 Calculator", f"**Expression:** `{expression}`\n**Result:** `{result}`", "success")
        except ZeroDivisionError:
            embed = make_embed("🧮 Calculator", "❌ Error: Division by zero!", "error")
        except Exception:
            embed = make_embed("🧮 Calculator", f"❌ Invalid expression: `{expression}`\n\nSupported: `+`, `-`, `*`, `/`, `**`, `sqrt()`, `sin()`, `cos()`, `log()`, etc.", "error")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="random_number", description="Generate a random number within a range")
    @app_commands.describe(minimum="Minimum value", maximum="Maximum value")
    async def random_number(self, interaction: discord.Interaction, minimum: int = 1, maximum: int = 100):
        if minimum >= maximum:
            await interaction.response.send_message(embed=make_embed("Error", "Minimum must be less than maximum.", "error"), ephemeral=True)
            return
        num = random.randint(minimum, maximum)
        embed = make_embed("🎲 Random Number", f"Range: `{minimum:,}` — `{maximum:,}`\n\n🎯 **Result: `{num:,}`**", "fun")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="percentage", description="Calculate X% of a number")
    @app_commands.describe(percent="The percentage", number="The base number")
    async def percentage(self, interaction: discord.Interaction, percent: float, number: float):
        result = (percent / 100) * number
        embed = make_embed("📊 Percentage", f"**{percent}%** of **{number}** = **`{result:,.2f}`**", "info")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="factor", description="Get the prime factorization of a number")
    @app_commands.describe(number="The number to factorize (2 to 10,000,000)")
    async def factor(self, interaction: discord.Interaction, number: int):
        if number < 2 or number > 10_000_000:
            await interaction.response.send_message(embed=make_embed("Error", "Number must be between 2 and 10,000,000.", "error"), ephemeral=True)
            return
        n = number
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        factored = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items())
        embed = make_embed("🔢 Prime Factorization", f"**{number}** = **{factored}**", "info")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fibonacci", description="Generate the Fibonacci sequence up to N terms")
    @app_commands.describe(terms="Number of terms (1-50)")
    async def fibonacci(self, interaction: discord.Interaction, terms: int):
        if terms < 1 or terms > 50:
            await interaction.response.send_message(embed=make_embed("Error", "Terms must be between 1 and 50.", "error"), ephemeral=True)
            return
        fib = [0, 1]
        for _ in range(terms - 2):
            fib.append(fib[-1] + fib[-2])
        seq = fib[:terms]
        embed = make_embed(f"🌀 Fibonacci ({terms} terms)", f"`{', '.join(map(str, seq))}`", "info")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="convert", description="Convert between common units")
    @app_commands.describe(value="The value to convert", from_unit="Source unit", to_unit="Target unit")
    @app_commands.choices(from_unit=[
        app_commands.Choice(name="Celsius", value="celsius"),
        app_commands.Choice(name="Fahrenheit", value="fahrenheit"),
        app_commands.Choice(name="Kilometers", value="km"),
        app_commands.Choice(name="Miles", value="miles"),
        app_commands.Choice(name="Kilograms", value="kg"),
        app_commands.Choice(name="Pounds", value="lbs"),
    ])
    @app_commands.choices(to_unit=[
        app_commands.Choice(name="Celsius", value="celsius"),
        app_commands.Choice(name="Fahrenheit", value="fahrenheit"),
        app_commands.Choice(name="Kilometers", value="km"),
        app_commands.Choice(name="Miles", value="miles"),
        app_commands.Choice(name="Kilograms", value="kg"),
        app_commands.Choice(name="Pounds", value="lbs"),
    ])
    async def convert(self, interaction: discord.Interaction, value: float, from_unit: app_commands.Choice[str], to_unit: app_commands.Choice[str]):
        f = from_unit.value
        t = to_unit.value
        conversions = {
            ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
            ("km", "miles"): lambda x: x * 0.621371,
            ("miles", "km"): lambda x: x * 1.60934,
            ("kg", "lbs"): lambda x: x * 2.20462,
            ("lbs", "kg"): lambda x: x * 0.453592,
        }
        if f == t:
            result = value
        elif (f, t) in conversions:
            result = conversions[(f, t)](value)
        else:
            await interaction.response.send_message(embed=make_embed("Error", f"Cannot convert from `{f}` to `{t}`.", "error"), ephemeral=True)
            return
        embed = make_embed("📏 Unit Converter", f"**{value} {f}** = **`{result:.4f} {t}`**", "info")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bmi", description="Calculate your Body Mass Index (BMI)")
    @app_commands.describe(weight_kg="Your weight in kilograms", height_cm="Your height in centimeters")
    async def bmi(self, interaction: discord.Interaction, weight_kg: float, height_cm: float):
        if weight_kg <= 0 or height_cm <= 0:
            await interaction.response.send_message(embed=make_embed("Error", "Values must be positive.", "error"), ephemeral=True)
            return
        height_m = height_cm / 100
        bmi_val = weight_kg / (height_m ** 2)
        if bmi_val < 18.5:
            category = "Underweight 🔵"
        elif bmi_val < 25:
            category = "Normal weight 🟢"
        elif bmi_val < 30:
            category = "Overweight 🟡"
        else:
            category = "Obese 🔴"
        embed = make_embed("⚖️ BMI Calculator", f"**Weight:** {weight_kg} kg | **Height:** {height_cm} cm\n\n**BMI:** `{bmi_val:.2f}`\n**Category:** {category}", "info")
        embed.set_footer(text="BMI is a general guide — consult a doctor for health advice.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Math(bot))