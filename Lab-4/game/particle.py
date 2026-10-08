import random
import pygame


class Particle:
    """A small splash droplet that flies out, falls with gravity and shrinks away."""

    GRAVITY = 0.35

    def __init__(self, x, y, color, upward=True):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3.5, 3.5)
        # droplets always shoot upward first, then gravity pulls them back down
        self.vy = random.uniform(-6.5, -2.0) if upward else random.uniform(-4.0, -1.0)
        self.max_life = random.randint(22, 40)   # frames
        self.life = self.max_life
        self.start_radius = random.uniform(2.5, 5.0)

    @property
    def alive(self):
        return self.life > 0

    def update(self):
        self.vy += self.GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def render(self, surface):
        # shrink as the droplet gets older, so it fades out smoothly
        radius = int(self.start_radius * (self.life / self.max_life))
        if radius >= 1:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)
