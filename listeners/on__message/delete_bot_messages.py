import discord

from discord.ext import commands
from utils.discordbot import Bot

class DeleteBotMessages(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            # Delete Dyno's disabled command message, if it was sent
            if msg.author.id == 155149108183695360:
                if len(msg.embeds) > 0:
                    for embed in msg.embeds:
                        if embed.description.find("command is disabled in this server.") >= 0:
                            await msg.delete()
            ## Our bot
            # elif msg.author.id == 1477564008772014142:
            #     if len(msg.embeds) > 0:
            #         embed:discord.Embed = msg.embeds[0]
            #         should_del = False
            #         if embed.description.find("was deleted in") >= 2:
            #             for banished_thing in banished:
            #                 if embed.description.find(banished_thing) >= 0:
            #                     should_del = True
            #             for banished_thing in banished_words_noignore:
            #                 if embed.description.find(banished_thing) >= 0:
            #                     should_del = True
            #             if len(banished_words_private) > 0:
            #                 for banished_thing in banished_words_private:
            #                     if embed.description.find(banished_thing) >= 0:
            #                         should_del = True

            #         if should_del:
            #             # print(f"\n{embed.title}\n{embed.description}")
            #             await msg.delete()
            return
        

async def setup(bot):
    await bot.add_cog(DeleteBotMessages(bot))
