class Checkpoint:
    def __init__(self, game, pos):
        self.game = game
        self.pos = list(pos)
        self.animation = self.game.assets['flag'].copy()

    def update(self):
        self.animation.update()

    def render(self, surf, offset=(0,0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))