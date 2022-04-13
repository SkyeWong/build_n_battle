import os
from discord import ButtonStyle
import nextcord
import json 
from datetime import datetime
import time
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed
from nextcord.ui import Button, View

class Utility(commands.Cog, name="Utility"):

    COG_EMOJI = "🔨"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 

    @bot.slash_command(name="invite", description="Invite me!", guild_ids=[919223073054539858])
    async def invite(self, interaction:nextcord.Interaction):
        embed = nextcord.Embed()
        embed.title = "Invite me to your server and have some fun!"
        embed.set_author(name=bot.user.name, icon_url= bot.user.avatar)
        embed.description = "[here](https://discord.com/api/oauth2/authorize?client_id=906505022441918485&permissions=8&scope=bot)"
        embed.colour = random.choice(main.embed_colours)
        await interaction.response.send_message(embed=embed)

    @bot.slash_command(name="help", description="Get a list of commands or info of a specific command.")
    async def help(self, interaction:nextcord.Interaction):
        await interaction.response.send_message("hi")
        msg = ""
        for cog_name, cog in self.bot.cogs.items():
            msg += f"\n{cog_name}"
            for cmd in cog.get_commands():
                msg += f" `{cmd.qualified_name}`"
        await interaction.followup.send(msg)

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))