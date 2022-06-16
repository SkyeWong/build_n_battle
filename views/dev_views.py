from nextcord import ButtonStyle
import nextcord
import database as db
from datetime import datetime
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands
from nextcord import Embed, Interaction, SelectOption
from nextcord.ui import Button, View, button, Modal, TextInput, select, Select
from mysql.connector import Error

class EmojiView(View):
    
    def __init__(self, slash_interaction: Interaction, emoji_list, get_embed_func):
        super().__init__(timeout=300)
        self.slash_interaction = slash_interaction
        self.emoji_list = emoji_list
        self.get_embed_func = get_embed_func
        self.page = 1
    
    async def btn_disable(self, interaction: Interaction):
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
        if self.page == len(self.emoji_list):
            next_btn.disabled = True
            last_btn.disabled = True
        else:
            next_btn.disabled = False
            last_btn.disabled = False
        await interaction.response.edit_message(view=self)

    @button(
        emoji = "⏮️",
        style = nextcord.ButtonStyle.blurple,
        custom_id = "first",
        disabled = True
    )
    async def first(self, button: Button, btn_interaction: Interaction):
        self.page = 1
        await self.btn_disable(btn_interaction)
        embed = self.get_embed_func(self.emoji_list, self.page)
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
        embed = self.get_embed_func(self.emoji_list, self.page)
        await self.slash_interaction.edit_original_message(embed=embed)

    @button(
        emoji = "▶️",
        style = nextcord.ButtonStyle.blurple,
        custom_id = "next"
    )
    async def next(self, button: Button, btn_interaction: Interaction):
        self.page += 1
        await self.btn_disable(btn_interaction)
        embed = self.get_embed_func(self.emoji_list, self.page)
        await self.slash_interaction.edit_original_message(embed=embed)

    @button(
        emoji = "⏭️",
        style = nextcord.ButtonStyle.blurple,
        custom_id = "last"
    )
    async def last(self, button: Button, btn_interaction: Interaction):
        self.page = len(self.emoji_list)
        await self.btn_disable(btn_interaction)
        embed = self.get_embed_func(self.emoji_list, self.page)
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

class EditItemView(View):
    def __init__(self, slash_interaction: Interaction, item_id):
        super().__init__(timeout=180)
        self.slash_interaction = slash_interaction
        self.item_id = item_id
        sql = """
            SELECT name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price
            FROM items
            WHERE id = %s
            LIMIT 1
        """
        cursor = db.execute_query_dict(sql, (item_id,))
        results = cursor.fetchall()
        if len(results) != 0:
            self.item = results[0] 
        else:
            self.stop()
        select = [i for i in self.children if i.custom_id == "item_select"][0]
        columns = self._get_item_columns()
        for column in columns: 
            select.options.append(
                SelectOption(
                    label = column
                )
            )
            
    def _get_item_columns(self):
        sql = """
            SHOW COLUMNS
            FROM items
        """
        cursor = db.execute_query(sql)
        results = cursor.fetchall()
        columns = []
        for i in results:
            name = i[0]
            if name.lower() != "id":
                columns.append(name)
        return columns

    @select(
        placeholder = "Choose a value...",
        options = [],
        custom_id = "item_select"
    )
    async def edit_value(self, select: Select, interaction: Interaction):
        await interaction.response.send_modal(EditItemModal(self.item_id, select.values[0]))

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

class EditItemModal(Modal):
    def __init__(self, item_id, column):
        sql = """
            SELECT name
            FROM items
            WHERE id = %s
            LIMIT 1
        """
        cursor = db.execute_query_dict(sql, (item_id,))
        results = cursor.fetchall()
        item = results[0]
        super().__init__(
            title = f"Edit the item {item['name']}",
            timeout = None
        )
        self.item_id = item_id
        self.column = column
        sql = """
            SHOW COLUMNS
            FROM items
        """
        cursor = db.execute_query(sql)
        results = cursor.fetchall()
        columns = []
        for i in results:
            name = i[0]
            if name.lower() != "id":
                columns.append(name)
        if column in columns:
            self.input = TextInput(
                label = column
            )
            self.add_item(self.input)
    
    async def callback(self, interaction: Interaction):
        value = self.input.value
        if self.column in ("buy_price", "sell_price", "trade_price"):
            value = str(main.text_to_num(self.input.value))
        sql = f"""
            UPDATE items
            SET {self.column} = %s
            WHERE id = 1
        """
        try:
            cursor = db.execute_query(sql, (value,))
            db.conn.commit()
        except (AttributeError, Error) as error:
            await interaction.send("either you entered an invalid value or an internal error occured.", ephemeral=True)
            raise error
        await interaction.send(f"{interaction.user.mention} set {self.column} to {self.input.value}")
