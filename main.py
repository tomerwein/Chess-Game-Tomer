import pygame

import ChessEngine
from ChessEngine import *
WIDTH = HEIGHT = 512
DIMENSION = 8  #8X8 bored
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
IMAGES = {}

def loadImages():
    #Pawns
    IMAGES['wP'] = pygame.transform.scale(pygame.image.load("Images/wp.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES['bP'] = pygame.transform.scale(pygame.image.load("Images/bp.png"), (SQ_SIZE,SQ_SIZE))

    #Rocks
    IMAGES['bR'] = pygame.transform.scale(pygame.image.load("Images/bR.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES['wR'] = pygame.transform.scale(pygame.image.load("Images/wR.png"), (SQ_SIZE,SQ_SIZE))

    #Bishops
    IMAGES['bB'] = pygame.transform.scale(pygame.image.load("Images/bB.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES['wB'] = pygame.transform.scale(pygame.image.load("Images/wB.png"), (SQ_SIZE,SQ_SIZE))

    #Knights
    IMAGES['bN'] = pygame.transform.scale(pygame.image.load("Images/bN.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES['wN'] = pygame.transform.scale(pygame.image.load("Images/wN.png"), (SQ_SIZE,SQ_SIZE))

    #Queens
    IMAGES['bQ'] = pygame.transform.scale(pygame.image.load("Images/bQ.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES['wQ'] = pygame.transform.scale(pygame.image.load("Images/wQ.png"), (SQ_SIZE,SQ_SIZE))

    #Kings
    IMAGES['bK'] = pygame.transform.scale(pygame.image.load("Images/bK.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES['wK'] = pygame.transform.scale(pygame.image.load("Images/wK.png"), (SQ_SIZE,SQ_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() # load the Images only once
    squareSelected = () # No square is selected so far (row and a col)
    playerClicks = [] # Move from sqaure 'a' to square 'b'
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # get x,y pos
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if squareSelected != (row, col):
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)

                # if first click is on empty space
                if len(playerClicks) == 1 and gs.board[row][col] == "--":
                    playerClicks.pop()

                # if the player made his chosen move
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1])
                    gs.makeMove(move)
                    squareSelected, playerClicks = (), []

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    gs.undoMove()
                if e.key == pygame.K_RIGHT:
                    gs.redoMove()

        drawGameState(screen, gs.board)
        clock.tick(FPS)
        pygame.display.flip()

# Draw the game state on the boards (Basically the graphics)
def drawGameState(screen, board):
    drawBoard(screen) # draw the board
    drawPieces(screen, board) # draw the pieces on the top of the board

def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("skyblue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if (r+c) % 2 == 0:
                color = colors[0] # it's a white piece of board
            else:
                color = colors[1] # it's a black piece of board
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] in IMAGES:
                screen.blit(IMAGES[board[r][c]], pygame.Rect(c*SQ_SIZE-2, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    main()