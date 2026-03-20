# "Hi I like money" - Mr Crabs

import sqlite3
import discord

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__AddMoney(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="add_money")
    async def add_money(self, ctx: Context, user: discord.Member, amount: int):
        """
        Add money to the balance of a user

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user you want to change the balance of
        amount:
            The preferred amount to give (0-10000)
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            if SemiFunc.is_command_exception(ctx.author, "reload"):
                pass
            else:
                await ctx.reply("That command is only usable by owners and managers.")
                return
        
        # No cooldown!!
        # if Economy.econ__is_on_cooldown(ctx.author, self.bot.logger):
        #     await ctx.reply(f"You are on cooldown! Please try again tomorrow.")
        #     return
        # else:
        #     Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)

        # If user is a bot. Do not check their balance
        if user.bot:
            await ctx.reply("Bots aren't able to use the economy system.")
            return

        not_in_db_msg = "They aren't in our user database, so we can't add to their balance at the moment."
        user_data = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={user.id}").fetchone()
        if user.id == ctx.author.id:
            not_in_db_msg = "You aren't in our user database, so we can't add to their balance at the moment."

        if len(user_data) > 0:
            # Max value.
            if amount > 10000:
                amount = 10000

            new_bal = user_data[3] + amount
    
            Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (new_bal, user.id))
            Database.userdata_conn.commit()
            await ctx.reply(f"You've added {amount} {Economy.get_curreny_name()} to {user.mention}'s balance successfully!")
        else:
            await ctx.reply(not_in_db_msg)

async def setup(bot):
    await bot.add_cog(Econ__AddMoney(bot))
