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

    async def get_farm_ui(self, ctx):
        # get user profile and set variables for them
        users = Users(ctx.author)
        user_profile = users.get_user_profile()
        crops = user_profile["farm"]["crops"]
        width = user_profile["farm"]["farm_width"]
        height = user_profile["farm"]["farm_height"]
        last_used = user_profile["commands_last_used"]["farm"]
        # grow the crops
        print("get now timestamp")
        now = int(datetime.now().timestamp())
        print("got now timestamp")
        await ctx.send(f"You left at <t:{last_used}:F>")
        await ctx.send(f"You left for {now - last_used} seconds.")
        left_for = now - last_used
        user_profile["commands_last_used"]["farm"] = now
        # for i in crops:
            
        # set up the embed
        farm_ui = Embed()
        farm_ui.set_author(name=f"{ctx.author.name}'s Farm")
        farm_ui.colour = random.choice(main.embed_colours)
        # turn crops into emoji
        crops_emoji = [
            "<:crop_empty:954022374116843591>",
            "<:crop_1:954022380945162250>",
            "<:crop_2:954022394962518046>",
            "<:crop_3:954022415032279120>" 
        ]
        crops_str = ""
        row = 1
        column = 1
        for i in crops:
            if i == "":
                crops_str += crops_emoji[0]
            elif i == 1:
                crops_str += crops_emoji[1]
            elif i == 2:
                crops_str += crops_emoji[2]
            elif i == 3:
                crops_str += crops_emoji[3]
            column += 1
            if column > width:
                crops_str += "\n"
                row += 1
                column = 1
            if row > height:
                break
        # add the crops field
        farm_ui.add_field(name="Crops", value=crops_str)
        # update the user profile
        user_profile = users.update_user_profile(user_profile)
        # send the embed
        return farm_ui

    @commands.command(name="farm")
    async def farm(self, ctx):
        farm_ui = await self.get_farm_ui(ctx)
        await ctx.send(embed=farm_ui)

def setup(bot: commands.Bot):
    bot.add_cog(Farm(bot))
