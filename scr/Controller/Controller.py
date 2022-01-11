import sys
import tkinter
from tkinter import messagebox
from Controller.IController import IController
from Model.IGameOfLifeModel import IGameOfLifeModel
from Resources.GameUtils import GameUtils
from View.IGameOfLifeView import IGameOfLifeView
from View.GameOfLifeView import StructAddView
from View.GameOfLifeView import ManageStructureView


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

    __automatic__advance():
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

    __add_structure(struct_name):
        Adds the current model pattern to the structure library (resources.txt file)

    __empty_game():
        Determines if the model has at least one living cell. Returns True is there are no living cells.

    __delete_structures(structs):
        Deletes structures from library based on the specified names.

    __reset_structures():
        Repopulates the structure library with the backup default structures from the back_up_resources.txt file.


    """

    def __init__(self, model: IGameOfLifeModel, view: IGameOfLifeView,
                 file_path="Resources/resources.txt", bu_file_path="Resources/back_up_resources.txt"):
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
        self.__struct_adder = None
        self.__struct_manager = None
        self.__file_path = file_path
        self.__bu_file_path = bu_file_path

    def execute(self):
        """ Starts the Game of Life. Initiates the view to render the model. """
        self.__view.set_button_listener(self)
        self.__view.render()

    def action_performed(self, command: str, event = None):
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
            self.__view.change_style(event)
        elif command == 'generate':
            self.__generate_structure(event)
        elif command == 'add structure':
            if event is None:
                if self.__play is True:
                    self.__toggle_play()
                self.__struct_adder = StructAddView(self)
                self.__struct_adder.mainloop()
            else:
                self.__add_structure(event)
        elif command == 'manage structures':
            self.__struct_manager = ManageStructureView(self)
            self.__struct_manager.mainloop()
        elif command == 'delete':
            self.__delete_structures(event)
        elif command == 'default':
            self.__reset_structures()
        else:
            raise ValueError('Invalid Command')
        self.__view.update()

    def __automatic___advance(self):
        """ Automatically updates the state of the game after a certain amount of time passed."""
        if self.__play:
            self.__advance()
        else:
            return
        self.__view.after(self.__speed, self.__automatic___advance)

    def __exit_game(self):
        """ Method that terminates the game and the program. """
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
        if self.__play:
            self.__automatic___advance()
        else:
            self.__advance()
        self.__view.toggle_start_stop_button(self.__play)

    def __advance(self):
        """ Method which updates the model and redraws the view. Used to progress the game. """
        self.__model.update_state()
        self.__view.update()

    def __toggle_cell_clicked(self, event: tkinter.Event):
        """
        Toggles the state of a cell (dead/alive) of a particular cell that was clicked. 
        :param event: mouse click coordinates
        """
        if event is None:
            raise ValueError('Mouse Click Cannot Be Null')
        cell_length = GameUtils().cell_length
        padding = GameUtils().canvas_padding
        x = (event.x - padding) // cell_length
        y = (event.y - padding) // cell_length
        if x < 0 or y < 0 or x + 1 > self.__model.get_width() or y + 1 > self.__model.get_height():
            return
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
        living cells in the middle of the game board. Error messagebox is displayed if the structure does not fit.
        :param struct_name: name of the structure which will be spawned
        """
        if struct_name is None:
            raise ValueError('Structure Name Cannot Be Null')

        u = GameUtils(self.__file_path)
        dimensions = u.get_struct_dimensions(struct_name)

        if dimensions[0] > self.__model.get_width() or dimensions[1] > self.__model.get_height():
            messagebox.showerror(title='Error Generating Structure',
                                 message="Structure is too large for this game!")
            return
        self.__reset_game()
        coordinates = u.get_struct_coordinates(struct_name)
        x_offset = self.__model.get_width() // 2 - dimensions[0]//2
        y_offset = self.__model.get_height() // 2 - dimensions[1]//2

        for i in coordinates:
            self.__model.toggle_cell(i[0] + x_offset, i[1] + y_offset)
        self.__view.update()

    def __add_structure(self, struct_name: str):
        """
        Adds the current pattern of living cells into the library with the provided name. This allows the program
        user to generate the pattern at any desired moment in future game play. The pattern needs to have at
        least one living cell.
        :param struct_name: Had to be a non-empty string which is not found in the resources.txt file.
        """

        if struct_name == "" or struct_name is None:
            messagebox.showerror(title='Error Adding Structure', message="Structure needs a name!")
            return
        if self.__empty_game():
            messagebox.showerror(title='Error Adding Structure', message="No structure found!")
            return
        r = GameUtils(self.__file_path)

        if struct_name in r.get_key_list("structures"):
            messagebox.showerror(title='Error Adding Structure', message="Name already taken!")
            return

        grid = self.__model.get_grid()
        first_x = self.__model.get_width()
        first_y = self.__model.get_height()

        # getting x offset
        for i in grid:
            idx = 0
            for j in i:
                if j is True:
                    if idx < first_x:
                        first_x = min(first_x, idx)
                idx += 1

        # getting y offset
        idx = 0
        for i in grid:
            if True in i:
                first_y = idx
                break
            idx += 1

        raw_coordinates = []
        idx_x = 0
        idx_y = 0
        while idx_y < len(grid):
            while idx_x < len(grid[idx_y]):
                if grid[idx_y][idx_x]:
                    raw_coordinates.append((idx_x, idx_y))
                idx_x += 1
            idx_x = 0
            idx_y += 1

        result_coordinates = []
        for c in raw_coordinates:
            result_coordinates.append((c[0] - first_x, c[1] - first_y))

        r.add_structure(struct_name, result_coordinates)
        self.__struct_adder.destroy()
        self.__view.update_struct_options(self)
        messagebox.showinfo(title='Success', message="Structure Added.")

    def __empty_game(self) -> bool:
        """
        Determines if the game is empty.
        :return: True if the model does not have living cells. False is the model has at least one living cell.
        """
        result = True
        for i in self.__model.get_grid():
            result = result and (True not in i)
        return result

    def __delete_structures(self, structs: [str]):
        """
        Removes existing patterns from the library (resources.txt file) based on the provided list of names.
        :param structs: list of names of patters to remove from the library
        """
        if len(structs) == 0:
            messagebox.showerror(title='Error Deleting', message="Need to Select a Structure!")
            return
        r = GameUtils(self.__file_path)
        for s in structs:
            r.remove_structure(s)
        self.__struct_manager.destroy()
        self.__view.update_struct_options(self)
        message = 'The following structures were deleted: '
        for s in structs:
            message += s + ", "
        tkinter.messagebox.showinfo(title='Delete Structures', message=message[:-2])

    def __reset_structures(self):
        """ Restores the structures in the library with those from a backup file. """
        r = GameUtils(self.__file_path)
        r.reset_default(self.__bu_file_path)
        self.__struct_manager.destroy()
        self.__view.update_struct_options(self)
        tkinter.messagebox.showinfo(title='Default Structures', message='Structure Library was reset to Default')
