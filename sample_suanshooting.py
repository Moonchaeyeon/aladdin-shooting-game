import pygame
import sys
import random
from time import sleep

BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640
rockImage = ['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png']

#점수 표시
def writeScore(count):
    global gamePad
    font = pygame.font.Font(None, 20)
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

#지나간 아이들 표시
def writePassed(count):
    global gamePad
    font = pygame.font.Font(None, 20)
    text = font.render('놓친 운석 수:' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))

#GAME OVER 등의 문구 표시
def writeMessage(text):
    global gamePad
    textfont = pygame.font.Font(None, 60)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text,textpos)
    pygame.display.update()
    sleep(2) #2초 쉬고
    runGame() #게임 다시 시작

def crash():
    global

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))


def initGame():
    global gamePad, clock, background, fighter
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('background.png')
    fighter = pygame.image.load('fighter.png')
    explosion = pygame.image.load('explosion.png')
    clock = pygame.time.Clock()

'''게임 실행'''
def runGame():
    global gapdPad, clock, background, fighter, missile

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key = pygame.K_LEFT:
                    fighterX -= 5
                elif event.key = pygame.K_RIGHT:
                    fighterX += 5
                elif event.key = pygame.K_SPACE:
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX,missileY])
            if event.type in[pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        fighterX = 0

        drawObject(background, 0, 0)

        #fighter 그리기
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        drawObject(fighter, x, y)

        #missile 그리기
        if len(missileXY) != 0:
                for i, bxy in enumerate(missileXY):
                    bxy[1] -= 10 #미사일 발사, 이동 시키기
                    missileXY[i][1] = bxy[1] #미사일 값 바꾸는 과정

                    #미사일이 운석을 맞췄을 경우
                    if bxy[1] < rockY:
                        if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                            missileXY.remove(bxy)
                            isShot = True
                            shotCount += 1

                    #화면 밖으로 나가는 미사일 제거
                    if bxy[1] <= 0:
                        try:
                            missileXY.remove(bxy)
                        except:
                            pass
                    if len(missileXY) != 0:
                        for bx, by in missileXY:
                            drawObject(missile, bx, by)

        #맞춘 운석 수 표시
        writeScore(shotCount)

        rockY += rockSpeed #암석 이동시키기

        #암석 그리기
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1 #지나간 운석의 개수

        #지나친 운석 수 표시
        writePassed(rockpassed)

        #explosion 운석과 미사일이 충돌했을 때 그림
        if isShot:
            #운석 폭발
            drawObject(explosion, rockX, rockY)

            #새로운 운석(랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False

            #운석을 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()
runGame()
