import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

NEKOS_BASE = "https://nekos.best/api/v2"
USER_AGENT = "AnimeBot/1.0"

COLORS = {
    "hug":     0xF4A7B9,
    "pat":     0xFFD6A5,
    "kiss":    0xFF85A1,
    "slap":    0xFF6B6B,
    "cuddle":  0xC9B8F0,
    "poke":    0x98D8C8,
    "bite":    0xFF9F7F,
    "punch":   0xFF6B6B,
    "cry":     0x91BEF2,
    "blush":   0xFFB3C6,
    "smile":   0xFFF0A0,
    "wave":    0xA8E6CF,
    "dance":   0xD4A8FF,
    "happy":   0xFFF176,
    "wink":    0xFFD6F5,
    "laugh":   0xFFE0A0,
    "neko":    0xB5D8FF,
    "waifu":   0xFFB3D9,
    "kitsune": 0xFFD0A0,
    "husbando": 0xA8C8FF,
    "default": 0x2B2D31,
}

ACTION_VERBS = {
    "hug":    ("{user} hugs {target}",              "{user} hugged themselves. Comfort arc."),
    "pat":    ("{user} pats {target}",              "{user} pats themselves on the head."),
    "kiss":   ("{user} kisses {target}",            "{user} blows a kiss into the void."),
    "slap":   ("{user} slaps {target}",             "{user} slaps themselves. Discipline."),
    "cuddle": ("{user} cuddles with {target}",      "{user} cuddles themselves. Valid."),
    "poke":   ("{user} pokes {target}",             "{user} pokes the air."),
    "bite":   ("{user} bites {target}",             "{user} bites themselves. Weird but ok."),
    "punch":  ("{user} punches {target}",           "{user} throws a punch at the air."),
    "wave":   ("{user} waves at {target}",          "{user} waves at nobody. Brave."),
    "wink":   ("{user} winks at {target}",          "{user} winks at the mirror."),
    "cry":    ("{user} cries on {target}'s shoulder", "{user} cries alone."),
    "blush":  ("{user} blushes at {target}",        "{user} blushes at their own reflection."),
    "smile":  ("{user} smiles at {target}",         "{user} smiles to themselves."),
    "dance":  ("{user} dances with {target}",       "{user} dances alone. Iconic."),
    "happy":  ("{user} celebrates with {target}",   "{user} radiates happiness."),
    "laugh":  ("{user} laughs with {target}",       "{user} laughs at their own jokes."),
}

HELP_LINES = [
    ("Images", "`/anime neko` `/anime waifu` `/anime kitsune` `/anime husbando`"),
    ("Actions", "`/anime hug` `/anime pat` `/anime kiss` `/anime slap` `/anime cuddle`\n`/anime poke` `/anime bite` `/anime punch` `/anime wave` `/anime wink`\n`/anime cry` `/anime blush` `/anime smile` `/anime dance` `/anime happy` `/anime laugh`"),
    ("Tip", "Action commands accept an optional `@user` target.\nLeave it blank to go solo."),
]


async def fetch_nekos(category: str) -> dict | None:
    url = f"{NEKOS_BASE}/{category}?amount=1"
    async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            results = data.get("results", [])
            return results[0] if results else None


def action_view(category: str, invoker: discord.Member, target: discord.Member | None, result: dict) -> discord.ui.LayoutView:
    color = COLORS.get(category, COLORS["default"])
    image_url = result.get("url", "")
    anime_name = result.get("anime_name", "")
    artist_name = result.get("artist_name", "")
    artist_href = result.get("artist_href", "")

    if target and target.id != invoker.id:
        title = ACTION_VERBS[category][0].format(user=invoker.display_name, target=target.display_name)
    else:
        title = ACTION_VERBS[category][1].format(user=invoker.display_name)

    meta_parts = []
    if anime_name:
        meta_parts.append(f"-# From **{anime_name}**")
    if artist_name:
        link = f"[{artist_name}]({artist_href})" if artist_href else artist_name
        meta_parts.append(f"-# Art by {link}")
    meta = "\n".join(meta_parts)

    class V(discord.ui.LayoutView):
        container = discord.ui.Container(accent_colour=discord.Colour(color))
        container.add_item(discord.ui.TextDisplay(f"## {title}"))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
        container.add_item(discord.ui.MediaGallery(discord.MediaGalleryItem(image_url)))
        if meta:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
            container.add_item(discord.ui.TextDisplay(meta))

    V.add_item(V.container)
    return V()


def image_view(category: str, result: dict) -> discord.ui.LayoutView:
    color = COLORS.get(category, COLORS["default"])
    image_url = result.get("url", "")
    anime_name = result.get("anime_name", "")
    artist_name = result.get("artist_name", "")
    artist_href = result.get("artist_href", "")

    label = category.capitalize()

    meta_parts = []
    if anime_name:
        meta_parts.append(f"-# From **{anime_name}**")
    if artist_name:
        link = f"[{artist_name}]({artist_href})" if artist_href else artist_name
        meta_parts.append(f"-# Art by {link}")
    meta = "\n".join(meta_parts)

    class V(discord.ui.LayoutView):
        container = discord.ui.Container(accent_colour=discord.Colour(color))
        container.add_item(discord.ui.TextDisplay(f"## {label}"))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
        container.add_item(discord.ui.MediaGallery(discord.MediaGalleryItem(image_url)))
        if meta:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
            container.add_item(discord.ui.TextDisplay(meta))

    V.add_item(V.container)
    return V()


def help_view() -> discord.ui.LayoutView:
    class V(discord.ui.LayoutView):
        container = discord.ui.Container(accent_colour=discord.Colour(0xB5D8FF))
        container.add_item(discord.ui.TextDisplay("## Anime Bot \u2014 Commands"))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
        for section_name, section_body in HELP_LINES:
            container.add_item(discord.ui.TextDisplay(f"**{section_name}**\n{section_body}"))
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))

    V.add_item(V.container)
    return V()


class AnimeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    anime = app_commands.Group(name="anime", description="Anime commands powered by nekos.best")

    # -- Image commands --

    @anime.command(name="neko", description="Get a neko image")
    async def neko(self, interaction: discord.Interaction):
        await interaction.response.defer()
        result = await fetch_nekos("neko")
        if not result:
            await interaction.followup.send("Could not fetch image. Try again!", ephemeral=True)
            return
        await interaction.followup.send(view=image_view("neko", result))

    @anime.command(name="waifu", description="Get a waifu image")
    async def waifu(self, interaction: discord.Interaction):
        await interaction.response.defer()
        result = await fetch_nekos("waifu")
        if not result:
            await interaction.followup.send("Could not fetch image. Try again!", ephemeral=True)
            return
        await interaction.followup.send(view=image_view("waifu", result))

    @anime.command(name="kitsune", description="Get a kitsune image")
    async def kitsune(self, interaction: discord.Interaction):
        await interaction.response.defer()
        result = await fetch_nekos("kitsune")
        if not result:
            await interaction.followup.send("Could not fetch image. Try again!", ephemeral=True)
            return
        await interaction.followup.send(view=image_view("kitsune", result))

    @anime.command(name="husbando", description="Get a husbando image")
    async def husbando(self, interaction: discord.Interaction):
        await interaction.response.defer()
        result = await fetch_nekos("husbando")
        if not result:
            await interaction.followup.send("Could not fetch image. Try again!", ephemeral=True)
            return
        await interaction.followup.send(view=image_view("husbando", result))

    # -- Action commands --

    async def _action(self, interaction: discord.Interaction, category: str, target: discord.Member | None):
        await interaction.response.defer()
        result = await fetch_nekos(category)
        if not result:
            await interaction.followup.send("Could not fetch GIF. Try again!", ephemeral=True)
            return
        invoker = interaction.user
        await interaction.followup.send(view=action_view(category, invoker, target, result))

    @anime.command(name="hug", description="Hug someone (or yourself)")
    @app_commands.describe(target="Who to hug")
    async def hug(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "hug", target)

    @anime.command(name="pat", description="Pat someone")
    @app_commands.describe(target="Who to pat")
    async def pat(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "pat", target)

    @anime.command(name="kiss", description="Kiss someone")
    @app_commands.describe(target="Who to kiss")
    async def kiss(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "kiss", target)

    @anime.command(name="slap", description="Slap someone")
    @app_commands.describe(target="Who to slap")
    async def slap(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "slap", target)

    @anime.command(name="cuddle", description="Cuddle with someone")
    @app_commands.describe(target="Who to cuddle with")
    async def cuddle(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "cuddle", target)

    @anime.command(name="poke", description="Poke someone")
    @app_commands.describe(target="Who to poke")
    async def poke(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "poke", target)

    @anime.command(name="bite", description="Bite someone")
    @app_commands.describe(target="Who to bite")
    async def bite(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "bite", target)

    @anime.command(name="punch", description="Punch someone")
    @app_commands.describe(target="Who to punch")
    async def punch(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "punch", target)

    @anime.command(name="wave", description="Wave at someone")
    @app_commands.describe(target="Who to wave at")
    async def wave(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "wave", target)

    @anime.command(name="wink", description="Wink at someone")
    @app_commands.describe(target="Who to wink at")
    async def wink(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "wink", target)

    @anime.command(name="cry", description="Cry (on someone's shoulder)")
    @app_commands.describe(target="Whose shoulder to cry on")
    async def cry(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "cry", target)

    @anime.command(name="blush", description="Blush at someone")
    @app_commands.describe(target="Who makes you blush")
    async def blush(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "blush", target)

    @anime.command(name="smile", description="Smile at someone")
    @app_commands.describe(target="Who to smile at")
    async def smile(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "smile", target)

    @anime.command(name="dance", description="Dance with someone")
    @app_commands.describe(target="Who to dance with")
    async def dance(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "dance", target)

    @anime.command(name="happy", description="Celebrate with someone")
    @app_commands.describe(target="Who to celebrate with")
    async def happy(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "happy", target)

    @anime.command(name="laugh", description="Laugh with someone")
    @app_commands.describe(target="Who to laugh with")
    async def laugh(self, interaction: discord.Interaction, target: discord.Member = None):
        await self._action(interaction, "laugh", target)

    # -- Help --

    @anime.command(name="help", description="List all anime commands")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=help_view(), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(AnimeCog(bot))
