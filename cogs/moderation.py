import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger('discord')

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Delete messages in bulk")
    @app_commands.describe(amount="Messages to delete（1-100）")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.guild_only()
    async def purge(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("The quantity must be between 1-100.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"Deleted {len(deleted)} a message.", ephemeral=True)
        except discord.Forbidden:
            logger.warning(f"Bot missing permissions to purge in {interaction.guild.name}")
            await interaction.followup.send("Delete failed: I don't have permission to delete messages in this channel.", ephemeral=True)
        except Exception as e:
            logger.error(f"Purge error: {e}")
            await interaction.followup.send("An unknown error occurred while deleting.", ephemeral=True)

    @purge.error
    async def purge_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("Permission Denied", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))