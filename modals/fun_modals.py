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

    def __init__(self, ans, num_label = "Enter a four-digit number"):
        super().__init__(
            title = "Guess a number:",
            timeout=None
        )
        self.num = TextInput(
            label = num_label,
            style = nextcord.TextInputStyle.paragraph,
            min_length = 4,
            max_length = 4
        )
        self.add_item(self.num)
        self.ans = ans

    async def callback(self, interaction: Interaction):
        correct_input = False
        while not correct_input:
            await interaction.response.send_modal(self(self.ans, "It isn't a four digit number. Try again."))
            if self.num.value.isnumeric():
                correct_input = True
        await interaction.send(f"you guessed: {self.num.value}\nthe correct number is: {''.join(self.ans)}")