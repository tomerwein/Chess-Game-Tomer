import pygame
from constants import *
import ChessEngine
from MenuButton import *
from helper import screen

def loadImages():
    #Pawns
    IMAGES['wP'] = pygame.transform.scale(pygame.image.load("Images/game/wp.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['bP'] = pygame.transform.scale(pygame.image.load("Images/game/bp.png"), (SQ_SIZE, SQ_SIZE))

    #Rocks
    IMAGES['bR'] = pygame.transform.scale(pygame.image.load("Images/game/bR.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['wR'] = pygame.transform.scale(pygame.image.load("Images/game/wR.png"), (SQ_SIZE, SQ_SIZE))

    #Bishops
    IMAGES['bB'] = pygame.transform.scale(pygame.image.load("Images/game/bB.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['wB'] = pygame.transform.scale(pygame.image.load("Images/game/wB.png"), (SQ_SIZE, SQ_SIZE))

    #Knights
    IMAGES['bN'] = pygame.transform.scale(pygame.image.load("Images/game/bN.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['wN'] = pygame.transform.scale(pygame.image.load("Images/game/wN.png"), (SQ_SIZE, SQ_SIZE))

    #Queens
    IMAGES['bQ'] = pygame.transform.scale(pygame.image.load("Images/game/bQ.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['wQ'] = pygame.transform.scale(pygame.image.load("Images/game/wQ.png"), (SQ_SIZE, SQ_SIZE))

    #Kings
    IMAGES['bK'] = pygame.transform.scale(pygame.image.load("Images/game/bK.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['wK'] = pygame.transform.scale(pygame.image.load("Images/game/wK.png"), (SQ_SIZE, SQ_SIZE))

# def get_font(size): # Returns Press-Start-2P in the desired size
#     return pygame.font.Font(pygame.font.SysFont('chalkduster.ttf', 15), size)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Images/menu/font.ttf", size)

def main_menu():
    BG = pygame.image.load("Images/menu/Background.jpg")
    BG = pygame.transform.scale(BG, (550, 550))
    rect = pygame.image.load("Images/menu/rect.png")
    running = True
    while running:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(image_white, (0,140))
        screen.blit(image_black, (390, 140))
        MENU_TEXT = get_font(40).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(260, 100))

        PLAY_BUTTON = MenuButton(image=rect, pos=(260, 200),
                                 text_input="PLAY", font=get_font(30), base_color="slate blue", hovering_color="Purple")
        OPTIONS_BUTTON = MenuButton(image=rect, pos=(260, 300),
                                    text_input="OPTIONS", font=get_font(30), base_color="slate blue", hovering_color="Purple")
        QUIT_BUTTON = MenuButton(image=rect, pos=(260, 400),
                                 text_input="QUIT", font=get_font(30), base_color="slate blue", hovering_color="Purple")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game()
                # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False

        pygame.display.update()

def game():
    squareSelected = () # No square is selected so far (row and a col)
    playerClicks = [] # Move from sqaure 'a' to square 'b'
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    running = True
    gameOn = True
    mateFirstTime = False
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if gameOn:
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
                        if mateFirstTime:
                            mateFirstTime = False
                        gs.undoMove()
                    if e.key == pygame.K_RIGHT:
                        gs.redoMove()

                if gameOn and gs.getStatus() == 2:
                    gameOn = False

                elif gameOn and gs.getStatus() == 3:
                    gameOn = False

                drawGameState(screen, gs.board)

            elif gs.getStatus() == 2:
                drawGameState(screen, gs.board)
                screen.blit(checkMate, (10,120))
            else:
                drawGameState(screen, gs.board)
                screen.blit(stalemate, (10, 120))

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    screen.fill("black")
                    drawGameState(screen, gs.board)
                    gs.notCheckMate()
                    gameOn = True

                if e.key == pygame.K_q:
                    running = False

                if e.key == pygame.K_r:
                    screen.fill("white")
                    game()
                    running = False

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


DIMENSION = 8  #8X8 board
HEIGHT = 512
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
IMAGES = {}
pygame.init()



loadImages()  # load the Images only once
main_menu()


