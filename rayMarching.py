import pygame
import numpy as np

pygame.init()

HEIGHT, WIDTH = 800, 800

screen = pygame.display.set_mode((HEIGHT, WIDTH))

res = 10

FOV = 60

vel = 4
avel = 3

def dist(x, y = []):
    if y == []:
        y = [0 for _ in range(len(x))]
    return(pow(sum(pow(x0 - y0, 2) for x0, y0 in zip(x, y)), 1/2))

def map(s, x0, x1, y0, y1):
    return y0 + (float(s - x0) / float(x1 - x0)) * (y1 - y0)

def clamp(s, x, y):
    return max(min(s, y), x)


def sdfLine(point, line, R):
    h = min(1, max(0, np.dot(point - line.a, line.b - line.a)/np.dot(line.b - line.a, line.b - line.a)))
    return np.linalg.norm(point - line.a - (line.b - line.a) * h) - R

class Ray():
    def __init__(self, x, y, angle):
        self.pi = np.array([x, y], dtype="float64")
        self.p = np.array([x, y], dtype="float64")
        self.angle = angle

    def march(self, objects, R):
        self.p = self.pi.copy()

        while True: 

            minDist = np.inf

            for object in objects:

                if object.type == "line":
                    sdf = sdfLine(self.p, object, R)

                if minDist > sdf:
                    minDist = sdf

            pygame.draw.circle(screen, "white", self.p, minDist, 1)

            self.p += np.array([np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle))], dtype="float64")*minDist
            
            if R > minDist or self.p[0] < 0 or self.p[0] > WIDTH or self.p[1] < 0 or self.p[1] > HEIGHT:
                break

    def move(self, xo, yo):
        self.pi = np.array([xo, yo], dtype="float64")

    def draw2D(self):
        pygame.draw.line(screen, "white", self.pi, self.p)

    def draw3D(self, a):
        ...


        # pygame.draw.line(screen, [255-map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), 0, 15)**2]*3, 
        #                  (map(self.angle, a - FOV//2, a + FOV//2, 0, WIDTH), HEIGHT//2-map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), HEIGHT//2, 0)),
        #                  (map(self.angle, a - FOV//2, a + FOV//2, 0, WIDTH), HEIGHT//2+map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), HEIGHT//2, 0)), WIDTH//(FOV//res)+1)
        
class Object():
    def __init__(self, ax, ay, bx, by):
        self.a = np.array([ax, ay], dtype="float64")
        self.b = np.array([bx, by], dtype="float64")
        self.type = "line"
    
    def draw(self):
        pygame.draw.line(screen, 'white', self.a, self.b)

def main():
    
    run = True
    clock = pygame.time.Clock()

    rays = []

    R = 10

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
                if e.key == pygame.K_e:
                    R += 1
                if e.key == pygame.K_q:
                    R -= 1

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
                xo = clamp(xo + np.cos(np.radians(a+90))*vel, 0, WIDTH)
                yo = clamp(yo + np.sin(np.radians(a+90))*vel, 0, HEIGHT)
            if i == 'A':
                xo = clamp(xo + np.cos(np.radians(a-90))*vel, 0, WIDTH)
                yo = clamp(yo + np.sin(np.radians(a-90))*vel, 0, HEIGHT)
            if i == 'W':
                xo = clamp(xo + np.cos(np.radians(a))*vel, 0, WIDTH)
                yo = clamp(yo + np.sin(np.radians(a))*vel, 0, HEIGHT)
            if i == 'S':
                xo = clamp(xo + np.cos(np.radians(a+180))*vel, 0, WIDTH)
                yo = clamp(yo + np.sin(np.radians(a+180))*vel, 0, HEIGHT)
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
            ray.march(objects, R)
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