import random
import sys

import pygame

pygame.init()

# Variables
board = [" " for x in range(10)]

# Constants
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# rgb: red green blue
RED = (255, 0, 0)
BACKGROUND_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


# Draws the 3 horizontal and vertical lines.
def drawLines():
    for x in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (200 * x, 0), (200 * x, 600), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 200 * x), (600, 200 * x), LINE_WIDTH)


# Inserts a player piece at a given position.
def insertLetter(letter, pos):
    board[pos] = letter


# Returns whether a square is filled.
def spaceIsFree(pos):
    return board[pos] == " "


# Returns a boolean to determine whether the given player is currently a winner.
def isWinner(boardCopy, playerChar, draw=False):
    # Vertical win check
    if boardCopy[1] == playerChar and boardCopy[4] == playerChar and boardCopy[7] == playerChar:
        if draw:
            pygame.draw.line(screen, RED, (0 * SQUARE_SIZE + 100, 25), (0 * SQUARE_SIZE + 100, HEIGHT - 25), LINE_WIDTH)
        return True
    elif boardCopy[2] == playerChar and boardCopy[5] == playerChar and boardCopy[8] == playerChar:
        if draw:
            pygame.draw.line(screen, RED, (1 * SQUARE_SIZE + 100, 25), (1 * SQUARE_SIZE + 100, HEIGHT - 25), LINE_WIDTH)
        return True
    elif boardCopy[3] == playerChar and boardCopy[6] == playerChar and boardCopy[9] == playerChar:
        if draw:
            pygame.draw.line(screen, RED, (2 * SQUARE_SIZE + 100, 25), (2 * SQUARE_SIZE + 100, HEIGHT - 25), LINE_WIDTH)
        return True

    # Horizontal win check
    elif boardCopy[1] == playerChar and boardCopy[2] == playerChar and boardCopy[3] == playerChar:
        if draw:
            pygame.draw.line(screen, RED, (25, 0 * SQUARE_SIZE + 100), (WIDTH - 25, 0 * SQUARE_SIZE + 100), LINE_WIDTH)
        return True
    elif boardCopy[4] == playerChar and boardCopy[5] == playerChar and boardCopy[6] == playerChar:
        if draw:
            pygame.draw.line(screen, RED, (25, 1 * SQUARE_SIZE + 100), (WIDTH - 25, 1 * SQUARE_SIZE + 100), LINE_WIDTH)
        return True
    elif boardCopy[7] == playerChar and boardCopy[8] == playerChar and boardCopy[9] == playerChar:
        if draw:
            pygame.draw.line(screen, RED, (25, 2 * SQUARE_SIZE + 100), (WIDTH - 25, 2 * SQUARE_SIZE + 100),  LINE_WIDTH)
        return True

    # Diagonal descending check
    elif boardCopy[1] == playerChar and boardCopy[5] == playerChar and boardCopy[9] == playerChar:
        if draw:
            pygame.draw.line(screen, RED, (25, 25), (WIDTH - 25, HEIGHT - 25), LINE_WIDTH)
        return True

    # Diagonal ascending check
    elif boardCopy[7] == playerChar and boardCopy[5] == playerChar and boardCopy[3] == playerChar:
        if draw:
            pygame.draw.line(screen, RED, (25, HEIGHT - 25), (WIDTH - 25, 25), LINE_WIDTH)
        return True
    # Otherwise, nobody is winning.
    return False


# Determines the computer's move using artificial intelligence.
def compMove():
    possibleMoves = [x for x, letter in enumerate(board) if letter == " " and x != 0]
    move = 0

    for let in ["O", "X"]:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let):
                move = i
                return move

    if 5 in possibleMoves:
        move = 5
        return move

    freeCorners = []
    for i in possibleMoves:
        if i in [1, 3, 7, 9]:
            freeCorners.append(i)

    if len(freeCorners) > 0:
        move = selectRandom(freeCorners)
        return move

    edgesOpen = []
    for i in possibleMoves:
        if i in [2, 4, 6, 8]:
            edgesOpen.append(i)

    if len(edgesOpen) > 0:
        move = selectRandom(edgesOpen)

    return move


def selectRandom(li):
    ln = len(li)
    r = random.randrange(0, ln)
    return li[r]


def restart():
    screen.fill(BACKGROUND_COLOR)
    drawLines()
    for x in range(10):
        board[x] = " "


def printGUIBoard():
    for x in range(1, 10):
        col = (x - 1) % 3
        row = (x - 1) // 3
        if board[x] == "O":
            pygame.draw.circle(screen, CIRCLE_COLOR,
                               (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                               CIRCLE_RADIUS, CIRCLE_WIDTH)
        elif board[x] == "X":
            pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                             (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                             (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                             CROSS_WIDTH)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe vs. Computer (Press 'R' to reset)")
screen.fill(BACKGROUND_COLOR)

drawLines()

game_over = False
# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clickedElement = int(mouseY // SQUARE_SIZE) * 3 + int(mouseX // SQUARE_SIZE)  # Convert from rows and
            # grids (range: 0 - 2) to list elements (range: 0 - 10)

            if spaceIsFree(clickedElement + 1):
                insertLetter("X", clickedElement + 1)
                printGUIBoard()
                if isWinner(board, "X", True):
                    game_over = True
                    break
                # player = player % 2 + 1

                # Computer's move
                insertLetter("O", compMove())
                if isWinner(board, "O", True):
                    game_over = True

                printGUIBoard()

        # To restart the game, press "r"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False

    pygame.display.update()
