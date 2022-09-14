import pygame

from src._types import Events
from src.enums import GameStates
from typing import Tuple


class InitStage:
	def __init__(self, last_frame: pygame.Surface):
		self.screen_size = last_frame.get_size()
		self.last_game_frame = last_frame
		self.screen_rect = pygame.Rect(0, 0, *self.screen_size)

		self.next_state = None


class BackgroundStage(InitStage):
	def __init__(self, last_frame: pygame.Surface):
		super().__init__(last_frame)

		self.fade_surface = pygame.Surface(self.screen_size)
		self.fade_surface.set_alpha(100)

		# surface that contains all the text
		self.text_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)

		title_font = pygame.font.Font(
            "assets/gfx/Montserrat-ExtraLight.ttf", 21
        )
		title_surf = title_font.render("Don't collide with the triangular objects", True, "white")
		title_rect = title_surf.get_rect(midtop=(self.screen_rect.centerx, self.screen_rect.centery / 15))
		
		instruction_surf = title_font.render("Press Space to start", True, "white")
		instruction_rect = instruction_surf.get_rect(midtop=(self.screen_rect.centerx, self.screen_rect.centery / 6))

		self.text_surface.blit(title_surf, title_rect)
		self.text_surface.blit(instruction_surf, instruction_rect)

	def update(self, events: Events):
		pass

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

		self.next_state = None
		for event in events["events"]:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.next_state = GameStates.GAME


class Menu(SwitchStage):
	pass