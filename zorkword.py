#!/usr/bin/env python3
import json
from enum import Enum
from pathlib import Path
import random
import constants

NO_ENGRAVINGS = "There are no engravings."
"""Zorkword - A text-based command processor."""
class Board:

    def __init__(self, filename: str):
        with open(f"{filename}.json", "r") as file:
            board_json = json.load(file)
        
        self.constructors = board_json["constructors"]
        self.editor = board_json["editor"]
        self.cells = board_json["body"][0]["cells"]
        self.clues = board_json["body"][0]["clues"]
        self.width = board_json["body"][0]["dimensions"]["width"]
        self.height = board_json["body"][0]["dimensions"]["height"]

    def get_constructors(self) -> str:
        return f"Your soul has been bound to this accursed board by the fiendish wizard(s) {', '.join(self.constructors)}. They were set to the task by their malevolent master {self.editor}."

class Player:

    def __init__(self):
        self.position: int = None
        self.solutions: dict[str, str] = None
        self.board: Board = None
        self.mode = "MENU"
        self.command_switch = {
            "MENU": {
                "START": start_puzzle,
                "EXIT": exit,
                "LIST": list_puzzles,
                "LOAD": load,
                "MAN": show_commands,
                "HELP": show_commands,
            },
            "PUZZLE": {
                "LOOK": look,
                "READ": read_clue,
                "POSIT": answer_clue,
                "GO": go,
                "BLINK": blink,
                "SOLVE": solve,
                "CHECK": check,
                "EXIT": exit,
                "MAN": show_commands,
                "HELP": show_commands,
            }
        }
        puzzles_dir = Path(__file__).parent / "puzzles"
        self.json_files = [f.stem for f in puzzles_dir.glob("*.json")]


    def move_direction(self, direction: str):
        if direction == "EAST":
            if self.position % self.board.width == self.board.width - 1:
                return False
            else:
                self.position += 1
                return True
        elif direction == "WEST":
            if self.position % self.board.width == 0:
                return False
            else:
                self.position -= 1
                return True
        elif direction == "NORTH":
            if self.position < self.board.width:
                return False
            else:
                self.position -= self.board.width
                return True
        elif direction == "SOUTH":
            if self.position >= self.board.width * (self.board.height - 1):
                return False
            else:
                self.position += self.board.width
                return True
        return True

    def set_position(self, position: int):
        self.position = position

    def set_solutions(self, solutions: dict[str, str]):
        self.solutions = solutions

    def set_player_mode(self, mode: str):
        self.mode = mode

    def set_board(self, board: Board):
        self.board = board

    def get_player_answer_at_position(self) -> str:
        if 'player_answer' in self.board.cells[self.position]:
            return f"You see your own markings here. You have written the letter: \x1B[3m{self.board.cells[self.position]['player_answer']}\x1B[0m.\n   "
        else:
            return ""

    def get_letter_at_position(self, position: int) -> str:
        try: 
            return self.board.cells[position]['player_answer']
        except KeyError:
            return None

    def get_readable_position(self) -> str:
        try:
            return f"You see a label an ancient engraving: {self.board.cells[self.position]['label']}."
        except KeyError:
            return NO_ENGRAVINGS

    # Gets the clues regardless of position within the answer.
    def get_clues_at_position(self) -> list[str]:
        current_cell = self.board.cells[self.position]
        if 'clues' in current_cell:
            return (self.board.clues[current_cell["clues"][0]], self.board.clues[current_cell["clues"][1]])
        return None

    # Returns only the clues that the user can read from the current cell.
    def get_accessible_clues_at_position(self) -> list[str]:
        current_cell = self.board.cells[self.position]
        if not 'label' in current_cell:
            return None
        if 'clues' in current_cell:
            clues = (self.board.clues[current_cell["clues"][0]], self.board.clues[current_cell["clues"][1]])
            # Do not show any clues that do not start from this cell.
            if clues[0]['label'] != current_cell['label']:
                clues = (None, clues[1])
            if clues[1]['label'] != current_cell['label']:
                clues = (clues[0], None)
            return clues
        return None

    # Answer length fit is checked by the command.
    def answer_clue_by_index(self, index: int, answer: str) -> str:
        clue_to_answer = self.board.clues[index]
        if len(answer) != len(clue_to_answer['cells']):
            return f"The answer must be {len(clue_to_answer['cells'])} letters long."
        self.board.clues[index]['player_answer'] = answer
        for index, cell in enumerate(clue_to_answer['cells']):
            self.board.cells[cell]['player_answer'] = answer[index]
        return f"You answer the {clue_to_answer['label']} clue with {answer}."

def process_command(command: str, player: Player) -> str:
    """Process a user command and return a response."""
    if len(command) == 0:
        return
    command = command.upper()
    command_set = command.split(" ")
    command_action = command_set[0]
    if command_action not in constants.valid_commands[player.mode]:
        return handle_invalid_command(command_action)
    return player.command_switch[player.mode][command_action](player, args=command_set[1:])

# Puzzle commands
def look_here(player):
    return "You look for a marker on the board. "+ content_at_position(player)

def content_at_position(player):
    placestring = f"{player.get_readable_position()}\n"
    placestring += player.get_player_answer_at_position()
    clues = player.get_accessible_clues_at_position()
    if clues:
        if clues[0]:
            placestring += f"You see a sign that that says \x1B[3m{clues[0]['label']} {clues[0]['direction']}\x1B[0m.\n"
        if clues[1]:
            placestring += f"You see a sign that that says \x1B[3m{clues[1]['label']} {clues[1]['direction']}\x1B[0m.\n"
    if NO_ENGRAVINGS in placestring:
        placestring += "You hear the lonely howl of the wind."
    return placestring

def look(player: Player, args: list[str]):
    placestring = ""
    if len(args) == 0:
        return look_here(player)
    direction = args[0]
    if direction not in constants.valid_directions:
        return "I don't know how to LOOK %s." % direction
    placestring += f"You look to the {direction}. You see: "
    clues = player.get_clues_at_position()
    if direction == "EAST" or direction == "WEST":
        relevant_clue = clues[0]
    elif direction == "NORTH" or direction == "SOUTH":
        relevant_clue = clues[1]
    iterate_direction = 1
    if direction == "WEST" or direction == "NORTH":
        iterate_direction = -1
    start_position = relevant_clue['cells'].index(player.position)
    if iterate_direction == -1:
        index = start_position - 1
        while index >= 0:
            letter = player.get_letter_at_position(relevant_clue['cells'][index])
            if letter:
                placestring += f"\x1B[3m{letter}\x1B[0m "
            else:
                placestring += "_ "
            index -= 1
    if iterate_direction == 1:
        index = start_position + 1
        for position in relevant_clue['cells'][index::]:          
            letter = player.get_letter_at_position(relevant_clue['cells'][index])
            if letter:
                placestring += f"\x1B[3m{letter}\x1B[0m "
            else:
                placestring += "_ "

    return placestring

def read_clue(player, args: list[str]):
    if len(args) == 0:
        return "You must specify which clue to read."
    word = args[0]
    if word not in ["ACROSS", "DOWN"]:
        return "You may only read the ACROSS or DOWN clues."
    clues = player.get_accessible_clues_at_position()
    cluestr = "You perform a rite to probe the spirits. They taunt you:\n"
    if word == "ACROSS" and clues[0]:
        cluestr += f"\x1B[3m{len(clues[0]['cells'])} letters: {clues[0]['text'][0]['plain']}\x1B[0m"
    elif word == "DOWN" and clues[1]:
        cluestr += f"\x1B[3m{len(clues[1]['cells'])} letters: {clues[1]['text'][0]['plain']}\x1B[0m"
    elif word == "ACROSS" and not clues[0]:
        cluestr += "There is no sign that says ACROSS."
    elif word == "DOWN" and not clues[1]:
        cluestr += "You see no sign that says DOWN."
    return cluestr

def answer_clue(player, args: list[str]):
    if len(args) == 0:
        return "You must specify which clue to answer."
    clue_word = args[0]
    if clue_word not in ["ACROSS", "DOWN"]:
        return "You may only answer the ACROSS or DOWN clues."
    clues = player.get_accessible_clues_at_position()
    if clue_word == "ACROSS" and clues[0]:
        if not clues[0]:
            return "There is no sign that says ACROSS here, you cannot posit an answer in this direction."
        clue = clues[0]
    else:
        if not clues[1]:
            return "There is no sign that says DOWN here, you cannot posit an answer in this direction."
        clue = clues[1]
    if len(args) == 1:
        return "You must specify your answer."
    answer = args[1]
    answer_str = player.answer_clue_by_index(player.board.clues.index(clue), answer)
    return answer_str

def check(player: Player, args: list[str]):
    return player.board.get_constructors()

def go(player: Player, args: list[str]):
    if len(args) == 0:
        return "You need to specify a direction to go."
    direction = args[0]
    if direction not in constants.valid_directions:
        return "You need to specify a valid direction to go."
    can_move = player.move_direction(direction)
    if can_move:
        return f"You move {direction}. " + content_at_position(player)
    else:
        return "You cannot move in that direction. You are at an edge of the board."

def blink():
    return "You blink and see a tree."

def solve():
    return "You solve the puzzle."

def exit():
    return "Goodbye!"


# Menu Commands
def start_puzzle(player: Player, args: list[str]):
    if len(args) == 0 or not args[0].isdigit():
        return "Please specify a puzzle to start by index."
    puzzle_index = int(args[0])
    player.set_player_mode("PUZZLE")
    player.set_position(0)
    player.set_solutions({})
    player.set_board(Board(f"puzzles/{player.json_files[puzzle_index]}"))
    return "You start the game for puzzle %s." % player.json_files[puzzle_index]

def exit(player: Player, args: list[str]):
    return "Goodbye!"

def list_puzzles(player: Player, args: list[str]):
    if not player.json_files:
        return "No puzzles available."
    puzzle_list = [f"{i}. {name}" for i, name in enumerate(player.json_files)]
    return "Available puzzles:\n  " + "\n  ".join(puzzle_list)

def load(player: Player, args: list[str]):
    return "You load the puzzle."

# Shared commands
def show_commands(player: Player, args: list[str]):
    return """ You are in {mode} mode. Valid commands are:
    {commands}
    """.format(mode=player.mode, commands=constants.valid_commands[player.mode])

def handle_invalid_command(command: str) -> str:
    """Handle an invalid command and return a response."""
    return random.choice(constants.invalid_command_response) % command


def main():
    """Main loop that listens for and processes user input."""
    print("Welcome to Zorkword!")
    print("Type 'EXIT' to quit.\n")

    player_instance = Player()
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
