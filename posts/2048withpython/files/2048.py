import random
gameBoard = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]



seedNumber_ = [2,4,8,16,32,64,128,254,512,1024,2048]



maxNumber_ = 0
while maxNumber_!=2048:
	count_=0
	index = []
	indexCount = 0
	for row in gameBoard:##############################################          random index fails #####
		for col in row:
			if col==0:
				count_+=1
				index.append(indexCount)
			if col>maxNumber_:
					maxNumber_ = col
			indexCount+=1
	seedIndex_ = random.choice(index)
	
	if maxNumber_==0:
		randomSeed_ = 2
	else:
		#print(random.choice(seedNumber_[0:seedNumber_.index(maxNumber_)+1]))
		randomSeed_ = random.choice(seedNumber_[0:seedNumber_.index(maxNumber_)+1])
#	print(maxNumber_)
	
	gameBoard[seedIndex_//4][seedIndex_-4*(seedIndex_//4)] = randomSeed_

	for row in gameBoard:
		print(row,end="\n")

	userInput_ = input("1-up/2-down/3-right/4-left: ")

	if int(userInput_) == 1:
		for i in range(4):
			columnList = [gameBoard[0][i],gameBoard[1][i],gameBoard[2][i],gameBoard[3][i]]
			_backupList = [i for i in columnList if i!=0]
			print()
			try:
				gameBoard[0][i]=_backupList[0]
			except:
				gameBoard[0][i]=0
			try:
				gameBoard[1][i]=_backupList[1]
			except:
				gameBoard[1][i]=0
			try:
				gameBoard[2][i]=_backupList[2]
			except:
				gameBoard[2][i]=0
			try:
				gameBoard[3][i]=_backupList[3]
			except:
				gameBoard[3][i]=0

				
		for i in range(4):
			if gameBoard[0][i] == gameBoard[1][i]:
				gameBoard[0][i] = gameBoard[0][i] + gameBoard[1][i]
				if gameBoard[2][i] == gameBoard[3][i]:
					gameBoard[1][i] = gameBoard[2][i] + gameBoard[3][i]
					gameBoard[2][i] = 0
					gameBoard[3][i] = 0
				else:
					gameBoard[1][i] = gameBoard[2][i]
					gameBoard[2][i] = gameBoard[3][i]
					gameBoard[3][i] = 0
			elif gameBoard[1][i] == gameBoard[2][i]:
				gameBoard[1][i] = gameBoard[1][i] + gameBoard[2][i]
				gameBoard[2][i] = gameBoard[3][i]
				gameBoard[3][i] = 0
			elif gameBoard[2][i] == gameBoard[3][i]:
				gameBoard[2][i] = gameBoard[2][i] + gameBoard[3][i]
				gameBoard[3][i] = 0
		
	elif int(userInput_) == 2:
		for i in range(4):
			columnList = [gameBoard[3][i],gameBoard[2][i],gameBoard[1][i],gameBoard[0][i]]
			_backupList = [i for i in columnList if i!=0]
			print()
			try:
				gameBoard[3][i]=_backupList[0]
			except:
				gameBoard[3][i]=0
			try:
				gameBoard[2][i]=_backupList[1]
			except:
				gameBoard[2][i]=0
			try:
				gameBoard[1][i]=_backupList[2]
			except:
				gameBoard[1][i]=0
			try:
				gameBoard[0][i]=_backupList[3]
			except:
				gameBoard[0][i]=0

				
		for i in range(4):
			if gameBoard[3][i] == gameBoard[2][i]:
				gameBoard[3][i] = gameBoard[3][i] + gameBoard[2][i]
				if gameBoard[1][i] == gameBoard[2][i]:
					gameBoard[2][i] = gameBoard[2][i] + gameBoard[1][i]
					gameBoard[1][i] = 0
					gameBoard[0][i] = 0
				else:
					gameBoard[2][i] = gameBoard[1][i]
					gameBoard[1][i] = gameBoard[0][i]
					gameBoard[0][i] = 0
			elif gameBoard[1][i] == gameBoard[2][i]:
				gameBoard[2][i] = gameBoard[1][i] + gameBoard[2][i]
				gameBoard[1][i] = gameBoard[0][i]
				gameBoard[0][i] = 0
			elif gameBoard[1][i] == gameBoard[0][i]:
				gameBoard[1][i] = gameBoard[1][i] + gameBoard[0][i]
				gameBoard[0][i] = 0
	elif int(userInput_) == 3:
		for i in range(4):
			columnList = gameBoard[i][::-1]
			_backupList = [i for i in columnList if i!=0]+[0,0,0,0]
			_backupList = _backupList[0:4]
			print()
			try:
				gameBoard[i][3]=_backupList[0]
			except:
				gameBoard[i][3]=0
			try:
				gameBoard[i][2]=_backupList[1]
			except:
				gameBoard[i][2]=0
			try:
				gameBoard[i][1]=_backupList[2]
			except:
				gameBoard[i][1]=0
			try:
				gameBoard[i][0]=_backupList[3]
			except:
				gameBoard[i][0]=0
		

		for i in range(4):
			if gameBoard[i][3] == gameBoard[i][2]:
				gameBoard[i][3] = gameBoard[i][3] + gameBoard[i][2]
				if gameBoard[i][1] == gameBoard[i][2]:
					gameBoard[i][2] = gameBoard[i][2] + gameBoard[i][1]
					gameBoard[i][1] = 0
					gameBoard[i][0] = 0
				else:
					gameBoard[i][2] = gameBoard[i][1]
					gameBoard[i][1] = gameBoard[i][0]
					gameBoard[i][0] = 0
			elif gameBoard[i][1] == gameBoard[i][2]:
				gameBoard[i][2] = gameBoard[i][1] + gameBoard[i][2]
				gameBoard[i][1] = gameBoard[i][0]
				gameBoard[i][0] = 0
			elif gameBoard[i][1] == gameBoard[i][0]:
				gameBoard[i][1] = gameBoard[i][1] + gameBoard[i][0]
				gameBoard[i][0] = 0

	elif int(userInput_) == 4:
		for i in range(4):
			columnList = gameBoard[i]
			_backupList = [i for i in columnList if i!=0]+[0,0,0,0]
			_backupList = _backupList[0:4]
			print()
			try:
				gameBoard[i][0]=_backupList[0]
			except:
				gameBoard[i][0]=0
			try:
				gameBoard[i][1]=_backupList[1]
			except:
				gameBoard[i][1]=0
			try:
				gameBoard[i][2]=_backupList[2]
			except:
				gameBoard[i][2]=0
			try:
				gameBoard[i][3]=_backupList[3]
			except:
				gameBoard[i][3]=0
		

		for i in range(4):
			if gameBoard[i][0] == gameBoard[i][1]:
				gameBoard[i][0] = gameBoard[i][1] + gameBoard[i][0]
				if gameBoard[i][1] == gameBoard[i][2]:
					gameBoard[i][1] = gameBoard[i][1] + gameBoard[i][2]
					gameBoard[i][2] = 0
					gameBoard[i][3] = 0
				else:
					gameBoard[i][1] = gameBoard[i][2]
					gameBoard[i][2] = gameBoard[i][3]
					gameBoard[i][3] = 0
			elif gameBoard[i][1] == gameBoard[i][2]:
				gameBoard[i][1] = gameBoard[i][1] + gameBoard[i][2]
				gameBoard[i][2] = gameBoard[i][3]
				gameBoard[i][3] = 0
			elif gameBoard[i][2] == gameBoard[i][3]:
				gameBoard[i][2] = gameBoard[i][2] + gameBoard[i][3]
				gameBoard[i][3] = 0
	else:
		break
	

