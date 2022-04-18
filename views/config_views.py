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

class AddSpaceInPrefix(View):

    def __init__(self, ctx, pages):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.pages = pages

    @Button(
        label = "Cancel", 
        style = nextcord.ButtonStyle.red, 
        emoji = "❎"
    )
    async def cancel(self, button, interaction):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(embed=self.pages.cancel_page(), view=self)

    @Button(
        label = "Confirm", 
        style = nextcord.ButtonStyle.green, 
        emoji = "✅"
    )
    async def confirm(self, button, interaction):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(embed=self.pages.confirm_page(), view=self)
    
    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.message.edit(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f"This is not for you, sorry.\nUse `{self.ctx.command}`", ephemeral=True)
            return False
        else:
            return True