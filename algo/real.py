from constants import *
import zope.event

class Robot(object):
    """docstring for Robot"""
    def __init__(self):
        super(Robot, self).__init__()
        self.explored_map = []
        
        self.MAX_ROW = 20
        self.MAX_COL = 15

        for i in range(self.MAX_ROW):
            self.explored_map.append([])
            for j in range(self.MAX_COL):
                self.explored_map[i].append(0)

        self.__recolor_later = []

        self.start = [18, 1]
        self.goal = [1, 13]


        self.sensors = []
        for i in range(6):
            self.sensors.append([])
            for j in range(4):
                self.sensors[i].append(None)

        # mark start & goal area
        self.__mark_surroundings(self.start, 6)
        self.__mark_surroundings(self.goal, 7)

        self.current = [18, 1] # find_centre(start)
        
        self.direction = NORTH # ODO: need to face NORTH in order to work!
        self.__mark_robot()


        zope.event.notify("INIT")

    def __mark_surroundings(self, _center, _value):
        directions = [[0, 0], [0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, 0], [1, 1], [1, -1]]
        for direction in directions:
            current_value = self.explored_map[_center[0] + direction[0]][_center[1] + direction[1]]
            if current_value == 1 or 6 <= current_value <= 9:
                self.__recolor_later.append({
                    "coord": [_center[0] + direction[0], _center[1] + direction[1]],
                    "value": current_value
                })

            self.explored_map[_center[0] + direction[0]][_center[1] + direction[1]] = _value
    
    def __mark_robot(self):
        self.__mark_surroundings(self.current, 3)
        self.explored_map[self.current[0]][self.current[1]] = 5
        if self.direction == NORTH:
            self.explored_map[self.current[0] - 1][self.current[1]] = 4
        elif self.direction == EAST:
            self.explored_map[self.current[0]][self.current[1] + 1] = 4
        elif self.direction == WEST:
            self.explored_map[self.current[0]][self.current[1] - 1] = 4
        else: # self.direction == SOUTH
            self.explored_map[self.current[0] + 1][self.current[1]] = 4
    def __clear_marks(self):
        # need to save original marks (e.g. 1, 6, 7, 8, 9)
        for o in self.__recolor_later:
            self.explored_map[o['coord'][0]][o['coord'][1]] = o['value']
        self.__recolor_later = []

    def __is_safe(self, _center):
        # now we're totally blind, we need to use explored_map!
        directions = [[0, 0], [0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, 0], [1, 1], [1, -1]]
        for direction in directions:
            if  _center[0] + direction[0] < 0 or _center[0] + direction[0] >= self.MAX_ROW or \
                _center[1] + direction[1] < 0 or _center[1] + direction[1] >= self.MAX_COL or \
                self.explored_map[_center[0] + direction[0]][_center[1] + direction[1]] == 2:
                # self.explored_map[_center[0] + direction[0]][_center[1] + direction[1]] == 1:
                return False
        return True

    def action(self, action, mark_value = 8):
        if action:
            if action == FORWARD or action.isdigit() or action.islower():
                times = int(action, 16)
                print(times)
                for i in range(times):
                    self.forward(mark_value)
            elif action == LEFT or action == RIGHT:
                self.rotate(action)
        zope.event.notify(action)

    def forward(self, mark_value = 8):
        self.__clear_marks()
        self.__mark_surroundings(self.start, 6)
        self.__mark_surroundings(self.goal, 7)
        if mark_value >= 0:
            self.explored_map[self.current[0]][self.current[1]] = mark_value

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
        self.__mark_robot()

    def alignment(self):
        # return list of alignment actions. Empty list means no alignment required
        if (self.sensors[0][0] == 2 or self.sensors[0][0] == 3) and (self.sensors[2][0] == 2 or self.sensors[2][0] == 3)  and (self.sensors[3][0] == 2 or self.sensors[3][0] == 3) and (self.sensors[5][0] == 2 or self.sensors[5][0] == 3):
            return [FD_ALIGN, LD_ALIGN, LA_ALIGN]
        elif(self.sensors[0][0] == 2 or self.sensors[0][0] == 3) and (self.sensors[2][0] == 2 or self.sensors[2][0] == 3):
            return [FA_ALIGN, FD_ALIGN]
        elif(self.sensors[3][0] == 2 or self.sensors[3][0] == 3) and (self.sensors[5][0] == 2 or self.sensors[5][0] == 3):
            return [LD_ALIGN, LA_ALIGN]
        else:
            return []

    def parse_sensors(self, sensorString):
        def represent_float(s):
            try: 
                float(s)
                return True
            except ValueError:
                return False
        def convert_long_sensor_distance(sensorOffset, sensorValue):
            if ((sensorValue >=  sensorOffset - 2 + 0 * 10) and (sensorValue <  sensorOffset + 8 + 0 * 10)):
                return [2, None, None, None, None, None, None, None, None, None]
            elif ((sensorValue >=  sensorOffset - 2 + 1 * 10) and (sensorValue <  sensorOffset + 8 + 1 * 10)):
                return [1, 2, None, None, None, None, None, None, None, None]
            elif ((sensorValue >=  sensorOffset - 2 + 2 * 10) and (sensorValue <  sensorOffset + 8 + 2 * 10)):
                return [1, 1, 2, None, None, None, None, None, None, None]
            elif ((sensorValue >=  sensorOffset - 2 + 3 * 10) and (sensorValue <  sensorOffset + 8 + 3 * 10)):
                return [1, 1, 1, 2, None, None, None, None, None, None]
            elif ((sensorValue >=  sensorOffset - 2 + 4 * 10) and (sensorValue <  sensorOffset + 8 + 4 * 10)):
                return [1, 1, 1, 1, 2, None, None, None, None, None]
            elif ((sensorValue >=  sensorOffset - 2 + 5 * 10) and (sensorValue <  sensorOffset + 8 + 5 * 10)):
                return [1, 1, 1, 1, 1, 2, None, None, None, None]
            elif ((sensorValue >=  sensorOffset - 2 + 6 * 10) and (sensorValue <  sensorOffset + 8 + 6 * 10)):
                return [1, 1, 1, 1, 1, 1, 2, None, None, None]
            elif ((sensorValue >=  sensorOffset - 2 + 7 * 10) and (sensorValue <  sensorOffset + 8 + 7 * 10)):
                return [1, 1, 1, 1, 1, 1, 1, 2, None, None]
            elif ((sensorValue >=  sensorOffset - 2 + 8 * 10) and (sensorValue <  sensorOffset + 8 + 8 * 10)):
                return [1, 1, 1, 1, 1, 1, 1, 1, 2, None]
            elif ((sensorValue >=  sensorOffset - 2 + 9 * 10) and (sensorValue <  sensorOffset + 8 + 9 * 10)):
                return [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
            elif (sensorValue >=  sensorOffset - 2 + 10 * 10):
                return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        def convert_short_sensor_distance(sensorValueStr):
            if represent_float(sensorValueStr):
                sensorValue = float(sensorValueStr)
                if ((sensorValue >=  0) and (sensorValue <  6)):
                    return [2, None, None, None] #5 - 14
                elif ((sensorValue >=  6) and (sensorValue <  16)):
                    return [1, 2, None, None] #15 - 24
                elif ((sensorValue >=  16) and (sensorValue <  26)):
                    return [1, 1, 2, 0] #25 - 34
                elif ((sensorValue >=  26) and (sensorValue <  36)):
                    return [1, 1, 1, 2] #35 - 44
                elif (sensorValue >=  36):
                    return [1, 1, 1, 1] #45

        sensors = []
        #for i in range(6):
        #    sensors.append([])
        #    for j in range(4):
        #       sensors[i].append(None)

        sensorList = sensorString.split(",")

        # FL
        sensors.append(convert_short_sensor_distance(sensorList[0]))
        # FM
        sensors.append(convert_short_sensor_distance(sensorList[1]))
        # FR
        sensors.append(convert_short_sensor_distance(sensorList[2]))
        # LT
        sensors.append(convert_short_sensor_distance(sensorList[3]))
        # RT
        sensors.append(convert_short_sensor_distance(sensorList[4]))
        # LB
        sensors.append(convert_short_sensor_distance(sensorList[5]))

        self.sensors = sensors
        return sensors

    def update_map(self):
        def upd(y, x, sensorValue):
            if sensorValue:
                self.explored_map[y][x] = sensorValue

        # FL
        for i in range(4):
            if self.direction == NORTH:
                upd(self.current[0] - i - 2, self.current[1] - 1, self.sensors[0][i])
            elif self.direction == EAST:
                upd(self.current[0] - 1 , self.current[1] + i + 2, self.sensors[0][i])
            elif self.direction == WEST:
                upd(self.current[0] + 1, self.current[1] - i - 2, self.sensors[0][i])
            else: # self.direction == SOUTH:
                upd(self.current[0] + i + 2, self.current[1] + 1, self.sensors[0][i])

        # FM
        for i in range(4):
            if self.direction == NORTH:
                upd(self.current[0] - i - 2, self.current[1], self.sensors[1][i])
            elif self.direction == EAST:
                upd(self.current[0], self.current[1] + i + 2, self.sensors[1][i])
            elif self.direction == WEST:
                upd(self.current[0], self.current[1] - i - 2, self.sensors[1][i])
            else: # self.direction == SOUTH:
                upd(self.current[0] + i + 2, self.current[1], self.sensors[1][i])

        # FR
        for i in range(4):
            if self.direction == NORTH:
                upd(self.current[0] - i - 2, self.current[1] + 1, self.sensors[2][i])
            elif self.direction == EAST:
                upd(self.current[0] + 1, self.current[1] + i + 2, self.sensors[2][i])
            elif self.direction == WEST:
                upd(self.current[0] - 1, self.current[1] - i - 2, self.sensors[2][i])
            else: # self.direction == SOUTH:
                upd(self.current[0] + i + 2, self.current[1] - 1, self.sensors[2][i])

        
        # LT
        for i in range(4):
            if self.direction == NORTH:
                upd(self.current[0] - 1, self.current[1] - i - 2, self.sensors[3][i])
            elif self.direction == EAST:
                upd(self.current[0] - i - 2, self.current[1] + 1, self.sensors[3][i])
            elif self.direction == WEST:
                upd(self.current[0] + i + 2, self.current[1] - 1, self.sensors[3][i])
            else: # self.direction == SOUTH:
                upd(self.current[0] + 1, self.current[1] + i + 2, self.sensors[3][i])


        # RT
        for i in range(4):
            if self.direction == NORTH:
                upd(self.current[0] - 1, self.current[1] + i + 2, self.sensors[4][i])
            elif self.direction == EAST:
                upd(self.current[0] + i + 2, self.current[1] + 1, self.sensors[4][i])
            elif self.direction == WEST:
                upd(self.current[0] - i - 2, self.current[1] - 1, self.sensors[4][i])
            else: # self.direction == SOUTH:
                upd(self.current[0] + 1, self.current[1] - i - 2, self.sensors[4][i])


        
        # LB
        for i in range(4):
            if self.direction == NORTH:
                upd(self.current[0] + 1, self.current[1] - i - 2, self.sensors[5][i])
            elif self.direction == EAST:
                upd(self.current[0] - i - 2, self.current[1] - 1, self.sensors[5][i])
            elif self.direction == WEST:
                upd(self.current[0] + i + 2, self.current[1] + 1, self.sensors[5][i])
            else: # self.direction == SOUTH:
                upd(self.current[0] - 1, self.current[1] + i + 2, self.sensors[5][i])

        zope.event.notify("SENSOR")
        return self.explored_map

    def descriptor_one(self):
        ret = [1, 1]
        for row in reversed(self.explored_map):
            for col in row:
                if col > 0:
                    ret.append(1)
                else:
                    ret.append(0)
        ret.append(1)
        ret.append(1)

        # print(ret)
        # print(len(ret))
        hex_ret = []
        temp = []
        for bit in ret:
            if len(temp) < 4:
                temp.append(bit)
            else:
                temp_str = ''.join([str(b) for b in temp])
                hex_ret.append(str(hex(int(temp_str, 2)))[2:])
                temp = [bit]
        if len(temp) > 0:
            temp_str = ''.join([str(b) for b in temp])
            hex_ret.append(str(hex(int(temp_str, 2)))[2:])

        # print(hex_ret)
        # print(len(hex_ret))

        return ''.join([h for h in hex_ret])

    def descriptor_two(self):
        ret = []
        cnt = 0
        for row in reversed(self.explored_map):
            for col in row:
                if col > 0:
                    cnt += 1
                    if col == 2:
                        ret.append(1)
                    else:
                        ret.append(0)
        while cnt % 8 != 0:
            ret.append(0)
            cnt += 1

        # print(ret)
        # print(len(ret))
        hex_ret = []
        temp = []
        for bit in ret:
            if len(temp) < 4:
                temp.append(bit)
            else:
                temp_str = ''.join([str(b) for b in temp])
                hex_ret.append(str(hex(int(temp_str, 2)))[2:])
                temp = [bit]
        if len(temp) > 0:
            temp_str = ''.join([str(b) for b in temp])
            hex_ret.append(str(hex(int(temp_str, 2)))[2:])
        
        # print(hex_ret)
        # print(len(hex_ret))

        return ''.join([h for h in hex_ret])