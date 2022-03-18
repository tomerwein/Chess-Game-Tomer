from Move import *


class GameState():
    def __init__(self):
        # Chess Bored 8X8
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.realRows = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
        self.realCols = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        self.index = -1
        self.whiteKingMoved, self.blackKingMoved = False, False
        self.whiteRightRockMoved, self.whiteLeftRockMoved = False, False
        self.blackRightRockMoved, self.blackLeftRockMoved = False, False

    def makeMove(self, move):
        # check the color of the current player
        if self.checkPossibleColor(move):
            # check if there is a check

            possible_moves = self.getPossibleMoves()
            print(len(possible_moves))

            if len(possible_moves) < 10:
                for move in possible_moves:
                    self.printMove(move)

            # check if the specific move is legal
            if self.isMoveLegal(move, possible_moves):
                endPoint = self.board[move.endRow][move.endCol]
                startPoint = self.board[move.startRow][move.startCol]

                # check the opponent color
                # if self.whiteToMove:
                #     opponent_color = "b"
                # else:
                #     opponent_color = "w"

                # check if the king move is legal (the square is not threaded)
                # if startPoint[1] == "K":
                #     if self.checkIfKingMovellegal(move.endRow, move.endCol, possible_moves, opponent_color):
                #         return

                self.board[move.endRow][move.endCol] = startPoint
                self.board[move.startRow][move.startCol] = "--"

                # check if still there is a check
                opposite_possible_moves = self.getOppositePossibleMoves()
                if self.checkExist(opposite_possible_moves):
                    self.board[move.startRow][move.startCol] = startPoint
                    self.board[move.endRow][move.endCol] = endPoint
                    print("illegal")
                    return

                    # check if a rock moved
                if startPoint == "wR" or \
                        startPoint == "bR":
                    self.updateRockMoves(move)

            elif self.castling(move):
                endPoint = self.board[move.endRow][move.endCol]

            else:
                return

            # if move legal, add the move to the moveLog (saves all the moves that had been done)
            if self.index == len(self.moveLog) - 1:
                self.moveLog.append([move, endPoint])
            else:
                while self.index != len(self.moveLog) - 1:
                    self.moveLog.pop()
                self.moveLog.append([move, endPoint])

            self.index += 1
            self.whiteToMove = not self.whiteToMove  # swap players move

            # check promotion
            self.promotion()

            # print move
            print(self.realCols[move.startCol] + self.realRows[move.startRow] + ":" +
                  self.realCols[move.endCol] + self.realRows[move.endRow])  # print the move

    def printMove(self, move):
        print("start move: " + str(move.startRow) + ":" + str(move.startCol))
        print("end move: " + str(move.endRow) + ":" + str(move.endCol))

    def checkExist(self, opposite_moves):
        if self.whiteToMove:
            for checkMove in opposite_moves:
                if self.board[checkMove.startRow][checkMove.startCol][0] == "b" and \
                        self.board[checkMove.endRow][checkMove.endCol] == "wK" and \
                        self.board[checkMove.startRow][checkMove.startCol][1] != "P":
                    return True
            return False

        else:
            for checkMove in opposite_moves:
                if self.board[checkMove.startRow][checkMove.startCol][0] == "w" and \
                        self.board[checkMove.endRow][checkMove.endCol] == "bK" and \
                        self.board[checkMove.startRow][checkMove.startCol][1] != "P":
                    print("check")
                    return True
            return False

    def updateRockMoves(self, move):
        r, c = move.startRow, move.startCol
        if r == 0 and c == 0:
            self.blackLeftRockMoved = True
        elif r == 0 and c == 7:
            self.blackRightRockMoved = True
        elif r == 7 and c == 0:
            self.whiteLeftRockMoved = True
        elif r == 7 and c == 7:
            self.whiteRightRockMoved = True

    def isMoveLegal(self, move, possible_moves):
        for checkMove in possible_moves:
            if checkMove == move:
                return True
        return False

    def undoMove(self):
        if self.index >= 0:
            move = self.moveLog[self.index]

            # Check if undo castling needed (next four conditions)
            if move[0] == Move((7, 4), (7, 6)):
                self.board[7][4], self.board[7][7] = "wK", "wR"
                self.board[7][5], self.board[7][6] = "--", "--"

            elif move[0] == Move((7, 4), (7, 2)):
                self.board[7][4], self.board[7][0] = "wK", "wR"
                self.board[7][2], self.board[7][3] = "--", "--"

            elif move[0] == Move((0, 4), (0, 6)):
                self.board[0][4], self.board[0][7] = "bK", "bR"
                self.board[0][5], self.board[0][6] = "--", "--"

            elif move[0] == Move((0, 4), (0, 2)):
                self.board[0][4], self.board[0][0] = "bK", "bR"
                self.board[0][2], self.board[0][3] = "--", "--"

            # Undo the rest of the cases
            else:
                self.board[move[0].startRow][move[0].startCol] = \
                    self.board[move[0].endRow][move[0].endCol]
                self.board[move[0].endRow][move[0].endCol] = move[1]
                self.whiteToMove = not self.whiteToMove  # swap players move

            self.index -= 1

    def redoMove(self):
        if self.index < len(self.moveLog) - 1:
            self.index += 1
            move = self.moveLog[self.index]
            # Check if redo move is castling
            if move[0] == Move((7, 4), (7, 6)):
                self.board[7][5], self.board[7][6] = "wR", "wK"
                self.board[7][4], self.board[7][7] = "--", "--"

            elif move[0] == Move((7, 4), (7, 2)):
                self.board[7][2], self.board[7][3] = "wK", "wR"
                self.board[7][0], self.board[7][4] = "--", "--"

            elif move[0] == Move((0, 4), (0, 6)):
                self.board[0][5], self.board[0][6] = "bR", "bK"
                self.board[0][4], self.board[0][7] = "--", "--"

            elif move[0] == Move((0, 4), (0, 2)):
                self.board[0][2], self.board[0][3] = "bK", "bR"
                self.board[0][0], self.board[0][4] = "--", "--"

            # if redo move isn't castling
            else:
                self.board[move[0].endRow][move[0].endCol] = \
                    self.board[move[0].startRow][move[0].startCol]
                self.board[move[0].startRow][move[0].startCol] = "--"
                self.whiteToMove = not self.whiteToMove  # swap players move

    def checkPossibleColor(self, move):
        if self.whiteToMove and self.board[move.startRow][move.startCol][0] == 'w':
            return True
        if not self.whiteToMove and self.board[move.startRow][move.startCol][0] == 'b':
            return True
        return False

    def getOppositePossibleMoves(self):
        self.whiteToMove = not self.whiteToMove  # swap players move
        oppositeMoves = self.getPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # swap players move
        return oppositeMoves

# get all possible moves in a list
    def getPossibleMoves(self):
        possibleMoves = []
        if self.whiteToMove:
            for r in range(len(self.board)):
                for c in range(len(self.board)):
                    if self.board[r][c][0] == "w":
                        if self.board[r][c][1] == "P":
                            self.getPawnMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "R":
                            self.getRockMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "B":
                            self.getBishopMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "N":
                            self.getKnightMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "Q":
                            self.getRockMoves(r, c, possibleMoves)
                            self.getBishopMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "K":
                            self.getKingMoves(r, c, possibleMoves)
        else:
            for r in range(len(self.board)):
                for c in range(len(self.board)):
                    if self.board[r][c][0] == "b":
                        if self.board[r][c][1] == "P":
                            self.getPawnMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "R":
                            self.getRockMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "B":
                            self.getBishopMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "N":
                            self.getKnightMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "Q":
                            self.getRockMoves(r, c, possibleMoves)
                            self.getBishopMoves(r, c, possibleMoves)
                        elif self.board[r][c][1] == "K":
                            self.getKingMoves(r, c, possibleMoves)

        return possibleMoves

# check if the move is castling and if it's legal
    def castling(self, move):
        # check if the white king has moved
        if not self.whiteKingMoved:
            # check white right castling
            if move.startRow == 7 and move.startCol == 4 and move.endRow == 7 and \
                    move.endCol == 6 and not self.whiteRightRockMoved and \
                    self.board[7][5] == "--" and self.board[7][6] == "--":
                self.board[7][4] = "--"
                self.board[7][5] = "wR"
                self.board[7][6] = "wK"
                self.board[7][7] = "--"
                self.whiteKingMoved = True
                return True

            # check white left castling
            if move.startRow == 7 and move.startCol == 4 and move.endRow == 7 and \
                    move.endCol == 2 and not self.whiteLeftRockMoved and \
                    self.board[7][1] == "--" and self.board[7][2] == "--" and \
                    self.board[7][3] == "--":
                self.board[7][0] = "--"
                self.board[7][2] = "wK"
                self.board[7][3] = "wR"
                self.board[7][4] = "--"
                self.whiteKingMoved = True
                return True

        # check if the black king has moved
        if not self.blackKingMoved:
            # check black right castling
            if move.startRow == 0 and move.startCol == 4 and move.endRow == 0 and \
                    move.endCol == 6 and not self.blackRightRockMoved and \
                    self.board[0][5] == "--" and self.board[0][6] == "--":
                self.board[0][4] = "--"
                self.board[0][5] = "bR"
                self.board[0][6] = "bK"
                self.board[0][7] = "--"
                self.blackKingMoved = True
                return True

            # check black left castling
            if move.startRow == 0 and move.startCol == 4 and move.endRow == 0 and \
                    move.endCol == 2 and not self.blackLeftRockMoved and \
                    self.board[0][1] == "--" and self.board[0][2] == "--" and \
                    self.board[0][3] == "--":
                self.board[0][0] = "--"
                self.board[0][2] = "bK"
                self.board[0][3] = "bR"
                self.board[0][4] = "--"
                self.blackKingMoved = True
                return True

# if king moves, check if the move is legal
    def checkIfKingMovellegal(self, r, c, moves, opponent_color):
        # Check if there is a pawn that threat that square
        if opponent_color == "w":
            if r+1 < len(self.board) and c+1 < len(self.board) and \
                    self.board[r+1][c+1] == "wP":
                return True
            elif r+1 < len(self.board) and c-1 >= 0 and self.board[r+1][c-1] == "wP":
                return True

        else:
            if r-1 > 0 and c+1 < len(self.board) and \
                    self.board[r - 1][c + 1] == "bP":
                return True
            elif r-1 > 0 and c-1 >= 0 and self.board[r - 1][c - 1] == "bP":
                return True

        # Check if there is an opponent move that hits the king's square
        for checkMove in moves:
            if checkMove.endRow == r and \
                    checkMove.endCol == c and \
                    self.board[checkMove.startRow][checkMove.startCol][0] == opponent_color and \
                    self.board[checkMove.startRow][checkMove.startRow][1] != "P":
                return True
        return False

    def getKingMoves(self, r, c, moves):
        # check the opponent color
        if self.whiteToMove:
            opponent_color = "b"
        else:
            opponent_color = "w"

        # option 1
        if r - 1 >= 0 and c - 1 >= 0 and \
                (self.board[r - 1][c - 1] == "--" or
                 self.board[r - 1][c - 1][0] == opponent_color):
            moves.append(Move((r, c), (r - 1, c - 1)))

        # option 2
        if r - 1 >= 0 and \
                (self.board[r - 1][c] == "--" or
                 self.board[r - 1][c][0] == opponent_color):
            moves.append(Move((r, c), (r - 1, c)))

        # option 3
        if r - 1 >= 0 and c + 1 < len(self.board) and \
                (self.board[r - 1][c + 1] == "--" or
                 self.board[r - 1][c + 1][0] == opponent_color):
            moves.append(Move((r, c), (r - 1, c + 1)))

        # option 4
        if r + 1 < len(self.board) and c - 1 >= 0 and \
                (self.board[r + 1][c - 1] == "--" or
                 self.board[r + 1][c - 1][0] == opponent_color):
            moves.append(Move((r, c), (r + 1, c - 1)))

        # option 5
        if r + 1 < len(self.board) and \
                (self.board[r + 1][c] == "--" or
                 self.board[r + 1][c][0] == opponent_color):
            moves.append(Move((r, c), (r + 1, c)))

        # option 6
        if r + 1 < len(self.board) - 1 and c + 1 < len(self.board) - 1 and \
                (self.board[r + 1][c + 1] == "--" or
                 self.board[r + 1][c + 1][0] == opponent_color):
            moves.append(Move((r, c), (r + 1, c + 1)))

        # option 7
        if c - 1 >= 0 and \
                (self.board[r][c - 1] == "--" or
                 self.board[r][c - 1][0] == opponent_color):
            moves.append(Move((r, c), (r, c - 1)))

        # option 8
        if c + 1 < len(self.board) and \
                (self.board[r][c + 1] == "--" or
                 self.board[r][c + 1][0] == opponent_color):
            moves.append(Move((r, c), (r, c + 1)))

    def getKnightMoves(self, r, c, moves):
        # check the opponent color
        if self.whiteToMove:
            opponent_color = "b"
        else:
            opponent_color = "w"

        # option 1
        if r - 1 >= 0 and c - 2 >= 0 and \
                (self.board[r - 1][c - 2] == "--" or
                 self.board[r - 1][c - 2][0] == opponent_color):
            moves.append(Move((r, c), (r - 1, c - 2)))

        # option 2
        if r - 1 >= 0 and c + 2 < len(self.board) and \
                (self.board[r - 1][c + 2] == "--" or
                 self.board[r - 1][c + 2][0] == opponent_color):
            moves.append(Move((r, c), (r - 1, c + 2)))

        # option 3
        if r - 2 >= 0 and c - 1 >= 0 and \
                (self.board[r - 2][c - 1] == "--" or
                 self.board[r - 2][c - 1][0] == opponent_color):
            moves.append(Move((r, c), (r - 2, c - 1)))

        # option 4
        if r - 2 >= 0 and c + 1 < len(self.board) and \
                (self.board[r - 2][c + 1] == "--" or
                 self.board[r - 2][c + 1][0] == opponent_color):
            moves.append(Move((r, c), (r - 2, c + 1)))

        # option 5
        if r + 1 < len(self.board) and c - 2 >= 0 and \
                (self.board[r + 1][c - 2] == "--" or
                 self.board[r + 1][c - 2][0] == opponent_color):
            moves.append(Move((r, c), (r + 1, c - 2)))

        # option 6
        if r + 1 < len(self.board) and c + 2 < len(self.board) and \
                (self.board[r + 1][c + 2] == "--" or
                 self.board[r + 1][c + 2][0] == opponent_color):
            moves.append(Move((r, c), (r + 1, c + 2)))

        # option 7
        if r + 2 < len(self.board) and c - 1 >= 0 and \
                (self.board[r + 2][c - 1] == "--" or
                 self.board[r + 2][c - 1][0] == opponent_color):
            moves.append(Move((r, c), (r + 2, c - 1)))

        # option 8
        if r + 2 < len(self.board) and c + 1 < len(self.board) and \
                (self.board[r + 2][c + 1] == "--" or
                 self.board[r + 2][c + 1][0] == opponent_color):
            moves.append(Move((r, c), (r + 2, c + 1)))

    def getBishopMoves(self, r, c, moves):
        # check the opponent color
        if self.whiteToMove:
            opponent_color = "b"
        else:
            opponent_color = "w"

        # check forward left diagonal moves
        row, col = r, c
        while row > 0 and col > 0:
            if self.board[row - 1][col - 1] == "--":
                moves.append(Move((r, c), (row - 1, col - 1)))
                row, col = row - 1, col - 1
            elif self.board[row - 1][col - 1][0] == opponent_color:
                moves.append(Move((r, c), (row - 1, col - 1)))
                break
            else:
                break

        # check backward left diagonal moves
        row, col = r, c
        while row < len(self.board) - 1 and col > 0:
            if self.board[row + 1][col - 1] == "--":
                moves.append(Move((r, c), (row + 1, col - 1)))
                row, col = row + 1, col - 1
            elif self.board[row + 1][col - 1][0] == opponent_color:
                moves.append(Move((r, c), (row + 1, col - 1)))
                break
            else:
                break

        # check forward right diagonal moves
        row, col = r, c
        while row > 0 and col < len(self.board) - 1:
            if self.board[row - 1][col + 1] == "--":
                moves.append(Move((r, c), (row - 1, col + 1)))
                row, col = row - 1, col + 1
            elif self.board[row - 1][col + 1][0] == opponent_color:
                moves.append(Move((r, c), (row - 1, col + 1)))
                break
            else:
                break

        # check backward right diagonal moves
        row, col = r, c
        while row < len(self.board) - 1 and col < len(self.board) - 1:
            if self.board[row + 1][col + 1] == "--":
                moves.append(Move((r, c), (row + 1, col + 1)))
                row, col = row + 1, col + 1
            elif self.board[row + 1][col + 1][0] == opponent_color:
                moves.append(Move((r, c), (row + 1, col + 1)))
                break
            else:
                break

    def getRockMoves(self, r, c, moves):
        # check the opponent color
        if self.whiteToMove:
            opponent_color = "b"
        else:
            opponent_color = "w"

        # check forward moves
        row = r
        while row > 0:
            if self.board[row - 1][c] == "--":
                moves.append(Move((r, c), (row - 1, c)))
                row -= 1
            elif self.board[row - 1][c][0] == opponent_color:
                moves.append(Move((r, c), (row - 1, c)))
                break
            else:
                break

        # check backward moves
        row = r
        while row < len(self.board) - 1:
            if self.board[row + 1][c] == "--":
                moves.append(Move((r, c), (row + 1, c)))
                row += 1
            elif self.board[row + 1][c][0] == opponent_color:
                moves.append(Move((r, c), (row + 1, c)))
                break
            else:
                break

        # check left moves
        col = c
        while col > 0:
            if self.board[r][col - 1] == "--":
                moves.append(Move((r, c), (r, col - 1)))
                col -= 1
            elif self.board[r][col - 1][0] == opponent_color:
                moves.append(Move((r, c), (r, col - 1)))
                break
            else:
                break

        # check right moves
        col = c
        while col < len(self.board) - 1:
            if self.board[r][col + 1] == "--":
                moves.append(Move((r, c), (r, col + 1)))
                col += 1
            elif self.board[r][col + 1][0] == opponent_color:
                moves.append(Move((r, c), (r, col + 1)))
                break
            else:
                break

    def getPawnMoves(self, r, c, moves):
        # white to move
        if self.whiteToMove:
            if r - 1 >= 0 and self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c)))
            if r == 6 and self.board[r - 2][c] == "--":
                moves.append(Move((r, c), (r - 2, c)))
            if r - 1 >= 0 and c - 1 >= 0 and self.board[r - 1][c - 1][0] == "b":
                moves.append(Move((r, c), (r - 1, c - 1)))
            if r - 1 >= 0 and c + 1 <= 7 and self.board[r - 1][c + 1][0] == "b":
                moves.append(Move((r, c), (r - 1, c + 1)))

        else:
            if r + 1 <= 7 and self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c)))
            if r == 1 and self.board[r + 2][c] == "--":
                moves.append(Move((r, c), (r + 2, c)))
            if r + 1 <= 7 and c - 1 >= 0 and self.board[r + 1][c - 1][0] == "w":
                moves.append(Move((r, c), (r + 1, c - 1)))
            if r + 1 <= 7 and c + 1 <= 7 and self.board[r + 1][c + 1][0] == "w":
                moves.append(Move((r, c), (r + 1, c + 1)))

    def promotion(self):
        for i in range(len(self.board)):
            if self.board[0][i] == "wP":
                new_piece = input("""
                Choose your new piece: 
                 1 - for Queen  
                 2 - for Rock 
                 3 - for Bishop 
                 4 - for knight 
                 """)

                if new_piece == "1":
                    self.board[0][i] = "wQ"
                elif new_piece == "2":
                    self.board[0][i] = "wR"
                elif new_piece == "3":
                    self.board[0][i] = "wB"
                elif new_piece == "4":
                    self.board[0][i] = "wN"
                return

            elif self.board[7][i] == "bP":
                new_piece = input("""
                Choose your new piece: 
                1 - for Queen  
                2 - for Rock  
                3 - for Bishop 
                4 - for knight 
                """)
                if new_piece == "1":
                    self.board[7][i] = "bQ"
                elif new_piece == "2":
                    self.board[7][i] = "bR"
                elif new_piece == "3":
                    self.board[7][i] = "bB"
                elif new_piece == "4":
                    self.board[7][i] = "bN"
                return

