# Tower Defense

This is a Python-based tower defense game that I built with two other team members using Pygame. In the game, you defeat waves of enemies by buying towers that damage them, to prevent them from reaching the end of the path. All of this runs on a window, and features a vast collection of custom-made sprites and animations.

## How It Works

The game is built around a main loop that handles input, updates the game state, and redraws the screen each frame. The main pieces are:

- **`Tower classes`** - Each tower type is its own class with its own range, damage, and fire rate. Every frame, each placed tower checks for enemies in range and attacks on a cooldown timer.
- **`Enemy system`** - Enemies follow predefined paths across the map, advancing toward the end point. Each enemy type has its own health, speed, and animation frames.
- **`Wave system`** - Enemies spawn from a queue on a timer, and the wave advances once all enemies are cleared or the wave timer runs out. Completing a wave grants bonus cash.
- **`Drag-and-drop placement`** - Towers are selected from a tray at the bottom of the screen and dragged onto valid tiles. Placement checks against a set of invalid tiles and already-occupied tiles.
- **`Sprite animation`** - Each enemy is animated frame-by-frame. Special enemies have their own animations for unique actions, like the boss attacking or the necromancer summoning.

## Key Features

- **Ten waves of increasing difficulty** - from basic zombies up to a final boss
- **Seven tower types** - each with distinct damage, fire rate, and range, including a slow-effect tower
- **Ten enemy types** - including speedy, heavy, hidden, flying, and several boss-tier enemies
- **Custom sprite animations** - hand-designed frames for movement, attacks, summoning, and other special actions
- **In-game economy** - buy towers with cash, earn cash from defeating enemies and completing waves

## Tech Stack

- **Python 3** - Core language
- **Pygame** - Game loop, rendering, input handling, and sound

## Controls

The game relies solely on the player's cursor, with buying and placing towers both being controlled by the mouse. To buy and place a tower, simply click on the desired tower in the tower shop at the bottom of the screen, drag the cursor onto an empty tile, and click again to place it down.

## Getting Started

### Prerequisites

Tower Defense requires Python 3.8 or later as well as the Pygame library.

To run the game, run these commands in your terminal:

```bash
pip install pygame
git clone https://github.com/BParniak/tower-defense.git
cd tower-defense
python Tower_Defense.py
```

After the initial setup, you do not need to clone the repository or reinstall Pygame. To start Tower Defense again, open a terminal and navigate to the Tower Defense folder:

```bash
cd path\to\tower-defense
python Tower_Defense.py
```

Replace ```path/to/tower-defense``` with the location where you cloned the repository.
