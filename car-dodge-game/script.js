class CarDodgeGame {
    constructor() {
        this.gameBoard = document.getElementById('gameBoard');
        this.playerCar = document.getElementById('playerCar');
        this.scoreElement = document.getElementById('score');
        this.speedElement = document.getElementById('speed');
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.gameOverDiv = document.getElementById('gameOver');
        this.finalScoreElement = document.getElementById('finalScore');
        this.restartBtn = document.getElementById('restartBtn');
        
        this.gameState = {
            isRunning: false,
            isPaused: false,
            score: 0,
            speed: 1,
            playerPosition: 1, // 0=left, 1=center, 2=right
            enemyCars: [],
            gameLoop: null,
            spawnTimer: 0,
            speedIncreaseTimer: 0
        };
        
        this.lanes = [25, 50, 75]; // Lane positions in percentage
        this.keys = {};
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.updateDisplay();
        this.updatePlayerPosition(); // Initialize player car position
    }
    
    bindEvents() {
        // Button events
        this.startBtn.addEventListener('click', () => this.startGame());
        this.pauseBtn.addEventListener('click', () => this.togglePause());
        this.restartBtn.addEventListener('click', () => this.restartGame());
        
        // Keyboard events
        document.addEventListener('keydown', (e) => {
            this.keys[e.key] = true;
            this.handleKeyPress(e.key);
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.key] = false;
        });
        
        // Prevent arrow key scrolling
        document.addEventListener('keydown', (e) => {
            if(['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                e.preventDefault();
            }
        });
    }
    
    handleKeyPress(key) {
        // Allow movement even when game is not running (for testing controls)
        // But prevent movement when paused
        if (this.gameState.isPaused) return;
        
        switch(key) {
            case 'ArrowLeft':
                this.movePlayer(-1);
                break;
            case 'ArrowRight':
                this.movePlayer(1);
                break;
        }
    }
    
    movePlayer(direction) {
        const newPosition = this.gameState.playerPosition + direction;
        if (newPosition >= 0 && newPosition <= 2) {
            this.gameState.playerPosition = newPosition;
            this.updatePlayerPosition();
        }
    }
    
    updatePlayerPosition() {
        const leftPosition = this.lanes[this.gameState.playerPosition];
        this.playerCar.style.left = `${leftPosition}%`;
        this.playerCar.style.transform = 'translateX(-50%)';
    }
    
    startGame() {
        this.gameState.isRunning = true;
        this.gameState.isPaused = false;
        this.gameState.score = 0;
        this.gameState.speed = 1;
        this.gameState.playerPosition = 1;
        this.gameState.enemyCars = [];
        this.gameState.spawnTimer = 0;
        this.gameState.speedIncreaseTimer = 0;
        
        this.startBtn.style.display = 'none';
        this.pauseBtn.style.display = 'inline-block';
        this.gameOverDiv.style.display = 'none';
        
        this.updatePlayerPosition();
        this.updateDisplay();
        this.clearEnemyCars();
        this.updateRoadSpeed();
        
        this.gameState.gameLoop = setInterval(() => this.gameUpdate(), 50);
    }
    
    togglePause() {
        this.gameState.isPaused = !this.gameState.isPaused;
        this.pauseBtn.textContent = this.gameState.isPaused ? 'RESUME' : 'PAUSE';
    }
    
    restartGame() {
        this.endGame();
        this.startGame();
    }
    
    endGame() {
        this.gameState.isRunning = false;
        this.gameState.isPaused = false;
        
        if (this.gameState.gameLoop) {
            clearInterval(this.gameState.gameLoop);
            this.gameState.gameLoop = null;
        }
        
        this.startBtn.style.display = 'inline-block';
        this.pauseBtn.style.display = 'none';
        this.gameOverDiv.style.display = 'block';
        this.finalScoreElement.textContent = this.gameState.score;
        
        this.clearEnemyCars();
    }
    
    gameUpdate() {
        if (!this.gameState.isRunning || this.gameState.isPaused) return;
        
        this.updateEnemyCars();
        this.spawnEnemyCar();
        this.checkCollisions();
        this.updateScore();
        this.updateSpeed();
        this.updateDisplay();
    }
    
    spawnEnemyCar() {
        this.gameState.spawnTimer++;
        
        // Spawn rate increases with speed
        const spawnRate = Math.max(30 - (this.gameState.speed * 3), 15);
        
        if (this.gameState.spawnTimer >= spawnRate) {
            this.gameState.spawnTimer = 0;
            
            // Random lane selection
            const lane = Math.floor(Math.random() * 3);
            const enemyCar = this.createEnemyCar(lane);
            this.gameState.enemyCars.push(enemyCar);
        }
    }
    
    createEnemyCar(lane) {
        const enemyDiv = document.createElement('div');
        enemyDiv.className = 'enemy-car';
        enemyDiv.style.left = `${this.lanes[lane]}%`;
        enemyDiv.style.transform = 'translateX(-50%)';
        enemyDiv.style.top = '-60px';
        
        this.gameBoard.appendChild(enemyDiv);
        
        return {
            element: enemyDiv,
            lane: lane,
            y: -60,
            speed: 3 + this.gameState.speed
        };
    }
    
    updateEnemyCars() {
        for (let i = this.gameState.enemyCars.length - 1; i >= 0; i--) {
            const car = this.gameState.enemyCars[i];
            car.y += car.speed;
            car.element.style.top = `${car.y}px`;
            
            // Remove cars that have gone off screen
            if (car.y > 500) {
                car.element.remove();
                this.gameState.enemyCars.splice(i, 1);
            }
        }
    }
    
    checkCollisions() {
        const playerLane = this.gameState.playerPosition;
        const playerY = 400; // Player car Y position (bottom 50px from 450px height)
        
        for (let car of this.gameState.enemyCars) {
            if (car.lane === playerLane) {
                // Check if enemy car is in collision range
                if (car.y >= playerY - 50 && car.y <= playerY + 30) {
                    this.endGame();
                    return;
                }
            }
        }
    }
    
    updateScore() {
        this.gameState.score += this.gameState.speed;
    }
    
    updateSpeed() {
        this.gameState.speedIncreaseTimer++;
        
        // Increase speed every 5 seconds (100 updates at 50ms intervals)
        if (this.gameState.speedIncreaseTimer >= 100) {
            this.gameState.speedIncreaseTimer = 0;
            this.gameState.speed = Math.min(this.gameState.speed + 1, 10);
            this.updateRoadSpeed();
        }
    }
    
    updateRoadSpeed() {
        // Update road animation speed based on game speed
        const road = document.querySelector('.road');
        road.className = 'road';
        
        if (this.gameState.speed >= 4) {
            road.classList.add('speed-boost');
        }
        if (this.gameState.speed >= 7) {
            road.classList.add('speed-boost-2');
        }
        if (this.gameState.speed >= 10) {
            road.classList.add('speed-boost-3');
        }
    }
    
    updateDisplay() {
        this.scoreElement.textContent = this.gameState.score;
        this.speedElement.textContent = this.gameState.speed;
    }
    
    clearEnemyCars() {
        // Remove all enemy cars from DOM and array
        this.gameState.enemyCars.forEach(car => {
            if (car.element && car.element.parentNode) {
                car.element.remove();
            }
        });
        this.gameState.enemyCars = [];
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new CarDodgeGame();
});

// Add some visual feedback for key presses
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        const playerCar = document.getElementById('playerCar');
        if (playerCar) {
            // Add a brief scale effect for visual feedback
            playerCar.style.transition = 'transform 0.1s ease';
            const currentTransform = playerCar.style.transform || 'translateX(-50%)';
            playerCar.style.transform = currentTransform + ' scale(1.1)';
            
            setTimeout(() => {
                playerCar.style.transform = currentTransform;
            }, 100);
        }
    }
});