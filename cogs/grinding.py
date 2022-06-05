import os
import nextcord
import random
import main
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed, Interaction
from nextcord.ui import Button, View
import database as db
from typing import Optional
from functions.users import Users

class Grinding(commands.Cog, name="Grinding"):
    
    COG_EMOJI = "🎮"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 

    @nextcord.slash_command(name="hunt")
    async def hunt(self, interaction: Interaction):
        await interaction.response.send_message("now i do nothing but sometime i will be the command you use most :)")

    @nextcord.slash_command(name="test1")
    async def test1(self, interaction: Interaction):
        await interaction.response.send_message("test1")
    

    @nextcord.slash_command(name="test2")
    async def test2(self, interaction: Interaction):
        await interaction.response.send_message("test2")
    

    @nextcord.slash_command(name="test3")
    async def test3(self, interaction: Interaction):
        await interaction.response.send_message("test3")
    

    @nextcord.slash_command(name="test4")
    async def test4(self, interaction: Interaction):
        await interaction.response.send_message("test4")
    

    @nextcord.slash_command(name="test5")
    async def test5(self, interaction: Interaction):
        await interaction.response.send_message("test5")
    

    @nextcord.slash_command(name="test6")
    async def test6(self, interaction: Interaction):
        await interaction.response.send_message("test6")
    

    @nextcord.slash_command(name="test7")
    async def test7(self, interaction: Interaction):
        await interaction.response.send_message("test7")@nextcord.slash_command(name="test8")
    async def test8(self, interaction: Interaction):
        await interaction.response.send_message("test8")
    

    @nextcord.slash_command(name="test9")
    async def test9(self, interaction: Interaction):
        await interaction.response.send_message("test9")
    

    @nextcord.slash_command(name="test10")
    async def test10(self, interaction: Interaction):
        await interaction.response.send_message("test10")
    

    @nextcord.slash_command(name="test11")
    async def test11(self, interaction: Interaction):
        await interaction.response.send_message("test11")
    

    @nextcord.slash_command(name="test12")
    async def test12(self, interaction: Interaction):
        await interaction.response.send_message("test12")
    

    @nextcord.slash_command(name="test13")
    async def test13(self, interaction: Interaction):
        await interaction.response.send_message("test13")
    

    @nextcord.slash_command(name="test14")
    async def test14(self, interaction: Interaction):
        await interaction.response.send_message("test14")
    

    @nextcord.slash_command(name="test15")
    async def test15(self, interaction: Interaction):
        await interaction.response.send_message("test15")
    

    @nextcord.slash_command(name="test16")
    async def test16(self, interaction: Interaction):
        await interaction.response.send_message("test16")
    

    @nextcord.slash_command(name="test17")
    async def test17(self, interaction: Interaction):
        await interaction.response.send_message("test17")
    

    @nextcord.slash_command(name="test18")
    async def test18(self, interaction: Interaction):
        await interaction.response.send_message("test18")
    

    @nextcord.slash_command(name="test19")
    async def test19(self, interaction: Interaction):
        await interaction.response.send_message("test19")
    

    @nextcord.slash_command(name="test20")
    async def test20(self, interaction: Interaction):
        await interaction.response.send_message("test20")
    

    @nextcord.slash_command(name="test21")
    async def test21(self, interaction: Interaction):
        await interaction.response.send_message("test21")
    

    @nextcord.slash_command(name="test22")
    async def test22(self, interaction: Interaction):
        await interaction.response.send_message("test22")
    

    @nextcord.slash_command(name="test23")
    async def test23(self, interaction: Interaction):
        await interaction.response.send_message("test23")
    

    @nextcord.slash_command(name="test24")
    async def test24(self, interaction: Interaction):
        await interaction.response.send_message("test24")
    

    @nextcord.slash_command(name="test25")
    async def test25(self, interaction: Interaction):
        await interaction.response.send_message("test25")
    

    @nextcord.slash_command(name="test26")
    async def test26(self, interaction: Interaction):
        await interaction.response.send_message("test26")
    

    @nextcord.slash_command(name="test27")
    async def test27(self, interaction: Interaction):
        await interaction.response.send_message("test27")
    

    @nextcord.slash_command(name="test28")
    async def test28(self, interaction: Interaction):
        await interaction.response.send_message("test28")
    

    @nextcord.slash_command(name="test29")
    async def test29(self, interaction: Interaction):
        await interaction.response.send_message("test29")
    

def setup(bot: commands.Bot):
    bot.add_cog(Grinding(bot))