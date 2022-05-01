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

class HitAndBlow(Modal):

    def __init__(self, timeout = None, message = None):
        super().__init__(
            title = "Guess a number:",
            timeout=timeout)
        self.text = TextInput(
            label = "enter whatever you like" or message,
            style = nextcord.TextInputStyle.paragraph,
            placeholder = "skye is really smart",
            min_length = 3,
            max_length = 50,
            required = True
        )
        self.add_item(self.text)
    
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} you typed: {self.text.value}")