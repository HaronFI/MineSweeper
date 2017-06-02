from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from solo.models import Game, LeaderBoard
import time
from random import randint
import math
from json import dumps, loads
from channels import Group

mapSizeX = 16
mapSizeY = 16

mapArray = None
underArray = None
mapList = None

mines = None
flags = None


gameState =0

def index(request):
	return render(request, 'solo/index.html')

def loadGame(request, gameID = "1"):
	
	g = Game.objects.get(pk=gameID)
	
	gameState = g.GameState
	
	if(request.method == "GET"):
		name = request.GET.get('name', None)
		score = request.GET.get('score', None)
		
		if(name != None):
			l = LeaderBoard(Name=name, Score=score)
			l.save()
	
	if( gameState != 0 ):
		return redirect('index')

	return render(request, 'solo/game.html')
	
def startGame(request):
	
	mines = None
	flags = []
	gameState = 0
	mapList = []
	
	if request.method == "POST" : 
		mapSizeX = int(request.POST["gridSizeX"])
		mapSizeY = int(request.POST["gridSizeY"])
		
	mapArray = []
	underArray = []
	
	for cnt1 in range(mapSizeY):
		mapArray.append([])
		underArray.append([])
		for cnt2 in range(mapSizeX):
			mapArray[cnt1].append(None)
			underArray[cnt1].append(0)

	g = Game(	MapSizeX = mapSizeX,
				MapSizeY = mapSizeY,
				MapArray = dumps(mapArray),
				UnderArray = dumps(underArray),
				GameState = gameState,
				Mines = dumps(mines),
				Flags = dumps(flags),
				MapList = dumps(mapList)
			)
	
	g.save()
	
	return redirect('/loadGame/'+str(g.pk))
	
def getSize(request):
	
	g = Game.objects.get(pk=request.GET['gameID'])

	board = []
	
	for i in LeaderBoard.objects.all().order_by("-Score"):
		board.append([i.Name,i.Score])
	

	return JsonResponse([g.MapSizeX,g.MapSizeY,board], safe=False)
	
def getMap(request):
	g = Game.objects.get(pk=request.GET['gameID'])

	return JsonResponse(loads(g.MapArray), safe=False)
	
def getGameState(request):

	g = Game.objects.get(pk=request.GET['gameID'])

	score =  1000000 - (len(loads(g.MapList)) * math.floor(1000000/(g.MapSizeX * g.MapSizeY)))

	return JsonResponse([g.GameState,score], safe=False)

def leftClick(request):

	global mapArray
	global underArray
	global mapList
	global gameState
	global mapSizeX
	global mapSizeY
	global mines
	global flags
	
	g = Game.objects.get(pk=request.GET['gameID'])
	
	mapArray = loads(g.MapArray)
	underArray = loads(g.UnderArray)
	mapList = loads(g.MapList)
	mines = loads(g.Mines)
	flags = loads(g.Flags)
	gameState = g.GameState
	mapSizeX = g.MapSizeX
	mapSizeY = g.MapSizeY
	mapList = loads(g.MapList)
	
	
	if(request.method == "GET"):
		x = int(request.GET["x"])
		y = int(request.GET["y"])
		
		updateMapList()
		
		if mines == None:
			createMines(y, x)
		
		
		if underArray[y][x] == 9:
			gameState = 2
			mapArray[y][x] = underArray[y][x]
		else:
			clearTiles(y, x)
			winCheck()

	g.MapArray = dumps(mapArray)
	g.UnderArray = dumps(underArray)
	g.MapList = dumps(mapList)
	g.Mines = dumps(mines)
	g.Flags = dumps(flags)
	g.GameState = gameState
	g.mapList = dumps(mapList)
	
	g.save()
			
	return JsonResponse(mapArray, safe=False)

def rightClick(request):
	global mapArray
	global underArray
	global mapList
	global gameState
	global mapSizeX
	global mapSizeY
	global mines
	global flags
	
	g = Game.objects.get(pk=request.GET['gameID'])
	
	mapArray = loads(g.MapArray)
	underArray = loads(g.UnderArray)
	mapList = loads(g.MapList)
	mines = loads(g.Mines)
	gameState = g.GameState
	mapSizeX = g.MapSizeX
	mapSizeY = g.MapSizeY
	mapList = loads(g.MapList)
	
	if(mines != None):
		if(request.method == "GET"):
			x = int(request.GET["x"])
			y = int(request.GET["y"])
			
			updateMapList()

			if(mapArray[y][x] == None):
				mapArray[y][x] = -1
				flags.append([y, x])
			else:
				mapArray[y][x] = None
				for f in flags:
					if f[0] == y and f[1] == x:
						f[0] = -100
						f[1] = -100
		
		g.MapArray = dumps(mapArray)
		g.UnderArray = dumps(underArray)
		g.MapList = dumps(mapList)
		g.Mines = dumps(mines)
		g.Flags = dumps(flags)
		g.GameState = gameState
		g.mapList = dumps(mapList)
	
		g.save()
	return JsonResponse(mapArray, safe=False)

def undo(request):

	global mapArray
	global underArray
	global mapList
	global gameState
	global mapSizeX
	global mapSizeY
	
	g = Game.objects.get(pk=request.GET['gameID'])
	
	mapArray = loads(g.MapArray)
	underArray = loads(g.UnderArray)
	mapList = loads(g.MapList)
	mines = loads(g.Mines)
	gameState = g.GameState
	mapSizeX = g.MapSizeX
	mapSizeY = g.MapSizeY
	mapList = loads(g.MapList)
	
	if len(mapList) != 0 and gameState == 0:
		mapArray = mapList.pop()
		gameState = 0 
	
		g.MapArray = dumps(mapArray)
		g.UnderArray = dumps(underArray)
		g.MapList = dumps(mapList)
		g.Mines = dumps(mines)
		g.Flags = dumps(flags)
		g.GameState = gameState
		g.mapList = dumps(mapList)
	
		g.save()
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

def winCheck():

	global gameState

	win = 3
	
	for cnt1 in range(mapSizeY):
		for cnt2 in range(mapSizeX):
			if underArray[cnt1][cnt2] != 9 and mapArray[cnt1][cnt2] == None:
				win = 0

	gameState = win		
			
	pass
	
def updateMapList():

	global mapList

	mapList.append([])
	
	for cnt1 in range(mapSizeY):
		mapList[len(mapList) - 1].append([])
		for cnt2 in range(mapSizeX):
			mapList[len(mapList) - 1][cnt1].append(mapArray[cnt1][cnt2])
			
	pass


def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("game").add(message.reply_channel)


def ws_message(message):
	print("message check")
	Group("game").send({
	"text": "[user] %s" % message.content['text'],
    })

def ws_disconnect(message):
    Group("game").discard(message.reply_channel)






















	
	
	
	
	
	
	
