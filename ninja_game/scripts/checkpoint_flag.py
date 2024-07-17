class Checkpoint:
    def __init__(self, game, pos):
        self.game = game
        self.pos = list(pos)
        self.animation = self.game.assets['flag'].copy()
        self.is_visited = False

    def update(self):
        self.animation.update()
        dist = (self.game.player.pos[0] - self.pos[0]) + (self.game.player.pos[1] - self.pos[1])
        if abs(dist) < 2:
            self.is_visited = True

    def render(self, surf, offset=(0,0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))