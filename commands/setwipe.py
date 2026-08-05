import discord
from discord import app_commands
from discord.ext import commands

from utils.storage import load_schedules, save_schedules


SCHEDULE_CHOICES = [
    app_commands.Choice(name="Weekly", value="weekly"),
    app_commands.Choice(name="Monthly", value="monthly"),
]


WEEK_CHOICES = [
    app_commands.Choice(name="First", value="first"),
    app_commands.Choice(name="Second", value="second"),
    app_commands.Choice(name="Third", value="third"),
    app_commands.Choice(name="Fourth", value="fourth"),
    app_commands.Choice(name="Last", value="last"),
]


DAY_CHOICES = [
    app_commands.Choice(name="Monday", value="monday"),
    app_commands.Choice(name="Tuesday", value="tuesday"),
    app_commands.Choice(name="Wednesday", value="wednesday"),
    app_commands.Choice(name="Thursday", value="thursday"),
    app_commands.Choice(name="Friday", value="friday"),
    app_commands.Choice(name="Saturday", value="saturday"),
    app_commands.Choice(name="Sunday", value="sunday"),
]


TIMEZONES = [
    "Asia/Kolkata",
    "Asia/Tokyo",
    "Asia/Singapore",
    "Asia/Dubai",
    "Europe/London",
    "Europe/Paris",
    "Europe/Berlin",
    "America/New_York",
    "America/Chicago",
    "America/Los_Angeles",
    "America/Toronto",
    "Australia/Sydney",
    "UTC",
]


async def timezone_autocomplete(
    interaction: discord.Interaction,
    current: str
):
    return [
        app_commands.Choice(
            name=tz,
            value=tz
        )
        for tz in TIMEZONES
        if current.lower() in tz.lower()
    ][:25]


class SetWipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setwipe",
        description="Configure the Rust wipe schedule."
    )
    @app_commands.describe(
        schedule="Weekly or Monthly",
        week="Only for Monthly wipes",
        weekday="Day of wipe",
        time="24 hour format (23:30)",
        timezone="Timezone"
    )
    @app_commands.choices(
        schedule=SCHEDULE_CHOICES,
        week=WEEK_CHOICES,
        weekday=DAY_CHOICES
    )
    @app_commands.autocomplete(
        timezone=timezone_autocomplete
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def setwipe(
        self,
        interaction: discord.Interaction,
        schedule: app_commands.Choice[str],
        weekday: app_commands.Choice[str],
        time: str,
        timezone: str,
        week: app_commands.Choice[str] = None
    ):

        try:
            hour, minute = map(int, time.split(":"))

            if hour > 23 or minute > 59:
                raise ValueError

        except:

            await interaction.response.send_message(
                "❌ Invalid time. Use format `23:30`",
                ephemeral=True
            )
            return


        if schedule.value == "monthly" and week is None:

            await interaction.response.send_message(
                "❌ Monthly wipe requires week selection.",
                ephemeral=True
            )
            return


        if schedule.value == "weekly":
            saved_week = "none"
        else:
            saved_week = week.value


        schedules = load_schedules()


        schedules[str(interaction.guild.id)] = {

            "schedule": schedule.value,
            "week": saved_week,
            "weekday": weekday.value,
            "time": time,
            "timezone": timezone

        }


        save_schedules(schedules)


        embed = discord.Embed(
            title="✅ Wipe Schedule Saved",
            color=discord.Color.green()
        )


        embed.add_field(
            name="Schedule",
            value=schedule.name,
            inline=True
        )


        if schedule.value == "monthly":

            embed.add_field(
                name="Week",
                value=week.name,
                inline=True
            )


        embed.add_field(
            name="Day",
            value=weekday.name,
            inline=True
        )


        embed.add_field(
            name="Time",
            value=time,
            inline=True
        )


        embed.add_field(
            name="Timezone",
            value=timezone,
            inline=False
        )


        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(SetWipe(bot))