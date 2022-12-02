from os.path import isfile, join
from os import listdir, walk, path
import pygame
import random
pygame.init()


class SoundLibrary:
    """
    Een klasse dat een soundlibrary voorstelt
    """

    
    def __find_audio_files(self, root):
        """ 
        Geeft alle paths terug van audiofiles in een directory
        
        Parameters
        ----------
        root : str
            naam van de root directory
        
        Returns
            array van filepaths 
        """

        entries = listdir(root + '/')
        files = []
        for f in entries:
            names = listdir(root + '/' + f)
            for i in names:
                files.append('./{}/{}'.format(f, i))
        return (files)

    def __derive_id(self, path, ext='.ogg'):
        """
        Geeft het id uit een path terug

        Parameters
        ----------
        path : str
            path naar een file
        ext : str
            de extensie van de bestanden, is nodig voor formatting. Staat by default op .ogg

        Returns
            een id als str
        """

        id = path.lstrip('./')
        id = id.rstrip(ext)
        return (id)

    def __create_sound_table(self, paths):
        """
        Creëert tabel van alle sound effect id's gelinkt aan hun juiste path

        Parameters
        ----------
        paths : array
            array van alle paths uit bepaalde directory
        
        Returns
            matrix met id's en corresponding paths in. van de vorm [[id, path], [id, path]]
        """

        idarr = []
        for i in paths:
            idarr.append(self.__derive_id(i))
        tablematrix = []
        for i in range(0, len(paths)):
            tablematrix.append([idarr[i], paths[i]])
        return tablematrix

    def __init__(self, path='sounds'):
        """
        Initialiseert soundLibrary

        Parameters
        ----------

        path : str
            Staat standaard op sounds, hangt af van welke root directory je wil gebruiken
        """

        paths = self.__find_audio_files(path)
        self.table = self.__create_sound_table(paths)

    def play_sound(self, soundName):
        """
        Speelt een bepaald sound effect af

        Parameters
        ----------

        soundName : str
            Id van het gewenste geluidseffect
        """


        for i in range(0, len(self.table)):
            if self.table[i][0] == soundName:
                name = 'sounds' + self.table[i][1].lstrip('.')

        pygame.mixer.Sound(name).play()

    def play_random_explosion(self):
        """
        Speelt random explosiegeluid af

        Parameters
        ----------
        None
        """

        randomex = random.randint(1, 6)
        self.play_sound('explosions/{}'.format(randomex))
