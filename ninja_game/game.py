import os
import pygame
import random
import math
from sys import exit
from scripts.entities import Player, Enemy
from scripts.utils import load_img, load_imgs, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.sparks import Spark
from scripts.checkpoint_flag import Checkpoint

class Game():
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Ninja Game')
        self.screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320,240))
        self.clock = pygame.time.Clock()

        self.movement = [False, False]
        self.assets = {
            'player':load_img('entities/player.png'),
            'decor':load_imgs('tiles/decor'),
            'large_decor':load_imgs('tiles/large_decor'),
            'grass':load_imgs('tiles/grass'),
            'stone':load_imgs('tiles/stone'),
            'background':load_img('background.png'),
            'clouds':load_imgs('clouds'),
            'enemy/idle': Animation(load_imgs('entities/enemy/idle'), img_dur = 6),
            'enemy/run': Animation(load_imgs('entities/enemy/run'), img_dur = 4),
            'player/idle': Animation(load_imgs('entities/player/idle'), img_dur = 6),
            'player/run': Animation(load_imgs('entities/player/run'), img_dur = 4),
            'player/jump': Animation(load_imgs('entities/player/jump')),
            'player/slide': Animation(load_imgs('entities/player/slide')),
            'player/wall_slide':Animation(load_imgs('entities/player/wall_slide')),
            'flag': Animation(load_imgs('tiles/flag'),img_dur = 10,loop=True),
            'particle/leaf':Animation(load_imgs('particles/leaf'), img_dur = 20, loop=False),
            'particle/particle':Animation(load_imgs(path='particles/particle'), img_dur=6, loop=False),
            'projectile':load_img('projectile.png'),
            'gun':load_img('gun.png')
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('ninja_game/data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('ninja_game/data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('ninja_game/data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('ninja_game/data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('ninja_game/data/sfx/ambience.wav'),
        }

        self.sfx['ambience'].set_volume(0.3)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.8)

        self.player = Player(self,(50,50),(8,15))
        self.tilemap = Tilemap(self, tile_size = 16)
        self.clouds = Clouds(self.assets['clouds'])

        self.level = 0
        self.load_level(self.level)
        self.screenshake = 0
        self.hit_count = 0

    def load_level(self, map_id):
        self.tilemap.load('ninja_game/data/maps/' + str(map_id) + '.json')
        self.leaf_spawners = list()
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        self.particles = []

        self.projectiles = []

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.checkpoints = []
        for flag in self.tilemap.extract([('flag', 0)], keep=False):
            self.checkpoints.append(Checkpoint(self, flag['pos']))

        self.sparks = []
        self.scroll = [0,0]
        self.dead = 0
        self.transition = -30

    def load_from_checkpoint(self):
        checkpoints_cpy = self.checkpoints.copy()
        loaded_from_checkpoint = False
        checkpoints_cpy.reverse()

        for checkpoint in checkpoints_cpy:
            if checkpoint.is_visited:
                loaded_from_checkpoint = True
                self.player.pos[0] = checkpoint.pos[0]
                self.player.pos[1] = checkpoint.pos[1] 
                self.dead = 0
                self.transition = -30
                break
        
        if not loaded_from_checkpoint:
            self.load_level(self.level)

    def run(self):
        pygame.mixer.music.load('ninja_game/data/music.wav')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        self.sfx['ambience'].play(-1)

        while True:
            self.display.blit(self.assets['background'], (0,0))

            self.screenshake = max(self.screenshake - 1, 0)

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('ninja_game/data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    if len(self.checkpoints):
                        self.load_from_checkpoint()
                    else:
                        self.load_level(self.level)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0]) / 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1]) / 10
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1,0.3], frame=random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for checkpoint in self.checkpoints:
                checkpoint.update()
                checkpoint.render(self.display, offset=render_scroll)

            for enemy in self.enemies:
                kill = enemy.update(self.tilemap, (0,0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0],0))
                self.player.render(self.display, offset=render_scroll)

            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1 
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.sfx['hit'].play()
                        self.hit_count += 1
                        if self.hit_count >= 3:
                            self.dead += 1
                            self.hit_count = 0
                        self.screenshake = max(16, self.screenshake)
                        for i in range(20):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle = angle, speed=speed))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, [math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], random.randint(0,7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                   particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        if self.player.jump():
                            self.sfx['jump'].play
                    if event.key == pygame.K_x:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2 ,self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0,0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)

Game().run()