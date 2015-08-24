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
INF = 2 << 64

def find_centre(coords):
    avg_coord = [0, 0]
    for coord in coords:
        avg_coord[0] += coord[0]
        avg_coord[1] += coord[1]
    avg_coord[0] = int(avg_coord[0] / len(coords))
    avg_coord[1] = int(avg_coord[1] / len(coords))

    return avg_coord
def expand(map, head):
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    ret = []
    for direction in directions:
        if 0 <= direction[0] + head[0] < len(map) and 0 <= direction[1] + head[1] < len (map[0]):
            ret.append([direction[0] + head[0], direction[1] + head[1]])
    return ret

def cost(_from, _to):
    return 1

def shortest_path(map):
    # determine start and goal
    start = []
    goal = []
    dist = []
    for i in range(len(map)):
        dist.append([])
        for j in range(len(map[i])):
            if map[i][j] == 6:
                start.append([i, j])
            elif map[i][j] == 7:
                goal.append([i, j])
            dist[i].append(INF)
    avg_start = find_centre(start)
    avg_goal = find_centre(goal)
    # note that it will be (y, x)
    # print(dist)

    # do Dijkstra/UCS or A*
    pq = PriorityQueue() 
    pq.put(avg_start)
    dist[avg_start[0]][avg_start[1]] = 0

    while not pq.empty():
        head = pq.get()
        # expand head
        neighbors = expand(map, head)

        # if not yet visited OR can be visited with lower cost, put in pq
        for neighbor in neighbors:
            if dist[head[0]][head[1]] + cost(head, neighbor) < dist[neighbor[0]][neighbor[1]]:
                pq.put(neighbor)
                dist[neighbor[0]][neighbor[1]] = dist[head[0]][head[1]] + cost(head, neighbor)
    
    print(dist)
    # return a map


shortest_path([[6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7], [6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7], [6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7]])