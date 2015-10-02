from shortest_path import ShortestPath
from constants import *
import random

class Exploration(object):
    """docstring for Exploration"""

    realTimeMap = []
    sensorList = []
    pathTaken = []
    repeatedArea = 0
    robotPrevMovement = "O"
    robotCurMovement = "O"

    robotCenterX = 1
    robotCenterY = 18
    robotDirectionX = 1
    robotDirectionY = 17
    repeatedArea = 0
    exploredArea = 0
    cnt = 0
    robotBreak = False

    def __init__(self, _exploredPercentage):
        super(Exploration, self).__init__()
        global cnt
        cnt = 0

        global realTimeMap
        global sensorList
        global pathTaken
        global robotPrevMovement
        global robotCurMovement
        global robotCenterX
        global robotCenterY
        global robotDirectionX
        global robotDirectionY
        global repeatedArea
        global exploredPercentage
        global robotBreak
        global exploredArea
        global spCounter
        global spList
        global repeatedTreshold
        repeatedTreshold = 10# 30

        spList = []
        spCounter = 0
        robotBreak = False
        exploredArea = 0
        exploredPercentage = _exploredPercentage
        
        # realTimeMap[0] = bottom row
        # realTimeMap[19] = top row
        realTimeMap = []
        
        # sensorList[0] = direction of robot (W-Facing up, S-Facing down, A-facing left, D-facing right)
        # sensorList[1] = frontleft
        # sensorList[2] = frontcenter
        # sensorList[3] = frontright
        # sensorList[4] = left
        # sensorList[5] = right
        # sensorList[6] = bottomleft
        sensorList = []
        pathTaken = []
        
        repeatedArea = 0
        robotPrevMovement = "O"
        robotCurMovement = "O"
        
        robotCenterX = 1
        robotCenterY = 18
        robotDirectionX = 1
        robotDirectionY = 17

        for i in range (0,20):
            Row = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            realTimeMap.append(Row)
        
        # set robot initial position as explored
        directions = [[0, 0], [0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, 0], [1, 1], [1, -1]]
        for direction in directions:
            realTimeMap[robotCenterY + direction[0]][robotCenterX + direction[1]] = 1


    def main(self, sensors, explored_map):
        def normalizeY(i):
            if 0 <= i <= 19:
                return i
            elif i < 0:
                return 0
            else:
                return 19
        def normalizeX(j):
            if 0 <= j <= 14:
                return j
            elif j < 0:
                return 0
            else:
                return 14
        def manhattan(_from, _to):
            return abs(_from[0] - _to[0]) + abs(_from[1] - _to[1])
        def okay(i, j):
            global realTimeMap
            global robotCenterX
            global robotCenterY
            if realTimeMap[i][j] == 0 or realTimeMap[i][j] == 2:
                return -INF
            directions = [[0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, 0], [1, 1], [1, -1]]
            for direction in directions:
                if realTimeMap[i + direction[0]][j + direction[1]] == 2:
                    return -INF
            

            directions = [[0, 2], [1, 2], [-1, 2], [0, -2], [1, -2], [-1, -2], [-2, 0], [-2, 1], [-2, -1], [2, 0], [2, -1], [2, 1]]
            dist = manhattan([robotCenterY, robotCenterX], [i, j])
            cnt = 0
            for direction in directions:
                temp = realTimeMap[normalizeY(i + direction[0])][normalizeX(j + direction[1])]
                if temp == 0:
                    cnt += 2
            return cnt * cnt * cnt - dist



        global realTimeMap
        global sensorList
        global pathTaken
        global robotCenterX
        global robotPrevMovement
        global robotCurMovement
        global robotCenterX
        global robotCenterY
        global robotDirectionX
        global robotDirectionY
        global repeatedArea
        global exploredPercentage
        global robotBreak
        global exploredArea

        global spList
        global spCounter
        global repeatedTreshold
        

        
        for i in range(20):
            for j in range(15):
                if explored_map[i][j] == 4:
                    robotDirectionY = i
                    robotDirectionX = j
                elif explored_map[i][j] == 5:
                    robotCenterY = i
                    robotCenterX = j

        for i in range(20):
            for j in range(15):
                val = explored_map[i][j]
                if val >= 3:
                    val = 1

                realTimeMap[i][j] = val
        
        #set robot starting position
        realTimeMap[robotCenterY][robotCenterX] = 5
        realTimeMap[robotDirectionY][robotDirectionX] = 4
        # print(robotCenterY, robotCenterX, ": ", robotDirectionY, robotDirectionX)
        
        if repeatedArea <= repeatedTreshold and exploredArea < exploredPercentage * 3: # exploredArea / 300 * 100 < exploredPercentage
            exploredArea = 0

            self.callAllMethods(sensors, explored_map)
            if len(spList) <= 0:
                for tup in pathTaken:
                    if tup == (robotCenterY, robotCenterX):
                        repeatedArea = repeatedArea + 1
                        break
            #x = []
            for i in range(0,20):
                for j in range(0,15):
                    if realTimeMap[i][j] != 0:
                        exploredArea = exploredArea + 1
                    #else:
                    #    x.append([i,j])
            #print(x)
            # print(repeatedArea, " ", exploredArea)
        else:
            robotCurMovement = None
            if exploredArea >= exploredPercentage * 3 or spCounter > 5:
                # good enough, break
                robotBreak = True
            else:
                # don't give up!
                rcurrent = [robotCenterY, robotCenterX]
                rdirection = NORTH

                if robotCenterY > robotDirectionY:
                    rdirection = NORTH
                elif robotCenterY < robotDirectionY:
                    rdirection = SOUTH
                elif robotCenterX < robotDirectionX:
                    rdirection = EAST
                elif robotCenterX > robotDirectionX:
                    rdirection = WEST

                dest = [10, 8]
                dest_candidate = []
                for i in range(1, 19):
                    for j in range(1, 14):
                        v = okay(i, j)
                        if v > -INF:
                            dest_candidate.append([[i, j], v])
                best_candidate_v = -INF
                best_candidate = [10, 8]
                for cand in dest_candidate:
                    if cand[1] > best_candidate_v:
                        best_candidate_v = cand[1]
                        best_candidate = cand[0]
                #print(dest_candidate)

                print("[Tornado] exploration.py > dest_candidate > %s" % (dest_candidate))
                dest = best_candidate

                sp = ShortestPath(realTimeMap, rdirection, rcurrent, dest)
                sp_list = sp.shortest_path(8)
                sp_sequence = sp_list['sequence']
                sp_sequence.reverse()
                spList = sp_sequence
                """
                print("--------------")
                print(rdirection)
                print(rcurrent)
                print(dest)
                print(spList)
                print("--------------")
                """
                #print(spList)
                print("[Tornado] exploration.py > spList > %s" % (spList))
                spCounter += 1
                repeatedArea = 0
                repeatedTreshold = 3

        # THIS IS THE CULPRIT, DO NOT MARK realTimeMap with 8 OR ELSE robotMovementAnalyses will fail :)
        # for tup in pathTaken:
        #   if realTimeMap[tup[0]][tup[1]] != 4 and realTimeMap[tup[0]][tup[1]] != 5:
        #       realTimeMap[tup[0]][tup[1]] = 8

    

    def callAllMethods(self, sensors, explored_map):
        global realTimeMap
        global sensorList
        global pathTaken
        global robotCenterX
        global robotPrevMovement
        global robotCurMovement
        global robotCenterX
        global robotCenterY
        global robotDirectionX
        global robotDirectionY
        
        sensorList = self.getSensor(robotCenterX, robotCenterY, robotDirectionX, robotDirectionY)
        sensors.insert(0, sensorList[0])
        sensorList = sensors


        for i in range(20):
            for j in range(15):
                val = explored_map[i][j]
                if val >= 3:
                    val = 1

                realTimeMap[i][j] = val

        #set robot starting position
        realTimeMap[robotCenterY][robotCenterX] = 5
        realTimeMap[robotDirectionY][robotDirectionX] = 4
        # realTimeMap = self.updateRealTimeMap(realTimeMap, sensorList, robotCenterX, robotCenterY)
        
        robotCurMovement = self.robotMovementAnalyses(realTimeMap, robotCenterX, robotCenterY, sensorList[0][0], robotPrevMovement, sensorList)
        robotPrevMovement = robotCurMovement
        if robotCurMovement == FORWARD:
            pathTaken.append((robotCenterY, robotCenterX))
        #print (robotCurMovement)
        # realTimeMap = self.executeRobotMovement(realTimeMap, robotCenterX, robotCenterY, sensorList[0][0], robotCurMovement)
        
        if sensorList[0][0] == NORTH:
            if robotCurMovement == RIGHT:
                robotDirectionX = robotDirectionX + 1
                robotDirectionY = robotDirectionY + 1
            elif robotCurMovement == FORWARD:
                robotCenterY = robotCenterY - 1
                robotDirectionY = robotDirectionY - 1
            elif robotCurMovement == LEFT:
                robotDirectionX = robotDirectionX - 1
                robotDirectionY = robotDirectionY + 1
        if sensorList[0][0] == SOUTH:
            if robotCurMovement == RIGHT:
                robotDirectionX = robotDirectionX - 1
                robotDirectionY = robotDirectionY - 1
            elif robotCurMovement == FORWARD:
                robotCenterY = robotCenterY + 1
                robotDirectionY = robotDirectionY + 1
            elif robotCurMovement == LEFT:
                robotDirectionX = robotDirectionX + 1
                robotDirectionY = robotDirectionY - 1
        if sensorList[0][0] == WEST:
            if robotCurMovement == RIGHT:
                robotDirectionX = robotDirectionX + 1
                robotDirectionY = robotDirectionY - 1
            elif robotCurMovement == FORWARD:
                robotCenterX = robotCenterX -1
                robotDirectionX = robotDirectionX - 1
            elif robotCurMovement == LEFT:
                robotDirectionX = robotDirectionX + 1
                robotDirectionY = robotDirectionY + 1
        if sensorList[0][0] == EAST:
            if robotCurMovement == RIGHT:
                robotDirectionX = robotDirectionX - 1
                robotDirectionY = robotDirectionY + 1
            elif robotCurMovement == FORWARD:
                robotCenterX = robotCenterX + 1
                robotDirectionX = robotDirectionX + 1
            elif robotCurMovement == LEFT:
                robotDirectionX = robotDirectionX - 1
                robotDirectionY = robotDirectionY - 1

            
    def getSensor(self, centerX, centerY, directionX, directionY):
        # returnValue[0] = direction of robot (W-Facing up, S-Facing down, A-facing left, D-facing right)
        # returnValue[1] = frontleft
        # returnValue[2] = frontcenter
        # returnValue[3] = frontright
        # returnValue[4] = left
        # returnValue[5] = right
        # returnValue[6] = bottomleft
        returnValue = []

        if (centerX == directionX) and (directionY < centerY):
            returnValue.append([NORTH])
        elif (centerX == directionX) and (directionY > centerY):
            returnValue.append([SOUTH])
        elif (centerY == directionY) and (directionX < centerX):
            returnValue.append([WEST])
        elif (centerY == directionY) and (directionX > centerX):
            returnValue.append([EAST])
        return returnValue

    def robotMovementAnalyses(self, realTimeMap, CenterX, CenterY, direction, prevMov, sensorList):

        def checkRealTimeMap(y, x):
            if 0 <= y < 20 and 0 <= x < 15 and realTimeMap[y][x] == 1:
                return True
            return False

        global spList
        if len(spList) > 0:
            resultMovement = spList.pop()
            return resultMovement

        if direction == NORTH:
            if sensorList[4][0] != None and checkRealTimeMap(CenterY-1, CenterX-2) and checkRealTimeMap(CenterY, CenterX-2) and checkRealTimeMap(CenterY+1, CenterX-2) and prevMov != LEFT:
                resultMovement = LEFT
            elif sensorList[1][0] != None and checkRealTimeMap(CenterY-2, CenterX-1) and checkRealTimeMap(CenterY-2, CenterX) and checkRealTimeMap(CenterY-2, CenterX+1):
                resultMovement = FORWARD
            elif sensorList[5][0] != None and checkRealTimeMap(CenterY-1, CenterX+2) and checkRealTimeMap(CenterY, CenterX+2) and checkRealTimeMap(CenterY+1, CenterX+2):
                resultMovement = RIGHT
            else:
                resultMovement = LEFT
        elif direction == SOUTH:
            if sensorList[4][0] != None and checkRealTimeMap(CenterY-1, CenterX+2) and checkRealTimeMap(CenterY, CenterX+2) and checkRealTimeMap(CenterY+1, CenterX+2) and prevMov != LEFT:
                resultMovement = LEFT
            elif sensorList[1][0] != None and checkRealTimeMap(CenterY+2, CenterX-1) and checkRealTimeMap(CenterY+2, CenterX) and checkRealTimeMap(CenterY+2, CenterX+1):
                resultMovement = FORWARD
            elif sensorList[5][0] != None and checkRealTimeMap(CenterY-1, CenterX-2) and checkRealTimeMap(CenterY, CenterX-2) and checkRealTimeMap(CenterY+1, CenterX-2):
                resultMovement = RIGHT
            else:
                resultMovement = LEFT
        elif direction == WEST:
            if sensorList[4][0] != None and checkRealTimeMap(CenterY+2, CenterX-1) and checkRealTimeMap(CenterY+2, CenterX) and checkRealTimeMap(CenterY+2, CenterX+1) and prevMov != LEFT:
                resultMovement = LEFT
            elif sensorList[1][0] != None and checkRealTimeMap(CenterY-1, CenterX-2) and checkRealTimeMap(CenterY, CenterX-2) and checkRealTimeMap(CenterY+1, CenterX-2):
                resultMovement = FORWARD
            elif sensorList[5][0] != None and checkRealTimeMap(CenterY-2, CenterX-1) and checkRealTimeMap(CenterY-2, CenterX) and checkRealTimeMap(CenterY-2, CenterX+1):
                resultMovement = RIGHT
            else:
                resultMovement = LEFT
        elif direction == EAST:
            if sensorList[4][0] != None and checkRealTimeMap(CenterY-2, CenterX-1) and checkRealTimeMap(CenterY-2, CenterX) and checkRealTimeMap(CenterY-2, CenterX+1) and prevMov != LEFT:
                resultMovement = LEFT
            elif sensorList[1][0] != None and checkRealTimeMap(CenterY-1, CenterX+2) and checkRealTimeMap(CenterY, CenterX+2) and checkRealTimeMap(CenterY+1, CenterX+2):
                resultMovement = FORWARD
            elif sensorList[5][0] != None and checkRealTimeMap(CenterY+2, CenterX-1) and checkRealTimeMap(CenterY+2, CenterX) and checkRealTimeMap(CenterY+2, CenterX+1):
                resultMovement = RIGHT
            else:
                resultMovement = LEFT
        return resultMovement
        
    def executeRobotMovement(self, realTimeMap, CenterX, CenterY, direction, movement):
        if direction == NORTH:
            if movement == RIGHT:
                realTimeMap[CenterY][CenterX+1] = 4
                realTimeMap[CenterY-1][CenterX] = 1
            elif movement == FORWARD:
                realTimeMap[CenterY][CenterX] = 1
                realTimeMap[CenterY-1][CenterX] = 5
                realTimeMap[CenterY-2][CenterX] = 4
            elif movement == LEFT:
                realTimeMap[CenterY][CenterX-1] = 4
                realTimeMap[CenterY-1][CenterX] = 1
        elif direction == SOUTH:
            if movement == RIGHT:
                realTimeMap[CenterY][CenterX-1] = 4
                realTimeMap[CenterY+1][CenterX] = 1
            elif movement == FORWARD:
                realTimeMap[CenterY][CenterX] = 1
                realTimeMap[CenterY+1][CenterX] = 5
                realTimeMap[CenterY+2][CenterX] = 4
            elif movement == LEFT:
                realTimeMap[CenterY][CenterX+1] = 4
                realTimeMap[CenterY+1][CenterX] = 1
        elif direction == WEST:
            if movement == RIGHT:
                realTimeMap[CenterY-1][CenterX] = 4
                realTimeMap[CenterY][CenterX-1] = 1
            elif movement == FORWARD:
                realTimeMap[CenterY][CenterX] = 1
                realTimeMap[CenterY][CenterX-1] = 5
                realTimeMap[CenterY][CenterX-2] = 4
            elif movement == LEFT:
                realTimeMap[CenterY+1][CenterX] = 4
                realTimeMap[CenterY][CenterX-1] = 1
        elif direction == EAST:
            if movement == RIGHT:
                realTimeMap[CenterY+1][CenterX] = 4
                realTimeMap[CenterY][CenterX+1] = 1
            elif movement == FORWARD:
                realTimeMap[CenterY][CenterX] = 1
                realTimeMap[CenterY][CenterX+1] = 5
                realTimeMap[CenterY][CenterX+2] = 4
            elif movement == LEFT:
                realTimeMap[CenterY-1][CenterX] = 4
                realTimeMap[CenterY][CenterX+1] = 1
        return realTimeMap
    

    def getRealTimeMap(self, sensors, explored_map):
        global cnt
        global realTimeMap
        global robotCurMovement
        global robotBreak
        global robotCenterX
        global robotCenterY
        #print(cnt + 1, "before: ",  robotCurMovement)
        self.main(sensors, explored_map)
        print("[Tornado] exploration.py > %d - %s : (%d, %d)" %(cnt + 1, robotCurMovement, robotCenterY, robotCenterX))
        cnt += 1
        return (robotCurMovement, robotBreak)