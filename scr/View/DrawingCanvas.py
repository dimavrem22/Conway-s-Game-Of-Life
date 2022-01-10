import tkinter
from Model.IGameOfLifeModel import IGameOfLifeModel
from Resources.GameUtils import GameUtils
from View.IDrawingCanvas import IDrawingCanvas
from View.IGameOfLifeView import IGameOfLifeView


class DrawingCanvas(IDrawingCanvas):
    """
    A class implementing the Drawing Canvas on which the cells of the game are displayed.

    Parameters
    ----------
    __model: the Game of Life model to be drawn
    __style: the coloring style which is used to display the cells
    __background_cells: list of dead cell shapes that cover the canvas
    __surface_cells: list of living cell shapes that are overlaying the background cells

    Methods
    -------
    __init__(master, width, height, model, style):
        creates an instance of the DrawingCanvas Object.
        takes the master, view object, width and height of canvas (in pixels), game model, and coloring style

    change_style(style):
        changes the coloring style of the cells to the specified style

    initialize_cells():
        sets the background of the canvas to be a grid of dead cells

    draw_game():
        draws living cells on top of the grid background
    """

    def __init__(self, master: IGameOfLifeView, width: int, height: int, model: IGameOfLifeModel, style):
        """
        Creates an instance of the DrawingCanvas class.
        :param master: view in which the canvas will be displayed
        :param width: the width of the canvas in pixels
        :param height: the height of the canvas in pixels
        :param model: the model from which the cells will be drawn
        :param style: the coloring style used in the display of the cells
        """
        super().__init__(master, height=height, width=width)
        self.__model = model
        self.__style = style
        self.__background_cells = []
        self.__surface_cells = []
        self.initialize_cells()

    def change_style(self, style):
        """
        changes the coloring style of the cells displayed
        :param style: the style which is drawn
        """
        self.__style = style
        for cell in self.__surface_cells:
            self.delete(cell)
        self.__surface_cells.clear()
        for cell in self.__background_cells:
            self.delete(cell)
        self.__background_cells.clear()
        self.initialize_cells()
        self.draw_game()

    def initialize_cells(self):
        """ Draws dead cells in the background to create a grid."""
        grid = self.__model.get_grid()
        outer_idx = 0
        while outer_idx < len(grid):
            inner_idx = 0
            while inner_idx < len(grid[outer_idx]):
                self.__add_cell(inner_idx, outer_idx, False)
                inner_idx += 1
            outer_idx += 1

    def draw_game(self):
        """ Draws the living cells above the dead cells."""
        self.__remove_surface()
        grid = self.__model.get_grid()
        outer_idx = 0
        while outer_idx < len(grid):
            inner_idx = 0
            while inner_idx < len(grid[outer_idx]):
                if grid[outer_idx][inner_idx]:
                    self.__add_cell(inner_idx, outer_idx, True)
                inner_idx += 1
            outer_idx += 1

    def __remove_surface(self):
        """ Clears all the living cells that are displayed on the canvas."""
        for cell in self.__surface_cells:
            self.delete(cell)
        self.__surface_cells.clear()

    def __add_cell(self, x: int, y: int, live: bool):
        """ Draws a cell in the canvas. """
        cell_length = GameUtils().cell_length
        padding = GameUtils().canvas_padding
        x0 = x * cell_length + padding
        x1 = x0 + cell_length
        y0 = y * cell_length + padding
        y1 = y0 + cell_length
        cell_color = self.__style['dead cell color']
        if live:
            cell_color = self.__style['alive cell color']
        cell = self.create_rectangle(x0, y0, x1, y1, fill=cell_color, outline=self.__style['grid color'])
        if not live:
            self.__background_cells.append(cell)
        else:
            self.__surface_cells.append(cell)
