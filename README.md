<div align="center">

# 🌸 Anime Discord Bot

**Fast, clean anime reactions & images for your Discord server.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![discord.py 2.x](https://img.shields.io/badge/discord.py-2.x-5865F2?style=flat-square&logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)
[![API: nekos.best](https://img.shields.io/badge/API-nekos.best-F48FB1?style=flat-square)](https://nekos.best)
[![Slash Commands](https://img.shields.io/badge/Commands-Slash-2B2D31?style=flat-square&logo=discord)](https://discord.com/developers/docs/interactions/application-commands)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A lightweight Discord bot that brings anime reactions and image commands to your server — no bloat, just vibes. Powered by the [nekos.best](https://nekos.best) API with polished embeds and slash command support.

</div>

---

## ✨ Features

- 🖼️ **Image commands** — Pull random `neko`, `waifu`, `kitsune`, and `husbando` images with artist credits
- 💬 **Reaction commands** — Express yourself with 16+ anime reactions, with optional `@target` support
- ⚡ **Slash commands** — Everything lives under `/anime`, no prefix needed
- 🎨 **Styled embeds** — Clean, consistent embed design with source attribution when available
- 🛡️ **Graceful error handling** — API failures return a friendly embed instead of crashing

---

## 📋 Commands

All commands are accessed via `/anime <command>`.

### 🖼️ Image Commands
| Command | Description |
|--------|-------------|
| `/anime neko` | Random neko image |
| `/anime waifu` | Random waifu image |
| `/anime kitsune` | Random kitsune image |
| `/anime husbando` | Random husbando image |

### 💞 Reaction Commands
| Command | Description |
|--------|-------------|
| `/anime hug [target]` | Give someone a hug |
| `/anime pat [target]` | Pat someone on the head |
| `/anime kiss [target]` | Send a kiss |
| `/anime slap [target]` | Slap someone |
| `/anime cuddle [target]` | Cuddle up |
| `/anime poke [target]` | Poke someone |
| `/anime bite [target]` | Nom |
| `/anime punch [target]` | Throw a punch |
| `/anime cry` | Let it out 😢 |
| `/anime blush` | 👉👈 |
| `/anime smile` | Smile! |
| `/anime wave [target]` | Wave hello |
| `/anime dance` | Dance it out |
| `/anime happy` | Happy vibes |
| `/anime wink [target]` | 😉 |
| `/anime laugh` | lol |

> **Tip:** All `[target]` parameters are optional. Without a target, the bot uses solo fallback text.

### 🔧 Utility
| Command | Description |
|--------|-------------|
| `/anime help` | Show all available commands |

---

## 🚀 Self-Hosting

### Prerequisites

- Python 3.10 or higher
- A [Discord bot token](https://discord.com/developers/applications)

### 1. Clone the repo

```bash
git clone https://github.com/osfv/Anime-Discord-Bot.git
cd Anime-Discord-Bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy the example env file and fill in your token:

```bash
cp .env.example .env
```

```env
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
```

### 4. Run the bot

```bash
python bot.py
```

The bot will load the anime cog and sync slash commands automatically on startup.

---

## 🔗 Discord Setup

When inviting the bot, make sure to include these OAuth2 scopes:

- `bot`
- `applications.commands`

> **Note:** Slash commands may take a few minutes to appear globally after the first sync.

---

## 🗂️ Project Structure

```
Anime-Discord-Bot/
├── bot.py              # Entry point — loads cogs and syncs commands
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── cogs/
    └── anime.py        # All anime commands
```

---

## 🛠️ Tech Stack

| Library | Purpose |
|--------|---------|
| [discord.py 2.x](https://github.com/Rapptz/discord.py) | Discord bot framework |
| [aiohttp](https://docs.aiohttp.org/) | Async HTTP requests to the API |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable loading |
| [nekos.best API](https://nekos.best) | Anime image & GIF source |

---

## 🗺️ Roadmap

- [ ] More reaction categories
- [ ] Server-specific settings
- [ ] Invite link once publicly deployed
- [ ] Embed preview screenshots / GIFs in README

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
Made with ❤️ by iqad :P
</div>
