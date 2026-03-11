import json
import utils.files as files

from datetime import datetime, timedelta
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

async def afk_cmd(self, ctx: Context, message: str, return_message: bool):
    await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
    
    afk = files.get_filepath("afk", "json")
    is_already_afk = False

    # await ctx.reply
    with open(afk, 'r+', encoding='utf8') as file:
        data = json.load(file)

        for i, entry in enumerate(data['users']):
            if entry['user_id'] == ctx.author.id:
                is_already_afk = True
                break


        if is_already_afk:
            await ctx.reply("Cannot change your status to AFK because you've already used ?afk or /afk. Did you mean to use ?afkupdate?")
        else:
            afkSince_createdat = ctx.message.created_at.strftime("%d/%m/%Y %H:%M")
 
            data['users'].append({
                "name": ctx.author.display_name,
                "user_id": ctx.author.id,
                "return_message": return_message,
                "msg": message,
                "since": f"{afkSince_createdat}"
            })
                        
            file.seek(0)

            json.dump(data, file, indent=4, ensure_ascii=False)
            try:
                await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
                await ctx.reply(f"I've set your status to AFK with the message `{message}`")
            except Forbidden as e:
                if e.text == "Missing Permissions":
                    await ctx.reply(f"I've set your status to AFK with the message `{message}`\n..however I cannot change your nickname to show you're AFK.")
            # except CommandInvokeError as e:
            #     print(e)


class afk(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="afk", description="Set your status to AFK!")
    async def afk(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.is_command_exception(ctx.author, "afk") or SemiFunc.is_staff(ctx, ctx.author):
            await afk_cmd(self, ctx, message, return_message)
            return
            
        if not SemiFunc.is_staff(ctx, ctx.author):
            await ctx.reply("That command is staff only.")
            return
        


async def setup(bot):
    await bot.add_cog(afk(bot))
