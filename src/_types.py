from typing import Dict, Sequence, TypeAlias, Union

import pygame

ColorValue: TypeAlias = Union[str, int, Sequence[int], pygame.Color]
Position: TypeAlias = Union[Sequence[int], pygame.Vector2]
Events: TypeAlias = Dict[str, Union[int, Sequence[int]]]
