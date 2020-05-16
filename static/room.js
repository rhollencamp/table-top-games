let playerName;
let roomCode;
let players = {};
let entities = {};

export function updatePlayerList(updatedPlayerList) {
    players = {};
    updatedPlayerList.forEach(function(player) {
        players[player.name] = player;
    });
}

export function addEntities(newEntities) {
    newEntities.forEach(function(entity) {
        entities[entity.id] = entity;
    });
}

export function getPlayer(name) {
    return players[name];
}


export function getPlayerName() {
    return playerName;
}

export function setPlayerName(newName) {
    playerName = newName;
}

export function getRoomCode() {
    return roomCode;
}

export function setRoomCode(newRoomCode) {
    roomCode = newRoomCode;
}
