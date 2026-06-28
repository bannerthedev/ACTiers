import discord
import asyncio
import traceback
import sys
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()


try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

# ------------- CONFIG (FILL THESE) -------------

# All guild IDs that should have these commands
GUILD_IDS = [
    1459768915432571135,  # guild 1 (current)
    1514480039003951134,  # guild 2
    1514489779423805492,  # guild 3
    1514488993058652210,  # guild 4
    1514485756419113161,  # guild 5
    1514487457649791017,  # guild 6
    1514486529978798222,  # guild 7
    1514487069383200910,  # guild 8
]

GUILDS = [discord.Object(id=g_id) for g_id in GUILD_IDS]

# Per-guild configuration; fill each guild entry
GUILD_CONFIG: dict[int, dict] = {
    # ---------------- GUILD 1 (your current server) ----------------
    1459768915432571135: {
        "TESTER_ROLE_ID": 1460598908509225165,

        "HT3_ROLE_ID": 1459770802458333318,
        "LT2_ROLE_ID": 1459770891171794984,
        "HT2_ROLE_ID": 1459771049355903088,
        "LT1_ROLE_ID": 1459771133179068457,
        "HT1_ROLE_ID": 1459771212380111010,

        "RANK_ROLE_IDS": {
            1459771212380111010,
            1459771133179068457,
            1459771049355903088,
            1459770891171794984,
            1459770802458333318,
            1459770716177170453,
            1459770642688905216,
            1459770572203364423,
            1459770467727704209,
            1459770306410315967,
        },

        "WAITLIST_CATEGORY_MAP": {
            "NA": 1499681150421962974,
            "EU": 1499680386177962055,
            "AS": 1499682180509466674,
        },

        "WAITROOM_CHANNEL_MAP": {
            "NA": 1514458799803596800,
            "EU": 1514458777271926886,
            "AS": 1514458641762353292,
        },

        "WAITLIST_ROLE_MAP": {
            "NA": 1499677030529105940,
            "EU": 1492836520317550753,
            "AS": 1499677081326456893,
        },

        "RESULTS_CHANNEL_ID": 1500142462918852659,
        "LOGO_EMOJI_ID": 1514492244697153596,

        "RANK_NAME_TO_ROLE_ID": {
            "High Tier 5": 1459770467727704209,
            "Low Tier 5": 1459770306410315967,
            "High Tier 4": 1459770642688905216,
            "Low Tier 4": 1459770572203364423,
            "High Tier 3": 1459770802458333318,
            "Low Tier 3": 1459770716177170453,
            "High Tier 2": 1459771049355903088,
            "Low Tier 2": 1459770891171794984,
            "High Tier 1": 1459771212380111010,
            "Low Tier 1": 1459771133179068457,
        },

        "WAITROOM_TEXT": {
            "offline_title": "[1.21+] Sword PvP Community",
            "offline_description": (
                "No Testers Online\n\n"
                "No testers for your region are available at this time.\n"
                "You will be pinged when a tester is available.\n"
                "Check back later!"
            ),
            "online_title": "Tester(s) Available!",
            "online_header": (
                "Tester(s) Available!\n\n"
                "⏱️ The queue updates every 1 minute.\n"
                "Use /leave if you wish to be removed from the waitlist or queue.\n\n"
            ),
            "queue_empty_text": "Queue: Empty",
            "queue_label": "Queue:",
            "testers_label": "Active Testers:",
        },
    },

    # ---------------- GUILD 2 ----------------
    1514480039003951134: {
        "TESTER_ROLE_ID": 1514480039025184888,
        "HT3_ROLE_ID": 1514480039016529925,
        "LT2_ROLE_ID": 1514480039016529926,
        "HT2_ROLE_ID": 1514480039016529927,
        "LT1_ROLE_ID": 1514480039016529928,
        "HT1_ROLE_ID": 1514480039016529929,

        "RANK_ROLE_IDS": set(),

        "WAITLIST_CATEGORY_MAP": {
            "NA": 1514480042904916054,
            "EU": 1514480042904916056,
            "AS": 1514480042904916058,
        },

        "WAITROOM_CHANNEL_MAP": {
            "NA": 1514480042904916055,
            "EU": 1514480042904916057,
            "AS": 1514480043101786152,
        },

        "WAITLIST_ROLE_MAP": {
            "NA": 1514480039003951136,
            "EU": 1514480039003951137,
            "AS": 1514480039003951135,
        },

        "RESULTS_CHANNEL_ID": 1514480042682351708,
        "LOGO_EMOJI_ID": 0,

        "RANK_NAME_TO_ROLE_ID": {
            "High Tier 5": 1514480039016529921,
            "Low Tier 5": 1514480039016529920,
            "High Tier 4": 1514480039016529923,
            "Low Tier 4": 1514480039016529922,
            "High Tier 3": 1514480039016529925,
            "Low Tier 3": 1514480039016529924,
            "High Tier 2": 1514480039016529927,
            "Low Tier 2": 1514480039016529926,
            "High Tier 1": 1514480039016529929,
            "Low Tier 1": 1514480039016529928,
        },

        "WAITROOM_TEXT": {
            "offline_title": "[1.21+] Mace PvP Community",
            "offline_description": (
                "No Testers Online\n\n"
                "No testers for your region are available at this time.\n"
                "You will be pinged when a tester is available.\n"
                "Check back later!"
            ),
            "online_title": "Staff Available!",
            "online_header": "Staff are now available.\n\n",
            "queue_empty_text": "Queue: Empty",
            "queue_label": "Queue:",
            "testers_label": "Available Staff:",
        },
    },

    # ---------------- GUILD 3 ----------------
    1514489779423805492: {
        "TESTER_ROLE_ID": 1514489779444650004,
        "HT3_ROLE_ID": 1514489779436130309,
        "LT2_ROLE_ID": 1514489779436130310,
        "HT2_ROLE_ID": 1514489779436130311,
        "LT1_ROLE_ID": 1514489779436130312,
        "HT1_ROLE_ID": 1514489779436130313,

        "RANK_ROLE_IDS": set(),

        "WAITLIST_CATEGORY_MAP": {
            "NA": 1514489784649646117,
            "EU": 1514489784649646119,
            "AS": 1514489785039978618,
        },

        "WAITROOM_CHANNEL_MAP": {
            "NA": 1514489784649646118,
            "EU": 1514489785039978617,
            "AS": 1514489785039978619,
        },

        "WAITLIST_ROLE_MAP": {
            "NA": 1514489779423805495,
            "EU": 1514489779423805494,
            "AS": 1514489779423805493,
        },

        "RESULTS_CHANNEL_ID": 1514489784381476908,
        "LOGO_EMOJI_ID": 0,

        "RANK_NAME_TO_ROLE_ID": {
            "High Tier 1": 1514489779436130313,
            "Low Tier 1": 1514489779436130312,
            "High Tier 2": 1514489779436130311,
            "Low Tier 2": 1514489779436130310,
            "High Tier 3": 1514489779436130309,
            "Low Tier 3": 1514489779436130308,
            "High Tier 4": 1514489779436130307,
            "Low Tier 4": 1514489779436130306,
            "High Tier 5": 1514489779436130305,
            "Low Tier 5": 1514489779436130304,
        },

        "WAITROOM_TEXT": {
            "offline_title": "[1.21+] Axe PvP Community",
            "offline_description": (
                "No Testers Online\n\n"
                "No testers for your region are available at this time.\n"
                "You will be pinged when a tester is available.\n"
                "Check back later!"
            ),
            "online_title": "Tester(s) Available!",
            "online_header": "Tester(s) online.\n\n",
            "queue_empty_text": "Queue: Empty",
            "queue_label": "Queue:",
            "testers_label": "Active Testers:",
        },
    },

    # ---------------- GUILD 4 ----------------
    1514488993058652210: {
        "TESTER_ROLE_ID": 1514488993113182299,
        "HT3_ROLE_ID": 1514488993088147491,
        "LT2_ROLE_ID": 1514488993088147492,
        "HT2_ROLE_ID": 1514488993088147493,
        "LT1_ROLE_ID": 1514488993088147494,
        "HT1_ROLE_ID": 1514488993088147495,

        "RANK_ROLE_IDS": set(),

        "WAITLIST_CATEGORY_MAP": {
            "NA": 1514488994333982795,
            "EU": 1514488994333982797,
            "AS": 1514488994333982799,
        },

        "WAITROOM_CHANNEL_MAP": {
            "NA": 1514488994333982796,
            "EU": 1514488994333982798,
            "AS": 1514488994560479332,
        },

        "WAITLIST_ROLE_MAP": {
            "NA": 1514488993058652213,
            "EU": 1514488993058652212,
            "AS": 1514488993058652211,
        },

        "RESULTS_CHANNEL_ID": 1514488994195443744,
        "LOGO_EMOJI_ID": 0,

        "RANK_NAME_TO_ROLE_ID": {
            "High Tier 1": 1514488993088147495,
            "Low Tier 1": 1514488993088147494,
            "High Tier 2": 1514488993088147493,
            "Low Tier 2": 1514488993088147492,
            "High Tier 3": 1514488993088147491,
            "Low Tier 3": 1514488993088147490,
            "High Tier 4": 1514488993088147489,
            "Low Tier 4": 1514488993088147488,
            "High Tier 5": 1514488993088147487,
            "Low Tier 5": 1514488993088147486,
        },

        "WAITROOM_TEXT": {
            "offline_title": "[1.21+] UHC PvP Community",
            "offline_description": (
                "No Testers Online\n\n"
                "No testers for your region are available at this time.\n"
                "You will be pinged when a tester is available.\n"
                "Check back later!"
            ),
            "online_title": "Tester(s) Available!",
            "online_header": "Tester(s) online.\n\n",
            "queue_empty_text": "Queue: Empty",
            "queue_label": "Queue:",
            "testers_label": "Active Testers:",
        },
    },

    # ---------------- GUILD 5 ----------------
    1514485756419113161: {
        "TESTER_ROLE_ID": 1514485756507455619,
        "HT3_ROLE_ID": 1514485756469710853,
        "LT2_ROLE_ID": 1514485756469710854,
        "HT2_ROLE_ID": 1514485756469710855,
        "LT1_ROLE_ID": 1514485756469710854,
        "HT1_ROLE_ID": 1514485756469710857,

        "RANK_ROLE_IDS": set(),

        "WAITLIST_CATEGORY_MAP": {
            "NA": 1514485758445224111,
            "EU": 1514485758445224113,
            "AS": 1514485758445224115,
        },

        "WAITROOM_CHANNEL_MAP": {
            "NA": 1514485758445224112,
            "EU": 1514485758445224114,
            "AS": 1514485758566596648,
        },

        "WAITLIST_ROLE_MAP": {
            "NA": 1514485756419113164,
            "EU": 1514485756419113163,
            "AS": 1514485756419113162,
        },

        "RESULTS_CHANNEL_ID": 1514485758260678799,
        "LOGO_EMOJI_ID": 0,

        "RANK_NAME_TO_ROLE_ID": {
            "High Tier 1": 1514485756469710857,
            "Low Tier 1": 1514485756469710856,
            "High Tier 2": 1514485756469710855,
            "Low Tier 2": 1514485756469710854,
            "High Tier 3": 1514485756469710853,
            "Low Tier 3": 1514485756469710852,
            "High Tier 4": 1514485756469710851,
            "Low Tier 4": 1514485756469710850,
            "High Tier 5": 1514485756469710849,
            "Low Tier 5": 1514485756469710848,
        },

        "WAITROOM_TEXT": {
            "offline_title": "[1.21+] Pot PvP Community",
            "offline_description": (
                "No Testers Online\n\n"
                "No testers for your region are available at this time.\n"
                "You will be pinged when a tester is available.\n"
                "Check back later!"
            ),
            "online_title": "Tester(s) Available!",
            "online_header": "Tester(s) online.\n\n",
            "queue_empty_text": "Queue: Empty",
            "queue_label": "Queue:",
            "testers_label": "Active Testers:",
        },
    },

    # ---------------- GUILD 6 ----------------
    1514487457649791017: {
        "TESTER_ROLE_ID": 1514487457670893650,
        "HT3_ROLE_ID": 1514487457666695195,
        "LT2_ROLE_ID": 1514487457666695196,
        "HT2_ROLE_ID": 1514487457666695197,
        "LT1_ROLE_ID": 1514487457666695198,
        "HT1_ROLE_ID": 1514487457666695199,

        "RANK_ROLE_IDS": set(),

        "WAITLIST_CATEGORY_MAP": {
            "NA": 1514487461215080503,
            "EU": 1514487461215080505,
            "AS": 1514487461215080507,
        },

        "WAITROOM_CHANNEL_MAP": {
            "NA": 1514487461215080504,
            "EU": 1514487461215080506,
            "AS": 1514487461336584343,
        },

        "WAITLIST_ROLE_MAP": {
            "NA": 1514487457649791020,
            "EU": 1514487457649791019,
            "AS": 1514487457649791018,
        },

        "RESULTS_CHANNEL_ID": 1514487461051629670,
        "LOGO_EMOJI_ID": 0,

        "RANK_NAME_TO_ROLE_ID": {
            "High Tier 1": 1514487457666695199,
            "Low Tier 1": 1514487457666695198,
            "High Tier 2": 1514487457666695197,
            "Low Tier 2": 1514487457666695196,
            "High Tier 3": 1514487457666695195,
            "Low Tier 3": 1514487457666695194,
            "High Tier 4": 1514487457666695193,
            "Low Tier 4": 1514487457666695192,
            "High Tier 5": 1514487457666695191,
            "Low Tier 5": 1514487457666695190,
        },

        "WAITROOM_TEXT": {
            "offline_title": "[1.21+] SMP PvP Community",
            "offline_description": (
                "No Testers Online\n\n"
                "No testers for your region are available at this time.\n"
                "You will be pinged when a tester is available.\n"
                "Check back later!"
            ),
            "online_title": "Tester(s) Available!",
            "online_header": "Tester(s) online.\n\n",
            "queue_empty_text": "Queue: Empty",
            "queue_label": "Queue:",
            "testers_label": "Active Testers:",
        },
    },

    # ---------------- GUILD 7 ----------------
    1514486529978798222: {
        "TESTER_ROLE_ID": 1514486530000027698,
        "HT3_ROLE_ID": 1514486529991512070,
        "LT2_ROLE_ID": 1514486529991512071,
        "HT2_ROLE_ID": 1514486529991512072,
        "LT1_ROLE_ID": 1514486529991512073,
        "HT1_ROLE_ID": 1514486529991512074,

        "RANK_ROLE_IDS": set(),

        "WAITLIST_CATEGORY_MAP": {
            "NA": 1514486530880831553,
            "EU": 1514486530880831555,
            "AS": 1514486530880831557,
        },

        "WAITROOM_CHANNEL_MAP": {
            "NA": 1514486530880831554,
            "EU": 1514486530880831556,
            "AS": 1514486531014791258,
        },

        "WAITLIST_ROLE_MAP": {
            "NA": 1514486529978798225,
            "EU": 1514486529978798224,
            "AS": 1514486529978798223,
        },

        "RESULTS_CHANNEL_ID": 1514486530742292502,
        "LOGO_EMOJI_ID": 0,

        "RANK_NAME_TO_ROLE_ID": {
            "High Tier 1": 1514486529991512074,
            "Low Tier 1": 1514486529991512073,
            "High Tier 2": 1514486529991512072,
            "Low Tier 2": 1514486529991512071,
            "High Tier 3": 1514486529991512070,
            "Low Tier 3": 1514486529991512069,
            "High Tier 4": 1514486529991512068,
            "Low Tier 4": 1514486529991512067,
            "High Tier 5": 1514486529991512066,
            "Low Tier 5": 1514486529991512065,
        },

        "WAITROOM_TEXT": {
            "offline_title": "[1.21+] Vanilla PvP Community",
            "offline_description": (
                "No Testers Online\n\n"
                "No testers for your region are available at this time.\n"
                "You will be pinged when a tester is available.\n"
                "Check back later!"
            ),
            "online_title": "Tester(s) Available!",
            "online_header": "Tester(s) online.\n\n",
            "queue_empty_text": "Queue: Empty",
            "queue_label": "Queue:",
            "testers_label": "Active Testers:",
        },
    },

    # ---------------- GUILD 8 ----------------
    1514487069383200910: {
        "TESTER_ROLE_ID": 1514487069513351168,
        "HT3_ROLE_ID": 1514487069471150167,
        "LT2_ROLE_ID": 1514487069471150168,
        "HT2_ROLE_ID": 1514487069471150169,
        "LT1_ROLE_ID": 1514487069471150170,
        "HT1_ROLE_ID": 1514487069471150171,

        "RANK_ROLE_IDS": set(),

        "WAITLIST_CATEGORY_MAP": {
            "NA": 1514487072281460788,
            "EU": 1514487072281460790,
            "AS": 1514487072281460792,
        },

        "WAITROOM_CHANNEL_MAP": {
            "NA": 1514487072281460789,
            "EU": 1514487072281460791,
            "AS": 1514487072281460793,
        },

        "WAITLIST_ROLE_MAP": {
            "NA": 1514487069383200913,
            "EU": 1514487069383200912,
            "AS": 1514487069383200911,
        },

        "RESULTS_CHANNEL_ID": 1514487071526359210,
        "LOGO_EMOJI_ID": 0,

        "RANK_NAME_TO_ROLE_ID": {
            "High Tier 1": 1514487069471150171,
            "Low Tier 1": 1514487069471150170,
            "High Tier 2": 1514487069471150169,
            "Low Tier 2": 1514487069471150168,
            "High Tier 3": 1514487069471150167,
            "Low Tier 3": 1514487069471150166,
            "High Tier 4": 1514487069471150165,
            "Low Tier 4": 1514487069471150164,
            "High Tier 5": 1514487069471150163,
            "Low Tier 5": 1514487069471150162,
        },

        "WAITROOM_TEXT": {
            "offline_title": "[1.21+] Netherite Pot PvP Community",
            "offline_description": (
                "No Testers Online\n\n"
                "No testers for your region are available at this time.\n"
                "You will be pinged when a tester is available.\n"
                "Check back later!"
            ),
            "online_title": "Tester(s) Available!",
            "online_header": "Tester(s) online.\n\n",
            "queue_empty_text": "Queue: Empty",
            "queue_label": "Queue:",
            "testers_label": "Active Testers:",
        },
    },
}

COOLDOWN_MONTHS = 1

# ------------- STATE -------------

cooldowns: dict[int, datetime] = {}  # global per user
user_submissions: dict[int, dict[str, str]] = {}  # user_id -> {"ign","region","server"}

# per-guild region data
last_testing_session: dict[int, dict[str, datetime]] = {}
region_queues: dict[int, dict[str, list[int]]] = {}
active_testers: dict[int, dict[str, set[int]]] = {}
queue_messages: dict[int, dict[str, tuple[int, int]]] = {}  # guild_id -> region_key -> (channel_id, msg_id)
ticket_owners: dict[int, int] = {}  # channel_id -> owner user_id

# ------------- BOT SETUP -------------

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ------------- HELPERS -------------

REGION_CHOICES = [
    app_commands.Choice(name="NA", value="NA"),
    app_commands.Choice(name="EU", value="EU"),
    app_commands.Choice(name="AS", value="AS"),
]


def get_config(guild: discord.Guild | None) -> dict:
    if guild is None:
        return {}
    return GUILD_CONFIG.get(guild.id, {})


def region_key_clean(region: str) -> str:
    r = (region or "").upper().strip()
    return r if r in ("NA", "EU", "AS") else "NA"


def ensure_guild_structs(guild_id: int):
    if guild_id not in region_queues:
        region_queues[guild_id] = {"NA": [], "EU": [], "AS": []}
    if guild_id not in active_testers:
        active_testers[guild_id] = {"NA": set(), "EU": set(), "AS": set()}
    if guild_id not in queue_messages:
        queue_messages[guild_id] = {}
    if guild_id not in last_testing_session:
        last_testing_session[guild_id] = {}


async def get_waitlist_category(guild: discord.Guild, region: str):
    cfg = get_config(guild)
    cat_map = cfg.get("WAITLIST_CATEGORY_MAP", {})
    default_cat_id = cat_map.get("NA")
    key = region_key_clean(region)
    cid = cat_map.get(key, default_cat_id)
    ch = guild.get_channel(cid) if cid else None
    return ch if isinstance(ch, discord.CategoryChannel) else None


async def get_waitroom_channel(guild: discord.Guild, region_key: str):
    cfg = get_config(guild)
    wr_map = cfg.get("WAITROOM_CHANNEL_MAP", {})
    default_ch_id = wr_map.get("NA")
    cid = wr_map.get(region_key_clean(region_key), default_ch_id)
    ch = guild.get_channel(cid) if cid else None
    return ch if isinstance(ch, discord.TextChannel) else None


def is_high_rank(member: discord.Member) -> bool:
    cfg = get_config(member.guild)
    high_ids = {
        cfg.get("HT3_ROLE_ID"),
        cfg.get("LT2_ROLE_ID"),
        cfg.get("HT2_ROLE_ID"),
        cfg.get("LT1_ROLE_ID"),
        cfg.get("HT1_ROLE_ID"),
    }
    high_ids = {i for i in high_ids if i}
    return any(role.id in high_ids for role in member.roles)


def get_region_from_topic_raw(channel: discord.TextChannel) -> str:
    if channel.topic and str(channel.topic).startswith("Region:"):
        return channel.topic.split(":", 1)[1].strip()
    return "UNKNOWN"


def format_last_session(guild_id: int, region_key: str) -> str:
    region_key = region_key_clean(region_key)
    dt = last_testing_session.get(guild_id, {}).get(region_key)
    if not dt:
        return "Last testing session: No tests recorded yet."
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    if ZoneInfo is not None:
        est = dt.astimezone(ZoneInfo("America/New_York"))
        cst = dt.astimezone(ZoneInfo("America/Chicago"))
        return (
            "Last testing session:\n"
            f"- EST: {est:%Y-%m-%d %I:%M %p} (EST)\n"
            f"- CST: {cst:%Y-%m-%d %I:%M %p} (CST)"
        )
    return f"Last testing session: {dt.astimezone(timezone.utc):%Y-%m-%d %H:%M UTC}"


def get_previous_rank(member: discord.Member) -> str:
    cfg = get_config(member.guild)
    rank_role_ids = cfg.get("RANK_ROLE_IDS", set())
    for role in reversed(member.roles):
        if role.id in rank_role_ids:
            return role.name
    return "Unranked"


def tester_role_check():
    async def predicate(interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            return False
        cfg = get_config(guild)
        tester_role_id = cfg.get("TESTER_ROLE_ID")
        if not tester_role_id:
            return False
        return any(r.id == tester_role_id for r in interaction.user.roles)
    return app_commands.check(predicate)

# ------------- UI: Accept button -------------

class AcceptView(discord.ui.View):
    def __init__(self, region_key: str):
        super().__init__(timeout=None)
        self.region_key = region_key

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary, custom_id="waitroom_accept")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = interaction.guild
        if guild is None:
            return await interaction.response.send_message("Guild not found.", ephemeral=True)

        ensure_guild_structs(guild.id)
        cfg = get_config(guild)

        region_key = self.region_key

        role_id = cfg.get("WAITLIST_ROLE_MAP", {}).get(region_key)
        if role_id:
            role = guild.get_role(role_id)
            if role and role not in user.roles:
                try:
                    await user.add_roles(role, reason="Entered waitlist via Accept button")
                except Exception:
                    pass

        data = user_submissions.get(user.id)
        if not data:
            return await interaction.response.send_message("You must **Verify Account** first.", ephemeral=True)
        ign = data.get("ign", user.display_name)
        server = data.get("server", "Not specified")

        queue = region_queues[guild.id].setdefault(region_key, [])
        if user.id in queue:
            return await interaction.response.send_message("You are already in the queue.", ephemeral=True)

        queue.append(user.id)
        position = queue.index(user.id) + 1
        now = datetime.utcnow()
        cooldowns[user.id] = now + timedelta(days=COOLDOWN_MONTHS * 30)

        ticket_text = ""
        region_active_testers = active_testers[guild.id].get(region_key, set())
        if position == 1 and region_active_testers:
            ticket_channel = await create_ticket_for_user(guild, user, region_key, ign, server)
            if ticket_channel:
                ticket_text = f" Your ticket: {ticket_channel.mention}"

        await update_queue_message(guild, region_key)
        await interaction.response.send_message(
            f"You have been added to the {region_key} waitlist (position #{position}).{ticket_text}",
            ephemeral=True
        )

# ------------- QUEUE MESSAGE UPDATE -------------

async def update_queue_message(guild: discord.Guild, region_key: str):
    ensure_guild_structs(guild.id)
    cfg = get_config(guild)
    guild_id = guild.id
    region_key = region_key_clean(region_key)

    waitroom = await get_waitroom_channel(guild, region_key)
    if waitroom is None:
        print(f"[update_queue_message] waitroom not found for {region_key} in guild {guild_id}")
        return

    queue = region_queues[guild_id].get(region_key, [])
    testers = active_testers[guild_id].get(region_key, set())

    # text config with defaults
    wt = cfg.get("WAITROOM_TEXT", {}) or {}
    offline_title_base = wt.get("offline_title", "Sword PvP Community")
    offline_description = wt.get(
        "offline_description",
        "No Testers Online\n\n"
        "No testers for your region are available at this time.\n"
        "You will be pinged when a tester is available.\n"
        "Check back later!"
    )
    online_title = wt.get("online_title", "Tester(s) Available!")
    online_header = wt.get(
        "online_header",
        "Tester(s) Available!\n\n"
        "⏱️ The queue updates every 1 minute.\n"
        "Use /leave if you wish to be removed from the waitlist or queue.\n\n"
    )
    queue_empty_text = wt.get("queue_empty_text", "Queue: Empty")
    queue_label = wt.get("queue_label", "Queue:")
    testers_label = wt.get("testers_label", "Active Testers:")

    view = None

    try:
        # OFFLINE: no testers
        if not testers:
            emoji_id = cfg.get("LOGO_EMOJI_ID")
            emoji_obj = guild.get_emoji(emoji_id) if emoji_id else None
            emoji_text = str(emoji_obj) if emoji_obj else ""
            title = f"{emoji_text} {offline_title_base}" if emoji_text else offline_title_base

            # add Last testing session line
            last_session_text = format_last_session(guild_id, region_key)
            full_desc = f"{offline_description}\n\n{last_session_text}"

            embed = discord.Embed(title=title, description=full_desc, color=discord.Color.blue())
            if emoji_obj:
                embed.set_thumbnail(url=emoji_obj.url)

            # delete stored message
            old = queue_messages[guild_id].pop(region_key, None)
            if old:
                old_ch_id, old_msg_id = old
                try:
                    old_ch = guild.get_channel(old_ch_id)
                    if isinstance(old_ch, discord.TextChannel):
                        old_msg = await old_ch.fetch_message(old_msg_id)
                        await old_msg.delete()
                except Exception:
                    pass

            # clear channel
            try:
                async for m in waitroom.history(limit=None):
                    try:
                        await m.delete()
                    except Exception:
                        pass
            except Exception:
                pass

            # send new offline embed
            try:
                msg = await waitroom.send(embed=embed)
                queue_messages[guild_id][region_key] = (waitroom.id, msg.id)
            except Exception as e:
                print(
                    f"[update_queue_message] failed to send offline queue message "
                    f"for {region_key} in guild {guild_id}: {e}"
                )
            return

    except Exception as e:
        print(
            f"[update_queue_message] unexpected error for {region_key} in guild {guild_id}: {e}",
            file=sys.stderr
        )
        traceback.print_exc()


# ------------- TICKET CREATION -------------

async def create_ticket_for_user(guild: discord.Guild, user: discord.Member, region_key: str, ign: str, server: str):
    ensure_guild_structs(guild.id)
    cfg = get_config(guild)

    category = await get_waitlist_category(guild, region_key)
    if category is None:
        return None

    previous_rank = get_previous_rank(user)
    sub = user_submissions.get(user.id)
    if sub:
        ign = ign or sub.get("ign", user.display_name)
        server = server or sub.get("server", "Not specified")

    channel_name_raw = f"{region_key} tested {user.display_name}"
    channel_name = channel_name_raw.lower().replace(" ", "-")
    tester_role_id = cfg.get("TESTER_ROLE_ID")
    tester_role = guild.get_role(tester_role_id) if tester_role_id else None

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
    }
    if tester_role is not None:
        overwrites[tester_role] = discord.PermissionOverwrite(
            view_channel=True, send_messages=True, read_message_history=True
        )

    wait_channel = await guild.create_text_channel(
        name=channel_name,
        category=category,
        overwrites=overwrites,
        reason="Evaluation Testing Waitlist"
    )
    try:
        await wait_channel.edit(topic=f"Region:{region_key}")
    except Exception:
        pass

    ticket_owners[wait_channel.id] = user.id

    info_embed = discord.Embed(
        description=(
            f"{user.mention}\n\n"
            f"**User:** {user.mention}\n"
            f"**Region:** {region_key}\n"
            f"**Server:** {server}\n"
            f"**Username (IGN):** {ign}\n"
            f"**Previous Rank:** {previous_rank}"
        ),
        color=discord.Color.red()
    )
    await wait_channel.send(content=user.mention, embed=info_embed)
    return wait_channel


# ------------- MODAL -------------

class VerifyModal(discord.ui.Modal, title="Verify Account"):
    ign = discord.ui.TextInput(label="1. What is your IGN?", max_length=50)
    region = discord.ui.TextInput(label="2. What is your Region? (NA/EU/AS)", max_length=50)
    server = discord.ui.TextInput(label="3. What server do you want to test on?", max_length=50)

    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        user_submissions[interaction.user.id] = {
            "ign": str(self.ign).strip(),
            "region": str(self.region).strip(),
            "server": str(self.server).strip()
        }
        self.parent_view.user_data[interaction.user.id] = user_submissions[interaction.user.id]
        await interaction.response.send_message(
            "✅ Your account has been verified for the waitlist.\nYou can now press **Enter Waitlist**.",
            ephemeral=True
        )


# ------------- MAIN VIEW -------------

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.user_data: dict[int, dict[str, str]] = {}

    @discord.ui.button(label="Verify Account", style=discord.ButtonStyle.primary)
    async def verify_account(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VerifyModal(self))

    @discord.ui.button(label="View Cooldown", style=discord.ButtonStyle.danger)
    async def view_cooldown(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        now = datetime.utcnow()
        if user.id not in cooldowns or cooldowns[user.id] <= now:
            await interaction.response.send_message(
                "You have **no active cooldown**. You can enter the waitlist.",
                ephemeral=True
            )
            return
        remaining = cooldowns[user.id] - now
        days = remaining.days
        hours = remaining.seconds // 3600
        mins = (remaining.seconds % 3600) // 60
        await interaction.response.send_message(
            f"⏳ Time left until you can enter the waitlist again: **{days}d {hours}h {mins}m**.",
            ephemeral=True
        )

    @discord.ui.button(label="Enter Waitlist", style=discord.ButtonStyle.success)
    async def enter_waitlist(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("Guild not found.", ephemeral=True)
            return

        ensure_guild_structs(guild.id)
        cfg = get_config(guild)

        now = datetime.utcnow()
        await interaction.response.defer(ephemeral=True)

        if user.id in cooldowns and cooldowns[user.id] > now:
            remaining = cooldowns[user.id] - now
            days = remaining.days
            hours = remaining.seconds // 3600
            mins = (remaining.seconds % 3600) // 60
            await interaction.followup.send(
                f"⏳ You are still on cooldown for **{days}d {hours}h {mins}m**.",
                ephemeral=True
            )
            return

        data = user_submissions.get(user.id) or self.user_data.get(user.id)
        if not data:
            await interaction.followup.send("You must **Verify Account** first.", ephemeral=True)
            return

        ign = data.get("ign", user.display_name)
        region = data.get("region", "").strip()
        server = data.get("server", "Not specified")

        region_key = region_key_clean(region)

        role_id = cfg.get("WAITLIST_ROLE_MAP", {}).get(region_key)
        if role_id is not None:
            role = guild.get_role(role_id)
            if role is not None and role not in user.roles:
                try:
                    await user.add_roles(role, reason="Entered waitlist")
                except Exception:
                    pass

        queue = region_queues[guild.id].setdefault(region_key, [])
        if user.id not in queue:
            queue.append(user.id)

        position = queue.index(user.id) + 1
        cooldowns[user.id] = now + timedelta(days=COOLDOWN_MONTHS * 30)

        ticket_text = ""
        region_active_testers = active_testers[guild.id].get(region_key, set())
        if position == 1 and region_active_testers:
            ticket_channel = await create_ticket_for_user(guild, user, region_key, ign, server)
            if ticket_channel:
                ticket_text = f" Your ticket: {ticket_channel.mention}"

        await update_queue_message(guild, region_key)
        await interaction.followup.send(
            f"✅ You have been added to the **{region_key}** waitlist.\n"
            f"Your position in queue: **#{position}**.{ticket_text}",
            ephemeral=True
        )


# ------------- /create-ticket -------------

@bot.tree.command(
    name="create-ticket",
    description="Post the Evaluation Testing Waitlist panel.",
    guilds=GUILDS
)
@app_commands.checks.has_permissions(administrator=True)
async def create_ticket(interaction: discord.Interaction, channel: discord.TextChannel):
    text = (
        "📝 **Evaluation Testing Waitlist**\n\n"
        "Upon applying, you will be added to a waitlist queue.\n"
        "You will be pinged when a tester of your region is available.\n"
        "If you are HT3 or higher, a high ticket will be created.\n\n"
        "• Region should be the region of the server you wish to test on\n"
        "• Username should be the name of the account you will be testing on\n\n"
        "🛑 Failure to provide authentic information will result in a denied test."
    )
    embed = discord.Embed(description=text, color=discord.Color.red())
    view = TicketView()
    await channel.send(embed=embed, view=view)

    guild = interaction.guild
    if guild:
        ensure_guild_structs(guild.id)
        await update_queue_message(guild, "NA")
        await update_queue_message(guild, "EU")
        await update_queue_message(guild, "AS")

    await interaction.response.send_message("✅ Waitlist panel created.", ephemeral=True)


# ------------- /start -------------

@bot.tree.command(
    name="start",
    description="(Tester) Mark this region as active (tester now handling this region).",
    guilds=GUILDS
)
@tester_role_check()
@app_commands.describe(region="Region to start (NA/EU/AS)")
@app_commands.choices(region=REGION_CHOICES)
async def start_test(interaction: discord.Interaction, region: app_commands.Choice[str]):
    tester = interaction.user
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("Guild not found.", ephemeral=True)
        return

    ensure_guild_structs(guild.id)

    region_key = region.value
    testers = active_testers[guild.id].setdefault(region_key, set())
    testers.add(tester.id)

    last_testing_session[guild.id][region_key] = datetime.now(timezone.utc)

    await interaction.response.send_message(f"Marked {region_key} as started by {tester.mention}.", ephemeral=True)

    online_embed = discord.Embed(
        title="Tester Available",
        description=f"A tester ({tester.mention}) is now available for **{region_key}**.\nPlease follow their instructions.",
        color=discord.Color.green()
    )
    if isinstance(interaction.channel, discord.TextChannel):
        await interaction.channel.send(embed=online_embed)

    await update_queue_message(guild, region_key)


# ------------- /next -------------

@bot.tree.command(
    name="next",
    description="(Tester) Pull the first person in the region queue into a ticket.",
    guilds=GUILDS
)
@tester_role_check()
@app_commands.describe(region="Region to pull next from (NA/EU/AS)")
@app_commands.choices(region=REGION_CHOICES)
async def next_in_queue(interaction: discord.Interaction, region: app_commands.Choice[str]):
    tester = interaction.user
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("Guild not found.", ephemeral=True)
        return

    ensure_guild_structs(guild.id)

    region_key = region.value
    queue = region_queues[guild.id].get(region_key, [])
    if not queue:
        await interaction.response.send_message(f"The **{region_key}** queue is currently empty.", ephemeral=True)
        return

    user_id = queue.pop(0)
    await update_queue_message(guild, region_key)

    member = guild.get_member(user_id)
    if member is None:
        await interaction.response.send_message(
            f"User <@{user_id}> is no longer in the server. Removed from queue.",
            ephemeral=True
        )
        return

    sub = user_submissions.get(member.id)
    ign = sub.get("ign") if sub else member.display_name
    server = sub.get("server") if sub else "Not specified"

    ticket_channel = await create_ticket_for_user(guild, member, region_key, ign, server)
    if ticket_channel is None:
        await interaction.response.send_message(f"Failed to create a ticket for {member.mention}.", ephemeral=True)
        return

    await interaction.response.send_message(
        f"Pulled {member.mention} from the **{region_key}** queue and created {ticket_channel.mention}.",
        ephemeral=True
    )


# ------------- /stop -------------

@bot.tree.command(
    name="stop",
    description="(Tester) Stop handling tests for a region (remove yourself from active testers).",
    guilds=GUILDS
)
@tester_role_check()
@app_commands.describe(region="Region to stop (NA/EU/AS)")
@app_commands.choices(region=REGION_CHOICES)
async def stop_test(interaction: discord.Interaction, region: app_commands.Choice[str]):
    tester = interaction.user
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("Guild not found.", ephemeral=True)
        return

    ensure_guild_structs(guild.id)

    region_key = region.value
    testers = active_testers[guild.id].setdefault(region_key, set())
    if tester.id in testers:
        testers.remove(tester.id)

    # record last testing session time when a tester stops
    last_testing_session[guild.id][region_key] = datetime.now(timezone.utc)

    # delete stored waitroom message
    old = queue_messages[guild.id].pop(region_key, None)
    if old:
        ch_id, msg_id = old
        try:
            ch = guild.get_channel(ch_id)
            if isinstance(ch, discord.TextChannel):
                msg = await ch.fetch_message(msg_id)
                await msg.delete()
        except Exception:
            pass

    await update_queue_message(guild, region_key)

    await interaction.response.send_message(
        f"You have stopped handling tests for **{region_key}**.",
        ephemeral=True
    )


# ------------- /close -------------

@bot.tree.command(
    name="close",
    description="(Tester) Close this ticket and post the test result.",
    guilds=GUILDS
)
@tester_role_check()
@app_commands.describe(ranking="Rank earned (e.g. 'High Tier 5')")
async def close_test(interaction: discord.Interaction, ranking: str):
    tester = interaction.user
    channel = interaction.channel
    guild = interaction.guild
    if guild is None or not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message("This command can only be used inside a ticket channel.", ephemeral=True)
        return

    ensure_guild_structs(guild.id)
    cfg = get_config(guild)

    # Determine region
    region_raw = get_region_from_topic_raw(channel)
    if region_raw == "UNKNOWN" and channel.category:
        region_raw = channel.category.name.split()[0]
    region_key = region_key_clean(region_raw)
    if region_raw == "UNKNOWN":
        await interaction.response.send_message("This doesn't look like a waitlist ticket channel.", ephemeral=True)
        return

    # Determine target
    target = None
    if ticket_owners.get(channel.id):
        uid = ticket_owners.get(channel.id)
        target = guild.get_member(uid)

    if target is None:
        tester_role_id = cfg.get("TESTER_ROLE_ID")
        tester_role = guild.get_role(tester_role_id) if tester_role_id else None
        for m in channel.members:
            if m.bot:
                continue
            if m.id == tester.id:
                continue
            if tester_role and tester_role in m.roles and len(m.roles) <= 2:
                continue
            target = m
            break

    if target is None:
        await interaction.response.send_message("Couldn't find the user being tested in this channel.", ephemeral=True)
        return

    previous_rank_name = get_previous_rank(target)

    rank_map = cfg.get("RANK_NAME_TO_ROLE_ID", {})
    rank_role_ids = cfg.get("RANK_ROLE_IDS", set())

    role_id_to_give = rank_map.get(ranking)
    new_role_obj = guild.get_role(role_id_to_give) if role_id_to_give else None

    roles_to_remove = [r for r in target.roles if r.id in rank_role_ids]
    try:
        if roles_to_remove:
            await target.remove_roles(*roles_to_remove, reason="Updating rank via /close")
    except Exception:
        pass

    if new_role_obj:
        try:
            await target.add_roles(new_role_obj, reason=f"Rank awarded: {ranking}")
        except Exception:
            pass

    title = f"{target.display_name}'s Test Results 🏆"
    embed = discord.Embed(title=title, color=discord.Color.red())
    embed.add_field(name="Tester:", value=tester.mention, inline=False)
    embed.add_field(name="Region:", value=region_key, inline=False)
    embed.add_field(name="Username:", value=target.display_name, inline=False)
    embed.add_field(name="Previous Rank:", value=previous_rank_name, inline=False)
    embed.add_field(name="Rank Earned:", value=ranking, inline=False)

    content_ping = target.mention
    await channel.send(content=content_ping, embed=embed)

    results_channel_id = cfg.get("RESULTS_CHANNEL_ID")
    results_channel = guild.get_channel(results_channel_id) if results_channel_id else None
    if isinstance(results_channel, discord.TextChannel):
        await results_channel.send(content=content_ping, embed=embed)

    ticket_owners.pop(channel.id, None)

    await interaction.response.send_message("Result posted. This ticket will be deleted shortly.", ephemeral=True)

    try:
        await asyncio.sleep(5)
        await channel.delete(reason="Test closed")
    except Exception:
        pass


# ------------- /leave -------------

@bot.tree.command(
    name="leave",
    description="Leave the waitlist queue for your region.",
    guilds=GUILDS
)
async def leave_queue(interaction: discord.Interaction):
    user = interaction.user
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("Guild not found.", ephemeral=True)
        return

    ensure_guild_structs(guild.id)

    removed_from = []
    for region_key, queue in region_queues[guild.id].items():
        if user.id in queue:
            queue.remove(user.id)
            removed_from.append(region_key)
            await update_queue_message(guild, region_key)

    if not removed_from:
        await interaction.response.send_message(
            "You are not currently in any region waitlist queue.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"You have been removed from the waitlist queue for: {', '.join(removed_from)}.",
        ephemeral=True
    )


# ------------- STARTUP -------------

@bot.event
async def on_ready():
    for g in GUILDS:
        try:
            await bot.tree.sync(guild=g)
            print(f"Synced commands for guild {g.id}")
        except Exception as e:
            print(f"Failed to sync for guild {g.id}: {e}")
    print(f"Ready: {bot.user}")


bot.run(os.getenv("TOKEN"))
