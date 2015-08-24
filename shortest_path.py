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
class ShortestPath(object):
    """docstring for ShortestPath"""
    INF = 2 << 64

    def __init__(self, map):
        super(ShortestPath, self).__init__()
        self.map = map

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

    def cost(self, _from, _to):
        return 1

    def shortest_path(self):
        # determine start and goal
        start = []
        goal = []
        dist = [] # for each cell, how far is it from the start?
        prev = [] # for each cell, what is its parent?
        for i in range(len(self.map)):
            dist.append([])
            prev.append([])
            for j in range(len(self.map[i])):
                if self.map[i][j] == 6:
                    start.append([i, j])
                elif self.map[i][j] == 7:
                    goal.append([i, j])
                dist[i].append(self.INF)
                prev[i].append([-1, -1])
        avg_start = self.find_centre(start)
        avg_goal = self.find_centre(goal)
        # note that it will be (y, x)

        # do Dijkstra/UCS or A*
        pq = PriorityQueue() 
        pq.put(avg_start)
        dist[avg_start[0]][avg_start[1]] = 0

        while not pq.empty():
            head = pq.get()
            # expand head
            neighbors =  self.expand(head)

            # if not yet visited OR can be visited with lower cost, put in pq
            for neighbor in neighbors:
                if dist[head[0]][head[1]] +  self.cost(head, neighbor) < dist[neighbor[0]][neighbor[1]]:
                    pq.put(neighbor)
                    dist[neighbor[0]][neighbor[1]] = dist[head[0]][head[1]] +  self.cost(head, neighbor)
                    prev[neighbor[0]][neighbor[1]] = head
        

        # construct path from goal
        cur = avg_goal
        ret_map = self.map
        while cur[0] != avg_start[0] or cur[1] != avg_start[1]:
            # print('a', ret_map)
            ret_map[cur[0]][cur[1]] = 9
            cur = prev[cur[0]][cur[1]]
            if cur[0] == -1 and cur[1] == -1:
                break # no path possible

        # return a map
        return ret_map


x = ShortestPath([[6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7], [6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7], [6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7]])
print(x.shortest_path())