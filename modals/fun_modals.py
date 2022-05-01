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
from nextcord.ui import Button, View, Modal, TextInput

class HitAndBlowModal(Modal):

    def __init__(self, message = None):
        super().__init__(
            title = "Guess a number:",
            timeout=None)
        self.text = TextInput(
            label = message or "enter whatever you want",
            style = nextcord.TextInputStyle.paragraph,
            placeholder = "skye is really smart",
            max_length = 150,
            required = True
        )
        self.add_item(self.text)
    
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} you typed: {self.text.value}", ephemeral=True)