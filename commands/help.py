import discord
from discord import app_commands
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="help",
        description="Show all Rust Wipe Bot commands."
    )
    async def help(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🧻 Rust Wipe Bot Help",
            description="Available commands:",
            color=discord.Color.orange()
        )


        embed.add_field(
            name="⚙️ Admin Commands",
            value=(
                "`/setwipe`\n"
                "Configure the wipe schedule.\n\n"

                "`/settings`\n"
                "Show current wipe configuration."
            ),
            inline=False
        )


        embed.add_field(
            name="📅 Wipe Commands",
            value=(
                "`/wipe`\n"
                "Show the next wipe time and countdown."
            ),
            inline=False
        )


        embed.add_field(
            name="📌 Information",
            value=(
                "`/help`\n"
                "Show this help menu."
            ),
            inline=False
        )


        embed.set_footer(
            text="Rust Wipe Bot"
        )


        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Help(bot))