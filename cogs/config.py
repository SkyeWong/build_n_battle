import os
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

class Config(commands.Cog, name="Config"):
    COG_EMOJI = "⚙️"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 
    
    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        await ctx.send(f"Guild name: {ctx.guild.name}\nGuild id: {ctx.guild.id}\nprefix: {prefix}")
        if len(prefix) > 15:
            await ctx.send("A prefix can only be 15 characters or shorter.")
        else:
            print("making sql")
            sql = f"""
                UPDATE 
                    server_prefixes
                SET
                    prefix = {prefix}
                WHERE
                    server_id = {ctx.guild.id}
                """
            print("made sql, executing")
            db.execute_query(sql)
            print("executed, commiting")
            db.conn.commit()
            print("commiting, sending message")
            await ctx.send(f"The prefix for {ctx.guild.name} has been changed to {prefix}")
            print("message sent")

def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))