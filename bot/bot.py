import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Discord intents
intents = discord.Intents.default()


class RustWipeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self):
        """Automatically load all command files."""
        commands_folder = Path("commands")

        for file in commands_folder.glob("*.py"):

            # Ignore private files
            if file.name.startswith("_"):
                continue

            # Ignore empty placeholder files
            if file.stat().st_size == 0:
                continue

            extension = f"commands.{file.stem}"

            try:
                await self.load_extension(extension)
                print(f"✅ Loaded {extension}")
            except Exception as e:
                print(f"❌ Failed to load {extension}")
                print(e)

        # Sync slash commands
        synced = await self.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")

    async def on_ready(self):
        print("=" * 40)
        print(f"Logged in as {self.user}")
        print("Rust Wipe Bot is ONLINE!")
        print("=" * 40)


bot = RustWipeBot()


def run_bot():
    if TOKEN is None:
        raise ValueError(
            "DISCORD_TOKEN not found.\n"
            "Check your .env file."
        )

    bot.run(TOKEN)