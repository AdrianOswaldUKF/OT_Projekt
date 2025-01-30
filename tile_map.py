from const import *
from pytmx import load_pygame
from sprites import Sprite, CollisionSprite
from player import Player
from enemy import Slime, FireSlime, WaterSlime, EarthSlime, AirSlime
from object import Chest
from sword import FireSword, WaterSword, BasicSword, EarthSword, AirSword

basic_sword = BasicSword()
water_sword = WaterSword()
fire_sword = FireSword()
earth_sword = EarthSword()
air_sword = AirSword()

class TileMap:

    def __init__(self, display_surface, path, all_sprites, collision_sprites, enemy_sprites, interactables_sprites):

        self.display_surface = display_surface
        self.player = None
        self.tile_map = load_pygame(path)
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites
        self.interactables_sprites = interactables_sprites

    def load_tilemap(self):

        for x, y, image in self.tile_map.get_layer_by_name('terrain').tiles():
            if image:
                Sprite((x * TILE_SIZE, y * TILE_SIZE), self.all_sprites, image) # const.py

        #for gameObject in self.tile_map.get_layer_by_name('objects'):
            #if gameObject.image:
                #CollisionSprite((gameObject.x, gameObject.y), (self.all_sprites, self.collision_sprites), gameObject.image)

        for entity in self.tile_map.get_layer_by_name('entities'):
            if entity.name == 'player':
                self.player = Player((entity.x, entity.y), self.all_sprites, self.collision_sprites, self.interactables_sprites, self.enemy_sprites)

            if entity.name == 'enemy_slime':
                Slime((entity.x, entity.y), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites, self.enemy_sprites)

            if entity.name == 'chest':
                Chest((entity.x, entity.y), (self.all_sprites, self.collision_sprites, self.interactables_sprites), self.player, basic_sword, self.collision_sprites)

            if entity.name == 'chest2':
                Chest((entity.x, entity.y), (self.all_sprites, self.collision_sprites, self.interactables_sprites), self.player, air_sword, self.collision_sprites)

            if entity.name == 'chest3':
                Chest((entity.x, entity.y), (self.all_sprites, self.collision_sprites, self.interactables_sprites), self.player, water_sword, self.collision_sprites)

            if entity.name == 'chest4':
                Chest((entity.x, entity.y), (self.all_sprites, self.collision_sprites, self.interactables_sprites), self.player, fire_sword, self.collision_sprites)

            if entity.name == 'chest5':
                Chest((entity.x, entity.y), (self.all_sprites, self.collision_sprites, self.interactables_sprites), self.player, earth_sword, self.collision_sprites)


        for x, y, image in self.tile_map.get_layer_by_name('map_border').tiles():
            if image:
                CollisionSprite((x * TILE_SIZE, y * TILE_SIZE), (self.all_sprites, self.collision_sprites), image)