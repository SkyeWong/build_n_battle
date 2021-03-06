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
            SELECT name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price, rarity
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
        select.options = []
        for column in self._get_item_columns(): 
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

    def get_item_embed(self):
        embed = Embed()
        item = self.item
        embed.colour = random.choice(main.embed_colours)
        embed.title = "Current values of "
        embed.title += item["name"]
        embed.description = ">>> "
        embed.description += item["description"]
        embed.description += f"\n\n**BUY** - {item['buy_price']}\n**SELL** - {item['sell_price']}\n**TRADE** - {item['trade_price']}"
        # **rarity**
        # 0 - common
        # 1 - uncommon
        # 2 - rare
        # 3 - epic
        # 4 - legendary
        # 5 - godly
        rarity = ["common", "uncommon", "rare", "epic", "legendary", "godly"]
        embed.add_field(name="Rarity", value=rarity[item["rarity"]])
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{item['emoji_id']}.png")
        return embed

    @select(
        placeholder = "Choose a value...",
        options = [],
        custom_id = "item_select"
    )
    async def edit_value(self, select: Select, interaction: Interaction):
        await interaction.response.send_modal(EditItemModal(self.slash_interaction, self.item_id, select.values[0]))

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
    def __init__(self, slash_interaction: Interaction, item_id: int, column):
        self.slash_interaction = slash_interaction
        sql = """
            SELECT name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price, rarity
            FROM items
            WHERE id = %s
            LIMIT 1
        """
        cursor = db.execute_query_dict(sql, (item_id,))
        self.item = cursor.fetchall()[0]
        super().__init__(
            title = f"Editing the item {self.item['name']}",
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
    
    def get_item_embed(self):
        embed = Embed()
        item = self.item
        embed.colour = random.choice(main.embed_colours)
        embed.title = "Current values of "
        embed.title += item["name"]
        embed.description = ">>> "
        embed.description += item["description"]
        embed.description += f"\n\n**BUY** - {item['buy_price']}\n**SELL** - {item['sell_price']}\n**TRADE** - {item['trade_price']}"
        # **rarity**
        # 0 - common
        # 1 - uncommon
        # 2 - rare
        # 3 - epic
        # 4 - legendary
        # 5 - godly
        rarity = ["common", "uncommon", "rare", "epic", "legendary", "godly"]
        embed.add_field(name="Rarity", value=rarity[item["rarity"]])
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{item['emoji_id']}.png")
        return embed
    
    async def callback(self, interaction: Interaction):
        # get the value from the modal
        value = self.input.value
        errors = []
        # if value in one of these convert them from "2k" to 2000
        if self.column in ("buy_price", "sell_price", "trade_price"):
            # if the value is 0, change it to None
            if value == 0:
                value = None
            else:
                value = str(main.text_to_num(self.input.value))
                if value == False:
                    errors.append("This is not a valid number. Tip: use `2k` for _2,000_, `5m 4k` for _5,004,000_")
        # if value is name max length = 30
        if self.column == "name" and len(value) > 30:
            errors.append("The name must not be more than 30 characters in length.")
        # if value is description max length = 100
        if self.column == "description" and len(value) > 100:
            errors.append("The description must not be more than 100 characters in length.")
        # **rarity**
        # 0 - common
        # 1 - uncommon
        # 2 - rare
        # 3 - epic
        # 4 - legendary
        # 5 - godly
        rarity = ["common", "uncommon", "rare", "epic", "legendary", "godly"]
        if self.column == "rarity":
            value = value.lower()
            if value.isnumeric():
                if int(value) < 0 or int(value) > 5 :
                    errors.append("use numbers 0-5 respectively representing `common`, `uncommon`, `rare`, `epic`, `legendary`, `epic` only")
            else:
                if value in rarity:
                    value = rarity.index(value)
                else:
                    errors.append("The rarity must be one of these: `common`, `uncommon`, `rare`, `epic`, `legendary`, `epic`")
        # if it is an invalid value send a message and return the function
        if len(errors) > 0:
            msg = "The following errors occured:"
            for i in errors:
                msg += f"\n{i}"
            await interaction.send(msg, ephemeral=True)
            return
        sql = f"""
            UPDATE items
            SET {self.column} = %s
            WHERE id = %s
        """
        try:
            cursor = db.execute_query(sql, (value, self.item_id))
            db.conn.commit()
        except (AttributeError, Error) as error:
            await interaction.send("either you entered an invalid value or an internal error occured.", ephemeral=True)
            raise error
        original_value = self.item[self.column]
        sql = """
            SELECT name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price, rarity
            FROM items
            WHERE id = %s
            LIMIT 1
        """
        cursor = db.execute_query_dict(sql, (self.item_id,))
        self.item = cursor.fetchall()[0]
        await self.slash_interaction.edit_original_message(embed=self.get_item_embed())
        await interaction.guild.get_channel(988046548309016586).send(f"{interaction.user.mention} set the `{self.column}` of `{self.item['name']}` from `{original_value}` to `{self.input.value}`, or `{value}`")

class ConfirmDelete(View):

    def __init__(self, slash_interaction: Interaction, item):
        super().__init__(timeout=30)
        self.slash_interaction = slash_interaction
        self.item = item
        embed = Embed()
        embed.colour = random.choice(main.embed_colours)
        embed.description = f"Item: `{item}`"
        self.embed = embed

    @button(
        emoji = "✅", 
        style = nextcord.ButtonStyle.blurple
    )
    async def confirm(self, button: Button, interaction: Interaction):
        sql = """
        DELETE 
        FROM items 
        WHERE name = %s
        """
        cursor = db.execute_query(sql, (self.item,))
        db.conn.commit()
        self.embed.title = "Item deleted!"
        button.style = nextcord.ButtonStyle.green
        button.disabled = True
        await self.slash_interaction.edit_original_message(view=self)
        await interaction.send(embed=self.embed)
        await interaction.guild.get_channel(988046548309016586).send(f"{self.slash_interaction.user.mention} deleted the item `{self.item}`")
    
    @button(
        emoji = "❎",
        style = nextcord.ButtonStyle.blurple
    )
    async def cancel(self, button: Button, interaction: Interaction):
        self.embed.title = "Item saved!"
        button.style = nextcord.ButtonStyle.red
        button.disabled = True
        await self.slash_interaction.edit_original_message(view=self)
        await interaction.send(embed=self.embed)
