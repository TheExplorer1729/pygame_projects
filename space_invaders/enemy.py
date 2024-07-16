import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface(size=(30,30))
        self.image.fill((100,100,100))
        self.rect = self.image.get_rect(center=pos)
        self.initial_x = self.rect.centerx
        self.initial_y = self.rect.centery
        self.increment = 0
        self.going_right = True
        self.going_left = False

    def update(self):
        self.increment += 0.002
        self.rect.centery = self.initial_y + (int(self.increment)*50)
        if(self.going_right):
            if(self.rect.centerx - self.initial_x < 80):
                self.rect.centerx += 1.5
            else:
                self.going_left = True
                self.going_right = False
        elif(self.going_left):
            if(self.initial_x -  self.rect.centerx < 80):
                self.rect.centerx -= 1.5
            else:
                self.going_left = False
                self.going_right = True
        
            
        
        
        

