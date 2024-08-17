


var config = {
    type: Phaser.AUTO,
    width: window.innerWidth,
    height: window.innerHeight,
    backgroundColor: '#1C1C1C',
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

var game = new Phaser.Game(config);

function preload() {
    // Load any assets here
}

function startPhaserGame(playerName) {
    var config = {
        // Phaser game configuration...
        scene: {
            preload: preload,
            create: function() { create.call(this, playerName); },
            update: update
        }
    };

    var game = new Phaser.Game(config);
}


function startGame() {
    var playerName = document.getElementById('playerName').value || 'Player';
    document.getElementById('nameForm').style.display = 'none'; // Hide the form

    // Pass the playerName to your game's start function or global variable
    startPhaserGame(playerName);
}

function create(playerName) {
    // Create game objects here

}

function update() {
    // Game logic updates here
}
