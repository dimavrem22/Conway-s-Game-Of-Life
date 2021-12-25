import abc


class IGameOfLifeModel(abc.ABC):
    """
    An abstract class representing the Model of Conway's Game of Life.

    Methods
    -------
    update_state():
        updates the game model to the next iteration of the game.
        Living cells that are surrounded by <2 or >3 living cells die.
        Dead cells that are surrounded by exactly 3 living cells are born.

    get_width():
        returns the width of the game grid

    get_height():
        returns the height of the game grid

    get_grid():
        returns a copy of the game grid

    toggle_cell(x, y):
        changes the cells with the coordinates, x and y, from dead to alive or from alive to dead

    """

    @abc.abstractmethod
    def update_state(self):
        """
        updates the game model to the next iteration of the game.
        Living cells that are surrounded by <2 or >3 living cells die.
        Dead cells that are surrounded by exactly 3 living cells are born.
        """
        pass

    @abc.abstractmethod
    def get_width(self) -> int:
        """
        :return: the width of the game grid
        """
        pass

    @abc.abstractmethod
    def get_height(self) -> int:
        """
        :return: the height of the game grid
        """
        pass

    @abc.abstractmethod
    def get_grid(self) -> [[bool]]:
        """
        :return: a copy of the grid
        """
        pass

    @abc.abstractmethod
    def toggle_cell(self, x: int, y: int):
        """
        switches the state of the cell with the specified coordinates
        :param x: x coordinate of cell to toggle
        :param y: y coordinate of cell to toggle
        """
        pass
