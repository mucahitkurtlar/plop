from plop import Plop
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    role_name = os.environ.get('ROLE_NAME')
    command_prefix = os.environ.get('COMMAND_PREFIX')
    token = os.environ.get('DISCORD_TOKEN')

    bot = Plop(command_prefix, role_name)
    bot.run(token)