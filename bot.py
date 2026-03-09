import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set. Check your .env file.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


async def setup_hook():
    await bot.load_extension("cogs.anime")
    try:
        synced = await bot.tree.sync()
        print(f"[+] Synced {len(synced)} slash command(s).")
    except Exception as error:
        print(f"[!] Failed to sync commands: {error}")


bot.setup_hook = setup_hook


@bot.event
async def on_ready():
    print(f"[+] Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="anime | /anime help",
        )
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
):
    print(f"[!] App command error: {error}")
    message = "Something went wrong while running that command. Try again in a moment."

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


if __name__ == "__main__":
    bot.run(TOKEN)
