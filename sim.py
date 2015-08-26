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

        # mark starting area
        self.explored_map[self.start[0]][self.start[1]] = 6
        self.explored_map[self.start[0] - 1][self.start[1]] = 6
        self.explored_map[self.start[0] + 1][self.start[1]] = 6
        self.explored_map[self.start[0]][self.start[1] - 1] = 6
        self.explored_map[self.start[0] - 1][self.start[1] - 1] = 6
        self.explored_map[self.start[0] + 1][self.start[1] - 1] = 6
        self.explored_map[self.start[0]][self.start[1] + 1] = 6
        self.explored_map[self.start[0] - 1][self.start[1] + 1] = 6
        self.explored_map[self.start[0] + 1][self.start[1] + 1] = 6
        # mark goal area
        self.explored_map[self.goal[0]][self.goal[1]] = 7
        self.explored_map[self.goal[0] - 1][self.goal[1]] = 7
        self.explored_map[self.goal[0] + 1][self.goal[1]] = 7
        self.explored_map[self.goal[0]][self.goal[1] - 1] = 7
        self.explored_map[self.goal[0] - 1][self.goal[1] - 1] = 7
        self.explored_map[self.goal[0] + 1][self.goal[1] - 1] = 7
        self.explored_map[self.goal[0]][self.goal[1] + 1] = 7
        self.explored_map[self.goal[0] - 1][self.goal[1] + 1] = 7
        self.explored_map[self.goal[0] + 1][self.goal[1] + 1] = 7

        self.current = [18, 1] # find_centre(start)
        # TODO:
        # mark and update the current Robot area
        # do not let Robot go through obstacles
        self.direction = NORTH
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
        if self.direction == NORTH:
            self.current[0] += -1
        elif self.direction == EAST:
            self.current[1] += 1
        elif self.direction == WEST:
            self.current[1] += -1
        else: # self.direction == SOUTH
            self.current[0] += 1

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
        # BUGS:
        # can "see through" obstacles
        sensors = []
        for i in range(6):
            sensors.append([])
        for i in range(4):
            sensors[0].append(self.__get_value(self.current[0] - i - 2, self.current[1] - 1))
            sensors[1].append(self.__get_value(self.current[0] - i - 2, self.current[1]))
            sensors[2].append(self.__get_value(self.current[0] - i - 2, self.current[1] + 1))
            sensors[3].append(self.__get_value(self.current[0] - 1, self.current[1] + i + 2))
            sensors[4].append(self.__get_value(self.current[0] - 1, self.current[1] - i - 2))
            sensors[5].append(self.__get_value(self.current[0] + 1, self.current[1] - i - 2))
        return sensors

if __name__ == '__main__':
    robot = Robot()
    print(robot.get_sensors())
    print(robot.explored_map)
