from panda3d.core import Vec3


key_switch_camera = 'c'

key_forward = 'w'
key_back = 's'
key_left = 'a'
key_right = 'd'

key_turn_left = 'n'
key_turn_right = 'm'


class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True

        self.hero = loader.loadModel('smiley')
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.setH(0)
        self.hero.reparentTo(render)

        self.cameraBind()
        self.accept_events()

    # ---------------- КАМЕРА (FPS) ----------------
    def cameraBind(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.6)   # ← В ГОЛОВЕ
        base.camera.setHpr(0, 0, 0)
        self.cameraOn = True

    def cameraUp(self):
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    # ---------------- ПОВОРОТ ----------------
    def turn_left(self):
        self.hero.setH(self.hero.getH() + 3)

    def turn_right(self):
        self.hero.setH(self.hero.getH() - 3)

    # ---------------- ДВИЖЕНИЕ ----------------
    def move(self, direction: Vec3):
        self.hero.setPos(self.hero.getPos() + direction)

    def forward(self):
        self.move(self.hero.getQuat().getForward())

    def back(self):
        self.move(-self.hero.getQuat().getForward())

    def left(self):
        self.move(-self.hero.getQuat().getRight())

    def right(self):
        self.move(self.hero.getQuat().getRight())

    # ---------------- СОБЫТИЯ ----------------
    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)

        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)

        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)

        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)

        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_switch_camera, self.changeView)
