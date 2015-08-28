def main():
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
	
	repeatedArea = 0
	
	robotCenterX = 6
	robotCenterY = 18
	robotDirectionX = 7
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
		
	realTimeMap = updateRobotPosition(realTimeMap, robotCenterX, robotCenterY, robotDirectionX, robotDirectionY)
	
	for i in range(0,20):
		for j in range(0,15):
			print (realTimeMap[i][j],end="")
		print()
	
	simulatorMap = simulatorReadMap()
	for i in range(0,20):
		for j in range(0,15):
			print (simulatorMap[i][j],end="")
		print()
			
		
	sensorList = getSensor(simulatorMap, robotCenterX, robotCenterY, robotDirectionX, robotDirectionY)
	
	for i in range(0,7):
		print(sensorList[i])
		
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
	
	#W-Facing up
	if (centerX == directionX) and (directionY < centerY):
		returnValue.append(["W"])
		print(1)
	#S-Facing down
	elif (centerX == directionX) and (directionY > centerY):
		returnValue.append(["S"])
		print(2)
	#A-facing left
	elif (centerY == directionY) and (directionX < centerX):
		returnValue.append(["A"])
		print(3)
	#D-facing right
	elif (centerY == directionY) and (directionX > centerX):
		returnValue.append(["D"])
		print(4)
	
	if returnValue[0][0] == "W":
		returnValue.append([simMap[centerY-2][centerX-1], simMap[centerY-3][centerX-1], simMap[centerY-4][centerX-1], simMap[centerY-5][centerX-1]])
		returnValue.append([simMap[centerY-2][centerX], simMap[centerY-3][centerX], simMap[centerY-4][centerX], simMap[centerY-5][centerX]])
		returnValue.append([simMap[centerY-2][centerX+1], simMap[centerY-3][centerX+1], simMap[centerY-4][centerX+1], simMap[centerY-5][centerX+1]])
		returnValue.append([simMap[centerY-1][centerX-2], simMap[centerY-1][centerX-3], simMap[centerY-1][centerX-4], simMap[centerY-1][centerX-5]])
		returnValue.append([simMap[centerY-1][centerX+2], simMap[centerY-1][centerX+3], simMap[centerY-1][centerX+4], simMap[centerY-1][centerX+5]])
		returnValue.append([simMap[centerY+1][centerX-2], simMap[centerY+1][centerX-3], simMap[centerY+1][centerX-4], simMap[centerY+1][centerX-5]])
	elif returnValue[0][0] == "S":
		returnValue.append([simMap[centerY+2][centerX+1], simMap[centerY+3][centerX+1], simMap[centerY+4][centerX+1], simMap[centerY+5][centerX+1]])
		returnValue.append([simMap[centerY+2][centerX], simMap[centerY+3][centerX], simMap[centerY+4][centerX], simMap[centerY+5][centerX]])
		returnValue.append([simMap[centerY+2][centerX-1], simMap[centerY+3][centerX-1], simMap[centerY+4][centerX-1], simMap[centerY+5][centerX-1]])
		returnValue.append([simMap[centerY+1][centerX+2], simMap[centerY+1][centerX+3], simMap[centerY+1][centerX+4], simMap[centerY+1][centerX+5]])
		returnValue.append([simMap[centerY+1][centerX-2], simMap[centerY+1][centerX-3], simMap[centerY+1][centerX-4], simMap[centerY+1][centerX-5]])
		returnValue.append([simMap[centerY-1][centerX+2], simMap[centerY-1][centerX+3], simMap[centerY-1][centerX+4], simMap[centerY-1][centerX+5]])
	elif returnValue[0][0] == "A":
		returnValue.append([simMap[centerY-1][centerX-2], simMap[centerY-1][centerX-3], simMap[centerY-1][centerX-4], simMap[centerY-1][centerX-5]])
		returnValue.append([simMap[centerY][centerX-2], simMap[centerY][centerX-3], simMap[centerY][centerX-4], simMap[centerY][centerX-5]])
		returnValue.append([simMap[centerY+1][centerX-2], simMap[centerY+1][centerX-3], simMap[centerY+1][centerX-4], simMap[centerY+1][centerX-5]])
		returnValue.append([simMap[centerY+2][centerX-1], simMap[centerY+3][centerX-1], simMap[centerY+4][centerX-1], simMap[centerY+5][centerX-1]])
		returnValue.append([simMap[centerY-2][centerX-1], simMap[centerY-3][centerX-1], simMap[centerY-4][centerX-1], simMap[centerY-5][centerX-1]])
		returnValue.append([simMap[centerY+2][centerX+1], simMap[centerY+3][centerX+1], simMap[centerY+4][centerX+1], simMap[centerY+5][centerX+1]])
	elif returnValue[0][0] == "D":
		returnValue.append([2 if outOfBoundRight>=4 else simMap[centerY-1][centerX+2], 2 if outOfBoundRight>=3 else simMap[centerY-1][centerX+3], 2 if outOfBoundRight>=2 else simMap[centerY-1][centerX+4], 2 if outOfBoundRight>=1 else simMap[centerY-1][centerX+5]])
		returnValue.append([2 if outOfBoundRight>=4 else simMap[centerY][centerX+2], 2 if outOfBoundRight>=3 else simMap[centerY][centerX+3], 2 if outOfBoundRight>=2 else simMap[centerY][centerX+4], 2 if outOfBoundRight>=1 else simMap[centerY][centerX+5]])
		returnValue.append([2 if outOfBoundRight>=4 else simMap[centerY+1][centerX+2], 2 if outOfBoundRight>=3 else simMap[centerY+1][centerX+3], 2 if outOfBoundRight>=2 else simMap[centerY+1][centerX+4], 2 if outOfBoundRight>=1 else simMap[centerY+1][centerX+5]])
		returnValue.append([2 if outOfBoundUp>=4 else simMap[centerY-2][centerX+1], 2 if outOfBoundUp>=3 else simMap[centerY-3][centerX+1], 2 if outOfBoundUp>=2 else simMap[centerY-4][centerX+1], 2 if outOfBoundUp>=1 else simMap[centerY-5][centerX+1]])
		returnValue.append([2 if outOfBoundDown>=4 else simMap[centerY+2][centerX+1], 2 if outOfBoundDown>=3 else simMap[centerY+3][centerX+1], 2 if outOfBoundDown>=2 else simMap[centerY+4][centerX+1], 2 if outOfBoundDown>=1 else simMap[centerY+5][centerX+1]])
		returnValue.append([2 if outOfBoundUp>=4 else simMap[centerY-2][centerX-1], 2 if outOfBoundUp>=3 else simMap[centerY-3][centerX-1], 2 if outOfBoundUp>=2 else simMap[centerY-4][centerX-1], 2 if outOfBoundUp>=1 else simMap[centerY-5][centerX-1]])
		
	return returnValue
	
def updateRobotPosition(realTimeMap, robotCenterX, robotCenterY, robotDirectionX, robotDirectionY):
	realTimeMap[robotCenterY][robotCenterX] = 5
	realTimeMap[robotDirectionY][robotDirectionX] = 4
	return realTimeMap
	
def simulatorReadMap():
	simulatorMap = []
	for line in reversed(list(open("Simulator Real Map.txt","r"))):
		oneRow = []
		count = 1
		for num in line:
			if count > 15:
				break
			oneRow.append(num)
			count = count + 1
		simulatorMap.append(oneRow)
	print("Done")
	return simulatorMap