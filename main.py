import math
import sys
from random import randint, choice

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk_1 = pygame.image.load("graphics/player_walk_1.png").convert_alpha()
        self.walk_2 = pygame.image.load("graphics/player_walk_2.png").convert_alpha()
        self.jump_image = pygame.image.load("graphics/player_jump.png").convert_alpha()
        self.player_walk = [self.walk_1, self.walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.speed = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def animate_player(self):
        if self.rect.bottom < 300:
            self.image = self.jump_image
        else:
            self.player_index = (0.1+self.player_index)%len(self.player_walk)
            self.image = self.player_walk[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.speed = -20
            self.jump_sound.play()
             
    def apply_gravity(self):
        self.speed += 1
        self.rect.y += self.speed
        if self.rect.bottom > 300:
            self.rect.bottom = 300
            self.speed = 0
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate_player()
        

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "snail":
            snail_1 = pygame.image.load("graphics/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        else:
            fly_1 = pygame.image.load("graphics/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
    def animation_state(self):
        self.animation_index = (self.animation_index+0.1)%len(self.frames)
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def move(self):
        self.rect.x -= 7

    def update(self):
        self.animation_state()
        self.move()
        self.destroy()


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        game_over_sound.play()
        pygame.time.wait(1000)
        return False
    return True


def display_score():
    score = (pygame.time.get_ticks() - start_time) // 100
    score_surface = font.render(f"{score}", False, "Black")
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return score


def display_high_score():
    high_score_surface = font.render(f"Best: {high_score}", False, "Black")
    high_score_rect = high_score_surface.get_rect(midleft=(10, 25))
    screen.blit(high_score_surface, high_score_rect)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Runner")
clock = pygame.time.Clock()
run = True
game_active = True
start_time = 0
high_score = 0
score = 0
count = 0
play_sound = False
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play(loops=-1)


# Sprite groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Background and sounds
font = pygame.font.Font("font/Pixeltype.ttf", 50)
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/Ground.png").convert()
game_over_sound = pygame.mixer.Sound("audio/game_over.mp3")
game_over_sound.set_volume(0.5)

# Intro screen
start_surface = font.render("Press any key to start!", False, ("black"))
start_rect = start_surface.get_rect(center=(400, 325))

game_name_surface = font.render("Pixel Runner", False, "black")
game_name_rect = game_name_surface.get_rect(center=(400, 50))

player_stand_surface = pygame.image.load("graphics/player_stand.png").convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 2)
player_stand_rect = player_stand_surface.get_rect(center=(400, 190))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            # Spawn obstacles
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly","snail","snail","snail"])))

        else:
            # Restart
            if event.type == pygame.KEYDOWN:
                play_sound = True
                game_active = True
                start_time = pygame.time.get_ticks()
                high_score = max(high_score, score)

    if game_active:
        # Background
        play_sound = True
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        display_high_score()

        # Player
        player.draw(screen)
        player.update()
        
        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collisions
        game_active = collision_sprite()

    else:
        
        # Start screen
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        screen.blit(player_stand_surface, player_stand_rect)
        screen.blit(game_name_surface, game_name_rect)
        new_record_surface = font.render(f"Best: {score}", False, ("black"))
        new_record_rect = new_record_surface.get_rect(topright=(790, 20))
        screen.blit(new_record_surface, new_record_rect)
        score_msg_surface = font.render(f"Your Score: {score}", False, "black")
        score_msg_rect = score_msg_surface.get_rect(center=(400, 370))
        screen.blit(score_msg_surface, score_msg_rect)

    pygame.display.update()
    clock.tick(60)
