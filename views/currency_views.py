import os
from discord import SelectOption
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
class EndInteraction(View):

    @nextcord.ui.button(label = "End Interaction", style = nextcord.ButtonStyle.red, emoji = "⏹️")
    async def button_callback(self, button, interaction):
        button.label = "Interaction ended"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Interaction ended.")

class generate(View):

    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx

    @nextcord.ui.button(label = "Generate gold!", style = nextcord.ButtonStyle.grey, emoji = "🪙")
    async def gold_generate(self, button, interaction):
        users = Users(self.ctx.author)
        profile = list(users.get_user_profile())
        profile[1] += 500
        profile = users.update_user_profile(profile)
        button.label = "Gold obtained!"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Something appears in front of you. You pick it up and be **really** suprised that it's some gold COINS!", ephemeral=True)

    @nextcord.ui.button(label = "Generate XP!", style = nextcord.ButtonStyle.grey, emoji = "📚")
    async def xp_generate(self, button, interaction):
        users = Users(self.ctx.author)
        profile = list(users.get_user_profile())
        profile[2] += random.choice(range(6))
        profile = users.update_user_profile(profile)
        button.label = "No more books..."
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("You take your time and read a book, and learnt something new!", ephemeral=True)
    
    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.message.edit(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.followup.send("This is not for you.", ephemeral=True)
            return False
        else:
            return True

class multipage(View):

    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx

    @nextcord.ui.select(
        placeholder = "Go to page:", 
        options = [
            SelectOption(
                label = "Go to page B",
                value = "page B"
            ),
            SelectOption(
                label = "Go to page C",
                value = "page C"
            )
        ],
        min_values = 1, 
        max_values = 1
    )
    async def select_menu(self, select, interaction):
        await interaction.response.send_message(f'You chose {select.values[0]}')

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.followup.send("This is not for you.", ephemeral=True)
            return False
        else:
            return True