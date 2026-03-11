import os
import re
import json
import random
import discord

from datetime import datetime
from discord.ext import commands
from misc import banished_words_private as banished_words_privateA
from utils.discordbot import Bot
from utils.files import files
from utils.semifunc import SemiFunc

class BanishMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        banished = files._banished()['banished_words']
        banished_nodelete = files._banished()['banished_nodelete']
        banished_words_noignore = files._banished()['banished_words_noignore']
        banished_ignore = files._banished()['banishedWordsBypasses']
        banished_words_private = banished_words_privateA.private_banished()
        msg_content_lower = msg.content.lower()
        content_lower_final = re.sub(r'[(#@-_\\/^,.)]', '', msg_content_lower).replace(" ", "")
        canBanish = True
        
        ### March 8, 2026 
        ## Okay so bots causes a error like this in the log.. This is to fix that.
        # 2026-03-08 12:22:42 ERROR    discord.client Ignoring exception in on_message
        # Traceback (most recent call last):
        # File "C:\Program Files\Python314\Lib\site-packages\discord\client.py", line 504, in _run_event
        #     await coro(*args, **kwargs)
        # File "D:\Code\Discord Bots\friendly-pikes-bot\listeners\on__message\banish_message.py", line 28, in on_message
        #     if SemiFunc.is_staff(msg, msg.author) == False:
        #     ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
        # File "D:\Code\Discord Bots\friendly-pikes-bot\utils\semifunc.py", line 52, in is_staff
        #     role = SemiFunc.get_role_id(ctx, "staff")
        # File "D:\Code\Discord Bots\friendly-pikes-bot\utils\semifunc.py", line 38, in get_role_id
        #     roles = files.get_role_ids(ctx)
        # File "D:\Code\Discord Bots\friendly-pikes-bot\utils\files.py", line 75, in get_role_ids
        #     main_test = main_or_test(ctx.guild.id)
        #                             ^^^^^^^^^^^^
        # AttributeError: 'NoneType' object has no attribute 'id'
        # 2026-03-08 12:22:42 ERROR    discord.client Ignoring exception in on_message
        # Traceback (most recent call last):
        # File "C:\Program Files\Python314\Lib\site-packages\discord\client.py", line 504, in _run_event
        #     await coro(*args, **kwargs)
        # File "D:\Code\Discord Bots\friendly-pikes-bot\listeners\on__message\banish_message.py", line 28, in on_message
        #     if SemiFunc.is_staff(msg, msg.author) == False:
        #     ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
        # File "D:\Code\Discord Bots\friendly-pikes-bot\utils\semifunc.py", line 52, in is_staff
        #     role = SemiFunc.get_role_id(ctx, "staff")
        # File "D:\Code\Discord Bots\friendly-pikes-bot\utils\semifunc.py", line 38, in get_role_id
        #     roles = files.get_role_ids(ctx)
        # File "D:\Code\Discord Bots\friendly-pikes-bot\utils\files.py", line 75, in get_role_ids
        #     main_test = main_or_test(ctx.guild.id)
        #                             ^^^^^^^^^^^^
        # AttributeError: 'NoneType' object has no attribute 'id'

        if msg.author.bot == False:

            for thing in banished_nodelete:
                    if content_lower_final.find(thing) >= 0:
                        await SemiFunc.moderate_user(self.bot, msg, msg.author, "message_banished_flagged", [None, thing])
                        shouldBanish = False


            if SemiFunc.is_staff(msg, msg.author) == False:
                
                # 1 - If a user is menitioned, and their userid has "67" in it, ignore
                if len(msg.mentions) > 0:
                    for mention in msg.mentions:
                        if str(mention.id).find("67") >= 0:
                            canBanish = False
                            # self.bot.logger.info(msg=f"Don't banish '{msg_content_lower}' sent by {msg.author.name}")
                
                # 2 - If in counting and the message has 67 in it, ignore
                if msg.channel.id == 1419042219842736299 and msg_content_lower.find("67") >= 0:
                    self.bot.logger.info(msg="We need them to count ffs!")
                    canBanish = False


                if canBanish:
                    for banished_thing in banished:
                        shouldBanish = True

                        # 3 - If banished_thing in banished_ignore, do not banish
                        for ignore in banished_ignore:
                            if content_lower_final.find(ignore) >= 0:
                                # self.bot.logger.info(msg=f"Don't banish '{msg_content_lower}' sent by {msg.author.name}")
                                shouldBanish = False
                            
                        if shouldBanish:
                            if msg_content_lower.find(banished_thing) >= 0:
                                # await msg.reply(banished[banished_thing])
                                await SemiFunc.moderate_user(self.bot, msg, msg.author, "message_banished", [banished[banished_thing], banished_thing])
                                await msg.delete()
                        
                # Last now - Private banish word list
                for banished_thing in banished_words_private:
                    if msg_content_lower.find(banished_thing) >= 0:
                        # await msg.reply(banished_words_private[banished_thing])
                        await SemiFunc.moderate_user(self.bot, msg, msg.author, "message_banished", [banished_words_private[banished_thing], banished_thing])
                        await msg.delete()
            
            
            # These are banished for ALL, even staff.
            for banished_thing in banished_words_noignore:
                if content_lower_final.find(banished_thing) >= 0:
                    # await msg.reply(banished_words_noignore[banished_thing])
                    await SemiFunc.moderate_user(self.bot, msg, msg.author, "message_banished", [banished_words_noignore[banished_thing], banished_thing])
                    await msg.delete()
                

                
            # Banish Snowy Paws
            if msg.author.id == 888072934114074624 or msg.author.id == 1257541858809217035 or msg.author.id == 1094359688541372457 or msg.author.id == 1403877222959419423:
                pawMsg = "You've been banished from using snowy's paws."
                if msg.author.id == 888072934114074624:
                    pawMsg = "You've been banished from using your paws."

                # First snowy, and only snowy for now
                if msg_content_lower.find("<:snowypawbs:1468047084664918278>") >= 0:
                    await msg.reply(pawMsg)
                    await msg.delete()
                if len(msg.stickers):
                    for sticker in msg.stickers:
                        if sticker.name == "Snowy Pawbs" or sticker.name == "Snowy Pawbs Real":
                            await msg.reply(pawMsg)
                            await msg.delete()


async def setup(bot):
    await bot.add_cog(BanishMessage(bot))
