import discord
from discord import app_commands
from discord.ext import commands

from utils.storage import load_schedules
from utils.scheduler import WipeScheduler


class Wipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.scheduler = WipeScheduler()


    @app_commands.command(
        name="wipe",
        description="Show the next Rust wipe time."
    )
    async def wipe(self, interaction: discord.Interaction):

        schedules = load_schedules()

        guild_id = str(interaction.guild.id)

        if guild_id not in schedules:
            await interaction.response.send_message(
                "❌ No wipe schedule has been set yet.",
                ephemeral=True
            )
            return


        schedule = schedules[guild_id]


        weekday_names = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6
        }


        weekday = weekday_names[
            schedule["weekday"].lower()
        ]


        next_wipe, after_that = self.scheduler.get_next_wipes(
            schedule_type=schedule["schedule"],
            week=schedule["week"],
            weekday=weekday,
            time=schedule["time"],
            timezone=schedule["timezone"]
        )


        next_timestamp = int(next_wipe.timestamp())
        after_timestamp = int(after_that.timestamp())


        embed = discord.Embed(
            title="🧻 Rust Wipe",
            color=discord.Color.orange()
        )


        embed.add_field(
            name="📅 Date",
            value=f"<t:{next_timestamp}:D>",
            inline=False
        )


        embed.add_field(
            name="🕒 Time",
            value=f"<t:{next_timestamp}:t>",
            inline=False
        )


        embed.add_field(
            name="⏳ Countdown",
            value=f"⏳ <t:{next_timestamp}:R>",
            inline=False
        )


        embed.add_field(
            name="🔄 After that",
            value=(
                f"📅 <t:{after_timestamp}:D>\n"
                f"🕒 <t:{after_timestamp}:t>\n"
                f"⏳ <t:{after_timestamp}:R>"
            ),
            inline=False
        )


        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Wipe(bot))
