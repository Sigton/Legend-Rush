'''
THE LEGEND
By Sigton

Tools:
Items held by the player
'''

import pygame
from pygame.locals import *

import constants, spritesheet, platforms, level, player

class Tool(pygame.sprite.Sprite):

    ''' Items to be held by the player '''

    player = None

    def __init__(self, player, tool):

        ''' Constructor '''

        # Call the parents constructor

        pygame.sprite.Sprite.__init__(self)

        # Load images from the sprite sheet

        self.spriteSheet = spritesheet.SpriteSheet("resources/images/tools.png")

        # Then set the images

        self.imageSwordR = self.spriteSheet.get_image(0,0,45,18)
        self.imageSwordL = pygame.transform.flip(self.imageSwordR, True, False)

        self.imageShieldR = self.spriteSheet.get_image(47,0,25,43)
        self.imageShieldL = pygame.transform.flip(self.imageShieldR, True, False)

        if tool == "sword":
            self.imageR = self.imageSwordR
            self.imageL = self.imageSwordL
            self.xOff = 14
            self.yOff = 40
            
        elif tool == "shield":
            self.imageR = self.imageShieldR
            self.imageL = self.imageShieldL
            self.xOff = 8
            self.yOff = 24

        self.player = player

        if self.player.direction == "R":
            self.image = self.imageR
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.player.rect.x+self.xOff,self.player.rect.y+self.yOff)

        else:
            self.image = self.imageL
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.player.rect.x-self.xOff,self.player.rect.y+self.yOff)

    def update(self):

        # Make sure it's pointing in the right direction

        if self.player.direction == "R":
            self.image = self.imageR
            self.rect.topleft = (self.player.rect.x+self.xOff,self.player.rect.y+self.yOff)
        else:
            self.image = self.imageL
            self.rect.topleft = (self.player.rect.x-self.xOff,self.player.rect.y+self.yOff)
