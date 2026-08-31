import pygame
import numpy as np

pygame.init()

HEIGHT, WIDTH, DEPTH = 800, 800, 800

screen = pygame.display.set_mode((HEIGHT, WIDTH))

res = 0.1

FOV = np.pi/3

vel = 4
avel = 3 * np.pi / 180

COLORS = {"line": (0, 255, 0)}

def clamp(s, x, y):
    return max(min(s, y), x)

def sdfLine(point, line, R):
    h = min(1, max(0, np.dot(point - line.a, line.b - line.a)/np.dot(line.b - line.a, line.b - line.a)))
    return np.linalg.norm(point - line.a - (line.b - line.a) * h) - R

class Ray():
    def __init__(self, x, y, z, theta, phi):
        self.pi = np.array([x, y, z], dtype="float64")
        self.p = np.array([x, y, z], dtype="float64")
        self.theta = theta
        self.phi = phi

    def march(self, objects, R):
        self.p = self.pi.copy()
        d = 0
        while True: 

            minDist = np.inf

            for object in objects:

                if object.type == "line":
                    sdf = sdfLine(self.p, object, R)
                    sdfType = "line"

                if minDist > sdf:
                    minDist = sdf
                    minType = sdfType

            #pygame.draw.circle(screen, "white", self.p, minDist, 1)

            self.p += np.array([np.cos(self.theta)*np.cos(self.phi), np.sin(self.theta)*np.cos(self.phi), np.sin(self.phi)], dtype="float64")*minDist
            d += minDist
            if 0.1 > minDist:
                return (minType, d)
            if self.p[0] < 0 or self.p[0] > WIDTH or self.p[1] < 0 or self.p[1] > HEIGHT or self.p[2] < 0 or self.p[2] > DEPTH:
                return (None, -1)

    def move(self, x0, y0, z0):
        self.pi = np.array([x0, y0, z0], dtype="float64")

class Line():
    def __init__(self, ax, ay, az, bx, by, bz):
        self.a = np.array([ax, ay, az], dtype="float64")
        self.b = np.array([bx, by, bz], dtype="float64")
        self.type = "line"

def main():
    
    run = True
    clock = pygame.time.Clock()

    rays = []

    R = 10

    x0 = 400
    y0 = 400
    z0 = 400

    theta = FOV
    phi = -FOV
    for i in range(int((phi-FOV/2) / res), int((phi+FOV/2) / res)):
        for j in range(int((theta-FOV/2) / res), int((theta+FOV/2) / res)):
        
            rays.append(Ray(x0, y0, z0, j*res, i*res))

    objects = []
    objects.append(Line(600, 600, 0, 600, 200, 0))
    objects.append(Line(100, 100, 100, 700, 500, 500))

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
                if e.key == pygame.K_UP:
                    inputs.append('U')
                if e.key == pygame.K_DOWN:
                    inputs.append('O') # search for a better letter
                if e.key == pygame.K_SPACE:
                    inputs.append('T')
                if e.key == pygame.K_LSHIFT:
                    inputs.append('B')
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
                if e.key == pygame.K_UP:
                    inputs.remove('U')
                if e.key == pygame.K_DOWN:
                    inputs.remove('O') # search for a better letter
                if e.key == pygame.K_SPACE:
                    inputs.remove('T')
                if e.key == pygame.K_LSHIFT:
                    inputs.remove('B')

        for i in inputs:
            if i == 'D':
                x0 = clamp(x0 + np.cos(np.radians(theta+np.pi/2))*vel, 0, WIDTH)
                y0 = clamp(y0 + np.sin(np.radians(theta+np.pi/2))*vel, 0, HEIGHT)
            if i == 'A':
                x0 = clamp(x0 + np.cos(np.radians(theta-np.pi/2))*vel, 0, WIDTH)
                y0 = clamp(y0 + np.sin(np.radians(theta-np.pi/2))*vel, 0, HEIGHT)
            if i == 'W':
                x0 = clamp(x0 + np.cos(np.radians(theta))*vel, 0, WIDTH)
                y0 = clamp(y0 + np.sin(np.radians(theta))*vel, 0, HEIGHT)
            if i == 'S':
                x0 = clamp(x0 + np.cos(np.radians(theta+np.pi))*vel, 0, WIDTH)
                y0 = clamp(y0 + np.sin(np.radians(theta+np.pi))*vel, 0, HEIGHT)
            if i == 'T':
                z0 = clamp(z0 + vel, 0, DEPTH)
            if i == 'B':
                z0 = clamp(z0 - vel, 0, DEPTH)
            if i == 'L':
                theta -= avel
                for ray in rays:
                    ray.theta -= avel
            if i == 'R':
                theta += avel
                for ray in rays:
                    ray.theta += avel
            if i == 'U':
                phi += avel
                for ray in rays:
                    ray.theta += avel
            if i == 'O':
                phi -= avel
                for ray in rays:
                    ray.phi -= avel

        screen.fill('black')
        pixels = pygame.PixelArray(screen)
        for i, ray in enumerate(rays):
            ray.move(x0, y0, z0)
            t, d = ray.march(objects, R)
            if d == -1:
                pixels[i%10, i//10] = [(160, 160, 160)]
            else:
                pixels[i%10, i//10] = [COLORS[t]]
        pixels.close()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()