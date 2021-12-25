import abc
import tkinter


class IController(abc.ABC):
    """
    An abstract class to represent a controller for the Game of Life.

    Methods
    -------
    execute():
        starts the game

    action_performed(command, event):
        performs a particular action on the view and/or the model based on the command.
        Some commands may have associated events such as the coordinates of a mouse click.
    """

    @abc.abstractmethod
    def execute(self):
        """
        Method which initiates the game of life with the use of the view and model.
        """
        pass

    @abc.abstractmethod
    def action_performed(self, command: str,  event: tkinter.Event = None):
        """
        Performs a particular action in response to a command which is fed into the controller.
        :param command: the command which specifies the exact action that needs to be performed
        :param event: additional information that may be associated with a specific command
            (e.g. coordinates of a mouse click)
        """
        pass
