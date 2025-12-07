from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        self.land.loadLand("land.txt")

game = Game()

game.run()
