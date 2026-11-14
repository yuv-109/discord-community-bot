import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import time
import random
import logging
logger = logging.getLogger('discord')

class Experience(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("levels.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                guild_id INTEGER,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0,
                last_xp_time REAL DEFAULT 0,
                PRIMARY KEY (user_id, guild_id)
            )
        """)
        self.db.commit()
        self.cooldown = 15 

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        user_id = message.author.id
        guild_id = message.guild.id
        now = time.time()

        try:
            self.cursor.execute(
                "SELECT xp, level, last_xp_time FROM users WHERE user_id = ? AND guild_id = ?",
                (user_id, guild_id)
            )
            row = self.cursor.fetchone()

            if row is None:
                self.cursor.execute(
                    "INSERT INTO users (user_id, guild_id, xp, level, last_xp_time) VALUES (?, ?, 0, 0, ?)",
                    (user_id, guild_id, now)
                )
                self.db.commit()
                return

            xp, level, last_time = row
            if now - last_time < self.cooldown:
                return

            xp_gained = random.randint(15, 25)
            new_xp = xp + xp_gained
            new_level = level
            
            xp_needed_for_next_level = 5 * (level ** 2) + (50 * level) + 100
            
            if new_xp >= xp_needed_for_next_level:
                new_level = level + 1

            self.cursor.execute(
                "UPDATE users SET xp = ?, level = ?, last_xp_time = ? WHERE user_id = ? AND guild_id = ?",
                (new_xp, new_level, now, user_id, guild_id)
            )
            self.db.commit()

            if new_level > level:
                await message.channel.send(f"{message.author.mention} leveled up **Level {new_level}**！")
        except Exception as e:
            logger.error(f"Database error in experience system: {e}")

    @app_commands.command(name="leaderboard", description="Check the experience leaderboard on this server")
    @app_commands.guild_only()
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            self.cursor.execute(
                "SELECT user_id, xp, level FROM users WHERE guild_id = ? ORDER BY xp DESC LIMIT 10",
                (interaction.guild_id,)
            )
            rows = self.cursor.fetchall()

            if not rows:
                await interaction.followup.send("no experience points yet")
                return

            embed = discord.Embed(title="🏆 Experience Leaderboard", color=discord.Color.gold())
            for i, (user_id, xp, level) in enumerate(rows, start=1):
                user = interaction.guild.get_member(user_id) or await interaction.client.fetch_user(user_id)
                name = user.display_name if user else f"user {user_id}"
                embed.add_field(
                    name=f"#{i} {name}",
                    value=f"Level {level} | {xp} XP",
                    inline=False
                )
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f"Leaderboard error: {e}")
            await interaction.followup.send("Leadreboard error")

async def setup(bot):
    await bot.add_cog(Experience(bot))