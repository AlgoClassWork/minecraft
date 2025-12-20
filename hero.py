# ----------------------------------------
# Настройка клавиш
# ----------------------------------------
key_switch_camera = 'c'  # камера привязана к герою или свободная
key_switch_mode = 'z'    # режим прохождения сквозь препятствия

key_forward = 'w'   # шаг вперед
key_back = 's'      # шаг назад
key_left = 'a'      # шаг влево (относительно камеры)
key_right = 'd'     # шаг вправо (относительно камеры)
key_up = 'e'        # шаг вверх
key_down = 'q'      # шаг вниз

key_turn_left = 'n'     # поворот героя налево
key_turn_right = 'm'    # поворот героя направо

key_build = 'b'     # построить блок перед собой
key_destroy = 'v'   # разрушить блок перед собой


# ----------------------------------------
# Класс героя
# ----------------------------------------
class Hero:
    def __init__(self, pos, land):
        """
        Инициализация героя.
        
        Args:
            pos (tuple): стартовая позиция героя (x, y, z)
            land (Mapmanager): объект карты
        """
        self.land = land
        self.mode = True  # Режим прохождения сквозь все препятствия
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setH(180)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)

        self.cameraBind()
        self.accept_events()

    # --------------------------
    # Камера
    # --------------------------
    def cameraBind(self):
        """Привязывает камеру к герою"""
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        """Отвязывает камеру от героя, включая свободное управление"""
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        """Переключение между привязанной камерой и свободной"""
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    # --------------------------
    # Повороты героя
    # --------------------------
    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    # --------------------------
    # Перемещения героя
    # --------------------------
    def look_at(self, angle):
        """
        Возвращает координаты, куда переместится герой, если сделает шаг
        в направлении angle.
        """
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        """Перемещается в нужные координаты без проверки препятствий"""
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        """Перемещается с учетом режима прохождения препятствий"""
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)  # Метод try_move должен быть реализован отдельно

    def check_dir(self, angle):
        """
        Возвращает изменения координат (dx, dy) в зависимости от угла движения.
        Угол 0 → движение по -Y, 90 → +X, 180 → +Y, 270 → -X
        """
        if 0 <= angle <= 20:
            return (0, 1)
        elif angle <= 65:
            return (-1, 1)
        elif angle <= 110:
            return (-1, 0)
        elif angle <= 155:
            return (-1, -1)
        elif angle <= 200:
            return (0, -1)
        elif angle <= 245:
            return (1, -1)
        elif angle <= 290:
            return (1, 0)
        elif angle <= 335:
            return (1, 1)
        else:
            return (0, 1)

    # --------------------------
    # Управление движением
    # --------------------------
    def forward(self):
        angle = self.hero.getH() % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def up(self):
        if self.mode:
            self.hero.setZ( self.hero.getZ() + 1 )

    def down(self):
        if self.mode:
            self.hero.setZ( self.hero.getZ() - 1 )

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.destroyBlock(pos)

    # --------------------------
    # События клавиш
    # --------------------------
    def accept_events(self):
        # Поворот камеры/героя
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        # Движение героя
        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)

        # Переключение вида камеры
        base.accept(key_switch_camera, self.changeView)
        # Переключение игрового режима
        base.accept(key_switch_mode, self.changeMode)
