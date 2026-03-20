
from discord.ext import commands
from utils.discordbot import Bot
from utils.database import Database
from utils.semifunc import SemiFunc
import utils.files as files

class OnReadyDatabase(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # 19/03/2026 - Do not do database stuff when we're testing.
        if self.bot.user.id != 1482861019582693507:
            # 16/03/2026 - add users to user_data
            guild = self.bot.get_guild(1414222707570118656)
            
            # Fuck my fluffy life.. getting members from create_databases didn't work, on_ready it is...
            for member in guild.members:
                if member.bot == False:
                    user = Database.userdata_conn.cursor().execute(f'SELECT * FROM user_data WHERE user_id={member.id}')
                    if len(user.fetchall()) < 1:
                        Database.userdata_conn.cursor().execute(f'INSERT INTO user_data VALUES ({member.id}, "{member.name}", "NULL", 0, 0, 0)')
            
            Database.userdata_conn.commit()

            print("Added all users to database.")
        

async def setup(bot):
    await bot.add_cog(OnReadyDatabase(bot))
