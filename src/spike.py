from typing import Sequence

import pygame

from src._types import Events


class Spike:
    SPEED = 1

    def __init__(
        self,
        pos: Sequence,
        image: pygame.Surface,
        facing_right: bool = True,
        move_to_pos=False,
    ):
        self.move_to_pos = move_to_pos
        if move_to_pos:
            width = image.get_width()
            starting_x = pos[0] - width if facing_right else pos[0] + width
            self.final_pos = pygame.Vector2(pos)

            self.rect = image.get_rect(topleft=(starting_x, pos[1]))
            self.pos = pygame.Vector2(self.rect.topleft)

        self.rect = image.get_rect(topleft=pos)

        self.mask = pygame.mask.from_surface(image)
        self.image = image

    def update(self, events: Events):
        if self.move_to_pos:
            self.pos.move_towards_ip(self.final_pos, self.SPEED * events["delta_time"])
            if self.pos.x != self.final_pos.x:
                self.rect.topleft = self.pos

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def get_collision(self, mask: pygame.Mask, rect: pygame.Rect):
        return self.mask.overlap(mask, (rect.x - self.rect.x, rect.y - self.rect.y))

    def __repr__(self):
        return f"<Spike at {self.rect.topleft}>"
