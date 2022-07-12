from main.commands.basecog import BaseCog


class Utils(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        # Initialise the docker container for translation.
