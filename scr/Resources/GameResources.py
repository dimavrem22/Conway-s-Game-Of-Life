class GameResources:
    coloring_styles = {
        'Light': {
            'dead cell color': 'white',
            'grid color': 'grey',
            'alive cell color': 'DarkGoldenrod2'},
        'Dark': {
            'dead cell color': 'black',
            'grid color': 'grey',
            'alive cell color': 'pink'},
        'No Grid': {
            'dead cell color': 'white',
            'grid color': 'white',
            'alive cell color': 'black'
        }
    }

    cell_length = 15

    structures = {
        'Glider': {
            'code': [(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)],
            'height': 3,
            'width': 3},
        'Copperhead Ship': {
            'code': [(1, 0), (2, 0), (5, 0), (6, 0),
                     (3, 1), (4, 1),
                     (3, 2), (4, 2),
                     (0, 3), (2, 3), (5, 3), (7, 3),
                     (0, 4), (7, 4),
                     (0, 6), (7, 6),
                     (1, 7), (2, 7), (5, 7), (6, 7),
                     (2, 8), (3, 8), (4, 8), (5, 8),
                     (3, 10), (4, 10),
                     (3, 11), (4, 11)],
            'height': 12,
            'width': 8},
        'Lightweight Ship': {
            'code': [(1, 0), (4, 0),
                     (0, 1),
                     (0, 2), (4, 2),
                     (0, 3), (1, 3), (2, 3), (3, 3)],
            'height': 4,
            'width': 5},
        'Glider Gun': {
            'code': [(24, 0),
                     (22, 1), (24, 1),
                     (12, 2), (13, 2), (20, 2), (21, 2), (34, 2), (35, 2),
                     (11, 3), (15, 3), (20, 3), (21, 3), (34, 3), (35, 3),
                     (0, 4), (1, 4), (10, 4), (16, 4), (20, 4), (21, 4),
                     (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5), (22, 5), (24, 5),
                     (10, 6), (16, 6), (24, 6),
                     (11, 7), (15, 7),
                     (12, 8), (13, 8)],
            'height': 14,
            'width': 36}
    }
