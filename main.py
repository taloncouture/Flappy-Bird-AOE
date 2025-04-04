import pygame
import random

WIDTH = 768
HEIGHT = 768
SCALEFACTOR = 2
FPS = 60


pygame.init()
pygame.display.set_caption("Roaree Flappy Bird")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



# background_image = pygame.image.load("background2.png")
# background_image = pygame.transform.scale(background_image, (background_image.get_width() * 3, background_image.get_height() * 3))

ground_image = pygame.image.load("ground.png")
ground_image = pygame.transform.scale(ground_image, (ground_image.get_width() * 4, ground_image.get_height() * 4))

roaree_image = pygame.image.load("roaree.png")
roaree_image = pygame.transform.scale(roaree_image, (roaree_image.get_width() *  3, roaree_image.get_height() * 3))

building_image = pygame.image.load("building.png")
building_image = pygame.transform.scale(building_image, (building_image.get_width() * 3, building_image.get_height() * 3))

background_x = 0

ground_x = 0
ground2_x = ground_image.get_width()


building_min = 200
building_max = 700
gap = 200


class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, bottom, index):
        if(bottom == False):
            self.image = pygame.transform.flip(building_image, False, True)
        else:
            self.image = building_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bottom = bottom
        self.index = index

    def update(self):
        self.rect.x -= 5

        if(self.rect.x + self.rect.width < 0):
            self.rect.x += 1200

            if(self.bottom):
                self.rect.y = random.randint(building_min, building_max)
            else:
                self.rect.y = buildings[self.index - 1].rect.y - building_image.get_height() - gap

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Roaree(pygame.sprite.Sprite):
    def __init__(self, x, y):

        self.image = roaree_image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0


    def update(self):

        self.velocity += 0.5

        self.rect.y += self.velocity

        if((self.rect.y + self.rect.height) > HEIGHT - 44):
            self.rect.y = HEIGHT - self.rect.height -44

    def input(self):
        keys = pygame.key.get_pressed()

        if(keys[pygame.K_SPACE]):
            self.velocity = -7
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)

buildings = []


running = True

roaree = Roaree(100, 100)

buildings.append(Building(WIDTH, random.randint(building_min, building_max), True, 0))
buildings.append(Building(WIDTH, buildings[0].rect.y - building_image.get_height() - gap, False, 1))
buildings.append(Building(WIDTH + 600, random.randint(building_min, building_max), True, 2))
buildings.append(Building(WIDTH + 600, buildings[2].rect.y - building_image.get_height() - gap, False, 3))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    #screen.blit(background_image, (background_x, 0))
    screen.fill((66, 191, 245))
    #background_x -= 1

    

    roaree.draw(screen)
    roaree.input()
    roaree.update()

    for building in buildings:

        building.draw(screen)
        building.update()


    screen.blit(ground_image, (ground_x, screen.get_height() - ground_image.get_height()))
    ground_x -= 5
    if(ground_x < -128):
        ground_x = 0

    pygame.display.update()
    clock.tick(FPS)