import pygame
from os import walk
from os.path import join
from const import *
from pytmx import load_pygame
from sprites import Sprite, CollisionSprite
from player import Player
from enemy import Slime

class TileMap:

    def __init__(self, path, all_sprites, collision_sprites, enemy_sprites):

        self.player = None
        self.tile_map = load_pygame(path)
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites

        self.enemy_spawn_positions = []
        self.enemy_frames = {}

    def load_tilemap(self):

        for x, y, image in self.tile_map.get_layer_by_name('terrain').tiles():
            if image:
                Sprite((x * TILE_SIZE, y * TILE_SIZE), self.all_sprites, image) # const.py

        for gameObject in self.tile_map.get_layer_by_name('objects'):
            if gameObject.image:
                CollisionSprite((gameObject.x, gameObject.y), (self.all_sprites, self.collision_sprites), gameObject.image)

        for x, y, image in self.tile_map.get_layer_by_name('map_wall').tiles():
            if image:
                CollisionSprite((x * TILE_SIZE, y * TILE_SIZE), (self.all_sprites, self.collision_sprites), image) # const.py

        for entity in self.tile_map.get_layer_by_name('entities'):
            if entity.name == 'Player':
                self.player = Player((entity.x, entity.y), self.all_sprites, self.collision_sprites)

            if entity.name == 'Slime':
                Slime((entity.x, entity.y), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

    def load_enemies(self):

        folders = list(walk(join('assets', 'sprites', 'enemies')))[0][1]
        for folder in folders:
            for folder_path, _, file_names in walk(join('assets', 'sprites', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surface = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surface)