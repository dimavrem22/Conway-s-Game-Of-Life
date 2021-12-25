import sys
import tkinter
from Controller.IController import IController
from Model.IGameOfLifeModel import IGameOfLifeModel
from Resources.GameResources import GameResources
from View.IGameOfLifeView import IGameOfLifeView


class Controller(IController):
    """
    A class representing a controller implementation for the Game of Life.

    Parameters
    ----------
    __view : the view of the game of life
    __model: the model for the game of life
    __speed: the delay in milliseconds between consecutive state updates of the game when it is played
    __play: boolean that determines if the game is currently being played (true) or if the game is
            paused (false)

    Methods
    -------
    __init__(model, view):
        creates a Controller object with a specific game view and a game model

    execute():
        initiates the view to render the model

    action_performed(command, event):
        Method that performs a specific action called by the user of the program (command).
        Some commands may have associated events such as the coordinates of a mouse click.

    __automatic___advance():
        starts an automatic progression of the game of life.
        sets __play to True.
        Updates the model and redraws automatically.

    __exit():
        terminates the game and the program.

    __toggle_play():
        Used to start/stop the automatic progression of the game.

    __advance():
        Used to update the model and view by a single state progression.

    __toggle_cell_clicked(event):
        Toggles the state of the clicked cell.
        event: Coordinates of the mouse click

    __reset_game():
        Clears all living cells from the model and from the view

    __generate_structure(struct_name):
        Clears all living cells and spawns a specified structure in the center of the game board.
    """

    def __init__(self, model: IGameOfLifeModel, view: IGameOfLifeView):
        """
        Initializes the Controller Object
        :param model: the game of life model (must be the same object passed into the view)
        :param view: the game of life view 
        """
        if model is None or view is None:
            raise ValueError("Params Cannot Be Null")

        if model.__hash__() != view.get_model_hash():
            raise ValueError("Model not linked to View")
        self.__view = view
        self.__model = model
        self.__speed = 500
        self.__play = False

    def execute(self):
        """
        Starts the Game of Life. Initiates the view to render the model. 
        """
        self.__view.set_button_listener(self)
        self.__view.render()

    def action_performed(self, command: str, event: tkinter.Event = None):
        """
        Method that performs a specific action called by the user of the program. 
        :param command: specific command that needs to be carries out
        :param event: additional information from the view (e.g. coordinates of a mouse click) 
        """
        if command == 'toggle play':
            self.__toggle_play()
        elif command == 'exit':
            self.__exit_game()
        elif command == 'next':
            self.__advance()
        elif command == 'toggle cell':
            self.__toggle_cell_clicked(event)
        elif command == 'reset':
            self.__reset_game()
        elif command == 'set speed':
            self.__speed = event
        elif command == 'change view mode':
            print(self.__speed)
            self.__view.change_style(event)
        elif command == 'generate':
            self.__generate_structure(event)
        else:
            raise ValueError('Invalid Command')
        self.__view.update()

    def __automatic___advance(self):
        if self.__play:
            self.__advance()
        else:
            return
        self.__view.after(self.__speed, self.__automatic___advance)

    def __exit_game(self):
        """
        Method that terminates the game and the program. 
        """
        if self.__play:
            self.__toggle_play()
        self.__automatic___advance()
        sys.exit("Program Ended")

    def __toggle_play(self):
        """
        Switches the __play parameter. If __play becomes True, __automatic___advance is called to start the 
        automatic progression of the game.
        """
        self.__play = not self.__play
        self.__view.toggle_start_stop_button(self.__play)
        if self.__play:
            self.__automatic___advance()
        else:
            self.__advance()

    def __advance(self):
        """
        Method which updates the model and redraws the view. Used to progress the game. 
        """
        self.__model.update_state()
        self.__view.update()

    def __toggle_cell_clicked(self, event: tkinter.Event):
        """
        Toggles the state of a cell (dead/alive) of a particular cell that was clicked. 
        :param event: mouse click coordinates
        """
        if event is None:
            raise ValueError('Mouse Click Cannot Be Null')
        cell_length = GameResources().cell_length
        x = (event.x - 5) // cell_length
        y = (event.y - 5) // cell_length
        self.__model.toggle_cell(x, y)
        self.__view.update()

    def __reset_game(self):
        """
        Calls for the model and for the view to clear all living cells. 
        If the game is automatically progressing, stops the automatic progression. 
        """
        if self.__play:
            self.__toggle_play()
        grid = self.__model.get_grid()
        outer_idx = 0
        inner_idx = 0
        while outer_idx < self.__model.get_height():
            while inner_idx < self.__model.get_width():
                if grid[outer_idx][inner_idx]:
                    self.__model.toggle_cell(inner_idx, outer_idx)
                inner_idx += 1
            outer_idx += 1
            inner_idx = 0

    def __generate_structure(self, struct_name: str):
        """
        Method that clears all living cells from the game and places a specified structure of
        living cells in the middle of the game board.
        :param struct_name: name of the structure which will be spawned
        """
        if struct_name is None:
            raise ValueError('Structure Name Cannot Be Null')

        self.__reset_game()
        structure = GameResources.structures[struct_name]

        x_offset = self.__model.get_width() // 2 - structure['width']//2
        y_offset = self.__model.get_height() // 2 - structure['height']//2

        for i in structure['code']:
            self.__model.toggle_cell(i[0] + x_offset, i[1] + y_offset)
        self.__view.update()
