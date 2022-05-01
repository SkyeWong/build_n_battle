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

    def __init__(self, slash_interaction: Interaction, btn_interaction: Interaction, ans, num_label = "Enter a four-digit number"):
        super().__init__(
            title = "Guess a number:",
            timeout=None
        )
        self.slash_interaction = slash_interaction
        self.btn_interaction = btn_interaction
        self.num = TextInput(
            label = num_label,
            style = nextcord.TextInputStyle.paragraph,
            min_length = 4,
            max_length = 4
        )
        self.add_item(self.num)
        self.ans = ans
        self.tries = []

    async def callback(self, interaction: Interaction):
        if self.num.value.isnumeric():
            msg_embed = slash_msg.embeds[0]
            if len(msg_embed.fields) > 0:
                msg_embed.remove_field(-1)
        else:
            slash_msg = await self.slash_interaction.original_message()
            msg_embed = slash_msg.embeds[0]
            if len(msg_embed.fields) > 0:
                msg_embed.remove_field(-1)
            msg_embed.add_field(name="⚠️ ERROR!", value="The inputted value is not a four-digit number")
        self.tries.append(self.num.value)
        msg_embed = slash_msg.embeds[0]
        guesses_field_value = ""
        for i in range(len(self.tries)):
            guesses_field_value += f"\n`{i + 1}` - `{self.tries[i]}`"
        msg_embed.add_field(name="GUESSES", value=guesses_field_value)
        await interaction.send(f"you guessed: {self.num.value}\nthe correct number is: {''.join(self.ans)}")