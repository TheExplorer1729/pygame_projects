import pygame
from sys import exit
import random

pygame.init()

screen = pygame.display.set_mode((800,700))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

background_surf = pygame.Surface(size = (800,700))
background_rect = background_surf.get_rect(topleft = (0,0))

player_surf = pygame.Surface(size = (20,120))
player_surf.fill('White')
player_rect = player_surf.get_rect(midleft = (10,400))

enemy_surf = pygame.Surface(size = (20,120))
enemy_surf.fill('White')
enemy_rect = enemy_surf.get_rect(midright = (790,400))

ball_surf = pygame.Surface(size = (20,20))
ball_rect = ball_surf.get_rect(center = (400,350))

player_score = 0
enemy_score = 0
text_font = pygame.font.Font(None,100)
player_score_text = text_font.render(f'{player_score}',False,'White')
player_score_text_rect = player_score_text.get_rect(center = (200,50))
enemy_score_text = text_font.render(f'{enemy_score}',False,'White')
enemy_score_text_rect = enemy_score_text.get_rect(center = (600,50))

direction = pygame.Vector2(random.random()*0.8 + 0.2,random.random()*0.8 + 0.2)
direction = direction.normalize()
speed = 18
enemy_speed = 0.15

game_on = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEMOTION:
            player_rect.centery = event.pos[1]
            
            if player_rect.top < 10:
                player_rect.top = 10
            elif player_rect.bottom > 690:
                player_rect.bottom = 690

    if game_on:
        screen.blit(background_surf,background_rect)
        screen.blit(player_surf,player_rect)
        pygame.draw.ellipse(screen,'White',ball_rect)
        screen.blit(enemy_surf,enemy_rect)

        ball_rect.x += direction.x * speed
        ball_rect.y += direction.y * speed

        if player_rect.colliderect(ball_rect) and ball_rect.left > player_rect.left:
            direction.x *= -1

        if enemy_rect.colliderect(ball_rect) and enemy_rect.left > ball_rect.left:
            direction.x *= -1

        if ball_rect.top < 10 or ball_rect.bottom > 690:
            direction.y *= -1

        # print((ball_rect.centery - enemy_rect.centery) * enemy_speed)
        if ball_rect.x > 0 and ball_rect.x < 800:
            enemy_rect.centery += (ball_rect.centery - enemy_rect.centery + random.random()) * enemy_speed

        if ball_rect.x < -400:
            ball_rect.center = (400,350)
            direction = pygame.Vector2(random.random()*0.8 + 0.2,random.random()*0.8 + 0.2)
            direction = direction.normalize()
            enemy_score += 1
        elif ball_rect.x > 1200:
            ball_rect.center = (400,350)
            direction = pygame.Vector2(random.random()*0.8 + 0.2,random.random()*0.8 + 0.2)
            direction = direction.normalize()
            player_score += 1

        player_score_text = text_font.render(f'{player_score}',False,'White')
        enemy_score_text = text_font.render(f'{enemy_score}',False,'White')
        screen.blit(player_score_text,player_score_text_rect)
        screen.blit(enemy_score_text,enemy_score_text_rect)
    
    pygame.display.update()
    clock.tick(60)