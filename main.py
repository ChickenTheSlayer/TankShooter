import random
import pygame
import time

COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)


class MainGame():
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600
    window = None
    Tank_1 = None
    ETank_List = []
    ETank_num = 5
    ETank_count = 5

    Bullet_list = []

    def __init__(self):
        pass

    def Startgame(self):
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        MainGame.Tank_1 = Tanks(250, 500)
        pygame.display.set_caption("Tanks")
        self.createETank()
        self.text_font('test')

        while True:

            MainGame.window.fill(COLOR_WHITE)
            self.get_events()

            MainGame.window.blit(self.text_font("Eliminations %d" % len(MainGame.ETank_List)), (10, 10))
            MainGame.Tank_1.display()
            self.blitETank()
            if MainGame.Tank_1 and not MainGame.Tank_1.press:
                MainGame.Tank_1.move()

            self.blitBullet()

            time.sleep(0.005)
            pygame.display.update()

    def createETank(self):
        top = 100
        speed = random.randint(1, 4)
        for i in range(MainGame.ETank_num):
            left = random.randint(1, 5)
            ETank = Enemytank(left*100, top, speed)
            MainGame.ETank_List.append(ETank)

    def blitETank(self):
        for ETank in MainGame.ETank_List:
            ETank.display()
            ETank.randMove()

    def blitBullet(self):
        for Bullet in MainGame.Bullet_list:
            Bullet.Display()
            Bullet.bullmove()


    def get_events(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                self.Endgame()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    MainGame.Tank_1.direction = 'L'
                    MainGame.Tank_1.press = False
                    MainGame.Tank_1.move()
                elif event.key == pygame.K_RIGHT:
                    MainGame.Tank_1.direction = 'R'
                    MainGame.Tank_1.press = False

                    MainGame.Tank_1.move()
                elif event.key == pygame.K_UP:
                    MainGame.Tank_1.direction = 'U'
                    MainGame.Tank_1.press = False

                    MainGame.Tank_1.move()
                elif event.key == pygame.K_DOWN:
                    MainGame.Tank_1.direction = 'D'
                    MainGame.Tank_1.press = False

                    MainGame.Tank_1.move()
                elif event.key == pygame.K_SPACE:
                    print("Shoot")
                    m = Bullet(MainGame.Tank_1)

                    MainGame.Bullet_list.append(m)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    MainGame.Tank_1.press = True

    def text_font(self, text):
        pygame.font.init()
        font_list = pygame.font.get_fonts()
        font = pygame.font.SysFont('arial', 17)
        textfont = font.render(text, 1, COLOR_BLACK)
        return textfont

    def Endgame(self):
        print("Ended")
        pygame.quit()
        exit()
class Tanks():
    def __init__(self,left,top):
        self.images = {
            'U': pygame.image.load('Images/Tank p1 U.png'),
            'D': pygame.image.load('Images/Tank p1 D.png'),
            'R': pygame.image.load('Images/Tank p1 R.png'),
            'L': pygame.image.load('Images/Tank p1 L.png'),

        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 1
        self.press = True

    def move(self):

        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed

    def shoot(self):
        pass

    def display(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


class Mytank(Tanks):
    def __init__(self):
        pass

    def move(self):
        pass

    def shoot(self):
        pass


class Enemytank(Tanks):

    def __init__(self, left, top, speed):

        self.images = {
            'U': pygame.image.load('Images/ETank U.png'),
            'D': pygame.image.load('Images/ETank D.png'),
            'R': pygame.image.load('Images/ETank R.png'),
            'L': pygame.image.load('Images/ETank L.png'),

        }
        self.direction = self.randDir()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.press = True
        self.step = 20

    def randDir(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'L'
        elif num == 3:
            return 'R'
        elif num == 4:
            return 'D'

    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDir()
            self.step = 40
        else:
            self.move()
            self.step = self.step-1

    def display(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)

    def move(self):
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed

    def shoot(self):
        return Bullet(self)
class Bullet():
    def __init__(self, Tanks):
        self.image = pygame.image.load("Images/bullet D.png")
        self.direction = Tanks.direction

        self.rect = self.image.get_rect()

        self.speed = 7

        if self.direction == 'U':
            self.rect.left = Tanks.rect.left + Tanks.rect.width/2 - self.rect.width/2
            self.rect.top = Tanks.rect.top - self.rect.height

        elif self.direction == 'L':
            self.rect.left = Tanks.rect.left - self.rect.width
            self.rect.top = Tanks.rect.top + Tanks.rect.height/2 - self.rect.height/2

        elif self.direction == 'R':
            self.rect.left = Tanks.rect.left + Tanks.rect.width
            self.rect.top = Tanks.rect.top + Tanks.rect.height/2 - self.rect.height/2

        elif self.direction == 'D':
            self.rect.left = Tanks.rect.left + Tanks.rect.width/2 - self.rect.width/2
            self.rect.top = Tanks.rect.top + Tanks.rect.height

    def bullmove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed

            else:
                pass

        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                pass

        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                pass
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                pass
    def Display(self):
        MainGame.window.blit(self.image, self.rect)


class Explosion():
    def __init__(self):
        pass

    def DisplayEx(self):
        pass


class Walls():
    def __init__(self):
        pass

    def DisplayWall(self):
        pass


class Music():
    def __init__(self):
        pass

    def PlayMusic(self):
        pass


if __name__ == "__main__":
    MainGame().Startgame()
