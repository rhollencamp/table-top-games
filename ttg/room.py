"""
A room represents a game in progress
"""

import random
import string


__rooms = {}


def create_room(name: str):
    room_code = __generate_unique_room_code()

    room = Room(room_code)
    __rooms[room_code] = room
    room.add_player(name)

    return room_code


def join_room(name: str, room_code: str):
    room = __rooms[room_code]

    if name in room.players:
        raise ValueError('Player already in room')

    room.add_player(name)


def leave_room(name: str, room_code: str):
    room = __rooms[room_code]
    room.remove_player(name)


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
        self.players = []

    def add_player(self, name):
        self.players.append(name)

    def remove_player(self, name):
        self.players.remove(name)
