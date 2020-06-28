import random
import string

_COLORS = {1, 2, 3, 4, 5, 6}
_ROOMS = {}


class Entity:
    """Object being used in a game"""

    def __init__(self, identifier, entity_def, template):
        self._identifier = identifier
        self._pos_x = self._get_attr('pos_x', entity_def, template)
        self._pos_y = self._get_attr('pos_y', entity_def, template)
        self._width = self._get_attr('width', entity_def, template)
        self._height = self._get_attr('height', entity_def, template)
        self._img = self._get_attr('img', entity_def, template)
        self._interactable = self._get_attr('interactable', entity_def,
                                            template, default=True)

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

    @staticmethod
    def _get_attr(key, entity_def, template, **kwargs):
        try:
            return entity_def[key]
        except KeyError:
            if template and key in template:
                return template[key]
            if 'default' in kwargs:
                return kwargs['default']
            raise ValueError()


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
        self._templates = {}
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
        if 'templates' in entity_defs:
            for name, template in entity_defs["templates"].items():
                if name in self._templates:
                    raise ValueError()
                self._templates[name] = template

        created_entities = []
        for entity_def in entity_defs["entities"]:
            try:
                template = self._templates[entity_def["template"]]
            except KeyError:
                template = None
            entity = Entity(self._next_identifier(), entity_def, template)
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
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
