import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface(size=(40,40))
        self.image.fill((250,250,250))
        self.rect = self.image.get_rect(center=pos)

    def playerMovement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT]:
            self.rect.centerx -= 10
        if keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_LEFT]:
            self.rect.centerx += 10
        if keys_pressed[pygame.K_UP] and not keys_pressed[pygame.K_DOWN]:
            self.rect.centery -= 10
        if keys_pressed[pygame.K_DOWN] and not keys_pressed[pygame.K_UP]:
            self.rect.centery += 10

