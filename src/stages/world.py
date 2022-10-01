import random
from typing import Tuple
import json

import pygame

from src._types import Events
from src.load import load_assets
from src.player import Player
from src.spike import Spike
from src.enums import GameStates

pygame.font.init()


class WorldInitStage:
    def __init__(self, assets: dict):
        self.screen_size = assets["bg"].get_size()
        self.screen_rect = pygame.Rect(0, 0, *self.screen_size)
        self.score = -1

        self.next_state = None

        self.assets = assets

        spike_image = self.assets["spike_left"]
        side_rect_image = self.assets["side_rect_down"]
        # rotating some of the assets
        # (merging two dictionaries: loaded assets and new rotates assets)
        # using the unpacking operator (**) for backwards compatibility
        self.assets = {
            **self.assets,
            **{
                "spike_right": pygame.transform.flip(spike_image, True, False),
                "spike_up": pygame.transform.rotate(spike_image, 90),
                "spike_down": pygame.transform.rotate(spike_image, 270),
                "side_rect_up": pygame.transform.flip(side_rect_image, False, True),
            },
        }
        self.spike_size = self.assets["spike_left"].get_size()


class BackgroundStage(WorldInitStage):
    def __init__(self, assets: dict):
        super().__init__(assets)

        # the rects at the top and bottom of the screen
        side_rect_height = self.assets["side_rect_down"].get_height()
        self.side_rects = (
            pygame.Rect(0, 0, self.screen_size[0], side_rect_height),
            pygame.Rect(
                0, self.screen_size[1] - side_rect_height, self.screen_size[0], side_rect_height
            ),
        )

    def draw(self, screen: pygame.Surface):
        screen.blit(self.assets["bg"], (0, 0))

        screen.blit(self.assets["side_rect_down"], self.side_rects[0])
        screen.blit(self.assets["side_rect_up"], self.side_rects[1])


class UIStage(BackgroundStage):
    def __init__(self, assets: dict):
        super().__init__(assets)
        self.score_font = pygame.font.Font("assets/gfx/Montserrat-ExtraLight.ttf", 186)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)

        score_text = self.score_font.render(f"{self.score}", True, (51, 57, 65))
        score_rect = score_text.get_rect(center=self.screen_rect.center)
        screen.blit(score_text, score_rect)


class PlayerStage(UIStage):
    def __init__(self, assets: dict):
        super().__init__(assets)

        self.player = Player(self.screen_rect.center, self.assets)

    def update(self, events: Events):
        self.player.update(events, self.screen_size)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)

        self.player.draw(screen)


class SpikeStage(PlayerStage):
    SPIKE_AMOUNT = 10

    def __init__(self, assets: dict):
        super().__init__(assets)

        static_spike_amount = self.screen_size[0] // self.spike_size[0]

        self.top_static_spikes = [
            Spike(
                (n * self.spike_size[1], self.side_rects[0].bottom),
                self.assets["spike_up"],
            )
            for n in range(static_spike_amount)
        ]
        self.bottom_static_spikes = [
            Spike(
                (n * self.spike_size[1], self.side_rects[1].top - self.spike_size[0]),
                self.assets["spike_down"],
            )
            for n in range(static_spike_amount)
        ]

        # the range of the y coordinates that spikes can get spawned on
        spike_vertical_range = (
            self.top_static_spikes[0].rect.bottom,
            self.bottom_static_spikes[0].rect.top,
            self.spike_size[1],  # step
        )
        # the y coordinates that spikes can get spawned on
        self.spike_vertical_coordinates = [y for y in range(*spike_vertical_range)]

        self.old_player_vel = pygame.Vector2()

    def generate_spikes(self):
        self.spikes = []
        for _ in range(self.SPIKE_AMOUNT):
            y = random.choice(self.spike_vertical_coordinates)
            new_spikes = (
                Spike(
                    (0, y),
                    self.assets["spike_right"],
                    facing_right=True,
                    move_to_pos=True,
                ),
                Spike(
                    (self.screen_size[0] - self.spike_size[0], y),
                    self.assets["spike_left"],
                    facing_right=False,
                    move_to_pos=True,
                ),
            )

            # the area around the player that spikes shouldn't spawn in
            player_area = pygame.Rect(
                0,
                self.player.rect.centery,
                self.screen_size[0],
                self.spike_size[1] * 1.5,
            )

            for spike in new_spikes:
                if spike.rect.colliderect(player_area):
                    player_colliding = True
                    break
                player_colliding = False

            if not player_colliding:
                self.spikes += new_spikes

    def update(self, events: Events):
        super().update(events)

        # if the player changed its direction:
        if int(self.old_player_vel.x) != int(self.player.vel.x):
            self.generate_spikes()
            self.score += 1
            self.player.speed *= 1.01
            self.player.gravity /= 1.01

        self.old_player_vel = self.player.vel.copy()

        self.next_state = None
        for spike in self.spikes + self.top_static_spikes + self.bottom_static_spikes:
            spike.update(events)

            if spike.rect.colliderect(self.player.rect):
                if spike.get_collision(self.player.mask, self.player.rect) is not None:
                    self.save()
                    self.next_state = GameStates.MENU

    def save(self):
        with open("assets/save.json", "r") as f:
            data = json.load(f)

        if self.score > data["high_score"]:
            data["high_score"] = self.score
        data["sum_score"] += self.score

        with open("assets/save.json", "w") as f:
            json.dump(data, f)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)

        for spike in self.spikes + self.top_static_spikes + self.bottom_static_spikes:
            spike.draw(screen)


class World(SpikeStage):
    pass
