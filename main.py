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
    EBullet_list = []
    Explode_list = []
    Wall_list = []
    
    def createMytank(self):
        MainGame.Tank_1 = Mytank(250, 500)
    def Startgame(self):
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        self.createMytank()
        pygame.display.set_caption("Tanks")
        self.createETank()
        self.createWalls()
        self.text_font('test')

        while True:

            MainGame.window.fill(COLOR_WHITE)
            self.get_events()

            MainGame.window.blit(self.text_font("Eliminations %d" % len(MainGame.ETank_List)), (10, 10))

            self.blitWalls()
            if MainGame.Tank_1 and MainGame.Tank_1.live:
                MainGame.Tank_1.display()
            else:
                del MainGame.Tank_1
                MainGame.Tank_1 = None

            self.blitETank()

            if MainGame.Tank_1 and not MainGame.Tank_1.press:
                MainGame.Tank_1.move()
                MainGame.Tank_1.hitWalls()
                MainGame.Tank_1.hitEnemyTank()

            self.blitBullet()

            self.EblitBullet()
            self.displayExplode()
            time.sleep(0.005)
            pygame.display.update()
    def createETank(self):
        top = 100
        for i in range(MainGame.ETank_num):
            speed = random.randint(2, 4)
            left = random.randint(1, 2)
            ETank = Enemytank(left*100, top, speed)
            MainGame.ETank_List.append(ETank)

    def createWalls(self):
        # create top wall
        for i in range(1, 10):
            wall = Walls(50 * i, 50)
            MainGame.Wall_list.append(wall)

        # create bottom wall
        for i in range(1, 10):
            wall = Walls(50 * i, 550)
            MainGame.Wall_list.append(wall)

        # create left wall
        for i in range(2, 10):
            wall = Walls(50, 50 * i)
            MainGame.Wall_list.append(wall)

        # create right wall
        for i in range(2, 10):
            wall = Walls(850, 50 * i)
            MainGame.Wall_list.append(wall)

    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.DisplayWall()
            else:
                MainGame.Wall_list.remove(wall)
    def blitETank(self):
        for ETank in MainGame.ETank_List:
            if ETank.live:
                ETank.display()
                ETank.randMove()
                ETank.hitWalls()
                ETank.hitMyTank()
                Ebullet = ETank.shot()
                if Ebullet:
                    #MainGame.EBullet_list.append(Ebullet)
                    pass
            else:
                MainGame.ETank_List.remove(ETank)

    def blitBullet(self):
        for Bullet in MainGame.Bullet_list:
            if Bullet.exist:
                Bullet.Display()
                Bullet.bullmove()
                Bullet.hitEtank()
                Bullet.hitWall()
            else:
                MainGame.Bullet_list.remove(Bullet)

    def EblitBullet(self):
        for Ebullet in MainGame.EBullet_list:
            if Ebullet.exist:
                Ebullet.Display()
                Ebullet.bullmove()
                Ebullet.hitWall()
                if MainGame.Tank_1 and MainGame.Tank_1.live:
                    Ebullet.hittank()

            else:
                MainGame.EBullet_list.remove(Ebullet)

    def displayExplode(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.DisplayEx()
            else:
                MainGame.Explode_list.remove(explode)

    def get_events(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                self.Endgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not MainGame.Tank_1:
                    self.createMytank()

                if MainGame.Tank_1 and MainGame.Tank_1.live:
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
                        if len(MainGame.Bullet_list) < 3:
                            m = Bullet(MainGame.Tank_1)
                            MainGame.Bullet_list.append(m)
                        else:
                            print("No bullets")
                        print("Current bullet number:%d" % len(MainGame.Bullet_list))

            if MainGame.Tank_1 and MainGame.Tank_1.live:
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
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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
        self.live = True
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    def stay(self):
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                # check if any corner of the tank's bounding box collides with the wall
                corners = [(self.rect.left, self.rect.top),
                           (self.rect.left + self.rect.width, self.rect.top),
                           (self.rect.left, self.rect.top + self.rect.height),
                           (self.rect.left + self.rect.width, self.rect.top + self.rect.height)]
                for corner in corners:
                    if wall.rect.collidepoint(corner):
                        # if a corner collides with the wall, revert the position to the previous position
                        self.rect.left = self.oldLeft
                        self.rect.top = self.oldTop
                        return

    def move(self):
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
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
    def __init__(self, left, top):
        super().__init__(left, top)

    def hitEnemyTank(self):
        for Etank in MainGame.ETank_List:
            if pygame.sprite.collide_rect(Etank, self):
                print("Mytank collided with an enemy tank!")
                self.rect.left = self.oldLeft
                self.rect.top = self.oldTop
                Etank.rect.left = Etank.oldLeft
                Etank.rect.top = Etank.oldTop
    def move(self):
        super().move()
        self.press = False  # set press to False when moving

    def shoot(self):
        pass


class Enemytank(Tanks):

    def __init__(self, left, top, speed):
        super(Enemytank, self).__init__(left, top)
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
        self.speed = 1
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

    def shot(self):
        num = random.randint(1, 1000)
        if num <= 20:
            return Bullet(self)

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.Tank_1):
            self.rect.left = self.oldLeft
            self.rect.top = self.oldTop

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

        self.exist = True

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
                self.exist = False


        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.exist = False

        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.exist = False

        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.exist = False

    def Display(self, ):
        MainGame.window.blit(self.image, self.rect)

    def hitEtank(self):
        for Etank in MainGame.ETank_List:
            if pygame.sprite.collide_rect(Etank, self):
                explode = Explosion(Etank)
                MainGame.Explode_list.append(explode)
                self.exist = False
                Etank.live = False

    def hittank(self):

        if pygame.sprite.collide_rect(self, MainGame.Tank_1):

            explode = Explosion(MainGame.Tank_1)
            MainGame.Explode_list.append(explode)

            self.exist = False

            MainGame.Tank_1.live = False

    def hitWall(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.exist = False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False

class Explosion():
    def __init__(self, Tanks):
        self.rect = Tanks.rect
        self.step = 0
        self.images = [
            pygame.image.load('Images/explosion big.png'),
            pygame.image.load('Images/explosion mid.png'),
            pygame.image.load('Images/explosion small.png'),
            pygame.image.load('Images/explosion tiny.png'),
            ]
        self.image = self.images[self.step]
        self.live = True
    def DisplayEx(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            pygame.time.delay(75)
            self.step += 1
        else:
            self.live = False
            self.step = 0


class Walls():
    def __init__(self, top, left):
        self.image = pygame.image.load('Images/walls.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 5

    def DisplayWall(self):
        MainGame.window.blit(self.image, self.rect)
class Music():
    def __init__(self):
        pass

    def PlayMusic(self):
        pass


if __name__ == "__main__":
    MainGame().Startgame()
