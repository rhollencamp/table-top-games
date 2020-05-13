let players = {};
let entities = {};

$(document).on("ttg.player-list", function(e, receivedPlayers) {
    players = {};
    receivedPlayers.forEach(function(player) {
        players[player.name] = player;
    });
});
