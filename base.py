import pygame


class Position:
    """
        Config a position.
    """
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y


class GameObject:
    """
        Base class to game objects.
    """
    def __init__(self, setup, screen):
        self.image = pygame.image.load(setup.image)
        self.pos = Position()
        self.screen = screen
        self.setup = setup

    def show(self):
        self.screen.blit(self.image, (self.pos.X, self.pos.Y))
        return self
