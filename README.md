# Discord Community Bot

I built this Discord bot from scratch in Python to learn backend development, asynchronous programming, and API integration. It handles leveling, moderation, and AI chat.

## Features
 **AI Chat (`/ask`):** Connects to the Google Gemini API. It tries to use the fastest model first, but if Google's servers are overloaded (503 error), it automatically falls back to a secondary model so it never breaks.
 **Leveling System:** Users get random XP (15-25) for chatting, with a cooldown to prevent spam.
 **Database:** Uses SQLite to save everyone's XP across restarts.
 **Moderation (`/purge`):** Safely deletes messages, with built-in checks to make sure the user and the bot have the right permissions.

## Tech Stack
 Python 3
 `discord.py` (using Cogs for modular code)
 SQLite3
 `google-genai` (Gemini API)
 `python-dotenv` (to hide my API keys)

## How to run it
1. Clone the repo.
2. Make a virtual environment: `python -m venv venv`
3. Activate it: `.\venv\Scripts\activate` (Windows)
4. Install requirements: `pip install -r requirements.txt`
5. Create a `.env` file in the main folder and add your keys:
   ```env
   DISCORD_TOKEN=your_token_here
   GEMINI_API_KEY=your_api_key_here
