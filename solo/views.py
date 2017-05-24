from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
import time
from random import randint
import math

lastMove = [None, None, None]

mapSizeX = 10
mapSizeY = 16

mapArray = None
underArray = None

mines = None
flags = None

def index(request):

	return render(request, 'solo/index.html')

	
	
def startGame(request):

	global mapArray
	global mapSizeX
	global mapSizeY
	global underArray
	global mines
	global flags
	
	mines = None
	
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
	

	return render(request, 'solo/game.html')

def setupGame(request):
	
	
	
	return JsonResponse([mapSizeX,mapSizeY], safe=False)


def updateMap(request):



	return JsonResponse(mapArray, safe=False)
	
	
def leftClick(request):
	
	if(request.method == "GET"):
		x = int(request.GET["x"])
		y = int(request.GET["y"])

		mapArray[y][x] = underArray[y][x]
		
		if mines == None:
			createMines(y, x)
	
		lastMove[0] = 1
		lastMove[1] = y
		lastMove[2] = x
	
	return JsonResponse(mapArray, safe=False)
	

def rightClick(request):
	
	if(request.method == "GET"):
		x = int(request.GET["x"])
		y = int(request.GET["y"])

		if(mapArray[y][x] == None):
			mapArray[y][x] = -1
		else:
			mapArray[y][x] = None
		
		lastMove[0] = 2
		lastMove[1] = y
		lastMove[2] = x
	
	return JsonResponse(mapArray, safe=False)

def undo(request):
	

	
	
	#1- leftClick
	#2- rightClick

	if(lastMove[0] == 1):
		mapArray[lastMove[1]][lastMove[2]] = None
	
	if(lastMove[0] == 2):
		if(mapArray[lastMove[1]][lastMove[2]] == None):
			mapArray[lastMove[1]][lastMove[2]] = -1
		else:
			mapArray[lastMove[1]][lastMove[2]] = None

		lastMove[0] = None
		lastMove[1] = None
		lastMove[2] = None
	
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
		
		mines.append(tempMine)
		underArray[tempMine[0]][tempMine[1]] = 9
		for spotY in range(-1,2):
			for spotX in range(-1,2):
				if spotX != 0 and spotY != 0:
					underArray[tempMine[0] + ][spotX+tempMine[1]] += 1
		































	
	
	
	
	
	
	
