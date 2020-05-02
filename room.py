import random
import string

_rooms = {}


def create_room(msg, wsock):
    name = msg['name']


def join_room(msg, wsock):
    pass


def _generate_room_code():
    return ''.join(random.choice(string.ascii_uppercase) for x in range(6))
