import math
import sys
from random import randint

import pygame


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump_surface
    else:
        player_index = (player_index + 0.1) % len(player_walk)
        player_surface = player_walk[int(player_index)]


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if obstacle_rect.colliderect(player):
                return False
    return True


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if obstacle_rect.right < 0:
                obstacle_list.remove(obstacle_rect)
            else:
                obstacle_rect.x -= obstacle_speed
                if obstacle_rect.bottom == 300:
                    screen.blit(snail_surface, obstacle_rect)
                else:
                    screen.blit(fly_surface, obstacle_rect)

        return obstacle_list
    else:
        return []


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
obstacle_speed = 7.5
player_speed = 0
start_time = 0
high_score = 0
score = 0
count = 0
play_sound = False

# Background
font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/Ground.png").convert()

jump_sound = pygame.mixer.Sound("audio/jump.mp3")
game_over_sound = pygame.mixer.Sound("audio/game_over.mp3")
bg_music = pygame.mixer.Sound("audio/music.wav")

# Obstacles
obstacle_rect_list = []

snail_1 = pygame.image.load("graphics/snail1.png").convert_alpha()
snail_2 = pygame.image.load("graphics/snail2.png").convert_alpha()
snail_walk = [snail_1, snail_2]
snail_index = 0
snail_surface = snail_walk[snail_index]
snail_rect = snail_surface.get_rect(bottomright=(600, 300))


fly_1 = pygame.image.load("graphics/Fly1.png").convert_alpha()
fly_2 = pygame.image.load("graphics/Fly2.png").convert_alpha()
fly_walk = [fly_1, fly_2]
fly_index = 0
fly_surface = fly_walk[fly_index]
fly_rect = fly_surface.get_rect(bottomright=(600, 200))

# Player
player_walk_1 = pygame.image.load("graphics/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump_surface = pygame.image.load("graphics/player_jump.png").convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(100, 300))

# Begin screen
start_surface = font.render("Press any key to start!", False, (111, 196, 169))
start_rect = start_surface.get_rect(center=(400, 325))

game_name_surface = font.render("Pixel Runner", False, "white")
game_name_rect = game_name_surface.get_rect(center=(400, 70))

player_stand_surface = pygame.image.load("graphics/player_stand.png").convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 2)
player_stand_rect = player_stand_surface.get_rect(center=(400, 200))


# Timer
# unique event value
obstable_timer = pygame.USEREVENT + 1
# sets an event to appear on event query every x ms
pygame.time.set_timer(obstable_timer, 1300)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

bg_music.play()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            # jump
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                player_speed = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    jump_sound.play()
                    player_speed = -20

            # add obstacle to list
            if event.type == obstable_timer:
                if randint(1, 10) < 7:
                    obstacle_rect_list.append(
                        snail_surface.get_rect(bottomright=(randint(900, 1100), 300))
                    )
                else:
                    obstacle_rect_list.append(
                        fly_surface.get_rect(bottomright=(randint(900, 1100), 200))
                    )

            # animate snail
            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_walk[snail_index]

            # animate fly
            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_walk[fly_index]

        else:
            # restart
            if event.type == pygame.KEYDOWN:
                play_sound = True
                game_active = True
                player_rect.midbottom = (100, 300)
                player_gravity = 0
                start_time = pygame.time.get_ticks()
                high_score = max(high_score, score)

    if game_active:
        # Background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        display_high_score()

        # Player
        player_speed += 1
        player_rect.y += player_speed
        if player_rect.bottom > 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Check collisions
        game_active = collisions(player_rect, obstacle_rect_list)

        # Increase speed
        # obstacle_speed = 5 + math.log(score + 0.01)
        # print(obstacle_speed)

    else:
        if play_sound:
            game_over_sound.play()
        play_sound = False
        pygame.time.wait(1000)
        obstacle_rect_list.clear()
        screen.fill((94, 129, 162))
        screen.blit(start_surface, start_rect)
        screen.blit(player_stand_surface, player_stand_rect)
        screen.blit(game_name_surface, game_name_rect)
        new_record_surface = font.render(f"Best: {score}", False, ("white"))
        new_record_rect = new_record_surface.get_rect(topright=(790, 20))
        screen.blit(new_record_surface, new_record_rect)
        score_msg_surface = font.render(f"Your Score: {score}", False, "white")
        score_msg_rect = score_msg_surface.get_rect(center=(400, 370))
        screen.blit(score_msg_surface, score_msg_rect)

    pygame.display.update()
    clock.tick(60)
