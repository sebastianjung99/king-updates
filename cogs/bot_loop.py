from discord.ext import tasks, commands


CHANNEL_ID = 1099438978693857340


class bot_loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(CHANNEL_ID)
        self.main_loop.start()

    @tasks.loop(seconds=30.0)
    async def main_loop(self):
        await self.channel.send("test")



async def setup(bot):  
    await bot.add_cog(bot_loop(bot))