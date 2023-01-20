import pygame
import os
import sys
import Button
import Logo
import Board


def load_image(name, size=(1, 1), to_scale=False, colorkey=None):
    fullname = os.path.join('Data', name)
    if not os.path.isfile(fullname):
        print('can not get file', fullname)
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if to_scale:
        image = pygame.transform.scale(image, size)
    return image


def drawBoard():
    topLeft = (0, 0)
    for row in range(9):
        for col in range(9):
            block = board.getBlock((row, col))
            image = images[getImage(block)]
            screen.blit(image, topLeft)
            topLeft = topLeft[0] + pieceSize[0], topLeft[1]
        topLeft = 0, topLeft[1] + pieceSize[1]

def loadBlocks():
    global images
    imagesDirectory = "Data"
    for fileName in os.listdir(imagesDirectory):
        if not fileName.endswith(".png"):
            continue
        path = imagesDirectory + r"/" + fileName
        img = pygame.image.load(path)
        img = img.convert()
        img = pygame.transform.scale(img, (int(pieceSize[0]), int(pieceSize[1])))
        images[fileName.split(".")[0]] = img


def getImage(block):
    if block.getClicked():
        return 'bomb-at-clicked-block' if block.hasBomb else str(block.getNumAround())
    else:
        return 'flag' if block.getFlagged() else 'empty_block'


def handleClick(position, rightClick):
    if board.getLost():
        return
    index = position[1] // pieceSize[1], position[0] // pieceSize[0]
    block = board.getBlock(index)
    board.handleClick(block, rightClick)


pygame.init()
pygame.display.set_caption('Сапёр')
clock = pygame.time.Clock()
size = width, height = 400, 600
screen = pygame.display.set_mode(size)
tr_x, tr_y = 0, -600
logo = Logo.LogoSprite(load_image('Logo.png'), 90, 15)
play_button = Button.Button(85, 220, load_image('PlayButton.png'),
                            load_image('PlayButtonPressed.png'))
exit_button = Button.Button(85, 300, load_image('ExitButton.png'),
                            load_image('ExitButtonPressed.png'))
images = {}
board = Board.Board((9, 9), 0.25)
pieceSize = (800 // board.getSize()[1]), (800 // board.getSize()[0])
loadBlocks()
menu_count = 0
running_menu = True
running_transition = False
running_game = False
difficult = ''


while running_menu:
    menu_count += 1
    screen.blit(load_image('MenuBackground.png'), [0, 0])
    logo.draw(screen, menu_count)
    play_button.draw(screen)
    exit_button.draw(screen)
    play_button.changeColor(screen)
    exit_button.changeColor(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or exit_button.draw(screen):
            running_menu = False
        if play_button.draw(screen):
            running_transition = True
            while running_transition:
                screen.blit(load_image('transition.png'), [tr_x, tr_y])
                tr_y += 15
                pygame.display.flip()
                if tr_y >= 0:
                    running_transition = False
            running_menu = False
            running_game = True
    pygame.display.flip()
size = 800, 800
pygame.display.set_mode(size)
while running_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            rightClick = pygame.mouse.get_pressed()[2]
            handleClick(position, rightClick)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        drawBoard()

    if board.getWon() or board.getLost():
        running_game = False
    pygame.display.flip()
pygame.quit()
