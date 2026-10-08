import random
import pygame

# Item kinds
GOOD = "fruit"      # catch it: +1 score, miss it: -1 life
ROTTEN = "rotten"   # catch it: score penalty, miss it: nothing
BOMB = "bomb"       # catch it: lose a life, miss it: nothing


class Fruit:
    def __init__(self, screen_width, kind=None, speed_boost=0.0):
        self.screen_width = screen_width
        self.radius = 14
        self.x = random.randint(30, screen_width - 30)
        self.y = -self.radius * 2
        self.speed = random.uniform(4.0, 6.5) + speed_boost   # harder as score climbs

        # Roughly 70% good fruit, 15% rotten fruit, 15% bombs
        if kind is None:
            kind = random.choices([GOOD, ROTTEN, BOMB], weights=[70, 15, 15])[0]
        self.kind = kind

        if self.kind == ROTTEN:
            self.color = (105, 125, 45)   # sickly green-brown
        elif self.kind == BOMB:
            self.color = (35, 35, 40)     # dark grey/black
        else:
            self.color = random.choice([
                (230, 45, 45),   # Apple
                (245, 140, 30),  # Orange
                (160, 60, 200),  # Grape
            ])

    @property
    def is_hazard(self):
        return self.kind != GOOD

    def update(self):
        self.y += self.speed

    def is_missed(self, screen_height):
        return self.y > screen_height

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def render(self, surface):
        cx, cy = int(self.x), int(self.y)
        center = (cx, cy)

        if self.kind == BOMB:
            pygame.draw.circle(surface, self.color, center, self.radius)
            pygame.draw.circle(surface, (200, 60, 60), center, self.radius, width=2)
            pygame.draw.circle(surface, (120, 120, 130), (cx - 4, cy - 4), 3)
            # fuse and spark
            pygame.draw.line(surface, (190, 170, 120), (cx + 4, cy - self.radius + 2), (cx + 9, cy - self.radius - 6), 3)
            pygame.draw.circle(surface, (255, 190, 40), (cx + 9, cy - self.radius - 7), 4)
        elif self.kind == ROTTEN:
            pygame.draw.circle(surface, self.color, center, self.radius)
            # dark rot spots
            pygame.draw.circle(surface, (60, 45, 25), (cx - 4, cy + 3), 4)
            pygame.draw.circle(surface, (60, 45, 25), (cx + 5, cy - 2), 3)
            pygame.draw.circle(surface, (60, 45, 25), (cx + 2, cy + 7), 2)
        else:
            pygame.draw.circle(surface, self.color, center, self.radius)
            pygame.draw.circle(surface, (255, 255, 255), (cx - 4, cy - 4), 3)
