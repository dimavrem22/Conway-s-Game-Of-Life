import unittest
from Model.GameOfLifeModel import GameOfLifeModel


class GameOfLifeModelTests(unittest.TestCase):
    """ A class used to run test for the GameOfLifeModel. """

    def test_constructor1(self):
        m = GameOfLifeModel(10,20)
        self.assertEqual(m.get_width(), 10)
        self.assertEqual(m.get_height(), 20)
        self.assertEqual(len(m.get_grid()), 20)
        self.assertEqual(len(m.get_grid()[0]), 10)
        self.assertEqual(m.get_grid()[0][0], False)
        self.assertEqual(m.get_grid()[19][9], False)
        self.assertEqual(m.get_grid()[3][2], False)


    def test_constructor_exceptions(self):
        with self.assertRaises(ValueError):
            m = GameOfLifeModel(0, 10)
        with self.assertRaises(ValueError):
            m = GameOfLifeModel(10, 0)
        with self.assertRaises(ValueError):
            m = GameOfLifeModel(-19, 4)
        with self.assertRaises(ValueError):
            m = GameOfLifeModel(10, -2)

    def test_toggle_cell(self):
        m = GameOfLifeModel(5, 5)
        self.assertEqual(m.get_grid()[0][0], False)
        m.toggle_cell(0, 0)
        self.assertEqual(m.get_grid()[0][0], True)
        m.toggle_cell(0, 0)
        self.assertEqual(m.get_grid()[0][0], False)
        m.toggle_cell(0, 0)
        m.toggle_cell(1, 0)
        m.toggle_cell(3, 4)
        m.toggle_cell(2, 2)
        self.assertEqual(m.get_grid()[0][0], True)
        self.assertEqual(m.get_grid()[0][1], True)
        self.assertEqual(m.get_grid()[4][3], True)
        self.assertEqual(m.get_grid()[2][2], True)
        with self.assertRaises(ValueError):
            m.toggle_cell(-1, 4)
        with self.assertRaises(ValueError):
            m.toggle_cell(4, -3)
        with self.assertRaises(ValueError):
            m.toggle_cell(5, 4)
        with self.assertRaises(ValueError):
            m.toggle_cell(4, 5)

    def test_get_width_height(self):
        m = GameOfLifeModel(1, 1)
        self.assertEqual(m.get_width(), 1)
        self.assertEqual(m.get_height(), 1)
        m = GameOfLifeModel(2, 10)
        self.assertEqual(m.get_width(), 2)
        self.assertEqual(m.get_height(), 10)

    def test_get_grid(self):
        m = GameOfLifeModel(1, 1)
        grid1 = [[False]]
        self.assertEqual(m.get_grid(), [[False]])
        m.toggle_cell(0, 0)
        self.assertEqual(m.get_grid(), [[True]])
        m = GameOfLifeModel(2, 3)
        self.assertEqual(m.get_grid(), [[False, False], [False, False], [False, False]])
        m.toggle_cell(0, 0)
        m.toggle_cell(1, 1)
        m.toggle_cell(0, 2)
        self.assertEqual(m.get_grid(), [[True, False], [False, True], [True, False]])

    def test_update_state(self):
        m = GameOfLifeModel(1, 1)
        m.toggle_cell(0, 0)
        self.assertEqual(m.get_grid()[0][0], True)
        m.update_state()
        self.assertEqual(m.get_grid()[0][0], False)
        m = GameOfLifeModel(3, 3)
        m.toggle_cell(0, 0)
        m.toggle_cell(0, 1)
        m.toggle_cell(1, 0)
        self.assertEqual(m.get_grid(), [[True, True, False],
                                        [True, False, False],
                                        [False, False, False]])
        m.update_state()
        self.assertEqual(m.get_grid(), [[True, True, False],
                                        [True, True, False],
                                        [False, False, False]])
        m.toggle_cell(2, 2)
        m.update_state()
        self.assertEqual(m.get_grid(), [[True, True, False],
                                        [True, False, True],
                                        [False, True, False]])
        m.update_state()
        self.assertEqual(m.get_grid(), [[True, True, False],
                                        [True, False, True],
                                        [False, True, False]])
        m.toggle_cell(2, 2)
        m.update_state()
        self.assertEqual(m.get_grid(), [[True, True, False],
                                        [True, False, True],
                                        [False, True, True]])
        m.toggle_cell(1, 1)
        m.update_state()
        self.assertEqual(m.get_grid(), [[True, False, True],
                                        [False, False, False],
                                        [True, False, True]])
        m.update_state()
        self.assertEqual(m.get_grid(), [[False, False, False],
                                        [False, False, False],
                                        [False, False, False]])
        m = GameOfLifeModel(4, 4)
        self.assertEqual(m.get_grid(), [[False, False, False, False],
                                        [False, False, False, False],
                                        [False, False, False, False],
                                        [False, False, False, False]])
        m.toggle_cell(1, 0)
        m.toggle_cell(0, 2)
        m.toggle_cell(1, 2)
        m.toggle_cell(2, 2)
        m.toggle_cell(2, 1)
        self.assertEqual(m.get_grid(), [[False, True, False, False],
                                        [False, False, True, False],
                                        [True, True, True, False],
                                        [False, False, False, False]])
        m.update_state()
        self.assertEqual(m.get_grid(), [[False, False, False, False],
                                        [True, False, True, False],
                                        [False, True, True, False],
                                        [False, True, False, False]])
        m.update_state()
        self.assertEqual(m.get_grid(), [[False, False, False, False],
                                        [False, False, True, False],
                                        [True, False, True, False],
                                        [False, True, True, False]])
        m.update_state()
        self.assertEqual(m.get_grid(), [[False, False, False, False],
                                        [False, True, False, False],
                                        [False, False, True, True],
                                        [False, True, True, False]])
        m.update_state()
        self.assertEqual(m.get_grid(), [[False, False, False, False],
                                        [False, False, True, False],
                                        [False, False, False, True],
                                        [False, True, True, True]])


if __name__ == '__main__':
    unittest.main()
