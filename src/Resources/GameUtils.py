import json
from os import path


def make_coordinate_tuple(s: str) -> ():
    """ Decodes string of x,y coordinate point and returns a tuple. """
    s = s[1:-1]
    idx = s.find(",")
    num1 = s[0:idx]
    num2 = s[idx + 1: len(s)]
    return int(num1), int(num2)


def write_coordinates_as_str(coordinate_list: []) -> str:
    """ Converts a list of coordinates into a string. """
    result = ""
    if len(coordinate_list) == 0:
        return result
    else:
        for coordinate in coordinate_list:
            result += "(" + str(coordinate[0]) + "," + str(coordinate[1]) + ") "
        return result[:-1]


def calc_struct_dimensions(coordinate_list: []):
    """ Calculates the width and height of a structure. """
    if len(coordinate_list) == 0:
        return 0, 0
    else:
        width = 0
        height = 0
        for c in coordinate_list:
            if c[0] > width:
                width = c[0]
            if c[1] > height:
                height = c[1]
        return width + 1, height + 1


class GameUtils:
    """
    A class used to store constants for the Game of Life implementation.

    Parameters
    ----------
    __file_path: path to the file containing necessary information.

    Methods
    -------
    __init__(file_path):
        Method used to create an instance of GameUtils class.

    get_key_list(key):
        Gets the list of keys for a specified section within the file.

    get_struct_coordinates(struct):
        Gets the list of coordinates for a particular structure within the library.

    get_struct_dimensions(struct):
        Gets the height and width of the specified structure of interest.

    add_structure(struct_name, coordinates):
        Adds the structure with the specified coordinated to the library under the specified name.

    delete_structure(struct_name):
        Removes the specified structure from the library.

    reset_default(backup_file_path):
        Resets the resources file from which structures to a specified backup file.

    """

    coloring_styles = {
        "Light": {
            "dead cell color": "white",
            "grid color": "grey",
            "alive cell color": "DarkGoldenrod2"},
        "Dark": {
            "dead cell color": "black",
            "grid color": "grey",
            "alive cell color": "pink"},
        "No Grid": {
            "dead cell color": "white",
            "grid color": "white",
            "alive cell color": "black"
        }
    }

    cell_length = 15

    canvas_padding = 5

    def __init__(self, file_path: str = None):
        """ Creates an instance of the class with the option of a file path. """
        self.__file_path = file_path

    def get_key_list(self, key: str):
        """
        Gets a list of keys within the specified section of a file.
        :param key: name of the file section
        :return: list of dict keys
        """
        if self.__file_path is None:
            raise FileNotFoundError("File path cannot be null.")
        f = open(self.__file_path, "r")
        contents = f.read()
        f.close()
        dictionary = json.loads(contents)
        if key not in dictionary.keys():
            raise ValueError("Invalid Key!")
        return dictionary[key].keys()

    def get_struct_coordinates(self, struct_name) -> []:
        """
        Gets the list of coordinates of living cells for a particular structure.
        :param struct_name: name of structure whose coordinates are requested
        :return: list of coordinates of a specified structure
        """
        if self.__file_path is None:
            raise FileNotFoundError("File path cannot be null.")
        if struct_name not in self.get_key_list("structures"):
            raise ValueError("Invalid Structure!")
        f = open(self.__file_path, "r")
        contents = f.read()
        f.close()
        d = json.loads(contents)
        coordinates = d["structures"][struct_name]["code"].split()
        result = []
        for i in coordinates:
            result.append(make_coordinate_tuple(i))
        return result

    def get_struct_dimensions(self, struct_name: str):
        """
        Gets the dimensions of a specified structure.
        :param struct_name: Name of structure whose dimensions are requested.
        :return: width and height of a specified structure
        """
        if self.__file_path is None:
            raise FileNotFoundError("File path cannot be null.")
        if struct_name not in self.get_key_list("structures"):
            raise ValueError("Invalid Structure!")
        f = open(self.__file_path, "r")
        contents = f.read()
        f.close()
        d = json.loads(contents)
        return int(d["structures"][struct_name]["width"]), int(d["structures"][struct_name]["height"])

    def add_structure(self, struct_name: str, coordinates: []):
        """
        Adds a structure to the library.
        :param struct_name: name of the structure to be added (cannot already exist in library).
        :param coordinates: coordinated of th structure to be added.
        """
        if self.__file_path is None:
            raise FileNotFoundError("File path cannot be null.")
        if struct_name in self.get_key_list('structures'):
            raise ValueError("Name already in file.")
        f = open(self.__file_path, "r")
        contents = f.read()
        f.close()
        d = json.loads(contents)

        dimensions = calc_struct_dimensions(coordinates)

        d["structures"][struct_name] = {
            "code": write_coordinates_as_str(coordinates),
            "width": str(dimensions[0]),
            "height": str(dimensions[1])}
        new_contents = json.dumps(d, sort_keys=True, indent=4)
        f = open(self.__file_path, "w")
        f.truncate()
        f.write(new_contents)
        f.close()

    def remove_structure(self, struct_name):
        """
        Removes a specified structure from the library.
        :param struct_name: Name of a structure to be removed from the library
        """
        if self.__file_path is None:
            raise FileNotFoundError("File path cannot be null.")
        if struct_name not in self.get_key_list('structures'):
            raise ValueError("Name already in file.")
        f = open(self.__file_path, "r")
        contents = f.read()
        f.close()
        d = json.loads(contents)
        d["structures"].pop(struct_name)
        new_contents = json.dumps(d, sort_keys=True, indent=4)
        f = open(self.__file_path, "w")
        f.truncate()
        f.write(new_contents)
        f.close()

    def reset_default(self, backup_file_path: str):
        """
        Resets the resources file using a default version.
        :param backup_file_path: file from which the resources file is reset
        """
        if self.__file_path is None:
            raise ValueError("File path cannot be null.")
        if not path.exists(backup_file_path):
            raise FileNotFoundError("Invalid Backup File")
        backup = open(backup_file_path, "r")
        backup_content = backup.read()
        backup.close()
        f = open(self.__file_path, 'w')
        f.truncate()
        f.write(backup_content)
        f.close()
