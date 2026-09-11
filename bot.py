import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN is missing. Put your bot token in the .env file."
    )

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("discord_bot")

# --------------------------------------------------
# Intents
# --------------------------------------------------

intents = discord.Intents.default()

# Needed for prefix commands and reading message content.
intents.message_content = True

# --------------------------------------------------
# Bot
# --------------------------------------------------

class GeneralBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        """
        Load all bot extensions before the bot starts.
        """

        extensions = [
            "cogs.utility",
            "cogs.moderation",
        ]

        for extension in extensions:
            try:
                await self.load_extension(extension)
                logger.info("Loaded extension: %s", extension)

            except Exception:
                logger.exception(
                    "Failed to load extension: %s",
                    extension
                )

        # Sync slash commands with Discord.
        try:
            synced = await self.tree.sync()
            logger.info(
                "Synced %d slash command(s).",
                len(synced)
            )

        except Exception:
            logger.exception("Failed to sync slash commands.")

    async def on_ready(self):
        logger.info(
            "Logged in as %s (ID: %s)",
            self.user,
            self.user.id
        )

        logger.info(
            "Connected to %d guild(s).",
            len(self.guilds)
        )

        await self.change_presence(
            activity=discord.Game(name="Managing the server")
        )


bot = GeneralBot()

# --------------------------------------------------
# Global Error Handler
# --------------------------------------------------

@bot.tree.error
async def slash_command_error(
    interaction: discord.Interaction,
    error: discord.app_commands.AppCommandError
):

    logger.error(
        "Slash command error: %s",
        error,
        exc_info=True
    )

    message = "Something went wrong while executing that command."

    if interaction.response.is_done():
        await interaction.followup.send(
            message,
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            message,
            ephemeral=True
        )


# --------------------------------------------------
# Start Bot
# --------------------------------------------------

if __name__ == "__main__":
    bot.run(TOKEN)
