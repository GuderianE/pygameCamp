import pygame
import time
from pygame.locals import * # type: ignore
from worldBuilder import buildWorldMatrix

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

asset_path = 'assets/images/'
animation_path = 'assets/animations/'
tile_size = 50

sun_image = pygame.image.load(asset_path + 'sun.png')
bg_image = pygame.image.load(asset_path + 'bg.png')

bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))


class Door():
    def __init__(self, x, y, width, height, image_list):
        self.image_list = image_list
        self.image = image_list[0]
        self.image = pygame.transform.scale(image_list[0], (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_open = False
        
    def open(self):
        self.is_open = True
        self.update()
        
    def close(self):
        self.is_open = False
        self.update()
        
    def update(self):
        if self.is_open:
            self.image = pygame.transform.scale(self.image_list[1], (self.rect.width, self.rect.height))
        else:
            self.image = pygame.transform.scale(self.image_list[0], (self.rect.width, self.rect.height))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        

class Button():
    def __init__(self, image, x, y, text, font):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.text = text
        self.font = font
        self.render_text()
        
    def render_text(self):
        self.image = self.image.copy()
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # White color
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surface, text_rect.topleft)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self):
        screen.blit(self.image, self.rect.center)
        

class MovingTile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, direction, speed, distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.start_y = y
        self.direction = direction
        self.speed = speed
        self.distance = distance
        self.move_counter = 0

    def update(self):
        if self.direction == 'horizontal':
            self.rect.x += self.speed
            self.move_counter += abs(self.speed)
            if self.move_counter >= self.distance:
                self.speed *= -1
                self.move_counter = 0
        elif self.direction == 'vertical':
            self.rect.y += self.speed
            self.move_counter += abs(self.speed)
            if self.move_counter >= self.distance:
                self.speed *= -1
                self.move_counter = 0


class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.health = 3
        self.index = 0
        self.counter = 0
        self.direction = 1
        self.is_death = False
        self.game_state = "running"
        self.death_img = pygame.image.load(asset_path + 'ghost.png') 
        
        
        for num in range(12):
            img_right = pygame.image.load(animation_path + f'walk/p2_walk{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_left.append(img_left)
            self.images_right.append(img_right)
                    
        if self.direction == 1:
            self.image = self.images_right[self.index]
        if self.direction == -1:
            self.image = self.images_left[self.index]
                    
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.on_moving_tile = None
        
    def is_on_ground(self):
         self.rect.y += 1
         on_ground = False
         for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                on_ground = True 
                break
         for tile in moving_tile_group:
            if tile.rect.colliderect(self.rect):
                self.on_moving_tile = tile
                on_ground = True
                break
         else:
            self.on_moving_tile = None
         self.rect.y -= 1
         return on_ground
        
    def update(self):
        dx = 0
        dy = 0
        
        if self.health > 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 5
                self.direction = -1
                self.index += 1
                if self.index >= len(self.images_left):
                    self.index = 0
                self.image = self.images_left[self.index]
            if key[pygame.K_RIGHT]:
                dx += 5
                self.direction = 1
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                self.image = self.images_right[self.index]
                
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                    
            if key[pygame.K_SPACE] and self.jumped == False and self.is_on_ground():
                self.vel_y = -15
                self.jumped = True
                    
            if key[pygame.K_SPACE] == False and self.is_on_ground():
                self.jumped = False
        
        if self.health <= 0 and not self.is_death:
            img = self.death_img
            self.image = pygame.transform.scale(img, (tile_size, tile_size))
            self.is_death = True
            
        if self.is_death == True:
            self.vel_y -= 2
            if self.rect.y * -1 > screen_height:
                self.game_state = "lost"
            
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10  
        dy += self.vel_y
        
        for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height) and self.is_death == False:
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height) and self.is_death == False:
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y += 1
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

        for tile in moving_tile_group:
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height) and self.is_death == False:
                dx = 0
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height) and self.is_death == False:
                if self.vel_y < 0:
                    dy = tile.rect.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile.rect.top - self.rect.bottom
                    self.vel_y = 0
        
        # if world.door_array[0].rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height) and self.is_death == False:
        #     world.door_array[0].open()
        #     self.game_state = "won"
                    
        if pygame.sprite.spritecollide(self, blob_group, False):
            self.health -= 1
        if pygame.sprite.spritecollide(self, lava_group, False):
            self.health -= 1
            
        self.rect.x += dx
        self.rect.y += dy
        
        if self.is_death == False:    
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel_y = 0
            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                self.vel_y = 0
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_width:
                self.rect.right = screen_width
        
        if self.on_moving_tile:
            if self.on_moving_tile.direction == 'horizontal':
                self.rect.x += self.on_moving_tile.speed
            if self.on_moving_tile.direction == 'vertical':
                self.rect.y += self.on_moving_tile.speed
            
        
        screen.blit(self.image, self.rect)
        
        
class World():
    def __init__(self, data):
        self.tile_list = []
        self.door_list = []
        self.door_array = []
        
        dirt_image = pygame.image.load(asset_path + 'brick.png')
        grass_img = pygame.image.load(asset_path + 'grass.png')
        moving_tile_img = pygame.image.load(asset_path + 'grass.png')
        door_closed_img = pygame.image.load(asset_path + 'door_closed.png')
        door_open_img = pygame.image.load(asset_path + 'door_open.png')
        self.door_list.append(door_closed_img)
        self.door_list.append(door_open_img)
        
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
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size 
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 4:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 5:
                     moving_tile = MovingTile(col_count * tile_size, row_count * tile_size, tile_size, tile_size, moving_tile_img, 'horizontal', 2, 100)
                     moving_tile_group.add(moving_tile)
                if tile == 6: 
                    moving_tile = MovingTile(col_count * tile_size, row_count * tile_size, tile_size, tile_size, moving_tile_img, 'vertical', 2, 100)
                    moving_tile_group.add(moving_tile)
                if tile == 7:
                    door = Door(col_count * tile_size - 25, row_count * (tile_size // 2) + 15, tile_size * 2, tile_size * 2, self.door_list)
                    self.door_array.append(door)
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        for door in self.door_array:
            door.draw(screen)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(asset_path + 'slime.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
            
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(asset_path + 'lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    

blocktuple = [(2, 5, 3), (3, 11, 10), (7, 18, 2), (5, 5, 10), (4, 9, 16), (6, 15, 3), (5, 8, 6), (4, 10, 16), (4, 11, 16), (4, 12, 16), (4, 13, 16), (3, 14, 10), (2, 17, 3), (2, 18, 3), (2, 10, 4), (2, 11, 4), (2, 12, 5), (2, 13, 5), (2, 4, 6), (2, 5, 6), (2, 6, 6), (2, 1, 7), (2, 2, 9), (2, 3, 10), (2, 9, 11), (2, 10, 11), (2, 11, 11), (2, 12, 11), (2, 13, 11), (2, 14, 11), (2, 15, 11), (2, 17, 13), (2, 10, 15), (2, 12, 15), (2, 14, 15), (2, 15, 15), (2, 16, 15), (2, 17, 15), (2, 18, 15), (2, 6, 16), (2, 7, 16), (2, 8, 16), (1, 14, 16), (1, 15, 16), (1, 16, 16), (1, 17, 16), (1, 18, 16), (2, 5, 17), (1, 6, 17), (1, 7, 17), (1, 8, 17), (1, 9, 17), (1, 10, 17), (1, 11, 17), (1, 12, 17), (1, 13, 17), (1, 14, 17), (1, 15, 17), (1, 16, 17), (1, 17, 17), (1, 18, 17), (2, 4, 18), (1, 5, 18), (1, 6, 18), (1, 7, 18), (1, 8, 18), (1, 9, 18), (1, 10, 18), (1, 11, 18), (1, 12, 18), (1, 13, 18), (1, 14, 18), (1, 15, 18), (1, 16, 18), (1, 17, 18), (1, 18, 18), (1, 4, 19), (1, 5, 19), (1, 6, 19), (1, 7, 19), (1, 8, 19), (1, 9, 19), (1, 10, 19), (1, 11, 19), (1, 12, 19), (1, 13, 19), (1, 14, 19), (1, 15, 19), (1, 16, 19), (1, 17, 19), (1, 18, 19)]

world_data = buildWorldMatrix(int(screen_width / tile_size), int(screen_height / tile_size), blocktuple)

def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

player = Player(100, screen_height - 130)


button_image = pygame.image.load(asset_path + 'button.png')
button_image = pygame.transform.scale(button_image, (150, 50))
font = pygame.font.Font(None, 40)
button = Button(button_image, 425, 550, "Restart", font) 

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
moving_tile_group = pygame.sprite.Group()

world = World(world_data)

def reset_game():
    global player, blob_group, lava_group, moving_tile_group, world
    blob_group = pygame.sprite.Group()
    player = Player(100, screen_height - 130)   
    lava_group = pygame.sprite.Group()
    moving_tile_group = pygame.sprite.Group()
    world = World(world_data)


run = True
while run:
    
    clock.tick(fps)
    if player.game_state == "running":
        screen.blit(bg_image, (0, 0))
        screen.blit(sun_image, (100, 100))
        
        world.draw()
        draw_grid()
        
        blob_group.update()
        blob_group.draw(screen)
        lava_group.update()
        lava_group.draw(screen)
        moving_tile_group.update()
        moving_tile_group.draw(screen)
        
        player.update()
        
    if player.game_state == "won":
        button.draw()
        font = pygame.font.Font(None, 74)
        text = font.render("You Won", 1, (0, 255, 0))
        screen.blit(text, (400, 450))  # Adjust position as needed
        
    if player.game_state == "lost":
        button.draw()
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", 1, (255, 0, 0))
        screen.blit(text, (360, 450))  # Adjust position as needed
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
       
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press 'Escape' to quit
                    run = False
        if button.is_clicked(event):
                    reset_game()
                    player.game_state = "running"

    pygame.display.update()
    
pygame.quit()