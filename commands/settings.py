import discord
from discord import app_commands
from discord.ext import commands

from utils.storage import load_schedules


class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="settings",
        description="Show current wipe settings."
    )
    async def settings(
        self,
        interaction: discord.Interaction
    ):

        schedules = load_schedules()

        guild_id = str(interaction.guild.id)


        if guild_id not in schedules:

            await interaction.response.send_message(
                "❌ No wipe schedule has been configured.",
                ephemeral=True
            )
            return


        data = schedules[guild_id]


        embed = discord.Embed(
            title="⚙️ Wipe Settings",
            color=discord.Color.blue()
        )


        embed.add_field(
            name="📅 Schedule",
            value=data["schedule"].title(),
            inline=True
        )


        if data["schedule"] == "monthly":

            embed.add_field(
                name="🔢 Week",
                value=data["week"].title(),
                inline=True
            )


        embed.add_field(
            name="📆 Day",
            value=data["weekday"].title(),
            inline=True
        )


        embed.add_field(
            name="🕒 Time",
            value=data["time"],
            inline=True
        )


        embed.add_field(
            name="🌍 Timezone",
            value=data["timezone"],
            inline=False
        )


        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Settings(bot))