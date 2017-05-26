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