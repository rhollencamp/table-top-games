from collections import defaultdict
from logging import getLogger
import json

from sanic.websocket import ConnectionClosed

from ttg.room import create_room
from ttg.room import get_room


_wsock_lookup = {}
_rooms = defaultdict(dict)
_logger = getLogger(__name__)


async def new_connection_established(wsock):
    """called when a new websocket is opened"""

    # first message: are they creating or joining a room
    msg = await _get_json_msg(wsock)
    name = msg['name']
    if msg['msg'] == 'create-game':
        room_code = create_room(name)
        _add_player(name, room_code, wsock)
        await wsock.send(json.dumps({
            'msg': 'room-created',
            'room': room_code
        }))
        await _broadcast_player_list(room_code)
    elif msg['msg'] == 'join-game':
        room_code = msg['room']
        await _handle_join_game(name, room_code, wsock)
    else:
        wsock.close()
        return

    while True:
        msg = await _get_json_msg(wsock)
        if msg is None:
            await _handle_disconnect(wsock)
            break
        await _handle_msg(name, room_code, msg)


async def _get_json_msg(wsock):
    try:
        msg = await wsock.recv()
        _logger.debug('Received message %s', msg)
        return json.loads(msg) if msg else msg
    except ConnectionClosed as exc:
        room_code, name = _wsock_lookup[wsock]
        _logger.debug('Websocket closed for %s %s',
                      room_code,
                      name,
                      exc_info=exc)
        return None


async def _handle_join_game(name, room_code, wsock):
    # add player to room itself
    room = get_room(room_code)
    room.add_player(name)

    # update netcode lookup maps
    _add_player(name, room_code, wsock)
    await _broadcast_player_list(room_code)

    # send entity list
    room = get_room(room_code)
    msg = json.dumps({
        'msg': 'new-entities',
        'entities': [_serialize_entity(x) for x in room.entities.values()]
    })
    await wsock.send(msg)


async def _handle_msg(name, room_code, msg):
    if msg['msg'] == 'load-entities':
        await _handle_msg_load_entities(room_code, msg['entity-defs'])
    elif msg['msg'] == 'start-interact':
        await _handle_msg_start_interact(name, room_code, msg['entity'])
    elif msg['msg'] == 'drag-drop-position':
        await _handle_drag_drop_position(name, room_code, msg['x'], msg['y'])
    elif msg['msg'] == 'stop-interacting':
        await _handle_stop_interacting(name, room_code)
    elif msg['msg'] == 'ping':
        pass
    else:
        raise ValueError('Unexpected message type ' + msg['msg'])


async def _handle_drag_drop_position(name, room_code, pos_x, pos_y):
    room = get_room(room_code)
    entity = room.move_entity(name, pos_x, pos_y)
    msg = json.dumps({
        'msg': 'update-entity',
        'entity': _serialize_entity(entity)
    })
    await _broadcast(room_code, msg, except_name=name)


async def _handle_stop_interacting(name, room_code):
    room = get_room(room_code)
    _, entity_id = room.stop_interacting(name)
    msg = json.dumps({
        'msg': 'stop-interacting',
        'name': name,
        'entity': entity_id
    })
    await _broadcast(room_code, msg)


async def _handle_msg_start_interact(name, room_code, entity_id):
    room = get_room(room_code)
    result = room.start_interaction(name, entity_id)
    if result:
        msg = json.dumps({
            'msg': 'interaction',
            'name': name,
            'entity': entity_id
        })
        await _broadcast(room_code, msg)


async def _handle_msg_load_entities(room_code, entity_defs):
    room = get_room(room_code)
    new_entities = room.process_entity_defs(entity_defs)
    msg = json.dumps({
        'msg': 'new-entities',
        'entities': [_serialize_entity(x) for x in new_entities]
    })
    await _broadcast(room_code, msg)


async def _handle_disconnect(wsock):
    room_code, name = _wsock_lookup[wsock]

    # remove player from room
    room = get_room(room_code)
    room.remove_player(name)

    # remove player from our lookup maps
    _remove_player(name, room_code, wsock)

    # send new player list to everyone else in room
    await _broadcast_player_list(room_code)


async def _broadcast_player_list(room_code):
    room = get_room(room_code)
    msg = json.dumps({
        'msg': 'player-list',
        'players': [_serialize_player(x) for x in room.players.values()]
    })
    await _broadcast(room_code, msg)


def _serialize_player(player):
    return {
        'name':  player.name,
        'color': player.color
    }


def _serialize_entity(entity):
    return {
        'identifier': entity.identifier,
        'pos_x':      entity.pos_x,
        'pos_y':      entity.pos_y,
        'width':      entity.width,
        'height':     entity.height,
        'img':        entity.img
    }


async def _broadcast(room_code, msg, except_name=None):
    """broadcast a message to all players in a room"""
    for name, wsock in _rooms[room_code].items():
        if except_name and name == except_name:
            continue
        await wsock.send(msg)


def _add_player(name, room_code, wsock):
    _wsock_lookup[wsock] = room_code, name
    _rooms[room_code][name] = wsock


def _remove_player(name, room_code, wsock):
    _wsock_lookup.pop(wsock)
    _rooms[room_code].pop(name)
    if not _rooms[room_code]:
        _rooms.pop(room_code)
