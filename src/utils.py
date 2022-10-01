import pygame


def fade_surface_in(surface: pygame.Surface, alpha: int, speed: float, delta_time: float):
    current_alpha = surface.get_alpha()
    if current_alpha < alpha:
        new_alpha = current_alpha + speed * delta_time
        surface.set_alpha(new_alpha)


def fade_surface_out(surface: pygame.Surface, alpha: int, speed: float, delta_time: float):
    current_alpha = surface.get_alpha()
    if current_alpha > alpha:
        new_alpha = current_alpha - speed * delta_time
        surface.set_alpha(new_alpha)
