from discord.ext import commands
from utils.discordbot import Bot
from utils.custom.context import Context
from utils.semifunc import SemiFunc

class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if ctx.command:
            # if ctx.command.name in ["reply", "repeat"]:
            #     await ctx.message.delete()
            #     return
            
            mention_snowy = "<@888072934114074624>"
            command_name = ctx.command.name

            # if ctx.interaction != None:
            #     command_name = ctx.interaction.command.name

            await ctx.reply(f"An error occured with the command! {mention_snowy}\n\n```{error}```")
            self.bot.logger.warn(f"An error occured with the command '{command_name}' used by {ctx.author.name}!\n{error}\n")
        else:
            self.bot.logger.warn(f"An error occured!\n{error}\n")
        
async def setup(bot):
    await bot.add_cog(OnCommandError(bot))
