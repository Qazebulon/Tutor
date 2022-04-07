#! /usr/bin/python
import pygame, os, sys
import random
from pygame.locals import *
import os
import time as t

pygame.init()
pygame.display.set_caption('Great Learning Tools from makingit.click')
print("Learn to write game software here:  http://sloankelly.net/")
print("Get More Great Learning Tools here: http://makingit.click/")

newStudent = False				#-----------------------------
fileFound = False
while ((fileFound == False) and (newStudent==False)):
	#print(newStudent)
	# Get Student's Infornation
	studentName = raw_input("Enter Student's Name: ")
	fileName = 'student_data/M1_'+studentName
	#print('File: '+fileName)
	# Check if Found
	try:
		f = open(fileName, 'r')
		f.close()
		fileFound = True
	except IOError:
		fileFound = False
		answ = raw_input('New Student? (y/n): ')
		if ((answ=='y') or (answ=='Y')):
			#print(answ)
			newStudent=True
			#print(newStudent)	#-----------------------------


pygame.mixer.init()
berrySound = pygame.mixer.Sound('assets/audio/pluck.wav')		# 'playershoot.wav' 'pluck.wav')
crashSound = pygame.mixer.Sound('assets/audio/boing.wav')		# ('bonk.wav' 'boing.wav')
errorSound = pygame.mixer.Sound('assets/audio/disconnect.wav')	# ('disconnect.wav' 'floop.wav')
timerSound = pygame.mixer.Sound('assets/audio/phone.wav')		# ('buzzer.wav' 'phone.wav')
tadaSound  = pygame.mixer.Sound('assets/audio/chime.wav')		# ('chime.wav' 'tada.wav')

pygame.init()
fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((848, 480))
#surface = pygame.display.set_mode((720, 480)) # For Special Hardware

font = pygame.font.Font(None, 80)

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class GameData:
	def __init__(self):
		self.lives = 3
		self.isDead = False
		self.blocks = []
		self.tick = 250
		self.speed = 250
		self.level = 1
		self.berrycount = 0
		self.segments = 1
		self.frame = 0
		bx = random.randint(1, 38)
		by = random.randint(1, 28)
		self.berry = Position(bx, by)
		self.blocks.append(Position(20,15))
		self.blocks.append(Position(19,15))
		self.direction = 0 # 0 = right, 1 = left, 2 = up, 3 = down

def loadMapFile(fileName):
	f = open(fileName, 'r')
	content = f.readlines()
	f.close()
	return content

def headHitBody(gamedata):
	# Body crash
	head = gamedata.blocks[0]
	for b in gamedata.blocks:
		if (b != head):
			if(b.x == head.x and b.y == head.y):
				return True
	return False

def headHitWall(map, gamedata):
	# Wall crash
	row = 0
	for line in map:
		col = 0
		for char in line:
			if ( char == '1'):
				if (gamedata.blocks[0].x == col and gamedata.blocks[0].y == row):
					return True
			col += 1
		row += 1
	return False

def drawFont(surface, c, x, y):
	# 0-14: "0123456789?+x___"
        if (c==0): text = font.render("0",1,(64,64,64))
        elif (c==1): text = font.render("1",1,(180,90,0))
        elif (c==2): text = font.render("2",1,(255,60,50))
        elif (c==3): text = font.render("3",1,(255,170,70))
        elif (c==4): text = font.render("4",1,(255,255,60))
        elif (c==5): text = font.render("5",1,(000,255,050))
        elif (c==6): text = font.render("6",1,(000,150,255))
        elif (c==7): text = font.render("7",1,(100,50,255))
        elif (c==8): text = font.render("8",1,(128,128,128))
        elif (c==9): text = font.render("9",1,(255,255,255))
        elif (c==10): text = font.render("?",1,(0,128,0))
        elif (c==11): text = font.render("+",1,(0,255,255))
        elif (c==12): text = font.render("x",1,(255,0,225))
        else: text = font.render(".",1,(0,255,255))
        textpos=text.get_rect(left=x, top=y-60)
	surface.blit(text, textpos)

def drawDots(surface, c, x, y):
	y = y-60
	text = font.render(".",1,(0,128,0))
	if (c & 1):
		textpos=text.get_rect(left=x+15, top=y-15)
		surface.blit(text, textpos)
	if (c & 2 or c & 4 or c & 8):
		textpos=text.get_rect(left=x, top=y)
		surface.blit(text, textpos)
		textpos=text.get_rect(left=x+30, top=y-30)
		surface.blit(text, textpos)
	if (c & 4 or c & 8):
		textpos=text.get_rect(left=x, top=y-30)
		surface.blit(text, textpos)
		textpos=text.get_rect(left=x+30, top=y)
		surface.blit(text, textpos)
	if (((c & 6) == 6) or c & 8):
		textpos=text.get_rect(left=x, top=y-15)
		surface.blit(text, textpos)
		textpos=text.get_rect(left=x+30, top=y-15)
		surface.blit(text, textpos)
	if (c & 8):
		textpos=text.get_rect(left=x+15, top=y)
		surface.blit(text, textpos)
		textpos=text.get_rect(left=x+15, top=y-30)
		surface.blit(text, textpos)
	pygame.draw.rect(surface,(0,128,0),(x-8,y,60,61),4)


def drawMulti(surface, xx, yy, x, y):
	text = font.render(".",1,(0,128,0))
        for n in range (0, xx):
		for m in range (0, yy):
			textpos=text.get_rect(left=x+15*n, top=y+15*m)
			surface.blit(text, textpos)

def drawData(surface, gamedata):
	font = pygame.font.Font(None, 50)
	text = font.render("Level: %d" % ( gamedata.level ), 0, (0, 128, 0))
	textpos = text.get_rect(left=25, top=20)
	surface.blit(text, textpos)

	text = font.render(studentName, 0, (0, 128, 0))
	textpos = text.get_rect(left=335, top=20)
	surface.blit(text, textpos)

	font = pygame.font.Font(None, 80)
	text = font.render("http://makingit.click", 0, (0, 48, 0))
	textpos = text.get_rect(left=65, top=400)
	surface.blit(text, textpos)

def drawLevel(surface, problemlevel):
	font = pygame.font.Font(None, 48)
	if problemlevel==145:
		text = font.render("Level: Top!", 0, (0, 128, 0))
	else:
		text = font.render("Level: %d" % ( problemlevel-4 ), 0, (0, 128, 0))
	textpos = text.get_rect(left=650, top=20)
	surface.blit(text, textpos)
	font = pygame.font.Font(None, 80)

def drawError(surface):
	text = font.render("Error:", 0, (255, 0, 0))
	textpos = text.get_rect(left=517, top=280)
	surface.blit(text, textpos)

def drawFix(surface):
	text = font.render("Press Backspace Key", 0, (255, 0, 0))
	textpos = text.get_rect(left=92, top=280)
	surface.blit(text, textpos)

def drawWalls(surface, img, map):
	row = 0
	for line in map:
		col = 0
		for char in line:
			if ( char == '1'):
				imgRect = img.get_rect()
				imgRect.left = col * 16
				imgRect.top = row * 16
				surface.blit(img, imgRect)
			col += 1
		row += 1

def drawSnake(surface, img, gamedata):
	first = True
	for b in gamedata.blocks:
		dest = (b.x * 16, b.y * 16, 16, 16)
		if ( first ):
			first = False
			src = (((gamedata.direction * 2) + gamedata.frame) * 16, 0, 16, 16)
		else:
			src = (8 * 16, 0, 16, 16)
		surface.blit(img, dest, src)

def drawGame(surface,snakemap,data,level,rrect):
	surface.fill((0, 0, 0))
	drawWalls(surface, images['wall'], snakemap)
	drawData(surface, data)
	drawLevel(surface,level)
	surface.blit(images['berry'], rrect)
	drawSnake(surface, images['snake'], data)

def drawProblem(sutrface, topNum, BotNum, prb, ans):
	# 0-14: "0123456789?+x___"
	drawFont(surface, topNum, 710, 135) #T
	drawFont(surface, botNum, 710, 195) #B
	drawFont(surface, prb+10, 665, 190) #F
	pygame.draw.rect(surface,(0,128,0),(660,206,90,7)) #U
	if (prb==1): # dots if addition
		drawDots(surface, topNum, 768, 135)
		drawDots(surface, botNum, 768, 195)
	else:
		drawMulti(surface, topNum, botNum, 668, 260) # T x B rectangle
	# Draw Answer
	ans = ans % 100
	lsAns = ans % 10 # MS and LS Digits of ans
	msAns=(ans-lsAns)/10
	if (ans == 0): drawFont(surface, 10, 710, 280) #L
	else: drawFont(surface, lsAns, 710, 280) #L
	if (msAns>0): drawFont(surface, msAns, 671, 280) #M

def updateGame(gamedata, gameTime):
	gamedata.tick -= gameTime
	head = gamedata.blocks[0]
	if (gamedata.tick < 0):
		gamedata.tick += gamedata.speed
		gamedata.frame += 1
		gamedata.frame %= 2
		if (gamedata.direction == 0):
			move = (1, 0)
		elif (gamedata.direction == 1):
			move = (-1, 0)
		elif (gamedata.direction == 2):
			move = (0, -1)
		else:
			move = (0, 1)
		newpos = Position(head.x + move[0], head.y + move[1])
		first = True
		for b in gamedata.blocks:
			temp = Position(b.x, b.y)
			b.x = newpos.x
			b.y = newpos.y
			newpos = Position(temp.x, temp.y)
	# snake movement
	keys = pygame.key.get_pressed()
	if ((keys[K_RIGHT] or keys[K_KP6]) and gamedata.direction != 1):
		gamedata.direction = 0
	elif((keys[K_LEFT] or keys[K_KP4]) and gamedata.direction != 0):
		gamedata.direction = 1
	elif ((keys[K_UP]  or keys[K_KP8]) and gamedata.direction != 3):
		gamedata.direction = 2
	elif ((keys[K_DOWN] or keys[K_KP2] or keys[K_KP5]) and gamedata.direction != 2):
		gamedata.direction = 3

	# berry collision
	if (head.x == gamedata.berry.x and head.y == gamedata.berry.y):
		berrySound.play()	# (too slow?)
		global gameStatus
		gameStatus = 1 #1 (problem)
		lastIdx = len(gamedata.blocks) - 1
		for i in range(gamedata.segments):
			gamedata.blocks.append(Position(gamedata.blocks[lastIdx].x, gamedata.blocks[lastIdx].y))
		bx = random.randint(1, 38)
		by = random.randint(1, 28)
		gamedata.berry = Position(bx, by)
		gamedata.berrycount += 1
		if (gamedata.berrycount == 10):
			gamedata.berrycount = 0
			gamedata.speed -= 25
			gamedata.level += 1
			gamedata.segments *= 2
			if (gamedata.segments > 64):
				gamedata.segments = 64
			if (gamedata.speed < 100):
				gamedata.speed = 100

def loadImages():
	wall = pygame.image.load('assets/image/wall.png')
	raspberry = pygame.image.load('assets/image/berry.png')
	snake = pygame.image.load('assets/image/snake.png')
	return {'wall':wall, 'berry':raspberry, 'snake':snake}

# ***** Main code begins here *****
# load Math-Facts Array & initiate probability array:
f1 =  open('assets/text/math.txt','r')
math = []
probability = []
for line1 in f1:
	math.append(line1)
	probability.append(16384) # (for new students)
f1.close()
level = 4 		# starting level
topLevel = level	# top level acheived (so far)

# Load Old-Student Data
if (not newStudent):
	probability = []
	f = open(fileName, 'r')
	for line in f:
		probability.append(int(line))
		#sys.stdout.write(line) # (like end='') Test
	f.close()

# Load Game Graphics:
images = loadImages()
images['berry'].set_colorkey((255, 0, 255))
snakemap = loadMapFile('assets/text/map.txt')
data = GameData()
topNum = 1
botNum = 1
prb = 1
ans = 0
gameStatus = 0	# 0: game,  1: problem,  2: answer,  3: error,  4: fix
gameTime = 0	# (and time)

# Main Program loop:
while True:

	if (gameStatus == 0): # 0: game
		x = random.randint(1, 38)
		y = random.randint(1, 28)
		rrect = images['berry'].get_rect()
		rrect.left = data.berry.x * 16
		rrect.top = data.berry.y * 16
		for event in pygame.event.get():
			if event.type == QUIT:
				f=open(fileName, 'w')	#-----------------------------
				for n in range(0,145):
					f.write(str(probability[n])+'\n')
				f.close
				print('Updated')
				pygame.quit()
				sys.exit()

		# Do update stuff here
		updateGame(data, fpsClock.get_time())
		crashed = headHitWall(snakemap, data) or headHitBody(data)
		gameTime = gameTime+1
		if (gameTime > 1000):
			timerSound.play()	# (too slow?)
			gameStatus = 1		# 1: problem
		if (crashed):
			crashSound.play()	# (too slow)
			#positionBerry(data)
			data = None
			data = GameData()
			gameStatus = 1	# 1: problem
		else: # 0: game
			# Do drawing stuff here
			drawGame(surface,snakemap,data,level,rrect)
			drawProblem(surface, topNum, botNum, prb, ans)

	if (gameStatus==1): # 1: problem
		# Calculate level
		max = 65536
		sum = 0
		n = 0
		while (sum <= max) and (n < 145):
			sum = sum + probability[n]
			n = n+1
		level = n
		if (level>topLevel): topLevel=level	# update topLevel
		# Normalize top, if necessary:
		if (max > sum):
			max = sum
		# ***** Select the Problem *****
		sum = 0
		n = 0
		randNum = random.randint(0,max)
		# add until sum > randNum
		while (sum <= randNum):
			###print (n, max, randNum, sum, probability[144], probability[145]) # Debug Only ####
			sum = sum + probability[n]
			n = n+1
		select = n-1
		# load the problem's "word"
		word=math[select]	# [1+1,2+2 ... 8x9,9x9]
		### word = "5+7" ### test only

		# Present the Problem
		topNum = ord(word[0])-48 # ASCII to number
		botNum = ord(word[2])-48 # ASCII to number
		if word[1] == "+":
			prb = 1	# add to 1
			okAns = topNum + botNum
		else:
			prb = 2	# multiply to 2
			okAns = topNum * botNum
		ans = 0 # assume 0 input
		# Redraw the Game & problem
		drawGame(surface,snakemap,data,level,rrect)
		drawProblem(surface, topNum, botNum, prb, ans)
		gameStatus = 2 # 2: answer

	if (gameStatus==2): # 2: answer
		error=False
		#keys = pygame.key.get_pressed()
		#if (keys[K_SPACE]):
		#	gameStatus = 0 # game
		for event in pygame.event.get():
			if event.type == QUIT:
				f=open(fileName, 'w')	#-----------------------------
				for n in range(0,145):
					f.write(str(probability[n])+'\n')
				f.close
				print('Updated')
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				# print(event.key) # (to reveal uncommon keycodes: 271, 266)
				if ((event.key == pygame.K_RETURN) or (event.key == 271)):
					# Good Entry

					if (ans == okAns):
						tadaSound.play()
						probability[select]=probability[select]/16+1
						gameStatus = 0	# game
						gameTime = 0	# and time
						if (level<topLevel):
							gameStatus = 1	# or another problem
					# Bad Entry
					else:
						error=True
						errorSound.play()
						probability[select] = 16384 # limit
						gameStatus = 3 # error
				if ((event.key == pygame.K_BACKSPACE) or (event.key == 266)):
					ans = (ans - ans % 10)/10
				if ((event.key == pygame.K_0) or (event.key == pygame.K_KP0)):
                                        ans = ans * 10
				if ((event.key == pygame.K_1) or (event.key == pygame.K_KP1)):
                                        ans = ans * 10 + 1
				if ((event.key == pygame.K_2) or (event.key == pygame.K_KP2)):
                                        ans = ans * 10 + 2
				if ((event.key == pygame.K_3) or (event.key == pygame.K_KP3)):
                                        ans = ans * 10 + 3
				if ((event.key == pygame.K_4) or (event.key == pygame.K_KP4)):
					ans = ans * 10 + 4
				if ((event.key == pygame.K_5) or (event.key == pygame.K_KP5)):
					ans = ans * 10 + 5
				if ((event.key == pygame.K_6) or (event.key == pygame.K_KP6)):
					ans = ans * 10 + 6
				if ((event.key == pygame.K_7) or (event.key == pygame.K_KP7)):
					ans = ans * 10 + 7
				if ((event.key == pygame.K_8) or (event.key == pygame.K_KP8)):
					ans = ans * 10 + 8
				if ((event.key == pygame.K_9) or (event.key == pygame.K_KP9)):
					ans = ans * 10 + 9

		# Do drawing stuff here
		drawGame(surface,snakemap,data,level,rrect)
		drawProblem(surface, topNum, botNum, prb, ans)
		if error==True:
			drawError(surface) # <--- ERROR

	if gameStatus == 3: # error while sound busy -- then Fix
		if (pygame.mixer.get_busy()): pass
		else:	# Do drawing stuff here
			ans=okAns # Switch to corrected ansewer
			# and Display it
			drawGame(surface,snakemap,data,level,rrect)
			drawFix(surface) # <--- FIX
			drawProblem(surface, topNum, botNum, prb, ans)
			gameStatus = 4 # fix

	if gameStatus == 4: # Fix error and wait
		error=False
		# Continue to display that corrected answer until:
		keys = pygame.key.get_pressed()
		if (keys[K_BACKSPACE]):
			gameStatus = 1 # problem
		for event in pygame.event.get():
			if event.type == QUIT:
				f=open(fileName, 'w')	#-----------------------------
				for n in range(0,145):
					f.write(str(probability[n])+'\n')
				f.close
				print('Updated')
				pygame.quit()
				sys.exit()

	pygame.display.update()
	fpsClock.tick(30)
