'''
THE LEGEND
By Sigton

Level:
Gerneric level parent class
'''

import pygame
from pygame.locals import *

import constants, spritesheet, platforms, imp, terrain, os, blob
import player as p

class Level():

    # List of sprites

    platformList = None
    cosmeticLit = None
    obstacleList = None
    liquidList = None
    impList = None
    entityList = None
    checkpointList = None

    player = None
    
    # Background image
    background = None

    # How far the level has been scrolled
    worldShift = 0

    def __init__(self, player):

        ''' Constructor '''

        self.platformList = pygame.sprite.Group()
        self.cosmeticList = pygame.sprite.Group()
        self.obstacleList = pygame.sprite.Group()
        self.liquidList = pygame.sprite.Group()
        self.impList = pygame.sprite.Group()
        self.entityList = pygame.sprite.Group()
        self.checkpointList = pygame.sprite.Group()

        self.player = player

    def update(self):
        # Update everything on this level

        self.platformList.update()
        self.cosmeticList.update()
        self.liquidList.update()
        self.impList.update()
        self.entityList.update()
        self.checkpointList.update()

    def draw(self, display):
        # Draw everything on this level

        # Draw the background
        # The background doesn't scroll as far as the sprites
        # to give a feeling of depth

        display.fill(constants.BLUE)
        display.blit(self.background, (self.worldShift // 3,0))

        # Draw all the sprite lists
        self.platformList.draw(display)
        self.cosmeticList.draw(display)
        self.obstacleList.draw(display)
        self.liquidList.draw(display)
        self.checkpointList.draw(display)

    def shift_world(self, shift_x):
        ''' When the player moves left/right we need to scroll the level '''

        self.worldShift += shift_x

        # Make sure we don't scroll too far
        if self.worldShift >= 0:
            self.worldShift = 0
        elif self.worldShift <= -3860:
            self.worldShift = -3860
        else:
            # Otherwise shift all sprites
            for platform in self.platformList:
                platform.rect.x += shift_x
            for liquid in self.liquidList:
                liquid.rect.x += shift_x
            for imp in self.impList:
                imp.rect.x += shift_x
            for cosmetic in self.cosmeticList:
                cosmetic.rect.x += shift_x
            for checkpoint in self.checkpointList:
                checkpoint.rect.x += shift_x

    def reset_world(self):

        ''' Reset the scrolling '''

        # Move the platforms back to thier original position

        for platform in self.platformList:
            platform.rect.x -= self.worldShift
        for liquid in self.liquidList:
            liquid.rect.x -= self.worldShift
        for imp in self.impList:
            imp.rect.x -= self.worldShift
        for cosmetic in self.cosmeticList:
            cosmetic.rect.x -= self.worldShift
        for checkpoint in self.checkpointList:
            checkpoint.rect.x -= self.worldShift

        # Then reset the world shift

        self.worldShift = 0

    def create_platform(self, tile, x, y):
        platform = platforms.Platform(tile)
        platform.rect.x = x
        platform.rect.y = y
        self.platformList.add(platform)

    def create_cosmetic(self, tile, x, y):
        platform = platforms.Platform(tile)
        platform.rect.x = x
        platform.rect.y = y
        self.cosmeticList.add(platform)

    def create_liquid(self, tile, x, y, isDangerous=False):
        platform = platforms.AnimatedPlatform(tile)
        platform.rect.x = x
        platform.rect.y = y
        self.liquidList.add(platform)
        if isDangerous:
            self.obstacleList.add(platform)

    def create_obstacle(self, tile, x, y):
        obs = platforms.Platform(tile)
        obs.rect.x = x
        obs.rect.y = y
        self.platformList.add(obs)
        self.obstacleList.add(obs)

    def create_imp(self, x, y):

        newImp = imp.Imp()

        newImp.level = self
        newImp.player = self.player

        newImp.rect.x = x
        newImp.rect.y = y

        self.impList.add(newImp)

    def create_blob(self, x, y):

        newBlob = blob.Blob()

        newBlob.level = self
        newBlob.player = self.player

        newBlob.rect.x = x
        newBlob.rect.y = y

        self.impList.add(newBlob)

    def create_checkpoint(self, tile, x, y):
        checkpoint = platforms.Platform(tile)
        checkpoint.rect.x = x
        checkpoint.rect.y = y
        self.checkpointList.add(checkpoint)

    def render(self, data):

        ''' Creates instances of all the tiles stored in the JSON file '''

        # Iterate and parse

        for tile in data:
            coords = tile[0]
            tileData = tile[1]
    
            if tileData['tile'] == 17: # First deal with special cases
                self.create_liquid(platforms.platforms[16], coords[0]*32, (coords[1]*32)+24, True)
                
            else:
                if tileData['type'] == "Solid":
                    self.create_platform(platforms.platforms[tileData['tile']-1], coords[0]*32, (coords[1]*32)+24)

                elif tileData['type'] == "Cosmetic":
                    self.create_cosmetic(platforms.platforms[tileData['tile']-1], coords[0]*32, (coords[1]*32)+24)    

                elif tileData['type'] == "Liquid":
                    self.create_liquid(platforms.platforms[tileData['tile']-1], coords[0]*32, (coords[1]*32)+24)

                elif tileData['type'] == "Obstacle":
                    self.create_obstacle(platforms.platforms[tileData['tile']-1], coords[0]*32, (coords[1]*32)+24)

                elif tileData['type'] == "Checkpoint":
                    self.create_checkpoint(platforms.platforms[tileData['tile']-1], coords[0]*32, (coords[1]*32)+24)

                elif tileData['type'] == "Enemy":
                    if tileData['tile'] == 27:
                        self.create_imp(coords[0]*32, (coords[1]*32)-14)
                    elif tileData['tile'] == 28:
                        self.create_blob(coords[0]*32, (coords[1]*32)-15)
                else:
                    continue

''' Levels for the platformer '''
        
class Level_01(Level):

    def __init__(self, player, write_data=False):
        ''' Create level 1 '''

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/images/background_01.png").convert()

        savefile = os.path.join("level_data", "level1", "data.json")
        tilefile = os.path.join("level_data", "level1", "tiles.png")
        typefile = os.path.join("level_data", "level1", "types.png")

        # Create an instance of the LevelData class

        level = terrain.LevelData(savefile, tilefile, typefile)
        if write_data:
            level.write_data()
            
        # Load the data
        levelData = level.load_data()

        # Then render it
        self.render(levelData)

class Level_02(Level):

    def __init__(self, player, write_data=False):
        ''' Create level 2 '''

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/images/background_01.png").convert()

        savefile = os.path.join("level_data", "level2", "data.json")
        tilefile = os.path.join("level_data", "level2", "tiles.png")
        typefile = os.path.join("level_data", "level2", "types.png")

        # Create an instance of the LevelData class

        level = terrain.LevelData(savefile, tilefile, typefile)
        if write_data:
            level.write_data()

        # Load the data
        levelData = level.load_data()

        # Then render it
        self.render(levelData)

class Level_03(Level):

    def __init__(self, player, write_data=False):
        ''' Create level 3 '''

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/images/background_01.png").convert()

        savefile = os.path.join("level_data", "level3", "data.json")
        tilefile = os.path.join("level_data", "level3", "tiles.png")
        typefile = os.path.join("level_data", "level3", "types.png")

        # Create an instance of the LevelData class

        level = terrain.LevelData(savefile, tilefile, typefile)
        if write_data:
            level.write_data()
            
        # Load the data
        levelData = level.load_data()

        # Then render it
        self.render(levelData)

class Level_04(Level):

    def __init__(self, player, write_data=False):
        ''' Create level 4 '''

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/images/background_01.png").convert()

        savefile = os.path.join("level_data", "level4", "data.json")
        tilefile = os.path.join("level_data", "level4", "tiles.png")
        typefile = os.path.join("level_data", "level4", "types.png")

        # Create an instance of the LevelData class

        level = terrain.LevelData(savefile, tilefile, typefile)
        if write_data:
            level.write_data()
            
        # Load the data
        levelData = level.load_data()

        # Then render it
        self.render(levelData)

class Level_05(Level):

    def __init__(self, player, write_data=False):

        ''' Create level 5 '''

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/images/background_01.png").convert()

        savefile = os.path.join("level_data", "level5", "data.json")
        tilefile = os.path.join("level_data", "level5", "tiles.png")
        typefile = os.path.join("level_data", "level5", "types.png")

        # Create an instance of the LevelData class

        level = terrain.LevelData(savefile, tilefile, typefile)

        if write_data:
            level.write_data()

        # Load the data
        levelData = level.load_data()

        # Then render it
        self.render(levelData)

class Level_06(Level):

    def __init__(self, player, write_data=False):

        ''' Create level 6 '''

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/images/background_01.png").convert()

        savefile = os.path.join("level_data", "level6", "data.json")
        tilefile = os.path.join("level_data", "level6", "tiles.png")
        typefile = os.path.join("level_data", "level6", "types.png")

        # Create an instance of the LevelData class

        level = terrain.LevelData(savefile, tilefile, typefile)

        if write_data:
            level.write_data()

            # Load the data
            levelData = level.load_data()

            # Then render it
            self.render(levelData)

