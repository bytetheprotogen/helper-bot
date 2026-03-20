import sqlite3

from utils.database import Database
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

# async def afk_cmd(self, ctx: Context, message: str, return_message: bool):

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="afk")
    async def afk(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
        """
        Set your status to AFK

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        message: str
            The message you want to use
        return_message: str
            Toggle the return message (UNUSED)
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        # if SemiFunc.is_command_exception(ctx.author, "afk") or SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await afk_cmd(self, ctx, message, return_message)
        #     return
            
        # if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await ctx.reply("That command is staff only.")
        #     return
        

        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        is_already_afk = False

        for user in SemiFunc.afk_users:
            if user['user_id'] == ctx.author.id:
                is_already_afk = True

        if is_already_afk:
            await ctx.reply("Cannot change your status to AFK because you've already used ?afk or /afk. Did you mean to use ?afkupdate?")
        else:
            cursor = Database.userdata_conn.cursor()
            
            nick = ctx.author.display_name
            afkSince_createdat = ctx.message.created_at.strftime("%d/%m/%Y %H:%M")

            if ctx.author.nick != nick:
                if ctx.author.nick == None:
                    nick = ctx.author.display_name
                else:
                    nick = ctx.author.nick

            cursor.execute(f'INSERT INTO afk_users VALUES ({ctx.author.id}, "{nick}", "{message}", "{afkSince_createdat}")')

            Database.userdata_conn.commit()

            try:
                await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
                await ctx.reply(f"I've set your status to AFK with the message `{message}`")
            except Forbidden as e:
                if e.text == "Missing Permissions":
                    await ctx.reply(f"I've set your status to AFK with the message `{message}`\n..however I cannot change your nickname to show you're AFK.")
            # except CommandInvokeError as e:
            #     print(e)

            # Update the AFK users list
            SemiFunc.update_afk(self.bot.logger)
        
        
    @commands.guild_only()
    @commands.hybrid_command(name="afkupdate")
    async def afkupdate(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
        """
        Update your afk status

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        message: str
            The new afk message you want to use
        return_message: bool
            Toggle the return message (UNUSED)
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        # if SemiFunc.is_command_exception(ctx.author, "afk") or SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await afk_cmd(self, ctx, message, return_message)
        #     return
            
        # if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await ctx.reply("That command is staff only.")
        #     return


        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        is_already_afk = False

        for user in SemiFunc.afk_users:
            if user['user_id'] == ctx.author.id:
                is_already_afk = True

        if is_already_afk:
            cursor = Database.userdata_conn.cursor()

            cursor.execute(f"UPDATE afk_users SET message=? WHERE user_id = ?", (message, ctx.author.id))
            await ctx.reply(f"I've set your AFK message to `{message}`")

            Database.userdata_conn.commit()

        else:
            await ctx.reply(f"Cannot set your AFK message because you've not used ?afk or /afk")

async def setup(bot):
    await bot.add_cog(AFK(bot))
