import discord
from discord.ext import commands
from discord import app_commands
import os
import logging
from google import genai

logger = logging.getLogger('discord')

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    @app_commands.command(name="ask", description="Ask the AI a question")
    @app_commands.describe(prompt="What do you want to ask?")
    @app_commands.guild_only()
    async def ask(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        
        try:
            try:
                response = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )
            except Exception as primary_error:
                logger.warning(f"Primary model failed ({primary_error}). Trying fallback model...")
                # If it fails (like a 503 overload), try this stable fallback
                response = self.client.models.generate_content(
                    model="gemini-2.5-pro", 
                    contents=prompt,
                )
        
            answer = response.text
            
            if len(answer) > 1900:
                answer = answer[:1900] + "\n\n... (truncated)"

            await interaction.followup.send(f"**You asked:** {prompt}\n\n**AI:** {answer}")
            
        except Exception as e:
            logger.error(f"AI Error: {e}")
            # Change this back to the friendly message when you are done debugging!
            await interaction.followup.send("Sorry, my AI brain is a bit tired right now. Try again later.")

async def setup(bot):
    await bot.add_cog(AI(bot))