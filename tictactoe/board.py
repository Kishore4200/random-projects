from square import Square
from enum import Enum, auto

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
        
class Direction(AutoName):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    NORTHEAST = auto()
    NORTHWEST = auto()
    SOUTHEAST = auto()
    SOUTHWEST = auto()
    
    def getOpposite(self):
        if (self == self.NORTH): return self.SOUTH
        if (self == self.SOUTH): return self.NORTH
        if (self == self.EAST): return self.WEST
        if (self == self.WEST): return self.EAST
        if (self == self.NORTHWEST): return self.SOUTHEAST
        if (self == self.NORTHEAST): return self.SOUTHWEST
        if (self == self.SOUTHWEST): return self.NORTHEAST
        if (self == self.SOUTHEAST): return self.NORTHWEST

board = []
for i in range(9):
    board.append(Square(i))
board[0].setNeighbors([[board[1], Direction.EAST], [board[3], Direction.SOUTH], [board[4], Direction.SOUTHEAST]])
board[1].setNeighbors([[board[0], Direction.WEST], [board[2], Direction.EAST], [board[3], Direction.SOUTHWEST], [board[4], Direction.SOUTH], [board[5], Direction.SOUTHEAST]])
board[2].setNeighbors([[board[1], Direction.WEST], [board[4], Direction.SOUTHWEST], [board[5], Direction.SOUTH]])
board[3].setNeighbors([[board[0], Direction.NORTH], [board[1], Direction.NORTHEAST], [board[4], Direction.EAST], [board[7], Direction.SOUTHEAST], [board[6], Direction.SOUTH]])
board[4].setNeighbors([[board[0], Direction.NORTHWEST], [board[1], Direction.NORTH], [board[2], Direction.NORTHEAST], [board[3], Direction.WEST], [board[5], Direction.EAST], [board[6], Direction.SOUTHWEST], [board[7], Direction.SOUTH], [board[8], Direction.SOUTHEAST]])
board[5].setNeighbors([[board[4], Direction.WEST], [board[1], Direction.NORTHWEST], [board[2], Direction.NORTH], [board[8], Direction.SOUTH], [board[7], Direction.SOUTHWEST]])
board[6].setNeighbors([[board[3], Direction.NORTH], [board[4], Direction.NORTHEAST], [board[7], Direction.EAST]])
board[7].setNeighbors([[board[6], Direction.WEST], [board[3], Direction.NORTHWEST], [board[4], Direction.NORTH], [board[5], Direction.NORTHEAST], [board[8], Direction.EAST]])
board[8].setNeighbors([[board[7], Direction.WEST], [board[4], Direction.NORTHWEST], [board[5], Direction.NORTH]])

def drawBoard():
    print(" ", board[0].getValue(), "|", board[1].getValue(), "|", board[2].getValue())
    print("  ----------")
    print(" ", board[3].getValue(), "|", board[4].getValue(), "|", board[5].getValue())
    print("  ----------")
    print(" ", board[6].getValue(), "|", board[7].getValue(), "|", board[8].getValue())

def isWinner(player, lastPlaced):
    candidates = board[lastPlaced].getMatchingNeighbors()

    # checks for candidates on opposite sides of the current square
    for c in candidates:
        for c2 in candidates:
            if (c[1] == c2[1].getOpposite()):
                return True

    # pursue lines in the directions of the matching neighbors
    while (len(candidates) > 0):
        toCheck = candidates[0]
        print("toCheck:", toCheck)
        secondaryNeighbors = toCheck[0].getMatchingNeighbors()
        for s in secondaryNeighbors:
            if (s[1] == toCheck[1]):
                print(s[0].getLocation())
                print(toCheck[0].getLocation())
                return True
        candidates.remove(candidates[0])

    return False

def calculateNeighbors(width, height, square):
    if (square > width*height-1 or square < 0):
        return [-1, -1]

    row = int(square/width)
    col = square % width

    neighbors = []
    neighbors.append([(row-1)*width + col, Direction.NORTH])
    neighbors.append([(row-1)*width + (col+1), Direction.NORTHEAST])
    neighbors.append([row*width + (col+1), Direction.EAST])
    neighbors.append([(row+1)*width + (col+1), Direction.SOUTHEAST])
    neighbors.append([(row+1)*width + col, Direction.SOUTH])
    neighbors.append([(row+1)*width + (col-1), Direction.SOUTHWEST])
    neighbors.append([row*width + (col-1), Direction.WEST])
    neighbors.append([(row-1)*width + (col-1), Direction.NORTHWEST])
    
    # remove neighbors that do not apply
    global i
    i = 0
    while (i < len(neighbors)):
        # if cell is in top row remove all neighbors to the north
        if (row == 0):
            if (neighbors[i][1] == Direction.NORTH or neighbors[i][1] == Direction.NORTHWEST or neighbors[i][1] == Direction.NORTHEAST):
                neighbors.remove(neighbors[i])
                i = i - 1
        # if cell is in bottom row remove all neighbors to the south
        if (row == height - 1):
            if (neighbors[i][1] == Direction.SOUTH or neighbors[i][1] == Direction.SOUTHWEST or neighbors[i][1] == Direction.SOUTHEAST):
                neighbors.remove(neighbors[i])
                i = i - 1        
        # if cell is in left column remove all neighbors to the west
        if (col == 0):
            if (neighbors[i][1] == Direction.WEST or neighbors[i][1] == Direction.SOUTHWEST or neighbors[i][1] == Direction.NORTHWEST):
                neighbors.remove(neighbors[i])
                i = i - 1             
        # if cell is in right column remove all neighbors to the east
        if (col == width - 1):
            if (neighbors[i][1] == Direction.EAST or neighbors[i][1] == Direction.NORTHEAST or neighbors[i][1] == Direction.SOUTHEAST):
                neighbors.remove(neighbors[i])
                i = i - 1 
        i = i + 1

    return neighbors
