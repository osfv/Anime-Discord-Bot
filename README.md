<div align="center">

# Anime Discord Bot

**A clean, fast Discord bot for anime GIFs and images — powered by [nekos.best](https://nekos.best).**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.6%2B-5865F2?style=flat-square&logo=discord)](https://discordpy.readthedocs.io/)
[![nekos.best](https://img.shields.io/badge/API-nekos.best-ff85a1?style=flat-square)](https://nekos.best)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## What it does

Every command lives under `/anime` — no top-level clutter, no underscores.  
Type `/anime` and Discord autocompletes the rest.

- **Image commands** — pull high-quality static art for neko, waifu, kitsune, and husbando
- **Action commands** — send animated GIFs to another member, or fly solo with self-aware fallback lines
- **Components V2** — every response uses Discord's modern layout system: `Container`, `MediaGallery`, `TextDisplay`, `Separator`. No legacy embeds.
- **Artist credits** — every image credits the artist and source anime inline, with a clickable link

---

## Commands

All commands are slash commands under the `/anime` group.

### Images

| Command | Description |
|---|---|
| `/anime neko` | A neko image |
| `/anime waifu` | A waifu image |
| `/anime kitsune` | A kitsune image |
| `/anime husbando` | A husbando image |

### Actions

All action commands accept an optional `@user` target. Leave it blank to go solo — the bot has a unique line for each solo case.

| Command | With target | Solo |
|---|---|---|
| `/anime hug` | Vince hugs Rei | Vince hugged themselves. Comfort arc. |
| `/anime pat` | Vince pats Rei | Vince pats themselves on the head. |
| `/anime kiss` | Vince kisses Rei | Vince blows a kiss into the void. |
| `/anime slap` | Vince slaps Rei | Vince slaps themselves. Discipline. |
| `/anime cuddle` | Vince cuddles with Rei | Vince cuddles themselves. Valid. |
| `/anime poke` | Vince pokes Rei | Vince pokes the air. |
| `/anime bite` | Vince bites Rei | Vince bites themselves. Weird but ok. |
| `/anime punch` | Vince punches Rei | Vince throws a punch at the air. |
| `/anime wave` | Vince waves at Rei | Vince waves at nobody. Brave. |
| `/anime wink` | Vince winks at Rei | Vince winks at the mirror. |
| `/anime cry` | Vince cries on Rei's shoulder | Vince cries alone. |
| `/anime blush` | Vince blushes at Rei | Vince blushes at their own reflection. |
| `/anime smile` | Vince smiles at Rei | Vince smiles to themselves. |
| `/anime dance` | Vince dances with Rei | Vince dances alone. Iconic. |
| `/anime happy` | Vince celebrates with Rei | Vince radiates happiness. |
| `/anime laugh` | Vince laughs with Rei | Vince laughs at their own jokes. |

### Help

| Command | Description |
|---|---|
| `/anime help` | Show all commands (ephemeral — only you can see it) |

---

## Setup

### Prerequisites

- Python 3.10 or higher
- A Discord bot token ([create one here](https://discord.com/developers/applications))

### Installation

**1. Clone the repo**
```bash
git clone https://github.com/osfv/Anime-Discord-Bot.git
cd Anime-Discord-Bot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment**
```bash
cp .env.example .env
```

Open `.env` and fill in your bot token:
```env
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
```

**4. Run**
```bash
python bot.py
```

You should see:
```
[+] Synced 21 slash command(s).
[+] Logged in as YourBot#0000 (ID: 123456789)
```

---

## Inviting the bot

When creating your bot at the [Discord Developer Portal](https://discord.com/developers/applications), make sure to enable:

- **Bot** scope
- **applications.commands** scope (required for slash commands)
- **Send Messages** and **Use Application Commands** permissions

---

## Project structure

```
Anime-Discord-Bot/
├── bot.py                  # Entry point — loads cogs, syncs command tree
├── cogs/
│   ├── __init__.py
│   └── anime.py            # All /anime commands and Components V2 views
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
└── README.md
```

---

## How it works

**Command structure**

All commands are subcommands of a single `app_commands.Group(name="anime")`. This is how Discord achieves the `/anime help` style — a group name plus a subcommand name, no spaces or underscores required.

**Components V2**

Each response is built with `discord.ui.LayoutView` containing:
- `Container` — wraps everything, carries the per-category accent color
- `TextDisplay` — renders the title and artist credit as markdown
- `Separator` — clean spacing between elements
- `MediaGallery` — renders the image or GIF at full width

**nekos.best API**

No API key required. Every call hits `https://nekos.best/api/v2/{category}?amount=1` and returns a result with `url`, `anime_name`, `artist_name`, and `artist_href`. The bot surfaces all of these.

---

## Adding more commands

nekos.best has 60+ categories. Adding a new action command takes 4 lines:

**1.** Add an entry to `ACTION_VERBS` in `cogs/anime.py`:
```python
"bonk": ("{user} bonks {target}", "{user} bonks the air. Deserved."),
```

**2.** Add a color to `COLORS`:
```python
"bonk": 0xFF6B6B,
```

**3.** Add the command to `AnimeCog`:
```python
@anime.command(name="bonk", description="Bonk someone")
@app_commands.describe(target="Who to bonk")
async def bonk(self, interaction: discord.Interaction, target: discord.Member = None):
    await self._action(interaction, "bonk", target)
```

That's it. Restart and it syncs automatically.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `discord.py` | `>=2.6.0` | Discord API wrapper with Components V2 support |
| `aiohttp` | `>=3.9.0` | Async HTTP client for nekos.best API calls |
| `python-dotenv` | `>=1.0.0` | Load `.env` file for the bot token |

---

## License

MIT — do whatever you want with it.