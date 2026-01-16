import constants

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
    if constants.NO_ENGRAVINGS in placestring:
        placestring += "You hear the lonely howl of the wind."
    return placestring

def look_direction(player, direction: str):
    placestring = ""
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
            letter = player.get_letter_at_position(position)
            if letter:
                placestring += f"\x1B[3m{letter}\x1B[0m "
            else:
                placestring += "_ "
    return placestring

def look(player, args: list[str]):
    placestring = ""
    if len(args) == 0:
        return look_here(player)
    direction = args[0]
    if direction not in constants.valid_directions:
        return "I don't know how to LOOK %s." % direction
    placestring += f"You look to the {direction}. You see: "
    placestring += look_direction(player, direction)
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

def check(player, args: list[str]):
    return player.board.get_constructors()

def go(player, args: list[str]):
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
