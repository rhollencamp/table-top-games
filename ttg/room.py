import json
import random
import string

from gevent.threading import Lock
from geventwebsocket.websocket import WebSocket

_rooms = {}
_room_lock = Lock()


def create_room(msg, wsock: WebSocket):
    with _room_lock:
        # generate a unique room code
        room_code = __generate_room_code()
        while room_code in _rooms:
            room_code = __generate_room_code()

        room = Room(room_code)
        _rooms[room_code] = room

        room.add_player(msg['name'], wsock)

    wsock.send(json.dumps({'msg': 'room-created', 'room': room_code}))


def join_room(msg, wsock: WebSocket):
    with _room_lock:
        room_code = msg['room']
        room = _rooms[room_code]
        if not room:
            raise ValueError('Room does not exist')

        name = msg['name']
        if name in room.players:
            raise ValueError('Player already in room')

        room.add_player(name, wsock)

    __broadcast_player_list(room.players.items())


def __broadcast_player_list(players):
    msg = json.dumps({
        'msg': 'player-list',
        'players': [x for x, _ in players]
    })
    for _, player_wsock in players:
        player_wsock.send(msg)


def __generate_room_code():
    return ''.join(random.choice(string.ascii_uppercase) for x in range(6))


class Room:

    def __init__(self, room_code):
        self.room_code = room_code
        self.players = {}

    def add_player(self, name, wsock):
        self.players[name] = wsock
