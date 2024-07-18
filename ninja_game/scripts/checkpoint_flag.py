class Checkpoint:
    def __init__(self, game, pos):
        self.game = game
        self.pos = list(pos)
        self.animation = self.game.assets['flag'].copy()
        self.is_visited = False

    def update(self):
        self.animation.update()

        if self.is_visited:
            frame_no = self.animation.frame
            self.animation = self.game.assets['green_flag'].copy()
            self.animation.frame = frame_no
            self.is_visited = False

    def render(self, surf, offset=(0,0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))