from Model.IGameOfLifeModel import IGameOfLifeModel


class MockModel(IGameOfLifeModel):
    """
    A class representing a Mock Model used for the testing of an interaction between game model and controller.

    Parameters
    ----------
    __call_log: a string representing all the functions called within the instance of the model.

    Methods
    -------
    get_call_log()
        Returns the log containing all the functions called within the object instance.
    """

    def __init__(self, width: int = 1, height: int = 1):
        self.__call_log = ''
        self.__width = width
        self.__height = height

    def update_state(self):
        self.__call_log += "update_state called;"
        return

    def get_width(self):
        self.__call_log += "get_width called;"
        return self.__width

    def get_height(self):
        self.__call_log += "get_height called;"
        return self.__height

    def get_grid(self):
        self.__call_log += "get_grid called;"
        grid = []
        for i in range(self.__width):
            row = []
            for j in range(self.__height):
                row.append(False)
            grid.append(row)
        return grid


    def toggle_cell(self, x: int, y: int):
        self.__call_log += "toggle_cell called (x:" + str(x) + ", y:" + str(y) + ");"
        return

    def get_call_log(self):
        return self.__call_log
