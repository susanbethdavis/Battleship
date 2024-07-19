# Battleship Game
### Author: Susan Davis, sed2001@ad.unc.edu, Onyen=sed2001

## Overview
The Battleship Game is a Python implementation of the classic board game "Battleship." This game allows for either one or two players to play against each other. In the single-player mode, the player competes against a computer-controlled opponent. The game continues until one player's fleet is entirely sunk.

## Classes

### BattleshipGame
The `BattleshipGame` class is the top-level class that manages the entire game.

#### Methods:
- `__init__(self, num_of_players)`: Initializes the game with either one or two players.
- `play(self)`: Runs the game, alternating turns between players until there is a winner.

### Board
The `Board` class manages the 10x10 grid where each player's boats are placed.

#### Methods:
- `__init__(self)`: Initializes the board as a 10x10 grid of empty cells.
- `__str__(self)`: Returns a string representation of the grid.
- `get_public_view(self)`: Returns a string representation of the grid with boat locations hidden.
- `add_boat(self, boat)`: Adds a boat to the board if the position is legal.
- `attack(self, x, y)`: Records an attack on a given grid cell.
- `is_defeated(self)`: Checks if all boats have been sunk.

### Boat
The `Boat` class represents one of the five boats in the game.

#### Methods:
- `__init__(self, label, size)`: Initializes the boat with a label and size.
- `set_position(self, x, y)`: Sets the boat's position.
- `set_orientation(self, orientation)`: Sets the boat's orientation.

### HumanPlayer
The `HumanPlayer` class represents a player controlled by user input.

#### Methods:
- `__init__(self, player_name)`: Initializes the player with a name, a board, and a fleet of boats.
- `display_stats(self)`: Displays the player's statistics.
- `set_opponent(self, opponent)`: Links the player to their opponent.
- `position_fleet(self)`: Positions the player's fleet on the board.
- `position_boat(self, boat)`: Positions a single boat on the board.
- `take_turn(self)`: Manages a single turn for the player.

### ComputerPlayer
The `ComputerPlayer` class represents a player controlled by a random number generator.

#### Methods:
- `__init__(self, player_name)`: Initializes the computer player with a name, a board, and a fleet of boats.
- `display_stats(self)`: Displays the computer player's statistics.
- `set_opponent(self, opponent)`: Links the computer player to their opponent.
- `position_fleet(self)`: Positions the computer player's fleet on the board.
- `take_turn(self)`: Manages a single turn for the computer player.
- `generate_attack(self)`: Generates a random attack position.

## How to Run
1. Ensure you have Python installed on your system.
2. Save the provided code in a file named `battleship.py`.
3. Open a terminal and navigate to the directory where `battleship.py` is saved.
4. Run the game by executing `python battleship.py`.
5. Follow the on-screen instructions to play the game.

## Game Rules
- Players take turns to attack positions on the opponent's board.
- The game continues until one player's fleet is entirely sunk.
- The player whose fleet remains afloat is declared the winner.

## Contact
For any issues or inquiries, please contact Susan Davis at sed2001@ad.unc.edu.
