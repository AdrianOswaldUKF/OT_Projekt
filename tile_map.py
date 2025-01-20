from const import *
from pytmx import load_pygame
from sprites import Sprite, CollisionSprite
from player import Player

class TileMap:

    def __init__(self, path, all_sprites, collision_sprites):

        self.player = None
        self.tile_map = load_pygame(path)
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites

    def load_map(self):

        tile_map = load_pygame(join('assets', 'map', 'tmx', 'map.tmx'))

        for x, y, image in tile_map.get_layer_by_name('terrain').tiles():
            if image:
                Sprite((x * TILE_SIZE, y * TILE_SIZE), self.all_sprites, image)

        for item in tile_map.get_layer_by_name('objects'):
            if item.image:
                CollisionSprite((item.x, item.y), (self.all_sprites, self.collision_sprites), item.image)

        for x, y, image in tile_map.get_layer_by_name('invisible_wall').tiles():
            if image:
                CollisionSprite((x * TILE_SIZE, y * TILE_SIZE), self.collision_sprites, image)

        for item in tile_map.get_layer_by_name('entities'):
            if item.name == 'Player':
                self.player = Player((item.x, item.y), self.all_sprites, self.collision_sprites)