import os
import nextcord
import random
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed, SelectOption 
from nextcord.ui import Button, View
import database as db
from typing import Optional
from functions.users import Users

class Analysis(View):
                
    def __init__(self, result, most, least):
        super().__init__(timeout=180)
        self.most = most
        self.least = least
        self.result = result

    @nextcord.ui.button(
        label = "Show Analysis", 
        style = nextcord.ButtonStyle.blurple, 
        emoji = "📊"
    )
    async def show_analysis(self, button, interaction):
        embed = Embed()
        msg = "```\n```md\n"
        msg += "# Analysis:\n"
        msg += "\t- <MOST>:\n"
        for i in self.most:
            msg += f"\t\t* [{self.result.count(str(i))}]({i}s)\n"
        msg += "\t- <LEAST>:\n"
        for i in self.least:
            msg += f"\t\t* [{self.result.count(str(i))}]({i}s)\n"
        msg += "> great, isn't it? took SkyeWong#8577 2 days to make this!```"
        embed.description = msg
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.message.edit(view=self)