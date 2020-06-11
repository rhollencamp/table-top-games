from collections import defaultdict
from logging import getLogger
import json

from sanic.websocket import ConnectionClosed

from ttg.room import create_room
from ttg.room import get_room


__wsock_lookup = {}
__rooms = defaultdict(dict)
__logger = getLogger(__name__)


async def new_connection_established(wsock):
    """called when a new websocket is opened"""

    # first message: are they creating or joining a room
    try:
        msg = await __get_json_msg(wsock)
        name = msg['name']
        if msg['msg'] == 'create-game':
            room_code = create_room(name)
            __add_player(name, room_code, wsock)
            await wsock.send(json.dumps({
                'msg': 'room-created',
                'room': room_code
            }))
            await __broadcast_player_list(room_code)
        elif msg['msg'] == 'join-game':
            room_code = msg['room']
            await __handle_join_game(name, room_code, wsock)
        else:
            wsock.close()
            return
    except ValueError as err:
        # TODO need to make sure we clean up
        await wsock.send(json.dumps({
            'msg': 'error',
            'details': str(err)
        }))
        return


    while True:
        msg = await __get_json_msg(wsock)
        if msg is None:
            await __handle_disconnect(wsock)
            break
        await __handle_msg(name, room_code, msg)


async def __get_json_msg(wsock):
    try:
        msg = await wsock.recv()
        __logger.debug('Received message %s', msg)
        return json.loads(msg) if msg else msg
    except ConnectionClosed as err:
        room_code, name = __wsock_lookup[wsock]
        __logger.debug('Websocket closed for %s %s',
                       room_code,
                       name,
                       exc_info=err)
        return None


async def __handle_join_game(name, room_code, wsock):
    # add player to room itself
    room = get_room(room_code)
    room.add_player(name)

    # update netcode lookup maps
    __add_player(name, room_code, wsock)
    await __broadcast_player_list(room_code)

    # send entity list
    room = get_room(room_code)
    msg = json.dumps({
        'msg': 'new-entities',
        'entities': [__serialize_entity(x) for x in room.entities.values()]
    })
    await wsock.send(msg)


async def __handle_msg(name, room_code, msg):
    if msg['msg'] == 'load-entities':
        await __handle_msg_load_entities(room_code, msg['entity-defs'])
    elif msg['msg'] == 'start-interact':
        await __handle_msg_start_interact(name, room_code, msg['entity'])
    elif msg['msg'] == 'drag-drop-position':
        await __handle_drag_drop_position(name, room_code, msg['x'], msg['y'])
    elif msg['msg'] == 'stop-interacting':
        await __handle_stop_interacting(name, room_code)
    elif msg['msg'] == 'ping':
        pass
    else:
        raise ValueError('Unexpected message type ' + msg['msg'])


async def __handle_drag_drop_position(name, room_code, pos_x, pos_y):
    room = get_room(room_code)
    entity = room.move_entity(name, pos_x, pos_y)
    msg = json.dumps({
        'msg': 'update-entity',
        'entity': __serialize_entity(entity)
    })
    await __broadcast(room_code, msg, except_name=name)


async def __handle_stop_interacting(name, room_code):
    room = get_room(room_code)
    _, entity_id = room.stop_interacting(name)
    msg = json.dumps({
        'msg': 'stop-interacting',
        'name': name,
        'entity': entity_id
    })
    await __broadcast(room_code, msg)


async def __handle_msg_start_interact(name, room_code, entity_id):
    room = get_room(room_code)
    result = room.start_interaction(name, entity_id)
    if result:
        msg = json.dumps({
            'msg': 'interaction',
            'name': name,
            'entity': entity_id
        })
        await __broadcast(room_code, msg)


async def __handle_msg_load_entities(room_code, entity_defs):
    room = get_room(room_code)
    new_entities = room.process_entity_defs(entity_defs)
    msg = json.dumps({
        'msg': 'new-entities',
        'entities': [__serialize_entity(x) for x in new_entities]
    })
    await __broadcast(room_code, msg)


async def __handle_disconnect(wsock):
    room_code, name = __wsock_lookup[wsock]

    # remove player from room
    room = get_room(room_code)
    room.remove_player(name)

    # remove player from our lookup maps
    __remove_player(name, room_code, wsock)

    # send new player list to everyone else in room
    await __broadcast_player_list(room_code)


async def __broadcast_player_list(room_code):
    room = get_room(room_code)
    msg = json.dumps({
        'msg': 'player-list',
        'players': [__serialize_player(x) for x in room.players.values()]
    })
    await __broadcast(room_code, msg)


def __serialize_player(player):
    return {
        'name':  player.name,
        'color': player.color
    }


def __serialize_entity(entity):
    return {
        'identifier': entity.identifier,
        'pos_x':      entity.pos_x,
        'pos_y':      entity.pos_y,
        'width':      entity.width,
        'height':     entity.height,
        'img':        entity.img
    }


async def __broadcast(room_code, msg, except_name=None):
    """broadcast a message to all players in a room"""
    for name, wsock in __rooms[room_code].items():
        if except_name and name == except_name:
            continue
        await wsock.send(msg)


def __add_player(name, room_code, wsock):
    __wsock_lookup[wsock] = room_code, name
    __rooms[room_code][name] = wsock


def __remove_player(name, room_code, wsock):
    __wsock_lookup.pop(wsock)
    __rooms[room_code].pop(name)
    if not __rooms[room_code]:
        __rooms.pop(room_code)
