"""
A room represents a game in progress
"""

import random
import string

__COLORS = set([1, 2, 3, 4, 5, 6])
__rooms = {}


class Entity:
    """Object being used in a game"""

    def __init__(self, identifier, pos_x, pos_y, width, height, url):
        self.identifier = identifier
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.url = url


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
        self.entities = {}
        self.interaction = None

    def add_player(self, player: Player):
        self.players[player.name] = player

    def remove_player(self, player: Player):
        self.players.pop(player.name)

    def add_entity(self, pos_x, pos_y, width, height, url):
        identifier = max(self.entities.keys()) + 1 if self.entities else 1
        entity = Entity(identifier, pos_x, pos_y, width, height, url)
        self.entities[identifier] = entity
        return entity

    def start_interaction(self, name, entity_id):
        if self.interaction is not None:
            return None
        self.interaction = name, entity_id
        return self.interaction


def process_entities_json(room_code, entity_defs):
    room = __rooms[room_code]

    created_entities = []
    for entity_def in entity_defs:
        entity = room.add_entity(entity_def['x'],
                                 entity_def['y'],
                                 entity_def['width'],
                                 entity_def['height'],
                                 entity_def['img'])
        created_entities.append(entity)
    return created_entities


def get_room(room_code) -> Room:
    return __rooms[room_code]


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
