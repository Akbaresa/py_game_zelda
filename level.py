import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import UI
class Level:
    def __init__(self):
        
        # get display surface
        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # attack sprite
        self.current_attack = None
        
        # sprite setup
        self.create_map()
        
        # user interface 
        self.ui = UI()
        
    
    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass' : import_csv_layout('./map/map_Grass.csv'),
            'object' : import_csv_layout('./map/map_Objects.csv')
        }
        
        graphics = {
            'grass' : import_folder('./graphics/Grass'),
            'objects' : import_folder('./graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            # buat lantai rumput
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            # buat object lantai
                            surface = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)
        
        self.player = Player(
            (2000,1430), 
            [self.visible_sprites], 
            self.obstacle_sprites, 
            self.create_attack, 
            self.destroy_attack,
            self.create_magic
            )
  
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])
    
    def create_magic(self, style, strength , cost):
        print(style)
        print(strength)
        print(cost)
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def run(self): 
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        # debug(self.player.status)
        
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)
        
        # buat lantai
        self.floor_surface = pygame.image.load('./graphics/tilemap/ground.png').convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
        
        
    def custom_draw(self, player):
        
        # get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # gambar lantai
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
