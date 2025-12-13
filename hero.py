class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turn_left(self):
        self.hero.setH( (self.hero.getH() + 5) % 360 )

    def turn_right(self):
        self.hero.setH( (self.hero.getH() - 5) % 360 )

    def forward(self):
        angle = self.hero.getH() % 360
        hero_x = self.hero.getX()
        hero_y = self.hero.getY()
        
        if angle <= 22 or angle >= 337:
            hero_y += 1
        elif angle < 67:
            hero_x -= 1
            hero_y += 1
        elif angle < 112:
            hero_x -= 1
        elif angle < 157:
            hero_x -= 1
            hero_y -= 1

        self.hero.setX(hero_x)
        self.hero.setY(hero_y)


    def accept_events(self):
        base.accept('c', self.changeView)

        base.accept('n', self.turn_left)
        base.accept('n' + '-repeat', self.turn_left)

        base.accept('m', self.turn_right)
        base.accept('m' + '-repeat', self.turn_right)

        base.accept('w', self.forward)
        base.accept('w' + '-repeat', self.forward)
