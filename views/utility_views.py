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

    def __init__(self, slash_interaction: Interaction, mapping: dict, default_cog_name: str = "Currency"):
        super().__init__(timeout=180)
        self.slash_interaction = slash_interaction
        self.mapping = mapping
        self.default_cog_name = default_cog_name
        self.cmd_list = mapping[default_cog_name][1]
        cog_select_menu = [i for i in self.children if i.custom_id == "cog_select"][0]
        cog_select_menu.options = self._get_cogs_option()
        self.page = 1
        self.cmd_per_page = 8
    
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
        set_author: bool = True,
        author_name: str = "Commands"
    ):  
        command_list = self.cmd_list
        embed = Embed()
        embed.colour = random.choice(main.embed_colours)
        if description:
            embed.description = description
        if set_author:
            avatar = bot.user.avatar or bot.user.default_avatar
            embed.set_author(name=author_name, icon_url=avatar.url)
        if not command_list:
            for cog_name in self.mapping:
                if cog_name == self.default_cog_name:
                    command_list = self.mapping[cog_name][1]
                    break
        filtered = []
        for i in command_list:
            cmd_in_guild = False
            if isinstance(i, nextcord.ApplicationCommand):
                if i.is_global:
                    cmd_in_guild = True
                elif self.slash_interaction.guild_id in i.guild_ids:
                    cmd_in_guild = True
            elif isinstance(i, nextcord.ApplicationSubcommand):
                parent_cmd = i.parent_command
                while not isinstance(parent_cmd, nextcord.ApplicationCommand):
                    parent_cmd = parent_cmd.parent_command
                if parent_cmd:
                    if parent_cmd.is_global:
                        cmd_in_guild = True
                    elif self.slash_interaction.guild_id in parent_cmd.guild_ids:
                        cmd_in_guild = True
            if cmd_in_guild:
                filtered.append(i)
        print(self.get_page_start_index(), self.get_page_end_index())
        final_cmd_list = filtered[self.get_page_start_index():self.get_page_end_index()]
        for cmd in final_cmd_list:
            value = cmd.description if cmd.description else "..."
            if len(value) > 50:
                value = f"{value[:50]}..."
            embed.add_field(
                name = f"/{cmd.name}" if isinstance(cmd, nextcord.ApplicationCommand) else f"/{cmd.full_parent_name} {cmd.name}",
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
        self.page = 1
        self.cmd_list = self.mapping[select.values[0]][1]
        embed = self.help_embed()
        for option in select.options:
            option.default = False
            if option.label == select.values[0]:
                option.default = True
        await self.slash_interaction.edit_original_message(embed=embed, view=self)

    def get_page_start_index(self):
        return (self.page - 1) * self.cmd_per_page

    def get_page_end_index(self):
        index = self.get_page_start_index() + self.cmd_per_page
        return index if index < len(self.cmd_list) else len(self.cmd_list) - 1
    
    async def btn_disable(self):
        back_btn = [i for i in self.children if i.custom_id=="back"][0]
        first_btn = [i for i in self.children if i.custom_id=="first"][0]
        if self.page == 1:
            back_btn.disabled = True
            first_btn.disabled = True
        else:
            back_btn.disabled = False
            first_btn.disabled = False
        next_btn = [i for i in self.children if i.custom_id=="next"][0]
        last_btn = [i for i in self.children if i.custom_id=="last"][0]
        if self.page == len(self.cmd_list):
            next_btn.disabled = True
            last_btn.disabled = True
        else:
            next_btn.disabled = False
            last_btn.disabled = False

    @button(
        emoji = "⏮️",
        style = nextcord.ButtonStyle.blurple,
        custom_id = "first",
        disabled = True
    )
    async def first(self, button: Button, btn_interaction: Interaction):
        self.page = 1
        await self.btn_disable(btn_interaction)
        embed = self.help_embed()
        await self.slash_interaction.edit_original_message(embed=embed)

    @button(
        emoji = "◀️",
        style = nextcord.ButtonStyle.blurple,
        disabled = True,
        custom_id = "back"
    )
    async def back(self, button: Button, btn_interaction: Interaction):
        self.page -= 1
        await self.btn_disable(btn_interaction)
        embed = self.help_embed()
        await self.slash_interaction.edit_original_message(embed=embed)

    @button(
        emoji = "▶️",
        style = nextcord.ButtonStyle.blurple,
        custom_id = "next"
    )
    async def next(self, button: Button, btn_interaction: Interaction):
        self.page += 1
        await self.btn_disable(btn_interaction)
        embed = self.help_embed()
        await self.slash_interaction.edit_original_message(embed=embed)

    @button(
        emoji = "⏭️",
        style = nextcord.ButtonStyle.blurple,
        custom_id = "last"
    )
    async def last(self, button: Button, btn_interaction: Interaction):
        self.page = len(self.cmd_list)
        await self.btn_disable(btn_interaction)
        embed = self.help_embed()
        await self.slash_interaction.edit_original_message(embed=embed)
    
    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.slash_interaction.edit_original_message(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.slash_interaction.user:
            await interaction.response.send_message(f"This is not for you, sorry.\nUse `/{self.slash_interaction.application_command}`", ephemeral=True)
            return False
        else:
            return True