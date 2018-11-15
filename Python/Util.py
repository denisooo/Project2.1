class STATES:
    ROLLED_IN = 0
    ROLLED_OUT = 1
    ROLLING = 2


class COMMANDS:
    SEND_TEMP = 0
    SEND_LIGHT = 1
    CHANGE_MODE = 2
    SEND_MODE = 3
    SEND_STATE = 4
    ROLL_OUT = 5
    ROLL_IN = 6
    INC_TEMP = 7
    DEC_TEMP = 8
    INC_LIGHT = 9
    DEC_LIGHT = 10


class MODES:
    AUTO = 0
    MANUAL = 1


class COLORS:
    GRAY = 90
    RED = 31
    LIME = 92
    YELLOW = 93
    BLUE = 94
    PINK = 95
    CYAN = 96
    BLACK = 97
    DEFAULT = 00


class TextStyle:
    DEFAULT = 0
    UNDERLINE = 4
    HIGHLIGHT = 7


def color(text, _color=COLORS.DEFAULT, style=TextStyle.DEFAULT):
    return '\033[{0};{1}m{2}\033[0;m'.format(style, _color, text)


DEBUG = True  # Enable debug, Implement manually
