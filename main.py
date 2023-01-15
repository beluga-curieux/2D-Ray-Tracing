from pygame.locals import *
import pygame
import sys
import math
import aparecium

pygame.init()

# -----Options-----
WINDOW_SIZE = (1200, 800) # Width x Height in pixels
NUM_RAYS = 500 # Must be between 1 and 360
SOLID_RAYS = False # Can be somewhat glitchy. For best results, set NUM_RAYS to 360
CLOCK = pygame.time.Clock()
#------------------
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)

mx, my = pygame.mouse.get_pos()
lastClosestPoint = (0, 0)
running = True
rays = []
walls = []
particles = []
angle = 0

info = aparecium.DataDisplay({"nombre de rayon": NUM_RAYS})


class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.dir = (math.cos(angle), math.sin(angle))

    def update(self, mx, my):
        self.x = mx
        self.y = my

    def get_collision(self, wall):
        x1 = wall.start_pos[0]
        y1 = wall.start_pos[1]
        x2 = wall.end_pos[0]
        y2 = wall.end_pos[1]

        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir[0]
        y4 = self.y + self.dir[1]

        # Using line-line intersection formula to get intersection point of ray and wall
        # Where (x1, y1), (x2, y2) are the ray pos and (x3, y3), (x4, y4) are the wall pos
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        if denominator == 0:
            return None

        t = numerator / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 1 > t > 0 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            collidePos = [x, y]
            return collidePos


class Wall:
    def __init__(self, start_pos, end_pos, color = 'white'):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.slope_x = end_pos[0] - start_pos[0]
        self.slope_y = end_pos[1] - start_pos[1]
        if self.slope_x == 0:
            self.slope = 0
        else:
            self.slope = self.slope_y / self.slope_x
        self.length = math.sqrt(self.slope_x**2 + self.slope_y**2)

    def draw(self):
        pygame.draw.line(display, self.color, self.start_pos, self.end_pos, 3)


class RotatedWall(Wall):
    def __init__(self, center: tuple[int, int], r: int, angle: int = 0):
        self.center = center
        self.r = r
        self.angle = angle
        self.col = 0

        self.set_angle(angle)


    def set_angle(self, angle):
        self.angle = angle
        super().__init__((self.center[0] + math.cos(math.radians(90 - angle)) * self.r, self.center[1] + math.sin(math.radians(90 - angle)) * self.r),
                         (self.center[0] - math.cos(math.radians(90 - angle)) * self.r, self.center[1] - math.sin(math.radians(90 - angle)) * self.r))

    def confirme_colition(self):
        self.col += 1

    def get_colition(self):
        col = self.col
        self.col = 0
        return col


main_wall = RotatedWall((WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2), 300, angle)


def draw_rays(rays, walls, color='white'):
    global lastClosestPoint
    for ray in rays:
        closest = 100000
        closestPoint = None
        for wall in walls:

            intersectPoint = ray.get_collision(wall)
            if intersectPoint is not None:
                if type(wall) is RotatedWall:
                    wall.confirme_colition()
                # Get distance between ray source and intersect point
                ray_dx = ray.x - intersectPoint[0]
                ray_dy = ray.y - intersectPoint[1]
                # If the intersect point is closer than the previous closest intersect point, it becomes the closest intersect point
                distance = math.sqrt(ray_dx**2 + ray_dy**2)
                if (distance < closest):
                    closest = distance
                    closestPoint = intersectPoint

        if closestPoint is not None:
            pygame.draw.line(display, color, (ray.x, ray.y), closestPoint)
            if SOLID_RAYS:
                pygame.draw.polygon(display, color, [(mx, my), closestPoint, lastClosestPoint])
                lastClosestPoint = closestPoint


for i in range(0, NUM_RAYS):
    rays.append(Ray(mx, my, math.radians(360*i/NUM_RAYS)))


def generate_walls():
    walls.clear()

    walls.append(Wall((0, 0), (WINDOW_SIZE[0], 0)))
    walls.append(Wall((0, 0), (0, WINDOW_SIZE[1])))
    walls.append(Wall((WINDOW_SIZE[0], 0), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
    walls.append(Wall((0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1])))

    walls.append(main_wall)


def draw():
    display.fill((0, 0, 0))

    for wall in walls:
        wall.draw()

    for particle in particles:
        particle.draw()

    draw_rays([ray for ray in rays], [wall for wall in walls])

    screen.blit(display, (0, 0))
    info.draw(screen)

    pygame.display.update()

generate_walls()


while running:
    CLOCK.tick(60)
    angle += 1
    main_wall.set_angle(angle)
    mx, my = (0, WINDOW_SIZE[1]//2)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

        if event.type == KEYDOWN:
            # Re-randomize walls on Space
            if event.key == pygame.K_SPACE:
                generate_walls()

    for ray in rays:
        ray.update(mx, my)

    info.update_data({"nb de colition": main_wall.get_colition()})

    draw()





