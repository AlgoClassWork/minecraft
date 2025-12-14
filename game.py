from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero


class Game(ShowBase):
    def __init__(self):
        """Инициализация игры"""
        super().__init__()  # Корректный вызов родительского конструктора

        # Создаём менеджер карты и загружаем уровень
        self.land = Mapmanager()
        map_width, map_height = self.land.loadLand("land.txt")

        # Создаём героя в центре карты
        hero_start_pos = (
            map_width // 2,
            map_height // 2,
            2
        )
        self.hero = Hero(hero_start_pos, self.land)

        # Настройка камеры
        base.camLens.setFov(90)


# Точка входа в программу
game = Game()
game.run()
