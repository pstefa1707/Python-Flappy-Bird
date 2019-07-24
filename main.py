import pygame
from pygame.locals import *
from lib import Bird, Scroller, Pipe

#Define game globals
FPS = 60
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
BASE_HEIGHT = WINDOW_HEIGHT * 0.79
PIPES = []

#Game State 0: Start Screen, 1: Game Over Screen, 2: In game
GAME_STATE = 0

#SCORE
SCORE = 0

#Pipe globals
PIPE_GAP = 100
PIPE_DISTANCE = 200
PIPE_SPEED = 3
PIPE_HEIGHT = 0 #Automatically calculated
PIPE_WIDTH = 0 #Automatically calculated
UL_MARGIN = 50

#Flappy globals
FALL_VELOCITY = 4
JUMP_VELOCITY = 5.5
JUMP_HEIGHT = 65

#Background and Base scroll speeds
BACKGROUND_SPEED = 1
BASE_SPEED = 3

#Player sprites
PLAYER = (
    'assets/sprites/yellowbird-upflap.png',
    'assets/sprites/yellowbird-midflap.png',
    'assets/sprites/yellowbird-downflap.png'
)
BACKGROUND_SPRITE = 'assets/sprites/background-day.png'
START_GAME = 'assets/sprites/message.png'
START_GAME_POS = (int((WINDOW_WIDTH - 184) / 2), int((WINDOW_HEIGHT - 267) / 2))
BASE_SPRITE = 'assets/sprites/base.png'
PIPE_SPRITE = 'assets/sprites/pipe-green.png'
NUMBER_SPRITES = (
    'assets/sprites/0.png',
    'assets/sprites/1.png',
    'assets/sprites/2.png',
    'assets/sprites/3.png',
    'assets/sprites/4.png',
    'assets/sprites/5.png',
    'assets/sprites/6.png',
    'assets/sprites/7.png',
    'assets/sprites/8.png',
    'assets/sprites/9.png'
)
GAMEOVER_SPRITE = "assets/sprites/gameover.png"
GAMEOVER_POS = (int((WINDOW_WIDTH - 250) / 2), int((WINDOW_HEIGHT - 126) / 2))

def main():
    global GAME_STATE
    #Initialise pygame
    pygame.init()
    #Draw window to screen 500 x 800
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    #Define clock for frame rate management
    CLOCK = pygame.time.Clock()
    #Set window title
    pygame.display.set_caption('Paras\' Flappy Bird Clone')
    #DEFINE SPRITES
    SPRITES = {
        'backGround': pygame.image.load(BACKGROUND_SPRITE).convert_alpha(),
        'startGame': pygame.image.load(START_GAME).convert_alpha(),
        'bird': [pygame.image.load(i).convert_alpha() for i in PLAYER],
        'base': pygame.image.load(BASE_SPRITE).convert_alpha(),
        'pipeUp': pygame.image.load(PIPE_SPRITE).convert_alpha(),
        'pipeDown': pygame.transform.flip(pygame.image.load(PIPE_SPRITE).convert_alpha(), False, True),
        'numbers': [pygame.image.load(i).convert_alpha() for i in NUMBER_SPRITES],
        'gameOver': pygame.image.load(GAMEOVER_SPRITE).convert_alpha()
    }
    #CALCULATE PIPE_HEIGHT
    PIPE_HEIGHT = SPRITES['pipeUp'].get_height()
    PIPE_WIDTH = SPRITES['pipeUp'].get_width()

    BIRD = None
    BASE = Scroller.Scroller(SPRITES['base'], BASE_SPEED, WINDOW_WIDTH)
    BACKGROUND = Scroller.Scroller(SPRITES['backGround'], BACKGROUND_SPEED, WINDOW_WIDTH)

    run = True
    while run:
        for event in pygame.event.get():  # Loop through a list of events
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if GAME_STATE == 0:
                    BIRD = Bird.Bird(WINDOW_WIDTH, WINDOW_HEIGHT, FALL_VELOCITY, JUMP_VELOCITY, JUMP_HEIGHT, BASE_HEIGHT)
                    PIPES.append(Pipe.Pipe(PIPE_SPEED, 
                        PIPE_GAP, 
                        PIPE_DISTANCE,
                        PIPE_WIDTH,
                        PIPE_HEIGHT,
                        WINDOW_HEIGHT, 
                        WINDOW_WIDTH, 
                        BASE_HEIGHT, 
                        UL_MARGIN))
                    GAME_STATE = 2
                elif GAME_STATE == 1:
                    global SCORE
                    SCORE = 0
                    GAME_STATE = 0
                else:
                    BIRD.jump()
            if event.type == pygame.QUIT:  # See if the user clicks the red x 
                run = False    # End the loop
                pygame.quit()  # Quit the game
                quit()

        def renderScore(ySize, gap, pos):
            global SCORE
            number = SCORE
            listNumber = list(str(number))
            letters = len(listNumber)
            for i in listNumber:
                listNumber[listNumber.index(i)] = int(i)
            xSize = int(ySize * (2/3))
            leftSide = pos[0] - (letters*(xSize + gap)/2)
            offset = xSize + 5
            for i in range(letters):
                SCREEN.blit(pygame.transform.scale(SPRITES['numbers'][listNumber[i]], (xSize, ySize)), (leftSide + (i*offset), pos[1]))

        def checkCollisions():
            global SCORE
            if BIRD.uLCollision():
                endGame()
            for i in PIPES:
                col = i.collisionChecks(BIRD.getPos(), SPRITES['bird'][1].get_size())
                if col == "collision":
                    endGame()
                elif col == "awardPoint":
                    SCORE += 1


        def renderBackground():
            newBackGroundPos = BACKGROUND.updatePositions()
            SCREEN.blit(SPRITES["backGround"], (newBackGroundPos[0], 0))
            SCREEN.blit(SPRITES["backGround"], (newBackGroundPos[1], 0))

        def renderBase():
            newBasePos = BASE.updatePositions()
            SCREEN.blit(SPRITES["base"], (newBasePos[0], BASE_HEIGHT))
            SCREEN.blit(SPRITES["base"], (newBasePos[1], BASE_HEIGHT))

        def drawGameOver():
            renderBackground()
            renderBase()
            SCREEN.blit(SPRITES["gameOver"], GAMEOVER_POS)
            renderScore(22, 5, (GAMEOVER_POS[0] + 205, GAMEOVER_POS[1] + 36))

        def drawStartScreen():
            renderBackground()
            renderBase()
            SCREEN.blit(SPRITES['startGame'], START_GAME_POS)

        def endGame():
            global GAME_STATE, PIPES, BIRD, SCORE
            PIPES = []
            BIRD = None
            GAME_STATE = 1

        def renderGame():
            #Render Background
            renderBackground()
            
            #Check Collisions
            checkCollisions()

            #Draw bird and update animation
            SCREEN.blit(SPRITES['bird'][BIRD.getAniIter()], BIRD.getPos())
            BIRD.updatePos()
            BIRD.incrementAniIter()
            BIRD.incrementCounter()

            #Loop through Pipes and draw
            for pipe in PIPES:
                if pipe.updatePos():
                    SCREEN.blit(SPRITES['pipeUp'], pipe.getLowerPos())
                    SCREEN.blit(SPRITES['pipeDown'], pipe.getUpperPos())
                else:
                    PIPES.append(Pipe.Pipe(PIPE_SPEED, 
                        PIPE_GAP, 
                        PIPE_DISTANCE,
                        PIPE_WIDTH,
                        PIPE_HEIGHT,
                        WINDOW_HEIGHT, 
                        WINDOW_WIDTH, 
                        BASE_HEIGHT, 
                        UL_MARGIN))
            renderScore(40, 10, (WINDOW_WIDTH/2, 10))
            
            renderBase()

        if GAME_STATE == 0:
            drawStartScreen()
        elif GAME_STATE == 1:
            drawGameOver()
        else:
            renderGame()

        pygame.display.flip()

        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()