import random
import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class eightball(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="8ball", description="The magic 8ball")
    async def eightball(self, ctx: Context, *, question: str):
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        response = random.choice(["Very likely", "Yes", "No", "Maybe", "Ask again later", "Definitely not", ])
        embed = self.bot.create_embed(
            title="🎱 Magic 8Ball",
            description=f"**Question**\n{question}\n\n**Response**\n{response}...",
            color=discord.Color.pink()
        )

        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(eightball(bot))
