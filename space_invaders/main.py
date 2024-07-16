import pygame
from sys import exit
import random
from enemy import Enemy
from player import Player
from bullets import Bullets

pygame.init()

screen = pygame.display.set_mode((800,800))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

#Background of the game
background_surface = pygame.Surface(size=(800,800))
background_rect = background_surface.get_rect(topleft = (0,0))
background_surface.fill((32,35,32))

#Creating the player and enemy instances
player = Player((400,700))
player_score = 0
enemies = []
enemies_sprites = pygame.sprite.Group()
for i in range(0,7):
    for j in range (1,6):
        enemy = Enemy((120+90*i,75*j))
        enemies.append(enemy)
        enemies_sprites.add(enemy)

#Adding them in a sprite group
entities = pygame.sprite.Group()
entities.add(player)
for enemy in enemies:
    entities.add(enemy)

#Array for storing enemy and player bullets
enemy_bullets = []
player_bullets = []

# Game on toggle (off if the player dies)
game_on = True
total_lives = 2

#Creating an event for enemy bullets
enemy_bullet_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_bullet_timer,300)

#Game over screen
game_over_surface = pygame.Surface(size=(800,800))
game_over_surface.fill('White')
game_over_rect = game_over_surface.get_rect(topleft=(0,0))

gameover_font = pygame.font.Font(None, 80)
gameover_text_surface = gameover_font.render('Game Over',False,"Black")
gameover_text_rect = gameover_text_surface.get_rect(center=(400,150))

score_font = pygame.font.Font(None, 40)

#Game main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_on:
            if event.type == enemy_bullet_timer:
                random_enemy = enemies[random.randint(0,len(enemies) - 1)]
                enemy_bullets.append(Bullets((random_enemy.rect.centerx,random_enemy.rect.centery+35),False))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_bullets.append(Bullets((player.rect.centerx,player.rect.centery-35),True,-9))
    
    player.playerMovement()


    if game_on:
        #Draw the background, player and enemies on the screen
        screen.blit(background_surface,background_rect)
        entities.draw(screen)

        enemies_sprites.update()
        for bullet in enemy_bullets:
            screen.blit(bullet.image,bullet.rect)
            bullet.move()

        for bullet in player_bullets:
            screen.blit(bullet.image,bullet.rect)
            bullet.move()

        for enemy_bullet in enemy_bullets:
            if (player.rect.colliderect(enemy_bullet.rect)):
                if(total_lives == 0):
                    game_on = False
                else:
                    total_lives -= 1
                    enemy_bullet.rect.centery = 850

        for enemy in enemies:
            for player_bullet in player_bullets:
                if (player_bullet.rect.colliderect(enemy.rect)):
                    entities.remove(enemy)
                    enemies_sprites.remove(enemy)
                    enemies = [e for e in enemies if e != enemy]
                    player_bullets = [p for p in player_bullets if p != player_bullet]
                    player_score += 100
                    
        enemy_bullets = [bullet for bullet in enemy_bullets if bullet.ypos() < 800]
        player_bullets = [bullet for bullet in player_bullets if bullet.ypos() > 0]

    else:
        screen.blit(game_over_surface,game_over_rect)
        screen.blit(gameover_text_surface, gameover_text_rect)
        score_text_surface = score_font.render(f'Player Score: {player_score}',False,"Black")
        score_text_rect = score_text_surface.get_rect(center=(350,350))
        screen.blit(score_text_surface,score_text_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_on = True

    pygame.display.update()
    clock.tick(60)
