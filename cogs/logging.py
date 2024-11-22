import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
import os

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)

        log_dir = "/resources/logging"
        os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist
        log_file = os.path.join(log_dir, "discord.log")

        handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'  # Ensure proper encoding for special characters
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


    @commands.Cog.listener()
    async def on_message(self, message):
        self.logger.info(f"Message from {message.author}: {message.content}")


def setup(bot):
    bot.add_cog(LoggingCog(bot))