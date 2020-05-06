//import { isKeyDown } from "./modules/keyboard.js";

$(document).ready(function() {
    $("#startCreateGame").on('click', function(e) {
        e.preventDefault();

        var ws = createWebSocket();
        ws.onopen = function() {
            ws.send(JSON.stringify({"msg": "create-game", "name": $("#startCreateUserName").val()}));
            $("#startAccordion").hide();
            $("#playingArea").show();

            ws.onmessage = function(evt) {
                addPlayer($("#startCreateUserName").val());
                var msg = JSON.parse(evt.data);
                alert(msg.room);

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

            ws.onmessage = onMsg;
        }
    })

    function createWebSocket() {
        var protocol = window.location.protocol == "https:" ? "wss" : "ws";
        var url = protocol + "://" + window.location.host + "/websocket";
        return new WebSocket(url);
    }

    function addPlayer(playerName) {
        $("#playerList").append($("<li class=\"list-group-item\">" + playerName + "</li>"))
    }

    function resetPlayerList(players) {
        $("#playerList").empty();
        players.forEach(addPlayer);
    }

    function onMsg(evt) {
        var msg = JSON.parse(evt.data);
        if (msg["msg"] == "player-list") {
            resetPlayerList(msg["players"]);
        }
    }
});
