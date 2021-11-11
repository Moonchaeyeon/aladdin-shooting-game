import pygame
import sys
import random
from time import sleep

padWidth = 600
padHeight = 700

pygame.init()

clock = pygame.time.Clock()
gamePad = pygame.display.set_mode((padWidth, padHeight))
pygame.display.set_caption('Aladdin Shooting Game')

#소리 설정
pygame.mixer.music.load('Carpet Chase(from Aladdin).wav')
pygame.mixer.music.play(-1)
gunSound = pygame.mixer.Sound('beepshot.wav')
bombSound = pygame.mixer.Sound('beeps.wav')
gameoverSound = pygame.mixer.Sound('gameover.wav')

class Drawable:
    speed = 0

    def __init__(self, image, bang, x, y):
        self.image = pygame.image.load(image)
        if bang != None:
            self.bang = pygame.image.load(bang)
        else:
            self.bang = None
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.x = x
        self.y = y

    def draw(self, image):
        global gamePad
        gamePad.blit(image, (self.x, self.y))

class Aladdin(Drawable):
    speed = 0
    score = 0

    def __init__(self):
        super().__init__('aladdin.png', 'bang_aladdin.png',
            (padWidth)/2, padHeight - 120)

class Parrot(Drawable):
    speed = 1
    isShot = False
    image_list = [['parrot_red.png','bang_red.png'],
                ['parrot_blue.png','bang_blue.png'],
                ['parrot_yellow.png','bang_yellow.png'],
                ['parrot_green.png','bang_green.png'],
                ['parrot_pink.png','bang_pink.png']]

    def __init__(self):
        super().__init__(self.image_list[0][0], self.image_list[0][1],
                        random.randint(0, padWidth-50), 0)
        random.shuffle(self.image_list)

class CrazyParrot(Parrot):
    isPass = 0
    image_list = [['parrot01.png', None],
                ['parrot02.png', None],
                ['parrot03.png', None]]

class Weapon(Drawable):
    speed = 8
    xy = [] #총알의 좌표가 담길 리스트
    def __init__(self):
        super().__init__('geniebullet.png',None, None, None)

#점수 표시
def wScore(count):
    global gamePad
    font = pygame.font.Font('a찐빵B.ttf', 15)
    text = font.render('SCORE : ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (420, 40))

#지나간 앵무새 표시
def wPassed(count):
    global gamePad
    font = pygame.font.Font('a찐빵B.ttf', 15)
    text = font.render('PASSED CRAZY PARROT : ' + str(count), True, (219, 0, 0))
    gamePad.blit(text, (420, 10))

#게임 시작 전
def OpeningGame():
    global gamePad, game_over
    OG = Drawable('intro.png',None, 0, 0)
    OG.draw(OG.image)
    pygame.display.update()
    sleep(3)
    OG2 = Drawable('aladdinIntro.png', None, 0, 0)
    OG2.draw(OG2.image)
    pygame.display.update()
    sleep(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #창 닫으면 종료
            pygame.quit()
            sys.exit()

#게임 오버 함수
def gameOver():
    global gameoverSound
    GO = Drawable('gameover.png', None, 0, 0)
    GO.x = (padWidth - GO.width)/2
    GO.y = (padHeight - GO.height)/2
    GO.draw(GO.image)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameoverSound.play()
    sleep(3)

def main():
    background = Drawable('062813_1_4.png', None, 0, -120)
    logo = Drawable('aladdin_logo.png', None, 10, 10)
    aladdin = Aladdin()
    parrot = Parrot()
    crazy = CrazyParrot()
    geniebullet = Weapon()

    OpeningGame()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #창 닫으면 종료
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN: #키를 눌렀을 때
                if event.key == pygame.K_RIGHT: #-> 이거면
                    aladdin.speed += 5
                elif event.key == pygame.K_LEFT: #<- 이거면
                    aladdin.speed -= 5
                if event.key == pygame.K_SPACE: #스페이스바이면
                    bulletX = aladdin.x + aladdin.width/2
                    bulletY = padHeight - 100
                    geniebullet.xy.append([bulletX, bulletY])
                    gunSound.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    aladdin.speed = 0

        #배경 그리기
        background.draw(background.image)
        logo.draw(logo.image)

        #알라딘 그리기
        aladdin.x += aladdin.speed

        if aladdin.x < 0: #알라딘 화면 밖으로 나가지 않도록 하기
            aladdin.x = 0
        elif aladdin.x > padWidth - aladdin.width:
            aladdin.x = padWidth - aladdin.width

        aladdin.draw(aladdin.image)

        #앵무새 그리기
        parrot.y += parrot.speed
        parrot.draw(parrot.image)

        if parrot.y > padHeight: #앵무새가 알라딘을 지나쳤을 때
            aladdin.score -= 5 #알라딘 점수 감점
            del(parrot)
            parrot = Parrot()
            parrot.draw(parrot.image)

        if Parrot.isShot : #앵무새가 지니총알과 충돌했다면
            parrot.draw(parrot.bang) #폭발 이미지 그리기
            aladdin.score += 10 #알라딘 점수 증가
            Parrot.isShot = False
            Parrot.speed += 0.5
            del(parrot)
            parrot = Parrot()
            parrot.draw(parrot.image)
            bombSound.play()

        if parrot.y > aladdin.y - parrot.height: #앵무새가 알라딘과 충돌
            if aladdin.x - parrot.width < parrot.x and parrot.x < aladdin.x + aladdin.width:
                aladdin.draw(aladdin.bang)
                bombSound.play()
                gameOver()
                game_over = True

        #미친 앵무새 그리기
        crazy.y += Parrot.speed
        crazy.x += Parrot.speed
        crazy.x %= padWidth - crazy.width
        crazy.draw(crazy.image)

        if crazy.y > padHeight: #미친앵무새가 알라딘을 지나쳤을 때
            CrazyParrot.isPass += 1 #지나간 미친앵무새 수 증가
            aladdin.score += 10 #알라딘 점수 증가
            del(crazy)
            crazy = CrazyParrot()
            crazy.draw(crazy.image)

        if crazy.y > aladdin.y - crazy.height: #앵무새가 알라딘과 충돌
            if aladdin.x - crazy.width < crazy.x < aladdin.x + aladdin.width:
                aladdin.draw(aladdin.bang)
                bombSound.play()
                gameOver()
                game_over = True

        #지니총알 그리기
        if len(geniebullet.xy) != 0: #총알이 발사됐다면
            for i, xy in enumerate(geniebullet.xy):
                xy[1] -= geniebullet.speed
                geniebullet.xy[i][1] = xy[1] #발사시키기

                #지니총알이 앵무새와 충돌했을 경우
                if xy[1] < parrot.y + parrot.height:
                    if parrot.x < xy[0] < parrot.x + parrot.width:
                        Parrot.isShot = True
                        geniebullet.xy.remove(xy)
                        bombSound.play()

                #지니총알이 밖으로 나갔을 경우
                elif xy[1] < 0:
                    geniebullet.xy.remove(xy)

                if len(geniebullet.xy) != 0:
                    geniebullet.x = xy[0]
                    geniebullet.y = xy[1]
                    geniebullet.draw(geniebullet.image)

        wScore(aladdin.score)
        wPassed(CrazyParrot.isPass)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
