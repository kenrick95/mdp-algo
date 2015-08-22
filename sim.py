class Robot(object):
    """docstring for Robot"""
    def __init__(self, arg):
        super(Robot, self).__init__()
        self.arg = arg
        self.start = {x: 1, y: 1}
        self.goal = {x: 13, y: 18}
        self.current = {x: 1, y: 1, direction: NORTH}

    def rotate(self, direction):
        if direction > 0: # clockwise
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

    def get_sensors(self):
        

# define map

# read map from file

# get_sensors

# move_forward

# rotate