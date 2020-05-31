import pygame, random, sys
from pygame.locals import *
# Started on 2/26/2020, revisited/finished on 5/31/2020 at 6:50 PM.

# The 'Best' score is not actually implemented yet.

#Initialize all imported pygame modules.
pygame.init()

#Define game variables.
scoreMarg = 50
WIN_WIDTH = 550
WIN_HEIGHT = 550 + scoreMarg
backgroudColour = (187, 173, 160)

timeElapsed = 0
clock = pygame.time.Clock()

cursorEvent = pygame.event.poll()

gameOver = False

gameArray = []
# for rows in range(4):
# 	gameArray.append([0, 0, 0, 0])
gameArray = [
[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0]
]
score = 0
numbahObjects = []
colors = [(238, 228, 218), (237, 224, 200), (242, 177, 121), (245, 149, 99), (246, 124, 95), (246, 94, 59), (237, 206, 115), (237, 204, 97), (237, 198, 81), (238, 199, 68), (236, 194, 46), (254, 61, 62), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33), (255, 32, 33)]

#Set up the Pygame window.
gameDisplay = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('2048')

gameDisplay.fill(backgroudColour)

# Reusable function to return desired text object, which can be displayed.
def drawText(labelText, xPos, yPos, labelType, size):
	color = (120, 111, 102)
	if labelType == "gray":
		color = (255, 255, 255)
	font = pygame.font.Font('freesansbold.ttf', size)
	text = font.render(labelText, True, color)
	textRect = text.get_rect()
	#textRect.center = (xPos // 2, yPos // 2)
	textRect.center = (xPos, yPos)
	return gameDisplay.blit(text, textRect)


class NUMBAH():
	def __init__(self, value, row, col):
		self.value = value
		self.row = row
		self.col = col
		self.gameArea = 4-1 # 3 (Index version)
		self.alreadyCombined = False

		gameArray[self.row][self.col] = self.value

	def draw(self):
		global gameArray
		if self.row <= self.gameArea and self.col <= self.gameArea and self.row >= 0 and self.col >= 0:
			gameArray[self.row][self.col] = self.value
		else: print("BADDDDDDDD Col: " + str(self.col) + ", and Row: " + str(self.row))

	def selfDestruct(self, otherRow, otherCol):
		global numbahObjects, gameArray, score
		print('destroying')
		gameArray[self.row][self.col] = 0
		gameArray[otherRow][otherCol] = 0
		newNum = self.value*2

		it = 0
		for obj in numbahObjects:
			it+=1
			if self.col == obj.col and self.row == obj.row:
				numbahObjects.pop(it-1)

		itt = 0
		for obj in numbahObjects:
			itt+=1
			if otherCol == obj.col and otherRow == obj.row:
				numbahObjects.pop(itt-1)

		numbahObjects.append(NUMBAH(newNum, otherRow, otherCol))
		score+=newNum
		numbahObjects[len(numbahObjects)-1].alreadyCombined = True

		# for obj in numbahObjects:
		# 	print(obj.alreadyCombined)

	def moveDown(self):
		global gameArray, anyMoves
		startRow = self.row
		if self.row < self.gameArea:
			#print('I AM: ' + str(self.value))

			for row in range(self.row+1, self.gameArea+1):
				#print('value: ' + str(gameArray[row][self.col]), end=", ")
				# if gameArray[row][self.col] == 0:
				# 	continue
				if gameArray[row][self.col] == self.value:
				
					#print('stop: ' + str(gameArray[row][self.col]))
					# self.selfDestruct(row, self.col)
					for obj in numbahObjects:
						if row == obj.row and self.col == obj.col:
							if obj.alreadyCombined == False:
								#Make a new combo block thing here yahuurd
								anyMoves = True
								self.selfDestruct(row, self.col)
							elif obj.alreadyCombined == True:
								
								gameArray[self.row][self.col] = 0
								self.row = row-1
								if self.row != startRow:
									anyMoves = True
								# self.draw()
					return

				elif gameArray[row][self.col] > 0 and gameArray[row][self.col] != self.value:
					#print('stop: ' + str(gameArray[row][self.col]))
					gameArray[self.row][self.col] = 0
					self.row = row-1
					if self.row != startRow:
						anyMoves = True
					self.draw()
					return
			#print('edge')
			anyMoves = True
			gameArray[self.row][self.col] = 0			
			self.row = self.gameArea
		gameArray[self.row][self.col] = self.value

	def moveUp(self):
		global gameArray, anyMoves

		startRow = self.row
		if self.row > 0:
			#print('I AM: ' + str(self.value))
			# gameArray[self.row][self.col] = 0
			for row in range(self.row-1,-1,-1):
				#print('value: ' + str(gameArray[row][self.col]), end=", ")
				# if gameArray[row][self.col] == 0:
				# 	continue
				if gameArray[row][self.col] == self.value:

					#Make a new combo block thing here yahuurd
					#print('stop: ' + str(gameArray[row][self.col]))
					# self.selfDestruct(row, self.col)
					for obj in numbahObjects:
						if row == obj.row and self.col == obj.col:
							if obj.alreadyCombined == False:
								anyMoves = True
								#Make a new combo block thing here yahuurd
								self.selfDestruct(row, self.col)
							elif obj.alreadyCombined == True:
								
								gameArray[self.row][self.col] = 0
								self.row = row+1
								if self.row != startRow:
									anyMoves = True
								# self.draw()
					return

				elif gameArray[row][self.col] > 0 and gameArray[row][self.col] != self.value:
					#print('stop: ' + str(gameArray[row][self.col]))
					gameArray[self.row][self.col] = 0
					self.row = row+1
					if self.row != startRow:
						anyMoves = True
					self.draw()
					return
			#print('edge')
			anyMoves = True
			gameArray[self.row][self.col] = 0
			self.row = 0
		self.draw()

	def moveRight(self):

		startCol = self.col
		global gameArray, anyMoves
		if self.col < self.gameArea:
			#print('I AM: ' + str(self.value))
			# /gameArray[self.row][self.col] = 0
			for col in range(self.col+1, self.gameArea+1):#range(self.col-1,-1,-1):
				#print('value: ' + str(gameArray[self.row][col]), end=", ")
				# if gameArray[row][self.col] == 0:
				# 	continue
				if gameArray[self.row][col] == self.value:
					#Make a new combo block thing here yahuurd
					#print('stop: ' + str(gameArray[self.row][col]))
					# self.selfDestruct(self.row, col)
					for obj in numbahObjects:
						if self.row == obj.row and col == obj.col:
							if obj.alreadyCombined == False:
								anyMoves = True
								#Make a new combo block thing here yahuurd
								self.selfDestruct(self.row, col)
							elif obj.alreadyCombined == True:
								
								gameArray[self.row][self.col] = 0
								self.col = col-1
								if self.col != startCol:
									anyMoves = True
								# self.draw()
					return

				elif gameArray[self.row][col] > 0 and gameArray[self.row][col] != self.value:
					#print('stop: ' + str(gameArray[self.row][col]))
					
					gameArray[self.row][self.col] = 0
					self.col = col-1
					if self.col != startCol:
						anyMoves = True
					self.draw()
					return
			#print('edge')
			anyMoves = True
			gameArray[self.row][self.col] = 0
			self.col = self.gameArea # Nothing in the way, reached the edge.
		self.draw() # Make sure to insert this into the array for other number blocks to see.

	def moveLeft(self):
		global gameArray, anyMoves

		startCol = self.col
		if self.col > 0:
			#print('I AM: ' + str(self.value))
			# gameArray[self.row][self.col] = 0
			for col in range(self.col-1,-1,-1):
				#print('value: ' + str(gameArray[self.row][col]), end=", ")
				# if gameArray[row][self.col] == 0:
				# 	continue
				if gameArray[self.row][col] == self.value:
					#Make a new combo block thing here yahuurd
					#print('stop: ' + str(gameArray[self.row][col]))
					# self.selfDestruct(self.row, col)
					for obj in numbahObjects:
						if self.row == obj.row and col == obj.col:
							if obj.alreadyCombined == False:
								anyMoves = True
								print('notCombined' + str(gameArray[self.row][col]))
								#Make a new combo block thing here yahuurd
								self.selfDestruct(self.row, col)
							elif obj.alreadyCombined == True:
								print('alreadyCombined' + str(gameArray[self.row][col]))
								gameArray[self.row][self.col] = 0
								self.col = col+1
								if self.col != startCol:
									anyMoves = True
								# //self.draw()
					return

				elif gameArray[self.row][col] > 0 and gameArray[self.row][col] != self.value:
					#print('stop: ' + str(gameArray[self.row][col])  + '\n')
					print(gameArray)
					print('different val' + str(gameArray[self.row][col]))
					gameArray[self.row][self.col] = 0
					self.col = col+1
					if self.col != startCol:
						anyMoves = True
					self.draw()
					return
			#print('edge')
			anyMoves = True
			gameArray[self.row][self.col] = 0
			self.col = 0 # Nothing in the way, reached the edge.
		self.draw()

numbahObjects.append(NUMBAH(2, 1, 0)) #val, row, col, indx

def getPower(num):
	count = 0
	while num > 1:
		count+=1
		num/=2
	return count


def drawGame():
	global numbahObjects
	global gameArray

	marg = 50
	square_Size = 110
	spacing = 1.16
	centerTxt = square_Size/4 + 3
	#gameDisplay.fill(backgroudColour)
	#print(str(numbahObjects[len(numbahObjects)-2].row))

	for row in range(4):
		for col in range(4):
			val = gameArray[row][col]
			fontType = None
			if val > 4:
				fontType = 'gray'
			if val > 0:
				pygame.draw.rect(gameDisplay, colors[getPower(val)], (int(col*spacing*square_Size) + int(marg/2), int((row*spacing*square_Size)) +int(marg/2), square_Size, square_Size))
			else:
				pygame.draw.rect(gameDisplay, (205, 193, 180), (int((col*spacing)*square_Size) + int(marg/2), int((row*spacing)*square_Size) +int(marg/2), square_Size, square_Size))
			drawText(str(gameArray[row][col]), (col*spacing)*(square_Size) + marg + centerTxt, (row*spacing)*(square_Size) + marg + centerTxt, fontType, 46)

	for i in numbahObjects:
		i.draw()


def drawScore():
	vertPos = WIN_HEIGHT-scoreMarg*0.75
	drawText('Score: ' + str(score), WIN_WIDTH/4, vertPos,'gray', 26)
	drawText('Best: ' + str(score), WIN_WIDTH*3/4, vertPos,'gray', 26)


def moveAllBlocks(direction):
	global numbahObjects, gameArray, anyMoves
	anyMoves = False
	# for obj in numbahObjects:
	# 	print(obj.alreadyCombined)
	# 	# obj.alreadyCombined = False

	if direction == "Up":
		for row in range(len(gameArray[0])):
			for column in range(len(gameArray[0])):
				if gameArray[row][column] > 0:
					for obj in numbahObjects:
						if row == obj.row and column == obj.col:
							obj.moveUp()


	elif direction == "Down":
		for row in range(len(gameArray[0])-1,-1,-1):
			for column in range(len(gameArray[0])):
				for obj in numbahObjects:
					if gameArray[row][column] > 0:
						if row == obj.row and column == obj.col:
							obj.moveDown()
	elif direction == "Right":
		for row in range(len(gameArray[0])):
			for column in range(len(gameArray[0])-1,-1,-1):			
				if gameArray[row][column] > 0:
					for obj in numbahObjects:
						if row == obj.row and column == obj.col:
							obj.moveRight()
	elif direction == "Left":
		# for i in range(len(gameArray[0])):
		# 	for i in numbahObjects:
		# 		i.draw()
		for row in range(len(gameArray[0])):
			for column in range(len(gameArray[0])):
				for obj in numbahObjects:
					if gameArray[row][column] > 0:
						if row == obj.row and column == obj.col:
							obj.moveLeft()

	for obj in numbahObjects:
		
		obj.alreadyCombined = False

	if anyMoves:
		spawn()

def spawn():
	global gameOver
	
	if not any(0 in sublist for sublist in gameArray):
		gameOver = True
		return

	xRand, yRand = random.randint(0, 3), random.randint(0, 3)
	while gameArray[yRand][xRand] != 0:
		xRand, yRand = random.randint(0, 3), random.randint(0, 3)

	numbahObjects.append(NUMBAH(2, yRand, xRand))

	# Spawn more blocks after this is done

def startGame():
	global gameOver, gameArray, numbahObjects, timeElapsed, score

	gameOver = False

	gameArray = [
	[0, 0, 0, 0],
	[0, 0, 0, 0],
	[0, 0, 0, 0],
	[0, 0, 0, 0]
	]
	numbahObjects = []

	timeElapsed, score = 0, 0

	gameLoop()

# Main loop to update and draw the game in gameDisplay.
def gameLoop():
	global gameOver,score
	global numbahObjects
	timeTracker = 0

	while not gameOver:
		timeTracker += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_q:
					pygame.quit()
				elif event.key == pygame.K_UP:
					moveAllBlocks("Up")#Go through the array from the down up
					drawGame()
				elif event.key == pygame.K_DOWN:
					# for i in numbahObjects:
					# 	i.moveDown()
					#Go through the array from the top down
					moveAllBlocks("Down")
					drawGame()
					# Spawn more blocks after this is done
				elif event.key == pygame.K_RIGHT:
					moveAllBlocks("Right")
					drawGame()			
					#Go through the array from the Left to right
					# Spawn more blocks after this is done
				elif  event.key == pygame.K_LEFT:
					moveAllBlocks("Left")#Go through the array from the right to left
					drawGame()
					# Spawn more blocks after this is done

		# # Do not update the images every single frame, however, key events are detected every frame.
		# if timeTracker % 10 == 0:
		# 	gameDisplay.fill(backgroudColour)
		gameDisplay.fill(backgroudColour)
		drawGame()
		drawScore()
		pygame.display.flip()	
		clock.tick(60)
		

	whiteOverlay = pygame.Surface((WIN_HEIGHT, WIN_HEIGHT))
	whiteOverlay.set_colorkey((255, 255, 255))
	whiteOverlay.set_alpha(70)
	pygame.draw.rect(whiteOverlay, (255, 255, 255), whiteOverlay.get_rect(),1)
	#Stop processing, wait for user to restart the game.
	while gameOver: 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				if  event.key == pygame.K_SPACE:
					startGame()
			
		gameDisplay.fill(backgroudColour)

		drawGame()
		
		gameDisplay.blit(whiteOverlay, (0, 0))
		drawText("Press space to restart.", WIN_WIDTH/2, (WIN_HEIGHT-scoreMarg)/2, 'gray', 26)

		pygame.display.flip()

		clock.tick(60)

gameLoop()