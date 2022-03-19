import os
import nextcord
import random
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed
from nextcord.ui import Button, View
import database as db
from typing import Optional
from functions.users import Users

class Farm(commands.Cog, name="Farm"):

    COG_EMOJI = "🌿"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="farm")
    async def farm(self, ctx):
        users = Users(ctx)
        user_profile = users.get_user_profile()
        await ctx.send(user_profile["farm"]["crops"])

def setup(bot: commands.Bot):
    bot.add_cog(Farm(bot))
