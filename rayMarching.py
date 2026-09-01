import pygame
import numpy as np

pygame.init()

HEIGHT, WIDTH, DEPTH = 800, 800, 800

screen = pygame.display.set_mode((HEIGHT, WIDTH))

COLORS = {"line": np.array([0, 1, 0]), "sphere": np.array([1, 0, 0]), "infPlane": np.array([1, 1, 1])}

def clamp(s, x, y):
    return max(min(s, y), x)

def sdfLine(point, line, R):
    h = min(1, max(0, np.dot(point - line.a, line.b - line.a)/np.dot(line.b - line.a, line.b - line.a)))
    return np.linalg.norm(point - line.a - (line.b - line.a) * h) - R

def sdfSphere(point, sphere):
    return ((point[0] - sphere.p[0])**2 + (point[1] - sphere.p[1])**2 + (point[2] - sphere.p[2])**2)**0.5 - sphere.r
    #return np.linalg.norm(point - sphere.p) - sphere.r

def sdfInfPlane(point, plane):
    return -(point[2]-plane.z)


def sdfScene(point, objects, R):
    minDist = np.inf
    minType = None
    for object in objects:
        if object.type == "line":
            sdf = sdfLine(point, object, R)
            sdfType = "line"
        elif object.type == "sphere":
            sdf = sdfSphere(point, object)
            sdfType = "sphere"
        elif object.type == "infPlane":
            sdf = sdfInfPlane(point, object)
            sdfType = "infPlane"
        if minDist > sdf:
            minDist = sdf
            minType = sdfType
    return minDist, minType

class Ray():
    def __init__(self, x, y, z, theta, phi):
        self.pi = np.array([x, y, z], dtype="float64")
        self.p = np.array([x, y, z], dtype="float64")
        self.theta = theta
        self.phi = phi
        self.direction = np.array([np.cos(self.theta)*np.cos(self.phi), np.sin(self.theta)*np.cos(self.phi), np.sin(self.phi)], dtype="float64")
    def march(self, objects, R):
        self.p = self.pi.copy()
        d = 0
        #direction = np.array([np.cos(self.theta)*np.cos(self.phi), np.sin(self.theta)*np.cos(self.phi), np.sin(self.phi)], dtype="float64")
        steps = 4
        while steps > 0: 
            steps -= 1
            minDist, minType = sdfScene(self.p, objects, R)

            self.p += self.direction*minDist
            d += minDist
            if minDist < 1:
                return (minType, d)
            if self.p[0] < 0 or self.p[0] > WIDTH or self.p[1] < 0 or self.p[1] > HEIGHT or self.p[2] < 0 or self.p[2] > DEPTH:
                return (None, -1)
        return (None, -1)

    def move(self, x0, y0, z0):
        self.pi = np.array([x0, y0, z0], dtype="float64")

class Line():
    def __init__(self, ax, ay, az, bx, by, bz):
        self.a = np.array([ax, ay, az], dtype="float64")
        self.b = np.array([bx, by, bz], dtype="float64")
        self.type = "line"

class Sphere():
    def __init__(self, x, y, z, r):
        self.p = np.array([x, y, z])
        self.r = r
        self.type = "sphere"

class InfPlane():
    def __init__(self, z):
        self.z = z
        self.type = "infPlane"

def main():
    
    run = True
    clock = pygame.time.Clock()

    rays = []

    R = 10

    res = 0.03

    FOV = np.pi/3

    vel = 3
    avel = 4 * np.pi / 180

    x0 = 400
    y0 = 400
    z0 = 400

    theta = 0
    phi = 0

    for i in range(int((phi-FOV/2) / res), int((phi+FOV/2) / res)):
        for j in range(int((theta-FOV/2) / res), int((theta+FOV/2) / res)):
        
            rays.append(Ray(x0, y0, z0, j*res, i*res))

    objects = []
    objects.append(Line(600, 600, 0, 600, 200, 0))
    objects.append(Line(100, 100, 100, 700, 500, 500))
    objects.append(Sphere(600, 400, 400, 50))
    objects.append(InfPlane(800))

    inputs = []
    frame = 0
    while run:
        frame += 1
        if frame % 10:
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
                x0 += np.cos(theta+np.pi/2)*vel
                y0 += np.sin(theta+np.pi/2)*vel
            if i == 'A':
                x0 += np.cos(theta-np.pi/2)*vel
                y0 += np.sin(theta-np.pi/2)*vel
            if i == 'W':
                x0 += np.cos(theta)*vel
                y0 += np.sin(theta)*vel
            if i == 'S':
                x0 += np.cos(theta+np.pi)*vel
                y0 += np.sin(theta+np.pi)*vel
            if i == 'T':
                z0 -= vel
            if i == 'B':
                z0 += vel
            if i == 'L':
                theta -= avel
                for ray in rays:
                    ray.direction = np.array([np.cos(ray.theta + theta)*np.cos(ray.phi + phi), np.sin(ray.theta + theta)*np.cos(ray.phi + phi), np.sin(ray.phi + phi)], dtype="float64")
            if i == 'R':
                theta += avel
                for ray in rays:
                    ray.direction = np.array([np.cos(ray.theta + theta)*np.cos(ray.phi + phi), np.sin(ray.theta + theta)*np.cos(ray.phi + phi), np.sin(ray.phi + phi)], dtype="float64")
            if i == 'U':
                phi = clamp(phi - avel, -np.pi, np.pi)
                for ray in rays:
                    ray.direction = np.array([np.cos(ray.theta + theta)*np.cos(ray.phi + phi), np.sin(ray.theta + theta)*np.cos(ray.phi + phi), np.sin(ray.phi + phi)], dtype="float64")
            if i == 'O':
                phi = clamp(phi + avel, -np.pi, np.pi)
                for ray in rays:
                    ray.direction = np.array([np.cos(ray.theta + theta)*np.cos(ray.phi + phi), np.sin(ray.theta + theta)*np.cos(ray.phi + phi), np.sin(ray.phi + phi)], dtype="float64")

        screen.fill('black')
        pixels = np.full((HEIGHT, WIDTH, 3), [160, 160, 160])
        size = int(np.sqrt(len(rays)))
        for i, ray in enumerate(rays):
            ray.move(x0, y0, z0)
            t, d = ray.march(objects, R)
            if d != -1:
                pixels[int((i%size) * 800/size): int((i%size) * 800/size) + int(max(size, 800/size)), int((i//size) * 800/size): int((i//size) * 800/size) + int(max(size, 800/size))] = COLORS[t] * clamp((255 + (d / 1386) * -255), 0, 255) # max distance = 1.386 inside a 800x800x800 cube
        #print([x0, y0, z0])
        surface = pygame.surfarray.make_surface(pixels)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()