"""
- 0: unexplored
- 1: explored
- 2: obstacle
- 3: robot body
- 4: robot head
- 5: robot center
- 6: start
- 7: goal
- 8: explored path
- 9: optimum path
"""
from queue import PriorityQueue
from constants import *

class PqNode(object):
    def __init__(self, _dict):
        self.weight = _dict["weight"]
        self.direction = _dict["direction"]
        self.position = _dict["position"]
    def __lt__(self, rhs):
        return self["weight"] < rhs["weight"]
    def __gt__(self, rhs):
        return self["weight"] > rhs["weight"]
    def __le__(self, rhs):
        return self["weight"] <= rhs["weight"]
    def __ge__(self, rhs):
        return self["weight"] >= rhs["weight"]
    def __getitem__(self, key):
        return getattr(self, key)
    def __setitem__(self, key, value):
        setattr(self, key, value)

class ShortestPath(object):
    """docstring for ShortestPath"""

    def __init__(self, map, direction):
        super(ShortestPath, self).__init__()
        self.map = map
        # direction: N, E, W, S
        self.directon = direction
        # note: positive x --> E; positive y --> S
        # coord[0] is y
        # coord[1] is x

    def find_centre(self, coords):
        avg_coord = [0, 0]
        for coord in coords:
            avg_coord[0] += coord[0]
            avg_coord[1] += coord[1]
        avg_coord[0] = int(avg_coord[0] / len(coords))
        avg_coord[1] = int(avg_coord[1] / len(coords))
        return avg_coord

    def is_okay(self, coord):
        return self.map[coord[0]][coord[1]] != 0 and self.map[coord[0]][coord[1]] != 2

    def expand(self, head):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        ret = []
        for direction in directions:
            if 0 <= direction[0] + head[0] < len(self.map) and 0 <= direction[1] + head[1] < len (self.map[0]) and  self.is_okay([direction[0] + head[0], direction[1] + head[1]]):
                ret.append([direction[0] + head[0], direction[1] + head[1]])
        return ret
    def direction(self, _from, _to):
        if _to[0] - _from[0] > 0:
            return SOUTH
        elif _to[0] - _from[0] < 0:
            return NORTH
        else:
            if _to[1] - _from[1] > 0:
                return EAST
            else:
                return WEST
    def action(self, _from, _to, _current_direction):
        # actions are: L (left), R (right), F (forward)
        if _current_direction == SOUTH:
            if _to[0] - _from[0] < 0:
                return [LEFT, LEFT, FORWARD]
            elif _to[0] - _from[0] == 0:
                if _to[1] - _from[1] > 0:
                    return [LEFT, FORWARD]
                else:
                    return [RIGHT, FORWARD]
        elif _current_direction == EAST:
            if _to[1] - _from[1] < 0:
                return [LEFT, LEFT, FORWARD]
            elif _to[1] - _from[1] == 0:
                if _to[0] - _from[0] > 0:
                    return [LEFT, FORWARD]
                else:
                    return [RIGHT, FORWARD]
        elif _current_direction == NORTH:
            if _to[0] - _from[0] > 0:
                return [LEFT, LEFT, FORWARD]
            elif _to[0] - _from[0] == 0:
                if _to[1] - _from[1] > 0:
                    return [RIGHT, FORWARD]
                else:
                    return [LEFT, FORWARD]
        elif _current_direction == WEST:
            if _to[1] - _from[1] > 0:
                return [LEFT, LEFT, FORWARD]
            elif _to[1] - _from[1] == 0:
                if _to[0] - _from[0] > 0:
                    return [LEFT, FORWARD]
                else:
                    return [RIGHT, FORWARD]
        return [FORWARD]
    def cost(self, _from, _to, _current_direction):
        # can be the heuristic function
        # if going backward of current direction, cost = 3
        # if going to turn left or right, cost = 2
        # else cost = 1
        return len(self.action(_from, _to, _current_direction))

    def shortest_path(self):
        # determine start and goal
        start = []
        goal = []
        dist = [] # for each cell, how far is it from the start?
        prev = [] # for each cell, what is its parent?
        next_post = [] # for each cell in optimized path, what is the next position?
        for i in range(len(self.map)):
            dist.append([])
            prev.append([])
            next_post.append([])
            for j in range(len(self.map[i])):
                if self.map[i][j] == 6:
                    start.append([i, j])
                elif self.map[i][j] == 7:
                    goal.append([i, j])
                dist[i].append(INF)
                prev[i].append([-1, -1])
                next_post[i].append([-1, -1])
        avg_start = self.find_centre(start)
        avg_goal = self.find_centre(goal)
        # note that it will be (y, x)

        # do Dijkstra/UCS or A*
        pq = PriorityQueue() 
        pq.put(PqNode({"position": avg_start, "direction": self.direction, "weight": 0}))
        dist[avg_start[0]][avg_start[1]] = 0

        while not pq.empty():
            head = pq.get()
            # expand head
            neighbors =  self.expand(head["position"])

            # if not yet visited OR can be visited with lower cost, put in pq
            for neighbor in neighbors:
                cost = self.cost(head["position"], neighbor, head["direction"])
                if dist[head["position"][0]][head["position"][1]] + cost < dist[neighbor[0]][neighbor[1]]:
                    
                    dist[neighbor[0]][neighbor[1]] = dist[head["position"][0]][head["position"][1]] + cost
                    prev[neighbor[0]][neighbor[1]] = head["position"]
                    pq.put(PqNode({"position": neighbor, "direction": self.direction(head["position"], neighbor), "weight": dist[neighbor[0]][neighbor[1]]}))

        # construct path from goal
        cur = avg_goal
        ret_map = self.map
        while cur[0] != avg_start[0] or cur[1] != avg_start[1]:
            # print('a', ret_map)
            ret_map[cur[0]][cur[1]] = 9
            prev_post = prev[cur[0]][cur[1]]
            next_post[prev_post[0]][prev_post[1]] = [cur[0], cur[1]]
            cur = prev_post
            if cur[0] == -1 and cur[1] == -1:
                break # no path possible
        
        # consruct direction from start
        cur = avg_start
        cur_dir = self.directon
        ret_seq = []
        while cur[0] != avg_goal[0] or cur[1] != avg_goal[1]:
            next_coord = next_post[cur[0]][cur[1]]
            for x in self.action(cur, next_coord, cur_dir):
                ret_seq.append(x)
            cur_dir = self.direction(cur, next_coord)
            cur = next_coord

        # return sequence of actions and the map
        return {
            "sequence": ret_seq,
            "map": ret_map
        }

if __name__ == '__main__':
    x = ShortestPath([[6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7], [6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7], [6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7]], NORTH)
    print(x.shortest_path())