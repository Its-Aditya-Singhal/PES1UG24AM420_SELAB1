import random
import pygame
from game.basket import Basket
from game.fruit import Fruit, GOOD, ROTTEN, BOMB
from game.particle import Particle

# Difficulty settings: every POINTS_PER_LEVEL points the game gets harder
BASE_SPAWN_DELAY = 750      # ms between spawns at the start
MIN_SPAWN_DELAY = 250       # spawn delay never goes below this
SPAWN_DELAY_STEP = 50       # ms removed from the delay each level
SPEED_STEP = 0.5            # extra falling speed added each level
MAX_SPEED_BOOST = 5.0       # cap so the game stays playable
POINTS_PER_LEVEL = 5

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.basket = Basket(width, height)
        self.fruits = []
        self.particles = []

        self.score = 0
        self.lives = 3
        self.level = 0
        self.speed_boost = 0.0
        self.spawn_delay = BASE_SPAWN_DELAY
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def update(self):
        self.update_particles()

        if self.game_state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        self.update_difficulty()

        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.spawn_delay:
            self.fruits.append(Fruit(self.width, speed_boost=self.speed_boost))
            self.last_spawn_time = now

        basket_rect = self.basket.rect
        for fruit in self.fruits[:]:
            fruit.update()

            if basket_rect.colliderect(fruit.rect):
                self.spawn_splash(fruit, self.basket.y)
                if fruit.kind == GOOD:
                    self.score += 1
                elif fruit.kind == ROTTEN:
                    self.score = max(0, self.score - 2)   # rotten fruit: score penalty
                elif fruit.kind == BOMB:
                    self.lives -= 1                       # bomb: lose a life
                    if self.lives <= 0:
                        self.lives = 0
                        self.game_state = "GAME_OVER"

                self.fruits.remove(fruit)
                if self.game_state == "GAME_OVER":
                    break
                continue

            if fruit.is_missed(self.height):
                self.spawn_splash(fruit, self.height - 25)
                self.fruits.remove(fruit)
                if fruit.is_hazard:
                    continue   # letting rotten fruit / bombs fall is safe
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                    self.game_state = "GAME_OVER"
                    break

    def spawn_splash(self, fruit, y):
        """Emit coloured droplets at (fruit.x, y) - used on basket catches and floor hits."""
        if fruit.kind == BOMB:
            colors = [(255, 150, 40), (255, 90, 40), (110, 110, 110)]   # explosion sparks
        else:
            colors = [fruit.color]
        for _ in range(14):
            self.particles.append(Particle(fruit.x, y, random.choice(colors)))

    def update_particles(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.alive]

    def update_difficulty(self):
        """Shrink the spawn delay and raise the base falling speed as score climbs."""
        self.level = self.score // POINTS_PER_LEVEL
        self.spawn_delay = max(MIN_SPAWN_DELAY, BASE_SPAWN_DELAY - self.level * SPAWN_DELAY_STEP)
        self.speed_boost = min(MAX_SPEED_BOOST, self.level * SPEED_STEP)

    def reset(self):
        self.basket = Basket(self.width, self.height)
        self.fruits.clear()
        self.particles.clear()
        self.score = 0
        self.lives = 3
        self.level = 0
        self.speed_boost = 0.0
        self.spawn_delay = BASE_SPAWN_DELAY
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

    def render(self, screen):
        screen.fill((28, 32, 40))

        ground_y = self.height - 25
        pygame.draw.rect(screen, (45, 50, 60), (0, ground_y, self.width, 25))

        self.basket.render(screen)
        for fruit in self.fruits:
            fruit.render(screen)
        for particle in self.particles:
            particle.render(screen)

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (25, 20))

        level_surf = self.font_medium.render(f"Level: {self.level + 1}", True, (140, 200, 255))
        screen.blit(level_surf, (self.width // 2 - level_surf.get_width() // 2, 20))

        lives_surf = self.font_medium.render(f"Lives: {self.lives}", True, (240, 80, 80))
        screen.blit(lives_surf, (self.width - lives_surf.get_width() - 25, 20))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("GAME OVER", True, (235, 70, 70))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_medium.render(f"Final Score: {self.score}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_medium.render("Press [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))
