from Controller.IController import IController
from Resources.GameUtils import GameUtils
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

    update_struct_options(controller):
        Updates the structure option menu after changes to the library have been made.

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
        cell_length = GameUtils.cell_length
        self.__height = model.get_height() * cell_length + 5
        self.__width = model.get_width() * cell_length + 10

        # where cells will be displayed
        self.__canvas = DrawingCanvas(self, self.__width, self.__height, self.__model,
                                      GameUtils.coloring_styles["Light"])
        # widget containing all buttons
        self.__button_frame = tkinter.Frame(self, height=30, width=self.__width)
        # widget containing the color style control
        self.__view_mode_frame = tkinter.Frame(self.__button_frame, padx=20)
        # widget containing structure spawning options
        self.__generate_structure_frame = tkinter.Frame(self.__button_frame, padx=20)
        # widget containing the speed control options
        self.__speed_slider = tkinter.Frame(self.__button_frame, padx=20)
        # widget for managing structures
        self.__manage_frame = tkinter.Frame(self, pady=5)

        self.__button_next = None
        self.__button_start = None
        self.__button_exit = None
        self.__button_reset = None
        self.__button_manage = None
        self.__button_add = None

        self.__struct_option_menu = None

    def render(self):
        """ Initiates the view to provide a display of the model. """
        self.__set_control_options()
        self.__initialize_buttons()
        self.__canvas.draw_game()
        self.__canvas.pack()
        self.__canvas.mainloop()

    def __set_control_options(self):
        """ Create the frames necessary for some control option. """
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
        Used in ensuring that the same model is passed into the controller and the view.
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
        style_options = [str(key) for key in GameUtils().coloring_styles.keys()]
        mode_menu_text = tkinter.StringVar(self.__view_mode_frame)
        mode_menu_text.set(style_options[0])
        view_mode_options = tkinter.OptionMenu(self.__view_mode_frame, mode_menu_text, *style_options,
                                               command=lambda event, c='change view mode':
                                               controller.action_performed(c, event))
        view_mode_options.pack(side='right')

        # spawn pattern dropdown list
        self.__initialize_struct_menu(controller)

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
        """ Place the interactive components of the view into the window. """
        self.__button_exit.pack(side='left')
        self.__button_reset.pack(side='left')
        self.__button_next.pack(side='left')
        self.__button_start.pack(side='left')
        self.__view_mode_frame.pack(side='left')
        self.__speed_slider.pack(side='left')
        self.__generate_structure_frame.pack(side='right')
        self.__button_frame.pack(side='top')
        self.__button_add.pack(side='left')
        self.__button_manage.pack(side='right')
        self.__manage_frame.pack(side='bottom')

    def change_style(self, style_name: str):
        """
        Changes the coloring of the display to a specified style.
        :param style_name: the color style to which the view will change
        """
        self.__canvas.change_style(GameUtils.coloring_styles[style_name])

    def update_struct_options(self, controller: IController):
        """
        Recreates the menu options for structure generation after the library has been modified.
        :param controller: controller which will listen for user input via option menu
        """
        self.__struct_option_menu.pack_forget()
        self.__initialize_struct_menu(controller)

    def __initialize_struct_menu(self, controller: IController):
        """
        Generates the option menu for the generation of structures in the game.
        :param controller: controller which will listen for user input via option menu
        """
        structure_options = GameUtils("Resources/resources.txt").get_key_list("structures")
        generate_menu_text = tkinter.StringVar(self.__generate_structure_frame)
        generate_menu_text.set('Import')
        self.__struct_option_menu = tkinter.OptionMenu(self.__generate_structure_frame, generate_menu_text,
                                                       *structure_options,
                                                       command=lambda event, c='generate':
                                                       controller.action_performed(c, event))
        self.__struct_option_menu.pack(side='right')

        self.__button_add = tkinter.Button(self.__manage_frame, text='Add Structure',
                                           command=lambda c='add structure': controller.action_performed(c))
        self.__button_manage = tkinter.Button(self.__manage_frame, text='Manage Structures',
                                              command=lambda c='manage structures': controller.action_performed(c))


class StructAddView(tkinter.Tk):
    """
    A class used to represent the window popup for the addition of structures to the library.

    Parameters
    ----------
    __button_frame: frame for buttons in the window
    __add_button: button for the addition of a structure to the library
    __cancel_button: exits the window without saving the structure to the library
    __entry_frame: frame containing the text input
    __entry_label: labels the location where the user will type structure name
    __name_entry: object which allows user to enter text

    Methods
    -------
    __init(controller):
        Creates an instance of the StructureAddView, taking a controller which will listen to for user input.

    GameUtils(controller):
        Creates buttons featured in the window and sets a controller to listen for user input.


    """

    def __init__(self, controller: IController):
        """
        Creates an instance of the StructureAddView and populates the window with appropriate features.
        :param controller: controller which will listen to for user input
        """
        super().__init__(className=' Structure Adder')
        self.__button_frame = tkinter.Frame(self, padx=20, pady=20)
        self.__add_button = None
        self.__cancel_button = None
        self.__entry_frame = tkinter.Frame(self, padx=20, pady=20)
        self.__entry_frame.pack(side='top')
        self.__entry_label = tkinter.Label(self.__entry_frame, text='Structure Name: ', font=("Arial", 15))
        self.__entry_label.pack(side='left')
        self.__entry_label.pack(side='left')
        self.__name_entry = None
        self.GameUtils(controller)
        self.__name_entry.pack(side='right')
        self.__add_button.pack(side='left')
        self.__cancel_button.pack(side='right')
        self.__button_frame.pack(side='top')

    def GameUtils(self, controller: IController):
        """
        Creates the necessary buttons and sets the controller to listen for user input.
        :param controller: controller which will listen to for user input
        """
        self.__add_button = tkinter.Button(self.__button_frame, text='Add',
                                           command=lambda c='add structure':
                                           controller.action_performed(c, self.__name_entry.get()))
        self.__cancel_button = tkinter.Button(self.__button_frame, text='Cancel', fg='red', command=self.destroy)
        self.__name_entry = tkinter.Entry(self.__entry_frame, width=25)


class ManageStructureView(tkinter.Tk):
    """
    A class used to represent the window popup for the management of structure library.

    Parameters
    ----------
    __exit_button: closes the window
    __delete_button: deletes the selected structures
    __default_button: used to reset the structure library
    __button_frame: frame containing the buttons featured in the window
    __check_frame: frame containing the checkboxes of structures from the library
    __selected_list: list of structures that are selected by the user

    Methods
    -------
    __init(controller):
        Creates an instance of the StructureAddView, taking a controller which will listen to for user input.

    __initialize_checkboxes():
        Generates the checkboxes for each structure.

    GameUtils(controller):
        Generates the buttons and sets the controller to listen for user input.

    __update_selected_list():
         Modifies the __selected_list to contain only the structures selected by the user via checkboxes.
    """

    def __init__(self, controller: IController):
        """
         Creates an instance of the StructureAddView.
        :param controller: Controller which will listen to for user input
        """
        super().__init__(className=' Structure Manager')
        self.__exit_button = None
        self.__delete_button = None
        self.__default_button = None
        self.__button_frame = tkinter.Frame(self, padx=20, pady=20)
        self.__check_frame = tkinter.Frame(self, padx=20, pady=20, width=1000)
        self.__selected_list = []
        self.__initialize_check_boxes()
        self.__check_frame.pack(side='top', anchor='w')
        self.GameUtils(controller)
        self.__button_frame.pack(side='bottom')

    def __initialize_check_boxes(self):
        """ Generates the checkboxes for each structure. """
        idx = 0
        for s in GameUtils("Resources/resources.txt").get_key_list("structures"):
            c = tkinter.Checkbutton(self.__check_frame, text=s)
            c['command'] = lambda struct=c['text']: self.__update_selected_list(struct)
            c.pack(side='top', anchor='w')
            idx += 1

    def GameUtils(self, controller: IController):
        """
        Generates the buttons and sets the controller to listen for user input.
        :param controller: controller listening to user input
        """
        self.__delete_button = tkinter.Button(self.__button_frame, text='Delete', padx='15',
                                              command=lambda c='delete':
                                              controller.action_performed(c, self.__selected_list))
        self.__delete_button.pack(side='left')
        self.__default_button = tkinter.Button(self.__button_frame, text='Reset To Default', padx='15',
                                               command=lambda c='default':
                                               controller.action_performed(c))
        self.__default_button.pack(side='left')
        self.__exit_button = tkinter.Button(self.__button_frame, text='Close', fg='red',
                                            padx='15', command=self.destroy)
        self.__exit_button.pack(side='left')

    def __update_selected_list(self, struct_name: str):
        """Modifies the __selected_list to contain only the structures selected by the user via checkboxes. """
        if struct_name in self.__selected_list:
            self.__selected_list.remove(struct_name)
        else:
            self.__selected_list.append(struct_name)
