from player import *
from asteroids import *

pygame.init()

back = pygame.image.load('images/location.png')

pygame.display.set_caption('Zachet')
win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0
highScore = 0



class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True


def redrawGameWindow():
    win.blit(back, (0,0))
    font = pygame.font.SysFont('TimesNewRoman',30)
    livesText = font.render('Жизней : ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Вы погибли. Нажмите пробел для начала', 1, (255,255,255))
    scoreText = font.render('Очков: ' + str(score), 1, (255,255,255))

    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)


    if gameover:
        win.blit(playAgainText, (sw//2-playAgainText.get_width()//2, sh//2 - playAgainText.get_height()//2))
    win.blit(scoreText, (sw - scoreText.get_width() - 25, 25))
    win.blit(livesText, (25, 25))
    pygame.display.update()



player = Player()
playerBullets = []
asteroids = []
count = 0
run = True
while run:
    clock.tick(60)
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid())

        player.Ship_out_of_bound()
        for b in playerBullets:
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b))


        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    break

            # bullet collision
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        score += 1
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))
                        break

        if lives <= 0:
            gameover = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playerBullets.append(Bullet())
            if event.key == pygame.K_SPACE:
                if gameover:
                    gameover = False
                    lives = 3
                    asteroids.clear()
                    if score > highScore:
                        highScore = score
                    score = 0

    redrawGameWindow()
pygame.quit()