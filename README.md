<div align="center">

<img src="https://avatars.githubusercontent.com/u/218491571?v=4" width="90" style="border-radius: 50%" />

# Anime Discord Bot

**A clean, fast Discord bot for anime reactions & images — built with Python and powered by [nekos.best](https://nekos.best).**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discordpy.readthedocs.io)
[![nekos.best](https://img.shields.io/badge/API-nekos.best-ff69b4?style=flat-square)](https://nekos.best)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## What it does

Send anime reaction GIFs and images straight in Discord using slash commands. Hug your friends, pat them, wave, cry dramatically — all with a single `/anime` command and a clean embed response.

Every command lives under `/anime` — so the command list stays organized and nothing clutters your server's slash menu.

---

## Commands

All commands follow the pattern `/anime <action>`.

| Command | Type | What it sends |
|---|---|---|
| `/anime hug` | GIF | Hug someone |
| `/anime pat` | GIF | Pat someone on the head |
| `/anime kiss` | GIF | Kiss someone |
| `/anime slap` | GIF | Slap (lovingly, of course) |
| `/anime cuddle` | GIF | Cuddle up |
| `/anime poke` | GIF | Poke someone |
| `/anime bite` | GIF | Bite |
| `/anime punch` | GIF | Punch |
| `/anime wave` | GIF | Wave hello |
| `/anime wink` | GIF | Wink |
| `/anime cry` | GIF | Cry |
| `/anime blush` | GIF | Blush |
| `/anime smile` | GIF | Smile |
| `/anime dance` | GIF | Dance |
| `/anime happy` | GIF | Happy reaction |
| `/anime laugh` | GIF | Laugh |
| `/anime neko` | Image | Random neko |
| `/anime waifu` | Image | Random waifu |
| `/anime kitsune` | Image | Random kitsune |
| `/anime husbando` | Image | Random husbando |
| `/anime help` | Info | Lists all commands |

---

## Setup

**Requirements:** Python 3.10+, a Discord bot token.

```bash
# 1. Clone the repo
git clone https://github.com/osfv/Anime-Discord-Bot.git
cd Anime-Discord-Bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your token
cp .env.example .env
# Open .env and paste your bot token

# 4. Run
python bot.py
```

Your `.env` should look like this:

```env
DISCORD_TOKEN=your_token_here
PREFIX=!
```

> Get your bot token from the [Discord Developer Portal](https://discord.com/developers/applications). Enable **slash commands** permission when inviting the bot.

---

## Adding new commands

Drop 4 lines inside the `AnimeGroup` class in `cogs/anime.py`:

```python
@app_commands.command(name="handhold", description="Hold someone's hand")
async def handhold(self, interaction: discord.Interaction, user: discord.Member = None):
    await self.send_reaction(interaction, "handhold", user)
```

That's it. Restart and the new command appears under `/anime` automatically.

---

## Tech

- **[discord.py 2.x](https://discordpy.readthedocs.io)** — slash commands via `app_commands`
- **[nekos.best](https://nekos.best)** — free anime GIF & image API, no key required
- **aiohttp** — async HTTP for fast API calls
- **python-dotenv** — clean environment variable management

---

## Author

<div align="center">

**iqad** · [@osfv](https://github.com/osfv)

[![GitHub](https://img.shields.io/badge/GitHub-osfv-181717?style=flat-square&logo=github)](https://github.com/osfv)
[![Email](https://img.shields.io/badge/Email-loser@nebula.me-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:loser@nebula.me)

*Feel free to fork, star, or open an issue.*

</div>

---

<div align="center">
<sub>MIT License · Built with Python · Powered by nekos.best</sub>
</div>
