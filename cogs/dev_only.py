import os
from discord import ButtonStyle
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
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def cog_check(self, ctx):
        #Check if user is owner and return it back
        return ctx.author.id in bot.owner_ids

    @bot.slash_command(name="dm", description="Send a message! also this is my first slash command")
    async def dm(self, interaction:Interaction, recipient: nextcord.Member, *, message: str):
        if recipient.bot == True:
            await interaction.response.send_message("I can't send a message to a BOT can i")
        else:
            await recipient.send(f"{interaction.user} sent a message to you via me, {bot.user.name}:\n {message}")
            embed = nextcord.Embed()
            embed.title = "DM succesfully sent!"
            embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            embed.description = "Message details:"
            embed.colour = random.choice(main.embed_colours)
            embed.add_field(name="From:", value=interaction.user, inline=True)
            embed.add_field(name="To:", value=recipient, inline=True)
            embed.add_field(name="Message:", value=message, inline=True)
            embed.add_field(name="Sent at:", value=f'<t:{int(datetime.now().timestamp())}>', inline=True)
            embed.set_footer(text="Note: markdowns and mentions will be escaped while sending the message!")
            await interaction.response.send_messsage(embed=embed)

    @commands.command(name="dice", brief="Roll a dice and make decisions!", help="The bot rolls a dice from 1 to 6 and displays the result. You can specify the number of dices! The number of dices is optional. Defaults to 1.") 
    async def dice(self, ctx, number_of_sides: int, number_of_dice: int=None):
        if number_of_dice == None:
            number_of_dice = 1
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        embed = nextcord.Embed()
        embed.title = f"I rolled {number_of_dice} dice(s) with {number_of_sides} sides and the result is:"
        embed.description = ", ".join(dice)
        embed.colour = random.choice(main.embed_colours)
        await ctx.send(embed=embed)

    @commands.command(name="karson", help="Shows Karson in a big collage!")
    async def karson(self, ctx):
        embed = nextcord.Embed()
        embed.set_image(url="https://i.ibb.co/vzRD2LC/big-collage.jpg")
        karson_user = await bot.fetch_user(708141816020729867)
        embed.set_author(name="MEET KARSON:", icon_url= karson_user.avatar)
        embed.colour = random.choice(main.embed_colours)
        await ctx.send(embed=embed)

    @commands.command(name="dicegame", brief="Play a simple dice game!", help="i will just do this later-if you sees this maybe remind me!")
    async def dicegame(self, ctx):
        money = 500
        author_avatar = ctx.author.avatar
        dice_ui = nextcord.Embed()
        dice_ui.colour = random.choice(main.embed_colours)
        dice_ui.set_author(name=f"{ctx.author.name}\"s Dicegame", icon_url= author_avatar)
        dice_ui_message = await ctx.send(embed=dice_ui)
        while money > 10:
            dice_ui.insert_field_at(index=0, name="Your money left:", value=f"${money}", inline=False)
            dice_ui.insert_field_at(index=1, name="Your next guess!", value="What is your guess for the next number? Small, middle, or big?\nOr you can type \"end\" to end the game!", inline=False)
            await dice_ui_message.edit(embed=dice_ui)
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            guess_message = await bot.wait_for("message", check=check)
            guess = guess_message.content.lower()
            await guess_message.delete()
            dice_ui.remove_field(1)
            while guess != "small" and guess != "middle" and guess != "big" and guess != "end":
                dice_ui.remove_field(1)
                dice_ui.insert_field_at(index=1, name="Your next guess:", value="I don\"t get it. =/ Small, middle or big? Or type end to end the game!", inline=False)
                await dice_ui_message.edit(embed=dice_ui)
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                guess_message = await bot.wait_for("message", check=check)
                guess = guess_message.content.lower()
                await guess_message.delete()
            dice_ui.remove_field(1)
            number = random.choice(range(1, 7))+random.choice(range(1, 7))
            result = ""
            dice_ui.clear_fields()
            if guess == "small" and number <= 6:
                result = "You\"re right!"
                money += 50
            elif guess == "middle" and number == 7:
                result = "You\"re right!"
                money += 300
            elif guess == "big" and number >=8 :
                result = "You\"re right!"
                money += 50
            elif guess != "end":
                result = "Oh no! :/ It seems like you\"re wrong..."
                money -= 50
            if guess != "end":
                dice_ui.insert_field_at(index=0, name="Your money left:", value=f"${money}", inline=False)
                dice_ui.insert_field_at(index=1, name="Your guess:", value=guess, inline=False)
                await dice_ui_message.edit(embed=dice_ui)
                dice_ui.insert_field_at(index=2, name="THE SOOO IMPORTANT NUMBER:", value=number, inline=False)
                dice_ui.insert_field_at(index=3, name="THE LONG-AWAITED RESULT:", value=result, inline=False)
                dice_ui.set_footer(text="The number is produced by rolling two die together!")
            else:
                dice_ui.clear_fields()
                dice_ui.insert_field_at(index=1, name="You ended the game!", value=f"OK then :D\n You have ${money}.", inline=False)
                await dice_ui_message.edit(embed=dice_ui)
                break
            await dice_ui_message.edit(embed=dice_ui)
            time.sleep(5)
            dice_ui.clear_fields()
            dice_ui.set_footer(text="")
            await dice_ui_message.edit(embed=dice_ui)
        if money <= 10:
            await ctx.send(f"You lost! You have only ${money}...")


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

