from email.message import Message
import os
import nextcord
import json 
from datetime import datetime
import time
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction, ButtonStyle, SlashOption
from nextcord.ui import Button, View

class Fun(commands.Cog, name="Fun"):

    COG_EMOJI = "🎡"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 

    @nextcord.slash_command(
        name = "dice", 
        description = "Roll a dice and make decisions!",
        guild_ids=[main.DEVS_SERVER_ID]
        ) 
    async def dice(
        self, 
        interaction: Interaction, 
        sides: int = SlashOption(
            name = "sides",
            description = "The sides of 1 die. Ranges from 2 to 40. Defaults as 6.",
            required = False,
            min_value = 2,
            max_value = 40,
            default = 6,
            verify = True
        ), 
        dice: int = SlashOption(
            name = "dice",
            description = "The number of dice. Ranges from 1 to 800. Defaults as 1.",
            required = False,
            min_value = 1,
            max_value = 800,
            default = 1,
            verify = True
        )
    ):
        result = [
                str(random.choice(range(1, sides + 1)))
                for _ in range(dice)
            ]
        embed = nextcord.Embed()
        embed.title = f"I rolled {dice} dice with {sides} sides and the result is:"
        if dice > 5:
            descr = "As there are more than 5 dice, I counted the results for you! 😊 ```css"
            for side in range(1, sides + 1):
                descr += f"\n* ({result.count(str(side))}) [{side}s]"
            descr += "```"
        else:
            descr = ", ".join(result)
        embed.description = descr
        embed.colour = random.choice(main.embed_colours)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="coinflip", description="Flip a coin!", guild_ids=[main.DEVS_SERVER_ID])
    async def coinflip(self, interaction: Interaction):
        embed = nextcord.Embed()
        embed.title = "Flippin' a coin..."
        embed.colour = random.choice(main.embed_colours)
        result = random.choice(range(2))
        if result == 0:
            embed.set_image(url="https://i.imgur.com/Mvy8BV8.gif")
        else:
            embed.set_image(url="https://i.imgur.com/mmjXem0.gif")
        await interaction.response.send_message(embed=embed)
        time.sleep(3.5)
        embed.title = "And the result is..."
        if result == 0:
            embed.description = "**`HEADS`**"
            embed.set_image(url="https://i.imgur.com/8BSllkX.png")
        else:
            embed.description = "**`TAIL`**"
            embed.set_image(url="https://i.imgur.com/VcqwLpT.png")
        await interaction.edit_original_message(embed=embed)

    @nextcord.slash_command(name="karson", description="Shows Karson in a big collage!", guild_ids=[main.DEVS_SERVER_ID])
    async def karson(self, interaction: Interaction):
        embed = nextcord.Embed()
        embed.set_image(url="https://i.ibb.co/vzRD2LC/big-collage.jpg")
        karson_user = await bot.fetch_user(708141816020729867)
        embed.set_author(name="MEET KARSON:", icon_url= karson_user.avatar)
        embed.colour = random.choice(main.embed_colours)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="8ball", description="Make decisions!", guild_ids=[main.DEVS_SERVER_ID])
    async def eight_ball(
        self, 
        interaction: Interaction, 
        whattodecide: str = SlashOption(
            name = "what-to-decide"
        )
    ):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ] 
        await interaction.response.send_message(f"You shook me and some words appeared...\n```md\n# {str(random.choices(responses)[0])}\n```")

    @commands.command(name="dicegame", brief="Play a simple dice game!")
    async def dicegame(self, ctx):
        money = 500
        author_avatar = ctx.author.avatar
        dice_ui = nextcord.Embed()
        dice_ui.colour = random.choice(main.embed_colours)
        dice_ui.set_author(name=f"{ctx.author.name}'s Dicegame", icon_url= author_avatar)
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

def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))