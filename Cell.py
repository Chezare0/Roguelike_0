from ursina import *


class Cell(Entity):
    def __init__(self, position, is_wall=False, model="cube", texture="brick"):
        super().__init__()
        self.is_wall = is_wall
        self.model = model if is_wall else "quad"
        self.texture = texture if is_wall else "grass"
        self.color = color.white
        self.scale_x = 0.5
        self.scale_y = 0.5
        self.scale_z = 0.5
        self.position = position
        if is_wall:
            self.collider = 'box'
        else:
            self.position_z = -1
