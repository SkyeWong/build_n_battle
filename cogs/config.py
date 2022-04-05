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
            prefix_ui.colour = random.choice(main.embed_colours)
            def get_embed_description(prefix_desc):
                return f"Server: `{ctx.guild.name}`\nPrefix: `{prefix_desc}`"
            def change_prefix(prefix):
                sql = f"""
                UPDATE 
                    server_prefixes
                SET
                    prefix = "{prefix}"
                WHERE
                    server_id = {ctx.guild.id}
                """
                db.execute_query(sql)
                db.conn.commit()
            prefix_ui.description = get_embed_description(prefix)
            if str(prefix[-1]).isalpha():
                prefix_ui.add_field(name="Add a space?", value="I noticed that the last character is a letter. Do you want me to add a space after it?")
                class ChangePrefix():
                    def __init__(self, ctx, prefix):
                        self.ctx = ctx
                        self.prefix = prefix

                    def confirm_page(self):
                        self.prefix += " "
                        change_prefix(self.prefix)
                        page = Embed()
                        page.title = "Prefix set!"
                        page.description = get_embed_description(self.prefix)
                        page.add_field(name="",value="Great! I added a space.")
                        return page
                    
                    def cancel_page(self):
                        change_prefix(self.prefix)
                        page = Embed()
                        page.title = "Prefix set!"
                        page.description = get_embed_description(self.prefix)
                        page.add_field(name="",value="Fine. The space is not added.")
                        return page
            
                changeprefix = ChangePrefix(ctx, prefix)
                view = AddSpaceInPrefix(ctx, changeprefix)
                prefix_ui.title = "Setting the prefix:"
                view.message = await ctx.send(embed=prefix_ui, view=view)
            else:
                change_prefix(prefix)
                prefix_ui.title = "Prefix set!"
                await ctx.send(embed=prefix_ui)

def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))