import discord
from discord.ext import commands
from discord import app_commands
import random
import bisect
import os
from PIL import Image
from utils.help import create_embed
from utils.gameslogic import *

ABS_PATH = os.path.dirname(__file__)
DEFAULT_BET = 1

class InsufficientFundsException(Exception):
    pass

class Economy():
    def __init__(self):
        self.accounts = {}

    def get_entry(self, user_id):
         if user_id not in self.accounts:
            self.accounts[user_id] = [user_id, "default_user", 100]
         return self.accounts[user_id]

    def add_credits(self, user_id, credits):
        if user_id not in self.accounts:
            self.accounts[user_id] = [user_id, "default_user", 100]
        self.accounts[user_id][2] += credits

class Slots(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.economy = Economy()

    def check_bet(self, ctx: commands.Context, bet: int=DEFAULT_BET):
        bet = int(bet)
        if bet <= 0 or bet > 1000:
            raise commands.errors.BadArgument()
        current = self.economy.get_entry(ctx.author.id)[2]
        if bet > current:
            raise InsufficientFundsException(current, bet)

    @app_commands.command(name="slots", description="Slot machine")
    @app_commands.describe(bet="The amount to bet (1-1000)")
    async def slots(self, interaction: discord.Interaction, bet: int=1):
        await interaction.response.defer()
        ctx = await commands.Context.from_interaction(interaction)
        try:
            self.check_bet(ctx, bet=bet)
        except commands.errors.BadArgument:
            await interaction.followup.send("Invalid bet amount. Bet must be between 1 and 1000.")
            return
        except InsufficientFundsException as e:
            await interaction.followup.send(f"Insufficient funds. You have {e.args[0]} credits, but you bet {e.args[1]}.")
            return

        path = os.path.join(ABS_PATH, 'modules/')
        facade = Image.open(f'{path}slot-face.png').convert('RGBA')
        reel = Image.open(f'{path}slot-reel.png').convert('RGBA')

        rw, rh = reel.size
        item = 180
        items = rh//item

        s1 = random.randint(1, items-1)
        s2 = random.randint(1, items-1)
        s3 = random.randint(1, items-1)

        win_rate = 98/100

        if random.random() < win_rate:
            symbols_weights = [3.5, 7, 15, 25, 55] # 
            x = round(random.random()*100, 1)
            pos = bisect.bisect(symbols_weights, x)
            s1 = pos + (random.randint(1, (items/6)-1) * 6)
            s2 = pos + (random.randint(1, (items/6)-1) * 6)
            s3 = pos + (random.randint(1, (items/6)-1) * 6)
            # ensure no reel hits the last symbol
            s1 = s1 - 6 if s1 == items else s1
            s2 = s2 - 6 if s2 == items else s2
            s3 = s3 - 6 if s3 == items else s3

        images = []
        speed = 6
        for i in range(1, (item//speed)+1):
            bg = Image.new('RGBA', facade.size, color=(255,255,255))
            bg.paste(reel, (25 + rw*0, 100-(speed * i * s1)))
            bg.paste(reel, (25 + rw*1, 100-(speed * i * s2))) # dont ask me why this works, but it took me hours
            bg.paste(reel, (25 + rw*2, 100-(speed * i * s3)))
            bg.alpha_composite(facade)
            images.append(bg)

        fp = str(id(ctx.author.id))+'.gif'
        images[0].save(
            fp,
            save_all=True,
            append_images=images[1:], # append all images after first to first
            duration=50  # duration of each slide (ms)
        )

        # win logic
        result = ('lost', bet)
        self.economy.add_credits(ctx.author.id, bet*-1)       
        # (1+s1)%6 gets the symbol 0-5 inclusive
        if (1+s1)%6 == (1+s2)%6 == (1+s3)%6:
            symbol = (1+s1)%6
            reward = [4, 80, 40, 25, 10, 5][symbol] * bet
            result = ('won', reward)
            self.economy.add_credits(ctx.author.id, reward)

        embed = create_embed(
            title=(
                f'You {result[0]} {result[1]} credits'+
                ('.' if result[0] == 'lost' else '!') # happy or sad based on outcome
            ),
            description=(
                'You now have ' +
                f'**{self.economy.get_entry(ctx.author.id)[2]}** ' +
                'credits.'
            ),
            color=(
                discord.Color.red() if result[0] == "lost"
                else discord.Color.green()
            )
        )

        file = discord.File(fp, filename=fp)
        embed.set_image(url=f"attachment://{fp}") # none of this makes sense to me :)
        await interaction.followup.send(
            file=file,
            embed=embed
        )

    @app_commands.command(name="blackjack", description="Play blackjack")
    @app_commands.describe(bet="The amount to bet")
    async def blackjack(self, interaction: discord.Interaction, bet: int):
        await interaction.response.send_message("Blackjack game logic will be implemented here.")

    @app_commands.command(name="coinflip", description="Flip a coin")
    @app_commands.describe(prediction="Heads or tails", bet="The amount to bet")
    async def coinflip(self, interaction: discord.Interaction, prediction: str, bet: int):
        await interaction.response.send_message("Coinflip game logic will be implemented here.")

    @app_commands.command(name="connectfour", description="Play connect four")
    async def connectfour(self, interaction: discord.Interaction):
        await interaction.response.send_message("Connect Four game logic will be implemented here.")

    @app_commands.command(name="crash", description="Play crash")
    @app_commands.describe(bet="The amount to bet")
    async def crash(self, interaction: discord.Interaction, bet: int):
        await interaction.response.send_message("Crash game logic will be implemented here.")

    @app_commands.command(name="findthelady", description="Find the lady")
    @app_commands.describe(bet="The amount to bet")
    async def findthelady(self, interaction: discord.Interaction, bet: int):
        await interaction.response.send_message("Find the lady game logic will be implemented here.")

    @app_commands.command(name="gamble", description="Gamble")
    @app_commands.describe(bet="The amount to bet")
    async def gamble(self, interaction: discord.Interaction, bet: int):
        await interaction.response.send_message("Gamble game logic will be implemented here.")

    @app_commands.command(name="higherorlower", description="Play higher or lower")
    async def higherorlower(self, interaction: discord.Interaction):
        await interaction.response.send_message("Higher or lower game logic will be implemented here.")

    @app_commands.command(name="poker", description="Play poker")
    @app_commands.describe(ante="The ante", bonus="The bonus")
    async def poker(self, interaction: discord.Interaction, ante: int, bonus: int):
        await interaction.response.send_message("Poker game logic will be implemented here.")

    @app_commands.command(name="race", description="Participate in a race")
    @app_commands.describe(racer_type="The type of racer", prediction="The predicted winner", bet="The amount to bet")
    async def race(self, interaction: discord.Interaction, racer_type: str, prediction: str, bet: int):
        await interaction.response.send_message("Race game logic will be implemented here.")

    @app_commands.command(name="roll", description="Roll the dice")
    @app_commands.describe(dice_type="The type of dice", prediction="The predicted number", bet="The amount to bet")
    async def roll(self, interaction: discord.Interaction, dice_type: str, prediction: str, bet: int):
        await interaction.response.send_message("Roll game logic will be implemented here.")

    @app_commands.command(name="roulette", description="Play roulette")
    @app_commands.describe(prediction="The predicted number", bet="The amount to bet")
    async def roulette(self, interaction: discord.Interaction, prediction: str, bet: int):
        await interaction.response.send_message("Roulette game logic will be implemented here.")

    @app_commands.command(name="rockpaperscissors", description="Play rock paper scissors")
    @app_commands.describe(selection="Rock, paper, or scissors", bet="The amount to bet")
    async def rockpaperscissors(self, interaction: discord.Interaction, selection: str, bet: int):
        await interaction.response.send_message("Rock paper scissors game logic will be implemented here.")

    @app_commands.command(name="sevens", description="Play sevens")
    @app_commands.describe(prediction="The predicted number", bet="The amount to bet")
    async def sevens(self, interaction: discord.Interaction, prediction: str, bet: int):
        await interaction.response.send_message("Sevens game logic will be implemented here.")

    @app_commands.command(name="tictactoe", description="Play tic tac toe")
    async def tictactoe(self, interaction: discord.Interaction):
        await interaction.response.send_message("Tic tac toe game logic will be implemented here.")

async def setup(client: commands.Bot):
    await client.add_cog(Slots(client))
