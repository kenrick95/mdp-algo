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
	robotDirectionX = 2
	robotDirectionY = 18
	cnt = 0

	def __init__(self):
		super(Exploration, self).__init__()

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
		global cnt
		cnt = 0
		
		Row0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row5 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row6 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row7 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row8 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row9 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row10 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row11 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row12 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row13 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row14 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row15 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row16 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row17 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row18 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Row19 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


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
		robotDirectionX = 2
		robotDirectionY = 18

		realTimeMap.append(Row0)
		realTimeMap.append(Row1)
		realTimeMap.append(Row2)
		realTimeMap.append(Row3)
		realTimeMap.append(Row4)
		realTimeMap.append(Row5)
		realTimeMap.append(Row6)
		realTimeMap.append(Row7)
		realTimeMap.append(Row8)
		realTimeMap.append(Row9)
		realTimeMap.append(Row10)
		realTimeMap.append(Row11)
		realTimeMap.append(Row12)
		realTimeMap.append(Row13)
		realTimeMap.append(Row14)
		realTimeMap.append(Row15)
		realTimeMap.append(Row16)
		realTimeMap.append(Row17)
		realTimeMap.append(Row18)
		realTimeMap.append(Row19)


		simulatorMap = self.simulatorReadMap()


	def main(self):
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
			
		realTimeMap = self.updateRobotPosition(realTimeMap, robotCenterX, robotCenterY, robotDirectionX, robotDirectionY)
		
		#for i in range(0,20):
		#	for j in range(0,15):
		#		print (simulatorMap[i][j],end="")
		#	print()
		# for k in range(0,150):
		#		for j in range(0,15):
		#			print (realTimeMap[i][j],end="")
		#		print()
		self.callAllMethods()
		# print("-----------------------------------------------------------------")
		
		for tup in pathTaken:
			if realTimeMap[tup[0]][tup[1]] != 4 and realTimeMap[tup[0]][tup[1]] != 5:
				realTimeMap[tup[0]][tup[1]] = 8
		# for i in range(0,20):
		# 	for j in range(0,15):
		# 		print (realTimeMap[i][j],end="")
		# 	print()

	def callAllMethods(self):
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
		#for i in range(0,7):
		#	print(sensorList[i])
		realTimeMap = self.updateRealTimeMap(realTimeMap, sensorList, robotCenterX, robotCenterY)
		
		robotCurMovement = self.robotMovementAnalyses(realTimeMap, robotCenterX, robotCenterY, sensorList[0][0], robotPrevMovement, sensorList)
		robotPrevMovement = robotCurMovement
		if robotCurMovement == "W":
			pathTaken.append((robotCenterY, robotCenterX))
		#print (robotCurMovement)
		realTimeMap = self.executeRobotMovement(realTimeMap, robotCenterX, robotCenterY, sensorList[0][0], robotCurMovement)
		
		if sensorList[0][0] == "U":
			if robotCurMovement == "D":
				robotDirectionX = robotDirectionX + 1
				robotDirectionY = robotDirectionY + 1
			elif robotCurMovement == "W":
				robotCenterY = robotCenterY - 1
				robotDirectionY = robotDirectionY - 1
			elif robotCurMovement == "A":
				robotDirectionX = robotDirectionX - 1
				robotDirectionY = robotDirectionY + 1
		if sensorList[0][0] == "D":
			if robotCurMovement == "D":
				robotDirectionX = robotDirectionX - 1
				robotDirectionY = robotDirectionY - 1
			elif robotCurMovement == "W":
				robotCenterY = robotCenterY + 1
				robotDirectionY = robotDirectionY + 1
			elif robotCurMovement == "A":
				robotDirectionX = robotDirectionX + 1
				robotDirectionY = robotDirectionY - 1
		if sensorList[0][0] == "L":
			if robotCurMovement == "D":
				robotDirectionX = robotDirectionX + 1
				robotDirectionY = robotDirectionY - 1
			elif robotCurMovement == "W":
				robotCenterX = robotCenterX -1
				robotDirectionX = robotDirectionX - 1
			elif robotCurMovement == "A":
				robotDirectionX = robotDirectionX + 1
				robotDirectionY = robotDirectionY + 1
		if sensorList[0][0] == "R":
			if robotCurMovement == "D":
				robotDirectionX = robotDirectionX - 1
				robotDirectionY = robotDirectionY + 1
			elif robotCurMovement == "W":
				robotCenterX = robotCenterX + 1
				robotDirectionX = robotDirectionX + 1
			elif robotCurMovement == "A":
				robotDirectionX = robotDirectionX - 1
				robotDirectionY = robotDirectionY - 1
		#for i in range(0,20):
		#	for j in range(0,15):
		#		print (realTimeMap[i][j],end="")
		#	print()
		#print("-----------------------------------------------------------------")
			
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
			returnValue.append(["U"])
		#D-Facing down
		elif (centerX == directionX) and (directionY > centerY):
			returnValue.append(["D"])
		#L-facing left
		elif (centerY == directionY) and (directionX < centerX):
			returnValue.append(["L"])
		#R-facing right
		elif (centerY == directionY) and (directionX > centerX):
			returnValue.append(["R"])
		
		if returnValue[0][0] == "U":
			returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX-1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX-1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX-1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX-1]])
			returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX]])
			returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX+1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX+1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX+1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX+1]])
			returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY-1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY-1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY-1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY-1][centerX-5]])
			returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY-1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY-1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY-1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY-1][centerX+5]])
			returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY+1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY+1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY+1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY+1][centerX-5]])
		elif returnValue[0][0] == "D":
			returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX+1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX+1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX+1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX+1]])
			returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX]])
			returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX-1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX-1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX-1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX-1]])
			returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY+1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY+1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY+1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY+1][centerX+5]])
			returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY+1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY+1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY+1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY+1][centerX-5]])
			returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY-1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY-1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY-1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY-1][centerX+5]])
		elif returnValue[0][0] == "L":
			returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY+1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY+1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY+1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY+1][centerX-5]])
			returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY][centerX-5]])
			returnValue.append([3 if outOfBoundLeft>=4 else simMap[centerY-1][centerX-2], 3 if outOfBoundLeft>=3 else simMap[centerY-1][centerX-3], 3 if outOfBoundLeft>=2 else simMap[centerY-1][centerX-4], 3 if outOfBoundLeft>=1 else simMap[centerY-1][centerX-5]])
			returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX-1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX-1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX-1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX-1]])
			returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX-1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX-1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX-1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX-1]])
			returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX+1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX+1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX+1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX+1]])
		elif returnValue[0][0] == "R":
			returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY-1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY-1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY-1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY-1][centerX+5]])
			returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY][centerX+5]])
			returnValue.append([3 if outOfBoundRight>=4 else simMap[centerY+1][centerX+2], 3 if outOfBoundRight>=3 else simMap[centerY+1][centerX+3], 3 if outOfBoundRight>=2 else simMap[centerY+1][centerX+4], 3 if outOfBoundRight>=1 else simMap[centerY+1][centerX+5]])
			returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX+1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX+1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX+1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX+1]])
			returnValue.append([3 if outOfBoundDown>=4 else simMap[centerY+2][centerX+1], 3 if outOfBoundDown>=3 else simMap[centerY+3][centerX+1], 3 if outOfBoundDown>=2 else simMap[centerY+4][centerX+1], 3 if outOfBoundDown>=1 else simMap[centerY+5][centerX+1]])
			returnValue.append([3 if outOfBoundUp>=4 else simMap[centerY-2][centerX-1], 3 if outOfBoundUp>=3 else simMap[centerY-3][centerX-1], 3 if outOfBoundUp>=2 else simMap[centerY-4][centerX-1], 3 if outOfBoundUp>=1 else simMap[centerY-5][centerX-1]])
			
		return returnValue
		
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
		if sensorList[0][0] == "U":
			#front left
			if sensorList[1][0] != 3 :realTimeMap[centerY-2][centerX-1] = sensorList[1][0]
			if sensorList[1][1] != 3 :realTimeMap[centerY-3][centerX-1] = sensorList[1][1]
			if sensorList[1][2] != 3 :realTimeMap[centerY-4][centerX-1] = sensorList[1][2]
			if sensorList[1][3] != 3 :realTimeMap[centerY-5][centerX-1] = sensorList[1][3]
			#front center
			if sensorList[2][0] != 3 :realTimeMap[centerY-2][centerX] = sensorList[2][0]
			if sensorList[2][1] != 3 :realTimeMap[centerY-3][centerX] = sensorList[2][1]
			if sensorList[2][2] != 3 :realTimeMap[centerY-4][centerX] = sensorList[2][2]
			if sensorList[2][3] != 3 :realTimeMap[centerY-5][centerX] = sensorList[2][3]
			#front right
			if sensorList[3][0] != 3 :realTimeMap[centerY-2][centerX+1] = sensorList[3][0]
			if sensorList[3][1] != 3 :realTimeMap[centerY-3][centerX+1] = sensorList[3][1]
			if sensorList[3][2] != 3 :realTimeMap[centerY-4][centerX+1] = sensorList[3][2]
			if sensorList[3][3] != 3 :realTimeMap[centerY-5][centerX+1] = sensorList[3][3]
			#left
			if sensorList[4][0] != 3 :realTimeMap[centerY-1][centerX-2] = sensorList[4][0]
			if sensorList[4][1] != 3 :realTimeMap[centerY-1][centerX-3] = sensorList[4][1]
			if sensorList[4][2] != 3 :realTimeMap[centerY-1][centerX-4] = sensorList[4][2]
			if sensorList[4][3] != 3 :realTimeMap[centerY-1][centerX-5] = sensorList[4][3]
			#right
			if sensorList[5][0] != 3 :realTimeMap[centerY-1][centerX+2] = sensorList[5][0]
			if sensorList[5][1] != 3 :realTimeMap[centerY-1][centerX+3] = sensorList[5][1]
			if sensorList[5][2] != 3 :realTimeMap[centerY-1][centerX+4] = sensorList[5][2]
			if sensorList[5][3] != 3 :realTimeMap[centerY-1][centerX+5] = sensorList[5][3]
			#bottom left
			if sensorList[6][0] != 3 :realTimeMap[centerY+1][centerX-2] = sensorList[6][0]
			if sensorList[6][1] != 3 :realTimeMap[centerY+1][centerX-3] = sensorList[6][1]
			if sensorList[6][2] != 3 :realTimeMap[centerY+1][centerX-4] = sensorList[6][2]
			if sensorList[6][3] != 3 :realTimeMap[centerY+1][centerX-5] = sensorList[6][3]
		elif sensorList[0][0] == "D":
			if sensorList[1][0] != 3 :realTimeMap[centerY+2][centerX+1] = sensorList[1][0]
			if sensorList[1][1] != 3 :realTimeMap[centerY+3][centerX+1] = sensorList[1][1]
			if sensorList[1][2] != 3 :realTimeMap[centerY+4][centerX+1] = sensorList[1][2]
			if sensorList[1][3] != 3 :realTimeMap[centerY+5][centerX+1] = sensorList[1][3]
			
			if sensorList[2][0] != 3 :realTimeMap[centerY+2][centerX] = sensorList[2][0]
			if sensorList[2][1] != 3 :realTimeMap[centerY+3][centerX] = sensorList[2][1]
			if sensorList[2][2] != 3 :realTimeMap[centerY+4][centerX] = sensorList[2][2]
			if sensorList[2][3] != 3 :realTimeMap[centerY+5][centerX] = sensorList[2][3]
			
			if sensorList[3][0] != 3 :realTimeMap[centerY+2][centerX-1] = sensorList[3][0]
			if sensorList[3][1] != 3 :realTimeMap[centerY+3][centerX-1] = sensorList[3][1]
			if sensorList[3][2] != 3 :realTimeMap[centerY+4][centerX-1] = sensorList[3][2]
			if sensorList[3][3] != 3 :realTimeMap[centerY+5][centerX-1] = sensorList[3][3]
			
			if sensorList[4][0] != 3 :realTimeMap[centerY+1][centerX+2] = sensorList[4][0]
			if sensorList[4][1] != 3 :realTimeMap[centerY+1][centerX+3] = sensorList[4][1]
			if sensorList[4][2] != 3 :realTimeMap[centerY+1][centerX+4] = sensorList[4][2]
			if sensorList[4][3] != 3 :realTimeMap[centerY+1][centerX+5] = sensorList[4][3]
			
			if sensorList[5][0] != 3 :realTimeMap[centerY+1][centerX-2] = sensorList[5][0]
			if sensorList[5][1] != 3 :realTimeMap[centerY+1][centerX-3] = sensorList[5][1]
			if sensorList[5][2] != 3 :realTimeMap[centerY+1][centerX-4] = sensorList[5][2]
			if sensorList[5][3] != 3 :realTimeMap[centerY+1][centerX-5] = sensorList[5][3]
			
			if sensorList[6][0] != 3 :realTimeMap[centerY-1][centerX+2] = sensorList[6][0]
			if sensorList[6][1] != 3 :realTimeMap[centerY-1][centerX+3] = sensorList[6][1]
			if sensorList[6][2] != 3 :realTimeMap[centerY-1][centerX+4] = sensorList[6][2]
			if sensorList[6][3] != 3 :realTimeMap[centerY-1][centerX+5] = sensorList[6][3]
		elif sensorList[0][0] == "L":
			if sensorList[1][0] != 3 :realTimeMap[centerY+1][centerX-2] = sensorList[1][0]
			if sensorList[1][1] != 3 :realTimeMap[centerY+1][centerX-3] = sensorList[1][1]
			if sensorList[1][2] != 3 :realTimeMap[centerY+1][centerX-4] = sensorList[1][2]
			if sensorList[1][3] != 3 :realTimeMap[centerY+1][centerX-5] = sensorList[1][3]
			
			if sensorList[2][0] != 3 :realTimeMap[centerY][centerX-2] = sensorList[2][0]
			if sensorList[2][1] != 3 :realTimeMap[centerY][centerX-3] = sensorList[2][1]
			if sensorList[2][2] != 3 :realTimeMap[centerY][centerX-4] = sensorList[2][2]
			if sensorList[2][3] != 3 :realTimeMap[centerY][centerX-5] = sensorList[2][3]
			
			if sensorList[3][0] != 3 :realTimeMap[centerY-1][centerX-2] = sensorList[3][0]
			if sensorList[3][1] != 3 :realTimeMap[centerY-1][centerX-3] = sensorList[3][1]
			if sensorList[3][2] != 3 :realTimeMap[centerY-1][centerX-4] = sensorList[3][2]
			if sensorList[3][3] != 3 :realTimeMap[centerY-1][centerX-5] = sensorList[3][3]
			
			if sensorList[4][0] != 3 :realTimeMap[centerY+2][centerX-1] = sensorList[4][0]
			if sensorList[4][1] != 3 :realTimeMap[centerY+3][centerX-1] = sensorList[4][1]
			if sensorList[4][2] != 3 :realTimeMap[centerY+4][centerX-1] = sensorList[4][2]
			if sensorList[4][3] != 3 :realTimeMap[centerY+5][centerX-1] = sensorList[4][3]
			
			if sensorList[5][0] != 3 :realTimeMap[centerY-2][centerX-1] = sensorList[5][0]
			if sensorList[5][1] != 3 :realTimeMap[centerY-3][centerX-1] = sensorList[5][1]
			if sensorList[5][2] != 3 :realTimeMap[centerY-4][centerX-1] = sensorList[5][2]
			if sensorList[5][3] != 3 :realTimeMap[centerY-5][centerX-1] = sensorList[5][3]
			
			if sensorList[6][0] != 3 :realTimeMap[centerY+2][centerX+1] = sensorList[6][0]
			if sensorList[6][1] != 3 :realTimeMap[centerY+3][centerX+1] = sensorList[6][1]
			if sensorList[6][2] != 3 :realTimeMap[centerY+4][centerX+1] = sensorList[6][2]
			if sensorList[6][3] != 3 :realTimeMap[centerY+5][centerX+1] = sensorList[6][3]
		elif sensorList[0][0] == "R":
			if sensorList[1][0] != 3 :realTimeMap[centerY-1][centerX+2] = sensorList[1][0]
			if sensorList[1][1] != 3 :realTimeMap[centerY-1][centerX+3] = sensorList[1][1]
			if sensorList[1][2] != 3 :realTimeMap[centerY-1][centerX+4] = sensorList[1][2]
			if sensorList[1][3] != 3 :realTimeMap[centerY-1][centerX+5] = sensorList[1][3]
			
			if sensorList[2][0] != 3 :realTimeMap[centerY][centerX+2] = sensorList[2][0]
			if sensorList[2][1] != 3 :realTimeMap[centerY][centerX+3] = sensorList[2][1]
			if sensorList[2][2] != 3 :realTimeMap[centerY][centerX+4] = sensorList[2][2]
			if sensorList[2][3] != 3 :realTimeMap[centerY][centerX+5] = sensorList[2][3]
			
			if sensorList[3][0] != 3 :realTimeMap[centerY+1][centerX+2] = sensorList[3][0]
			if sensorList[3][1] != 3 :realTimeMap[centerY+1][centerX+3] = sensorList[3][1]
			if sensorList[3][2] != 3 :realTimeMap[centerY+1][centerX+4] = sensorList[3][2]
			if sensorList[3][3] != 3 :realTimeMap[centerY+1][centerX+5] = sensorList[3][3]
			
			if sensorList[4][0] != 3 :realTimeMap[centerY-2][centerX+1] = sensorList[4][0]
			if sensorList[4][1] != 3 :realTimeMap[centerY-3][centerX+1] = sensorList[4][1]
			if sensorList[4][2] != 3 :realTimeMap[centerY-4][centerX+1] = sensorList[4][2]
			if sensorList[4][3] != 3 :realTimeMap[centerY-5][centerX+1] = sensorList[4][3]
			
			if sensorList[5][0] != 3 :realTimeMap[centerY+2][centerX+1] = sensorList[5][0]
			if sensorList[5][1] != 3 :realTimeMap[centerY+3][centerX+1] = sensorList[5][1]
			if sensorList[5][2] != 3 :realTimeMap[centerY+4][centerX+1] = sensorList[5][2]
			if sensorList[5][3] != 3 :realTimeMap[centerY+5][centerX+1] = sensorList[5][3]
			
			if sensorList[6][0] != 3 :realTimeMap[centerY-2][centerX-1] = sensorList[6][0]
			if sensorList[6][1] != 3 :realTimeMap[centerY-3][centerX-1] = sensorList[6][1]
			if sensorList[6][2] != 3 :realTimeMap[centerY-4][centerX-1] = sensorList[6][2]
			if sensorList[6][3] != 3 :realTimeMap[centerY-5][centerX-1] = sensorList[6][3]
		return realTimeMap
		
	def robotMovementAnalyses(self, realTimeMap, CenterX, CenterY, direction, prevMov, sensorList):
		if direction == "U":
			if sensorList[5][0] != 3 and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1 and prevMov != "D":
				resultMovement = "D"
			elif sensorList[1][0] != 3 and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1:
				resultMovement = "W"
			elif sensorList[4][0] != 3 and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1:
				resultMovement = "A"
			else:
				resultMovement = "D"
		elif direction == "D":
			if sensorList[5][0] != 3 and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1 and prevMov != "D":
				resultMovement = "D"
			elif sensorList[1][0] != 3 and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1:
				resultMovement = "W"
			elif sensorList[4][0] != 3 and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1:
				resultMovement = "A"
			else:
				resultMovement = "D"
		elif direction == "L":
			if sensorList[5][0] != 3 and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1 and prevMov != "D":
				resultMovement = "D"
			elif sensorList[1][0] != 3 and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1:
				resultMovement = "W"
			elif sensorList[4][0] != 3 and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1:
				resultMovement = "A"
			else:
				resultMovement = "D"
		elif direction == "R":
			if sensorList[5][0] != 3 and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1 and prevMov != "D":
				resultMovement = "D"
			elif sensorList[1][0] != 3 and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1:
				resultMovement = "W"
			elif sensorList[4][0] != 3 and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1:
				resultMovement = "A"
			else:
				resultMovement = "D"
		return resultMovement
		
	def executeRobotMovement(self, realTimeMap, CenterX, CenterY, direction, movement):
		if direction == "U":
			if movement == "D":
				realTimeMap[CenterY][CenterX+1] = 4
				realTimeMap[CenterY-1][CenterX] = 1
			elif movement == "W":
				realTimeMap[CenterY][CenterX] = 1
				realTimeMap[CenterY-1][CenterX] = 5
				realTimeMap[CenterY-2][CenterX] = 4
			elif movement == "A":
				realTimeMap[CenterY][CenterX-1] = 4
				realTimeMap[CenterY-1][CenterX] = 1
		elif direction == "D":
			if movement == "D":
				realTimeMap[CenterY][CenterX-1] = 4
				realTimeMap[CenterY+1][CenterX] = 1
			elif movement == "W":
				realTimeMap[CenterY][CenterX] = 1
				realTimeMap[CenterY+1][CenterX] = 5
				realTimeMap[CenterY+2][CenterX] = 4
			elif movement == "A":
				realTimeMap[CenterY][CenterX+1] = 4
				realTimeMap[CenterY+1][CenterX] = 1
		elif direction == "L":
			if movement == "D":
				realTimeMap[CenterY-1][CenterX] = 4
				realTimeMap[CenterY][CenterX-1] = 1
			elif movement == "W":
				realTimeMap[CenterY][CenterX] = 1
				realTimeMap[CenterY][CenterX-1] = 5
				realTimeMap[CenterY][CenterX-2] = 4
			elif movement == "A":
				realTimeMap[CenterY+1][CenterX] = 4
				realTimeMap[CenterY][CenterX-1] = 1
		elif direction == "R":
			if movement == "D":
				realTimeMap[CenterY+1][CenterX] = 4
				realTimeMap[CenterY][CenterX+1] = 1
			elif movement == "W":
				realTimeMap[CenterY][CenterX] = 1
				realTimeMap[CenterY][CenterX+1] = 5
				realTimeMap[CenterY][CenterX+2] = 4
			elif movement == "A":
				realTimeMap[CenterY-1][CenterX] = 4
				realTimeMap[CenterY][CenterX+1] = 1
		return realTimeMap
	

	def getRealTimeMap(self):
		global cnt
		global realTimeMap
		global robotCurMovement
		self.main()
		print(cnt + 1, robotCurMovement)
		cnt += 1
		return (realTimeMap, robotCurMovement)