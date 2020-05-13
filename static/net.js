let wsock;

function createWebSocket() {
    let protocol = window.location.protocol == "https:" ? "wss" : "ws";
    let url = `${protocol}://${window.location.host}/websocket`;
    return new WebSocket(url);
}

function onMsg(evt) {
    let msg = JSON.parse(evt.data);
    if (msg["msg"] == "player-list") {
        $(document).trigger("ttg.player-list", [msg["players"]]);
    } else if (msg["msg"] == "new-entities") {
        $(document).trigger("ttg.new-entities", [msg["entities"]]);
    } else if (msg["msg"] == "interaction") {
        let entityId = msg["entity"];
        let interactingName = msg["name"];
        let interactingDom = $(`#entity-${entityId}`).addClass('border').addClass('border-primary');
    }
}

$(document).on('ttg.create-game', function(e, name) {
    wsock = createWebSocket();
    wsock.onopen = function() {
        wsock.send(JSON.stringify({
            "msg": "create-game",
            "name": name
        }));

        wsock.onmessage = function(evt) {
            let msg = JSON.parse(evt.data);

            $(document).trigger('ttg.enter-room', [msg.room]);

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
});

$(document).on('ttg.join-game', function(e, name, roomCode) {
    wsock = createWebSocket();
    wsock.onopen = function() {
        wsock.send(JSON.stringify({
            "msg": "join-game",
            "name": name,
            "room": roomCode
        }));

        // TODO wait for a response?
        $(document).trigger('ttg.enter-room', [roomCode]);

        wsock.onmessage = onMsg;
    }
});
