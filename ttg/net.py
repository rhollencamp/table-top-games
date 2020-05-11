"""
netcode

deals with sending and receiving messages on websockets
"""

from collections import defaultdict
from logging import getLogger
import json

from geventwebsocket import WebSocketError

from ttg.room import create_room
from ttg.room import get_player
from ttg.room import get_room
from ttg.room import join_room
from ttg.room import leave_room
from ttg.room import process_entities_json


__wsock_lookup = {}
__rooms = defaultdict(dict)
__logger = getLogger(__name__)


def new_connection_established(wsock):
    """called when a new websocket is opened"""

    # first message: are they creating or joining a room
    msg = __get_json_msg(wsock)
    name = msg['name']
    if msg['msg'] == 'create-game':
        room_code = create_room(name)
        __add_player(name, room_code, wsock)
        wsock.send(json.dumps({
            'msg': 'room-created',
            'room': room_code
        }))
        __broadcast_player_list(room_code)
    elif msg['msg'] == 'join-game':
        room_code = msg['room']
        join_room(name, room_code)
        __add_player(name, room_code, wsock)
        __broadcast_player_list(room_code)
    else:
        wsock.close()
        return

    while True:
        try:
            msg = __get_json_msg(wsock)
            if msg is None:
                __handle_disconnect(wsock)
                break
            __handle_msg(name, room_code, msg)
        except WebSocketError as err:
            __logger.exception(err)


def __get_json_msg(wsock):
    msg = wsock.receive()
    __logger.debug('Received message %s', msg)
    return json.loads(msg) if msg else msg


def __handle_msg(name, room_code, msg):
    if msg['msg'] == 'load-entities':
        __handle_msg_load_entities(name, room_code, msg['entity-defs'])
    elif msg['msg'] == 'start-interact':
        __handle_msg_start_interact(name, room_code, msg['entity'])
    else:
        raise ValueError('Unexpected message type ' + msg['msg'])


def __handle_msg_start_interact(name, room_code, entity_id):
    room = get_room(room_code)
    result = room.start_interaction(name, entity_id)
    if result:
        msg = json.dumps({
            'msg': 'interaction',
            'name': name,
            'entity': entity_id
        })
        __broadcast(room_code, msg)


def __handle_msg_load_entities(name, room_code, entity_defs):
    new_entities = process_entities_json(room_code, entity_defs)
    msg = json.dumps({
        'msg': 'new-entities',
        'entities': [x.__dict__ for x in new_entities]
    })
    __broadcast(room_code, msg)


def __handle_disconnect(wsock):
    room_code, name = __wsock_lookup[wsock]
    leave_room(name, room_code)
    __remove_player(name, room_code, wsock)
    __broadcast_player_list(room_code)


def __broadcast_player_list(room_code):
    players = {}
    for player_name in __rooms[room_code]:
        player = get_player(room_code, player_name)
        players[player_name] = {'color': player.color}

    msg = json.dumps({
        'msg': 'player-list',
        'players': players
    })
    __broadcast(room_code, msg)


def __broadcast(room_code, msg):
    """broadcast a message to all players in a room"""
    for _, wsock in __rooms[room_code].items():
        wsock.send(msg)


def __add_player(name, room_code, wsock):
    __wsock_lookup[wsock] = room_code, name
    __rooms[room_code][name] = wsock


def __remove_player(name, room_code, wsock):
    __wsock_lookup.pop(wsock)
    __rooms[room_code].pop(name)
    if not __rooms[room_code]:
        __rooms.pop(room_code)
