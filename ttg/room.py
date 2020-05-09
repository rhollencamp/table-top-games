"""
A room represents a game in progress
"""

import random
import string

__COLORS = set([1, 2, 3, 4, 5, 6])
__rooms = {}


class Player:
    """State for a player"""

    def __init__(self, room_code, name, color):
        self.room_code = room_code
        self.name = name
        self.color = color


class Room:
    """State for a game room"""

    def __init__(self, room_code):
        self.room_code = room_code
        self.players = {}

    def add_player(self, player: Player):
        self.players[player.name] = player

    def remove_player(self, player: Player):
        self.players.pop(player.name)


def get_player(room_code, name):
    return __rooms[room_code].players[name]


def create_room(name: str):
    room_code = __generate_unique_room_code()

    room = Room(room_code)
    __rooms[room_code] = room

    player = Player(room_code, name, __get_unused_color(room))
    room.add_player(player)

    return room_code


def join_room(name: str, room_code: str):
    room = __rooms[room_code]

    if name in room.players:
        raise ValueError('Player already in room')

    player = Player(room_code, name, __get_unused_color(room))
    room.add_player(player)


def leave_room(name: str, room_code: str):
    room = __rooms[room_code]
    room.remove_player(room.players[name])


def __get_unused_color(room):
    available_colors = set(__COLORS)
    for player in room.players.values():
        available_colors.remove(player.color)
    return random.choice(tuple(available_colors))


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
