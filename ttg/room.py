import random
import string

_COLORS = set([1, 2, 3, 4, 5, 6])
_ROOMS = {}


class Entity:
    """Object being used in a game"""

    def __init__(self, identifier, entity_def):
        self._identifier = identifier
        self._pos_x = entity_def['pos_x']
        self._pos_y = entity_def['pos_y']
        self._width = entity_def['width']
        self._height = entity_def['height']
        self._img = entity_def['img']
        self._interactable = entity_def.get('interactable', True)

    @property
    def identifier(self):
        return self._identifier

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, new_pos_x):
        self._pos_x = max(new_pos_x, 0)

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, new_pos_y):
        self._pos_y = max(new_pos_y, 0)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def img(self):
        return self._img

    @property
    def interactable(self):
        return self._interactable


class Player:
    """State for a player"""

    def __init__(self, name, color):
        self._name = name
        self._color = color

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color


class Room:
    """State for a game room"""

    def __init__(self, room_code):
        self._room_code = room_code
        self._players = {}
        self._entities = {}
        self._interaction = None

    @property
    def room_code(self):
        return self._room_code

    @property
    def players(self):
        return self._players

    @property
    def entities(self):
        return self._entities

    @property
    def interaction(self):
        return self._interaction

    def add_player(self, name):
        if name in self._players:
            raise ValueError('Player already in room')

        player = Player(name, self._get_unused_color())
        self._players[name] = player

    def remove_player(self, name):
        self._players.pop(name)

    def start_interaction(self, name, entity_id):
        # one interaction at a time
        if self._interaction is not None:
            return None

        # make sure entity is interactable
        entity = self._entities[entity_id]
        if not entity.interactable:
            return None

        self._interaction = name, entity_id
        return self._interaction

    def move_entity(self, _, new_pos_x, new_pos_y):
        _, entity_id = self._interaction
        entity = self._entities[entity_id]
        entity.pos_x = new_pos_x
        entity.pos_y = new_pos_y
        return entity

    def stop_interacting(self, name):
        _, entity_id = self._interaction
        self._interaction = None
        return name, entity_id

    def process_entity_defs(self, entity_defs):
        created_entities = []
        for entity_def in entity_defs:
            entity = Entity(self._next_identifier(), entity_def)
            self._entities[entity.identifier] = entity
            created_entities.append(entity)
        return created_entities

    def _next_identifier(self):
        return max(self._entities.keys()) + 1 if self._entities else 1

    def _get_unused_color(self):
        available_colors = set(_COLORS)
        for player in self._players.values():
            available_colors.remove(player.color)
        return random.choice(tuple(available_colors))


def get_room(room_code) -> Room:
    return _ROOMS[room_code]


def create_room(name: str):
    room_code = _generate_unique_room_code()

    room = Room(room_code)
    _ROOMS[room_code] = room

    room.add_player(name)

    return room_code


def _generate_unique_room_code():
    """
    Generate a room code that is unique / not already in use
    """
    room_code = _generate_random_code()
    while room_code in _ROOMS:
        room_code = _generate_random_code()
    return room_code


def _generate_random_code():
    """
    Generate 6 random characters that can be used as a room code
    """
    return ''.join(random.choice(string.ascii_uppercase) for x in range(6))
