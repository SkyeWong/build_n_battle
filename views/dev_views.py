import os
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
    
    async def btn_disable(self, interaction: Interaction):
        back_btn = [i for i in self.children if i.custom_id=="back"][0]
        if self.page == 1:
            back_btn.disabled = True
        else:
            back_btn.disabled = False
        next_btn = [i for i in self.children if i.custom_id=="next"][0]
        if self.page == len(self.emoji_list):
            next_btn.disabled = True
        else:
            next_btn.disabled = False
        await interaction.response.edit_message(view=self)

    @nextcord.ui.button(
        emoji = "◀️",
        style = nextcord.ButtonStyle.blurple,
        disabled = True,
        custom_id = "back"
    )
    async def back(self, button: Button, btn_interaction: Interaction):
        self.page -= 1
        await self.btn_disable(btn_interaction)
        embed = self.get_embed_func(self.emoji_list, self.page)
        await self.slash_interaction.edit_original_message(embed=embed)

    @nextcord.ui.button(
        emoji = "▶️",
        style = nextcord.ButtonStyle.blurple,
        custom_id = "next"
    )
    async def next(self, button: Button, btn_interaction: Interaction):
        self.page += 1
        await self.btn_disable(btn_interaction)
        embed = self.get_embed_func(self.emoji_list, self.page)
        await self.slash_interaction.edit_original_message(embed=embed)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.slash_interaction.edit_original_message(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.slash_interaction.user:
            await interaction.response.send_message(f"This is not for you, sorry.", ephemeral=True)
            return False
        else:
            return True
