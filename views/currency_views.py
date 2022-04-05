import os
import nextcord
import random
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed, SelectOption 
from nextcord.ui import Button, View
import database as db
from typing import Optional
from functions.users import Users

class EndInteraction(View):

    @nextcord.ui.button(label = "End Interaction", style = nextcord.ButtonStyle.red, emoji = "⏹️")
    async def button_callback(self, button, interaction):
        button.label = "Interaction ended"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Interaction ended.")

class Generate(View):

    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx

    @nextcord.ui.button(
        label = "Generate gold!", 
        style = nextcord.ButtonStyle.grey, 
        emoji = "🪙"
    )
    async def gold_generate(self, button, interaction):
        users = Users(self.ctx.author)
        profile = users.get_user_profile()
        profile["user"]["gold"] += 500
        profile = users.update_user_profile(profile)
        button.label = "Gold obtained!"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Something appears in front of you. You pick it up and be **really** suprised that it's some gold COINS!", ephemeral=True)

    @nextcord.ui.button(
        label = "Generate XP!", 
        style = nextcord.ButtonStyle.grey, 
        emoji = "📚"
    )
    async def xp_generate(self, button, interaction):
        users = Users(self.ctx.author)
        profile = users.get_user_profile()
        profile["user"]["xp"] += random.choice(range(6))
        profile = users.update_user_profile(profile)
        button.label = "No more books..."
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("You take your time and read a book, and learnt something new!", ephemeral=True)
    
    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.message.edit(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f"This is not for you, sorry.\nUse `{self.ctx.command}`", ephemeral=True)
            return False
        else:
            return True

class MultiplePages(View):

    def __init__(self, ctx, pages):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.pages = pages
        self.page_to_return = None
        self.to_page_b_btn = None
        self.go_back_btn = Button(
            label = "Go Back",
            style = nextcord.ButtonStyle.grey,
            row = 4,
            custom_id = "go_back"
      	)
        async def go_back(go_back_interaction):
            if self.page_to_return and [i for i in self.children if i.custom_id=="go_back"][0]:
                page_ui = self.page_to_return 
                self.page_to_return = None
                to_page_b_btn = None
                for i in self.children:
                    if i.custom_id == "to_page_b":
                        to_page_b_btn = i
                if not to_page_b_btn:
                    self.add_item(self.to_page_b_btn)
                self.remove_item(self.go_back_btn)
                await go_back_interaction.response.edit_message(embed=page_ui, view=self)
                self.message = await self.ctx.fetch_message(self.message.id)
        self.go_back_btn.callback = go_back

    @nextcord.ui.button(
        label = "Go to page B",
        style = nextcord.ButtonStyle.grey,
        emoji = "🔖",
        custom_id = "to_page_b"
    ) 
    async def to_page_b(self, button, interaction):
        page_ui = self.pages.page_ui_b()        
        self.page_to_return = self.message.embeds[0]
        self.to_page_b_btn = button
        self.remove_item(button)
        go_back_btn = None
        for i in self.children:
            if i.custom_id == "go_back":
                go_back_btn = i
        if not go_back_btn:
            self.add_item(self.go_back_btn)
        await interaction.response.edit_message(embed=page_ui, view=self)
        self.message = await self.ctx.fetch_message(self.message.id)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.message.edit(view=self)
        self.message = await self.ctx.fetch_message(self.message.id)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f"This is not for you, sorry.\nUse `{self.ctx.command}`", ephemeral=True)
            return False
        else:
            return True

class PagesWithSelect(View):

    def __init__(self, ctx, pages):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.pages = pages
        self.page_to_return = []
        self.go_back_btn = Button(
            label = "Go Back",
            style = nextcord.ButtonStyle.grey,
            row = 4,
            custom_id = "go_back"
      	)
        async def go_back(go_back_interaction):
            if self.page_to_return != [] and [i for i in self.children if i.custom_id=="go_back"][0]:
                page_ui = self.page_to_return[-1]
                self.page_to_return.pop()
                if self.page_to_return == []:
                    self.remove_item(self.go_back_btn)
                await go_back_interaction.response.edit_message(embed=page_ui, view=self)
                self.message = await self.ctx.fetch_message(self.message.id)
        self.go_back_btn.callback = go_back

    @nextcord.ui.select(
        placeholder = "Go to page:",  
        options = [
            SelectOption(
                label = "Go to page 1",
                value = "page A"
            ),
            SelectOption(
                label = "Go to page 2",
                value = "page B"
            ),
            SelectOption(
                label = "Go to page 3",
                value = "page C"
            )
        ],
        min_values = 1, 
        max_values = 1
    )
    async def select_menu(self, select, interaction):
        if select.values[0] == "page A":
            page_ui = self.pages.something()
        elif select.values[0] == "page B":
            page_ui = await self.pages.keith_sucks()
        elif select.values[0] == "page C":
            page_ui = self.pages.everything()
        self.page_to_return.append(self.message.embeds[0])
        go_back_btn = None
        for i in self.children:
            if i.custom_id == "go_back":
                go_back_btn = i
        if not go_back_btn:
            self.add_item(self.go_back_btn)
        await interaction.response.edit_message(embed=page_ui, view=self)
        self.message = await self.ctx.fetch_message(self.message.id)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.message.edit(view=self)
        self.message = await self.ctx.fetch_message(self.message.id)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f"This is not for you, sorry.\nUse `{self.ctx.command}`", ephemeral=True)
            return False
        else:
            return True
