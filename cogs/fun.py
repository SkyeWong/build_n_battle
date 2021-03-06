import os
import nextcord
import json 
from datetime import datetime
import time 
import texttable
import random
import asyncio
import main
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction, SlashOption
from nextcord.ui import Button, View, Modal, TextInput
from views.fun_views import Analysis, HitAndBlowView, HitAndBlowData, HappyBirthdayView
from functions.users import Users
class Fun(commands.Cog, name="Fun"):

    COG_EMOJI = "🎡"

    def __init__(self):
        self._last_member = None 

    async def cog_application_command_before_invoke(self, interaction: Interaction):
        users = Users(interaction.user)
        if users.if_user_present() == False:
            users.create_user_profile()

    @nextcord.slash_command(
        name = "dice", 
        description = "Roll a dice and make decisions!"
        ) 
    async def dice(
        self, 
        interaction: Interaction, 
        sides: int = SlashOption(
            name = "sides",
            description = "The sides of 1 die. Ranges from 2 to 50. Defaults as 6.",
            required = False,
            min_value = 2,
            max_value = 50,
            default = 6,
            verify = True
        ), 
        dice: int = SlashOption(
            name = "dice",
            description = "The number of dice. Ranges from 1 to 5000. Defaults as 1.",
            required = False,
            min_value = 1,
            max_value = 5000,
            default = 1,
            verify = True
        )
    ):
        result = [
                str(random.choice(range(1, sides + 1)))
                for _ in range(dice)
            ]
        embed = Embed()
        embed.title = f"I rolled {dice} dice with {sides} sides and the result is:"
        embed.colour = random.choice(main.embed_colours)
        if dice > 5:
            most = [0]
            least = [1]
            descr = "As there are more than 5 dice, I counted the results for you-"
            descr += "\n```css"
            for side in range(1, sides + 1):
                count = result.count(str(side))
                descr += f"\n* ({count}) [{side}s]"
                if count > result.count(str(most[0])):
                    most = [side]
                elif count == result.count(str(most[0])):
                    most.append(side)
                if count < result.count(str(least[0])):
                    least = [side]
                elif count == result.count(str(least[0])):
                    least.append(side)
            descr += "\n```"
            embed.description = descr
            view = Analysis(interaction, result, most, least)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            descr = ", ".join(result)
            embed.description = descr
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="coinflip", description="Flip a coin!")
    async def coinflip(self, interaction: Interaction):
        embed = Embed()
        embed.title = "Flippin' a coin..."
        embed.colour = random.choice(main.embed_colours)
        result = random.choice(range(2))
        if result == 0:
            embed.set_image(url="https://i.imgur.com/lr3DjHO.gif")
        else:
            embed.set_image(url="https://i.imgur.com/An6Vm2C.gif")
        await interaction.response.send_message(embed=embed)
        embed.title = "And the result is..."
        if result == 0:
            embed.description = "**`HEADS`**"
            embed.set_image(url="https://i.imgur.com/8BSllkX.png")
            await asyncio.sleep(2)
        else:
            embed.description = "**`TAIL`**"
            embed.set_image(url="https://i.imgur.com/VcqwLpT.png")
            await asyncio.sleep(3)
        await interaction.edit_original_message(embed=embed)

    @nextcord.slash_command(name="karson", description="Shows Karson in a big collage!")
    async def karson(self, interaction: Interaction):
        embed = Embed()
        embed.set_image(url="https://i.ibb.co/vzRD2LC/big-collage.jpg")
        karson_user = await interaction.client.fetch_user(708141816020729867)
        embed.set_author(name="MEET KARSON:", icon_url= karson_user.avatar)
        embed.colour = random.choice(main.embed_colours)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="8ball", description="I can tell you the future... make decisions! 🎱")
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

    @nextcord.slash_command(name="hit-and-blow", description="Play a fun hit & blow game!", guild_ids=[main.DEVS_SERVER_ID])
    async def hit_and_blow(
        self, 
        interaction: Interaction, 
        bet_str: str = SlashOption(
            name = "bet",
            description = "Well, play big or go home. 🏠 MAX 80k MIN 5k",
            required = False,
            default = None
        )
    ):
        bet_msg = ""
        valid = False
        bet = 0
        if bet_str != None:
            bet = main.text_to_num(bet_str)
            if bet != False:
                users = Users(interaction.user)
                if bet > users.modify_gold(0):
                    await interaction.response.send_message("You didn't actually have THAT much to lose, do you?", ephemeral=True)
                elif bet > 80000:
                    await interaction.response.send_message("The max gamble amount is 80k, sorry.")
                elif bet < 5000:
                    await interaction.response.send_message("Bet at least 5k, wait do you even have 5k???")
                else:
                    valid = True
                    bet_msg = f" ● betting {bet_str}"
            else:
                await interaction.response.send_message(f"what do you mean by _`{bet_str}`_??? come on gimme a valid value", ephemeral=True)
        else:
            valid = True
        if valid:
            embed = Embed()
            embed.set_author(name=f"{interaction.user.name}'s Hit & Blow Game", icon_url=interaction.user.display_avatar.url)
            embed.description = f"Click the button to guess a number・`H` for **`HITS`** & `B` for **`BLOWS`**"
            embed.colour = random.choice(main.embed_colours)
            embed.set_footer(text=f"0 guesses {bet_msg}")
            view = HitAndBlowView(interaction, HitAndBlowData(), bet)
            await interaction.response.send_message(embed=embed, view=view)
    
    @nextcord.slash_command(name="happy-birthday-hoho", description="Happy Birthday! 🎉 Use this on 25/5", guild_ids=[main.DEVS_SERVER_ID])
    async def happy_birthday_hoho(self, interaction: Interaction):
        questions = [
            {
                "question": "How many passengers ride the MTR each day?",
                "answers": {
                    "1.38m": False,
                    "2.46m": True,
                    "6.9m": False,
                    "4.2m": False,
                    "3.24m": False,
                }
            },
            {
                "question": "What year was the TKO line opened?",
                "answers": {
                    "2000": False,
                    "1995": False,
                    "2005": False,
                    "2002": True,
                    "2008": False,
                }
            },
            {
                "question": "What year was the London underground (i prefer 'tube') opened?",
                "answers": {
                    "1863": True,
                    "1879": False,
                    "1854": False,
                    "1865": False,
                    "1848": False,
                }
            },
            {
                "question": "True or False. All tube stations are underground. easy one dude.",
                "answers": {
                    "True": False,
                    "False": True
                }
            },
            {
                "question": "Choose the right combination. Which tube line is fastest and how fast exactly is it?",
                "answers": {
                    "DLR Line, 77 kmh": False,
                    "Circle Line, 108 kmh": False,
                    "Bakerloo Line, 68 kmh": False,
                    "Metropolitan Line, 96 kmh": True,
                }
            },
            {
                "question": "Which of the following stations are ACTUALLY real tube station names? (i suppose u know the number of correct answers?)",
                "answers": {
                    "Swiss Cottage": True,
                    "Grand Central Terminal": False,
                    "Chicago Union Station": False,
                    "King's Cross": True,
                    "Ogilvie Transportation Center": False,
                    "Aldgate": True,
                    "South Station": False,
                    "Abbey Wood": True,
                    "Woolwich": True,
                    "Montreal Central Station": False,
                    "Platform 9 ¾": False
                }
            },
            {
                "question": "What is Hoho's favourite number? tip: the more the merrier!",
                "answers": {
                    "7": False,
                    "6942": True,
                    "420": False,
                    "69": False,
                }
            },
            {
                "question": "What is Hoho's favourite number? tip: the more the merrier!",
                "answers": {
                    "7": False,
                    "6942": True,
                    "420": False,
                    "69": False,
                }
            },
        ]
        view = HappyBirthdayView(interaction, questions)
        embed = view.get_question_embed()
        await interaction.send(embed=embed, view=view)

def setup(bot: commands.Bot):
    bot.add_cog(Fun())
