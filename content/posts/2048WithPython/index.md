+++
title = "2048 with Python"
description = "This python script will create 2048 game Board"
date = 2020-04-17T07:34:48+08:30
featured = false
draft = false
comment = false
toc = false
reward = false
categories = [
  "Game"
]
tags = [
  "",
  ""
]
series = []
images = []
+++
### Introduction 
Hey mates😊. How are you? Hope you all begin well. Do you know 2048 game? Yeah! Of course, everyone knew that. Ok then, Let me create it on my own 🥲.

#### Why I'm doing this GameBoard?
Actually, One of my seniors in my college asked me to do this for their exam. That senior need to submit this GameBoard code which is written in python to get selected for InterView in OffCampus placement. OMG author, Did seniors asks you to code their project? Yes, but some seniors only 🥱. Is it true😬? Ofcourse yes rey🤫. But .. ? Just stop asking question🤧?
```
```
#### Lets Code it.
Total number of blocks in 2048 is 16 which is looks like 4x4 matrix. First of all we need a empty board to start the game. So we have to create a empty 2D array of length 4 and width also 4. And at starting of the game we also need to generate the board with a value 2 at random place.
```python3
import random

emptyIndexCount = 16
gameBoard = [	[0, 0, 0, 0],
				[0, 0, 0, 0],
				[0, 0, 0, 0],
				[0, 0, 0, 0]         ]
seedIndex = random.randint(1,16)
gameBoard[seedIndex_//4][seedIndex_-4*(seedIndex_//4)] = 2
print(gameBoard)

```
       [[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 2, 0, 0],
		[0, 0, 0, 0]]
		
Now our initial step to build gameBoard is successfully done. So Now going to step2,
In step 2 user need to give input to gameBoard. Initially let work on left move. So when user gives left Input then what we need to do is remove empty indexes and collect others values in each row and shift them to left.
ex: for above array after left shift

		[[0, 0, 0, 0],
		[0, 0, 0, 0],
		[2, 0, 0, 0],
		[0, 0, 0, 0]]

After shifting value to left we need to add values if corresponding index holded values are same and move to left by 1 index.

	[[0,2,2,4]] => [[2,2,4,0]] => [[4,4,0,0,]]

lets implement this
```python3
userInput_ = input("1-up/2-down/3-right/4-left: ")
if int(userInput_) == 4:
		for i in range(4):
			columnList = gameBoard[i]
			_backupList = [i for i in columnList if i!=0]+[0,0,0,0]
			_backupList = _backupList[0:4]
			print()
			gameBoard[i] = _backupList
			
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

```
In the above code I have checked that if corresponding values in the resultant array is matched then I add them and replace the result sum with first indexed value.

	[[0,2,4,4]] => [[2,4,4]]+[[0]] => [[2,4,4,0]] => [[2,8,0,0]]

Huh! Irritating arrays right? haha .. yes but very easy. And one more thing Now we have to generate another number in random position in gameBoard. So, first we need to take list of empty indexes and the count of that list. And that random number is between 0 to maxnumber which is existed in gameBoard.
```python3
seedNumber_ = [2,4,8,16,32,64,128,254,512,1024,2048]
maxNumber = 0
count_=0
index = []
indexCount = 0
for row in gameBoard:
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
print(gameBoard)
```
This will generate the new random value in any of the empty indexes.

		[[0, 0, 0, 0],
		[0, 0, 2, 0],  ==> generated random value at gameBoard[1][2] position
		[2, 0, 0, 0],
		[0, 0, 0, 0]]

Okay! Same for the right but the list is reversed in above code's first if condition
```python3
userInput_ = input("1-up/2-down/3-right/4-left: ")
if int(userInput_) == 3:
		for i in range(4):
			columnList = gameBoard[i]
			_backupList = [i for i in columnList if i!=0]+[0,0,0,0]
			_backupList = _backupList[0:4][::-1]
			print()
			gameBoard[i] = _backupList
			
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
```
This will throw value in gameboard to right side and new random value also generated because of loop.

		[[0, 0, 0, 0],
		[0, 0, 0, 2], 
		[0, 2, 0, 2],  ==> generated random value at gameBoard[2][1] position
		[0, 0, 0, 0]]
We are completed the Left and Right key operation to 2048 gameBoard. Now, we need to perform Up and Down key to the gameBoard. So
let us do for UP key first

When Up key presses what happends in gameBoard? 

[2048GameBoard.py](files/2048.py)

Hope you guys like and Subscribe to this Utube account 😂😂.

---
```
```
##### Thanks for reading! {align=center}
