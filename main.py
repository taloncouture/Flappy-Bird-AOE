import pygame
import random

WIDTH = 768
HEIGHT = 768
SCALEFACTOR = 2
FPS = 60

score = 0


pygame.init()
pygame.font.init()
pygame.display.set_caption("Roaree Flappy Bird")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

vga_font = pygame.font.Font("VGA9.ttf", 30)
vga_large = pygame.font.Font("VGA9.ttf", 60)
#score_surface = vga_font.render(str(score), False, (0, 0, 0))

background_image = pygame.image.load("background3_0.png")
background_image = pygame.transform.scale(background_image, (background_image.get_width(), background_image.get_height()))

ground_image = pygame.image.load("ground.png")
ground_image = pygame.transform.scale(ground_image, (ground_image.get_width() * 4, ground_image.get_height() * 4))

roaree_image = pygame.image.load("roaree.png")
roaree_image = pygame.transform.scale(roaree_image, (roaree_image.get_width() *  2.5, roaree_image.get_height() * 2.5))

roaree_large = pygame.transform.scale(roaree_image, (roaree_image.get_width() *  2, roaree_image.get_height() * 2))

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

        if(keys[pygame.K_r]):
            self.velocity = -7
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)

buildings = []
roaree = Roaree(WIDTH / 2, HEIGHT / 2)

def init_game():

    buildings.clear()

    buildings.append(Building(WIDTH, random.randint(building_min, building_max), True, 0))
    buildings.append(Building(WIDTH, buildings[0].rect.y - building_image.get_height() - gap, False, 1))
    buildings.append(Building(WIDTH + 600, random.randint(building_min, building_max), True, 2))
    buildings.append(Building(WIDTH + 600, buildings[2].rect.y - building_image.get_height() - gap, False, 3))

running = True
playing = False
initalized = False

init_game()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if(keys[pygame.K_r] and playing == False):
        init_game()
        initalized = True
        score = 0
        roaree.rect.x = 100
        roaree.rect.y = 100
        playing = True

    
    screen.fill((66, 191, 245))
    

    if(initalized):

        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + background_image.get_width(), 0))

        for building in buildings:
            building.draw(screen)

        screen.blit(ground_image, (ground_x, screen.get_height() - ground_image.get_height()))
        roaree.draw(screen)

    else:

        screen.blit(roaree_large, roaree_large.get_rect(center = (WIDTH / 2, HEIGHT / 2)))


    if(playing):

        
        roaree.input()
        roaree.update()

        for building in buildings:

            building.update()
            
            if(roaree.rect.colliderect(building.rect) or (roaree.rect.y + roaree.rect.height) >= HEIGHT - 44):
                playing = False

            if(building.rect.x + building.rect.width < 0):
                building.rect.x += 1200

                if(building.bottom):
                    building.rect.y = random.randint(building_min, building_max)
                    score += 1
                else:
                    building.rect.y = buildings[building.index - 1].rect.y - building_image.get_height() - gap
        
        ground_x -= 5
        if(ground_x < -128):
            ground_x = 0

        
        
        if(background_x <= -background_image.get_width()):
            background_x = 0
        
        background_x -= 1

        score_surface = vga_font.render(str(score), False, (0, 0, 0))
        screen.blit(score_surface, score_surface.get_rect(midtop = (WIDTH / 2, 20)))

    elif(initalized):

        final_score = vga_large.render(str(score), False, (0, 0, 0))
        screen.blit(final_score, final_score.get_rect(center = (WIDTH / 2, HEIGHT / 2)))

    pygame.display.update()
    clock.tick(FPS)
