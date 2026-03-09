import asyncio

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

NEKOS_BASE = "https://nekos.best/api/v2"
USER_AGENT = "AnimeBot/1.0 (https://github.com/osfv/Anime-Discord-Bot)"
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=15)

COLORS = {
    "hug": 0xF4A7B9,
    "pat": 0xFFD6A5,
    "kiss": 0xFF85A1,
    "slap": 0xFF6B6B,
    "cuddle": 0xC9B8F0,
    "poke": 0x98D8C8,
    "bite": 0xFF9F7F,
    "punch": 0xFF6B6B,
    "cry": 0x91BEF2,
    "blush": 0xFFB3C6,
    "smile": 0xFFF0A0,
    "wave": 0xA8E6CF,
    "dance": 0xD4A8FF,
    "happy": 0xFFF176,
    "wink": 0xFFD6F5,
    "laugh": 0xFFE0A0,
    "neko": 0xB5D8FF,
    "waifu": 0xFFB3D9,
    "kitsune": 0xFFD0A0,
    "husb": 0x9BC4FF,
    "default": 0x2B2D31,
}

ACTION_VERBS = {
    "hug": ("{user} hugs {target}", "{user} hugged themselves... comfort arc."),
    "pat": ("{user} pats {target}", "{user} pats themselves on the head."),
    "kiss": ("{user} kisses {target}", "{user} blows a kiss into the void."),
    "slap": ("{user} slaps {target}", "{user} slaps themselves. Discipline."),
    "cuddle": ("{user} cuddles {target}", "{user} cuddles themselves. Valid."),
    "poke": ("{user} pokes {target}", "{user} pokes the air."),
    "bite": ("{user} bites {target}", "{user} bites themselves. Weird but ok."),
    "punch": ("{user} punches {target}", "{user} throws a punch at the air."),
    "wave": ("{user} waves at {target}", "{user} waves at nobody. Brave."),
    "wink": ("{user} winks at {target}", "{user} winks at the mirror."),
    "cry": ("{user} cries on {target}'s shoulder", "{user} cries alone."),
    "blush": ("{user} blushes at {target}", "{user} blushes at their own reflection."),
    "smile": ("{user} smiles at {target}", "{user} smiles to themselves."),
    "dance": ("{user} dances with {target}", "{user} dances alone. Iconic."),
    "happy": ("{user} is happy with {target}", "{user} radiates happiness."),
    "laugh": ("{user} laughs with {target}", "{user} laughs at their own jokes."),
}

IMAGE_LABELS = {
    "neko": "Neko",
    "waifu": "Waifu",
    "kitsune": "Kitsune",
    "husb": "Husbando",
}

DiscordUser = discord.User | discord.Member
_session: aiohttp.ClientSession | None = None


async def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
    return _session


async def fetch_nekos(category: str, amount: int = 1) -> list[dict]:
    url = f"{NEKOS_BASE}/{category}?amount={amount}"
    session = await _get_session()

    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                return []
            data = await resp.json()
    except (aiohttp.ClientError, aiohttp.ContentTypeError, asyncio.TimeoutError):
        return []

    return data.get("results", [])


def _avatar_url(user: DiscordUser) -> str:
    return user.display_avatar.url


def build_action_embed(
    category: str,
    invoker: DiscordUser,
    target: discord.Member | None,
    result: dict,
) -> discord.Embed:
    color = COLORS.get(category, COLORS["default"])
    image_url = result.get("url", "")
    anime_name = result.get("anime_name", "")
    artist_name = result.get("artist_name", "")
    artist_href = result.get("artist_href", "")

    if target and target.id != invoker.id:
        verb_template, _ = ACTION_VERBS.get(category, ("{user} does something to {target}", ""))
        title = verb_template.format(user=invoker.display_name, target=target.display_name)
    else:
        _, solo_template = ACTION_VERBS.get(category, ("", "{user} does something."))
        title = solo_template.format(user=invoker.display_name)

    embed = discord.Embed(title=title, color=color)
    if image_url:
        embed.set_image(url=image_url)

    meta_parts = []
    if anime_name:
        meta_parts.append(f"**Anime:** {anime_name}")
    if artist_name:
        if artist_href:
            meta_parts.append(f"**Art by:** [{artist_name}]({artist_href})")
        else:
            meta_parts.append(f"**Art by:** {artist_name}")
    if meta_parts:
        embed.description = "\n".join(meta_parts)

    embed.set_footer(text=f"Requested by {invoker.display_name}", icon_url=_avatar_url(invoker))
    return embed


def build_image_embed(category: str, result: dict, invoker: DiscordUser) -> discord.Embed:
    color = COLORS.get(category, COLORS["default"])
    image_url = result.get("url", "")
    artist_name = result.get("artist_name", "")
    artist_href = result.get("artist_href", "")
    source_url = result.get("source_url", "")

    embed = discord.Embed(title=IMAGE_LABELS.get(category, category.title()), color=color)
    if image_url:
        embed.set_image(url=image_url)

    meta_parts = []
    if artist_name:
        if artist_href:
            meta_parts.append(f"**Art by:** [{artist_name}]({artist_href})")
        else:
            meta_parts.append(f"**Art by:** {artist_name}")
    if source_url:
        meta_parts.append(f"[Source]({source_url})")
    if meta_parts:
        embed.description = "\n".join(meta_parts)

    embed.set_footer(text=f"Requested by {invoker.display_name}", icon_url=_avatar_url(invoker))
    return embed


def build_error_embed(message: str) -> discord.Embed:
    return discord.Embed(title="Something went wrong", description=message, color=0xFF6B6B)


def build_help_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Anime Bot Commands",
        description="All commands live under `/anime`.",
        color=COLORS["neko"],
    )
    embed.add_field(
        name="Images",
        value="`/anime neko` `/anime waifu` `/anime kitsune` `/anime husbando`\nGet a random SFW anime image.",
        inline=False,
    )
    embed.add_field(
        name="Actions",
        value=(
            "`/anime hug` `/anime pat` `/anime kiss` `/anime slap` `/anime cuddle` `/anime poke`\n"
            "`/anime bite` `/anime punch` `/anime cry` `/anime blush` `/anime smile` `/anime wave`\n"
            "`/anime dance` `/anime happy` `/anime wink` `/anime laugh`\n"
            "All action commands accept an optional `target`."
        ),
        inline=False,
    )
    embed.set_footer(text="Powered by nekos.best")
    return embed


class Anime(commands.GroupCog, group_name="anime", group_description="Anime reactions and images"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_unload(self):
        global _session
        if _session and not _session.closed:
            await _session.close()
            _session = None

    async def _send_image(self, interaction: discord.Interaction, category: str):
        await interaction.response.defer()
        results = await fetch_nekos(category)
        if not results:
            await interaction.followup.send(embed=build_error_embed("Could not fetch from nekos.best."))
            return
        await interaction.followup.send(embed=build_image_embed(category, results[0], interaction.user))

    async def _action(self, interaction: discord.Interaction, category: str, target: discord.Member | None):
        await interaction.response.defer()
        results = await fetch_nekos(category)
        if not results:
            await interaction.followup.send(embed=build_error_embed("Could not fetch from nekos.best."))
            return
        await interaction.followup.send(
            embed=build_action_embed(category, interaction.user, target, results[0])
        )

    @app_commands.command(name="neko", description="Get a random neko image.")
    async def neko(self, interaction: discord.Interaction):
        await self._send_image(interaction, "neko")

    @app_commands.command(name="waifu", description="Get a random waifu image.")
    async def waifu(self, interaction: discord.Interaction):
        await self._send_image(interaction, "waifu")

    @app_commands.command(name="kitsune", description="Get a random kitsune image.")
    async def kitsune(self, interaction: discord.Interaction):
        await self._send_image(interaction, "kitsune")

    @app_commands.command(name="husbando", description="Get a random husbando image.")
    async def husbando(self, interaction: discord.Interaction):
        await self._send_image(interaction, "husb")

    @app_commands.command(name="hug", description="Hug someone!")
    @app_commands.describe(target="Who do you want to hug?")
    async def hug(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "hug", target)

    @app_commands.command(name="pat", description="Pat someone!")
    @app_commands.describe(target="Who do you want to pat?")
    async def pat(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "pat", target)

    @app_commands.command(name="kiss", description="Kiss someone!")
    @app_commands.describe(target="Who do you want to kiss?")
    async def kiss(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "kiss", target)

    @app_commands.command(name="slap", description="Slap someone!")
    @app_commands.describe(target="Who do you want to slap?")
    async def slap(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "slap", target)

    @app_commands.command(name="cuddle", description="Cuddle with someone!")
    @app_commands.describe(target="Who do you want to cuddle?")
    async def cuddle(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "cuddle", target)

    @app_commands.command(name="poke", description="Poke someone!")
    @app_commands.describe(target="Who do you want to poke?")
    async def poke(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "poke", target)

    @app_commands.command(name="bite", description="Bite someone!")
    @app_commands.describe(target="Who do you want to bite?")
    async def bite(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "bite", target)

    @app_commands.command(name="punch", description="Punch someone!")
    @app_commands.describe(target="Who do you want to punch?")
    async def punch(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "punch", target)

    @app_commands.command(name="cry", description="Cry (optionally on someone's shoulder).")
    @app_commands.describe(target="Whose shoulder do you cry on?")
    async def cry(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "cry", target)

    @app_commands.command(name="blush", description="Blush at someone!")
    @app_commands.describe(target="Who are you blushing at?")
    async def blush(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "blush", target)

    @app_commands.command(name="smile", description="Smile at someone!")
    @app_commands.describe(target="Who are you smiling at?")
    async def smile(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "smile", target)

    @app_commands.command(name="wave", description="Wave at someone!")
    @app_commands.describe(target="Who are you waving at?")
    async def wave(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "wave", target)

    @app_commands.command(name="dance", description="Dance (with someone if you like).")
    @app_commands.describe(target="Your dance partner?")
    async def dance(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "dance", target)

    @app_commands.command(name="happy", description="Express happiness!")
    @app_commands.describe(target="Share your happiness with someone?")
    async def happy(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "happy", target)

    @app_commands.command(name="wink", description="Wink at someone!")
    @app_commands.describe(target="Who are you winking at?")
    async def wink(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "wink", target)

    @app_commands.command(name="laugh", description="Laugh with someone!")
    @app_commands.describe(target="Who are you laughing with?")
    async def laugh(self, interaction: discord.Interaction, target: discord.Member | None = None):
        await self._action(interaction, "laugh", target)

    @app_commands.command(name="help", description="List all anime bot commands.")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=build_help_embed(), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Anime(bot))
