import pygame
from sys import exit
from random import randint

def score():
    curr_score = int(pygame.time.get_ticks()/100)
    return curr_score

def obstacle_movement(obstacle_rect_array):
    if obstacle_rect_array:
        for obstacle in obstacle_rect_array:
            screen.blit(enemy_surface,obstacle)
            obstacle.x -= 8
        obstacle_rect_array = [obstacle for obstacle in obstacle_rect_array if obstacle.x > -100]
        return obstacle_rect_array
    else:
        return []
    
def collision(test_rect,obstacle_rect_array):
    if obstacle_rect_array:
        for obstacle in obstacle_rect_array:
            if test_rect.colliderect(obstacle):
                return False
    return True

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 400:
        player_surf = player_walk_list[0]
    else:
        player_index += 0.12
        if player_index >= len(player_walk_list): player_index = 0
        player_surf = player_walk_list[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption('Dash')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 30)

background_surface = pygame.image.load('D:/Downloads/Unity Game Development Course Stuff/meadow-with-pond-conifers-hills-night/background.jpg').convert_alpha()
background_rect = background_surface.get_rect(midbottom = (400,400))


player_walk_1 = pygame.image.load('D:/Downloads/Unity Game Development Course Stuff/game-character-viking-walk-jump-cycle-sequence/character_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('D:/Downloads/Unity Game Development Course Stuff/game-character-viking-walk-jump-cycle-sequence/character_walk_2.png').convert_alpha()
player_walk_3 = pygame.image.load('D:/Downloads/Unity Game Development Course Stuff/game-character-viking-walk-jump-cycle-sequence/character_walk_3.png').convert_alpha()
player_walk_4 = pygame.image.load('D:/Downloads/Unity Game Development Course Stuff/game-character-viking-walk-jump-cycle-sequence/character_walk_4.png').convert_alpha()
player_walk_5 = pygame.image.load('D:/Downloads/Unity Game Development Course Stuff/game-character-viking-walk-jump-cycle-sequence/character_walk_5.png').convert_alpha()
player_walk_list = [player_walk_1,player_walk_2,player_walk_3,player_walk_4,player_walk_5]
player_index = 0
player_surf = player_walk_list[player_index]
player_rect = player_surf.get_rect(midbottom = (100,400))


ground_surface = pygame.image.load('D:/Downloads/Unity Game Development Course Stuff/meadow-with-pond-conifers-hills-night/ground_cropped.jpg').convert()
ground_rect = ground_surface.get_rect(midtop = (400,400))

enemy_surface = pygame.Surface((100,80))
enemy_rect = enemy_surface.get_rect(midbottom=(900,400))

gameover_font = pygame.font.Font(None, 80)
gameover_surface = gameover_font.render('Game Over',False,"White")
gameover_rect = gameover_surface.get_rect(center=(400,75))

gravity = 0
score_disp = 0
total_time = 0

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

obstacle_rect_array = []
game_on = True

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_on == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 400: 
                    gravity = -20
            
            if event.type == obstacle_timer:
                obstacle_rect_array.append(enemy_surface.get_rect(midbottom = (randint(900,1100),400)))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    enemy_rect.x = 900 
                    game_on = True
                    total_time = score()

    if game_on == True:
        screen.blit(background_surface,background_rect)
        screen.blit(ground_surface,ground_rect)
        player_animation()
        screen.blit(player_surf,player_rect)

        score_disp = score() - total_time
        score_surface = test_font.render(f'Score: {score_disp}',False,"White")
        score_rect = score_surface.get_rect(center=(400,75))
        screen.blit(score_surface,score_rect)

        obstacle_rect_array = obstacle_movement(obstacle_rect_array)

        gravity += 1
        player_rect.bottom += gravity
        if gravity > 1e3: gravity = 1e3

        if player_rect.bottom >= 400: player_rect.bottom = 400

        if collision(player_rect,obstacle_rect_array) == False:
            game_on = False
            obstacle_rect_array = []
    
    else:
        screen.fill("Grey")
        
        screen.blit(gameover_surface,gameover_rect)
        player_rect.midbottom = (100,400)
        gravity = 0

        score_surface = test_font.render(f'Your score: {score_disp}',False,"Black")
        score_rect = score_surface.get_rect(center=(400,300))
        screen.blit(score_surface,score_rect)


    pygame.display.update()
    clock.tick(60)