import * as net from '/static/net.js';
import * as room from '/static/room.js';

let colorLookup = {
    1: 'primary',
    2: 'secondary',
    3: 'success',
    4: 'danger',
    5: 'warning',
    6: 'info'
};

let dragDropData = {};

function enterRoom(roomCode) {
    $("#startAccordion").hide();
    $("#playingAreaCard").show();

    $("#roomCode").html(`Room Code: ${roomCode}`);
}

export function renderPlayerList(players) {
    $("#playerList").empty();
    players.forEach(function(player) {
        let color = colorLookup[player.color];
        $("#playerList").append($(`<li class="list-group-item text-white fong-weight-bold bg-${color}">${player.name}</li>`));
    });
}

export function renderNewEntities(entities) {
    entities.forEach(function(entity) {
        let style=`position: absolute; top: ${entity.y}; left: ${entity.x}`
        $("#playingArea").append($(`<img id="entity-${entity.identifier}" data-entity-id="${entity.identifier}" src="${entity.img}" width="${entity.width}" height="${entity.height}" style="${style}"></img>`))
        $(`#entity-${entity.identifier}`).on('mousedown', entityOnMouseDown);
    });
}

export function startUserInteraction(entityId, playerName) {
    let player = room.getPlayer(playerName);
    let color = colorLookup[player.color];
    $(`#entity-${entityId}`).addClass('border').addClass(`border-${color}`);

    // are we the ones moving the thing?
    if (playerName == room.getPlayerName()) {
        $(document).on('mousemove', entityDragMouseMove);
        dragDropData.interval = setInterval(sendDragDropPosToServer, 50);
        $(document).on('mouseup', function() {
            clearInterval(dragDropData.interval);
            $(document).off('mousemove');
            $(document).off('mouseup');
            dragDropData = {};
            net.stopInteracting();
        })
    }
}

export function stopInteracting(name, entityId) {
    let player = room.getPlayer(name);
    let color = colorLookup[player.color];
    $(`#entity-${entityId}`).removeClass('border').removeClass(`border-${color}`);
    //$(`#entity-${entity.identifier}`).on('mousedown', entityOnMouseDown);
}

function sendDragDropPosToServer() {
    net.sendDragDropPosition(dragDropData.left, dragDropData.top);
}

function entityOnMouseDown(evt) {
    evt.preventDefault();

    let entityId = $(evt.target).data("entity-id");

    dragDropData.x = evt.clientX;
    dragDropData.y = evt.clientY;
    dragDropData.dom = $(evt.target);
    dragDropData.top = parseInt(dragDropData.dom.css('top'));
    dragDropData.left = parseInt(dragDropData.dom.css('left'));

    net.tryInteract(entityId);
}

function entityDragMouseMove(evt) {
    evt.preventDefault();

    let dx = dragDropData.x - evt.clientX;
    let dy = dragDropData.y - evt.clientY;
    dragDropData.x = evt.clientX;
    dragDropData.y = evt.clientY;
    dragDropData.top -= dy;
    dragDropData.left -= dx;

    //console.info(`curTop ${curTop} curLeft ${curLeft} dx ${dx} dy ${dy}`);

    dragDropData.dom.css({
        'top': dragDropData.top,
        'left': dragDropData.left
    });
}

export function updateEntity(entityId, x, y) {
    $(`#entity-${entityId}`).css({
        'left': x,
        'top': y
    });
}

$(document).ready(function() {
    $("#startCreateGame").on('click', function(e) {
        e.preventDefault();

        let playerName = $("#startCreateUserName").val();
        room.setPlayerName(playerName);
        net.createRoom(playerName, enterRoom);
    });

    $("#startJoinGame").on('click', function(e) {
        e.preventDefault();

        let playerName = $("#startJoinUserName").val();
        let roomCode = $("#startJoinRoomCode").val();

        room.setPlayerName(playerName);
        room.setRoomCode(roomCode);
        net.joinRoom(playerName, roomCode, enterRoom);
    });
});
