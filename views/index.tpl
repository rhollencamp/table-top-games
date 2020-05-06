<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Table-Top.games</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <link rel="stylesheet" href="/static/ttg.css">
    <link rel="icon" href="/static/favicon.svg" sizes="any" type="image/svg+xml">
</head>
<body>

<div class="container-fluid h-100 d-flex flex-column" style="padding: 0;">
    <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-5 flex-shrink-0">
        <a class="navbar-brand" href="/">Table-Top.games</a>
    </nav>

    <div class="row flex-grow-1" style="margin: 0;">
        <div class="container accordion" id="startAccordion">
            <div class="card">
                <div class="card-header" id="startCreateGameHeading">
                    <h2 class="mb-0">
                        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#startCreateGameBody" aria-expanded="true" aria-controls="startCreateGameBody">
                            Create A Room
                        </button>
                    </h2>
                </div>
                <div id="startCreateGameBody" class="collapse" aria-labelledby="startCreateGameHeading" data-parent="#startAccordion">
                    <div class="card-body">
                        <form>
                            <div class="form-group">
                                <label for="startCreateUserName">Name</label>
                                <input type="text" class="form-control" id="startCreateUserName">
                            </div>
                            <button type="submit" class="btn btn-primary" id="startCreateGame">Play</button>
                        </form>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header" id="startJoinGameHeading">
                    <h2 class="mb-0">
                        <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#startJoinGameBody" aria-expanded="false" aria-controls="startJoinGameBody">
                            Join A Room
                        </button>
                    </h2>
                </div>
                <div id="startJoinGameBody" class="collapse" aria-labelledby="startJoinGameHeading" data-parent="#startAccordion">
                    <div class="card-body">
                        <form>
                            <div class="form-group">
                                <label for="startJoinUserName">Name</label>
                                <input type="text" class="form-control" id="startJoinUserName">
                            </div>
                            <div class="form-group">
                                <label for="startJoinRoomCode">Room Code</label>
                                <input type="text" class="form-control" id="startJoinRoomCode">
                            </div>
                            <button type="submit" class="btn btn-primary" id="startJoinGame">Play</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <div class="container-fluid" id="playingArea" style="display: none; height: calc(100% - 1rem);">
            <div class="row h-100">
                <div class="col h-100">
                    <div class="card h-100">
                        <div id="roomCode" class="card-header">Room Code: ABC123</div>
                        <div class="card-body">
                            TODO game goes here :)
                        </div>
                    </div>
                </div>
                <div class="col-2">
                    <div class="card">
                        <div class="card-header">Players</div>
                        <ul id="playerList" class="list-group list-group-flush"></ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
<script type="module" src="/static/app.js"></script>

</body>
</html>
