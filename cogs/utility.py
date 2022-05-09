import os
import nextcord
from datetime import datetime
import time
import random
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction, ButtonStyle, SlashOption
from nextcord.ui import Button, View
from views.utility_views import HelpView

class Utility(commands.Cog, name="Utility"):

    COG_EMOJI = "🔨"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 

    @nextcord.slash_command(name="invite", description="Invite me!")
    async def invite(self, interaction: Interaction):
        embed = Embed()
        embed.title = "Invite me to your server and have some fun!"
        embed.set_author(name=bot.user.name, icon_url= bot.user.avatar)
        embed.description = "[here](https://discord.com/api/oauth2/authorize?client_id=906505022441918485&permissions=8&scope=bot)"
        embed.colour = random.choice(main.embed_colours)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="help")
    async def help(
        self, 
        interaction:Interaction,
        command: str = SlashOption(
            description = "Get extra info for this command",
            default = None,
            required = False
        )
    ):
        """Get a list of commands or info of a specific command."""
        if not command:
            cog_commands = {}
            msg = "Help Command"
            for cog_name, cog in self.bot.cogs.items():
                commands = []
                for application_cmd in cog.to_register:
                    cmd_in_guild = False
                    if application_cmd.is_global:
                        cmd_in_guild = True
                    elif interaction.guild_id in application_cmd.guild_ids:
                        cmd_in_guild = True
                    if cmd_in_guild == True:
                        commands.append(application_cmd)
                if len(commands) != 0:
                    cog_commands[cog_name] = (cog, commands)
            view = HelpView(interaction, cog_commands, "Currency")
            await interaction.send(msg, view=view)
        else:
            cmd_found = False
            for i in bot.get_all_application_commands():
                if i.name == command:
                    cmd_found = True
                    cmd = i
            if cmd_found:
                embed = Embed()
                embed.title = f"Info of /{cmd.name}"
                embed.set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)
                embed.description = cmd.description
                cmd_options = [i for i in list(cmd.options.values())]
                usage = f"`{cmd.name}"
                for option in cmd_options:
                    if option.required == True:
                        usage += f"<{option.name}> "
                    else:
                        usage += f"[{option.name}] "
                usage = usage[:-1]
                usage += "`"
                embed.add_field(name="Usage", value=usage)
                embed.colour = random.choice(main.embed_colours)
                embed.set_footer(text="<required> [optional]")
                await interaction.send(embed=embed)
            else:
                await interaction.send("The command is not found! Use `/help` for a list of available commands")


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))