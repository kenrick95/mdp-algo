from shortest_path import ShortestPath
from constants import *
import random

class Exploration(object):
    """docstring for Exploration"""

    realTimeMap = []
    simulatorMap = []
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
        global simulatorMap
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
        spList = []
        spCounter = 0
        robotBreak = False
        exploredArea = 0
        exploredPercentage = _exploredPercentage
        
        # realTimeMap[0] = bottom row
        # realTimeMap[19] = top row
        realTimeMap = []
        
        # simulatorMap[0] = bottom row
        # simulatorMap[19] = top row
        simulatorMap = []
        
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


        simulatorMap = self.simulatorReadMap()


    def main(self, sensors):
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
        global simulatorMap
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
        
        #set robot starting position
        realTimeMap[robotCenterY][robotCenterX] = 5
        realTimeMap[robotDirectionY][robotDirectionX] = 4
        # print(robotCenterY, robotCenterX, ": ", robotDirectionY, robotDirectionX)
        
        if repeatedArea <= 30 and exploredArea < exploredPercentage * 3: # exploredArea / 300 * 100 < exploredPercentage
            exploredArea = 0

            self.callAllMethods(sensors)
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
                        if v > -100000007:
                            dest_candidate.append([[i, j], v])
                best_candidate_v = -100000007
                best_candidate = [10, 8]
                for cand in dest_candidate:
                    if cand[1] > best_candidate_v:
                        best_candidate_v = cand[1]
                        best_candidate = cand[0]
                print(dest_candidate)
                dest = best_candidate

                sp = ShortestPath(realTimeMap, rdirection, rcurrent, dest)
                sp_list = sp.shortest_path(8)
                sp_sequence = sp_list['sequence']
                #sp_sequence.reverse()
                spList = sp_sequence
                """
                print("--------------")
                print(rdirection)
                print(rcurrent)
                print(dest)
                print(spList)
                print("--------------")
                """
                print(spList)
                spCounter += 1
                repeatedArea = 0

        # THIS IS THE CULPRIT, DO NOT MARK realTimeMap with 8 OR ELSE robotMovementAnalyses will fail :)
        # for tup in pathTaken:
        #   if realTimeMap[tup[0]][tup[1]] != 4 and realTimeMap[tup[0]][tup[1]] != 5:
        #       realTimeMap[tup[0]][tup[1]] = 8

    

    def callAllMethods(self, sensors):
        global realTimeMap
        global simulatorMap
        global sensorList
        global pathTaken
        global robotCenterX
        global robotPrevMovement
        global robotCurMovement
        global robotCenterX
        global robotCenterY
        global robotDirectionX
        global robotDirectionY
        
        sensorList = self.getSensor(simulatorMap, robotCenterX, robotCenterY, robotDirectionX, robotDirectionY)
        sensors.insert(0, sensorList[0])
        sensorList = sensors

        realTimeMap = self.updateRealTimeMap(realTimeMap, sensorList, robotCenterX, robotCenterY)
        
        robotCurMovement = self.robotMovementAnalyses(realTimeMap, robotCenterX, robotCenterY, sensorList[0][0], robotPrevMovement, sensorList)
        robotPrevMovement = robotCurMovement
        if robotCurMovement == FORWARD:
            pathTaken.append((robotCenterY, robotCenterX))
        #print (robotCurMovement)
        realTimeMap = self.executeRobotMovement(realTimeMap, robotCenterX, robotCenterY, sensorList[0][0], robotCurMovement)
        
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

            
    def getSensor(self, simMap, centerX, centerY, directionX, directionY):
        # returnValue[0] = direction of robot (W-Facing up, S-Facing down, A-facing left, D-facing right)
        # returnValue[1] = frontleft
        # returnValue[2] = frontcenter
        # returnValue[3] = frontright
        # returnValue[4] = left
        # returnValue[5] = right
        # returnValue[6] = bottomleft
        returnValue = []
        outOfBoundLeft = 0
        outOfBoundRight = 0
        outOfBoundUp = 0
        outOfBoundDown = 0
        
        if centerX <= 4:
            if centerX == 1:
                outOfBoundLeft = 4
            elif centerX == 2:
                outOfBoundLeft = 3
            elif centerX == 3:
                outOfBoundLeft = 2
            elif centerX == 4:
                outOfBoundLeft = 1
        if centerX >= 10:
            if centerX == 13:
                outOfBoundRight = 4
            elif centerX == 12:
                outOfBoundRight = 3
            elif centerX == 11:
                outOfBoundRight = 2
            elif centerX == 10:
                outOfBoundRight = 1
        if centerY <= 4:
            if centerY == 1:
                outOfBoundUp = 4
            elif centerY == 2:
                outOfBoundUp = 3
            elif centerY == 3:
                outOfBoundUp = 2
            elif centerY == 4:
                outOfBoundUp = 1
        if centerY >= 15:
            if centerY == 18:
                outOfBoundDown = 4
            elif centerY == 17:
                outOfBoundDown = 3
            elif centerY == 16:
                outOfBoundDown = 2
            elif centerY == 15:
                outOfBoundDown = 1
        
        #U-Facing up
        if (centerX == directionX) and (directionY < centerY):
            returnValue.append([NORTH])
        #D-Facing down
        elif (centerX == directionX) and (directionY > centerY):
            returnValue.append([SOUTH])
        #L-facing left
        elif (centerY == directionY) and (directionX < centerX):
            returnValue.append([WEST])
        #R-facing right
        elif (centerY == directionY) and (directionX > centerX):
            returnValue.append([EAST])
        return returnValue
        
        """
        #get sensor value from simulator map
        if returnValue[0][0] == NORTH:            
            returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX-1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX-1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX-1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX-1]])
            returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX]])
            returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX+1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX+1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX+1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX+1]])
            returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY-1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY-1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY-1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY-1][centerX-5]])
            returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY-1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY-1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY-1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY-1][centerX+5]])
            returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY+1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY+1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY+1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY+1][centerX-5]])
        elif returnValue[0][0] == SOUTH:
            returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX+1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX+1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX+1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX+1]])
            returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX]])
            returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX-1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX-1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX-1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX-1]])
            returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY+1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY+1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY+1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY+1][centerX+5]])
            returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY+1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY+1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY+1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY+1][centerX-5]])
            returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY-1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY-1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY-1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY-1][centerX+5]])
        elif returnValue[0][0] == WEST:
            returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY+1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY+1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY+1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY+1][centerX-5]])
            returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY][centerX-5]])
            returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY-1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY-1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY-1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY-1][centerX-5]])
            returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX-1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX-1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX-1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX-1]])
            returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX-1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX-1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX-1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX-1]])
            returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX+1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX+1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX+1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX+1]])
        elif returnValue[0][0] == EAST:
            returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY-1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY-1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY-1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY-1][centerX+5]])
            returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY][centerX+5]])
            returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY+1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY+1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY+1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY+1][centerX+5]])
            returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX+1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX+1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX+1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX+1]])
            returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX+1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX+1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX+1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX+1]])
            returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX-1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX-1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX-1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX-1]])
            
        return returnValue
        """
        
    def updateRobotPosition(self, realTimeMap, robotCenterX, robotCenterY, robotDirectionX, robotDirectionY):
        realTimeMap[robotCenterY][robotCenterX] = 5
        realTimeMap[robotDirectionY][robotDirectionX] = 4
        return realTimeMap
        
    def simulatorReadMap(self):
        simulatorMap = []
        for line in list(open("Simulator Real Map.txt","r")):
            oneRow = []
            count = 1
            for num in line:
                if count > 15:
                    break
                oneRow.append(int(num))
                count = count + 1
            simulatorMap.append(oneRow)
        print("Done")
        return simulatorMap
        
    def updateRealTimeMap(self, realTimeMap, sensorList, centerX, centerY):
        if sensorList[0][0] == NORTH:
            #front left
            if sensorList[1][0] != None :realTimeMap[centerY-2][centerX-1] = sensorList[1][0]
            if sensorList[1][0] != 2:
                if sensorList[1][1] != None :realTimeMap[centerY-3][centerX-1] = sensorList[1][1]
                if sensorList[1][1] != 2:
                    if sensorList[1][2] != None :realTimeMap[centerY-4][centerX-1] = sensorList[1][2]
                    if sensorList[1][2] != 2:
                        if sensorList[1][3] != None :realTimeMap[centerY-5][centerX-1] = sensorList[1][3]
            #front center
            if sensorList[2][0] != None :realTimeMap[centerY-2][centerX] = sensorList[2][0]
            if sensorList[2][0] != 2:
                if sensorList[2][1] != None :realTimeMap[centerY-3][centerX] = sensorList[2][1]
                if sensorList[2][1] != 2:
                    if sensorList[2][2] != None :realTimeMap[centerY-4][centerX] = sensorList[2][2]
                    if sensorList[2][2] != 2:
                        if sensorList[2][3] != None :realTimeMap[centerY-5][centerX] = sensorList[2][3]
            #front right
            if sensorList[3][0] != None :realTimeMap[centerY-2][centerX+1] = sensorList[3][0]
            if sensorList[3][0] != 2:
                if sensorList[3][1] != None :realTimeMap[centerY-3][centerX+1] = sensorList[3][1]
                if sensorList[3][1] != 2:
                    if sensorList[3][2] != None :realTimeMap[centerY-4][centerX+1] = sensorList[3][2]
                    if sensorList[3][2] != 2:
                        if sensorList[3][3] != None :realTimeMap[centerY-5][centerX+1] = sensorList[3][3]
            #left
            if sensorList[4][0] != None :realTimeMap[centerY-1][centerX-2] = sensorList[4][0]
            if sensorList[4][0] != 2:
                if sensorList[4][1] != None :realTimeMap[centerY-1][centerX-3] = sensorList[4][1]
                if sensorList[4][1] != 2:
                    if sensorList[4][2] != None :realTimeMap[centerY-1][centerX-4] = sensorList[4][2]
                    if sensorList[4][2] != 2:
                        if sensorList[4][3] != None :realTimeMap[centerY-1][centerX-5] = sensorList[4][3]
            #right
            if sensorList[5][0] != None :realTimeMap[centerY-1][centerX+2] = sensorList[5][0]
            if sensorList[5][0] != 2:
                if sensorList[5][1] != None :realTimeMap[centerY-1][centerX+3] = sensorList[5][1]
                if sensorList[5][1] != 2:
                    if sensorList[5][2] != None :realTimeMap[centerY-1][centerX+4] = sensorList[5][2]
                    if sensorList[5][2] != 2:
                        if sensorList[5][3] != None :realTimeMap[centerY-1][centerX+5] = sensorList[5][3]
            #bottom left
            if sensorList[6][0] != None :realTimeMap[centerY+1][centerX-2] = sensorList[6][0]
            if sensorList[6][0] != 2:
                if sensorList[6][1] != None :realTimeMap[centerY+1][centerX-3] = sensorList[6][1]
                if sensorList[6][1] != 2:
                    if sensorList[6][2] != None :realTimeMap[centerY+1][centerX-4] = sensorList[6][2]
                    if sensorList[6][2] != 2:
                        if sensorList[6][3] != None :realTimeMap[centerY+1][centerX-5] = sensorList[6][3]
        elif sensorList[0][0] == SOUTH:
            if sensorList[1][0] != None :realTimeMap[centerY+2][centerX+1] = sensorList[1][0]
            if sensorList[1][0] != 2:
                if sensorList[1][1] != None :realTimeMap[centerY+3][centerX+1] = sensorList[1][1]
                if sensorList[1][1] != 2:
                    if sensorList[1][2] != None :realTimeMap[centerY+4][centerX+1] = sensorList[1][2]
                    if sensorList[1][2] != 2:
                        if sensorList[1][3] != None :realTimeMap[centerY+5][centerX+1] = sensorList[1][3]
            
            if sensorList[2][0] != None :realTimeMap[centerY+2][centerX] = sensorList[2][0]
            if sensorList[2][0] != 2:
                if sensorList[2][1] != None :realTimeMap[centerY+3][centerX] = sensorList[2][1]
                if sensorList[2][1] != 2:
                    if sensorList[2][2] != None :realTimeMap[centerY+4][centerX] = sensorList[2][2]
                    if sensorList[2][2] != 2:
                        if sensorList[2][3] != None :realTimeMap[centerY+5][centerX] = sensorList[2][3]
            
            if sensorList[3][0] != None :realTimeMap[centerY+2][centerX-1] = sensorList[3][0]
            if sensorList[3][0] != 2:
                if sensorList[3][1] != None :realTimeMap[centerY+3][centerX-1] = sensorList[3][1]
                if sensorList[3][1] != 2:
                    if sensorList[3][2] != None :realTimeMap[centerY+4][centerX-1] = sensorList[3][2]
                    if sensorList[3][2] != 2:
                        if sensorList[3][3] != None :realTimeMap[centerY+5][centerX-1] = sensorList[3][3]
            
            if sensorList[4][0] != None :realTimeMap[centerY+1][centerX+2] = sensorList[4][0]
            if sensorList[4][0] != 2:
                if sensorList[4][1] != None :realTimeMap[centerY+1][centerX+3] = sensorList[4][1]
                if sensorList[4][1] != 2:
                    if sensorList[4][2] != None :realTimeMap[centerY+1][centerX+4] = sensorList[4][2]
                    if sensorList[4][2] != 2:
                        if sensorList[4][3] != None :realTimeMap[centerY+1][centerX+5] = sensorList[4][3]
            
            if sensorList[5][0] != None :realTimeMap[centerY+1][centerX-2] = sensorList[5][0]
            if sensorList[5][0] != 2:
                if sensorList[5][1] != None :realTimeMap[centerY+1][centerX-3] = sensorList[5][1]
                if sensorList[5][1] != 2:
                    if sensorList[5][2] != None :realTimeMap[centerY+1][centerX-4] = sensorList[5][2]
                    if sensorList[5][2] != 2:
                        if sensorList[5][3] != None :realTimeMap[centerY+1][centerX-5] = sensorList[5][3]
            
            if sensorList[6][0] != None :realTimeMap[centerY-1][centerX+2] = sensorList[6][0]
            if sensorList[6][0] != 2:
                if sensorList[6][1] != None :realTimeMap[centerY-1][centerX+3] = sensorList[6][1]
                if sensorList[6][1] != 2:
                    if sensorList[6][2] != None :realTimeMap[centerY-1][centerX+4] = sensorList[6][2]
                    if sensorList[6][2] != 2:
                        if sensorList[6][3] != None :realTimeMap[centerY-1][centerX+5] = sensorList[6][3]
        elif sensorList[0][0] == WEST:
            if sensorList[1][0] != None :realTimeMap[centerY+1][centerX-2] = sensorList[1][0]
            if sensorList[1][0] != 2:
                if sensorList[1][1] != None :realTimeMap[centerY+1][centerX-3] = sensorList[1][1]
                if sensorList[1][1] != 2:
                    if sensorList[1][2] != None :realTimeMap[centerY+1][centerX-4] = sensorList[1][2]
                    if sensorList[1][2] != 2:
                        if sensorList[1][3] != None :realTimeMap[centerY+1][centerX-5] = sensorList[1][3]
            
            if sensorList[2][0] != None :realTimeMap[centerY][centerX-2] = sensorList[2][0]
            if sensorList[2][0] != 2:
                if sensorList[2][1] != None :realTimeMap[centerY][centerX-3] = sensorList[2][1]
                if sensorList[2][1] != 2:
                    if sensorList[2][2] != None :realTimeMap[centerY][centerX-4] = sensorList[2][2]
                    if sensorList[2][2] != 2:
                        if sensorList[2][3] != None :realTimeMap[centerY][centerX-5] = sensorList[2][3]
            
            if sensorList[3][0] != None :realTimeMap[centerY-1][centerX-2] = sensorList[3][0]
            if sensorList[3][0] != 2:
                if sensorList[3][1] != None :realTimeMap[centerY-1][centerX-3] = sensorList[3][1]
                if sensorList[3][1] != 2:
                    if sensorList[3][2] != None :realTimeMap[centerY-1][centerX-4] = sensorList[3][2]
                    if sensorList[3][2] != 2:
                        if sensorList[3][3] != None :realTimeMap[centerY-1][centerX-5] = sensorList[3][3]
            
            if sensorList[4][0] != None :realTimeMap[centerY+2][centerX-1] = sensorList[4][0]
            if sensorList[4][0] != 2:
                if sensorList[4][1] != None :realTimeMap[centerY+3][centerX-1] = sensorList[4][1]
                if sensorList[4][1] != 2:
                    if sensorList[4][2] != None :realTimeMap[centerY+4][centerX-1] = sensorList[4][2]
                    if sensorList[4][2] != 2:
                        if sensorList[4][3] != None :realTimeMap[centerY+5][centerX-1] = sensorList[4][3]
            
            if sensorList[5][0] != None :realTimeMap[centerY-2][centerX-1] = sensorList[5][0]
            if sensorList[5][0] != 2:
                if sensorList[5][1] != None :realTimeMap[centerY-3][centerX-1] = sensorList[5][1]
                if sensorList[5][1] != 2:
                    if sensorList[5][2] != None :realTimeMap[centerY-4][centerX-1] = sensorList[5][2]
                    if sensorList[5][2] != 2:
                        if sensorList[5][3] != None :realTimeMap[centerY-5][centerX-1] = sensorList[5][3]
            
            if sensorList[6][0] != None :realTimeMap[centerY+2][centerX+1] = sensorList[6][0]
            if sensorList[6][0] != 2:
                if sensorList[6][1] != None :realTimeMap[centerY+3][centerX+1] = sensorList[6][1]
                if sensorList[6][1] != 2:
                    if sensorList[6][2] != None :realTimeMap[centerY+4][centerX+1] = sensorList[6][2]
                    if sensorList[6][2] != 2:
                        if sensorList[6][3] != None :realTimeMap[centerY+5][centerX+1] = sensorList[6][3]
        elif sensorList[0][0] == EAST:
            if sensorList[1][0] != None :realTimeMap[centerY-1][centerX+2] = sensorList[1][0]
            if sensorList[1][0] != 2:
                if sensorList[1][1] != None :realTimeMap[centerY-1][centerX+3] = sensorList[1][1]
                if sensorList[1][1] != 2:
                    if sensorList[1][2] != None :realTimeMap[centerY-1][centerX+4] = sensorList[1][2]
                    if sensorList[1][2] != 2:
                        if sensorList[1][3] != None :realTimeMap[centerY-1][centerX+5] = sensorList[1][3]
            
            if sensorList[2][0] != None :realTimeMap[centerY][centerX+2] = sensorList[2][0]
            if sensorList[2][0] != 2:
                if sensorList[2][1] != None :realTimeMap[centerY][centerX+3] = sensorList[2][1]
                if sensorList[2][1] != 2:
                    if sensorList[2][2] != None :realTimeMap[centerY][centerX+4] = sensorList[2][2]
                    if sensorList[2][2] != 2:
                        if sensorList[2][3] != None :realTimeMap[centerY][centerX+5] = sensorList[2][3]
            
            if sensorList[3][0] != None :realTimeMap[centerY+1][centerX+2] = sensorList[3][0]
            if sensorList[3][0] != 2:
                if sensorList[3][1] != None :realTimeMap[centerY+1][centerX+3] = sensorList[3][1]
                if sensorList[3][1] != 2:
                    if sensorList[3][2] != None :realTimeMap[centerY+1][centerX+4] = sensorList[3][2]
                    if sensorList[3][2] != 2:
                        if sensorList[3][3] != None :realTimeMap[centerY+1][centerX+5] = sensorList[3][3]
            
            if sensorList[4][0] != None :realTimeMap[centerY-2][centerX+1] = sensorList[4][0]
            if sensorList[4][0] != 2:
                if sensorList[4][1] != None :realTimeMap[centerY-3][centerX+1] = sensorList[4][1]
                if sensorList[4][1] != 2:
                    if sensorList[4][2] != None :realTimeMap[centerY-4][centerX+1] = sensorList[4][2]
                    if sensorList[4][2] != 2:
                        if sensorList[4][3] != None :realTimeMap[centerY-5][centerX+1] = sensorList[4][3]
            
            if sensorList[5][0] != None :realTimeMap[centerY+2][centerX+1] = sensorList[5][0]
            if sensorList[5][0] != 2:
                if sensorList[5][1] != None :realTimeMap[centerY+3][centerX+1] = sensorList[5][1]
                if sensorList[5][1] != 2:
                    if sensorList[5][2] != None :realTimeMap[centerY+4][centerX+1] = sensorList[5][2]
                    if sensorList[5][2] != 2:
                        if sensorList[5][3] != None :realTimeMap[centerY+5][centerX+1] = sensorList[5][3]
            
            if sensorList[6][0] != None :realTimeMap[centerY-2][centerX-1] = sensorList[6][0]
            if sensorList[6][0] != 2:
                if sensorList[6][1] != None :realTimeMap[centerY-3][centerX-1] = sensorList[6][1]
                if sensorList[6][1] != 2:
                    if sensorList[6][2] != None :realTimeMap[centerY-4][centerX-1] = sensorList[6][2]
                    if sensorList[6][2] != 2:
                        if sensorList[6][3] != None :realTimeMap[centerY-5][centerX-1] = sensorList[6][3]
        return realTimeMap

        
    def robotMovementAnalyses(self, realTimeMap, CenterX, CenterY, direction, prevMov, sensorList):
        def translate_back(action):
            if action == FORWARD:
                return FORWARD
            elif action == LEFT:
                return LEFT
            elif action == RIGHT:
                return RIGHT

        global spList
        if len(spList) > 0:
            resultMovement = translate_back(spList[0])
            spList = spList[1:]
            return resultMovement


        if direction == NORTH:
            if sensorList[4][0] != None and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1 and prevMov != LEFT:
                resultMovement = LEFT
            elif sensorList[1][0] != None and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1:
                resultMovement = FORWARD
            elif sensorList[5][0] != None and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1:
                resultMovement = RIGHT
            else:
                resultMovement = LEFT
        elif direction == SOUTH:
            if sensorList[4][0] != None and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1 and prevMov != LEFT:
                resultMovement = LEFT
            elif sensorList[1][0] != None and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1:
                resultMovement = FORWARD
            elif sensorList[5][0] != None and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1:
                resultMovement = RIGHT
            else:
                resultMovement = LEFT
        elif direction == WEST:
            if sensorList[4][0] != None and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1 and prevMov != LEFT:
                resultMovement = LEFT
            elif sensorList[1][0] != None and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1:
                resultMovement = FORWARD
            elif sensorList[5][0] != None and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1:
                resultMovement = RIGHT
            else:
                resultMovement = LEFT
        elif direction == EAST:
            if sensorList[4][0] != None and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1 and prevMov != LEFT:
                resultMovement = LEFT
            elif sensorList[1][0] != None and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1:
                resultMovement = FORWARD
            elif sensorList[5][0] != None and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1:
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
    

    def getRealTimeMap(self, sensors):
        global cnt
        global realTimeMap
        global robotCurMovement
        global robotBreak
        global robotCenterX
        global robotCenterY
        #print(cnt + 1, "before: ",  robotCurMovement)
        self.main(sensors)
        print(cnt + 1, robotCurMovement, ': ', robotCenterY, robotCenterX)
        cnt += 1
        return (robotCurMovement, robotBreak)