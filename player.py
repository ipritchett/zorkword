from board import Board
import menu_mode
import puzzle_mode 
import shared_mode
from pathlib import Path

class Player:

    def __init__(self):
        self.position: int = None
        self.solutions: dict[str, str] = None
        self.board: Board = None
        self.mode = "MENU"
        self.command_switch = {
            "MENU": {
                "START": menu_mode.start_puzzle,
                "EXIT": menu_mode.exit,
                "LIST": menu_mode.list_puzzles,
                "LOAD": menu_mode.load,
                "MAN": shared_mode.show_commands,
                "HELP": shared_mode.show_commands,
            },
            "PUZZLE": {
                "LOOK": puzzle_mode.look,
                "READ": puzzle_mode.read_clue,
                "POSIT": puzzle_mode.answer_clue,
                "GO": puzzle_mode.go,
                "BLINK": puzzle_mode.blink,
                "SOLVE": puzzle_mode.solve,
                "CHECK": puzzle_mode.check,
                "EXIT": puzzle_mode.exit,
                "MAN": shared_mode.show_commands,
                "HELP": shared_mode.show_commands,
            }
        }
        puzzles_dir = Path(__file__).parent / "puzzles"
        self.json_files = [f.stem for f in puzzles_dir.glob("*.json")]


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
            return contsants.NO_ENGRAVINGS

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
