import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"ivan": 0}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# 👇 funkce na skloňování
def sklonuj_hry(pocet):
    if pocet == 1:
        return "hru"
    elif 2 <= pocet <= 4:
        return "hry"
    else:
        return "her"

@bot.event
async def on_ready():
    print(f"Přihlášen jako {bot.user}")

async def add_reactions(message, kind="default"):
    if kind == "plus":
        emojis = ["🇩","🇴","🇼","🇳","🇮","🇰"]
    else:
        emojis = ["\u2642", "🇸", "🇪", "🇽"]
    for emoji in emojis:
        await message.add_reaction(emoji)

def create_embed(title, description, color=discord.Color.pink()):
    return discord.Embed(title=title, description=description, color=color)

@bot.command()
async def prohry(ctx):
    data = load_data()
    pocet = data["ivan"]
    slovo = sklonuj_hry(pocet)

    embed = create_embed(
        "Celkové skóre",
        f"Ivan nám prohrál přesně **{pocet} {slovo}**"
    )
    msg = await ctx.send(embed=embed)
    await add_reactions(msg)

@bot.command()
async def plus(ctx):
    data = load_data()
    data["ivan"] += 1
    save_data(data)
    embed = create_embed("Zas a znovu", f"Ivanovo prohry +1", color=discord.Color.green())
    msg = await ctx.send(embed=embed)
    await add_reactions(msg, kind="plus")

@bot.command()
async def minus(ctx):
    data = load_data()
    data["ivan"] -= 1
    save_data(data)
    embed = create_embed("No to teda nevim, ale...", f"Ivanovo prohry -1", color=discord.Color.orange())
    msg = await ctx.send(embed=embed)
    await add_reactions(msg)

@bot.command()
async def reset(ctx):
    data = {"ivan": 0}
    save_data(data)
    embed = create_embed("A to jako proč", "Proběhl velký Ivan reset", color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    await add_reactions(msg)

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("No TOKEN")
else:
    bot.run(TOKEN)
