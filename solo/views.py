from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from solo.models import Game
import time
from random import randint
import math
import json

newGame = False

lastMove = [None, None, None]

mapSizeX = 16
mapSizeY = 16

mapArray = None
underArray = None

mines = None
flags = None

currentGame = None


gameState =0
#0 - Playing
#3 - Win
#2 - Lose


def index(request):

	return render(request, 'solo/index.html')

def loadGame(request):
	
	if currentGame == None:
		return redirect('index')
				
	return render(request, 'solo/game.html')
	
def startGame(request):

	global mapArray
	global mapSizeX
	global mapSizeY
	global underArray
	global mines
	global flags
	global gameState
	global currentGame
	
	global newGame
	newGame = True
	
	mines = None
	flags = []
	gameState = 0
	
	if request.method == "POST" : 
		mapSizeX = int(request.POST["gridSizeX"])
		mapSizeY = int(request.POST["gridSizeY"])
		
		
	mapArray = []
	
	for cnt1 in range(mapSizeY):
		mapArray.append([])
		for cnt2 in range(mapSizeX):
			mapArray[cnt1].append(None)
	
	
	underArray = []
			
	for cnt1 in range(mapSizeY):
		underArray.append([])
		for cnt2 in range(mapSizeX):
			underArray[cnt1].append(0)
	
	
	currentGame = Game(	
		MapSizeX = mapSizeX,
		MapSizeY = mapSizeY,
		MapArray = json.dumps(mapArray),
		UnderArray = json.dumps(underArray),
		GameState = gameState,
		Mines = json.dumps(mines),
		Flags = json.dumps(flags))
	currentGame.save()

	return redirect('/loadGame/')

	
def setupGame(request):
	
	
	
	return JsonResponse([mapSizeX,mapSizeY], safe=False)

def updateMap(request):



	return JsonResponse(mapArray, safe=False)
	
	
def getGameState(request):

	return JsonResponse(gameState, safe=False)


def leftClick(request):

	global mapArray
	global gameState
	
	if(request.method == "GET"):
		x = int(request.GET["x"])
		y = int(request.GET["y"])
		
		if mines == None:
			createMines(y, x)
		
		if underArray[y][x] == 9:
			gameState = 2
			mapArray[y][x] = underArray[y][x]
		else:
			clearTiles(y, x)
	
		lastMove[0] = 1
		lastMove[1] = y
		lastMove[2] = x
		updateDataBase()
	
	return JsonResponse(mapArray, safe=False)


def rightClick(request):

	global flags
	if(mines != None):
		if(request.method == "GET"):
			x = int(request.GET["x"])
			y = int(request.GET["y"])

			if(mapArray[y][x] == None):
				mapArray[y][x] = -1
				flags.append([y, x])
				compareFlags()
			else:
				mapArray[y][x] = None
				for f in flags:
					if f[0] == y and f[1] == x:
						f[0] = -100
						f[1] = -100
			
			
			lastMove[0] = 2
			lastMove[1] = y
			lastMove[2] = x
	
	return JsonResponse(mapArray, safe=False)

	
def undo(request):

	global gameState;
	
	#1- leftClick
	#2- rightClick

	if(lastMove[0] == 1):
		undoClearTiles(lastMove[1],lastMove[2])
	
	if(lastMove[0] == 2):
		if(mapArray[lastMove[1]][lastMove[2]] == None):
			mapArray[lastMove[1]][lastMove[2]] = -1
		else:
			mapArray[lastMove[1]][lastMove[2]] = None
			for f in flags:
				if f[0] == lastMove[1] and f[1] == lastMove[2]:
					f[0] = -100
					f[1] = -100

	lastMove[0] = None
	lastMove[1] = None
	lastMove[2] = None
	
	gameState = 0
	
	return JsonResponse(mapArray, safe=False)

	
def createMines(y, x):
	global mines
	mines = []
		
	for cnt1 in range(math.floor(mapSizeX*mapSizeY/8)):
		tempMine = [None, None]
		while True:
			tempMine = [randint(0,mapSizeY-1),randint(0,mapSizeX-1)]
			if tempMine[0] != y and tempMine[1] != x:
				break
			
			for m in mines:
				if m[0] == tempMine[0] and m[1] == tempMine[1]:
					break
		
		mines.append(tempMine)
		underArray[tempMine[0]][tempMine[1]] = 9
		
		for cnt1 in range(-1,2):
			for cnt2 in range(-1,2):
				if cnt1+tempMine[0] in range(mapSizeY) and cnt2+tempMine[1] in range(mapSizeX):
					if underArray[cnt1+tempMine[0]][cnt2+tempMine[1]] != 9:
						underArray[cnt1+tempMine[0]][cnt2+tempMine[1]] += 1
	
	
	
	pass
	
	
def clearTiles(y, x):
	
	if underArray[y][x] != 9:
		mapArray[y][x] = underArray[y][x]
	
	if underArray[y][x] == 0:
		for cnt1 in range(-1,2):
			for cnt2 in range(-1,2):
				if cnt1+y in range(mapSizeY) and cnt2+x in range(mapSizeX):
					if mapArray[cnt1+y][cnt2+x] != 0:
						clearTiles(cnt1+y,cnt2+x)

	pass
	
	
def undoClearTiles(y, x):

	global mapArray
	
	if mapArray[y][x] != None:
		mapArray[y][x] = None
		print("L1")
		if mapArray[y][x] == 0:
			print("L2")
			for cnt1 in range(-1,2):
				print("L3")
				for cnt2 in range(-1,2):
					print("L4")
					if cnt1+y in range(mapSizeY) and cnt2+x in range(mapSizeX):
						clearTiles(cnt1+y,cnt2+x)
	
	pass
	
	
def compareFlags():
	
	global gameState
	
	mineAmount = len(mines)
	hitCnt = 0
	
	for f in flags:
		for m in mines:
			if f[0] == m[0] and m[1] == f[1]:
				hitCnt += 1
	
	if hitCnt == mineAmount:
		gameState = 3
	
	
	pass
	
	
def updateDataBase():

	currentGame.MapArray = json.dumps(mapArray)
	currentGame.GameState = gameState
	currentGame.Mines = json.dumps(mines)
	currentGame.Flags = json.dumps(flags)
	currentGame.save()
	
	pass

























	
	
	
	
	
	
	
