#!/usr/bin/env python3
import constants
import player
import shared_mode
"""Zorkword - A text-based command processor."""

def process_command(command: str, player: player.Player) -> str:
    """Process a user command and return a response."""
    if len(command) == 0:
        return
    command = command.upper()
    command_set = command.split(" ")
    command_action = command_set[0]
    if command_action not in constants.valid_commands[player.mode]:
        return shared_mode.handle_invalid_command(command_action)
    return player.command_switch[player.mode][command_action](player, args=command_set[1:])


def main():
    """Main loop that listens for and processes user input."""
    print("Welcome to Zorkword!")
    print("Type 'EXIT' to quit.\n")

    player_instance = player.Player()
    while True:
        try:
            user_input = input("> ").strip()

            if user_input.upper() == "EXIT":
                print("Goodbye!")
                break

            if not user_input:
                continue

            response = process_command(user_input, player_instance)
            print(response)

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
