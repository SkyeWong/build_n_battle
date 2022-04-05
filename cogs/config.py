from curses.ascii import isalpha
import os
from discord import ButtonStyle
import nextcord
import random
import main
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed
from nextcord.ui import Button, View
import database as db
from typing import Optional
from functions.users import Users
from views.config_views import AddSpaceInPrefix
class Config(commands.Cog, name="Config"):
    COG_EMOJI = "⚙️"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 
    
    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        if len(prefix) > 15:
            await ctx.send("A prefix can only be 15 characters or shorter.")
        else:
            prefix_ui = Embed()
            prefix_ui.title = f"Setting the prefix:"
            def get_embed_description():
                return f"Server: `{ctx.guild.name}`\nPrefix: `{prefix}`"
            prefix_ui.description = get_embed_description()
            if str(prefix[-1]).isalpha():
                prefix_ui.add_field(name="Add a space?", value="I noticed that the last character is a letter. Do you want me to add a space after it?")
                class ChangePrefix():
                    def __init__(self, ctx, prefix):
                        self.ctx = ctx
                        self.prefix = prefix

                    def confirm_page(self):
                        self.prefix += " "
                        page = Embed()
                        page.title = prefix_ui.title
                        page.description = get_embed_description()
                        page.add_field(name="Great! I added a space.")
                        return page
                    
                    def cancel_page(self):
                        page = Embed()
                        page.title = prefix_ui.title
                        page.description = get_embed_description()
                        page.add_field(name="Fine. The space is not added.")
                        return page
                        
                changeprefix = ChangePrefix(ctx, prefix)
                view = AddSpaceInPrefix(ctx, ChangePrefix)
                view.message = await ctx.send(embed=prefix_ui, view=view)
            await ctx.send(embed=prefix_ui)

def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))