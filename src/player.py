from typing import Tuple

import pygame

from src._types import Events, Position


class Player:
    def __init__(self, center: Position):
        self.image = pygame.Surface((18, 18))
        self.image.fill((6, 6, 8))

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=center)
        self.pos = pygame.Vector2(self.rect.topleft)

        self.speed = 3
        self.jump_height = -5
        self.vel = pygame.Vector2(self.speed, self.jump_height)
        self.gravity = 0.125

    def render_input(self, events: Events):
        for event in events["events"]:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_SPACE):
                    self.vel.y = self.jump_height

        self.vel.y += self.gravity * events["delta_time"]

    def move(self, events: Events, screen_size: Tuple[int]):
        delta_time = events["delta_time"]

        if self.rect.left <= 0:
            self.vel.x = self.speed
        elif self.rect.right >= screen_size[0]:
            self.vel.x = -self.speed

        self.pos.x += self.vel.x * delta_time
        self.rect.x = round(self.pos.x)

        self.pos.y += self.vel.y * delta_time
        self.rect.y = round(self.pos.y)

    def update(self, events: Events, screen_size: Tuple[int]):
        self.render_input(events)
        self.move(events, screen_size)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.pos)
