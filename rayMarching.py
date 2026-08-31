import pygame
import math

pygame.init()

HEIGHT, WIDTH = 800, 800

screen = pygame.display.set_mode((HEIGHT, WIDTH))

res = 4

FOV = 60

vel = 4
avel = 3

def dist(x, y):
    return(pow(pow(x[0]-y[0], 2) + pow(x[1]-y[1], 2), 1/2))

def map(s, x0, x1, y0, y1):
    return y0 + (float(s - x0) / float(x1 - x0)) * (y1 - y0)

def clamp(s, x, y):
    return max(min(s, y), x)

def dot(x, y):
    return sum(x0 * y0 for x0, y0 in zip(x, y))

def Sum(x, y):
    return [x0 + y0 for x0, y0 in zip(x, y)]

def Sub(x, y):
    return [x0 - y0 for x0, y0 in zip(x, y)]

def Mult(t, x):
    return [t * x0 for x0 in x]


def sdfLine(point, line, R):
    h = min(1, max(0, dot(Sub(point, line.a), Sub(line.b, line.a))/dot(Sub(line.b, line.a), Sub(line.b, line.a))))
    return dist([0, 0], Sub(Sub(point, line.a), Mult(h, Sub(line.b, line.a)))) - R

class Ray():
    def __init__(self, x, y, angle):
        self.pi = [x, y]
        self.p = [x, y]
        self.angle = angle

    def march(self, objects):
        self.p = self.pi.copy()
        while True: 

            minDist = math.inf

            for object in objects:

                if object.type == "line":
                    sdf = sdfLine(self.p, object, 10)

                if minDist > sdf:
                    minDist = sdf
            
            self.p = Sum(self.p, [math.cos(self.angle), math.sin(self.angle)])
                
            if 1 > minDist or minDist > 1000:
                break

    def move(self, xo, yo):
        self.pi = [xo, yo]

    def draw2D(self):
        pygame.draw.line(screen, "white", self.pi, self.p)

    def draw3D(self, a):

        ...


        # pygame.draw.line(screen, [255-map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), 0, 15)**2]*3, 
        #                  (map(self.angle, a - FOV//2, a + FOV//2, 0, WIDTH), HEIGHT//2-map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), HEIGHT//2, 0)),
        #                  (map(self.angle, a - FOV//2, a + FOV//2, 0, WIDTH), HEIGHT//2+map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), HEIGHT//2, 0)), WIDTH//(FOV//res)+1)
        
class Object():
    def __init__(self, ax, ay, bx, by):
        self.a = [ax, ay]
        self.b = [bx, by]
        self.type = "line"
    
    def draw(self):
        pygame.draw.line(screen, 'white', self.a, self.b)

def main():
    
    run = True
    clock = pygame.time.Clock()

    rays = []

    xo = 400
    yo = 400

    a = FOV

    mode = "2D"

    for i in range(int((a-FOV//2) / res), int((a+FOV//2) / res)):
        rays.append(Ray(xo, yo, i*res))

    objects = []
    objects.append(Object(600, 600, 600, 200))
    objects.append(Object(100, 100, 700, 500))

    inputs = []

    while run:

        pygame.display.set_caption("FPS: " + str(clock.get_fps()))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    run = False
                if e.key == pygame.K_d:
                    inputs.append('D')
                if e.key == pygame.K_a:
                    inputs.append('A')
                if e.key == pygame.K_w:
                    inputs.append('W')
                if e.key == pygame.K_s:
                    inputs.append('S')
                if e.key == pygame.K_LEFT:
                    inputs.append('L')
                if e.key == pygame.K_RIGHT:
                    inputs.append('R')
                if e.key == pygame.K_SPACE:
                    if mode == "3D":
                        mode = "2D"
                    else:
                        mode = "3D"

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_d:
                    inputs.remove('D')
                if e.key == pygame.K_a:
                    inputs.remove('A')
                if e.key == pygame.K_w:
                    inputs.remove('W')
                if e.key == pygame.K_s:
                    inputs.remove('S')
                if e.key == pygame.K_LEFT:
                    inputs.remove('L')
                if e.key == pygame.K_RIGHT:
                    inputs.remove('R')
        for i in inputs:
            if i == 'D':
                xo = clamp(xo + math.cos(math.radians(a+90))*vel, 0, WIDTH)
                yo = clamp(yo + math.sin(math.radians(a+90))*vel, 0, HEIGHT)
            if i == 'A':
                xo = clamp(xo + math.cos(math.radians(a-90))*vel, 0, WIDTH)
                yo = clamp(yo + math.sin(math.radians(a-90))*vel, 0, HEIGHT)
            if i == 'W':
                xo = clamp(xo + math.cos(math.radians(a))*vel, 0, WIDTH)
                yo = clamp(yo + math.sin(math.radians(a))*vel, 0, HEIGHT)
            if i == 'S':
                xo = clamp(xo + math.cos(math.radians(a+180))*vel, 0, WIDTH)
                yo = clamp(yo + math.sin(math.radians(a+180))*vel, 0, HEIGHT)
            if i == 'L':
                a -= avel
                for ray in rays:
                    ray.angle -= avel
            if i == 'R':
                a += avel
                for ray in rays:
                    ray.angle += avel

        screen.fill('black')

        for ray in rays:
            ray.move(xo, yo)
            ray.march(objects)
            if mode == "2D":
                ray.draw2D()
            else:
                ray.draw3D(a)
        if mode == "2D":
            for object in objects:
                object.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()