import os
import nextcord
from datetime import datetime
import time
import random
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction, ButtonStyle
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

    @nextcord.slash_command(name="help", description="Get a list of commands or info of a specific command.")
    async def help(self, interaction:Interaction):
        # .get_signature()[0] --> for later use
        cog_commands = {}
        msg = "hi"
        for cog_name, cog in self.bot.cogs.items():
            commands = []
            for cmd in cog.get_commands():
                commands.append(cmd)
            for application_cmd in cog.to_register:
                if application_cmd.is_global:
                    cmd_in_guild = True
                elif interaction.guild_id in application_cmd.guild_ids:
                    cmd_in_guild = True
                if cmd_in_guild == True:
                    commands.append(application_cmd)
            cog_commands[cog_name] = commands
        view = HelpView(interaction, cog_commands, list(cog_commands.keys())[0])
        await interaction.send(msg)

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))