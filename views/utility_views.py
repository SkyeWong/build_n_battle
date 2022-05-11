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

    def __init__(self, slash_interaction: Interaction, mapping: dict, default_cog_name: str):
        super().__init__(timeout=180)
        self.slash_interaction = slash_interaction
        self.mapping = mapping
        self.default_cog_name = default_cog_name
        cog_select_menu = [i for i in self.children if i.custom_id == "cog_select"][0]
        cog_select_menu.options = self._get_cogs_option()
    
    def _get_cogs_option(self) -> list[SelectOption]:
        options: list[SelectOption] = []
        for cog_name in self.mapping:
            default = False
            if cog_name == self.default_cog_name:
                default = True
            cog = self.mapping[cog_name][0]
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

    def help_embed(
        self, 
        description: Optional[str] = None, 
        command_list: Optional[list[nextcord.ApplicationCommand]] = None, 
        set_author: bool = True
    ):
        embed = Embed()
        embed.colour = random.choice(main.embed_colours)
        if description:
            embed.description = description
        if set_author:
            avatar = bot.user.avatar or bot.user.default_avatar
            embed.set_author(name="Commands", icon_url=avatar.url)
        if not command_list:
            for cog_name in self.mapping:
                if cog_name == self.default_cog_name:
                    command_list = self.mapping[cog_name][0].to_register
                    break
        filtered = []
        for i in command_list:
            cmd_in_guild = False
            if i.is_global:
                cmd_in_guild = True
            elif self.slash_interaction.guild_id in i.guild_ids:
                cmd_in_guild = True
            if cmd_in_guild == True:
                filtered.append(i)
        for cmd in filtered:
            value = cmd.description if cmd.description else "..."
            if len(value) > 50:
                value = f"{description[:50]}..."
            embed.add_field(
                name = cmd.name,
                value = f"`➸` {value}",
                inline = False
            )
        return embed

    @select(
        placeholder = "Choose a category...",  
        options = [],
        min_values = 1,
        max_values = 1,
        custom_id = "cog_select"
    )
    async def select_cog(self, select: nextcord.ui.Select, interaction: Interaction):
        print(type(self.mapping[select.values[0]][1]), self.mapping[select.values[0]][1][0].name)
        embed = self.help_embed(self.mapping[select.values[0]][1])
        for option in select.options:
            option.default = False
            if option.label == select.values[0]:
                option.default = True
        await self.slash_interaction.edit_original_message(embed=embed, view=self)

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