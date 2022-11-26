import discord
from discord.ext import commands

class CardDeck(discord.ui.Select):
    def __init__(self, role_name):
        self.role_name = role_name
        self.results = []
        efforts = [0, 1, 2, 3, 5, 8, 13, 20, 40, 100]
        
        options = [
            # Start with end voting option
            discord.SelectOption(label='Show Results', description='Ends the picking session', emoji='🛑'),
        ]
        for effort in efforts:
            options.append(discord.SelectOption(label=f'{effort}', description=f'{effort} effort', emoji='🃏'))
        
        super().__init__(placeholder='Pick your card...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        voter = interaction.user

        if self.role_name in [role.name for role in voter.roles]:
            # Check if 'End Voting' was selected
            if self.values[0] == 'Show Results':
                # End voting
                result_text = 'Here is the results!\n'
                for result in self.results:
                    result_text += f'{result[0]}:\t{result[1]}\n'
                # Add min and max estimates to the results
                result_text += f'\nLowest estimate\t{min(self.results, key=lambda x: x[1])[1]} '
                result_text += f'from {min(self.results, key=lambda x: x[1])[0]}\n'
                result_text += f'Highest estimate:\t{max(self.results, key=lambda x: x[1])[1]} '
                result_text += f'from {max(self.results, key=lambda x: x[1])[0]}'

                await interaction.response.send_message(f'```{result_text}```')
                
            # If voter is not in the result names
            elif voter.name not in [result[0] for result in self.results]:
                # Add voter and vote to dictionary
                self.results.append((voter.name, int(self.values[0])))

                await interaction.response.send_message(f'{voter.name} picked a card!')
            else:
                # Warn voter that they have already voted
                await interaction.response.send_message(f'{voter.name} has already picked!')
        else:
            await interaction.response.send_message(f'{voter.name} cannot pick a card!')

class CardDeckView(discord.ui.View):
    def __init__(self, role_name):
        super().__init__()

        self.add_item(CardDeck(role_name))


class Plop(commands.Bot):
    def __init__(self, command_prefix, role_name):
        self.role_name = role_name
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or(command_prefix), intents=intents)
        self.add_commands()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    def add_commands(self):
        @self.command(name='cards', pass_context=True)
        async def card(ctx):
            """Sends a dropdown containing card options."""
            view = CardDeckView(self.role_name)
            await ctx.send('Estimate the effort:', view=view)
