from board import Board

# Menu Commands
def start_puzzle(player, args: list[str]):
    if len(args) == 0 or not args[0].isdigit():
        return "Please specify a puzzle to start by index."
    puzzle_index = int(args[0])
    player.set_player_mode("PUZZLE")
    player.set_position(0)
    player.set_solutions({})
    player.set_board(Board(f"puzzles/{player.json_files[puzzle_index]}"))
    return "You start the game for puzzle %s." % player.json_files[puzzle_index]

def exit(player, args: list[str]):
    return "Goodbye!"

def list_puzzles(player, args: list[str]):
    if not player.json_files:
        return "No puzzles available."
    puzzle_list = [f"{i}. {name}" for i, name in enumerate(player.json_files)]
    return "Available puzzles:\n  " + "\n  ".join(puzzle_list)

def load(player, args: list[str]):
    return "You load the puzzle."