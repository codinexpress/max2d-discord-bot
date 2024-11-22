import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
import os


class LoggingCog(commands.Cog):
    """Cog for logging messages to a file."""

    def __init__(self, bot: commands.Bot):
        """Initialize the LoggingCog."""
        self.bot = bot  
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Set up the logger."""
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)

        log_dir = "resources/logging"  # Use a relative path for better portability
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "discord.log")

        handler = RotatingFileHandler(filename=log_file, maxBytes=10485760, backupCount=5, encoding='utf-8') 
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Log messages to the file."""
        if not message.author.bot:  # Avoid logging bot messages
            self.logger.info(f"Message from {message.author}: {message.content}")


async def setup(bot):
    await bot.add_cog(LoggingCog(bot))