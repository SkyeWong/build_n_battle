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
    
    def __init__(self, slash_interaction: Interaction, get_embed_class):
        super().__init__(timeout=300)
        self.slash_interaction = slash_interaction
        self.get_embed_class = get_embed_class
        self.page = 0

    @nextcord.ui.button(
        emoji = "▶️",
        style = nextcord.ButtonStyle.blurple
    )
    async def next(self, button: Button, btn_interaction: Interaction):
        self.page += 1
        embed = self.get_embed_class.get_emoji_embed(self.page)
        await self.slash_interaction.edit_original_message(embed=embed)
    
    @nextcord.ui.button(
        emoji = "◀️",
        style = nextcord.ButtonStyle.blurple
    )
    async def back(self, button: Button, btn_interaction: Interaction):
        self.page -= 1
        embed = self.get_embed_class.get_emoji_embed(self.page)
        await self.slash_interaction.edit_original_message(embed=embed)