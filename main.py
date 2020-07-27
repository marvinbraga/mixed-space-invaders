import math
import random
from enum import Enum

import pygame
from pygame import mixer
from setups import *
from base import GameObject, Position


class Enemy:
    """
        Enemy class.
    """
    def __init__(self, image, screen):
        self.image = pygame.image.load(image)
        self.pos = Position(x=random.randint(0, 736), y=random.randint(50, 150))
        self.change = Position(x=4, y=40)
        self.screen = screen

    def move(self):
        self.pos.X += self.change.X
        if self.pos.X <= 0:
            self.change.X = 4
            self.pos.Y += self.change.Y
        elif self.pos.X >= 736:
            self.change.X = -4
            self.pos.Y += self.change.Y

        return self

    def show(self):
        self.screen.blit(self.image, (self.pos.X, self.pos.Y))
        return self

    def out(self):
        self.pos.Y = 2000
        return self


class Enemies:
    """
        Enemies class.
    """
    def __init__(self, setup, screen, count=7):
        self.count = count
        self.images = setup.images
        self.items = []
        self.screen = screen
        self.setup = setup
        # start a number of count enemies.
        image_index = 0
        for index in range(count):
            img = setup.images[image_index]
            self.items.append(Enemy(image=img, screen=screen))
            image_index += 1
            if image_index >= len(setup.images):
                image_index = 0


class Player(GameObject):
    """
        Player class.
    """
    def __init__(self, setup, screen):
        super().__init__(setup=setup, screen=screen)
        self.pos.X = 370
        self.pos.Y = 480
        self.change = 0

    def move(self):
        self.pos.X += self.change
        if self.pos.X <= 0:
            self.pos.X = 0
        elif self.pos.X >= 736:
            self.pos.X = 736


class Bullet(GameObject):
    """
        Bullet class.
    """
    class State(Enum):
        """
            State of bullet class.
        """
        READY = 0
        FIRE = 1

    def __init__(self, setup, screen):
        super().__init__(setup=setup, screen=screen)
        self.state = Bullet.State.READY
        self.pos.X = 0
        self.pos.Y = 480
        self.change = Position(x=0, y=10)
        self.sound = mixer.Sound(setup.sound)

    def fire(self):
        self.state = Bullet.State.FIRE
        self.screen.blit(self.image, (self.pos.X + 16, self.pos.Y + 10))
        return self

    def move(self):
        if self.pos.Y <= 0:
            self.pos.Y = 480
            self.state = Bullet.State.READY

        if self.state is Bullet.State.FIRE:
            self.fire()
            self.pos.Y -= self.change.Y
        return self

    def is_collision(self, enemy):
        distance = math.sqrt(
            math.pow(enemy.pos.X - self.pos.X, 2) + math.pow(enemy.pos.Y - self.pos.Y, 2))
        result = (distance < 27)
        if result:
            self.pos.Y = 480
            self.state = Bullet.State.READY
        return result

    def prepared(self, x):
        self.pos.X = x
        self.sound.play()
        return self


class Score:

    def __init__(self, screen, font='freesansbold.ttf', over_font='freesansbold.ttf'):
        self.value = 0
        self.font = pygame.font.Font(font, 32)
        self.pos = Position(x=10, y=10)
        self.screen = screen
        # Game Over
        self.over_font = pygame.font.Font(over_font, 64)

    def show(self):
        score = self.font.render("Score : " + str(self.value), True, (255, 255, 255))
        self.screen.blit(score, (self.pos.X, self.pos.Y))
        return self


class SpaceInvaders:
    """
        Space Invaders Game
    """
    def __init__(self, setup):
        self.setup = setup
        self.screen = None
        self.mixer = None
        self.background = None
        self.score = None
        self.player = None
        self.enemies = None
        self.bullet = None
        self.explosion_sound = None
        # setup display and objects.
        self.setup_display().live_objects()

    def setup_display(self):
        """
            Setup display informations.
            :return: self
        """
        # create the screen
        self.screen = pygame.display.set_mode((self.setup.game.width, self.setup.game.height))
        # Background
        self.background = pygame.image.load(self.setup.game.background)
        # Sound
        self.mixer = mixer
        self.start_background_music()
        self.explosion_sound = self.mixer.Sound(self.setup.game.sound_explosion)
        # Caption and Icon
        pygame.display.set_caption(self.setup.game.caption)
        pygame.display.set_icon(pygame.image.load(self.setup.game.icon))
        return self

    def live_objects(self):
        """
            Start all game objects.
            :return: self
        """
        # Score
        self.score = Score(screen=self.screen)
        # Enemies
        self.enemies = Enemies(setup=self.setup.enemies, screen=self.screen)
        # Player
        self.player = Player(setup=self.setup.player, screen=self.screen)
        # Bullet
        self.bullet = Bullet(setup=self.setup.bullet, screen=self.screen)

        return self

    def start_background_music(self):
        """
            Start game music.
            :return: self
        """
        self.mixer.music.load(self.setup.game.background_music)
        self.mixer.music.play(-1)
        return self

    def game_over_text(self):
        """
            Print game over text.
            :return: self
        """
        over_text = self.score.over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))
        return self

    def check_key_events(self, event):
        running = True
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.change = -5
            if event.key == pygame.K_RIGHT:
                self.player.change = 5
            if event.key == pygame.K_SPACE:
                if self.bullet.state is Bullet.State.READY:
                    # Get the current x coordinate of the spaceship
                    self.bullet.prepared(x=self.player.pos.X)
                    self.bullet.fire()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.player.change = 0

        return running

    def check_game_over(self, enemy):
        result = False
        if enemy.pos.Y > 450:
            for en in self.enemies.items:
                en.out()
            self.game_over_text()
            result = True
        return result

    def check_collision(self, enemy):
        if self.bullet.is_collision(enemy=enemy):
            self.explosion_sound.play()
            self.score.value += 1
            enemy.pos.X = random.randint(0, 736)
            enemy.pos.Y = random.randint(50, 150)
        return self

    def show_background(self):
        # RGB = Red, Green, Blue
        self.screen.fill((0, 0, 0))
        # Background Image
        self.screen.blit(self.background, (0, 0))
        return self

    def run(self):
        """
            Game run!
            :return: self
        """
        # Game Loop
        running = True
        while running:
            self.show_background()
            # Player movement
            for event in pygame.event.get():
                running = self.check_key_events(event)
            self.player.move()
            # Enemy Movement
            for enemy in self.enemies.items:
                # Game Over
                if self.check_game_over(enemy=enemy):
                    break
                enemy.move()
                # Collision
                self.check_collision(enemy=enemy)
                # Enemy show
                enemy.show()
            # Bullet Movement
            self.bullet.move()
            self.player.show()
            self.score.show()
            pygame.display.update()
        return self


class Game:
    """
        Wrapper to Space Invaders Game
    """
    @staticmethod
    def start():
        pygame.init()
        setup = Setup(
            game=GameSetup(background='./resources/background.png', background_music='./resources/background.wav'),
            player=PlayerSetup(image='./resources/mario64.png'),
            enemy=EnemiesSetup(images=['./resources/enemy.png', './resources/pacman64.png', './resources/enemy3.png']),
            bullet=BulletSetup(image='./resources/bullet2.png')
        )
        SpaceInvaders(setup=setup).run()


if __name__ == '__main__':
    Game.start()
