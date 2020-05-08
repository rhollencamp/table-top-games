"""
A room represents a game in progress
"""

import json
import random
import string

from gevent.threading import Lock
from geventwebsocket.websocket import WebSocket

__rooms = {}
__room_lock = Lock()
__wsock_lookup = {}


def create_room(name: str, wsock: WebSocket):
    with __room_lock:
        room_code = __generate_unique_room_code()

        room = Room(room_code)
        __rooms[room_code] = room

        room.add_player(name, wsock)

    __wsock_lookup[wsock] = room_code, name
    wsock.send(json.dumps({'msg': 'room-created', 'room': room_code}))


def join_room(name: str, room_code: str, wsock: WebSocket):
    with __room_lock:
        room = __rooms[room_code]

        if name in room.players:
            raise ValueError('Player already in room')

        room.add_player(name, wsock)

    __broadcast_player_list(room)
    __wsock_lookup[wsock] = room_code, name


def leave_room(wsock: WebSocket):
    room_code, player_name = __wsock_lookup[wsock]
    room = __rooms[room_code]
    room.remove_player(player_name)
    __broadcast_player_list(room)


def __broadcast_player_list(room):
    msg = json.dumps({
        'msg': 'player-list',
        'players': [*room.players]
    })
    room.broadcast(msg)


def __generate_unique_room_code():
    """
    Generate a room code that is unique / not already in use
    """
    room_code = __generate_random_code()
    while room_code in __rooms:
        room_code = __generate_random_code()
    return room_code


def __generate_random_code():
    """
    Generate 6 random characters that can be used as a room code
    """
    return ''.join(random.choice(string.ascii_uppercase) for x in range(6))


class Room:
    """
    Represents a game in progress, and all its state
    """

    def __init__(self, room_code):
        self.room_code = room_code
        self.players = {}

    def add_player(self, name, wsock):
        self.players[name] = wsock

    def remove_player(self, name):
        self.players.pop(name)

    def broadcast(self, msg):
        for _, wsock in self.players.items():
            wsock.send(msg)
