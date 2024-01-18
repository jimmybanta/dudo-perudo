var config = {
    type: Phaser.AUTO,
    width: window.innerWidth,
    height: window.innerHeight,
    // background should be tan
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

function create() {
    // Create game objects here
}

function update() {
    // Game logic updates here
}
