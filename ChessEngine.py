import pygame

from Move import *
from helper import *
from buttons import *

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

        self.dimension = 8  # 8X8 board
        self.height = 512
        self.SQ = self.height // self.dimension
        self.whiteToMove = True
        self.moveLog = []
        self.realRows = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
        self.realCols = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        self.index = -1
        self.whiteKingMoved, self.blackKingMoved = False, False
        self.whiteRightRockMoved, self.whiteLeftRockMoved = False, False
        self.blackRightRockMoved, self.blackLeftRockMoved = False, False
        self.countTurns = 0
        self.countPieces = 32
        self.turnsNoEatNoMovePawn = 0
        self.status = 1

    def notCheckMate(self):
        self.status = 1

    def makeMove(self, move):
        # check the color of the current player

        if self.checkPossibleColor(move):
            # check if there is a check

            possible_moves = self.getPossibleMoves()
            opposite_moves = self.getOppositePossibleMoves()
            print(len(possible_moves))
            if len(possible_moves) == 1:
                print(str(possible_moves[0].startRow) + str(possible_moves[0].startCol))
                print(str(possible_moves[0].endRow) + str(possible_moves[0].endRow))

            # check if the specific move is legal
            specialMove, kingRockMoved = False, False
            if self.isMoveLegal(move, possible_moves):
                if self.board[move.startRow][move.startCol] == "bK" and not self.blackKingMoved:
                    self.blackKingMoved, kingRockMoved = True, True
                elif self.board[move.startRow][move.startCol] == "wK" and not self.whiteKingMoved:
                    self.whiteKingMoved, kingRockMoved = True, True
                elif self.moveSpecial(move):
                    specialMove = True
                endPoint = self.board[move.endRow][move.endCol]
                startPoint = self.board[move.startRow][move.startCol]

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
                    kingRockMoved = self.updateRockMoves(move)

            elif self.castling(move):
                endPoint = self.board[move.endRow][move.endCol]

            else:
                return

                # check promotion
            new_piece = self.promotion()

            # if move legal, add the move to the moveLog (saves all the moves that had been done)

            if self.index == len(self.moveLog) - 1:
                self.moveLog.append([move, endPoint, specialMove, new_piece, kingRockMoved])
            else:
                while self.index != len(self.moveLog) - 1:
                    self.moveLog.pop()
                self.moveLog.append([move, endPoint, specialMove, new_piece, kingRockMoved])

            currentColor = "b"
            if self.whiteToMove:
                self.countTurns += 1
                currentColor = "w"

            self.index += 1
            self.whiteToMove = not self.whiteToMove  # swap players move

            # print move
            print(str(self.countTurns) + currentColor + ". " +
                  self.realCols[move.startCol] + self.realRows[move.startRow] + ":" +
                  self.realCols[move.endCol] + self.realRows[move.endRow])  # print the move

            opposite_moves = self.getOppositePossibleMoves()
            possible_moves = self.getPossibleMoves()
            # self.removeIllegalKingMoves(possible_moves, opposite_moves)

            # check if there is a check-mate

            # check if there is a stalemate

            if self.checkExist(opposite_moves) and self.mateExist(possible_moves):
                self.status = 2
                print("check-mate")

            else:
                print("possible moves" + str(len(possible_moves)))
                self.removeIllegalKingMoves(possible_moves, opposite_moves)
                if len(possible_moves) == 0:
                    self.status = 3

            # check if there is a pat of three-fold repetition
            if len(self.moveLog) > 9 and self.checkThreeFoldRepetition():
                self.status = 3

            if self.insufficientMaterial():
                self.status = 3

            if self.checkFiftyMovesRule():
                self.status = 3

    def moveSpecial(self, move):
        if self.whiteToMove:
            if move.startRow == 3 and self.board[move.startRow][move.startCol] == "wP" and \
                    self.board[move.endRow][move.endCol] == "--":
                if move.startRow - 1 == move.endRow and move.startCol + 1 == move.endCol:
                    self.board[move.startRow][move.startCol + 1] = "--"
                    return True
                elif move.startRow - 1 == move.endRow and move.startCol - 1 == move.endCol:
                    self.board[move.startRow][move.startCol - 1] = "--"
                    return True
        else:
            if move.startRow == 4 and self.board[move.startRow][move.startCol] == "bP" and \
                    self.board[move.endRow][move.endCol] == "--":
                if move.startRow + 1 == move.endRow and move.startCol + 1 == move.endCol:
                    self.board[move.startRow][move.startCol + 1] = "--"
                    return True
                elif move.startRow + 1 == move.endRow and move.startCol - 1 == move.endCol:
                    self.board[move.startRow][move.startCol - 1] = "--"
                    return True

        return False

    def checkFiftyMovesRule(self):
        countEmptySquares = 0
        lastMove = self.moveLog[-1][0]
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == "--":
                    countEmptySquares += 1

        if countEmptySquares != self.countPieces:
            self.countPieces = countEmptySquares
            self.turnsNoEatNoMovePawn = 0

        else:
            if self.board[lastMove.endRow][lastMove.endCol] != "wP" and \
                    self.board[lastMove.endRow][lastMove.endCol] != "bP":
                self.turnsNoEatNoMovePawn += 1
                if self.turnsNoEatNoMovePawn == 100:
                    return True
            else:
                self.turnsNoEatNoMovePawn = 0

        return False

    def insufficientMaterial(self):
        countEmptySqaures, activeSquares = 0, {}
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != "--":
                    activeSquares[self.board[r][c]] = r + c

        if len(activeSquares) == 2:
            return True

        elif len(activeSquares) == 3 and ("bB" in activeSquares or "wB" in activeSquares or
                                          "bN" in activeSquares or "wN" in activeSquares):
            return True

        elif len(activeSquares) == 4 and "bB" in activeSquares and "wB" in activeSquares and \
                activeSquares["bB"] % 2 == activeSquares["wB"] % 2:
            return True

        return False

    def checkThreeFoldRepetition(self):
        print()
        self.whiteToMove = not self.whiteToMove  # swap players move
        move_one, move_two, countReptition = self.moveLog[-1][0], self.moveLog[-2][0], 1
        rowOne, colOne = move_one.endRow, move_one.endCol
        rowTwo, colTwo = move_two.endRow, move_two.endCol

        pieceOne = self.board[move_one.endRow][move_one.endCol]
        pieceTwo = self.board[move_two.endRow][move_two.endCol]

        for repeat in range(1, 3):
            move_one, move_two = self.moveLog[-1 - repeat * 4][0], self.moveLog[-2 - repeat * 4][0]
            if pieceOne == self.board[move_one.endRow][move_one.endCol] and \
                    pieceTwo == self.board[move_two.endRow][move_two.endCol]\
                    and rowOne == move_one.endRow and colOne == move_one.endCol\
                    and rowTwo == move_two.endRow and colTwo == move_two.endCol:
                countReptition += 1

        print(countReptition)
        self.whiteToMove = not self.whiteToMove  # swap players move
        if countReptition == 3:
            return True
        return False

    def mateExist(self, moves):
        print("cp1" + str(len(moves)))
        for i in range(len(moves) - 1, -1, -1):
            bol = True
            startMove = self.board[moves[i].startRow][moves[i].startCol]
            endMove = self.board[moves[i].endRow][moves[i].endCol]
            self.board[moves[i].startRow][moves[i].startCol] = "--"
            self.board[moves[i].endRow][moves[i].endCol] = startMove

            opp_moves = self.getOppositePossibleMoves()
            if not self.checkExist(opp_moves):
                bol = False

            self.board[moves[i].startRow][moves[i].startCol] = startMove
            self.board[moves[i].endRow][moves[i].endCol] = endMove

            if bol:
                moves.remove(moves[i])

        print("len of moves " + str(len(moves)))
        if len(moves) == 2:
            print(str(moves[0].startRow) + str(moves[0].startCol))
            print(str(moves[0].endRow) + str(moves[0].endCol))
            print(str(moves[1].startRow) + str(moves[1].startCol))
            print(str(moves[1].endRow) + str(moves[1].endCol))

        isProtectedPiece = False
        if len(moves) == 1:
            isProtectedPiece = self.isProtected(moves[0])
            print(isProtectedPiece)
            print(str(moves[0].startRow) + str(moves[0].startCol))
            print(str(moves[0].endRow) + str(moves[0].endCol))

        if len(moves) == 0 or isProtectedPiece:
            return True
        return False

    def checkExist(self, opposite_moves):
        if self.whiteToMove:
            for checkMove in opposite_moves:
                if self.board[checkMove.startRow][checkMove.startCol][0] == "b" and \
                        self.board[checkMove.endRow][checkMove.endCol] == "wK":
                    return True
            return False

        else:
            for checkMove in opposite_moves:
                if self.board[checkMove.startRow][checkMove.startCol][0] == "w" and \
                        self.board[checkMove.endRow][checkMove.endCol] == "bK":
                    return True
            return False

    def updateRockMoves(self, move):
        r, c = move.startRow, move.startCol
        updated = False
        if r == 0 and c == 0 and not self.blackLeftRockMoved:
            updated, self.blackLeftRockMoved = True, True
        elif r == 0 and c == 7 and not self.blackRightRockMoved:
            updated, self.blackRightRockMoved = True, True
        elif r == 7 and c == 0 and not self.whiteLeftRockMoved:
            updated, self.whiteLeftRockMoved = True, True
        elif r == 7 and c == 7 and not self.whiteRightRockMoved:
            updated, self.whiteRightRockMoved = True, True

        return updated

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
                self.whiteKingMoved = False

            elif move[0] == Move((7, 4), (7, 2)):
                self.board[7][4], self.board[7][0] = "wK", "wR"
                self.board[7][2], self.board[7][3] = "--", "--"
                self.whiteKingMoved = False

            elif move[0] == Move((0, 4), (0, 6)):
                self.board[0][4], self.board[0][7] = "bK", "bR"
                self.board[0][5], self.board[0][6] = "--", "--"
                self.blackKingMoved = False

            elif move[0] == Move((0, 4), (0, 2)):
                self.board[0][4], self.board[0][0] = "bK", "bR"
                self.board[0][2], self.board[0][3] = "--", "--"
                self.blackKingMoved = False

            # Undo the rest of the cases
            else:
                if move[2]:
                    if self.whiteToMove:
                        c = move[0].startCol - move[0].endCol
                        self.board[move[0].startRow][move[0].startCol - c] = "wP"
                    else:
                        c = move[0].startCol - move[0].endCol
                        self.board[move[0].startRow][move[0].startCol - c] = "bP"

                self.board[move[0].startRow][move[0].startCol] = \
                    self.board[move[0].endRow][move[0].endCol]
                self.board[move[0].endRow][move[0].endCol] = move[1]


                # if the rock moved for the first time
                if move[4]:
                    r, c = move[0].startRow, move[0].startCol
                    if r == 0 and c == 4 and self.board[r][c] == "bK":
                        self.blackKingMoved = False
                    if r == 7 and c == 4 and self.board[r][c] == "wK":
                        self.whiteKingMoved = False
                    if r == 0 and c == 0:
                        self.blackLeftRockMoved = False
                    elif r == 0 and c == 7:
                        self.blackRightRockMoved = False
                    elif r == 7 and c == 0:
                        self.whiteLeftRockMoved = False
                    elif r == 7 and c == 7:
                        self.whiteRightRockMoved = False

                if move[3] != "0" and move[0].endRow == 0:
                    self.board[move[0].startRow][move[0].startCol] = "wP"
                elif move[3] != "0" and move[0].endRow == 7:
                    self.board[move[0].startRow][move[0].startCol] = "bP"

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
                if move[2]:
                    self.board[move[0].startRow][move[0].endCol] = "--"
                elif move[3] != "0":
                    if self.whiteToMove:
                        if move[3] == "1":
                            self.board[move[0].startRow][move[0].startCol] = "wQ"
                        elif move[3] == "2":
                            self.board[move[0].startRow][move[0].startCol] = "wR"
                        elif move[3] == "3":
                            self.board[move[0].startRow][move[0].startCol] = "wB"
                        elif move[3] == "4":
                            self.board[move[0].startRow][move[0].startCol] = "wN"
                    else:
                        if move[3] == "1":
                            self.board[move[0].startRow][move[0].startCol] = "bQ"
                        elif move[3] == "2":
                            self.board[move[0].startRow][move[0].startCol] = "bR"
                        elif move[3] == "3":
                            self.board[move[0].startRow][move[0].startCol] = "bB"
                        elif move[3] == "4":
                            self.board[move[0].startRow][move[0].startCol] = "bN"

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
    def removeIllegalKingMoves(self, moves, opposite_moves):
        illegalIndexesList = []
        for move in moves:
            if self.board[move.startRow][move.startCol][1] == "K" and \
                    self.checkIfKingMovellegal(move.endRow, move.endCol, opposite_moves):
                illegalIndexesList.append(move)

        # print(illegalIndexesList)
        # print("len before" + str(len((moves))))
        for illegalMove in illegalIndexesList:
            moves.remove(illegalMove)
        # print("len after" + str(len(moves)))

    def checkIfKingMovellegal(self, r, c, opposite_moves):
        # Check if there is a pawn that threat that square
        if self.whiteToMove:
            opponent_color = "b"
        else:
            opponent_color = "w"

        if opponent_color == "w":
            if r + 1 < len(self.board) and c + 1 < len(self.board) and \
                    self.board[r + 1][c + 1] == "wP":
                return True
            elif r + 1 < len(self.board) and c - 1 >= 0 and self.board[r + 1][c - 1] == "wP":
                return True

        else:
            if r - 1 > 0 and c + 1 < len(self.board) and \
                    self.board[r - 1][c + 1] == "bP":
                return True
            elif r - 1 > 0 and c - 1 >= 0 and self.board[r - 1][c - 1] == "bP":
                return True

        # Check if there is an opponent move that hits the king's square
        for checkMove in opposite_moves:
            if checkMove.endRow == r and \
                    checkMove.endCol == c and \
                    self.board[checkMove.startRow][checkMove.startCol][0] == opponent_color and \
                    self.board[checkMove.startRow][checkMove.startRow][1] != "P":
                return True
        return False

    def isProtected(self, move):
        protected = False
        pieceChecked = self.board[move.endRow][move.endCol]
        startPiece = self.board[move.startRow][move.startCol]
        self.board[move.endRow][move.endCol] = startPiece
        self.board[move.startRow][move.startCol] = "--"
        oppositeMoves = self.getOppositePossibleMoves()
        if self.checkExist(oppositeMoves):
            protected = True

        self.board[move.startRow][move.startCol] = startPiece
        self.board[move.endRow][move.endCol] = pieceChecked

        print("the piece is protected? " + str(protected))

        return protected

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
        if r + 1 < len(self.board) and c + 1 < len(self.board) and \
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
            if len(self.moveLog) > 1 and r == 3:
                lastMove = self.moveLog[self.index][0]
                if c - 1 >= 0 and self.board[3][c - 1] == "bP" and \
                        lastMove.startRow == 1 and \
                        lastMove.endRow == 3 and lastMove.endCol == c - 1:
                    moves.append(Move((r, c), (r - 1, c - 1)))

                if c + 1 < len(self.board) and \
                        self.board[3][c + 1] == "bP" and lastMove.startRow == 1 and \
                        lastMove.endRow == 3 and lastMove.endCol == c + 1:
                    moves.append(Move((r, c), (r - 1, c + 1)))

            if r - 1 >= 0 and self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c)))
            if r == 6 and self.board[r - 2][c] == "--":
                moves.append(Move((r, c), (r - 2, c)))
            if r - 1 >= 0 and c - 1 >= 0 and self.board[r - 1][c - 1][0] == "b":
                moves.append(Move((r, c), (r - 1, c - 1)))
            if r - 1 >= 0 and c + 1 <= 7 and self.board[r - 1][c + 1][0] == "b":
                moves.append(Move((r, c), (r - 1, c + 1)))

        else:
            if len(self.moveLog) > 1 and r == 4:
                lastMove = self.moveLog[self.index][0]
                if c + 1 < len(self.board) and self.board[4][c - 1] == "wP" and \
                        lastMove.startRow == 6 and \
                        lastMove.endRow == 4 and lastMove.endCol == c - 1:
                    moves.append(Move((r, c), (r + 1, c - 1)))

                if c + 1 < len(self.board) and \
                        self.board[4][c + 1] == "wP" and lastMove.startRow == 6 and \
                        lastMove.endRow == 4 and lastMove.endCol == c + 1:
                    moves.append(Move((r, c), (r + 1, c + 1)))

            if r + 1 <= 7 and self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c)))
            if r == 1 and self.board[r + 2][c] == "--":
                moves.append(Move((r, c), (r + 2, c)))
            if r + 1 <= 7 and c - 1 >= 0 and self.board[r + 1][c - 1][0] == "w":
                moves.append(Move((r, c), (r + 1, c - 1)))
            if r + 1 <= 7 and c + 1 <= 7 and self.board[r + 1][c + 1][0] == "w":
                moves.append(Move((r, c), (r + 1, c + 1)))

    def promotion(self):
        new_piece = "0"
        for i in range(len(self.board)):
            if self.board[0][i] == "wP":
                promotion = pygame.transform.scale(pygame.image.load("Images/promotion/square.png"), (320, 80))
                imageWQ = pygame.transform.scale(pygame.image.load("Images/promotion/wQ.png"), (80,80))
                imageWR = pygame.transform.scale(pygame.image.load("Images/promotion/wR.png"), (80, 80))
                imageWB = pygame.transform.scale(pygame.image.load("Images/promotion/wB.png"), (80, 80))
                imageWN = pygame.transform.scale(pygame.image.load("Images/promotion/wN.png"), (80, 80))
                screen.blit(promotion, (95,50))
                screen.blit(imageWQ, (95,50))
                screen.blit(imageWR, (175, 50))
                screen.blit(imageWB, (255, 50))
                screen.blit(imageWN, (335, 50))

                pygame.display.flip()

                while new_piece == "0":
                    for event in pygame.event.get():
                        # for button in [whiteQueen, whiteRock, whiteBishop, whiteKnight]:
                        #     button.changeColor(event.pos)
                        #     button.update(screen)

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if mouse_in_button(whiteQueen, event.pos):
                                new_piece = "1"

                            if mouse_in_button(whiteRock, event.pos):
                                new_piece = "2"

                            if mouse_in_button(whiteBishop, event.pos):
                                new_piece = "3"

                            if mouse_in_button(whiteKnight, event.pos):
                                new_piece = "4"

                if new_piece == "1":
                    self.board[0][i] = "wQ"
                elif new_piece == "2":
                    self.board[0][i] = "wR"
                elif new_piece == "3":
                    self.board[0][i] = "wB"
                elif new_piece == "4":
                    self.board[0][i] = "wN"

            elif self.board[7][i] == "bP":
                promotion = pygame.transform.scale(pygame.image.load("Images/promotion/square.png"), (320, 80))
                imageBQ = pygame.transform.scale(pygame.image.load("Images/promotion/bQ.png"), (80, 80))
                imageBR = pygame.transform.scale(pygame.image.load("Images/promotion/bR.png"), (80, 80))
                imageBB = pygame.transform.scale(pygame.image.load("Images/promotion/bB.png"), (80, 80))
                imageBN = pygame.transform.scale(pygame.image.load("Images/promotion/bN.png"), (80, 80))
                screen.blit(promotion, (95, 385))
                screen.blit(imageBQ, (95, 385))
                screen.blit(imageBR, (175, 385))
                screen.blit(imageBB, (255, 385))
                screen.blit(imageBN, (335, 385))
                pygame.display.flip()

                while new_piece == "0":
                    for event in pygame.event.get():
                        # for button in [whiteQueen, whiteRock, whiteBishop, whiteKnight]:
                        #     button.changeColor(event.pos)
                        #     button.update(screen)

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if mouse_in_button(blackQueen, event.pos):
                                new_piece = "1"

                            if mouse_in_button(blackRock, event.pos):
                                new_piece = "2"

                            if mouse_in_button(blackBishop, event.pos):
                                new_piece = "3"

                            if mouse_in_button(blackKnight, event.pos):
                                new_piece = "4"

                if new_piece == "1":
                    self.board[7][i] = "bQ"
                elif new_piece == "2":
                    self.board[7][i] = "bR"
                elif new_piece == "3":
                    self.board[7][i] = "bB"
                elif new_piece == "4":
                    self.board[7][i] = "bN"

        return new_piece

    def getStatus(self):
        return self.status