from Controller.IController import IController
from Resources.GameResources import GameResources
from View.IGameOfLifeView import IGameOfLifeView
from Model.IGameOfLifeModel import IGameOfLifeModel
import tkinter
from View.DrawingCanvas import DrawingCanvas


class GameOfLifeView(IGameOfLifeView):
    """
    A class implementation the Game of Life View. 
    
    Parameters
    ----------
    __model: the game of life model which the view will be rendering
    __height: height of the window in which the game will be displayed
    __width: width of the window in which the game will be displayed
    __canvas: where the cell of the game are displayed
    __button_frame: widget which will house the buttons within the view
    __button_next: button which the user can press to update the state of the game
    __button_start: button that starts and stops the automatic progression of the game
    __button_exit: button that exits and terminates the game
    __button_reset: button that is used to reset the game; clean grid
    __speed_slider: scale used to control the speed at which the game automatically advances
    __view_mode_frame: frame which houses the options to change the coloring style of the grid
    __generate_structure_frame: frame which houses the options to populate the grid with a specific pattern

    Methods
    -------
    __init__(model):
        Constructor method that initiates an instance of the GameOfLifeView object taking a specified game model

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

    __initialize_buttons():
        place the interactive components of the view into the window

    __set_control_options():
        create the frames necessary for some control options
    """

    def __init__(self, model: IGameOfLifeModel):
        """
        __init__(model):
        Constructor method that initiates an instance of the GameOfLifeView object taking a specified game model
        :param model: game model around which the view is constructed
        """
        super().__init__(className=' Game of Life')
        if model is None:
            raise ValueError('Model Cannot Be Null')
        self.__model = model
        cell_length = GameResources.cell_length
        self.__height = model.get_height() * cell_length + 10
        self.__width = model.get_width() * cell_length + 10

        # where cells will be displayed
        self.__canvas = DrawingCanvas(self, self.__width, self.__height, self.__model,
                                      GameResources.coloring_styles["Light"])
        # widget containing all buttons
        self.__button_frame = tkinter.Frame(self, height=30, width=self.__width)
        # widget containing the color style control
        self.__view_mode_frame = tkinter.Frame(self.__button_frame, padx=20)
        # widget containing structure spawning options
        self.__generate_structure_frame = tkinter.Frame(self.__button_frame, padx=20)
        # widget containing the speed control options
        self.__speed_slider = tkinter.Frame(self.__button_frame, padx=20)

        self.__button_next = None
        self.__button_start = None
        self.__button_exit = None
        self.__button_reset = None

    def render(self):
        """
        initiates the view to provide a display of the model
        """
        self.__set_control_options()
        self.__initialize_buttons()
        self.__canvas.draw_game()
        self.__canvas.pack()
        self.__canvas.mainloop()

    def __set_control_options(self):
        """
        create the frames necessary for some control option
        """
        # frame for color mode options
        view_mode_text = tkinter.Label(self.__view_mode_frame, text='View Mode: ', font=("Arial", 15))
        view_mode_text.pack(side='left')
        # frame for speed slider
        speed_text = tkinter.Label(self.__speed_slider, text='Speed: ', font=("Arial", 15))
        speed_text.pack(side='left')
        # frame for pattern spawning options
        generate_structure_text = tkinter.Label(self.__generate_structure_frame, text='Generate: ', font=("Arial", 15))
        generate_structure_text.pack(side='left')

    def get_model_hash(self):
        """
        used in ensuring that the same model is passed into the controller and the view
        :return hash of the model object
        """
        return self.__model.__hash__()

    def update(self):
        """
        redraws the current state of the model into the view
        """
        self.__canvas.draw_game()

    def set_button_listener(self, controller: IController):
        """
        Binds the buttons in the view to the Controller within the game.
        Allows the controller to listen to commands from the program user.
        :param controller: controller which will respond to user commands from the buttons
        """
        if controller is None:
            raise ValueError("Controller Cannot Be Null")
        # exit button
        self.__button_exit = tkinter.Button(self.__button_frame, text='Exit', bg='#ffb3fe',
                                            command=lambda c='exit': controller.action_performed(c),
                                            fg='red', )
        # next button
        self.__button_next = tkinter.Button(self.__button_frame, text='Next',
                                            command=lambda c='next': controller.action_performed(c))
        # clicking on grid to toggle cells state
        self.__canvas.bind("<Button-1>", lambda event, c='toggle cell': controller.action_performed(c, event))

        # start button
        self.__button_start = tkinter.Button(self.__button_frame, text='Start',
                                             command=lambda c='toggle play': controller.action_performed(c))
        # reset button
        self.__button_reset = tkinter.Button(self.__button_frame, text='Reset',
                                             command=lambda c='reset': controller.action_performed(c))
        # speed scale
        speed_scale = tkinter.Scale(self.__speed_slider, from_=1000, to=10, length=150, orient='horizontal',
                                    showvalue=False,
                                    command=lambda event, c='set speed': controller.action_performed(c, event))
        speed_scale.set(500)
        speed_scale.pack(side='right')

        # color mode dropdown list
        style_options = [str(key) for key in GameResources().coloring_styles.keys()]
        mode_menu_text = tkinter.StringVar(self.__view_mode_frame)
        mode_menu_text.set(style_options[0])
        view_mode_options = tkinter.OptionMenu(self.__view_mode_frame, mode_menu_text, *style_options,
                                               command=lambda event, c='change view mode':
                                               controller.action_performed(c, event))
        view_mode_options.pack(side='right')

        # spawn pattern dropdown list
        structure_options = [str(key) for key in GameResources().structures.keys()]
        generate_menu_text = tkinter.StringVar(self.__generate_structure_frame)
        generate_menu_text.set('Import')
        generate_structure_options = tkinter.OptionMenu(self.__generate_structure_frame, generate_menu_text,
                                                        *structure_options,
                                                        command=lambda event, c='generate':
                                                        controller.action_performed(c, event))
        generate_structure_options.pack(side='right')

    def toggle_start_stop_button(self, boolean: bool):
        """
        :param boolean: whether the game is playing (True) or paused (False)
        :return:
        """
        if boolean:
            self.__button_start['text'] = 'Stop'
        else:
            self.__button_start['text'] = 'Start'

    def __initialize_buttons(self):
        """
        place the interactive components of the view into the window
        """
        self.__button_exit.pack(side='left')
        self.__button_reset.pack(side='left')
        self.__button_next.pack(side='left')
        self.__button_start.pack(side='left')
        self.__view_mode_frame.pack(side='left')
        self.__speed_slider.pack(side='left')
        self.__generate_structure_frame.pack(side='right')
        self.__button_frame.pack(side='top')

    def change_style(self, style_name: str):
        """
        changes the coloring of the display to a specified style
        :param style_name: the color style to which the view will change
        """
        self.__canvas.change_style(GameResources.coloring_styles[style_name])
