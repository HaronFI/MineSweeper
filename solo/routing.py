from channels.routing import route
channel_routing = [
    route("websocket.connect", "solo.views.leftClick"),
    route("websocket.receive", "solo.views.updateDataBase"),
]