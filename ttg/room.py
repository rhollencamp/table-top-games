import random
import re
import string

COLORS = set([1, 2, 3, 4, 5, 6])
VALID_NAME_RE = re.compile('^[a-zA-Z0-9_-]{3,15}$')
__rooms = {}


class Entity:
    """Object being used in a game"""

    def __init__(self, identifier, entity_def):
        self.__identifier = identifier
        self.__pos_x = entity_def['pos_x']
        self.__pos_y = entity_def['pos_y']
        self.__width = entity_def['width']
        self.__height = entity_def['height']
        self.__img = entity_def['img']
        self.__interactable = entity_def.get('interactable', True)

    @property
    def identifier(self):
        return self.__identifier

    @property
    def pos_x(self):
        return self.__pos_x

    @pos_x.setter
    def pos_x(self, new_pos_x):
        self.__pos_x = max(new_pos_x, 0)

    @property
    def pos_y(self):
        return self.__pos_y

    @pos_y.setter
    def pos_y(self, new_pos_y):
        self.__pos_y = max(new_pos_y, 0)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def img(self):
        return self.__img

    @property
    def interactable(self):
        return self.__interactable


class Player:
    """State for a player"""

    def __init__(self, name, color):
        self.__name = name
        self.__color = color

    @property
    def name(self):
        return self.__name

    @property
    def color(self):
        return self.__color


class Room:
    """State for a game room"""

    def __init__(self, room_code):
        self.room_code = room_code
        self.players = {}
        self.entities = {}
        self.interaction = None

    def add_player(self, name):
        # validate player name
        if not VALID_NAME_RE.match(name):
            raise ValueError('Invalid player name')

        if name in self.players:
            raise ValueError('Player with this name already in room')

        player = Player(name, self.__get_unused_color())
        self.players[name] = player

    def remove_player(self, name):
        self.players.pop(name)

    def start_interaction(self, name, entity_id):
        # one interaction at a time
        if self.interaction is not None:
            return None

        # make sure entity is interactable
        entity = self.entities[entity_id]
        if not entity.interactable:
            return None

        self.interaction = name, entity_id
        return self.interaction

    def move_entity(self, _, new_pos_x, new_pos_y):
        _, entity_id = self.interaction
        entity = self.entities[entity_id]
        entity.pos_x = new_pos_x
        entity.pos_y = new_pos_y
        return entity

    def stop_interacting(self, name):
        _, entity_id = self.interaction
        self.interaction = None
        return name, entity_id

    def process_entity_defs(self, entity_defs):
        created_entities = []
        for entity_def in entity_defs:
            entity = Entity(self.__next_identifier(), entity_def)
            self.entities[entity.identifier] = entity
            created_entities.append(entity)
        return created_entities

    def __next_identifier(self):
        return max(self.entities.keys()) + 1 if self.entities else 1

    def __get_unused_color(self):
        available_colors = set(COLORS)
        for player in self.players.values():
            available_colors.remove(player.color)
        return random.choice(tuple(available_colors))


def get_room(room_code) -> Room:
    return __rooms[room_code]


def create_room(name: str):
    room_code = __generate_unique_room_code()

    room = Room(room_code)
    __rooms[room_code] = room

    room.add_player(name)

    return room_code


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
