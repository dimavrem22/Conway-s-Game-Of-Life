import sys
from Controller.Controller import Controller
from Model.GameOfLifeModel import GameOfLifeModel
from View.GameOfLifeView import GameOfLifeView


def main():
    """
    Main method through which the Game of Life is initiated.
    Command line arguments can contain the desired height and width of the game (in cells).
    In the absence of commandline arguments, width and height are set to default values of 30 and 50 cells.
    """
    args = sys.argv
    game_height = extract_argument(args, '--height')
    game_width = extract_argument(args, '--width')

    # setting default values for game height and width in case they are not provided
    if game_width is None:
        game_width = 50
    if game_height is None:
        game_height = 30

    # initiating the game
    m = GameOfLifeModel(game_width, game_height)
    v = GameOfLifeView(m)
    c = Controller(m, v)
    c.execute()


def extract_argument(args: [str], key: str):
    """
    searches through a list of arguments and identifies the value of a parameter with the provided key
    :param args: list of string arguments through which to parse
    :param key: the string which indicates the parameter that needs to be identified
    :return: the value of the parameter if present; None if parameter is not present
    """
    i = 0
    while i < len(args) - 1:
        if args[i] == key:
            return int(args[i + 1])
        else:
            i += 1
    return None


if __name__ == '__main__':
    main()
