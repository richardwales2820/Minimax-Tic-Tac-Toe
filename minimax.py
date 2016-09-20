"""
Richie Wales, Fall 2016
Minimax for Tic-Tac-Toe, for fun :)
"""

from copy import deepcopy

class TicTacToe:
    """
    This class encompasses all of the logic to set-up and play a test game
    of Tic-Tac-Toe to see the AI in action :) 
    
    The minimax method selects the 
    successor state that leads to the most possible wins. The recursive calls
    add up the amount of possible wins, bubbling up from the terminal node where
    the board is full.
    
    Attributes:
        board: 2D array of the Tic-Tac-Toe board
    """
    
    def __init__(self):
        """Inits TicTacToe with an empty board to play on"""
        self.board = self.createBoard()
        
    def createBoard(self):
        """Sets up an empty 3x3 board for the game"""
        board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        return board
    
    def printBoard(self, board=None):
        """Prints out the 2D array in a TicTacToe, readable form
        
        Args: board: a 2D array corresponding to the game board. If no board is
        passed explicitly, the board instance variable is used.
        """
        
        # Default argument allows any board to be passed for debugging board
        # states in the minimax function
        if not board:
            board = self.board
        
        # eol (end of line) is initially blank so that a row of "-" chars is not
        # printed the first iteration of the loop
        eol = ""
        for row in board:
            print eol
            print "%c | %c | %c" % tuple(row)
            eol = "----------"
        print
    
    def minimax(self, state, maximizing, wins):
        """
        The magic behind minimax. This function takes a board state and finds
        the best successor state that will lead to the most possible wins.
        
        Args:
            state: A 2D array corresponding to a board state of X's and O's
            maximizing: A boolean that details whether the player running this
                function is a MAX player or a MINI adversary.
            wins: An integer that holds the amount of wins from previous states
                to add on new additional wins to be returned by the function
        """
        
        letter = 'X' if maximizing else 'O'
        
        winsDict = {}
        
        # If the O player wins, no win is added. Else, MAX won, so add a win!
        if self.containsWin(state, 'O'):
            return state, wins
            
        if self.containsWin(state, 'X'):
            return state, 1+wins
        
        # The state 2D array must have a deepcopy passed so that if it is 
        # modified, those changes don't affect our state here. Try placing a
        # letter in every possible square and see how those successor states
        # turn out.
        for successor in self.placeLetter(deepcopy(state), letter):
            newState, win = self.minimax(successor, maximizing ^ True, wins)
            winsDict[win] = successor
        
        # Sort the number of wins we achieve so that we can easily access the 
        # best state and max number of wins, or in the case of the MINI opponent
        # we would easily choose the state with the least wins for 'X'
        keys = sorted(winsDict.keys())
        
        if not keys:
            return state, wins
        
        # Return max wins and successor state associated with max wins
        if maximizing:
            return winsDict[keys[-1]], keys[-1]
        
        # Return lowest wins and successor state with least wins
        return winsDict[keys[0]], keys[0]
            
    def playGame(self):
        """
        Continuously calls minimax for the opponent turns, then after placing an
        'X', the player gets a chance to place an 'O' to combat the MAX player.
        """
        
        # While there is no winner, keep playing
        while (not self.containsWin(self.board, 'X')) and \
              (not self.containsWin(self.board, 'O')):
            print "Opponent thinking..."
            self.board, wins = self.minimax(self.board, True, 0)
            self.printBoard()
            
            # Break if a win was found as the player's turn is not needed now
            if self.containsWin(self.board, 'X') or \
               self.containsWin(self.board, 'O'):
                break
            
            print "Select where to place 'O' as row,col (e.g. 0,0 for top-left)"
            coordinates = [int(n) for n in raw_input().split(',')]
            
            # Check for invalid input by the player
            while self.board[coordinates[0]][coordinates[1]] != ' ' or \
            coordinates[0] > 2 or coordinates[1] > 2:
                print "Invalid: Select where to place 'O' as x,y"
                coordinates = [int(n) for n in raw_input().split(',')]
                
            self.board[coordinates[0]][coordinates[1]] = 'O'

        self.printBoard()
        
        if self.containsWin(self.board, 'X'):
            print "X WINS"
            return
            
        print "O WINS"
        
    def placeLetter(self, board, letter):
        """
        Place a letter in every available spot. Add these possible successors
        to the successors list to be returned to the minimax function. 
        
        Args:
            board: 2D array corresponding to a game board state
            letter: The letter of the current player to be placed (X/O)
        
        Returns:
            A list of all of the possible successor board states where a letter
            was placed by the current player.
        """
        successors = []
        for i in xrange(len(board)):
            for j in xrange(len(board[i])):
                if board[i][j] == ' ':
                    newBoard = deepcopy(board)
                    newBoard[i][j] = letter
                    successors.append(newBoard)
        return successors

    
    def checkWin(self, board, dx, dy, startx, starty, letter):
        """
        Checks if there is a win located, provided the start position to check,
        as well as the change row and column position (are we checking row/col
        or a diag).
        
        Args:
            board: 2D array that contains a game board state
            dx: Change in row to be used to check succeeding tiles from the start
                position.
            dy: Change in col to be used to check succeeding tiles from start.
            startx: Start row coordinate for the first tile to be checked
            starty: Start col coordinate ''        ''              ''
            letter: The letter being checked for a win. If we see 3 of letter,
                then a win is decided
        
        Returns:
            True if 3 tiles of the same 'letter' are seen in a row
        """
        tiles = 0
        for i in xrange(3):
            if board[startx + i*dx][starty + i*dy] == letter:
                tiles += 1
        return tiles == 3
            
    def boardFull(self, board):
        """ Checks if there are no free spots in the board
        
        Args:
            board: a 2D array that contains a game board state
            
        Returns:
            False if an empty spot remains. True otherwise.
        """
        for row in board:
            for tile in board:
                if tile == ' ':
                    return False
        return True
            
    def containsWin(self, board, letter):
        """
        This function checks a board state to see if it contains a win by calling
        the checkWin function at every row, col, and diag.
        
        Args:
            board: a 2D array that contains a game board state
            letter: The letter being checked for a win. (X/O)
            
        Returns:
            True if there is a win, False otherwise.
        """
        for i in xrange(3):
            if self.checkWin(board, 0, 1, i, 0, letter) or \
                  self.checkWin(board, 1, 0, 0, i, letter):
                return True
        if self.checkWin(board, 1, 1, 0, 0, letter) or \
           self.checkWin(board, 1, -1, 0, 2, letter):
               return True
        
        return False

if __name__ == '__main__':
    t = TicTacToe()
    t.printBoard()
    t.playGame()
