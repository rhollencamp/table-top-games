$(document).ready(function() {

    let colorLookup = {
        1: 'primary',
        2: 'secondary',
        3: 'success',
        4: 'danger',
        5: 'warning',
        6: 'info'
    };

    let ws;

    $("#startCreateGame").on('click', function(e) {
        e.preventDefault();

        ws = createWebSocket();
        ws.onopen = function() {
            ws.send(JSON.stringify({"msg": "create-game", "name": $("#startCreateUserName").val()}));
            $("#startAccordion").hide();
            $("#playingAreaCard").show();

            ws.onmessage = function(evt) {
                let msg = JSON.parse(evt.data);
                $("#roomCode").html(`Room Code: ${msg.room}`);

                ws.onmessage = onMsg;

                // testing
                ws.send(JSON.stringify({
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

    $("#startJoinGame").on('click', function(e) {
        e.preventDefault();

        ws = createWebSocket();
        ws.onopen = function() {
            ws.send(JSON.stringify({
                "msg": "join-game",
                "name": $("#startJoinUserName").val(),
                "room": $("#startJoinRoomCode").val()
            }));
            $("#startAccordion").hide();
            $("#playingAreaCard").show();
            $("#roomCode").html("Room Code: " + $("#startJoinRoomCode").val());

            ws.onmessage = onMsg;
        }
    })

    function createWebSocket() {
        let protocol = window.location.protocol == "https:" ? "wss" : "ws";
        let url = `${protocol}://${window.location.host}/websocket`;
        return new WebSocket(url);
    }

    function addPlayer(playerName, color) {
        $("#playerList").append($(`<li class="list-group-item text-white fong-weight-bold bg-${color}">${playerName}</li>`))
    }

    function resetPlayerList(players) {
        $("#playerList").empty();
        players.forEach(function(player) {
            addPlayer(player.name, colorLookup[player.color]);
        });
    }

    function receiveNewEntities(entities) {
        entities.forEach(function(entity) {
            $("#playingArea").append($(`<img id="entity-${entity.identifier}" data-entity-id="${entity.identifier}" src="${entity.img}" width="${entity.width}" height="${entity.height}"></img>`))
            $(`#entity-${entity.identifier}`).on('mousedown', entityOnMouseDown);
        });
    }

    function onMsg(evt) {
        let msg = JSON.parse(evt.data);
        if (msg["msg"] == "player-list") {
            resetPlayerList(msg["players"]);
        } else if (msg["msg"] == "new-entities") {
            receiveNewEntities(msg["entities"]);
        } else if (msg["msg"] == "interaction") {
            let entityId = msg["entity"];
            let interactingName = msg["name"];
            let interactingDom = $(`#entity-${entityId}`).addClass('border').addClass('border-primary');
        }
    }

    function entityOnMouseDown(evt) {
        let entityId = $(evt.target).data("entity-id");
        ws.send(JSON.stringify({
            "msg": "start-interact",
            "entity": entityId
        }));
    }
});
