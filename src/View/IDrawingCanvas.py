import abc
import tkinter


class IDrawingCanvas(tkinter.Canvas, abc.ABC):
    """
    An abstract class used to represent the canvas which will be displaying the grid of the Game of Life.

    Methods
    -------
    change_style(style):
        changes the coloring style of the cells to the specified style

    initialize_cells():
        sets the background of the canvas to be a grid of dead cells

    draw_game():
        draws living cells on top of the grid background
    """

    @abc.abstractmethod
    def change_style(self, style):
        """
        changes the coloring style of the cells to the specified style
        :param style: the coloring style which will be used to draw the cells
        """
        pass

    @abc.abstractmethod
    def initialize_cells(self):
        """sets the background of the canvas to be a grid of dead cells"""
        pass

    @abc.abstractmethod
    def draw_game(self):
        """ draws living cells on top of the grid background """
        pass
