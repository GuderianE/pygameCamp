import pygame
from pygame.locals import *
import worldBuilder

pygame.init()

screen_width = 1000
Screen_height = 1000


screen = pygame.display.set_mode((screen_width, Screen_height))
pygame.display.set_caption('Platformer')

asset_path = 'assets/images/'
tile_size = 200

sun_image = pygame.image.load(asset_path + 'sun.png')
bg_image = pygame.image.load(asset_path + 'bg.png')

bg_image = pygame.transform.scale(bg_image, (screen_width, Screen_height))

class World():
    def __init__(self, data):
        self.title_list = []
        
        dirt_image = pygame.image.load(asset_path + 'brick.png')
        grass_img = pygame.image.load(asset_path + 'grass.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size 
                    tile = (img, img_rect)
                    self.title_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size 
                    tile = (img, img_rect)
                    self.title_list.append(tile)
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.title_list:
            screen.blit(tile[0], tile[1])
        

world_data = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 2, 2, 2, 1]
]

def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, Screen_height))

world = World(world_data)

run = True
while run:
    
    screen.blit(bg_image, (0, 0))
    screen.blit(sun_image, (100, 100))
    
    world.draw()
    draw_grid()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    
pygame.quit()