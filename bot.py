import os
import dotenv
import discord
import utils.files as files

from utils.discordbot import Bot
dotenv.load_dotenv()

token = os.getenv('DISCORD_TOKEN')
config = files._config()

bot = Bot(
    command_prefix=config['prefix'],
    prefix=config['prefix'], command_attrs=dict(hidden=True),
    allowed_mentions=discord.AllowedMentions(
        everyone=False, roles=False, users=True
    ),
    intents=discord.Intents.all()
)

try:
    bot.run(token)
except Exception as e:
    bot.logger.error(f"Error when logging in: {e}")
