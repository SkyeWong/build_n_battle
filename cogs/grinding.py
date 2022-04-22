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

def setup(bot: commands.Bot):
    bot.add_cog(Grinding(bot))