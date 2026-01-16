import json

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
