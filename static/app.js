$(document).ready(function() {

    var colorLookup = {
        1: 'primary',
        2: 'secondary',
        3: 'success',
        4: 'danger',
        5: 'warning',
        6: 'info'
    };

    $("#startCreateGame").on('click', function(e) {
        e.preventDefault();

        var ws = createWebSocket();
        ws.onopen = function() {
            ws.send(JSON.stringify({"msg": "create-game", "name": $("#startCreateUserName").val()}));
            $("#startAccordion").hide();
            $("#playingArea").show();

            ws.onmessage = function(evt) {
                var msg = JSON.parse(evt.data);
                $("#roomCode").html(`Room Code: ${msg.room}`);

                ws.onmessage = onMsg;
            }
        }
    });

    $("#startJoinGame").on('click', function(e) {
        e.preventDefault();

        var ws = createWebSocket();
        ws.onopen = function() {
            ws.send(JSON.stringify({
                "msg": "join-game",
                "name": $("#startJoinUserName").val(),
                "room": $("#startJoinRoomCode").val()
            }));
            $("#startAccordion").hide();
            $("#playingArea").show();
            $("#roomCode").html("Room Code: " + $("#startJoinRoomCode").val());

            ws.onmessage = onMsg;
        }
    })

    function createWebSocket() {
        var protocol = window.location.protocol == "https:" ? "wss" : "ws";
        var url = `${protocol}://${window.location.host}/websocket`;
        return new WebSocket(url);
    }

    function addPlayer(playerName, color) {
        $("#playerList").append($(`<li class="list-group-item text-white fong-weight-bold bg-${color}">${playerName}</li>`))
    }

    function resetPlayerList(players) {
        $("#playerList").empty();
        for (let [name, props] of Object.entries(players)) {
            addPlayer(name, colorLookup[props["color"]]);
        }
    }

    function onMsg(evt) {
        var msg = JSON.parse(evt.data);
        if (msg["msg"] == "player-list") {
            resetPlayerList(msg["players"]);
        }
    }
});
