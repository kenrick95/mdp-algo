def main():
	oneRow = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	# realTimeMap[0] = bottom row
	# realTimeMap[19] = top row
	realTimeMap = []
	# simulatorMap[0] = bottom row
	# simulatorMap[19] = top row
	simulatorMap = []
	# sensorList[0] = frontleft
	# sensorList[1] = frontcenter
	# sensorList[2] = frontright
	# sensorList[3] = left
	# sensorList[4] = right
	# sensorList[5] = bottomleft
	sensorList = []
	
	repeatedArea = 0
	
	robotCenterX = 1
	robotCenterY = 1
	robotDirectionX = 2
	robotDirectionY = 1

	for i in range(0,20):
		realTimeMap.append(oneRow)
	
	for i in range(0,20):
		for j in range(0,15):
			print (realTimeMap[19-i][j],end="")
		print()
	
	simulatorMap = simulatorReadMap()
	for i in range(0,20):
		for j in range(0,15):
			print (simulatorMap[19-i][j],end="")
		print()
		
	#getSensor(simulatorMap, robotCenterX, robotCenterY, robotDirectionX, robotDirectionX)
		
def getSensor(simulatorMap, centerX, centerY, directionX, directionY):
	# returnValue[0] = direction of robot (W-Facing up, S-Facing down, A-facing left, D-facing right)
	# returnValue[1] = frontleft
	# returnValue[2] = frontcenter
	# returnValue[3] = frontright
	# returnValue[4] = left
	# returnValue[5] = right
	# returnValue[6] = bottomleft
	returnValue = []
	
	#W-Facing up
	if (centerY == directionY) and (directionY < centerY):
		returnValue.append([W])
		print(1)
	elif (centerY == directionY) and (directionY > centerY):
		returnValue.append([S])
		print(2)
	elif (centerX == directionX) and (directionX < centerX):
		returnValue.append([A])
		print(3)
	elif (centerX == directionX) and (directionX > centerX):
		returnValue.append([D])
		print(4)
	 
	
def simulatorReadMap():
	simulatorMap = []
	f = open("Simulator Real Map.txt","r")
	for line in f:
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