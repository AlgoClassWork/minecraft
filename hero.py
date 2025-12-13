key_switch_camera = 'c'
key_switch_mode = 'z'
key_forward = 'w'   
key_back = 's'      
key_left = 'a'      
key_right = 'd'     
key_up = 'e'      
key_down = 'q'   
key_turn_left = 'n'     
key_turn_right = 'm'    
key_build = 'b'     
key_destroy = 'v'   
key_savemap = 'k'
key_loadmap = 'l'


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
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def check_dir(self, angle):
        angle = angle % 360

        if angle < 22.5 or angle >= 337.5:
            return (0, 1)      # вперед
        elif angle < 67.5:
            return (-1, 1)     # вперед-влево
        elif angle < 112.5:
            return (-1, 0)     # влево
        elif angle < 157.5:
            return (-1, -1)    # назад-влево
        elif angle < 202.5:
            return (0, -1)     # назад
        elif angle < 247.5:
            return (1, -1)     # назад-вправо
        elif angle < 292.5:
            return (1, 0)      # вправо
        else:
            return (1, 1)      # вперед-вправо

    def forward(self):
        angle = self.hero.getH()
        dx, dy = self.check_dir(angle)

        self.hero.setX(self.hero.getX() + dx)
        self.hero.setY(self.hero.getY() + dy)

    def accept_events(self):
        base.accept(key_switch_camera, self.changeView)

        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)

        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
