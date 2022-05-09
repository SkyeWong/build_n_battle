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
        cog_select_menu.options = self._get_cogs_option()
    
    def _get_cogs_option(self) -> list[SelectOption]:
        options: list[SelectOption] = []
        for cog_name in self.cog_commands:
            default = False
            if cog_name == self.default_cog_name:
                default = True
            cog = self.cog_commands[cog_name][0]
            emoji = getattr(cog, "COG_EMOJI", None)
            description = ""
            if cog.description:
                if len(cog.description) > 90:
                    description = f"{cog.description[:90]}..."
                else:
                    description = cog.description
            options.append(SelectOption(
                label = cog_name, 
                emoji = emoji,
                description = description if cog.description else "...",
                default = default
            ))
        return options

    def get_help_embed(self, cog_name):
        exists = False
        for i in self.cog_commands:
            if i == cog_name:
                exists = True
                break
        if not exists:
            return False
        else:
            embed = Embed()
            embed.colour = random.choice(main.embed_colours)
            embed.set_author(name="Commands", icon_url=bot.user.display_avatar.url)
            for cmd in self.cog_commands[cog_name][1]:
                embed.add_field(name=f"/{cmd.get_signature()[0]}\n", value=f"`➼` {cmd.description if len(cmd.description) < 30 else cmd.desciription[-30] + '...'}", inline=False)
            return embed

    @select(
        placeholder = "Choose a category...",  
        options = [],
        min_values = 1,
        max_values = 1,
        custom_id = "cog_select"
    )
    async def select_cog(self, select: nextcord.ui.Select, interaction: Interaction):
        embed = self.get_help_embed(select.values[0])
        for option in select.options:
            option.default = False
            if option.label == select.values[0]:
                option.default = True
        await self.slash_interaction.edit_original_message(embed=embed, view=self)
        await interaction.send(f"you chose the category: {select.values[0]}", ephemeral=True)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.slash_interaction.edit_original_message(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.slash_interaction.user:
            await interaction.response.send_message(f"This is not for you, sorry.\nUse `{self.slash_interaction.application_command}`", ephemeral=True)
            return False
        else:
            return True