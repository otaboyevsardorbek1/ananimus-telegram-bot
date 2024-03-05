from dataclasses import dataclass

@dataclass
class BotConfig:
    """Configuration for a bot."""
    token: str = ''  # The token for authenticating the bot.
