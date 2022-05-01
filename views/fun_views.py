import os
import nextcord
import random
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed, SelectOption, Interaction
from nextcord.ui import Button, View, button, Modal, TextInput
import database as db
from typing import Optional
from functions.users import Users

class Analysis(View):
                
    def __init__(self, interaction: Interaction, result, most, least):
        super().__init__(timeout=180)
        self.interaction = interaction
        self.most = most
        self.least = least
        self.result = result

    @button(
        label = "Show Analysis", 
        style = nextcord.ButtonStyle.blurple, 
        emoji = "📊"
    )
    async def show_analysis(self, button, interaction):
        embed = Embed()
        msg = "```md\n"
        msg += "# Analysis:\n"
        msg += "\t- <MOST>:\n"
        for i in self.most:
            msg += f"\t\t* [{self.result.count(str(i))}]({i}s)\n"
        msg += "\t- <LEAST>:\n"
        for i in self.least:
            msg += f"\t\t* [{self.result.count(str(i))}]({i}s)\n"
        msg += "> great, isn't it? took SkyeWong#8577 2 days to make this!\n"
        msg += "```"
        embed.description = msg
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.interaction.edit_original_message(view=self)

class HitAndBlowData():
    
    def __init__(self):
        self.ans = []
        for i in range(4):
            self.ans.append(str(random.randint(0, 9)))
        self.tries = []
class HitAndBlowView(View):

    def __init__(self, slash_interaction: Interaction, data_class):
        super().__init__(timeout=3600)
        self.slash_interaction = slash_interaction
        self.data_class = data_class

    @button(
        label = "GUESS!",
        emoji = "🔢",
        style = nextcord.ButtonStyle.blurple
    )
    async def show_modal(self, button, interaction: Interaction):
        await interaction.response.send_modal(HitAndBlowModal(self.slash_interaction, interaction, self.data_class))

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.slash_interaction.user:
            await interaction.response.send_message(f"This is not for you, sorry.", ephemeral=True)
            return False
        else:
            return True

class HitAndBlowModal(Modal):

    def __init__(self, slash_interaction: Interaction, btn_interaction: Interaction, data_class):
        super().__init__(
            title = "Hit & Blow",
            timeout=None
        )
        self.slash_interaction = slash_interaction
        self.btn_interaction = btn_interaction
        self.data_class = data_class
        self.num = TextInput(
            label = "Enter a four-digit number",
            min_length = 4,
            max_length = 4
        )
        self.add_item(self.num)

    async def callback(self, interaction: Interaction):
        slash_msg = await self.slash_interaction.original_message()
        msg_embed = slash_msg.embeds[0]
        if len(msg_embed.fields) > 0:
            if msg_embed.fields[-1].name == "⚠️ ERROR!":
                msg_embed.remove_field(-1)
        if self.num.value.isnumeric():
            tries = self.data_class.tries
            tries.append(self.num.value)
            guesses_field_value = ""
            for i in range(len(tries)):
                guesses_field_value += f"\n`{i + 1}` - `{tries[i]}`"
            msg_embed.add_field(name="GUESSES", value=guesses_field_value)
            await interaction.send(f"you guessed: {self.num.value}\nthe correct number is: {''.join(self.data_class.ans)}", ephemeral=True)
        else:
            msg_embed.add_field(name="⚠️ ERROR!", value="The inputted value is not a four-digit number")
        await self.slash_interaction.edit_original_message(embed=msg_embed)