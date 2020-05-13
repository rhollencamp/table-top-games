let colorLookup = {
    1: 'primary',
    2: 'secondary',
    3: 'success',
    4: 'danger',
    5: 'warning',
    6: 'info'
};

$(document).on('ttg.enter-room', function(e, roomCode) {
    $("#startAccordion").hide();
    $("#playingAreaCard").show();

    $("#roomCode").html(`Room Code: ${roomCode}`);
});

$(document).on('ttg.player-list', function(e, players) {
    $("#playerList").empty();
    players.forEach(function(player) {
        let color = colorLookup[player.color];
        $("#playerList").append($(`<li class="list-group-item text-white fong-weight-bold bg-${color}">${player.name}</li>`));
    });
});

$(document).on("ttg.new-entities", function(e, entities) {
    entities.forEach(function(entity) {
        $("#playingArea").append($(`<img id="entity-${entity.identifier}" data-entity-id="${entity.identifier}" src="${entity.img}" width="${entity.width}" height="${entity.height}"></img>`))
        $(`#entity-${entity.identifier}`).on('mousedown', entityOnMouseDown);
    });
});

function entityOnMouseDown(evt) {
    let entityId = $(evt.target).data("entity-id");
    ws.send(JSON.stringify({
        "msg": "start-interact",
        "entity": entityId
    }));
}

$(document).ready(function() {
    $("#startCreateGame").on('click', function(e) {
        e.preventDefault();
        $(document).trigger('ttg.create-game', [$("#startCreateUserName").val()])
    });

    $("#startJoinGame").on('click', function(e) {
        e.preventDefault();
        $(document).trigger('ttg.join-game', [$("#startJoinUserName").val(), $("#startJoinRoomCode").val()]);
    });
});
