class Setup:
    """
        Setup game informations.
    """
    def __init__(self, game, player, enemy, bullet):
        self.game = game
        self.player = player
        self.enemies = enemy
        self.bullet = bullet


class GameSetup:
    """
        Game general informations.
    """
    def __init__(self, background, background_music, width=800, height=600, caption='Mixed Space Invaders',
                 icon='./resources/ufo.png', sound_explosion='./resources/explosion.wav'):
        self.width = width
        self.height = height
        self.background = background
        self.background_music = background_music
        self.caption = caption
        self.icon = icon
        self.sound_explosion = sound_explosion


class PlayerSetup:
    """
        Player base informations.
    """
    def __init__(self, image):
        self.image = image


class EnemiesSetup:
    """
        Enemies base informations.
    """
    def __init__(self, images):
        self.images = images


class BulletSetup:
    """
        Bullet base informations.
    """
    def __init__(self, image, sound='./resources/laser.wav'):
        self.image = image
        self.sound = sound
