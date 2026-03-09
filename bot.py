import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    await bot.load_extension("cogs.anime")
    try:
        synced = await bot.tree.sync()
        print(f"[+] Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"[!] Failed to sync commands: {e}")
    print(f"[+] Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="anime  |  /anime help"
        )
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


if __name__ == "__main__":
    bot.run(TOKEN)
