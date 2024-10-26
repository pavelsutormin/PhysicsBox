# imports
import random
import noise
import sys
import pygame
from phys_tools import *
import asyncio

# init
pygame.init()
fpsClock = pygame.time.Clock()
SMALL_FONT = pygame.font.SysFont("andalemono", 28)
MEDIUM_FONT = pygame.font.SysFont("andalemono", 56)
BIG_FONT = pygame.font.SysFont("andalemono", 112)

WIDTH = 1920
HEIGHT = 1080

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")


# terrain generation
r_n = random.randint(0, 15000)
def gen_terrain(i):
    return noise.pnoise1(i/r_n) * 1000


heightByX = HeightByXCreate(HEIGHT, WIDTH, gen_terrain)


# classes
class Bot:
    def __init__(self, scr: pygame.Surface, color: tuple[int, int, int] = (0, 255, 255), start_x: int = 100,
                 start_y: int = 0, radius: int = 20):
        self.x = start_x
        self.y = start_y
        self.screen = scr
        self.color = color
        self.radius = radius
        self.comp = 1
        self.direction = 0
        self.velocity = 0
        print("Bot Initialized!")

    def update(self):
        if random.randint(0, 100) == 0:
            if self.direction == 0:
                self.direction = random.choice([-4, 4])
            else:
                self.direction = 0
        if self.y > HEIGHT // 2:
            if random.randint(0, 50) == 0:
                for _b in range(1, 50):
                    self.velocity = -3.3
        self.x -= self.direction
        if self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
        if self.x < self.radius:
            self.x = self.radius
        self.y += self.velocity
        while calcMinDist(self, WIDTH, heightByX) < 0:
            self.y -= 1
        if self.y < self.radius:
            self.y = self.radius
        self.velocity += 0.1
        pygame.draw.ellipse(self.screen, self.color,
                            (self.x - self.radius, self.y - self.radius * self.comp,
                             self.radius * 2, self.radius * (self.comp + 1)))


class Player:
    def __init__(self, scr: pygame.Surface, color: tuple[int, int, int] = (0, 255, 255), start_x: int = 100,
                 start_y: int = 0, radius: int = 20):
        self.x = start_x
        self.y = start_y
        self.screen = scr
        self.color = color
        self.radius = radius
        self.comp = 1
        self.direction = 0
        self.velocity = 0
        print("Player Initialized!")

    def update(self):
        self.x -= self.direction
        if self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
        if self.x < self.radius:
            self.x = self.radius
        self.y += self.velocity
        while calcMinDist(self, WIDTH, heightByX) < 0:
            self.y -= 1
        if self.y < self.radius:
            self.y = self.radius
        self.velocity += 0.1
        pygame.draw.ellipse(self.screen, self.color,
                            (self.x - self.radius, self.y - self.radius * self.comp,
                             self.radius * 2, self.radius * (self.comp + 1)))


class Rock:
    def __init__(self, scr: pygame.Surface, color: tuple[int, int, int] = (0, 255, 255), start_x: int = 100,
                 start_y: int = 0, radius: int = 10):
        self.x = start_x
        self.y = start_y
        self.screen = scr
        self.color = color
        self.radius = radius
        self.velocity = 0
        print("Rock Initialized!")

    def update(self, ):  # rocks: []):
        if heightByX[self.x] < heightByX[self.x + 5]:
            self.x += random.randint(0, 100) // 25
        elif heightByX[self.x] < heightByX[self.x - 5]:
            self.x -= random.randint(0, 100) // 25
        if self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
        if self.x < self.radius:
            self.x = self.radius
        self.y += self.velocity
        while calcMinDist(self, WIDTH, heightByX) < 0:
            self.y -= 1
        if self.y < self.radius:
            self.y = self.radius
        self.velocity += random.randint(100, 150) / 100
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


# definitions
bot = Bot(screen, (100, 149, 237), WIDTH // 3, HEIGHT // 3, 20)
player = Player(screen, (242, 140, 40), WIDTH // 3 * 2, HEIGHT // 3, 20)
rocky = Rock(screen, (100, 100, 100), WIDTH // 2, 50, 10)
drawing = False
drawing_strait = False
start_pos = (0, 0)
end_pos = (0, 0)
direct = 0


async def main():
    # global statements
    global drawing
    global bot
    global player
    global direct
    global start_pos
    global end_pos
    global drawing_strait
    while True:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                if event.button == pygame.BUTTON_LEFT:
                    start_pos = pygame.mouse.get_pos()
                    drawing_strait = False
                if event.button == pygame.BUTTON_RIGHT:
                    start_pos = pygame.mouse.get_pos()
                    drawing_strait = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                if event.button == pygame.BUTTON_LEFT:
                    points = calcSeg(start_pos, end_pos)
                    for i in range(start_pos[0], end_pos[0] + 1):
                        try:
                            heightByX[i] = points[i]
                        except KeyError:
                            print("There was a KeyError!")
                if event.button == pygame.BUTTON_RIGHT:
                    for i in range(start_pos[0], end_pos[0] + 1):
                        try:
                            heightByX[i] = start_pos[1]
                        except KeyError:
                            print("There was a KeyError!")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.direction = 4
                if event.key == pygame.K_RIGHT:
                    player.direction = -4
                if event.key == pygame.K_UP:
                    player.velocity = -3.3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.direction = 0
                if event.key == pygame.K_RIGHT:
                    player.direction = 0
        # clear screen
        screen.fill((50, 50, 50))
        # update items
        bot.update()
        player.update()
        rocky.update()
        # draw the ground
        b_points = [(0, HEIGHT)]
        b_points.extend(hbx2points(heightByX))
        b_points.extend([(WIDTH, HEIGHT)])
        pygame.draw.polygon(screen, (0, 150, 0), b_points)
        pygame.draw.lines(screen, (0, 50, 0), True, b_points, 1)
        # draw the editing line
        if drawing:
            if drawing_strait:
                end_pos = (pygame.mouse.get_pos()[0], start_pos[1])
            else:
                end_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 3)
        # draw the console
        rect_surf = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
        rect_surf.fill((0, 0, 0, 200))
        if True:
            rect_surf.blit(SMALL_FONT.render("It's made by me, Pasha!", True, (255, 255, 255)), (0, 0))
        screen.blit(rect_surf, (0, 0))
        # draw the text
        fps_text = SMALL_FONT.render(f"Fps: {round(fpsClock.get_fps(), 2)}", True, (255, 255, 255))
        screen.blit(fps_text, (WIDTH - fps_text.get_width(), 0))
        # update screen
        pygame.display.flip()
        fpsClock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())
