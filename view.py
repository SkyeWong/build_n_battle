from nextcord.ui import Button, View
import nextcord
from typing import Optional
import random
from cogs import build_and_battle as bnb
class EndInteraction(View):
    @nextcord.ui.button(label = "End Interaction", style = nextcord.ButtonStyle.red, emoji = "⏹️")
    async def button_callback(self, button, interaction):
        button.label = "Interaction ended"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Interaction ended.")

class generate(View):

    def __init__(self, ctx):
        super().__init__(timeout=30)
        #self.ctx = ctx
    
    @nextcord.ui.button(label = "Test", emoji="😀")
    async def whatever(self, button, interaction):
        button.label = "Absolutely test"
        button.emoji = "😁"
        await interaction.response.edit_message(view=self)

    # @nextcord.ui.button(label = "Generate gold!", style = nextcord.ButtonStyle.grey, emoji = "🪙")
    # async def gold_generate(self, button, interaction):
    #     profile = list(bnb.get_user_profile(self.ctx.author))
    #     profile[1] += 500
    #     profile = bnb.update_user_profile(self.ctx.author, profile)
    #     button.label = "Gold optained!"
    #     button.disabled = True
    #     await interaction.response.edit_message(view=self)
    #     await interaction.followup.send("Something appears in front of you. You pick it up and be **really** suprised that it's some gold COINS!", ephemeral=True)

    # @nextcord.ui.button(label = "Generate XP!", style = nextcord.ButtonStyle.grey, emoji = "📚")
    # async def xp_generate(self, button, interaction):
    #     profile = list(bnb.get_user_profile(self.ctx.author))
    #     profile[2] += random.choice(range(6))
    #     profile = bnb.update_user_profile(self.ctx.author, profile)
    #     button.label = "No more books..."
    #     button.disabled = True
    #     await interaction.response.edit_message(view=self)
    #     await interaction.followup.send("You take your time and read a book, and learnt something new!", ephemeral=True)