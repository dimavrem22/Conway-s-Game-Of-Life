from Model.IGameOfLifeModel import IGameOfLifeModel


class GameOfLifeModel(IGameOfLifeModel):
    """
    A class implementing the game of life Model.

    Parameters
    ----------
    __grid: array of array of booleans representing the game of life grid
    __width: width of the game grid (in cells)
    __height: height of the game grid (in cells)

    Methods
    -------
    __init__(width, height):
        Constructor which initializes the GameOfLifeModel Object with a specified grid width and height

    __generate_grid(width, height):
        creates an array of array of booleans representing the grid of the game
        with specified width and height

    toggle_cell(x, y):
        switches the status of the specified cell

    update_state():
        updates the state of the game based on the Game of Life Rules:
            1. If a dead cell has exactly 3 living cells around it, it becomes alive
            2. If a living cell has 4 or more living cells around it, it dies.
            3. If a living cell has less than 2 living cells around it, it dies.

    get_width():
        returns width of game grid

    get_height():
        returns height of the game grid

    get_grid():
        returns the list of list of booleans representing a copy of the game grid
    """

    def __init__(self, width: int, height: int):
        """
        Initializes the GameOfLifeModel Object
        :param width: width of the game grid
        :param height: height of the game grid
        """
        if width <= 0 or height <= 0:
            raise ValueError('Invalid Grid Parameters!')
        else:
            self.__grid = self.__generate_grid(width, height)
            self.__width = width
            self.__height = height

    @staticmethod
    def __generate_grid(width: int, height: int) -> [[bool]]:
        """
        Creates the game grid.
        :param width: width of the grid (in cells)
        :param height: height of the grid (in cells)
        :return: array of array of booleans representing the game grid
        """
        if width <= 0 or height <= 0 or width is None or height is None:
            raise ValueError('Invalid Grid Parameters!')
        else:
            grid = []
            for i in range(height):
                row = []
                for j in range(width):
                    row.append(False)
                grid.append(row)
            return grid

    def toggle_cell(self, x: int, y: int):
        """
        Switches the status of the specified cell. From living to dead or from dead to living.
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        """
        if x < 0 or y < 0 or x is None or y is None or y >= len(self.__grid) or x >= len(self.__grid[0]):
            raise ValueError('Invalid Cell Coordinates!')
        else:
            self.__grid[y][x] = not self.__grid[y][x]

    def __surrounding_live_cells(self, x: int, y: int) -> int:
        """
        :param x: x coordinate of the cell in the grid (column)
        :param y: y coordinate of the cell in the grid (row)
        :return: the number of living cells surrounding the cell with the coordinates (x,y)
        """
        if x < 0 or y < 0 or x is None or y is None or y >= len(self.__grid) or x >= len(self.__grid[0]):
            raise ValueError('Invalid Cell Coordinates!')
        else:
            startX = max(0, x - 1)
            endX = min(self.__width - 1, x + 1)
            startY = max(0, y - 1)
            endY = min(self.__height - 1, y + 1)
            result = 0
            while startY <= endY:
                sX = startX
                while sX <= endX:
                    if self.__grid[startY][sX]:
                        result += 1
                    sX += 1
                startY += 1
            if self.__grid[y][x]:
                return result - 1
            else:
                return result

    def update_state(self):
        """
        updates the state of the game based on the Game of Life Rules:
        1. If a dead cell has exactly 3 living cells around it, it becomes alive
        2. If a living cell has 4 or more living cells around it, it dies.
        3. If a living cell has less than 2 living cells around it, it dies.
        """
        toggle_list = []
        i = 0
        j = 0
        while i < self.__height:
            j = 0
            while j < self.__width:
                neighbors = self.__surrounding_live_cells(j, i)
                alive = self.__grid[i][j]
                if alive and (neighbors < 2 or neighbors > 3):
                    toggle_list.append((j, i))
                elif not alive and neighbors == 3:
                    toggle_list.append((j, i))
                j += 1
            i += 1
        for x in toggle_list:
            self.toggle_cell(x[0], x[1])

    def get_width(self) -> int:
        """
        :return: the width of the grid
        """
        return self.__width

    def get_height(self) -> int:
        """
        :return: the height of the grid
        """
        return self.__height

    def get_grid(self) -> [[bool]]:
        """
        does not allow for the mutation of the actual grid
        :return: copy of the array as a list of list of booleans
        """
        grid = []
        for i in range(self.__height):
            row = []
            for j in range(self.__width):
                row.append(self.__grid[i][j])
            grid.append(row)
        return grid
