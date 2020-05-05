//import { isKeyDown } from "./modules/keyboard.js";

$(document).ready(function() {
    $("#startCreateGame").on('click', function(e) {
        e.preventDefault();

        var ws = createWebSocket();
        ws.onopen = function() {
            ws.send(JSON.stringify({"msg": "create-game", "name": $("#startCreateUserName").val()}));
            $("#startAccordion").hide();

            ws.onmessage = function(evt) {
                var msg = JSON.parse(evt.data);
                alert(msg.room);
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

            ws.onmessage = function(evt) {
                var msg = JSON.parse(evt.data);
                alert(msg.room);
            }
        }
    })

    function createWebSocket() {
        var protocol = window.location.protocol == "https:" ? "wss" : "ws";
        var url = protocol + "://" + window.location.host + "/websocket";
        return new WebSocket(url);
    }
});
