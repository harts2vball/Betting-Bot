from random import randint

class csgoWildCoinFlip:

    url = 'csgowild.com'
    gameNum = 0

    def __init__(self):
        self.url = 'csgowild.com'
        gameNum = 0

    """
    This function randomly returns either a 1 or 0.
    """
    def chooseSide(self):
        random = randint(0,9)
        if( random < 5):
            return 0
        else:
            return 1

