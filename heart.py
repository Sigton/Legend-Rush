'''
THE LEGEND
By Sigton

Heart:
Represents the health of the player
'''

import pygame
from pygame.locals import *

import constants, spritesheet, player

class Heart(pygame.sprite.Sprite):

    ''' A heart to represent the health of the player '''

    state = 0 # 0 = full, 1 = half, 2 = empty

    spriteSheet = None

    images = []

    player = None

    ''' Methods '''
    
    def __init__(self,num):

        ''' Constructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.spriteSheet = spritesheet.SpriteSheet("resources/images/hearts.png")

        # Grab the sprites from the spritesheet
        image = self.spriteSheet.get_image(0,0,46,40)
        self.images.append(image)
        image = self.spriteSheet.get_image(46,0,46,40)
        self.images.append(image)
        image = self.spriteSheet.get_image(92,0,46,40)
        self.images.append(image)

        self.image = self.images[self.state]

        self.rect = self.image.get_rect()

        self.id = num

        # Set position
        self.rect.x = self.id*50+10
        self.rect.y = 10

    def update(self):

        ''' Updates the status of the heart '''

        self.upperLimit = (self.id*2)+2
        self.lowerLimit = (self.id*2)+1

        if self.player.health < self.upperLimit:
            if self.player.health == self.lowerLimit:
                self.state = 1
            else:
                self.state = 2
        else:
            self.state = 0

        self.image = self.images[self.state]





















        

    
