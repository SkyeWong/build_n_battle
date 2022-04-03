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

    async def get_farm_ui(ctx):
        users = Users(ctx.author)
        user_profile = users.get_user_profile()
        await ctx.send("get user profile")
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
        farm_ui.set_author(name=f"{ctx.author.name}'s Farm", icon_url=ctx.author.display_avatar.url)
        await ctx.send("set author")
        crops_str = ""
        row = 1
        column = 1
        await ctx.send("initiate varibles")
        await ctx.send("`Row Column`")
        for i in crops:
            await ctx.send(f"` {row}:    {column}`")
            if i == "":
                crops_str += crops_emoji[0]
            elif i == 1:
                crops_str += crops_emoji[1]
            elif i == 2:
                crops_str += crops_emoji[2]
            elif i == 3:
                crops_str += crops_emoji[3]
            column += 1
            if column == width:
                crops_str += "\n"
                row += 1
                column = 1
            if row > height:
                break
        farm_ui.add_field(name="Crops", value=crops_str)
        return farm_ui

    @commands.command(name="farm")
    async def farm(self, ctx):
        farm_ui = await self.get_farm_ui(ctx)
        await ctx.send(farm_ui)

def setup(bot: commands.Bot):
    bot.add_cog(Farm(bot))
