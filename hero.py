class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3) 
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
