from Controller.IController import IController
from Model.IGameOfLifeModel import IGameOfLifeModel
from View.GameOfLifeView import GameOfLifeView



class MockView(GameOfLifeView):
    """
    A class representing a Mock View used to test the interaction between game view and controller
    """

    def __init__(self, m: IGameOfLifeModel):
        super().__init__(m)
        self.__call_log = ""

    def render(self):
        self.__call_log += "render called; "

    def get_model_hash(self):
        self.__call_log += "get_model_hash called; "
        return super().get_model_hash()

    def update(self):
        self.__call_log += "update called; "

    def set_button_listener(self, controller: IController):
        self.__call_log += "set_button_listener called; "

    def change_style(self, style):
        self.__call_log += "change_style called: " + style + "; "

    def update_struct_options(self, controller: IController):
        self.__call_log += "update_struct_options called; "

    def get_call_log(self):
        return self.__call_log
