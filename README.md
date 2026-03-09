# Anime Discord Bot

A Discord bot for anime reactions and image commands powered by [nekos.best](https://nekos.best).

## Commands

All slash commands live under `/anime`.

### Image commands

- `/anime neko`
- `/anime waifu`
- `/anime kitsune`
- `/anime husbando`

### Action commands

- `/anime hug`
- `/anime pat`
- `/anime kiss`
- `/anime slap`
- `/anime cuddle`
- `/anime poke`
- `/anime bite`
- `/anime punch`
- `/anime cry`
- `/anime blush`
- `/anime smile`
- `/anime wave`
- `/anime dance`
- `/anime happy`
- `/anime wink`
- `/anime laugh`

Every action command accepts an optional `target` user.

### Help

- `/anime help`

## Setup

Requirements:

- Python 3.10+
- A Discord bot token

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_token_here
PREFIX=!
```

Run the bot:

```bash
python bot.py
```

## Notes

- The bot uses standard embeds and stable `discord.py` APIs.
- Slash commands are synced on startup. Global command sync can take a little time to appear in Discord.
- Make sure the bot has the `applications.commands` scope when you invite it.
