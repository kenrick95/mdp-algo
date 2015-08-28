from constants import *
import zope.event

class Robot(object):
    """docstring for Robot"""
    def __init__(self):
        super(Robot, self).__init__()
        # def find_centre(coords):
        #     avg_coord = [0, 0]
        #     for coord in coords:
        #         avg_coord[0] += coord[0]
        #         avg_coord[1] += coord[1]
        #     avg_coord[0] = int(avg_coord[0] / len(coords))
        #     avg_coord[1] = int(avg_coord[1] / len(coords))
        #     return avg_coord
        self.__map = []
        self.explored_map = []
        self.__get_map()
        
        self.MAX_ROW = len(self.__map)
        self.MAX_COL = len(self.__map[0])

        # for i in range(self.MAX_ROW):
        #     for j in range(self.MAX_COL):
        #         if self.__map[i][j] == 6:
        #             start.append([i, j])
        #         elif self.__map[i][j] == 7:
        #             goal.append([i, j])

        self.start = [18, 1] # find_centre(start)
        self.goal = [1, 13] # find_centre(goal)

        # mark start & goal area
        self.__mark_surroundings(self.start, 6)
        self.__mark_surroundings(self.goal, 7)

        self.current = [18, 1] # find_centre(start)
        self.__mark_robot()
        self.direction = NORTH


        zope.event.notify("INIT")

    def __mark_surroundings(self, _center, _value):
        directions = [[0, 0], [0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, 0], [1, 1], [1, -1]]
        for direction in directions:
            self.explored_map[_center[0] + direction[0]][_center[1] + direction[1]] = _value
    
    def __mark_robot(self):
        self.__mark_surroundings(self.current, 3)
        self.explored_map[self.current[0]][self.current[1]] = 5
        self.explored_map[self.current[0] - 1][self.current[1]] = 4
    def __clear_marks(self):
        directions = [[0, 0], [0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, 0], [1, 1], [1, -1]]
        for direction in directions:
            value = 1
            self.explored_map[self.current[0] + direction[0]][self.current[1] + direction[1]] = value

    def __is_safe(self, _center):
        directions = [[0, 0], [0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, 0], [1, 1], [1, -1]]
        for direction in directions:
            if self.__map[_center[0] + direction[0]][_center[1] + direction[1]] == 1:
                return False
        return True

    def __get_map(self):
        start = []
        goal = []
        with open("map.txt") as f:
            content = f.readlines()
            for line in content:
                temp = []
                temp0 = []
                for char in line:
                    if char.isdigit():
                        temp.append(int(char))
                        temp0.append(0)
                self.__map.append(temp)
                self.explored_map.append(temp0)

    def action(self, action):
        zope.event.notify(action)
        if action == FORWARD:
            self.forward()
        else:
            self.rotate(action)

    def forward(self):
        # TODO, do proper "trailing" path
        self.__clear_marks()
        self.__mark_surroundings(self.start, 6)
        self.__mark_surroundings(self.goal, 7)
        self.explored_map[self.current[0]][self.current[1]] = 8

        next_coords = []
        next_coords.append(self.current[0])
        next_coords.append(self.current[1])
        if self.direction == NORTH:
            next_coords[0] += -1
        elif self.direction == EAST:
            next_coords[1] += 1
        elif self.direction == WEST:
            next_coords[1] += -1
        else: # self.direction == SOUTH
            next_coords[0] += 1
        if 0 <= next_coords[0] < self.MAX_ROW and 0 <= next_coords[1] < self.MAX_COL and self.__is_safe(next_coords):
            self.current[0] = next_coords[0]
            self.current[1] = next_coords[1]
        self.__mark_robot()

    def rotate(self, direction):
        if direction == RIGHT: # clockwise
            if self.direction == NORTH:
                self.direction = EAST
            elif self.direction == EAST:
                self.direction = SOUTH
            elif self.direction == SOUTH:
                self.direction = WEST
            elif self.direction == WEST:
                self.direction = NORTH
        else: # Counter-clockwise
            if self.direction == NORTH:
                self.direction = WEST
            elif self.direction == EAST:
                self.direction = NORTH
            elif self.direction == SOUTH:
                self.direction = EAST
            elif self.direction == WEST:
                self.direction = SOUTH

    def __get_value(self, y, x):
        if 0 <= y < self.MAX_ROW and 0 <= x < self.MAX_COL:
            if self.__map[y][x] == 1:
                if self.explored_map[y][x] == 0:
                    self.explored_map[y][x] = 2
                return 2
            else:
                if self.explored_map[y][x] == 0:
                    self.explored_map[y][x] = 1
                return 1
        return 2

    def get_sensors(self):
        sensors = []
        for i in range(6):
            sensors.append([])
            for j in range(4):
                sensors[i].append([])

        for i in range(4):
            sensors[0][i] = self.__get_value(self.current[0] - i - 2, self.current[1] - 1)
            if sensors[0][i] == 2:
                break
        for i in range(4):
            sensors[1][i] = self.__get_value(self.current[0] - i - 2, self.current[1])
            if sensors[1][i] == 2:
                break
        for i in range(4):
            sensors[2][i] = self.__get_value(self.current[0] - i - 2, self.current[1] + 1)
            if sensors[2][i] == 2:
                break
        for i in range(4):
            sensors[3][i] = self.__get_value(self.current[0] - 1, self.current[1] + i + 2)
            if sensors[3][i] == 2:
                break
        for i in range(4):
            sensors[4][i] = self.__get_value(self.current[0] - 1, self.current[1] - i - 2)
            if sensors[4][i] == 2:
                break
        for i in range(4):
            sensors[5][i] = self.__get_value(self.current[0] + 1, self.current[1] - i - 2)
            if sensors[5][i] == 2:
                break
        return sensors

if __name__ == '__main__':
    robot = Robot()
    print(robot.get_sensors())
    print(robot.explored_map)
