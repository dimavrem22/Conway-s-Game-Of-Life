from Model.GameOfLifeModel import GameOfLifeModel


class OptimizedGameOfLifeModel(GameOfLifeModel):

    def __init__(self, width: int = 20, height: int = 10):
        super().__init__(width, height)
        self.__list_alive = []

    def toggle_cell(self, x: int, y: int):
        if self.get_grid()[y][x]:
            self.__list_alive.remove((x, y))
        else:
            self.__list_alive.append((x, y))
        super().toggle_cell(x, y)

    def update_state(self):
        toggle_list = []
        list_to_check = []
        for i in self.__list_alive:
            startX = max(0, i[1] - 1)
            endX = min(self.get_width() - 1, i[1] + 1)
            startY = max(0, i[0] - 1)
            endY = min(self.get_height() - 1, i[0] + 1)
            while startY <= endY:
                sX = startX
                while sX <= endX:
                    if (sX, startY) not in list_to_check:
                        list_to_check.append((sX, startY))
                    sX += 1
                startY += 1

        for i in list_to_check:
            neighbors = self.surrounding_live_cells(i[0], i[1])
            alive = self.get_grid()[i[1]][i[0]]
            if alive and (neighbors < 2 or neighbors > 3):
                toggle_list.append((i[0], i[1]))
            elif not alive and neighbors == 3:
                toggle_list.append((i[0], i[1]))

        for i in toggle_list:
            self.toggle_cell(i[0], i[1])

