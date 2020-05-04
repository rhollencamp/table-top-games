import json
import random
import string

from gevent.threading import Lock
from geventwebsocket.websocket import WebSocket

_rooms = {}
_room_lock = Lock()


def create_room(msg, wsock: WebSocket):
    _room_lock.acquire()
    try:
        # generate a unique room code
        room_code = _generate_room_code()
        while room_code in _rooms:
            room_code = _generate_room_code()

        room = Room(room_code)
        _rooms[room_code] = room

        room.add_player(msg['name'], wsock)
    finally:
        _room_lock.release()

    wsock.send(json.dumps({"room": room_code}))


def join_room(msg, wsock: WebSocket):
    _room_lock.acquire()
    try:
        room_code = msg['room']
        room = _rooms[room_code]
        if not room:
            raise ValueError('Room does not exist')

        name = msg['name']
        if name in room.players:
            raise ValueError('Player already in room')

        room.add_player(name, wsock)
    finally:
        _room_lock.release()


def _generate_room_code():
    return ''.join(random.choice(string.ascii_uppercase) for x in range(6))


class Room:

    def __init__(self, room_code):
        self.room_code = room_code
        self.players = {}

    def add_player(self, name, wsock):
        self.players[name] = wsock
