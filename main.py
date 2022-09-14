import pygame

from src.stages.world import World
from src.stages.menu import Menu
from src.enums import GameStates


WIDTH, HEIGHT = 416, 640


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.clock = pygame.time.Clock()

        self.states = {
            GameStates.GAME: World,
            GameStates.MENU: Menu,
        }
        self.state = self.states[GameStates.MENU](self.screen.copy())

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            delta_time = self.clock.tick(60) / 10
            events = {
                "events": events,
                "delta_time": delta_time,
                "keys": pygame.key.get_pressed(),
            }

            self.state.update(events)
            self.state.draw(self.screen)

            if self.state.next_state is not None:
                if self.state.next_state == GameStates.GAME:
                    self.state = self.states[self.state.next_state]((WIDTH, HEIGHT))
                else:
                    self.state = self.states[self.state.next_state](self.screen.copy())

            pygame.display.flip()
            pygame.display.set_caption(
                f"FPS: {self.clock.get_fps():.0f}"
            )

if __name__ == "__main__":
    Game().run()