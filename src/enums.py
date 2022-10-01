import enum


class GameStates:
    GAME = enum.auto()
    MENU = enum.auto()


class PlayerStates:
    IDLE = enum.auto()
    JUMP = enum.auto()
