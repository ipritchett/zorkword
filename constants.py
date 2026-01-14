valid_commands = { "MENU": ["START", "EXIT", "LIST", "LOAD", "MAN", "HELP"],
"PUZZLE":  ["LOOK", "GO", "BLINK", "SOLVE", "CHECK", "EXIT", "SAVE", "MAN", "HELP", "READ", "POSIT"]}

valid_directions = ["NORTH", "SOUTH", "EAST", "WEST"]

invalid_command_response = [
    "I don't know how to %s.",
    "%s doesn't sound right to me.",
    "%s? Are you sure?",
    "I'm not sure what %s means.",
    "If you want to %s, I can't help you."
]