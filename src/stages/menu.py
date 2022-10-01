import pygame

from src._types import Events
from src.enums import GameStates
from src.utils import fade_surface_in, fade_surface_out
from typing import Tuple
import json


class InitStage:
    def __init__(self, last_frame: pygame.Surface):
        self.screen_size = last_frame.get_size()
        self.last_game_frame = last_frame
        self.screen_rect = pygame.Rect(0, 0, *self.screen_size)

        self.next_state = None

        # fade in the fade surface, make buttons appearing
        self.animate_out = False


class BackgroundStage(InitStage):
    FADE_SPEED = 4
    FADE_SURFACE_MAX_ALPHA = 100
    TEXT_SURFACE_MAX_ALPHA = 255
    def __init__(self, last_frame: pygame.Surface):
        super().__init__(last_frame)

        self.fade_surface = pygame.Surface(self.screen_size)
        self.fade_surface_alpha = 0
        self.fade_surface.set_alpha(self.fade_surface_alpha)

        # surface that contains all the text
        self.text_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)

        title_font = pygame.font.Font("assets/gfx/Montserrat-ExtraLight.ttf", 21)
        title_surf = title_font.render(
            "Don't collide with the triangular objects", True, "white"
        )
        title_rect = title_surf.get_rect(
            midtop=(self.screen_rect.centerx, self.screen_rect.centery / 15)
        )
        instruction_surf = title_font.render("Press Space to start", True, "white")
        instruction_rect = instruction_surf.get_rect(
            midtop=(self.screen_rect.centerx, self.screen_rect.centery / 6)
        )

        with open("assets/save.json", "r") as f:
            data = json.load(f)

        high_score_surf = title_font.render(
            f"Highest score: {data['high_score']}", True, "white"
        )
        high_score_rect = high_score_surf.get_rect(midleft=(15, self.screen_rect.centery * 1.5))
        sum_score_surf = title_font.render(
            f"You have {data['sum_score']} points", True, "white"
        )
        sum_score_rect = sum_score_surf.get_rect(midright=(self.screen_size[0] - 15, self.screen_rect.centery * 1.5))        

        self.text_surface.blit(title_surf, title_rect)
        self.text_surface.blit(instruction_surf, instruction_rect)
        self.text_surface.blit(high_score_surf, high_score_rect)
        self.text_surface.blit(sum_score_surf, sum_score_rect)

        self.text_surface_alpha = 0
        self.text_surface.set_alpha(self.text_surface_alpha)

    def update(self, events: Events):
        if not self.animate_out:
            fade_surface_in(self.fade_surface, self.FADE_SURFACE_MAX_ALPHA, self.FADE_SPEED, events["delta_time"])
            fade_surface_in(self.text_surface, self.TEXT_SURFACE_MAX_ALPHA, self.FADE_SPEED, events["delta_time"])
        else:
            fade_surface_out(self.fade_surface, 0, self.FADE_SPEED, events["delta_time"])
            fade_surface_out(self.text_surface, 0, self.FADE_SPEED, events["delta_time"])

        if (self.animate_out and
            self.fade_surface.get_alpha() <= 0 and
            self.text_surface.get_alpha() <= 0
        ):
            self.next_state = GameStates.GAME

    def draw(self, screen: pygame.Surface):
        screen.blit(self.last_game_frame, (0, 0))
        screen.blit(self.fade_surface, (0, 0))

        screen.blit(self.text_surface, (0, 0))


class UIStage(BackgroundStage):
    def __init__(self, last_frame: pygame.Surface):
        super().__init__(last_frame)

    def update(self, events: Events):
        super().update(events)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)


class SwitchStage(UIStage):
    """
    Stage that handles game state switches (menu -> game)
    """

    def update(self, events: Events):
        super().update(events)

        for event in events["events"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.animate_out = True


class Menu(SwitchStage):
    pass
