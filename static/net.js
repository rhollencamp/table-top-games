import * as ui from '/static/ui.js';
import * as room from '/static/room.js';

let wsock;

function createWebSocket() {
    let protocol = window.location.protocol == "https:" ? "wss" : "ws";
    let url = `${protocol}://${window.location.host}/websocket`;
    return new WebSocket(url);
}

function onMsg(evt) {
    let msg = JSON.parse(evt.data);
    if (msg.msg == 'player-list') {
        room.updatePlayerList(msg.players);
        ui.renderPlayerList(msg.players);
    } else if (msg.msg == 'new-entities') {
        room.addEntities(msg.entities);
        ui.renderNewEntities(msg.entities);
    } else if (msg.msg == "interaction") {
        ui.startUserInteraction(msg.entity, msg.name);
    } else if (msg.msg == 'update-entity') {
        ui.updateEntity(msg.entity.identifier, msg.entity.pos_x, msg.entity.pos_y);
        //room.updateEntity(msg.entity.identifier, msg.entity.pos_x, msg.entity.pos_y);
    } else if (msg.msg == 'stop-interacting') {
        ui.stopInteracting(msg.name, msg.entity);
    }
}

export function createRoom(name, callback) {
    wsock = createWebSocket();
    wsock.onopen = function() {
        wsock.send(JSON.stringify({
            "msg": "create-game",
            "name": name
        }));

        wsock.onmessage = function(evt) {
            let msg = JSON.parse(evt.data);

            callback(msg.room);

            wsock.onmessage = onMsg;

            // testing
            wsock.send(JSON.stringify({
                "msg": "load-entities",
                "entity-defs": [{
                    "type": "game-piece",
                    "img": "/static/test/chess-pawn.svg",
                    "width": 100,
                    "height": 100,
                    "pos_x": 0,
                    "pos_y": 0
                }]
            }));
        }
    }
}

export function joinRoom(name, roomCode, callback) {
    wsock = createWebSocket();
    wsock.onopen = function() {
        wsock.send(JSON.stringify({
            "msg": "join-game",
            "name": name,
            "room": roomCode
        }));

        // TODO wait for a response?
        callback(roomCode);

        wsock.onmessage = onMsg;
    }
}

export function tryInteract(entityId) {
    wsock.send(JSON.stringify({
        "msg": "start-interact",
        "entity": entityId
    }));
}

export function sendDragDropPosition(x, y) {
    wsock.send(JSON.stringify({
        'msg': 'drag-drop-position',
        'x': x,
        'y': y
    }));
}

export function stopInteracting() {
    wsock.send(JSON.stringify({
        'msg': 'stop-interacting'
    }));
}
