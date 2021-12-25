import abc
import tkinter
from Controller.IController import IController


class IGameOfLifeView(tkinter.Tk, abc.ABC):
    """
    An abstract class representing the Game of Life View.

    Methods:
    -------

    render():
        initiates the view to provide a display of the model

    get_model_hash():
        used in ensuring that the same model is passed into the controller and the view
        :return hash of the model object

    update():
        redraws the current state of the model into the view

    set_button_listener(controller):
        Binds the buttons in the view to the Controller within the game.
        Allows the controller to listen to commands from the program user.

    change_style(style):
        changes the coloring of the display to a specified style
    """

    @abc.abstractmethod
    def render(self):
        """
        Initiates the view to display the game.
        """
        pass

    @abc.abstractmethod
    def get_model_hash(self):
        """
        used to ensure that the same model object is passed into the view and the controller
        :return: hashcode of the Game of Life model
        """
        pass

    @abc.abstractmethod
    def update(self):
        """
        used to redraw the current state of the model within the view
        """
        pass

    @abc.abstractmethod
    def set_button_listener(self, controller: IController):
        """
        binds buttons within the view with the controller to allow the controller to receive commands form the user
        :param controller:  the controller which will be listening for input from the user of the program
        """
        pass

    @abc.abstractmethod
    def change_style(self, style):
        """
        changes the coloring style of the display of the game
        :param style: name of the style to which the view needs to change
        :return:
        """
        pass
