import unittest
from Controller.Controller import Controller
from Model.GameOfLifeModel import GameOfLifeModel
from Model.MockModel import MockModel
from View.GameOfLifeView import GameOfLifeView
from View.MockView import MockView


class Coordinates:
    """ A class used to mimic the coordinates of a mouse click for testing cell toggling. """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class ControllerTests(unittest.TestCase):
    """ A class usd to test the game controller. """

    def test_controller_constructor(self):
        m = GameOfLifeModel(10, 10)
        v = GameOfLifeView(m)
        c = Controller(m, v)
        m_other = GameOfLifeModel(10, 10)

        # controller and view cannot have different instances of model
        with self.assertRaises(ValueError):
            c = Controller(m_other, v)

    def test_initial_controller_communication(self):

        m = MockModel()
        self.assertEqual(m.get_call_log(), "")
        v = MockView(m)
        self.assertEqual(v.get_call_log(), "")

        c = Controller(m, v)
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; ")

        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

    def test_fake_action(self):
        m = MockModel()
        v = MockView(m)
        c = Controller(m, v)
        c.execute()
        with self.assertRaises(ValueError):
            c.action_performed("fake command")
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

    def test_action_toggle_play(self):

        m = MockModel()
        v = MockView(m)
        c = Controller(m, v)
        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("toggle play")
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;update_state called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; update called; ")

        c.action_performed("toggle play")
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;update_state called;'
                                           'update_state called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; update called; update called; update called; ")

    def test_action_next(self):
        m = MockModel()
        v = MockView(m)
        c = Controller(m, v)
        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("next")
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;update_state called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called;"
                                           " update called; update called; ")

    def test_action_reset(self):
        m = MockModel()
        v = MockView(m)
        c = Controller(m, v)
        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("reset")
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;'
                                           'get_grid called;get_height called;get_width called;'
                                           'get_width called;get_height called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; ")

    def test_action_speed(self):
        m = MockModel()
        v = MockView(m)
        c = Controller(m, v)
        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("set speed")
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called;"
                                           " update called; ")

    def test_action_view_mode(self):
        m = MockModel()
        v = MockView(m)
        c = Controller(m, v)
        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("change view mode", "light")
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "change_style called: light; update called; ")

        c.action_performed("change view mode", "dark")
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "change_style called: light; update called; "
                                           "change_style called: dark; update called; ")

    def test_action_toggle_cell(self):
        m = MockModel()
        v = MockView(m)
        c = Controller(m, v, "test_resources.txt", "test_backup_resources.txt")

        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("toggle cell", Coordinates(7, 7))
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;get_width called;'
                                           'get_height called;toggle_cell called (x:0, y:0);')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; update called; ")

    def test_action_toggle_cell_big_grid(self):
        m = MockModel(5, 5)
        v = MockView(m)
        c = Controller(m, v, "test_resources.txt", "test_backup_resources.txt")

        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("toggle cell", Coordinates(7, 7))
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;get_width called;'
                                           'get_height called;toggle_cell called (x:0, y:0);')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; update called; ")

        c.action_performed("toggle cell", Coordinates(34, 72))
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;'
                                           'get_width called;get_height called;toggle_cell called (x:0, y:0);'
                                           'get_width called;get_height called;toggle_cell called (x:1, y:4);')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; update called; update called; update called; ")

        # coordinates out of bounds with the current canvas padding; should not toggle any cells
        c.action_performed("toggle cell", Coordinates(2, 2))
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;'
                                           'get_width called;get_height called;toggle_cell called (x:0, y:0);'
                                           'get_width called;get_height called;toggle_cell called (x:1, y:4);')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; update called; update called; update called;"
                                           " update called; ")

    def test_action_generate_dot(self):
        m = MockModel()
        v = MockView(m)
        c = Controller(m, v, "test_resources.txt", "test_backup_resources.txt")

        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("generate", 'Dot')
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;'
                                           'get_width called;get_height called;get_grid called;'
                                           'get_height called;get_width called;get_width called;get_height called;'
                                           'get_width called;get_height called;toggle_cell called (x:0, y:0);')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; update called; ")

    def test_action_generate_glider(self):
        m = MockModel(3, 3)
        v = MockView(m)
        c = Controller(m, v, "test_resources.txt", "test_backup_resources.txt")

        c.execute()
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; ")

        c.action_performed("generate", 'Glider')
        self.assertEqual(m.get_call_log(), 'get_height called;get_width called;get_grid called;get_width called;'
                                           'get_height called;get_grid called;get_height called;get_width called;'
                                           'get_width called;get_width called;get_width called;get_height called;'
                                           'get_width called;get_width called;get_width called;get_width called;'
                                           'get_height called;get_width called;get_width called;get_width called;'
                                           'get_width called;get_height called;get_width called;get_height called;'
                                           'toggle_cell called (x:2, y:0);toggle_cell called (x:0, y:1);'
                                           'toggle_cell called (x:2, y:1);toggle_cell called (x:1, y:2);'
                                           'toggle_cell called (x:2, y:2);')
        self.assertEqual(v.get_call_log(), "get_model_hash called; set_button_listener called; render called; "
                                           "update called; update called; ")

    def test_generate_file_unchanged(self):

        f = open("test_resources.txt", 'r')
        contents = f.read()
        f.close()

        m = MockModel(10, 10)
        v = MockView(m)
        c = Controller(m, v, "test_resources.txt", "test_backup_resources.txt")
        c.execute()
        c.action_performed("generate", "Glider")
        c.action_performed("generate", "Dot")

        f = open("test_resources.txt", 'r')
        new_contents = f.read()
        f.close()

        self.assertEqual(contents, new_contents)


if __name__ == '__main__':
    unittest.main()
