import os
import discord
import random
import main
import math 
import json
from main import bot
from datetime import datetime
from discord.ext import commands
from discord import Embed
from discord.ui import Button, View
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
        now = int(datetime.now().timestamp())
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

    @commands.command(name="testforhelp1")
    async def testforhelp1(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp2")
    async def testforhelp2(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp3")
    async def testforhelp3(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp4")
    async def testforhelp4(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")
    
    @commands.command(name="testforhelp5")
    async def testforhelp5(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")
   
    @commands.command(name="testforhelp6")
    async def testforhelp6(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")
    
    @commands.command(name="testforhelp7")
    async def testforhelp7(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp8")
    async def testforhelp8(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp9")
    async def testforhelp9(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp10")
    async def testforhelp10(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp11")
    async def testforhelp11(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp12")
    async def testforhelp12(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp13")
    async def testforhelp13(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp14")
    async def testforhelp14(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp15")
    async def testforhelp15(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp16")
    async def testforhelp16(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp17")
    async def testforhelp17(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp18")
    async def testforhelp18(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp19")
    async def testforhelp19(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp20")
    async def testforhelp20(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp21")
    async def testforhelp21(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp22")
    async def testforhelp22(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp23")
    async def testforhelp23(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp24")
    async def testforhelp24(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp25")
    async def testforhelp25(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp26")
    async def testforhelp26(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp27")
    async def testforhelp27(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp28")
    async def testforhelp28(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

    @commands.command(name="testforhelp29")
    async def testforhelp29(self, ctx):
        await ctx.send("This actually does **nothing**. Well, it does something, bcs skye uses this to test for the help command paginating function.")

def setup(bot: commands.Bot):
    bot.add_cog(Farm(bot))
