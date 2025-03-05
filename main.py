import json
from ursina import *
from Cell import *


class Game(Entity):
    def __init__(self):
        super().__init__()
        self.player = None
        self.grid = []
        self.create_grid_from_file(r'src\rooms\start_room.json', shift=(0, 0))  # Загрузка комнаты из JSON файла
        self.create_bridge(shift=(-30, 0), left=False, right=True, up=False, down=False)
        self.player_init()

    def player_init(self):
        self.player = Entity(collider='box', model="cube", texture=r"src\Assets\player.png", scale=0.4, position=(7.5, 7.5, 0))
        self.player.speed = 5
        self.player.max_health = 100
        self.player.health = 100

    def create_grid_from_file(self, filename, shift=(0, 0, 0)):
        if not os.path.isfile(filename):
            print(f"Файл {filename} не найден.")
            return

        with open(filename, 'r') as file:
            data = json.load(file)

        for cell_data in data['cells']:
            position = tuple(cell_data['position'])
            is_wall = cell_data.get('is_wall', False)
            cell = Cell(position=((position[0] + shift[0]) * 0.5, (position[1] + shift[1]) * 0.5), is_wall=is_wall)
            self.grid.append(cell)

    def create_grid(self):
        for x in range(-3, 4):
            for y in range(-3, 4):
                is_wall = (x == -3 or x == 3 or y == -3 or y == 3)
                self.grid.append(Cell(position=(x * 0.5, y * 0.5), is_wall=is_wall))

    def update(self):
        if held_keys["a"]:
            self.player.x -= self.player.speed * time.dt
            for cell in self.grid:
                if cell.is_wall:
                    if self.player.intersects(cell).hit:
                        self.player.x += self.player.speed * time.dt
        if held_keys["d"]:
            self.player.x += self.player.speed * time.dt
            for cell in self.grid:
                if cell.is_wall:
                    if self.player.intersects(cell).hit:
                        self.player.x -= self.player.speed * time.dt
        if held_keys["s"]:
            self.player.y -= self.player.speed * time.dt
            for cell in self.grid:
                if cell.is_wall:
                    if self.player.intersects(cell).hit:
                        self.player.y += self.player.speed * time.dt
        if held_keys["w"]:
            self.player.y += self.player.speed * time.dt
            for cell in self.grid:
                if cell.is_wall:
                    if self.player.intersects(cell).hit:
                        self.player.y -= self.player.speed * time.dt
        camera.position = (self.player.x, self.player.y, self.player.z - 15)
        camera.look_at(self.player)

    def create_bridge(self, shift, up=False, down=False, left=False, right=False):
        width_start, width_stop, height_start, height_stop = 0 + shift[0], 31 + shift[0], 0 + shift[1], 31 + shift[1]
        if left:
            x = (width_start - width_stop) // 2 - 1
            y = (height_stop - height_start) // 2
            cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
            self.grid.append(cell)
            for y in range((height_stop - height_start) // 2 - 1, (height_stop - height_start - 1) // 2 + 2):
                for x in range(width_start, (width_start - width_stop) // 2 - 1):
                    if y == (height_stop - height_start) // 2:
                        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
                    else:
                        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
                    self.grid.append(cell)
        else:
            x = (width_start - width_stop) // 2 - 1
            y = (height_stop - height_start) // 2
            cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
            self.grid.append(cell)

        if right:
            x = (width_start - width_stop) // 2 + 1
            y = (height_stop - height_start) // 2
            cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
            self.grid.append(cell)
            for y in range((height_stop - height_start) // 2 - 1, (height_stop - height_start - 1) // 2 + 2):
                for x in range((width_start - width_stop) // 2 + 2, width_stop):
                    if y == (height_stop - height_start) // 2:
                        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
                    else:
                        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
                    self.grid.append(cell)
        else:
            x = (width_start - width_stop) // 2 + 1
            y = (height_stop - height_start) // 2
            cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
            self.grid.append(cell)
        if up:
            x = (width_start - width_stop) // 2
            y = (height_stop - height_start) // 2 + 1
            cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
            self.grid.append(cell)
            for x in range((width_start - width_stop) // 2 - 1, (width_start - width_stop - 1) // 2 + 2):
                for y in range((height_stop - height_start) // 2 + 2, height_stop):
                    if x == (width_start - width_stop) // 2:
                        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
                    else:
                        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
                    self.grid.append(cell)
        else:
            x = (width_start - width_stop) // 2
            y = (height_stop - height_start) // 2 + 1
            cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
            self.grid.append(cell)
        if down:
            x = (width_start - width_stop) // 2
            y = (height_stop - height_start) // 2 - 1
            cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
            self.grid.append(cell)
            for x in range((width_start - width_stop) // 2 - 1, (width_start - width_stop - 1) // 2 + 2):
                for y in range(height_start, (height_stop - height_start) // 2 - 1):
                    if x == (width_start - width_stop) // 2:
                        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
                    else:
                        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
                    self.grid.append(cell)
        else:
            x = (width_start - width_stop) // 2
            y = (height_stop - height_start) // 2 - 1
            cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
            self.grid.append(cell)
        # center
        x = (width_start - width_stop) // 2
        y = (height_stop - height_start) // 2
        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=False)
        self.grid.append(cell)
        # left up center wall
        x = (width_start - width_stop) // 2 - 1
        y = (height_stop - height_start) // 2 + 1
        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
        self.grid.append(cell)
        # left down center wall
        x = (width_start - width_stop) // 2 - 1
        y = (height_stop - height_start) // 2 - 1
        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
        self.grid.append(cell)
        # right up center wall
        x = (width_start - width_stop) // 2 + 1
        y = (height_stop - height_start) // 2 + 1
        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
        self.grid.append(cell)
        # right down center wall
        x = (width_start - width_stop) // 2 + 1
        y = (height_stop - height_start) // 2 - 1
        cell = Cell(position=(x * 0.5, y * 0.5), is_wall=True)
        self.grid.append(cell)


if __name__ == "__main__":
    app = Ursina()
    window.windowed_size = window.fullscreen_size
    window.position = Vec2(0, 0)
    game = Game()
    app.run()
