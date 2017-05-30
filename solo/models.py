from django.db import models

class Game(models.Model):

	_DATABASE = "Default"

	MapSizeX = models.IntegerField()
	MapSizeY = models.IntegerField()
	MapArray = models.TextField()
	UnderArray = models.TextField()
	GameState = models.IntegerField()
	Mines = models.TextField()
	Flags = models.TextField()
	MapList = models.TextField()
	
class LeaderBoard(models.Model):
	
	_DATABASE = "Default"
	
	Name = models.TextField()
	Score = models.IntegerField()