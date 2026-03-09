# Anime Discord Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py 2.x" />
  <img src="https://img.shields.io/badge/API-nekos.best-F48FB1?style=for-the-badge" alt="nekos.best API" />
  <img src="https://img.shields.io/badge/Commands-Slash-2B2D31?style=for-the-badge&logo=discord" alt="Slash Commands" />
</p>

A clean Discord bot for anime reactions and image commands, powered by [nekos.best](https://nekos.best).

It keeps the scope simple: fast slash commands, polished embeds, and enough variety to make a server feel more alive without turning the bot into a bloated multipurpose project.

## Overview

- Image commands for `neko`, `waifu`, `kitsune`, and `husbando`
- Reaction commands like `hug`, `pat`, `kiss`, `slap`, `cuddle`, and more
- Optional `target` support on reaction commands
- Styled embeds with credits and source links when available
- Lightweight setup with `discord.py`, `aiohttp`, and `.env` configuration

## Commands

Everything lives under `/anime`.

| Type | Commands |
| --- | --- |
| Image | `/anime neko`, `/anime waifu`, `/anime kitsune`, `/anime husbando` |
| Reaction | `/anime hug`, `/anime pat`, `/anime kiss`, `/anime slap`, `/anime cuddle`, `/anime poke`, `/anime bite`, `/anime punch`, `/anime cry`, `/anime blush`, `/anime smile`, `/anime wave`, `/anime dance`, `/anime happy`, `/anime wink`, `/anime laugh` |
| Utility | `/anime help` |

Every reaction command accepts an optional `target`.

## Highlights

### Image commands

Get random anime images inside Discord with clean embeds and attribution when the API provides artist metadata.

### Reaction commands

Send expressive anime reactions to another user, or let the command fall back to solo text when no target is provided.

### Built for simplicity

The project is intentionally small, easy to run locally, and straightforward to extend if you want to add more commands later.

## Setup

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Create a `.env` file

```env
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
```

`PREFIX` is part of the bot configuration, but the current user-facing interface is slash-command based.

### 3. Run the bot

```bash
python bot.py
```

On startup, the bot loads the anime cog and syncs slash commands automatically.

## Discord Setup

Invite the bot with these scopes:

- `bot`
- `applications.commands`

If you plan to expand the project with prefix commands later, enable the message content intent in the Discord Developer Portal as well.

## Tech Stack

- [Python](https://www.python.org/)
- [discord.py](https://github.com/Rapptz/discord.py)
- [aiohttp](https://docs.aiohttp.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [nekos.best API](https://nekos.best)

## Project Structure

```text
.
|-- bot.py
|-- requirements.txt
`-- cogs/
    `-- anime.py
```

## Notes

- Slash command sync can take a little time to appear globally.
- If the upstream API fails, the bot returns an error embed instead of crashing.
- Artist and source metadata are displayed whenever the API provides them.

## Future Ideas

- Add more reaction categories
- Add server-specific settings
- Add a simple invite link section once the bot is deployed
- Add screenshots or GIF previews of embeds in action

## License

MIT.

