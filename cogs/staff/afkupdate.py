import json

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

async def afk_cmd(self, ctx: Context, message: str, return_message: bool):
    await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

    afk = files.get_filepath("afk", "json")
    is_already_afk = False

    with open(afk, "r", encoding="utf8") as file:
        data = json.load(file)

    for entry in data['users']:
        if entry['user_id'] == ctx.author.id:
            is_already_afk = True
            entry['msg'] = message
            break
                    
    with open(afk, 'w', encoding='utf8') as file:
        if is_already_afk:
            await ctx.reply(f"I've updated you AFK message to `{message}`")
        else:
            await ctx.reply(f"Cannot set your AFK message because you've not used ?afk or /afk")

        json.dump(data, file, indent=4, ensure_ascii=False)


class afkupdate(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="afkupdate", description="Update your AFK status!")
    async def afkupdate(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
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
    await bot.add_cog(afkupdate(bot))
