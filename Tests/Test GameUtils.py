import unittest
from Resources.GameUtils import GameUtils


class GameUtilsTests(unittest.TestCase):
    """ A class used to test the functionality of GameUtils. """

    def test_get_key_list(self):
        u = GameUtils()
        with self.assertRaises(FileNotFoundError):
            u.get_key_list("key")
        with self.assertRaises(FileNotFoundError):
            u.get_key_list("structures")
        u = GameUtils("test_resources.txt")
        with self.assertRaises(ValueError):
            u.get_key_list("key")
        with self.assertRaises(ValueError):
            u.get_key_list("invalid key")

        self.assertEqual(list(u.get_key_list("structures")),
                         ['Bee', 'Diamond', 'Dot', 'Glider', 'Glider Gun', 'Heart'])
        self.assertEqual(list(u.get_key_list("colors")), [])

    def test_get_struct_dimensions(self):
        u = GameUtils()
        with self.assertRaises(FileNotFoundError):
            u.get_struct_dimensions("Dot")

        u = GameUtils("test_resources.txt")
        with self.assertRaises(ValueError):
            u.get_struct_dimensions("Invalid structure")

        self.assertEqual(u.get_struct_dimensions("Dot"), (1, 1))
        self.assertEqual(u.get_struct_dimensions("Glider"), (3, 3))
        self.assertEqual(u.get_struct_dimensions("Glider Gun"), (36, 20))
        self.assertEqual(u.get_struct_dimensions("Diamond"), (12, 9))

    def test_get_struct_coordinates(self):
        u = GameUtils()
        with self.assertRaises(FileNotFoundError):
            u.get_struct_coordinates("Dot")

        u = GameUtils("test_resources.txt")
        with self.assertRaises(ValueError):
            u.get_struct_coordinates("Invalid structure")

        self.assertEqual(u.get_struct_coordinates("Dot"), [(0, 0)])
        self.assertEqual(u.get_struct_coordinates("Glider"), [(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)])
        self.assertEqual(u.get_struct_coordinates("Glider Gun"), [(24, 0), (22, 1), (24, 1), (12, 2), (13, 2), (20, 2),
                                                                  (21, 2), (34, 2), (35, 2), (11, 3), (15, 3), (20, 3),
                                                                  (21, 3), (34, 3), (35, 3), (0, 4), (1, 4), (10, 4),
                                                                  (16, 4), (20, 4), (21, 4), (0, 5), (1, 5), (10, 5),
                                                                  (14, 5), (16, 5), (17, 5), (22, 5), (24, 5), (10, 6),
                                                                  (16, 6), (24, 6), (11, 7), (15, 7), (12, 8), (13, 8)])

    def test_add_structure(self):
        u = GameUtils()
        with self.assertRaises(FileNotFoundError):
            u.add_structure("New", [(0, 0)])

        u = GameUtils("test_resources.txt")
        f = open("test_resources.txt", 'r')
        contents = f.read()

        self.assertFalse("New" in u.get_key_list("structures"))

        with self.assertRaises(ValueError):
            u.add_structure("Dot", [(2, 3), (4, 2)])
        u.add_structure("New", [(0, 0)])

        self.assertTrue("New" in u.get_key_list("structures"))
        self.assertEqual(u.get_struct_dimensions("New"), (1, 1))
        self.assertEqual(u.get_struct_coordinates("New"), [(0, 0)])

        u.add_structure("New2", [(0, 0), (1, 1), (1, 2)])

        self.assertTrue("New2" in u.get_key_list("structures"))
        self.assertEqual(u.get_struct_coordinates("New2"), [(0, 0), (1, 1), (1, 2)])
        self.assertEqual(u.get_struct_dimensions("New2"), (2, 3))

        f = open("test_resources.txt", 'w')
        f.truncate()
        f.write(contents)
        f.close()
        self.assertFalse("New" in u.get_key_list("structures"))
        self.assertFalse("New2" in u.get_key_list("structures"))

    def test_remove_structure(self):
        u = GameUtils()
        with self.assertRaises(FileNotFoundError):
            u.remove_structure("Dot")

        u = GameUtils("test_resources.txt")
        with self.assertRaises(ValueError):
            u.remove_structure("Invalid Structure")

        f = open("test_resources.txt", "r")
        contents = f.read()
        f.close()

        self.assertTrue("Dot" in u.get_key_list("structures"))
        u.remove_structure("Dot")
        self.assertFalse("Dot" in u.get_key_list("structures"))
        with self.assertRaises(ValueError):
            u.remove_structure("Dot")
        with self.assertRaises(ValueError):
            u.get_struct_coordinates("Dot")

        self.assertTrue("Glider" in u.get_key_list("structures"))
        u.remove_structure("Glider")
        self.assertFalse("Dot" in u.get_key_list("structures"))
        with self.assertRaises(ValueError):
            u.remove_structure("Glider")
        with self.assertRaises(ValueError):
            u.get_struct_coordinates("Glider")

        f = open("test_resources.txt", "w")
        f.truncate()
        f.write(contents)
        f.close()

    def test_reset_default(self):
        f = open("test_resources.txt", "r")
        contents = f.read()
        f.close()

        u = GameUtils()
        with self.assertRaises(ValueError):
            u.reset_default("test_backup_resources.txt")

        u = GameUtils("test_resources.txt")
        with self.assertRaises(FileNotFoundError):
            u.reset_default("Invalid Structure")

        u.remove_structure("Dot")
        u.remove_structure("Glider")
        u.remove_structure("Bee")
        u.remove_structure("Diamond")
        u.remove_structure("Heart")

        self.assertEqual(list(u.get_key_list("structures")), ["Glider Gun"])

        u_back_up = GameUtils("test_backup_resources.txt")
        self.assertEqual(list(u_back_up.get_key_list("structures")), ["Dot", "Glider"])

        u.reset_default("test_backup_resources.txt")
        self.assertEqual(list(u.get_key_list("structures")), ["Dot", "Glider"])

        f = open("test_resources.txt", "w")
        f.truncate()
        f.write(contents)
        f.close()


if __name__ == '__main__':
    unittest.main()
