

class LoopingVariable:
    """
    klasse die een loopingvariabele is/maakt
    
    Attributen
    ----------
    max = int
    __current = int
    """
    def __init__(self, max):
        """
        initialiseert de klasse

        Parameters
        ----------
        max : int
        """
        self.max = max
        self.__value = 0

    def increase(self, amount):
        """
        verhoogt de loopingvariabele met een bepaalde hoeveelheid

        Parameters
        ----------
        amount : int
        """
        if (self.__value + amount) >= self.max:
            amount -= self.max - self.__value
            self.__value = 0
            self.__value += amount
            
        else:
            self.__value += amount
    
    @property
    def value(self):
        """
        Is het private current attribuut da wordt gereturned
        """
        return self.__value