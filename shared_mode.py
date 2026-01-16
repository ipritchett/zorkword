import constants 
import random

def show_commands(player, args: list[str]):
    return """ You are in {mode} mode. Valid commands are:
    {commands}
    """.format(mode=player.mode, commands=constants.valid_commands[player.mode])

def handle_invalid_command(command: str) -> str:
    """Handle an invalid command and return a response."""
    return random.choice(constants.invalid_command_response) % command