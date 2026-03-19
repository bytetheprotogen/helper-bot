import sqlite3
import discord

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Give(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="give")
    async def give(self, ctx: Context, user: discord.Member, amount: int):
        """
        

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user you want to give money to
        amount: int
            The amount of money you want to give
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        # if Economy.econ__is_on_cooldown(ctx, ctx.author, self.bot.logger):
        #     await ctx.reply(f"You are on cooldown! Please try again tomorrow.")
        #     return
        # else:
        #     Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)

        if user.bot:
            await ctx.reply("Bots can't use the economy system.")
            return
        
        if user.id == ctx.author.id:
            await ctx.reply("You can't do that you goober! You can't give yourself your own money!")
            return

        user_data = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()
        user_togive_data = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={user.id}").fetchone()

        if amount > user_data[3]:
            await ctx.reply(f"You can't give more than what you have! You have {Economy.format_amount(user_data[3])} {Economy.get_curreny_name()}.")
        else:
            new_bal = user_data[3] - amount
            new_bal_togive = user_togive_data[3] + amount
            
            Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (new_bal, ctx.author.id))
            Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (new_bal_togive, user.id))
            Database.userdata_conn.commit()

            await ctx.reply(f"**{ctx.author.mention} gave {Economy.format_amount(amount)} {Economy.get_curreny_name()} to {user.mention}!**")



        # if len(user) > 0:
        #     job = user[2]
        #     for job_ in jobs:
        #         if job_[0] == job:
        #             job = job_

        #     if user[2] == "NULL":
        #         await ctx.reply("You can't work if you don't have a job.")
        #     else:
        #         issues = []
        #         if hours > 10:
        #             hours = 9
        #             issues.append("You can work a maximum of 9 hours.")
                    
        #         wage = job[1] * hours
        #         bal = user[3]

        #         Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (bal + wage, ctx.author.id))
        #         Database.userdata_conn.commit()
        #         await ctx.reply(f"You went work for {job[0]} for {hours} hours, and earned {wage} {Economy.get_curreny_name()}!")

        #         if len(issues) > 0:
        #             for issue in issues:
        #                 await ctx.send(f"-# {issue}")
        # else:
        #     await ctx.reply("You aren't in our user database, so you aren't able to apply for a job right now.")

async def setup(bot):
    await bot.add_cog(Econ__Give(bot))
