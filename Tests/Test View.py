import unittest
from Model.GameOfLifeModel import GameOfLifeModel
from View.GameOfLifeView import GameOfLifeView


class ViewTests(unittest.TestCase):
    """ A class used to test the game view. """

    def test_get_model_hash(self):
        m = GameOfLifeModel(10, 10)
        v = GameOfLifeView(m)
        m_other = GameOfLifeModel(10, 10)

        self.assertTrue(v.get_model_hash() == m.__hash__())
        self.assertFalse(v.get_model_hash() == m_other.__hash__())


if __name__ == '__main__':
    unittest.main()
