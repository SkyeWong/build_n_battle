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

    def get_farm_ui(user):
        users = Users(user)
        user_profile = users.get_user_profile()
        crops = user_profile["farm"]["crops"]
        width = user_profile["farm"]["farm_width"]
        height = user_profile["farm"]["farm_height"]
        crops_emoji = [
            "<:crop_empty:954022374116843591>",
            "<:crop_1:954022380945162250>",
            "<:crop_2:954022394962518046>",
            "<:crop_3:954022415032279120>" 
            ]
        farm_ui = Embed()
        farm_ui.set_author(name=f"{user.name}'s Farm", icon_url=user.avatar.url)
        crops_str = ""
        row = 0
        column = 0
        for i in json.loads(crops):
            column += 1
            if i == "":
                crops_str += crops_emoji[0]
            elif i == 1:
                crops_str += crops_emoji[1]
            elif i == 2:
                crops_str += crops_emoji[2]
            elif i == 3:
                crops_str += crops_emoji[3]
            if column == width:
                crops_str += "\n"
                row += 1
            if row == height:
                break
        farm_ui.add_field(name="Crops", value=crops_str)
        return farm_ui

    @commands.command(name="farm")
    async def farm(self, ctx):
        farm_ui = self.get_farm_ui()
        await ctx.send(farm_ui)

def setup(bot: commands.Bot):
    bot.add_cog(Farm(bot))
