import pygame, random
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


class SlimeSpawner:

    def __init__(self, x, y, all_sprites, collision_sprites, enemy_sprites, player, spawners):

        self.x = x
        self.y = y
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites
        self.player = player
        self.spawners = spawners

        self.spawn_interval = SPAWNER_INTERVAL
        self.max_slimes = SPAWNER_MAX_ENEMIES
        self.global_cap = SPAWNER_GLOBAL_MAX

        self.slime_variants = [Slime, FireSlime, WaterSlime, EarthSlime, AirSlime]

        self.max_waves = SPAWNER_MAX_WAVES
        self.wave_count = 0

        self.spawned_slimes = []
        self.slime_spawn_count = 0
        self.next_spawn_time = 0

        self.wave_active = False

    def spawn_wave(self):

        if self.wave_count >= self.max_waves:

            self.delete_spawner()
            return

        self.wave_active = True
        self.spawned_slimes = []
        self.slime_spawn_count = 0
        self.next_spawn_time = pygame.time.get_ticks()
        self.wave_count += 1

    def spawn(self):

        current_time = pygame.time.get_ticks()

        if self.wave_active and self.slime_spawn_count < self.max_slimes and current_time >= self.next_spawn_time:

            slime_variant = random.choice(self.slime_variants)
            slime = slime_variant(
                (self.x, self.y),
                (self.all_sprites, self.enemy_sprites),
                self.player,
                self.collision_sprites,
                self.enemy_sprites
            )
            self.spawned_slimes.append(slime)
            self.slime_spawn_count += 1
            self.next_spawn_time = current_time + self.spawn_interval

    def update(self):

        self.spawned_slimes = [slime for slime in self.spawned_slimes if slime.alive]

        if not self.spawned_slimes and self.slime_spawn_count >= self.max_slimes:

            self.wave_active = False

        if not self.wave_active:

            self.spawn_wave()

        self.spawn()

    def delete_spawner(self):

        self.spawners.remove(self)



class TileMap:

    def __init__(self, display_surface, path, all_sprites, collision_sprites, enemy_sprites, interactables_sprites):

        self.display_surface = display_surface
        self.player = None
        self.tile_map = load_pygame(path)
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites
        self.interactables_sprites = interactables_sprites
        self.spawners = []

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

            if entity.name == 'slime_spawner':

                spawner = SlimeSpawner(entity.x, entity.y, self.all_sprites, self.collision_sprites, self.enemy_sprites, self.player, self.spawners)
                self.spawners.append(spawner)

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