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

    def search_subcommand(self, cmd, cmd_name):
        print(f"searching {cmd_name} in {cmd.name}")
        cmd_found = False
        subcommands = cmd.children.values()
        if len(subcommands) > 0:
            for x in subcommands:
                subcmd_name = x.name
                if cmd_name in f"{x.full_parent_name} {subcmd_name}":
                    if cmd_name == f"{x.full_parent_name} {subcmd_name}":
                        cmd_found = True
                        cmd = x
                        break
                    if len(x.children) > 0:
                        return self.search_subcommand(x, cmd_name)                       
        return cmd_found, cmd

    @nextcord.slash_command(name="help")
    async def help(
        self, 
        interaction: Interaction,
        command: str = SlashOption(
            description = "Get extra info for this command",
            default = None,
            required = False
        )
    ):
        """Get a list of commands or info of a specific command."""
        mapping = main.get_mapping(interaction)
        if not command:
            view = HelpView(interaction, mapping)
            embed = view.help_embed()
            await interaction.send(embed=embed, view=view)
        else:
            command = command.strip()
            cmd_found = False
            for cog, commands in mapping.values():
                for i in commands:
                    cmd_in_guild = False
                    if i.is_global:
                        cmd_in_guild = True
                    elif interaction.guild_id in i.guild_ids:
                        cmd_in_guild = True
                    if cmd_in_guild:
                        if i.name == command:
                            cmd_found = True
                            cmd = i
                            break
                        else:
                            if len(i.children) > 0:
                                cmd_found, cmd = self.search_subcommand(i, command)
                                if cmd_found:
                                    break
                if cmd_found: 
                    break
            if cmd_found:
                embed = Embed()
                name = cmd.name if isinstance(cmd, nextcord.ApplicationCommand) else f"{cmd.full_parent_name} {cmd.name}"
                embed.title = f"Info of /{name}"
                embed.set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)
                if len(cmd.children) > 0:
                    view = HelpView(interaction, mapping)
                    embed = view.help_embed(command_list=cmd.children.values(), author_name=f"Subcommands of /{name}")
                else:
                    embed.description = cmd.description
                    cmd_options = [i for i in list(cmd.options.values())]
                    usage = f"`/{name} "
                    for option in cmd_options:
                        if option.required == True:
                            usage += f"<{option.name}> "
                        else:
                            usage += f"[{option.name}] "
                    usage = usage[:-1]
                    usage += "`"
                    embed.add_field(name="Usage", value=usage)
                    embed.set_footer(text="Syntax: <required> [optional]")
                embed.colour = random.choice(main.embed_colours)
                await interaction.send(embed=embed)
            else:
                await interaction.send("The command is not found! Use `/help` for a list of available commands")


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))