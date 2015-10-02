realTimeMap = []
simulatorMap = []
sensorList = []
pathTaken = []
alignmentAction = []
mapState = []
mapStateChanged = []
repeatedArea = 0
robotPrevMovement = "O"
robotCurMovement = "O"

robotCenterX = 1
robotCenterY = 18
robotDirectionX = 1
robotDirectionY = 17

def explorationMain(exploredPercentage):
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
	
	variableInitialisation()
	#set robot starting position
	realTimeMap[robotCenterY][robotCenterX] = 5
	realTimeMap[robotDirectionY][robotDirectionX] = 4
	
	#for i in range(0,20):
	#	for j in range(0,15):
	#		print (simulatorMap[i][j],end="")
	#	print()
	#for i in range(0,20):
	#	for j in range(0,15):
	#		print (realTimeMap[i][j],end="")
	#	print()
	exploredArea = 0
	indexing = 1
	while repeatedArea <= 20 and (exploredArea*100) < (exploredPercentage*300):
		print ("Index:", indexing)
		indexing = indexing + 1
		exploredArea = 0
		callAllMethods()
		for tup in pathTaken:
			if tup == (robotCenterY, robotCenterX):
				repeatedArea = repeatedArea + 1
				break;
		for i in range(0,20):
			for j in range(0,15):
				if realTimeMap[i][j] != 0:
					exploredArea = exploredArea + 1
		print ("repeated Area:", repeatedArea)
		print ("exploredArea:", exploredArea)
		print("-----------------------------------------------------------------")
	
	for tup in pathTaken:
		if realTimeMap[tup[0]][tup[1]] != 4 and realTimeMap[tup[0]][tup[1]] != 5:
			realTimeMap[tup[0]][tup[1]] = 8

	for i in range(0,20):
		for j in range(0,15):
			print (realTimeMap[i][j],end="")
		print()
		
def variableInitialisation():
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
	global mapState
	
	mapState = []
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
	realTimeMap[17][0] = 1
	realTimeMap[17][2] = 1
	realTimeMap[18][0] = 1
	realTimeMap[18][2] = 1
	realTimeMap[19][0] = 1
	realTimeMap[19][1] = 1
	realTimeMap[19][2] = 1
	
	simulatorMap = simulatorReadMap()
	
	for i in range (0,20):
		Row = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		mapState.append(Row)
	mapState[17][0] = 1
	mapState[17][1] = 1
	mapState[17][2] = 1
	mapState[18][0] = 1
	mapState[18][1] = 1
	mapState[18][2] = 1
	mapState[19][0] = 1
	mapState[19][1] = 1
	mapState[19][2] = 1

def callAllMethods():
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
	global alignmentAction
	global mapState
	global mapStateChanged
	oldMapTemp = []
	mapStateChanged = []
	
	sensorList = getSensor(simulatorMap, robotCenterX, robotCenterY, robotDirectionX, robotDirectionY)
	for i in range (0,20):
		Row = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		ChangedRow = ["N","N","N","N","N","N","N","N","N","N","N","N","N","N","N"]
		oldMapTemp.append(Row)
		mapStateChanged.append(ChangedRow)
		for j in range(0,15):
			oldMapTemp[i][j] = realTimeMap[i][j]
	
	realTimeMap = updateRealTimeMap(realTimeMap, sensorList, robotCenterX, robotCenterY)
	
	#for i in range(0,20):
	#	for j in range(0,15):
	#		print (mapStateChanged[i][j],end="")
	#	print()
	for i in range(0,20):
		for j in range(0,15):
			print (realTimeMap[i][j],end="")
		print()
	print("1------------------------------------------1")
	mapStateAnalysis(oldMapTemp)
	for i in range(0,20):
		for j in range(0,15):
			print (mapState[i][j],end="")
		print()
	print("2------------------------------------------2")
	
	#for i in range(0,20):
	#	for j in range(0,15):
	#		print (mapState[i][j],end="")
	#	print()
	
	robotCurMovement = robotMovementAnalyses(realTimeMap, robotCenterX, robotCenterY, sensorList[0][0], robotPrevMovement, sensorList)
	robotPrevMovement = robotCurMovement
	if robotCurMovement == "W":
		pathTaken.append((robotCenterY, robotCenterX))
	alignmentAction = robotAngleAndDistanceAlignment(sensorList)
	print (alignmentAction)
		
	realTimeMap = executeRobotMovement(realTimeMap, robotCenterX, robotCenterY, sensorList[0][0], robotCurMovement)
	
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
		
def getSensor(simMap, centerX, centerY, directionX, directionY):
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
	#get sensor value from simulator map
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

#load simulatorMap from text file
def simulatorReadMap():
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
	
def updateRealTimeMap(realTimeMap, sensorList, centerX, centerY):
	global mapStateChanged
	if sensorList[0][0] == "U":
		#front left
		if sensorList[1][0] != 3 :realTimeMap[centerY-2][centerX-1] = sensorList[1][0]; mapStateChanged[centerY-2][centerX-1] = "C"
		if sensorList[1][0] != 2:
			if sensorList[1][1] != 3 :realTimeMap[centerY-3][centerX-1] = sensorList[1][1]; mapStateChanged[centerY-3][centerX-1] = "C"
			if sensorList[1][1] != 2:
				if sensorList[1][2] != 3 :realTimeMap[centerY-4][centerX-1] = sensorList[1][2]; mapStateChanged[centerY-4][centerX-1] = "C"
				if sensorList[1][2] != 2:
					if sensorList[1][3] != 3 :realTimeMap[centerY-5][centerX-1] = sensorList[1][3]; mapStateChanged[centerY-5][centerX-1] = "C"
		#front center
		if sensorList[2][0] != 3 :realTimeMap[centerY-2][centerX] = sensorList[2][0]; mapStateChanged[centerY-2][centerX] = "C"
		if sensorList[2][0] != 2:
			if sensorList[2][1] != 3 :realTimeMap[centerY-3][centerX] = sensorList[2][1]; mapStateChanged[centerY-3][centerX] = "C"
			if sensorList[2][1] != 2:
				if sensorList[2][2] != 3 :realTimeMap[centerY-4][centerX] = sensorList[2][2]; mapStateChanged[centerY-4][centerX] = "C"
				if sensorList[2][2] != 2:
					if sensorList[2][3] != 3 :realTimeMap[centerY-5][centerX] = sensorList[2][3]; mapStateChanged[centerY-5][centerX] = "C"
		#front right
		if sensorList[3][0] != 3 :realTimeMap[centerY-2][centerX+1] = sensorList[3][0]; mapStateChanged[centerY-2][centerX+1] = "C"
		if sensorList[3][0] != 2:
			if sensorList[3][1] != 3 :realTimeMap[centerY-3][centerX+1] = sensorList[3][1]; mapStateChanged[centerY-3][centerX+1] = "C"
			if sensorList[3][1] != 2:
				if sensorList[3][2] != 3 :realTimeMap[centerY-4][centerX+1] = sensorList[3][2]; mapStateChanged[centerY-4][centerX+1] = "C"
				if sensorList[3][2] != 2:
					if sensorList[3][3] != 3 :realTimeMap[centerY-5][centerX+1] = sensorList[3][3]; mapStateChanged[centerY-5][centerX+1] = "C"
		#left
		if sensorList[4][0] != 3 :realTimeMap[centerY-1][centerX-2] = sensorList[4][0]; mapStateChanged[centerY-1][centerX-2] = "C"
		if sensorList[4][0] != 2:
			if sensorList[4][1] != 3 :realTimeMap[centerY-1][centerX-3] = sensorList[4][1]; mapStateChanged[centerY-1][centerX-3] = "C"
			if sensorList[4][1] != 2:
				if sensorList[4][2] != 3 :realTimeMap[centerY-1][centerX-4] = sensorList[4][2]; mapStateChanged[centerY-1][centerX-4] = "C"
				if sensorList[4][2] != 2:
					if sensorList[4][3] != 3 :realTimeMap[centerY-1][centerX-5] = sensorList[4][3]; mapStateChanged[centerY-1][centerX-5] = "C"
		#right
		if sensorList[5][0] != 3 :realTimeMap[centerY-1][centerX+2] = sensorList[5][0]; mapStateChanged[centerY-1][centerX+2] = "C"
		if sensorList[5][0] != 2:
			if sensorList[5][1] != 3 :realTimeMap[centerY-1][centerX+3] = sensorList[5][1]; mapStateChanged[centerY-1][centerX+3] = "C"
			if sensorList[5][1] != 2:
				if sensorList[5][2] != 3 :realTimeMap[centerY-1][centerX+4] = sensorList[5][2]; mapStateChanged[centerY-1][centerX+4] = "C"
				if sensorList[5][2] != 2:
					if sensorList[5][3] != 3 :realTimeMap[centerY-1][centerX+5] = sensorList[5][3]; mapStateChanged[centerY-1][centerX+5] = "C"
		#bottom left
		if sensorList[6][0] != 3 :realTimeMap[centerY+1][centerX-2] = sensorList[6][0]; mapStateChanged[centerY+1][centerX-2] = "C"
		if sensorList[6][0] != 2:
			if sensorList[6][1] != 3 :realTimeMap[centerY+1][centerX-3] = sensorList[6][1]; mapStateChanged[centerY+1][centerX-3] = "C"
			if sensorList[6][1] != 2:
				if sensorList[6][2] != 3 :realTimeMap[centerY+1][centerX-4] = sensorList[6][2]; mapStateChanged[centerY+1][centerX-4] = "C"
				if sensorList[6][2] != 2:
					if sensorList[6][3] != 3 :realTimeMap[centerY+1][centerX-5] = sensorList[6][3]; mapStateChanged[centerY+1][centerX-5] = "C"
	elif sensorList[0][0] == "D":
		if sensorList[1][0] != 3 :realTimeMap[centerY+2][centerX+1] = sensorList[1][0]; mapStateChanged[centerY+2][centerX+1] = "C"
		if sensorList[1][0] != 2:
			if sensorList[1][1] != 3 :realTimeMap[centerY+3][centerX+1] = sensorList[1][1]; mapStateChanged[centerY+3][centerX+1] = "C"
			if sensorList[1][1] != 2:
				if sensorList[1][2] != 3 :realTimeMap[centerY+4][centerX+1] = sensorList[1][2]; mapStateChanged[centerY+4][centerX+1] = "C"
				if sensorList[1][2] != 2:
					if sensorList[1][3] != 3 :realTimeMap[centerY+5][centerX+1] = sensorList[1][3]; mapStateChanged[centerY+5][centerX+1] = "C"
		
		if sensorList[2][0] != 3 :realTimeMap[centerY+2][centerX] = sensorList[2][0]; mapStateChanged[centerY+2][centerX] = "C"
		if sensorList[2][0] != 2:
			if sensorList[2][1] != 3 :realTimeMap[centerY+3][centerX] = sensorList[2][1]; mapStateChanged[centerY+3][centerX] = "C"
			if sensorList[2][1] != 2:
				if sensorList[2][2] != 3 :realTimeMap[centerY+4][centerX] = sensorList[2][2]; mapStateChanged[centerY+4][centerX] = "C"
				if sensorList[2][2] != 2:
					if sensorList[2][3] != 3 :realTimeMap[centerY+5][centerX] = sensorList[2][3]; mapStateChanged[centerY+5][centerX] = "C"
		
		if sensorList[3][0] != 3 :realTimeMap[centerY+2][centerX-1] = sensorList[3][0]; mapStateChanged[centerY+2][centerX-1] = "C"
		if sensorList[3][0] != 2:
			if sensorList[3][1] != 3 :realTimeMap[centerY+3][centerX-1] = sensorList[3][1]; mapStateChanged[centerY+3][centerX-1] = "C"
			if sensorList[3][1] != 2:
				if sensorList[3][2] != 3 :realTimeMap[centerY+4][centerX-1] = sensorList[3][2]; mapStateChanged[centerY+4][centerX-1] = "C"
				if sensorList[3][2] != 2:
					if sensorList[3][3] != 3 :realTimeMap[centerY+5][centerX-1] = sensorList[3][3]; mapStateChanged[centerY+5][centerX-1] = "C"
		
		if sensorList[4][0] != 3 :realTimeMap[centerY+1][centerX+2] = sensorList[4][0]; mapStateChanged[centerY+1][centerX+2] = "C"
		if sensorList[4][0] != 2:
			if sensorList[4][1] != 3 :realTimeMap[centerY+1][centerX+3] = sensorList[4][1]; mapStateChanged[centerY+1][centerX+3] = "C"
			if sensorList[4][1] != 2:
				if sensorList[4][2] != 3 :realTimeMap[centerY+1][centerX+4] = sensorList[4][2]; mapStateChanged[centerY+1][centerX+4] = "C"
				if sensorList[4][2] != 2:
					if sensorList[4][3] != 3 :realTimeMap[centerY+1][centerX+5] = sensorList[4][3]; mapStateChanged[centerY+1][centerX+5] = "C"
		
		if sensorList[5][0] != 3 :realTimeMap[centerY+1][centerX-2] = sensorList[5][0]; mapStateChanged[centerY+1][centerX-2] = "C"
		if sensorList[5][0] != 2:
			if sensorList[5][1] != 3 :realTimeMap[centerY+1][centerX-3] = sensorList[5][1]; mapStateChanged[centerY+1][centerX-3] = "C"
			if sensorList[5][1] != 2:
				if sensorList[5][2] != 3 :realTimeMap[centerY+1][centerX-4] = sensorList[5][2]; mapStateChanged[centerY+1][centerX-4] = "C"
				if sensorList[5][2] != 2:
					if sensorList[5][3] != 3 :realTimeMap[centerY+1][centerX-5] = sensorList[5][3]; mapStateChanged[centerY+1][centerX-5] = "C"
		
		if sensorList[6][0] != 3 :realTimeMap[centerY-1][centerX+2] = sensorList[6][0]; mapStateChanged[centerY-1][centerX+2] = "C"
		if sensorList[6][0] != 2:
			if sensorList[6][1] != 3 :realTimeMap[centerY-1][centerX+3] = sensorList[6][1]; mapStateChanged[centerY-1][centerX+3] = "C"
			if sensorList[6][1] != 2:
				if sensorList[6][2] != 3 :realTimeMap[centerY-1][centerX+4] = sensorList[6][2]; mapStateChanged[centerY-1][centerX+4] = "C"
				if sensorList[6][2] != 2:
					if sensorList[6][3] != 3 :realTimeMap[centerY-1][centerX+5] = sensorList[6][3]; mapStateChanged[centerY-1][centerX+5] = "C"
	elif sensorList[0][0] == "L":
		if sensorList[1][0] != 3 :realTimeMap[centerY+1][centerX-2] = sensorList[1][0]; mapStateChanged[centerY+1][centerX-2] = "C"
		if sensorList[1][0] != 2:
			if sensorList[1][1] != 3 :realTimeMap[centerY+1][centerX-3] = sensorList[1][1]; mapStateChanged[centerY+1][centerX-3] = "C"
			if sensorList[1][1] != 2:
				if sensorList[1][2] != 3 :realTimeMap[centerY+1][centerX-4] = sensorList[1][2]; mapStateChanged[centerY+1][centerX-4] = "C"
				if sensorList[1][2] != 2:
					if sensorList[1][3] != 3 :realTimeMap[centerY+1][centerX-5] = sensorList[1][3]; mapStateChanged[centerY+1][centerX-5] = "C"
		
		if sensorList[2][0] != 3 :realTimeMap[centerY][centerX-2] = sensorList[2][0]; mapStateChanged[centerY][centerX-2] = "C"
		if sensorList[2][0] != 2:
			if sensorList[2][1] != 3 :realTimeMap[centerY][centerX-3] = sensorList[2][1]; mapStateChanged[centerY][centerX-3] = "C"
			if sensorList[2][1] != 2:
				if sensorList[2][2] != 3 :realTimeMap[centerY][centerX-4] = sensorList[2][2]; mapStateChanged[centerY][centerX-4] = "C"
				if sensorList[2][2] != 2:
					if sensorList[2][3] != 3 :realTimeMap[centerY][centerX-5] = sensorList[2][3]; mapStateChanged[centerY][centerX-5] = "C"
		
		if sensorList[3][0] != 3 :realTimeMap[centerY-1][centerX-2] = sensorList[3][0]; mapStateChanged[centerY-1][centerX-2] = "C"
		if sensorList[3][0] != 2:
			if sensorList[3][1] != 3 :realTimeMap[centerY-1][centerX-3] = sensorList[3][1]; mapStateChanged[centerY-1][centerX-3] = "C"
			if sensorList[3][1] != 2:
				if sensorList[3][2] != 3 :realTimeMap[centerY-1][centerX-4] = sensorList[3][2]; mapStateChanged[centerY-1][centerX-4] = "C"
				if sensorList[3][2] != 2:
					if sensorList[3][3] != 3 :realTimeMap[centerY-1][centerX-5] = sensorList[3][3]; mapStateChanged[centerY-1][centerX-5] = "C"
		
		if sensorList[4][0] != 3 :realTimeMap[centerY+2][centerX-1] = sensorList[4][0]; mapStateChanged[centerY+2][centerX-1] = "C"
		if sensorList[4][0] != 2:
			if sensorList[4][1] != 3 :realTimeMap[centerY+3][centerX-1] = sensorList[4][1]; mapStateChanged[centerY+3][centerX-1] = "C"
			if sensorList[4][1] != 2:
				if sensorList[4][2] != 3 :realTimeMap[centerY+4][centerX-1] = sensorList[4][2]; mapStateChanged[centerY+4][centerX-1] = "C"
				if sensorList[4][2] != 2:
					if sensorList[4][3] != 3 :realTimeMap[centerY+5][centerX-1] = sensorList[4][3]; mapStateChanged[centerY+5][centerX-1] = "C"
		
		if sensorList[5][0] != 3 :realTimeMap[centerY-2][centerX-1] = sensorList[5][0]; mapStateChanged[centerY-2][centerX-1] = "C"
		if sensorList[5][0] != 2:
			if sensorList[5][1] != 3 :realTimeMap[centerY-3][centerX-1] = sensorList[5][1]; mapStateChanged[centerY-3][centerX-1] = "C"
			if sensorList[5][1] != 2:
				if sensorList[5][2] != 3 :realTimeMap[centerY-4][centerX-1] = sensorList[5][2]; mapStateChanged[centerY-4][centerX-1] = "C"
				if sensorList[5][2] != 2:
					if sensorList[5][3] != 3 :realTimeMap[centerY-5][centerX-1] = sensorList[5][3]; mapStateChanged[centerY-5][centerX-1] = "C"
		
		if sensorList[6][0] != 3 :realTimeMap[centerY+2][centerX+1] = sensorList[6][0]; mapStateChanged[centerY+2][centerX+1] = "C"
		if sensorList[6][0] != 2:
			if sensorList[6][1] != 3 :realTimeMap[centerY+3][centerX+1] = sensorList[6][1]; mapStateChanged[centerY+3][centerX+1] = "C"
			if sensorList[6][1] != 2:
				if sensorList[6][2] != 3 :realTimeMap[centerY+4][centerX+1] = sensorList[6][2]; mapStateChanged[centerY+4][centerX+1] = "C"
				if sensorList[6][2] != 2:
					if sensorList[6][3] != 3 :realTimeMap[centerY+5][centerX+1] = sensorList[6][3]; mapStateChanged[centerY+5][centerX+1] = "C"
	elif sensorList[0][0] == "R":
		if sensorList[1][0] != 3 :realTimeMap[centerY-1][centerX+2] = sensorList[1][0]; mapStateChanged[centerY-1][centerX+2] = "C"
		if sensorList[1][0] != 2:
			if sensorList[1][1] != 3 :realTimeMap[centerY-1][centerX+3] = sensorList[1][1]; mapStateChanged[centerY-1][centerX+3] = "C"
			if sensorList[1][1] != 2:
				if sensorList[1][2] != 3 :realTimeMap[centerY-1][centerX+4] = sensorList[1][2]; mapStateChanged[centerY-1][centerX+4] = "C"
				if sensorList[1][2] != 2:
					if sensorList[1][3] != 3 :realTimeMap[centerY-1][centerX+5] = sensorList[1][3]; mapStateChanged[centerY-1][centerX+5] = "C"
		
		if sensorList[2][0] != 3 :realTimeMap[centerY][centerX+2] = sensorList[2][0]; mapStateChanged[centerY][centerX+2] = "C"
		if sensorList[2][0] != 2:
			if sensorList[2][1] != 3 :realTimeMap[centerY][centerX+3] = sensorList[2][1]; mapStateChanged[centerY][centerX+3] = "C"
			if sensorList[2][1] != 2:
				if sensorList[2][2] != 3 :realTimeMap[centerY][centerX+4] = sensorList[2][2]; mapStateChanged[centerY][centerX+4] = "C"
				if sensorList[2][2] != 2:
					if sensorList[2][3] != 3 :realTimeMap[centerY][centerX+5] = sensorList[2][3]; mapStateChanged[centerY][centerX+5] = "C"
		
		if sensorList[3][0] != 3 :realTimeMap[centerY+1][centerX+2] = sensorList[3][0]; mapStateChanged[centerY+1][centerX+2] = "C"
		if sensorList[3][0] != 2:
			if sensorList[3][1] != 3 :realTimeMap[centerY+1][centerX+3] = sensorList[3][1]; mapStateChanged[centerY+1][centerX+3] = "C"
			if sensorList[3][1] != 2:
				if sensorList[3][2] != 3 :realTimeMap[centerY+1][centerX+4] = sensorList[3][2]; mapStateChanged[centerY+1][centerX+4] = "C"
				if sensorList[3][2] != 2:
					if sensorList[3][3] != 3 :realTimeMap[centerY+1][centerX+5] = sensorList[3][3]; mapStateChanged[centerY+1][centerX+5] = "C"
		
		if sensorList[4][0] != 3 :realTimeMap[centerY-2][centerX+1] = sensorList[4][0]; mapStateChanged[centerY-2][centerX+1] = "C"
		if sensorList[4][0] != 2:
			if sensorList[4][1] != 3 :realTimeMap[centerY-3][centerX+1] = sensorList[4][1]; mapStateChanged[centerY-3][centerX+1] = "C"
			if sensorList[4][1] != 2:
				if sensorList[4][2] != 3 :realTimeMap[centerY-4][centerX+1] = sensorList[4][2]; mapStateChanged[centerY-4][centerX+1] = "C"
				if sensorList[4][2] != 2:
					if sensorList[4][3] != 3 :realTimeMap[centerY-5][centerX+1] = sensorList[4][3]; mapStateChanged[centerY-5][centerX+1] = "C"
		
		if sensorList[5][0] != 3 :realTimeMap[centerY+2][centerX+1] = sensorList[5][0]; mapStateChanged[centerY+2][centerX+1] = "C"
		if sensorList[5][0] != 2:
			if sensorList[5][1] != 3 :realTimeMap[centerY+3][centerX+1] = sensorList[5][1]; mapStateChanged[centerY+3][centerX+1] = "C"
			if sensorList[5][1] != 2:
				if sensorList[5][2] != 3 :realTimeMap[centerY+4][centerX+1] = sensorList[5][2]; mapStateChanged[centerY+4][centerX+1] = "C"
				if sensorList[5][2] != 2:
					if sensorList[5][3] != 3 :realTimeMap[centerY+5][centerX+1] = sensorList[5][3]; mapStateChanged[centerY+5][centerX+1] = "C"
		
		if sensorList[6][0] != 3 :realTimeMap[centerY-2][centerX-1] = sensorList[6][0]; mapStateChanged[centerY-2][centerX-1] = "C"
		if sensorList[6][0] != 2:
			if sensorList[6][1] != 3 :realTimeMap[centerY-3][centerX-1] = sensorList[6][1]; mapStateChanged[centerY-3][centerX-1] = "C"
			if sensorList[6][1] != 2:
				if sensorList[6][2] != 3 :realTimeMap[centerY-4][centerX-1] = sensorList[6][2]; mapStateChanged[centerY-4][centerX-1] = "C"
				if sensorList[6][2] != 2:
					if sensorList[6][3] != 3 :realTimeMap[centerY-5][centerX-1] = sensorList[6][3]; mapStateChanged[centerY-5][centerX-1] = "C"
					
	for tup in pathTaken:
		if tup == (robotCenterY, robotCenterX):
			mapStateChanged[robotCenterY,robotCenterX] = "F"
			mapStateChanged[robotCenterY+1,robotCenterX+1] = "F"
			mapStateChanged[robotCenterY-1,robotCenterX-1] = "F"
			mapStateChanged[robotCenterY+1,robotCenterX-1] = "F"
			mapStateChanged[robotCenterY-1,robotCenterX+1] = "F"
			mapStateChanged[robotCenterY,robotCenterX+1] = "F"
			mapStateChanged[robotCenterY,robotCenterX-1] = "F"
			mapStateChanged[robotCenterY+1,robotCenterX] = "F"
			mapStateChanged[robotCenterY-1,robotCenterX] = "F"
	return realTimeMap
	
def robotMovementAnalyses(realTimeMap, CenterX, CenterY, direction, prevMov, sensorList):
	#print (direction)
	if direction == "U":
		if sensorList[4][0] != 3 and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1 and prevMov != "A":
			resultMovement = "A"
		elif sensorList[1][0] != 3 and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1:
			resultMovement = "W"
		elif sensorList[5][0] != 3 and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1:
			resultMovement = "D"
		else:
			resultMovement = "A"
	elif direction == "D":
		if sensorList[4][0] != 3 and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1 and prevMov != "A":
			resultMovement = "A"
		elif sensorList[1][0] != 3 and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1:
			resultMovement = "W"
		elif sensorList[5][0] != 3 and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1:
			resultMovement = "D"
		else:
			resultMovement = "A"
	elif direction == "L":
		if sensorList[4][0] != 3 and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1 and prevMov != "A":
			resultMovement = "A"
		elif sensorList[1][0] != 3 and realTimeMap[CenterY-1][CenterX-2] == 1 and realTimeMap[CenterY][CenterX-2] == 1 and realTimeMap[CenterY+1][CenterX-2] == 1:
			resultMovement = "W"
		elif sensorList[5][0] != 3 and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1:
			resultMovement = "D"
		else:
			resultMovement = "A"
	elif direction == "R":
		if sensorList[4][0] != 3 and realTimeMap[CenterY-2][CenterX-1] == 1 and realTimeMap[CenterY-2][CenterX] == 1 and realTimeMap[CenterY-2][CenterX+1] == 1 and prevMov != "A":
			resultMovement = "A"
		elif sensorList[1][0] != 3 and realTimeMap[CenterY-1][CenterX+2] == 1 and realTimeMap[CenterY][CenterX+2] == 1 and realTimeMap[CenterY+1][CenterX+2] == 1:
			resultMovement = "W"
		elif sensorList[5][0] != 3 and realTimeMap[CenterY+2][CenterX-1] == 1 and realTimeMap[CenterY+2][CenterX] == 1 and realTimeMap[CenterY+2][CenterX+1] == 1:
			resultMovement = "D"
		else:
			resultMovement = "A"
	print (resultMovement)
	return resultMovement
	
def robotAngleAndDistanceAlignment(sensorList):
	# L = left angle alignment
	# Q = left distance alignment (Includes rotate left and right back)
	# F = front angle alignment
	# W = front distance alignment
	# return list of alignment actions. Empty list means no alignment required
	if (sensorList[1][0] == 2 or sensorList[1][0] == 3) and (sensorList[3][0] == 2 or sensorList[3][0] == 3)  and (sensorList[4][0] == 2 or sensorList[4][0] == 3) and (sensorList[6][0] == 2 or sensorList[6][0] == 3):
		return ["W","Q","L"]
	elif(sensorList[1][0] == 2 or sensorList[1][0] == 3) and (sensorList[3][0] == 2 or sensorList[3][0] == 3):
		return ["F","W"]
	elif(sensorList[4][0] == 2 or sensorList[4][0] == 3) and (sensorList[6][0] == 2 or sensorList[6][0] == 3):
		return ["Q","L"]
	else:
		return []
	
def executeRobotMovement(realTimeMap, CenterX, CenterY, direction, movement):
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
	
def mapStateAnalysis(oldMap):
	#compare before executing new movement
	global realTimeMap
	global mapState
	global mapStateChanged
		
	for i in range(0,20):
		for j in range(0,15):  
			if mapStateChanged[i][j] == "F":
				if mapState[i][j] == 2 or mapState[i][j] == 1:
					mapState[i][j] = 1
					realTimeMap[i][j] = 1
			elif realTimeMap[i][j] != 4 and realTimeMap[i][j] != 5 and mapStateChanged[i][j] == "C":
				if realTimeMap[i][j] == 2 and oldMap[i][j] == 0:
					mapState[i][j] = 3 #assign new state
				elif realTimeMap[i][j] == 1 and oldMap[i][j] == 0:
					mapState[i][j] = 2 #assign new state
				elif realTimeMap[i][j] == 1 and oldMap[i][j] == 1 and mapState[i][j] == 2:
					mapState[i][j] = 1 #(-1)
				elif realTimeMap[i][j] == 1 and oldMap[i][j] == 1 and mapState[i][j] == 1:
					mapState[i][j] = 1 #constant
				elif realTimeMap[i][j] == 2 and oldMap[i][j] == 2 and mapState[i][j] == 3:
					mapState[i][j] = 4 #(+1)
				elif realTimeMap[i][j] == 2 and oldMap[i][j] == 2 and mapState[i][j] == 4:
					mapState[i][j] = 4 #constant
				elif realTimeMap[i][j] == 2 and oldMap[i][j] == 1 and mapState[i][j] == 1:
					mapState[i][j] = mapState[i][j] + 1 #changed in state but current state at extreme end
				elif realTimeMap[i][j] == 1 and oldMap[i][j] == 2 and mapState[i][j] == 4:
					mapState[i][j] = mapState[i][j] - 1 #changed in state but current state at extreme end
				elif realTimeMap[i][j] == 2 and oldMap[i][j] == 1 and mapState[i][j] == 2:
					mapState[i][j] = mapState[i][j] + 1 #changed in state and current state in middle
					realTimeMap[i][j] = 2
				elif realTimeMap[i][j] == 1 and oldMap[i][j] == 2 and mapState[i][j] == 3:
					mapState[i][j] = mapState[i][j] - 1 #changed in state and current state in middle
					realTimeMap[i][j] = 1
			
def getRealTimeMap():
	global robotCurMovement
	global realTimeMap
	main()
	return (realTimeMap, robotCurMovement, alignmentAction)