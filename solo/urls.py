from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
	url(r'^startGame$', views.startGame, name = 'startGame'),
	url(r'^loadGame/$', views.loadGame, name = 'loadGame'),
	url(r'^getSize$', views.getSize, name = 'getSize'),
	url(r'^getMap$', views.getMap, name = 'getMap'),
	url(r'^leftClick$', views.leftClick, name = 'leftClick'),
	url(r'^rightClick$', views.rightClick, name = 'rightClick'),
	url(r'^undo$', views.undo, name = 'undo'),
	url(r'^getGameState$', views.getGameState, name = 'getGameState'),
]
