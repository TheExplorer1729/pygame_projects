import pygame

class Bullets(pygame.sprite.Sprite):
    def __init__(self,pos,is_player,bullet_speed = 9):
        super().__init__()
        self.image = pygame.Surface(size=(5,15))
        if not is_player:
            self.image.fill('Red')
        else:
            self.image.fill('Blue')
        self.rect = self.image.get_rect(center = pos)
        self.bullet_speed = bullet_speed

    def ypos(self):
        return self.rect.centery
    
    def move(self):
        self.rect.centery += self.bullet_speed