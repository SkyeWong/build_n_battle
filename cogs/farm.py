import os
import nextcord
import random
import main
import math 
import json
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
        users = Users(ctx.author)
        user_profile = users.get_user_profile()
        crops = user_profile["farm"]["crops"]
        crops_emoji = [
            "<:crop_empty:954022374116843591>",
            "<:crop_1:954022380945162250>",
            "<:crop_2:954022394962518046>",
            "<:crop_3:954022415032279120>" 
            ]
        crops_str = ""
        for i in json.loads(crops):
            if i == "":
                crops_str += crops_emoji[0]
            elif i == 1:
                crops_str += crops_emoji[1]
            elif i == 2:
                crops_str += crops_emoji[2]
            elif i == 3:
                crops_str += crops_emoji[3]
        await ctx.send(crops_str)

def setup(bot: commands.Bot):
    bot.add_cog(Farm(bot))
