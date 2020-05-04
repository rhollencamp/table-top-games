//import { isKeyDown } from "./modules/keyboard.js";

$(document).ready(function() {
    /*    var ws = createWebSocket();
        ws.onmessage = function (evt) {
            var pos = JSON.parse(evt.data);
            $("#player").css("top", pos.y);
            $("#player").css("left", pos.x);
        };

        window.setInterval(function() {
            var inputUpdate = "";
            if (isKeyDown("w")) inputUpdate += "U";
            if (isKeyDown("s")) inputUpdate += "D";
            if (isKeyDown("a")) inputUpdate += "L";
            if (isKeyDown("d")) inputUpdate += "R";
            ws.send(inputUpdate);
        }, 15);

        function createWebSocket() {
            var protocol = window.location.protocol == "https:" ? "wss" : "ws";
            var url = protocol + "://" + window.location.host + "/test?foo=bar";
            return new WebSocket(url);
        }*/

    $("#startCreateGame").on('click', function(e) {
        e.preventDefault();


        var ws = createWebSocket();
        ws.onopen = function() {
            ws.send(JSON.stringify({"action": "create", "name": $("#startCreateUserName").val()}));
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
