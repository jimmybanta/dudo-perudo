
function startGame() {
    var playerName = document.getElementById('playerName').value || 'Player';
    document.getElementById('nameForm').style.display = 'none'; // Hide the form

    // Pass the playerName to your game's start function or global variable
    startPhaserGame(playerName);
}


