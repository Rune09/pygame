class Cooldown:
    """
    Klasse Cooldown, zorgt ervoor da ge geschoten bullets kunt limitten

    Attributen
    ----------
    time_passed : float
    ready : boolean
    __max_time : float
    """
    def __init__(self, max_time = 0.5):
        """
        Initialiseert de klasse

        Parameters
        ----------
        max_time : float -> standaard == 0.5
        """
        self.time_passed = 0
        self.ready = False
        self.__max_time = max_time

    def reset(self):
        """
        Resets the class
        """
        self.time_passed = 0
        self.ready = False
    
    def update(self, elapsed_seconds):
        """
        update de positie van de klasse adhv gepasseerde tijd

        Parameters
        ----------
        elapsed_seconds : float
        """
        self.time_passed += elapsed_seconds
        if self.time_passed < self.__max_time:
            self.ready = False
        else:
            self.ready = True
            
            