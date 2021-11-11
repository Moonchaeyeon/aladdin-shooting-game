import pygame
import sys
import random
from time import sleep

padWidth = 700
padHeight = 800

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad,background, cloud, aladdin, parrot, zapa
    pygame.init()
    pygame.key.set_repeat(5,5)
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    background = pygame.image.load('062813_1_4.png')
    cloud = pygame.image.load('구름1.png')
    aladdin = pygame.image.load('파일_001.png')
    parrot = pygame.image.load('parrot01.png')
#    zapa = pygame.image.load('')

def runGame():
    global gamePad, background, cloud, aladdin, parrot, zapa

    #구름에 관한 정보
    cloudSpeed = 0.5
    cloudX = random.randrange(-5, padWidth-5)
    cloudY = 0

    #알라딘에 관한 정보
    aladdinSize = aladdin.get_rect().size
    aladdinWidth = aladdinSize[0]
    aladdinHeight = aladdinSize[1]

    aladdinSpeed = 0
    x = (padWidth-aladdinWidth)/2
    y = padHeight-aladdinHeight - 50

    #앵무새에 관한 정보
    parrotSize = parrot.get_rect().size
    parrotWidth = parrotSize[0]
    parrotHeight = parrotSize[1]
    parrotX = random.randrange(0, padWidth-parrotWidth)
    parrotY = 0

    onGame = False

    while not onGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    aladdinSpeed += 2 #가속도 설정
                elif event.key == pygame.K_LEFT:
                    aladdinSpeed -= 2
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        aladdinSpeed = 0 #속도 리셋

        #배경 그리기(구름)
        drawObject(background, 0, 0)

        cloudY += cloudSpeed

        drawObject(cloud, cloudX, cloudY)

        #알라딘 그리기
        x += aladdinSpeed

        if x < 0: #화면 밖으로 안나가게 해주기!
            x = 0
        elif x > padWidth - aladdinWidth:
            x = padWidth - aladdinWidth

        drawObject(aladdin, x, y)

        #앵무새 그리기
        drawObject(parrot, padHeight/2, padWidth/2)


        #자파 그리기

        pygame.display.update()
    pygame.quit()

initGame()
runGame()


'''    #직사각형 그리기
    pygame.draw.rect(screen, WHITE, my_rect)
    pygame.draw.rect(screen, RED, my_rrect)
    for x in range(0,1024,4):
        pygame.draw.line(screen, my_color, (x,0),(x,512), 3)
    for y in range(0,512,4):
        pygame.draw.line(screen, my_color, (0,y),(1024,y), 3)

    #글씨 쓰기
    sysfont = pygame.font.SysFont('a디딤돌', 70)
    message = sysfont.render("abc 문채연", True, WHITE)
    message_rect = message.get_rect()
    message_rect.center = (400,100)
    screen.blit(message, message_rect) '''
