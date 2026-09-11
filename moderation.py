import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --------------------------------------------------
    # Kick
    # --------------------------------------------------

    @app_commands.command(
        name="kick",
        description="Kick a member from the server."
    )
    @app_commands.describe(
        member="The member to kick.",
        reason="Reason for the kick."
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided."
    ):

        if member == interaction.user:
            await interaction.response.send_message(
                "You cannot kick yourself.",
                ephemeral=True
            )
            return

        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "You cannot kick someone with an equal or higher role.",
                ephemeral=True
            )
            return

        try:
            await member.kick(reason=reason)

            await interaction.response.send_message(
                f"👢 **{member}** has been kicked.\n"
                f"**Reason:** {reason}"
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to kick that member.",
                ephemeral=True
            )

    # --------------------------------------------------
    # Ban
    # --------------------------------------------------

    @app_commands.command(
        name="ban",
        description="Ban a member from the server."
    )
    @app_commands.describe(
        member="The member to ban.",
        reason="Reason for the ban."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided."
    ):

        if member == interaction.user:
            await interaction.response.send_message(
                "You cannot ban yourself.",
                ephemeral=True
            )
            return

        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "You cannot ban someone with an equal or higher role.",
                ephemeral=True
            )
            return

        try:
            await member.ban(
                reason=reason,
                delete_message_seconds=0
            )

            await interaction.response.send_message(
                f"🔨 **{member}** has been banned.\n"
                f"**Reason:** {reason}"
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to ban that member.",
                ephemeral=True
            )

    # --------------------------------------------------
    # Clear Messages
    # --------------------------------------------------

    @app_commands.command(
        name="clear",
        description="Delete messages from a channel."
    )
    @app_commands.describe(
        amount="Number of messages to delete."
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def clear(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1, 100]
    ):

        channel = interaction.channel

        if not isinstance(
            channel,
            discord.TextChannel
        ):
            await interaction.response.send_message(
                "This command can only be used in a text channel.",
                ephemeral=True
            )
            return

        await interaction.response.defer(
            ephemeral=True
        )

        deleted = await channel.purge(
            limit=amount
        )

        await interaction.followup.send(
            f"🧹 Deleted **{len(deleted)}** message(s).",
            ephemeral=True
        )

    # --------------------------------------------------
    # Timeout
    # --------------------------------------------------

    @app_commands.command(
        name="timeout",
        description="Timeout a member."
    )
    @app_commands.describe(
        member="The member to timeout.",
        minutes="Length of the timeout in minutes.",
        reason="Reason for the timeout."
    )
    @app_commands.checks.has_permissions(
        moderate_members=True
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: app_commands.Range[int, 1, 40320],
        reason: str = "No reason provided."
    ):

        if member == interaction.user:
            await interaction.response.send_message(
                "You cannot timeout yourself.",
                ephemeral=True
            )
            return

        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "You cannot timeout someone with an equal or higher role.",
                ephemeral=True
            )
            return

        duration = discord.utils.utcnow() + discord.timedelta(
            minutes=minutes
        )

        try:
            await member.timeout(
                duration,
                reason=reason
            )

            await interaction.response.send_message(
                f"⏱️ **{member}** has been timed out for "
                f"**{minutes} minute(s)**.\n"
                f"**Reason:** {reason}"
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to timeout that member.",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
