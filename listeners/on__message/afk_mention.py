import os
import re
import json
import random
import discord

from datetime import datetime
from discord.ext import commands
from utils.discordbot import Bot
from utils.files import files

class AFKMention(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        afk = files.get_filepath("afk", "json")
        
        if msg.author.bot == False:
            if len(msg.mentions) > 0:
                for mention in msg.mentions:
                    if mention.id != msg.author.id:
                        with open(afk, 'r+', encoding='utf8') as file:
                            data = json.load(file)
                        
                        users = data['users']
                        if data['users']:
                            for entry in users:
                                if str(mention.id) == str(entry['user_id']):
                                    afk_time = datetime.strptime(entry['since'], "%d/%m/%Y %H:%M")
                                    now_time = datetime.now()
                                    afk_dur = now_time - afk_time

                                    seconds = int(afk_dur.total_seconds())

                                    days = seconds // 86400
                                    hours = seconds // 3600
                                    minutes = (seconds % 3600) // 60
                                    secondsB = seconds & 60

                                    hours_text = "hour"
                                    minutes_text = "minute"
                                    days_text = "day"
                                    if minutes > 1 or minutes == 0:
                                        minutes_text = "minutes"
                                    if hours > 1 or hours == 0:
                                        hours_text = "hours"
                                    if days > 1 or days == 0:
                                        days_text = "days"
                                            
                                    if minutes > 0 and hours == 0 and days == 0:
                                        await msg.reply(f"`{entry['name']}` is AFK: {entry['msg']}\nThey've been AFK for {minutes} {minutes_text}")
                                    if hours > 0 and days == 0:
                                        await msg.reply(f"`{entry['name']}` is AFK: {entry['msg']}\nThey've been AFK for {hours} {hours_text}, {minutes} {minutes_text}")
                                    if days > 0:
                                        await msg.reply(f"`{entry['name']}` is AFK: {entry['msg']}\nThey've been AFK for {days} {days_text}, {hours} {hours_text}, {minutes} {minutes_text}")

async def setup(bot):
    await bot.add_cog(AFKMention(bot))