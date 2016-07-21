'''
THE LEGEND
By Sigton

Platforms:
Managing tiles and platforms
'''

import pygame
from pygame.locals import *

import constants, spritesheet

GRASS = (0,0,32,32)
DIRT = (32,0,32,32)
ROCK = (64,0,32,32)
MOSSY_ROCK = (96,0,32,32)
COBBLE = (128,0,32,32)
MOSSY_COBBLE = (160,0,32,32)
PLANKS_LIGHT = (192,0,32,32)
PLANKS_DARK = (224,0,32,32)
TRUNK_LIGHT = (0,32,32,32)
TRUNK_DARK = (32,32,32,32)
LEAVES_LIGHT = (64,32,32,32)
LEAVES_DARK = (96,32,32,32)
BRICKS = (128,32,32,32)
THATCH = (160,32,32,32)
GLASS = (192,32,32,32)
WATER = (
         (0,64,32,32),
         (32,64,32,32)
        )
LAVA = (
         (64,64,32,32),
         (96,64,32,32)
        )
SPIKE_1 = (128,64,32,32)
SPIKE_2 = (160,64,32,32)
TALL_GRASS_1 = (0,96,32,32)
TALL_GRASS_2 = (32,96,32,32)
TALL_GRASS_3 = (96,96,32,32)
FLOWER = (64,96,32,32)
GEM = (224,32,32,32)
DOOR_1 = (192,64,32,32)
DOOR_2 = (224,64,32,32)

platforms = (
    GRASS,
    DIRT,
    ROCK,
    MOSSY_ROCK,
    COBBLE,
    MOSSY_COBBLE,
    PLANKS_LIGHT,
    PLANKS_DARK,
    TRUNK_LIGHT,
    TRUNK_DARK,
    LEAVES_LIGHT,
    LEAVES_DARK,
    BRICKS,
    THATCH,
    GLASS,
    WATER,
    LAVA,
    SPIKE_1,
    SPIKE_2,
    TALL_GRASS_1,
    TALL_GRASS_2,
    TALL_GRASS_3,
    FLOWER,
    GEM,
    DOOR_1,
    DOOR_2
    )

class Platform(pygame.sprite.Sprite):
    ''' A tile displayed on screen '''

    def __init__(self, spriteSheetData):
        ''' Platform contructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        spriteSheet = spritesheet.SpriteSheet("resources/images/terrain.png")

        # Take the image from the spritesheet
        self.image = spriteSheet.get_image(spriteSheetData[0],
                                           spriteSheetData[1],
                                           spriteSheetData[2],
                                           spriteSheetData[3])

        self.rect = self.image.get_rect()

class AnimatedPlatform(pygame.sprite.Sprite):

    def __init__(self, spriteSheetData):
        ''' Constructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        spriteSheet = spritesheet.SpriteSheet("resources/images/terrain.png")

        self.images = []

        # Take the image for each srite from the spritesheet
        # and add it to the list of frames

        for sprite in spriteSheetData:
            newImage = spriteSheet.get_image(sprite[0],
                                             sprite[1],
                                             sprite[2],
                                             sprite[3])
            self.images.append(newImage)

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # A timer var for the animation

        self.tick = 0
        self.costume = 0

    def update(self):

        self.tick += 1

        if self.tick % 10 == 0:
            self.costume = (self.costume + 1) % len(self.images)
            self.image = self.images[self.costume]
