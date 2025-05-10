We are a team of students from the College of Computer Science & AI at Ahram Canadian University. Our collaborative efforts are dedicated to developing Chicken Invaders, a project created as part of our coursework. We enjoy combining creativity with technical skills to build engaging and interactive gaming experiences.

# Chicken Invaders 🐔🚀

A modern space shooter game where players defend against waves of invading chickens. Built with Python and Pygame.

![Game Screenshot](Images/Screenshots/gameplay.png)
*Main gameplay screenshot*

## Table of Contents
- [Chicken Invaders 🐔🚀](#chicken-invaders-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
    - [Core Gameplay](#core-gameplay)
    - [Enemy Types](#enemy-types)
    - [Power-ups](#power-ups)
  - [Chicken Types and Behaviors](#chicken-types-and-behaviors)
    - [Basic Movement Patterns](#basic-movement-patterns)
      - [Straight Movement](#straight-movement)
      - [Zigzag Movement](#zigzag-movement)
      - [Circular Movement](#circular-movement)
      - [Dive Attack](#dive-attack)
    - [Special Behaviors](#special-behaviors)
      - [Shield Ability](#shield-ability)
      - [Freeze Ability](#freeze-ability)
      - [Resurrection](#resurrection)
      - [Teleportation](#teleportation)
      - [Cloning](#cloning)
    - [Boss Behaviors](#boss-behaviors)
      - [Klaus Chicken](#klaus-chicken)
      - [Big Chicken](#big-chicken)
      - [Yolk Star](#yolk-star)
    - [Behavior Mechanics](#behavior-mechanics)
  - [Game Mechanics](#game-mechanics)
    - [Player Controls](#player-controls)
    - [Scoring System](#scoring-system)
    - [Level Progression](#level-progression)
  - [Levels](#levels)
    - [Early Levels (1-5)](#early-levels-1-5)
    - [Mid-Game Levels (6-15)](#mid-game-levels-6-15)
    - [Advanced Levels (16-20)](#advanced-levels-16-20)
    - [Final Levels (21-25)](#final-levels-21-25)
    - [Level Features](#level-features)
  - [Technical Details](#technical-details)
    - [Game States](#game-states)
    - [Asset Management](#asset-management)
    - [Collision Detection](#collision-detection)
  - [Installation](#installation)
  - [How to Play](#how-to-play)
  - [Development Team](#development-team)
    - [Team Members](#team-members)
    - [Instructor](#instructor)
  - [Credits](#credits)

## Overview

Chicken Invaders is a browser-based arcade game where players pilot a spaceship to fend off waves of invading chickens. The game features multiple levels, power-ups, different enemy types, and a progression system that increases in difficulty.

![Game Menu](Images/Screenshots/menu.png)
*Main menu screen*

## Features

### Core Gameplay
- **Multiple Levels**: 25 unique levels with increasing difficulty
- **Diverse Enemy Types**: 25 different chicken types with unique behaviors and abilities
- **Power-up System**: Collect various power-ups to enhance your ship
- **Shop System**: Spend points to upgrade your ship and abilities
- **High Score System**: Compete for the highest score
- **Customizable Ships**: Choose from multiple spacecraft designs
- **Customizable Weapons**: Select different fire and missile types

### Enemy Types
1. **Ordinary Chicken**: Basic enemy with straight movement
2. **Military Chicken**: Moves in zigzag pattern
3. **Drone Chicken**: Can shoot at the player
4. **Pilot Chicken**: Performs dive attacks
5. **Metal Chicken**: Has shield ability
6. **Coward Chicken**: Flees from the player
7. **Toxic Chicken**: Can poison the player
8. **Balloon Chicken**: Floats with unpredictable movement
9. **Klaus Chicken**: Boss-type enemy
10. **Chiller Chickens**: Can freeze the player
11. **Phoenix Chicken**: Can resurrect after being defeated
12. **UFO Chicken**: Can teleport
13. **Submarine Chicken**: Can submerge underwater
14. **Slob Chicken**: Has high health
15. **Chickenaut**: Can transform
16. **Egg Ship Chicken**: Can spawn additional enemies
17. **Big Chicken**: Boss-type enemy
18. **Super Chicken**: Can power up
19. **Infini Chicken**: Can clone itself
20. **Feather Brain**: Smart movement patterns
21. **Yolk Star**: Final boss

### Power-ups
- **Health Boost**: Increases max health by 20%
- **Faster Shooting**: Reduces shoot delay by 30%
- **Side Guns**: Adds two additional guns
- **Missile Pack**: Adds 3 missiles
- **Shield**: Reduces damage for one level
- **New Ship**: Unlocks a new ship type

## Chicken Types and Behaviors

### Basic Movement Patterns

#### Straight Movement
![Ordinary Chicken](Images/Objects/Chickens/OrdinaryChickenRegular.png)
- Basic forward movement
- Consistent speed
- No special abilities
- Perfect for beginners

#### Zigzag Movement
![Military Chicken](Images/Objects/Chickens/OrdinaryChickenMilitary.png)
- Side-to-side movement
- Increased speed
- More challenging to hit
- Common in early levels

#### Circular Movement
![Drone Chicken](Images/Objects/Chickens/DroneChicken.png)
- Orbital path around a center point
- Can shoot at player
- Requires timing to hit
- Mid-game challenge

#### Dive Attack
![Pilot Chicken](Images/Objects/Chickens/PilotChicken.png)
- Sudden speed increase
- Direct path to player
- Quick and aggressive
- Requires quick reflexes

### Special Behaviors

#### Shield Ability
![Metal Chicken](Images/Objects/Chickens/MetalSuitChickenRegular.png)
- Activates shield at 50% health
- Reduces damage taken
- Requires strategic shooting
- Common in mid-game

#### Freeze Ability
![Chiller Chicken](Images/Objects/Chickens/Chiller1.png)
- Slows player movement
- Reduces fire rate
- Creates ice particles
- Dangerous in groups

#### Resurrection
![Phoenix Chicken](Images/Objects/Chickens/Phoenix_Chicken_.png)
- Returns to life once
- 50% health on revival
- Requires double elimination
- Late-game challenge

#### Teleportation
![UFO Chicken](Images/Objects/Chickens/UFOChicken.png)
- Random position changes
- Unpredictable movement
- Hard to track
- Advanced gameplay

#### Cloning
![Infini Chicken](Images/Objects/Chickens/CI4_InfiniChick.png)
- Creates copies of itself
- Each clone has full health
- Exponential threat
- Ultimate challenge

### Boss Behaviors

#### Klaus Chicken
![Klaus Chicken](Images/Objects/Chickens/KlausChicken.png)
- High health pool
- Multiple attack patterns
- Shield phases
- First major boss

#### Big Chicken
![Big Chicken](Images/Objects/Chickens/BigChickenCI4.png)
- Massive health pool
- Area attacks
- Summons minions
- Mid-game boss

#### Yolk Star
![Yolk Star](Images/Objects/Chickens/YolkStar.png)
- Final boss
- Multiple phases
- All special abilities
- Ultimate challenge

### Behavior Mechanics

1. **Movement Patterns**
   - Straight: Basic forward movement
   - Zigzag: Sinusoidal movement
   - Circle: Orbital movement
   - Dive: Direct attack pattern
   - Float: Slow, unpredictable movement
   - Flee: Runs from player
   - Teleport: Random position changes

2. **Special Abilities**
   - Shield: Damage reduction
   - Freeze: Player slowdown
   - Poison: Continuous damage
   - Clone: Self-replication
   - Transform: Stat changes
   - Spawn: Creates minions
   - Resurrect: Self-revival

3. **Attack Patterns**
   - Direct: Straight line attacks
   - Spread: Multiple projectiles
   - Area: Damage zones
   - Tracking: Follows player
   - Burst: Rapid fire
   - Charge: Powerful single shot

4. **Defense Mechanisms**
   - Health scaling
   - Shield activation
   - Damage reduction
   - Movement speed
   - Size variation
   - Special immunities

## Game Mechanics

### Player Controls
- **Movement**: Arrow keys or WASD
- **Shoot**: Space bar
- **Missile**: M key
- **Shop**: P key
- **Pause**: ESC key
- **Fullscreen**: F11 key

### Scoring System
- Points are awarded for defeating enemies
- Different enemy types give different point values
- Bonus points for completing levels
- High scores are saved locally

### Level Progression
- Each level introduces new enemy types
- Difficulty increases with each level
- Enemy health and speed scale with level
- Special boss levels at key milestones

## Levels

The game features 25 unique levels, each with increasing difficulty and unique challenges. Here's a breakdown of the level progression:

### Early Levels (1-5)
![Early Levels](Images/Screenshots/early_levels.png)
- Introduction to basic chicken types
- Simple movement patterns
- Basic power-ups
- Focus on learning controls and mechanics

### Mid-Game Levels (6-15)
![Mid-Game](Images/Screenshots/mid_game.png)
- Introduction of special abilities
- More complex enemy patterns
- Increased enemy health and speed
- First boss encounter (Klaus Chicken)

### Advanced Levels (16-20)
![Advanced Levels](Images/Screenshots/advanced_levels.png)
- Multiple enemy types per level
- Complex attack patterns
- Special boss encounters
- Challenging power-up combinations

### Final Levels (21-25)
![Final Levels](Images/Screenshots/final_levels.png)
- Ultimate challenges
- Multiple boss encounters
- Maximum difficulty
- Final boss: Yolk Star

### Level Features
1. **Progressive Difficulty**
   - Enemy health increases by 10% per level
   - Enemy speed increases by 5% per level
   - Number of enemies increases with level

2. **Special Events**
   - Boss battles at levels 10, 15, 20, and 25
   - Power-up rain events
   - Special challenge waves

3. **Level Rewards**
   - Score multipliers
   - Special power-ups
   - Unlockable content

4. **Level Transitions**
   - Smooth transitions between levels
   - Level preview
   - Shop access between levels

![Level Transition](Images/Screenshots/level_transition.png)
*Level transition screen*

## Technical Details

### Game States
- **INTRO**: Initial game introduction
- **MENU**: Main menu screen
- **PLAYING**: Active gameplay
- **GAME_OVER**: Game over screen
- **SHOP**: In-game shop
- **LEVEL_TRANSITION**: Between levels
- **PAUSED**: Game pause screen
- **SETTINGS**: Game settings
- **NAME_INPUT**: Player name input
- **HIGH_SCORES**: High score display
- **ABOUT**: Game information

### Asset Management
- **Images**: Sprites, backgrounds, and UI elements
- **Sounds**: Music, effects, and voice lines
- **Fonts**: Different sizes for various text elements

### Collision Detection
- Pixel-perfect collision using masks
- Multiple collision types:
  - Player-Enemy
  - Bullet-Enemy
  - Missile-Enemy
  - Player-Powerup

## Installation

1. Ensure you have Python 3.x installed
2. Install required packages:
   ```bash
   pip install pygame pillow
   ```
3. Clone the repository:
   ```bash
   git clone [repository-url]
   ```
4. Run the game:
   ```bash
   python Mainv10.py
   ```

## How to Play

1. Start the game and enter your name
2. Use the main menu to:
   - Start a new game
   - View high scores
   - Access settings
   - View about information
3. During gameplay:
   - Defeat waves of chickens
   - Collect power-ups
   - Visit the shop between levels
   - Try to achieve the highest score

## Development Team

### Team Members
| Role        | Name                 | Student ID | Group |
| ----------- | -------------------- | ---------- | ----- |
| Team Leader | Moataz Mahmoud       | 42210055   | B2    |
| Team Member | Adel Adel Ahmed      | 42210211   | A4    |
| Team Member | Ahmed Haytham        | 42210126   | B2    |
| Team Member | Abdelrahman Ahmed    | 42210259   | A1    |
| Team Member | Mohamed Abdel Fattah | 42210180   | B2    |
| Team Member | Ahmed Farhat         | 42210249   | A1    |

### Instructor
- Eng. Diana Emad

## Credits

- Game created with ❤️ by Zer0Day Team
- © 2025 Zer0Day Team. All rights reserved.
- Special thanks to all contributors and testers

---

For any issues or suggestions, please contact the development team. 
