import os
import json
import discord

from datetime import datetime
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.discordbot import Bot
from utils.files import files

class AFKReturn(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        afk = files.get_filepath("afk", "json")
        
        if not msg.content.startswith("?"):
            if os.path.exists(afk):
                with open(afk, "r", encoding="utf8") as file:
                    data = json.load(file)

                users = data['users']

                if data['users']:
                    for i, entry in enumerate(users):
                        if entry['user_id'] == msg.author.id:
                            afk_time = datetime.strptime(entry['since'], "%d/%m/%Y %H:%M")
                            now_time = datetime.now()
                            afk_dur = now_time - afk_time

                            seconds = int(afk_dur.total_seconds())

                            minutes = (seconds % 3600) // 60

                            if minutes > 1:
                                users.pop(i)

                                with open(afk, "w", encoding="utf8") as file:
                                    json.dump(data, file, indent=4, ensure_ascii=False)

                                
                                try:
                                    await msg.author.edit(nick=entry['name'], reason="They are back")
                                except Forbidden as e:
                                    print(f"Cannot change {msg.author.display_name}'s name")
                                
                                await msg.channel.send(content=f"Welcome back {msg.author.mention}, I removed your AFK status.", delete_after=5)


async def setup(bot):
    await bot.add_cog(AFKReturn(bot))
