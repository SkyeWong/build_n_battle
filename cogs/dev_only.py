import os
from nextcord import ButtonStyle
import nextcord
import json 
from datetime import datetime
import time
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction
from nextcord.ui import Button, View
class dev_only(commands.Cog, name="Dev Only"):
    """Commands only for the devs."""

    COG_EMOJI = "👨‍💻"
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    async def cog_check(self, ctx):
        #Check if user is owner and return it back
        return ctx.author.id in bot.owner_ids

    @nextcord.slash_command(name="dm", description="Send a message!", guild_ids=[main.DEVS_SERVER_ID])
    async def dm(self, interaction: Interaction, recipient: nextcord.Member, *, message: str):
        if interaction.user.id not in self.bot.owner_ids:
            await interaction.response.send_message("you are not a dev.")
        else:
            if recipient.bot == True:
                await interaction.response.send_message("I can't send a message to a BOT can i")
            else:
                await recipient.send(f"{interaction.user} sent a message to you via me, {bot.user.name}:\n {message}")
                embed = Embed()
                embed.title = "DM succesfully sent!"
                embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
                embed.description = "Message details:"
                embed.colour = random.choice(main.embed_colours)
                embed.add_field(name="From:", value=interaction.user, inline=True)
                embed.add_field(name="To:", value=recipient, inline=True)
                embed.add_field(name="Message:", value=message, inline=True)
                embed.add_field(name="Sent at:", value=f'<t:{int(datetime.now().timestamp())}>', inline=True)
                embed.set_footer(text="Note: markdowns and mentions will be escaped while sending the message!")
                await interaction.response.send_message(embed=embed)

    @commands.command(name="avatar", help="Shows avatar!")
    async def avatar(self, ctx, user: nextcord.Member=None):
        if user == None:
            user = ctx.author
        await ctx.send(f"<{user.display_avatar.url}>")
        await ctx.send(user.display_avatar.url)

    @commands.command(name="emoji")
    async def emoji(self, ctx, *, emojiname:str):
        """Let the bot find you any emojis in any servers that the bot is in.
        Search the emoji by typing the emoji name. Seperate emojis with ",".
        Please note that the bot ONLY searches for server emojis. Default emojis will **NOT** be searched."""
        emojis = emojiname.split(", ")
        emojis_found = []
        guild_emojis = []
        for guild in bot.guilds:
            for emoji in guild.emojis:
                guild_emojis.append(emoji)
        for i in emojis:
            emojis_found.append(nextcord.utils.get(guild_emojis, name=i))
        response = "The emoji(s) you required should be: "
        for i in range(len(emojis_found)):
            emoji = emojis_found[i]
            response += f"\n\n{i+1}: "
            if emojis_found[i] == None:
                response += f"No emoji is found for \"{emojis[i]}\"! Check the name and try again. Is it a default emoji? The bot only searches for server emojis."
            else:
                response += f"{emoji}\n> Name - :{emoji.name}:\n> Guild - {emoji.guild.name}\n> ID - `{emoji.id}`\n> Url - `{emoji.url}`"
        response += "\n\nThe bot only checks for the first match of the emoji. Other emojis with identical names won't be found."
        await ctx.send(response)

def setup(bot: commands.Bot):
    bot.add_cog(dev_only(bot))

