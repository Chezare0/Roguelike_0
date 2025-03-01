import json

from ursina import *


class Cell(Entity):
    def __init__(self, position, is_wall=False):
        super().__init__()
        self.is_wall = is_wall
        self.model = "cube" if is_wall else "quad"
        self.texture = "brick" if is_wall else "grass"
        self.color = color.white
        self.scale_x = 0.5
        self.scale_y = 0.5
        self.scale_z = 0.5
        self.position = position
        if is_wall:
            self.collider = 'box'
        else:
            self.position_z = -1


class Game(Entity):
    def __init__(self):
        super().__init__()
        # self.camera = Entity(parent=camera.ui, position=(0, 0, -5), rotation=(0, 0, 0))
        self.grid = []
        self.create_grid_from_file(r'src\room_test1.json')  # Загрузка комнаты из JSON файла
        # self.create_grid()
        self.player = Entity(collider='box', model="cube", texture="player.png", scale=0.5, position=(0, 0, 0))
        self.player_speed = 5

    def create_grid_from_file(self, filename):
        if not os.path.isfile(filename):
            print(f"Файл {filename} не найден.")
            return

        with open(filename, 'r') as file:
            data = json.load(file)

        for cell_data in data['cells']:
            position = tuple(cell_data['position'])
            is_wall = cell_data.get('is_wall', False)
            cell = Cell(position=(position[0] * 0.5, position[1] * 0.5), is_wall=is_wall)
            self.grid.append(cell)

    def create_grid(self):
        for x in range(-3, 4):
            for y in range(-3, 4):
                is_wall = (x == -3 or x == 3 or y == -3 or y == 3)
                self.grid.append(Cell(position=(x * 0.5, y * 0.5), is_wall=is_wall))

    def update(self):
        if held_keys["a"]:
            self.player.x -= self.player_speed * time.dt
            for cell in self.grid:
                if cell.is_wall:
                    if self.player.intersects(cell).hit:
                        self.player.x += self.player_speed * time.dt
        if held_keys["d"]:
            self.player.x += self.player_speed * time.dt
            for cell in self.grid:
                if cell.is_wall:
                    if self.player.intersects(cell).hit:
                        self.player.x -= self.player_speed * time.dt
        if held_keys["s"]:
            self.player.y -= self.player_speed * time.dt
            for cell in self.grid:
                if cell.is_wall:
                    if self.player.intersects(cell).hit:
                        self.player.y += self.player_speed * time.dt
        if held_keys["w"]:
            self.player.y += self.player_speed * time.dt
            for cell in self.grid:
                if cell.is_wall:
                    if self.player.intersects(cell).hit:
                        self.player.y -= self.player_speed * time.dt
        # self.camera.position = (self.player.x, self.player.y, self.player.z - 5)
        # self.camera.look_at(self.player)
        camera.position = (self.player.x, self.player.y, self.player.z - 15)
        camera.look_at(self.player)


if __name__ == "__main__":
    app = Ursina()
    window.windowed_size = window.fullscreen_size
    window.position = Vec2(0, 0)
    game = Game()
    app.run()
