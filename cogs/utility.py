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

class Utility(commands.cog, name="Utility"):

    COG_EMOJI = "🔨"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 

    @commands.command(name="invite", brief="Invite me!", help="Shows the invite link for this bot. Nothing more, nothing less.")
    async def invite(self, ctx):
        embed = nextcord.Embed()
        embed.title = "Invite me to your server and have some fun!"
        embed.set_author(name=bot.user.name, icon_url= bot.user.avatar)
        embed.description = "[here](https://discord.com/api/oauth2/authorize?client_id=906505022441918485&permissions=8&scope=bot)"
        embed.colour = random.choice(main.embed_colours)
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))