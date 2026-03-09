import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import random

NEKOS_BASE = "https://nekos.best/api/v2"
USER_AGENT = "AnimeBot/1.0 (https://github.com/osfv/Anime-Discord-Bot)"

# Accent colors per category feel
COLORS = {
    "hug":       0xF4A7B9,
    "pat":       0xFFD6A5,
    "kiss":      0xFF85A1,
    "slap":      0xFF6B6B,
    "cuddle":    0xC9B8F0,
    "poke":      0x98D8C8,
    "bite":      0xFF9F7F,
    "punch":     0xFF6B6B,
    "cry":       0x91BEF2,
    "blush":     0xFFB3C6,
    "smile":     0xFFF0A0,
    "wave":      0xA8E6CF,
    "dance":     0xD4A8FF,
    "happy":     0xFFF176,
    "wink":      0xFFD6F5,
    "laugh":     0xFFE0A0,
    "neko":      0xB5D8FF,
    "waifu":     0xFFB3D9,
    "kitsune":   0xFFD0A0,
    "default":   0x2B2D31,
}

ACTION_VERBS = {
    "hug":     ("{user} hugs {target}", "{user} hugged themselves... comfort arc."),
    "pat":     ("{user} pats {target}", "{user} pats themselves on the head."),
    "kiss":    ("{user} kisses {target}", "{user} blows a kiss into the void."),
    "slap":    ("{user} slaps {target}", "{user} slaps themselves. Discipline."),
    "cuddle":  ("{user} cuddles {target}", "{user} cuddles themselves. Valid."),
    "poke":    ("{user} pokes {target}", "{user} pokes the air."),
    "bite":    ("{user} bites {target}", "{user} bites themselves. Weird but ok."),
    "punch":   ("{user} punches {target}", "{user} throws a punch at the air."),
    "wave":    ("{user} waves at {target}", "{user} waves at nobody. Brave."),
    "wink":    ("{user} winks at {target}", "{user} winks at the mirror."),
    "cry":     ("{user} cries on {target}'s shoulder", "{user} cries alone."),
    "blush":   ("{user} blushes at {target}", "{user} blushes at their own reflection."),
    "smile":   ("{user} smiles at {target}", "{user} smiles to themselves."),
    "dance":   ("{user} dances with {target}", "{user} dances alone. Iconic."),
    "happy":   ("{user} is happy with {target}", "{user} radiates happiness."),
    "laugh":   ("{user} laughs with {target}", "{user} laughs at their own jokes."),
}

_session: aiohttp.ClientSession | None = None

async def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(headers={"User-Agent": USER_AGENT})
    return _session


async def fetch_nekos(category: str, amount: int = 1) -> list[dict]:
    url = f"{NEKOS_BASE}/{category}?amount={amount}"
    session = await _get_session()
    async with session.get(url) as resp:
        if resp.status != 200:
            return []
        data = await resp.json()
        return data.get("results", [])


def build_action_view(category: str, invoker: discord.User, target: discord.User | None, result: dict) -> discord.ui.LayoutView:
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

    meta_parts = []
    if anime_name:
        meta_parts.append(f"**Anime:** {anime_name}")
    if artist_name:
        if artist_href:
            meta_parts.append(f"**Art by:** [{artist_name}]({artist_href})")
        else:
            meta_parts.append(f"**Art by:** {artist_name}")
    meta_text = "\n".join(meta_parts) if meta_parts else ""

    class ActionLayout(discord.ui.LayoutView):
        container = discord.ui.Container(accent_colour=discord.Colour(color))

        header = discord.ui.TextDisplay(f"## {title}")
        container.add_item(header)

        sep1 = discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
        container.add_item(sep1)

        gallery = discord.ui.MediaGallery(discord.ui.MediaGalleryItem(image_url))
        container.add_item(gallery)

        if meta_text:
            sep2 = discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
            container.add_item(sep2)
            meta = discord.ui.TextDisplay(f"-# {meta_text}")
            container.add_item(meta)

    return ActionLayout()


def build_image_view(category: str, result: dict, invoker: discord.User) -> discord.ui.LayoutView:
    color = COLORS.get(category, COLORS["default"])
    image_url = result.get("url", "")
    artist_name = result.get("artist_name", "")
    artist_href = result.get("artist_href", "")
    source_url = result.get("source_url", "")

    label_map = {"neko": "Neko", "waifu": "Waifu", "kitsune": "Kitsune", "husb": "Husb"}
    label = label_map.get(category, category.title())

    meta_parts = []
    if artist_name:
        if artist_href:
            meta_parts.append(f"**Art by:** [{artist_name}]({artist_href})")
        else:
            meta_parts.append(f"**Art by:** {artist_name}")
    if source_url:
        meta_parts.append(f"[Source]({source_url})")
    meta_text = "  \u00b7  ".join(meta_parts) if meta_parts else ""

    class ImageLayout(discord.ui.LayoutView):
        container = discord.ui.Container(accent_colour=discord.Colour(color))

        header_text = discord.ui.TextDisplay(f"## {label}")
        container.add_item(header_text)

        sep = discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
        container.add_item(sep)

        gallery = discord.ui.MediaGallery(discord.ui.MediaGalleryItem(image_url))
        container.add_item(gallery)

        if meta_text:
            sep2 = discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
            container.add_item(sep2)
            meta = discord.ui.TextDisplay(f"-# {meta_text}")
            container.add_item(meta)

        footer_sep = discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
        container.add_item(footer_sep)

        footer = discord.ui.TextDisplay(f"-# Requested by {invoker.display_name}")
        container.add_item(footer)

    return ImageLayout()


def build_error_view(message: str) -> discord.ui.LayoutView:
    class ErrorLayout(discord.ui.LayoutView):
        container = discord.ui.Container(accent_colour=discord.Colour(0xFF6B6B))
        text = discord.ui.TextDisplay(f"### Something went wrong\n{message}")
        container.add_item(text)
    return ErrorLayout()


class Anime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_unload(self):
        global _session
        if _session and not _session.closed:
            await _session.close()
            _session = None

    # -- Image commands ------------------------------------------------------

    @app_commands.command(name="neko", description="Get a random neko image.")
    async def neko(self, interaction: discord.Interaction):
        await interaction.response.defer()
        results = await fetch_nekos("neko")
        if not results:
            await interaction.followup.send(view=build_error_view("Could not fetch from nekos.best."), flags=discord.MessageFlags.is_components_v2)
            return
        await interaction.followup.send(view=build_image_view("neko", results[0], interaction.user), flags=discord.MessageFlags.is_components_v2)

    @app_commands.command(name="waifu", description="Get a random waifu image.")
    async def waifu(self, interaction: discord.Interaction):
        await interaction.response.defer()
        results = await fetch_nekos("waifu")
        if not results:
            await interaction.followup.send(view=build_error_view("Could not fetch from nekos.best."), flags=discord.MessageFlags.is_components_v2)
            return
        await interaction.followup.send(view=build_image_view("waifu", results[0], interaction.user), flags=discord.MessageFlags.is_components_v2)

    @app_commands.command(name="kitsune", description="Get a random kitsune image.")
    async def kitsune(self, interaction: discord.Interaction):
        await interaction.response.defer()
        results = await fetch_nekos("kitsune")
        if not results:
            await interaction.followup.send(view=build_error_view("Could not fetch from nekos.best."), flags=discord.MessageFlags.is_components_v2)
            return
        await interaction.followup.send(view=build_image_view("kitsune", results[0], interaction.user), flags=discord.MessageFlags.is_components_v2)

    @app_commands.command(name="husb", description="Get a random husb image.")
    async def husb(self, interaction: discord.Interaction):
        await interaction.response.defer()
        results = await fetch_nekos("husb")
        if not results:
            await interaction.followup.send(view=build_error_view("Could not fetch from nekos.best."), flags=discord.MessageFlags.is_components_v2)
            return
        await interaction.followup.send(view=build_image_view("husb", results[0], interaction.user), flags=discord.MessageFlags.is_components_v2)

    # -- Action commands -----------------------------------------------------

    async def _action(self, interaction: discord.Interaction, category: str, target: discord.Member | None):
        await interaction.response.defer()
        results = await fetch_nekos(category)
        if not results:
            await interaction.followup.send(view=build_error_view("Could not fetch from nekos.best."), flags=discord.MessageFlags.is_components_v2)
            return
        view = build_action_view(category, interaction.user, target, results[0])
        await interaction.followup.send(view=view, flags=discord.MessageFlags.is_components_v2)

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

    # -- Info ----------------------------------------------------------------

    @app_commands.command(name="anime_help", description="List all anime bot commands.")
    async def anime_help(self, interaction: discord.Interaction):
        class HelpLayout(discord.ui.LayoutView):
            container = discord.ui.Container(accent_colour=discord.Colour(0xB5D8FF))

            title = discord.ui.TextDisplay("## Anime Bot Commands")
            container.add_item(title)

            sep = discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
            container.add_item(sep)

            images_text = discord.ui.TextDisplay(
                "### Images\n"
                "`/neko` `/waifu` `/kitsune` `/husb`\n"
                "Get a random SFW anime image."
            )
            container.add_item(images_text)

            sep2 = discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
            container.add_item(sep2)

            actions_text = discord.ui.TextDisplay(
                "### Actions\n"
                "`/hug` `/pat` `/kiss` `/slap` `/cuddle` `/poke`\n"
                "`/bite` `/punch` `/cry` `/blush` `/smile` `/wave`\n"
                "`/dance` `/happy` `/wink` `/laugh`\n\n"
                "All action commands accept an optional `target` to mention someone."
            )
            container.add_item(actions_text)

            sep3 = discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
            container.add_item(sep3)

            footer = discord.ui.TextDisplay("-# Powered by [nekos.best](https://nekos.best)")
            container.add_item(footer)

        await interaction.response.send_message(view=HelpLayout(), flags=discord.MessageFlags.is_components_v2, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Anime(bot))
