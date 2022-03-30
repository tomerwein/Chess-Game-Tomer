class Move():
    def __init__(self, start_square, end_square):
        self.startRow, self.startCol = start_square[0], start_square[1]
        self.endRow, self.endCol = end_square[0], end_square[1]

    def __eq__(self, other):
        # check if two moves are equal
        if self.startRow == other.startRow and self.startCol == other.startCol and self.endRow == other.endRow and self.endCol == other.endCol:
            return True
        return False
