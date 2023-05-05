from discord.ext import tasks, commands
from datetime import datetime

import tools
import updates


CHANNEL_ID = 1099438978693857340


class bot_loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(CHANNEL_ID)

        # get config
        self.config = tools.get_json("config.json")

        # store channel name, a bool value to check if live message has already been sent
        self.twitch_channels = [[channel_name, False] for channel_name in self.config['TWITCH']]

        # start main loop
        self.main_loop.start()

    
    async def check_twitch(self):
        """
        Checks if a twitch channel is live and sends a message to self.channel if live.
        """

        for channel in self.twitch_channels:
            streamer = channel[0]
            is_live, title, start = updates.get_twitch_status(streamer)

            # check if live and if live if live message has already been sent
            if is_live and not channel[1]:
                # set to True and send message
                channel[1] = True                
                tools.LOGGER.info(f"Sending live message for {streamer} and creating DB entry.")
                await self.channel.send(f'{streamer} is live: \"{title}\"\nhttps://twitch.tv/{streamer}')

                # create database entry                
                mariadb_connection, cursor = tools.get_db_connection()
                sql_statement = """
                    INSERT INTO twitch (channel_name, title, start_time) 
                    VALUES (%s, %s, %s);"""
                values = (streamer, title, start)                
                cursor.execute(sql_statement, values)
                mariadb_connection.commit()
                mariadb_connection.close()
                
                tools.LOGGER.debug(f"Created datbase entry. Query: {sql_statement}" % values)


            # if not live anymore set status to false and update db entry
            elif not is_live and channel[1]:
                channel[1] = False

                tools.LOGGER.debug(f"{streamer} went offline. Updating Database...")

                now = datetime.now()
                mariadb_connection, cursor = tools.get_db_connection()

                sql_statement = """
                    SELECT start_time 
                    FROM twitch 
                    WHERE channel_name = %s 
                    ORDER BY id 
                    DESC LIMIT 1;"""
                values = (streamer,)
                cursor.execute(sql_statement, values)
                res = cursor.fetchall()
                tools.LOGGER.debug(f"Getting start_time. Query: {sql_statement}\nResult: {res}" % values)

                # calculate time_streamed and format it
                time_streamed = now - res[0]['start_time']
                seconds = time_streamed.total_seconds()
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                time_streamed = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                # update database
                sql_statement = """
                    UPDATE twitch 
                    SET end_time = %s 
                    WHERE channel_name = %s 
                    ORDER BY id 
                    DESC LIMIT 1;"""
                values = (now, streamer)
                cursor.execute(sql_statement, values)
                tools.LOGGER.debug(f"Updated end_time. Query: {sql_statement}" % values)

                sql_statement = """
                    UPDATE twitch 
                    SET time_streamed = %s 
                    WHERE channel_name = %s 
                    ORDER BY id 
                    DESC LIMIT 1;"""
                values = (time_streamed, streamer)
                cursor.execute(sql_statement, values)                
                tools.LOGGER.debug(f"Updated stream_time. Query: {sql_statement}" % values)

                mariadb_connection.commit()
                mariadb_connection.close()
                
                tools.LOGGER.info(f"{streamer} went offline. Updated Database.")



    @tasks.loop(seconds=30.0)
    async def main_loop(self):
        tools.LOGGER.debug(f"Checking Twitch statuses.")
        await self.check_twitch()



async def setup(bot):  
    await bot.add_cog(bot_loop(bot))