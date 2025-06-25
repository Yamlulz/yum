# LED Car Dodge Game

A classic retro-style car dodge game with LED/neon aesthetics. Move left and right using arrow keys to avoid oncoming traffic and survive as long as possible!

## Features

- **Retro LED Graphics**: Classic green neon-style visuals with pixelated car designs
- **Progressive Difficulty**: Game speed increases over time for greater challenge
- **Score System**: Earn points based on survival time and current speed
- **Responsive Controls**: Smooth left/right movement using arrow keys
- **Visual Feedback**: Car scaling effect when moving, speed-based road animations

## How to Play

1. **Controls**: Use the ← and → arrow keys to move your car left and right
2. **Objective**: Avoid the red enemy cars coming towards you
3. **Scoring**: Your score increases continuously based on your current speed level
4. **Speed**: The game gets faster every 5 seconds, making it more challenging
5. **Game Over**: The game ends when you collide with an enemy car

## How to Run

### Option 1: Direct File Opening
1. Open `index.html` directly in your web browser
2. The game should load and be ready to play

### Option 2: Local Server (Recommended)
1. Navigate to the game directory in your terminal
2. Start a local server:
   ```bash
   # Using Python 3
   python3 -m http.server 8000
   
   # Or using Python 2
   python -m SimpleHTTPServer 8000
   
   # Or using Node.js (if you have http-server installed)
   npx http-server
   ```
3. Open your browser and go to `http://localhost:8000`

## Game Controls

- **Arrow Left (←)**: Move car to the left lane
- **Arrow Right (→)**: Move car to the right lane
- **START GAME**: Begin a new game
- **PAUSE/RESUME**: Pause or resume the current game
- **RESTART**: Start over after game over

## Technical Details

- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: LED/Neon theme with CSS animations
- **Game Loop**: 50ms intervals (20 FPS) for smooth gameplay
- **Collision Detection**: Lane-based collision system
- **Responsive Design**: Adapts to different screen sizes

## Game Mechanics

- **Player Car**: Green LED-style car that moves between 3 lanes
- **Enemy Cars**: Red cars that spawn randomly and move downward
- **Speed Levels**: 1-10, with visual and gameplay effects
- **Spawn Rate**: Enemy cars spawn more frequently as speed increases
- **Lane System**: 3-lane highway with yellow dividers

Enjoy the nostalgic LED car dodge experience!