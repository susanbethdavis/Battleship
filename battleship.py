__author__ = 'Susan Davis, sed2001@ad.unc.edu, Onyen=sed2001'
import random
# The BattleshipGame class is the top level class.  A game is created for 1 or 2 players, then the game is played
# until there is a winner.


class BattleshipGame:

    # Initialize the game based on the number of players.  Create the two player objects (two humans, or one human
    # and one computer.  Then link the players so that they are aware of their opponent (required to let one player
    # attack the board of the other player.
    def __init__(self, num_of_players):
        # Create the players.
        if num_of_players == 1:
            self.players = [HumanPlayer("Player 1"), ComputerPlayer("The Computer")]
        else:
            self.players = [HumanPlayer("Player 1"), HumanPlayer("Player 2")]

        # Let the two players know about each other, so they can attack the opponent when the game starts.
        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

    # This method runs the game.  It first has the two players position their boats.  It then goes into a loop,
    # in which players alternate turns until there is a winner.
    def play(self):

        # Positioning the fleets for both players
        self.players[0].position_fleet()
        self.players[1].position_fleet()

        # Next, begin the game.  Repeat the game-play loop as long as there is not a winner.
        input("The boats are ready... it's time to play.  Press enter to begin!")
        winner = False
        first_players_turn = True
        while not winner:
            print("Current Game Stats:")
            self.players[0].display_stats()
            self.players[1].display_stats()
            print()
            # Take a turn for the next player.
            if first_players_turn:

                winner = self.players[0].take_turn()
                # Check to see if the game is over.
                if winner:
                    print("Game over!", self.players[0].player_name, "wins!")
            else:

                winner = self.players[1].take_turn()
                # Check to see if the game is over.
                if winner:
                    print("Game over!", self.players[1].player_name, "wins!")

            # Swap the turn so that the other player goes on the next iteration.
            first_players_turn = not first_players_turn


# The Board class manages the 10x10 grid that contains each player's boats.  The board has cells, each of which
# is set to one of four values:
# Boat: A square that has a boat.  Represented as " B".
# Empty: A square that has no boat. Represented as " _".
# Hit: A square that was a boat, but one that was hit by an attack. Represented as "X"
# Miss: A square that was attacked, but that has no boat.  Represented as "_O"
class Board:

    # Initialize the board to a 10x10 grid of empty cells
    def __init__(self):
        # The grid
        self.grid = [[" _"]*10 for i in range(10)]
        # The hit count, used to count successful attacks. When the hit count reaches 17, the game is over.  This
        # counter allows us to avoid looking for un-hit boats each turn to see if the game is over.  Instead, we
        # can simply count hits as they happen and look for us to reach the total of 17.
        self.hit_count = 0

    # Converts the grid to a string representation for printing.
    def __str__(self):
        str_val = "  0 1 2 3 4 5 6 7 8 9\n"
        for i in range(10):
            str_val += str(i)
            for j in range(10):
                str_val += self.grid[i][j]
            if i != 9:
                str_val += "\n"
        return str_val

    # Converts the grid to a string representation with boat locations hidden. Used to show the board to the opponent.
    def get_public_view(self):
        str_val = "  0 1 2 3 4 5 6 7 8 9\n"
        for i in range(10):
            str_val += str(i)
            for j in range(10):
                if self.grid[i][j] == " B":
                    str_val += " _"
                else:
                    str_val += self.grid[i][j]
            if i != 9:
                str_val += "\n"
        return str_val

    # Adds a boat to the board.  Returns False if the boat can't legally be positioned at the requested location.
    # A legal position must be entirely on the board and must not overlap with any other boats.
    def add_boat(self, boat):
        # First check to make sure the boat position is within range.
        width = 1
        height = 1
        if boat.orientation == "v":
            height = boat.size
        else:
            width = boat.size
        if (boat.x < 0) or (boat.y < 0) or (boat.x+width > 10) or (boat.y+height > 10):
            return False

        # Next check to see if the boat's position is occupied
        for x in range(width):
            for y in range(height):
                if self.grid[boat.y + y][boat.x + x] != " _":
                    return False

        # The function would have returned False if the board didn't fit.  That means the position is valid.
        # We can now update the board to show that the boat is in place.
        for x in range(width):
            for y in range(height):
                self.grid[boat.y + y][boat.x + x] = " B"
        return True

    # The attack method records an attack on a given grid cell
    def attack(self, x, y):
        # See what is currently at this position.
        current_value = self.grid[y][x]
        # We can only have a hit if this is a Boat cell.
        if current_value == " B":
            self.grid[y][x] = " X"
            self.hit_count += 1
            return True
        # If the cell is empty, we can mark it as a miss.
        elif current_value == " _":
            self.grid[y][x] = " O"
            return False
        # If the cell was not empty or boat, then it must have previously been attacked.  We can ignore a repeat attack
        # since nothing in the grid should change.
        else:
            return False

    # Checks to see if the board has been fully defeated (i.e. if all boats have been sunk).
    def is_defeated(self):
        if self.hit_count == 17:
            return True
        else:
            return False


# The boat class represents one of the 5 boats.
class Boat:
    # Initialize the boat with a label (e.g., Destroyer) and a size (e.g., 3).  The position gets set later and will
    # be undefined even after the initialization method.
    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.x = None
        self.y = None
        self.orientation = None

    # Set the boat position.  The x,y value corresponds to the top-left position of the boat.  It extends either to the
    # right or down (depending on the boat's orientation) by SIZE cells.
    def set_position(self, x, y):
        self.x = x
        self.y = y

    # Set the boat orientation.  The orientation must be either "v" or "h" for vertical or horizontal respectively.
    def set_orientation(self, orientation):
        self.orientation = orientation


# The HumanPlayer class represents a player controlled by user input.
class HumanPlayer:
    # Initialize the player with a name, a blank board, and a fleet of five boats.
    def __init__(self, player_name):
        self.player_name = player_name
        self.board = Board()
        self.fleet = [Boat("Aircraft Carrier", 5), Boat("Battleship", 4), Boat("Submarine", 3), Boat("Destroyer", 3), \
                      Boat("Patrol Boat", 2)]
        self.opponent = None
        self.total_attacks = 0
        self.hits = 0
        self.misses = 0

    # Display the statistics for each round played for each player

    def display_stats(self):
        print(f"{self.player_name} Stats - Attacks: {self.total_attacks}, Hits: {self.hits}, Misses: {self.misses}")

    # Link the player to his/her opponent.
    def set_opponent(self, opponent):
        self.opponent = opponent

    # Position the fleet, one boat at a time.
    def position_fleet(self):
        # Warn the user about what he/she needs to do...
        input(self.player_name+": Are you ready to position your fleet?  Press enter to begin!")

        # Position the boats.
        for boat in self.fleet:
            self.position_boat(boat)

        # Confirm the final board to the user now that the positioning is done.
        print("Your fleet is ready to play.  Your board is positioned as follows:")
        print(self.board)

    # Positions a single boat.  Helper method for positionFleet
    def position_boat(self, boat):
        # Show the board as it exists before this boat is positioned.
        print(self.board)
        print("You need to position a", boat.label, "of length", boat.size, "on the board above.")
        # Ask the user to say if the boat is horizontal or vertical.
        orientation = None
        while orientation is None:
            orientation = input("Would you like to use a vertical or horizontal orientation? (v/h) ")
            if (orientation != "v") and (orientation != "h"):
                print("You must enter a 'v' or a 'h'.  Please try again.")
                orientation = None
        # Ask the user for the top-left position of the boat.
        position = None
        while position is None:
            try:
                position = input("Please enter the position for the top-left location of the boat. " + \
                                 " Use the form x,y (e.g., 1,3): ")
                coords = position.split(",")
                x = int(coords[0])
                y = int(coords[1])
                boat.set_orientation(orientation)
                boat.set_position(x,y)
                # Add the boat to the board.
                if not self.board.add_boat(boat):
                    # The board refused to add the boat!!! Raise an exception so that the user is forced
                    # to try a new position.
                    raise Exception
            except ValueError:
                print("You must a valid position for the boat.  Please try again.")
                position = None
            except:
                print("You must choose a position that is (a) on the board and (b) doesn't intersect" + \
                      "with any other boats.")
                position = None

    # This function managers a single turn for the player.
    def take_turn(self):
        # Display boards.
        print(self.player_name+"'s board:")
        print(self.board)
        print()
        print("Your view of "+self.opponent.player_name+"'s board:")
        print(self.opponent.board.get_public_view())
        # Get attack position.
        position = None
        while position is None:
            try:
                position = input(f"{self.player_name}, please enter the position you would like to attack. Use the form x,y (e.g., 1,3): ")
                coords = position.split(",")
                x = int(coords[0])
                y = int(coords[1])
                if (x < 0) or (x > 9) or (y < 0) or (y > 9):
                    raise Exception
            except:
                print("You must a valid position in the form x,y where both x and y are integers in the range of" + \
                      "0-9. Please try again.")
                position = None

        # Perform attack
        self.total_attacks += 1
        hit_flag = self.opponent.board.attack(x, y)
        if hit_flag:
            self.hits += 1
            print("You hit a boat!")
        else:
            self.misses += 1
            print("You missed.")

        # Return true if the opponent has been defeated.  Otherwise, false.
        if self.opponent.board.is_defeated():
            return True
        else:
            return False

# The ComputerPlayer class represents a player controlled by a random number generator.


class ComputerPlayer:
    def __init__(self, player_name):
        self.player_name = player_name
        self.board = Board()
        self.fleet = [Boat("Aircraft Carrier", 5), Boat("Battleship", 4),
                      Boat("Submarine", 3), Boat("Destroyer", 3),
                      Boat("Patrol Boat", 2)]
        self.opponent = None
        self.attacked_positions = set()
        self.total_attacks = 0
        self.hits = 0
        self.misses = 0

    # Display the statistics for each round played for the computer

    def display_stats(self):
        print(f"{self.player_name} Stats - Attacks: {self.total_attacks}, Hits: {self.hits}, Misses: {self.misses}")

    # Link the computer to its opponent
    def set_opponent(self, opponent):
        self.opponent = opponent

    # Position the fleet, one boat at a time.

    def position_fleet(self):
        for boat in self.fleet:
            positioned = False
            while not positioned:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation = random.choice(["v", "h"])
                boat.set_orientation(orientation)
                boat.set_position(x, y)
                positioned = self.board.add_boat(boat)

    # This function managers a single turn for the computer.

    def take_turn(self):
        x, y = self.generate_attack()
        if (x, y) in self.attacked_positions:
            return False
        self.attacked_positions.add((x, y))
        self.total_attacks += 1
        hit_flag = self.opponent.board.attack(x, y)
        if hit_flag:
            self.hits += 1
            print(f"{self.player_name} hit a boat at ({x}, {y})!")
        else:
            self.misses += 1
            print(f"{self.player_name} missed at ({x}, {y}).")

        return self.opponent.board.is_defeated()

    # Perform attack
    def generate_attack(self):
        x, y = random.randint(0, 9), random.randint(0, 9)
        while (x, y) in self.attacked_positions and len(self.attacked_positions) < 100:
            x, y = random.randint(0, 9), random.randint(0, 9)
        return x, y


