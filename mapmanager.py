class Mapmanager:
    """Управление картой: создание блоков, загрузка карты из файла"""

    def __init__(self):
        # Модель и текстура блока
        self.model = 'block'       # Файл модели: block.egg
        self.texture = 'block.png' # Файл текстуры

        # Цвета блоков по высоте (RGBA)
        self.colors = [
            (0.2, 0.2, 0.35, 1),  # Пример: темный
            (0.2, 0.5, 0.2, 1),   # Зеленый
            (0.7, 0.2, 0.2, 1),   # Красный
            (0.5, 0.3, 0.0, 1)    # Коричневый
        ]

        # Создаем основной узел карты
        self.startNew()

    def startNew(self):
        """Создаёт основу для новой карты"""
        self.land = render.attachNewNode("Land")  # Узел, к которому будут привязаны все блоки

    def getColor(self, z):
        """
        Возвращает цвет блока в зависимости от высоты z.
        Если z превышает количество доступных цветов, возвращается последний цвет.
        """
        return self.colors[z] if z < len(self.colors) else self.colors[-1]

    def addBlock(self, position):
        """
        Создаёт строительный блок на карте в указанной позиции.

        Args:
            position (tuple): координаты блока (x, y, z)
        """
        block = loader.loadModel(self.model)
        block.setTexture(loader.loadTexture(self.texture))
        block.setPos(position)
        block.setColor(self.getColor(int(position[2])))
        block.setTag("at", str(position))
        block.reparentTo(self.land)

    def clear(self):
        """Удаляет все блоки карты и создает пустую основу"""
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        """
        Загружает карту из текстового файла и создаёт блоки.

        Args:
            filename (str): путь к текстовому файлу карты

        Returns:
            tuple: размеры карты (ширина, высота)
        """
        self.clear()
        y = 0
        with open(filename, "r") as file:
            for line in file:
                x = 0
                for z_str in line.strip().split():
                    height = int(z_str)
                    for z0 in range(height + 1):
                        self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y
