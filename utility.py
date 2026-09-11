import discord
from discord import app_commands
from discord.ext import commands


class Utility(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --------------------------------------------------
    # Prefix Command
    # --------------------------------------------------

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        Check the bot's latency.
        """

        latency = round(self.bot.latency * 1000)

        await ctx.send(
            f"🏓 Pong! `{latency}ms`"
        )

    # --------------------------------------------------
    # Slash Command
    # --------------------------------------------------

    @app_commands.command(
        name="ping",
        description="Check the bot's latency."
    )
    async def slash_ping(
        self,
        interaction: discord.Interaction
    ):

        latency = round(self.bot.latency * 1000)

        await interaction.response.send_message(
            f"🏓 Pong! `{latency}ms`"
        )

    # --------------------------------------------------
    # Server Information
    # --------------------------------------------------

    @app_commands.command(
        name="serverinfo",
        description="Display information about this server."
    )
    async def serverinfo(
        self,
        interaction: discord.Interaction
    ):

        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "This command can only be used inside a server.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.blurple()
        )

        if guild.icon:
            embed.set_thumbnail(
                url=guild.icon.url
            )

        embed.add_field(
            name="Server ID",
            value=guild.id,
            inline=False
        )

        embed.add_field(
            name="Owner",
            value=f"<@{guild.owner_id}>",
            inline=True
        )

        embed.add_field(
            name="Members",
            value=guild.member_count,
            inline=True
        )

        embed.add_field(
            name="Channels",
            value=len(guild.channels),
            inline=True
        )

        embed.add_field(
            name="Roles",
            value=len(guild.roles),
            inline=True
        )

        embed.add_field(
            name="Created",
            value=discord.utils.format_dt(
                guild.created_at,
                style="F"
            ),
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )

    # --------------------------------------------------
    # User Information
    # --------------------------------------------------

    @app_commands.command(
        name="userinfo",
        description="Display information about a user."
    )
    @app_commands.describe(
        user="The user to inspect."
    )
    async def userinfo(
        self,
        interaction: discord.Interaction,
        user: discord.Member
    ):

        embed = discord.Embed(
            title=f"User Information — {user}",
            color=user.color
        )

        embed.set_thumbnail(
            url=user.display_avatar.url
        )

        embed.add_field(
            name="User ID",
            value=user.id,
            inline=False
        )

        embed.add_field(
            name="Account Created",
            value=discord.utils.format_dt(
                user.created_at,
                style="F"
            ),
            inline=False
        )

        if user.joined_at:
            embed.add_field(
                name="Joined Server",
                value=discord.utils.format_dt(
                    user.joined_at,
                    style="F"
                ),
                inline=False
            )

        embed.add_field(
            name="Top Role",
            value=user.top_role.mention,
            inline=True
        )

        embed.add_field(
            name="Bot",
            value="Yes" if user.bot else "No",
            inline=True
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
