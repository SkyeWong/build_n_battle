import os
from discord import SlashOption
from nextcord import ButtonStyle
import nextcord
import json 
from datetime import datetime
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction
from nextcord.ui import Button, View

class EmojiView(View):
    
    def __init__(self, slash_interaction: Interaction, emoji_list, get_embed_func):
        super().__init__(timeout=300)
        self.slash_interaction = slash_interaction
        self.emoji_list = emoji_list
        self.get_embed_func = get_embed_func
        self.page = 1

    @nextcord.ui.button(
        emoji = "◀️",
        style = nextcord.ButtonStyle.blurple,
        disabled = True
    )
    async def back(self, button: Button, btn_interaction: Interaction):
        self.page -= 1
        if self.page == 1:
            button.disabled = True
        else:
            button.disabled = False
        embed = self.get_embed_func(self.emoji_list, self.page)
        await self.slash_interaction.edit_original_message(embed=embed)

    @nextcord.ui.button(
        emoji = "▶️",
        style = nextcord.ButtonStyle.blurple
    )
    async def next(self, button: Button, btn_interaction: Interaction):
        self.page += 1
        if self.page == len(self.emoji_list):
            button.disabled = True
        else:
            button.disabled = False
        embed = self.get_embed_func(self.emoji_list, self.page)
        await self.slash_interaction.edit_original_message(embed=embed)
