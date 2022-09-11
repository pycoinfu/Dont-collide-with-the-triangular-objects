import pygame

from src.world import World

WIDTH, HEIGHT = 416, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
clock = pygame.time.Clock()

world = World((WIDTH, HEIGHT))

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    delta_time = clock.tick(60) / 10
    events = {
        "events": events,
        "delta_time": delta_time,
        "keys": pygame.key.get_pressed(),
    }

    screen.fill("black")

    world.update(events)
    world.draw(screen)

    pygame.display.flip()
    pygame.display.set_caption(
        f"Don't collide with the triangular objects | FPS: {clock.get_fps():.0f}"
    )
