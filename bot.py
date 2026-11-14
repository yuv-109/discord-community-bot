import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord')

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#server ID
TEST_GUILD = discord.Object(id=1570751993683906701) 

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")
    try:
        # Copy commands to your server and sync them
        bot.tree.copy_global_to(guild=TEST_GUILD)
        synced = await bot.tree.sync(guild=TEST_GUILD)
        logger.info(f"Synced {len(synced)} slash commands instantly to your server")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    logger.error(f"Slash command error: {error}")
    if not interaction.response.is_done():
        await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f"Loaded cog: {filename}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())