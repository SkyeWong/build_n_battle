import os
import nextcord
import random
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed, SelectOption, Interaction
from nextcord.ui import Button, View, button, select, Modal, TextInput
import database as db
from typing import Optional
from functions.users import Users

class HelpView(View):

    def __init__(self, slash_interaction: Interaction, cog_commands: dict, default_cog_name: str):
        super().__init__(timeout=180)
        self.slash_interaction = slash_interaction
        self.cog_commands = cog_commands
        self.default_cog_name = default_cog_name
        cog_select_menu = [i for i in self.children if i.custom_id == "cog_select"][0]
        cog_select_menu.options = self.get_cogs_option()
    
    def get_cogs_option(self):
        selectoptions = []
        for cog_name in self.cog_commands:
            default = False
            if cog_name == self.default_cog_name:
                default = True
            selectoptions.append(SelectOption(label = cog_name, default = default))
        return selectoptions

    @select(
        placeholder = "Choose a category...",  
        options = [],
        min_values = 1,
        max_values = 1,
        custom_id = "cog_select"
    )
    async def select_cog(self, select, interaction: Interaction):
        pass