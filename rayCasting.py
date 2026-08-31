import pygame
import math

pygame.init()

HEIGHT, WIDTH = 800, 800

screen = pygame.display.set_mode((HEIGHT, WIDTH))

res = 1

FOV = 60

vel = 4
avel = 3

# TODO: Hacer que cuanto más cerca esté un rayo más ancho sea. Se podría hacer llevando la cuenta del WIDTH usado con 
# una variable y mapeando el valor que tendrían que tener la suma de los rayos para que diesen el valor que hiciese 
# que ocupase toda la pantalla.

def dist(x, y):
    return(pow(pow(x[0]-y[0], 2) + pow(x[1]-y[1], 2), 1/2))

def map(s, x0, x1, y0, y1):
    return y0 + (float(s - x0) / float(x1 - x0)) * (y1 - y0)

def clamp(s, x, y):
    return max(min(s, y), x)

class Ray():
    def __init__(self, x, y, angle):
        self.xi = x
        self.yi = y
        self.x = x
        self.y = y
        self.angle = angle
        self.collided = False
        self.len = 0
    
    def cast(self, objects):
        
        self.dirx = math.cos(math.radians(self.angle))
        self.diry = math.sin(math.radians(self.angle))
        self.x = self.xi
        self.y = self.yi
        self.collided = False

        while not self.collided and not self.x > HEIGHT and not self.y > WIDTH and not self.x < 0 and not self.y < 0:
        
            self.x += self.dirx
            self.y += self.diry

            for other in objects:
                denom = (self.xi - self.x) * (other.y1 - other.y2) - (self.yi - self.y) * (other.x1 - other.x2)
                if denom == 0:
                    denom = 0.001
                t = ((self.xi - other.x1) * (other.y1 - other.y2) - (self.yi - other.y1) * (other.x1 - other.x2)) / denom
                u = - ((self.xi - self.x) * (self.yi - other.y1) - (self.yi - self.y) * (self.xi - other.x1)) / denom

                
                if t >= 0 and t <= 1 and u >= 0 and u <= 1 or self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
                    self.collided = True
                    self.len = dist([self.x, self.y], [self.xi, self.yi])

    def move(self, xo, yo):
        self.xi = xo
        self.yi = yo
                
    def draw2D(self):
        pygame.draw.line(screen, 'white', (self.xi, self.yi), (self.x, self.y))

    def draw3D(self, a):
        pygame.draw.line(screen, [255-map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), 0, 15)**2]*3, 
                         (map(self.angle, a - FOV//2, a + FOV//2, 0, WIDTH), HEIGHT//2-map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), HEIGHT//2, 0)),
                         (map(self.angle, a - FOV//2, a + FOV//2, 0, WIDTH), HEIGHT//2+map(self.len, 0, 2**(1/2)*max(HEIGHT, WIDTH), HEIGHT//2, 0)), WIDTH//(FOV//res)+1)

class Object():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def draw(self):
        pygame.draw.line(screen, 'white', (self.x1, self.y1), (self.x2, self.y2))

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
            ray.cast(objects)
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