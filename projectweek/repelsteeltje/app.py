import pygame
import looper
import time
from random import randint, randrange
from pygame.time import Clock
from tkinter import Tk
from cooldown import Cooldown
import soundLibrary


def create_main_function():  # scherm maken
    """
    creëert een window

    Returns
        een window
    """
    return pygame.display.set_mode((1024, 768), pygame.RESIZABLE)


def opstart():
    """
    Startscherm
    """
    GameDisplay = create_main_function()
    pygame.init()
    titel = pygame.image.load("images/backgrounds/logo.png")
    titel = pygame.transform.scale(titel, (pygame.display.get_surface().get_size()[
                                   0], pygame.display.get_surface().get_size()[1]))
    titel_loc = titel.get_rect()
    titel_loc.center = pygame.display.get_surface().get_size(
    )[0]/2, pygame.display.get_surface().get_size()[1]/2
    GameDisplay.blit(titel, titel_loc)
    pygame.display.flip()
    pygame.time.delay(2000)


def gedaan_met_spelen():
    """
    Scherm vr als je sterft
    """
    GameDisplay = create_main_function()
    pygame.init()
    titel = pygame.image.load("images/backgrounds/death.jpg")
    titel = pygame.transform.scale(titel, (pygame.display.get_surface().get_size()[
                                   0], pygame.display.get_surface().get_size()[1]))
    titel_loc = titel.get_rect()
    titel_loc.center = pygame.display.get_surface().get_size(
    )[0]/2, pygame.display.get_surface().get_size()[1]/2
    GameDisplay.blit(titel, titel_loc)
    pygame.display.flip()
    pygame.time.delay(20)


def render_frame(surface, klasse):  # rendert frame en laadt image blijkbaar
    """
    Roept de render in een bepaalde klasse op

    Parameters
    ----------
    surface : class Surface
    klasse : een klasse
    """
    klasse.render(surface)


def clear_surface(surface):  # achtergrond resetten zodat er geen trail achterblijft
    """
    Maakt de window volledig zwart zodat er geen trail achterblijft. Lijkt me redundant.
    """
    pygame.Surface.fill(surface, (0, 0, 0))


def process_key_input(state, elapsed_seconds):
    """
    Processt de key input en kijkt welke toets er is ingedrukt. Roept de bijhorende functie op

    Parameters
    ----------
    state : class state
    elapsed_seconds : float


    Returns
        functioncall
    """
    ship = state.spaceship
    frame = ship.speed * elapsed_seconds
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        state.add_bullet(state)
    if pressed[pygame.K_a]:
        state.add_dragon()
    if pressed[pygame.K_RIGHT]:
        old_x = ship.position[0]
        old_y = ship.position[1]
        new_position = (old_x + frame, old_y)
        ship.position = new_position
    elif pressed[pygame.K_LEFT]:
        old_x = ship.position[0]
        old_y = ship.position[1]
        new_position = (old_x - frame, old_y)
        ship.position = new_position


class Background:
    """
    klasse voor de achtergrond
    """

    def __init__(self, path):
        """
        initialiseert klasse met gegeven path

        Parameters
        ----------
        path : str
        y : int -> default == 0
        """
        self.__image = path

    def __create_image(self):
        """
        private methode die de afbeelding laadt

        Returns
            Gelaadde afbeelding
        """
        return pygame.image.load(self.__image)

    def __flip_image_vertically(self):
        """
        Draait een image rond hun horizontale as

        Returns
            nieuwe surface object
        """
        return pygame.transform.flip(self.__create_image(), flip_x=True, flip_y=False)

    def render(self, surface):
        """
        rendert de eigen afbeelding op een meegegeven surface

        Parameters
        ----------
        surface : klasse surface
        """
        image = self.__create_image()
        new_image = self.__flip_image_vertically()
        h = pygame.Surface.get_height(image)

        pygame.Surface.blit(surface, image,
                            (-5, 0))
        pygame.Surface.blit(surface, new_image,
                            (pygame.Surface.get_width(image)-5, 0))
        pygame.Surface.blit(surface, image,
                            (pygame.Surface.get_width(image)*2-10, 0))


class Bullet:
    """
    Klasse voor elke kogel die wordt afgeschoten

    Attributen
    ----------
    x : float
    y : float
    disposed : boolean
    __speed : float
    __time_left : float
    __bounding_box : Rect
    """

    def __init__(self, x=500, y=500):
        """
        Initialiseert de klasse

        Parameters
        ----------
        x : float
        y : float
        """
        self.x = x
        self.y = y
        self.disposed = False
        self.__speed = 420
        self.__time_left = 2
        self.__bounding_box = pygame.Rect(
            self.x - self.__create_img().get_width()/2, self.y - self.__create_img().get_height()/2, self.__create_img().get_width(), self.__create_img().get_height())

    @property
    def bounding_box(self):
        """
        maakt hitbox publiekelijk readable

        Returns
            __bounding_box : Rect
        """
        return self.__bounding_box

    def __create_img(self):
        """
        Private klasse die de afbeelding inlaadt

        Return
            Ingelaadde afbeelding
        """
        return pygame.image.load('images/sprites/bullets/arrow.png')

    def render(self, surface):
        """
        Rendert de kogel op het scherm

        Parameters
        ----------
        surface : klasse Surface
        """
        pygame.Surface.blit(surface, self.__create_img(),
                            (self.x, self.y))

    def update(self, elapsed_seconds):
        """
        Update zijn eigen positie

        Parameters
        ----------
        elapsed_seconds : float
        """
        self.y -= self.__speed*elapsed_seconds
        self.__time_left -= elapsed_seconds
        if self.__time_left < 0:
            self.__time_left = 0
        if self.__time_left == 0:
            self.disposed = True
        self.__bounding_box = pygame.Rect(
            self.x - self.__create_img().get_width()/2, self.y - self.__create_img().get_height()/2, self.__create_img().get_width(), self.__create_img().get_height())


class Dragon:
    """
    Klasse voor de enemies

    Attributen
    ----------
    __image : een ingelaadde afbeelding
    __position : tuple
    __x : int
    __y : int
    __bounding_box : Rect
    speed : int
    direction : int
    counter : float
    disposed : boolean
    """

    def __init__(self):
        """
        Initialiseert de klasse
        """
        self.__image = pygame.image.load('images/sprites/dragon.png')
        self.__position = (
            20, pygame.display.get_surface().get_size()[1] - 175)
        self.__x = randrange(-50, (pygame.display.get_surface().get_size()
                             [0] + 50), (pygame.display.get_surface().get_size()[0] + 100))
        self.__y = 0  # pygame.display.get_surface().get_size()[1]
        self.speed = 690
        self.direction = randint(-1, 1)
        self.counter = 0
        self.disposed = False

        self.__bounding_box = pygame.Rect(
            self.__x - self.__image.get_width()/2, self.__y - self.__image.get_height()/2, self.__image.get_width(), self.__image.get_height())

        # self.__bounding_box = pygame.draw.rect(self.__image, (255, 255, 255), (
        #    0, 0, self.__image.get_width(), self.__image.get_height()))

    @property
    def x(self):
        """
        maakt x publiekelijk readable

        Returns
            __x : int
        """
        return self.__x

    @property
    def y(self):
        """
        maakt y publiekelijk readable

        Returns
            __y : int
        """
        return self.__y

    @property
    def bounding_box(self):
        """
        maakt hitbox publiekelijk readable

        Returns
            __bounding_box : Rect
        """
        return self.__bounding_box

    def update(self, elapsed_seconds):
        """
        Zou de positie moeten updaten

        Parameters
        ----------
        elapsed_seconds : float
        """
        if self.counter > 50:
            self.direction = randint(-1, 1)
            self.speed = randint(200, 500)
            self.counter = 0
            self.__y += 35
        if self.__x >= pygame.display.get_surface().get_size()[0] - 75:
            self.direction = -1
        if self.__x <= 0 + 75:
            self.direction = 1
        self.__x += self.speed*elapsed_seconds * self.direction
        self.counter += 1
        self.__bounding_box = pygame.Rect(
            self.__x - self.__image.get_width()/2, self.__y - self.__image.get_height()/2, self.__image.get_width(), self.__image.get_height())

    def render(self, surface):
        """
        Callt de render_dragon functie

        Parameters
        ----------
        surface : klasse Surface
        """
        render_dragon(self.__image, surface, (self.__x, self.__y))


class State:
    """
    Is een class die alle game-related info groepeert

    Attributen
    ----------
    circle_x : int
    circle_y : int
    animations : array
    __background : class Background
    """

    def __init__(self, background=Background('images/backgrounds/background_game.jpg'), circle_x=512, circle_y=384):
        """
        Initialiseert een state

        Parameters
        ----------
        circle_x  : int -> standaard == 512
        circle_y : int -> standaard == 384
        background : class Background
        """
        self.circle_x = circle_x
        self.circle_y = circle_y
        self.animations = []
        self.__background = background
        self.cooldown = Cooldown(1)
        self.cooldown_dragon = Cooldown(1)
        self.__spaceship = Spaceship()
        self.__bullets = []
        self.__score = Score_counter()
        self.__dragons = []
        self.__sound = soundLibrary.SoundLibrary()

    @property
    def dragon(self):
        """
        maakt dragon publiekelijk readable

        Returns
            __dragons : list
        """
        return self.__dragons

    @ dragon.setter
    def dragon(self, new_value):
        """
        voegt een nieuwe waarde toe aan __dragons

        parameters
        ----------
        new_value : int
        """
        self.__dragons.append(new_value)

    @property
    def bullets(self):
        """
        maakt bullets publiekelijk readable

        Returns
            __bullets : list
        """
        return self.__bullets

    @ property
    def spaceship(self):
        """
        maakt __spaceship publiekelijk readable

        Returns
            __spaceship : tuple
        """
        return self.__spaceship

    def remove_dragon(self, index):
        """
        removes a dragon and updates the array value

        Parameters
        ----------
        index : int
        """
        result = []
        for i in range(0, len(self.__dragons)):
            if index != i:
                result.append(self.__dragons[i])
        self.__dragons = result

    def remove_bullet(self, index):
        """
        removes a bullet and updates the array value

        Parameters
        ----------
        index : int
        """
        result = []
        for i in range(0, len(self.__bullets)):
            if index != i:
                result.append(self.__bullets[i])
        self.__bullets = result

    def update(self, time, clock):
        """
        roept de update functies op

        parameters
        ----------
        time : float
        """
        self.__score.update(clock)
        bullet = []
        dragon = []
        for i in range(0, len(self.__bullets)):
            y = self.__bullets[i]
            y.update(time)
            if not y.disposed:
                bullet.append(y)
        for i in range(0, len(self.dragon)):
            y = self.dragon[i]
            y.update(time)
            if not y.disposed:
                dragon.append(y)
        self.__bullets = bullet
        self.__dragons = (dragon)
        self.cooldown.update(time)
        self.cooldown_dragon.update(time)

    def add_bullet(self, state):
        """
        Voegt een bullet toe aan de game

        parameters
        ----------
        state : State
        """
        if self.cooldown.ready:
            avatar = state.spaceship
            pos = avatar.position
            x = pos[0]
            y = pos[1]
            b = Bullet(x, y)
            self.__bullets.append(b)
            self.cooldown.reset()
            self.__sound.play_sound('shots/bullet')

    def add_dragon(self):
        """
        Voegt een draak aan de game toe
        """
        if self.cooldown_dragon.ready:
            drachon = Dragon()
            self.__dragons.append(drachon)
            self.cooldown_dragon.reset()

    def render(self, surface):
        """
        Rendert state(moet nog aan gewerkt worden cuz iets klopt er niet)

        Parameters
        ---------
        surface : object surface
        """

        self.__background.render(surface)
        self.__spaceship.render(surface)
        self.__spaceship.render(surface)
        for bullet in self.__bullets:
            bullet.render(surface)
        for dragon in self.dragon:
            dragon.render(surface)
        self.__score.render(surface)
        pygame.display.flip()

    def add_animations(self, animation):
        """
        Voegt nieuwe animatie toe aan het array animations

        Parameters
        ----------
        animation : array
        """
        self.animations.append(animation)


def render_score_counter(surface, score):
    """
    zou de score moeten renderen

    parameters
    ----------
    surface : Surface
    score : int
    """
    print(score)
    font = pygame.font.SysFont("Times New Roman", 50)
    Label = font.render(("SCORE: " + str(score)), 1, (0, 0, 0))
    pygame.Surface.blit(surface, Label, (0, 0))


class Score_counter:
    """
    Houdt de score bij

    Attributen
    ----------
    score : int -> standaard 0
    """

    def __init__(self):
        self.score = 0

    def render(self, surface):
        font = pygame.font.SysFont("Times New Roman", 50)
        Label = font.render(("SCORE: " + str(self.score)), 1, (0, 0, 0))
        pygame.Surface.blit(surface, Label, (0, 0))

    def update(self, clock):
        self.score += round(clock.get_time()/100)


def render_spaceship(ship, surface, position):
    """
    Rendert de avatar on screen

    Parameters
    ----------
    surface : klasse Surface
    position : tuple
    """
    pygame.Surface.blit(surface, ship, (position[0] - (ship.get_width() //
                                                       2), position[1] - (ship.get_height() // 2)), area=None)


def render_dragon(avatar, surface, position):
    """
    Rendert de enemy on screen

    Parameterts
    -----------
    surface : klasse Surface
    position : tuple
    """
    pygame.Surface.blit(surface, avatar, (position[0] - (
        avatar.get_width() // 2), position[1] - (avatar.get_height() // 2)), area=None)


class Spaceship:
    """
    Klasse voor de avatar

    Attributen
    ---------
    __image : een ingelade afbeelding
    __postition : tuple
    speed : int
    """

    def __init__(self):
        """
        Initialiseert spaceship
        """
        self.__image = pygame.image.load('images/sprites/avatar.png')
        self.__position = (512,
                           pygame.display.get_surface().get_size()[1] - (self.__image.get_height() - 100))
        self.__x = 512
        self.__y = pygame.display.get_surface().get_size()[
            1] - (self.__image.get_height())
        self.speed = 690
        self.__bounding_box = pygame.Rect(
            self.__position[0] - self.__image.get_width()/2, self.__position[1] - self.__image.get_height()/2, self.__image.get_width(), self.__image.get_height())

    @ property
    def bounding_box(self):
        """
        maakt de hitbox publiekelijk readable

        Returns
            __bounding_box : Rect
        """
        return self.__bounding_box

    @ property
    def position(self):
        """
        maakt position publiekelijk readable

        Returns
            __position : int
        """
        return self.__position

    @ position.setter
    def position(self, new_value):
        """
        Checkt out of bounds

        Parameters
        ----------
        new_value : tuple
        """
        surface = pygame.display.get_surface()
        x, y = size = surface.get_width(), surface.get_height()
        # out of bounds check rechts
        if (new_value[0] > (x-(self.__image.get_width()/2))):
            templijst = list(new_value)
            templijst[0] = (x-(self.__image.get_width()/2))
            new_value = tuple(templijst)
        # out of bounds check links
        if (new_value[0] < 0 + (self.__image.get_width()/2)):
            templijst = list(new_value)
            templijst[0] = 0 + (self.__image.get_width()/2)
            new_value = tuple(templijst)
        # out of bounds check boven
        # if (new_value[1] < 0 + (self.__image.get_height()/2)):
        #    templijst = list(new_value)
        #    templijst[1] = 0 + (self.__image.get_height()/2)
        #    new_value = tuple(templijst)
        # out of bounds check onder
        # if (new_value[1] > (y-(self.__image.get_height()/2))):
        #    templijst = list(new_value)
        #    templijst[1] = (y-(self.__image.get_height()/2))
        #    new_value = tuple(templijst)
        self.__position = new_value
        self.__bounding_box = pygame.Rect(
            self.__position[0] - self.__image.get_width()/2, self.__position[1] - self.__image.get_height()/2, self.__image.get_width(), self.__image.get_height())

    def render(self, surface):
        """
        Callt de functie render_spaceship^

        Parameters
        ----------
        surface : klasse Surface
        """
        render_spaceship(self.__image, surface,
                         self.__position)


class FrameBasedAnimation:
    """
    animatie
    """

    def __init__(self, frames, duration, klasse):
        """
        initialiseert klasse FrameBasedAnimation

        Attributen
        ----------
        x : int
        y : int
        duration_frame : float
        frames : array
        count : int

        Parameters
        ----------
        frames : array
        duration : float
        klasse : class State
        """
        self.x = klasse.x
        self.y = klasse.y
        self.duration_frame = duration
        self.frames = frames
        self.count = 0

    def render(self, surface):
        """
        rendert de explosie ig

        Parameters
        ----------
        surface : class Surface

        Returns
            True
            -> als count even groot is als de lengte van array frames
            False
        """
        for i in range(1, len(self.frames) + 1):
            current_frame = self.frames[self.count]
            pygame.Surface.blit(surface, current_frame, (self.x - (current_frame.get_width(
            ) // 2), self.y - (current_frame.get_height() // 2)), area=None)
            pygame.display.flip()
            self.count += 1
            time.sleep(0.02)
            if self.count == len(self.frames):
                return False
        return True


def main():
    """
    main functie van het programma, doet vanalles
    """
    pygame.init()
    pygame.mixer.music.load('music/main2.ogg')
    pygame.mixer.music.play()
    opstart()
    sounds = soundLibrary.SoundLibrary()
    surface = create_main_function()
    active = True
    state = State()  # classeding van state wordt aangemaakt
    clock = Clock()
    elapsed_seconds = 0
    total_seconds = 0
    score = Score_counter()
    score_clock = Clock()
    frames = [pygame.image.load(
        f'images/sprites/explosion/{i}.png') for i in range(1, 9 + 1)]
    while active:

        # een call nr update elke keer de loop doorlopen wordt.
        if total_seconds <= 10:
            if round(total_seconds) % 5 == 0:
                state.add_dragon()
        elif total_seconds <= 20:
            if round(total_seconds) % 3 == 0:
                state.add_dragon()
        else:
            if round(total_seconds) % 1 == 0:
                state.add_dragon()

        state.update(elapsed_seconds, score_clock)
        process_key_input(state, elapsed_seconds)
        elapsed_seconds = 0
        render_frame(surface, state)
        # kijkt of een draak de avatar raakt, if so, end game
        dragons = [dragon.bounding_box for dragon in state.dragon]
        if pygame.Rect.collidelist(state.spaceship.bounding_box, dragons) != -1:
            game_over = Background('images/backgrounds/death.jpg')
            render_frame(surface, game_over)
            active = False
        bullets = [bullet.bounding_box for bullet in state.bullets]
        # canLoop zorgt ervoor dat er maar 1 keer in if statement kan gegaan worden zodat er per cycle maar 1 draak en bullet verwijderd worden
        canLoop = True
        for i in range(0, len(dragons)):
            if pygame.Rect.collidelist(dragons[i], bullets) != -1 and canLoop == True:
                canLoop = False
                sounds.play_random_explosion()
                state.remove_dragon(i)
                state.remove_bullet(
                    pygame.Rect.collidelist(dragons[i], bullets))
            # animation1 = FrameBasedAnimation(frames, 0.1, i)
        for event in pygame.event.get():  # voor window te kunnen sluiten
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    active = False
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
            if event.type == pygame.QUIT:
                active = False
        clock.tick()
        score_clock.tick()
        score.update(score_clock)
        elapsed_seconds += clock.get_time()/1000
        total_seconds += clock.get_time()/1000

    # Voor death screen te behouden zodat je opnieuw kan spelen
    end = True
    sounds.play_random_explosion()
    pygame.mixer.music.load('music/death.ogg')
    pygame.mixer.music.play()

    game_over = Background('images/backgrounds/death.jpg')
    render_frame(surface, game_over)
    gedaan_met_spelen()
    while end:
        for event in pygame.event.get():  # voor window te kunnen sluiten
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_ESCAPE:
                    end = False
            if event.type == pygame.QUIT:
                end = False


main()
