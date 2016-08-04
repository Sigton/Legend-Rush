'''
LEGEND RUSH
By Sigton

Blob:
Another enemy for the player to fight.
'''

import pygame
from pygame.locals import *

import constants, spritesheet, player, level
import math

class Blob(pygame.sprite.Sprite):
    ''' Blob class for the player to fight '''

    ''' Attributes '''
    
    walkingFramesR = []
    walkingFramesL = []

    # Set speed vector

    xv = 0
    yv = 0

    direction = "R"

    canRun = False
    canJump = False
    jumping = False

    jumpDelay = 0

    # Other sprites to interact with

    player = None
    level = None

    knockback = 0
    attackedPlayer = False

    ''' Methods '''

    def __init__(self):

        ''' Constructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the images
        self.spriteSheet = spritesheet.SpriteSheet("resources/images/blob2.png")

        # Grab the sprites
        self.imageR = self.spriteSheet.get_image(0,0,43,33)
        self.imageL = pygame.transform.flip(self.imageR, True, False)

        self.image = self.imageR

        self.rect = self.image.get_rect()

    def update(self):

        ''' Updates the blob each frame '''

        # Gravity
        self.calc_gravity()

        # Momentum
        self.xv *= constants.IMP_FRICTION
        if abs(self.xv) <= 0.5:
            self.xv = 0
        
        self.rect.x += self.xv

        # Collision detection (x)

        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in blockHitList:
            if block.rect.x > self.rect.x:
                self.rect.right = block.rect.left
            elif block.rect.x < self.rect.x:
                self.rect.left = block.rect.right
            self.xv = 0

        if self.dist_to(self.player.rect.x, self.player.rect.y) < constants.BLOB_FOLLOW_DISTANCE:
            self.canRun = True
        else:
            self.canRun = False

        # Knockback        
        self.attackedPlayer = self.attacked_player()

        self.do_knockback()

        self.rect.y += self.yv

        # Collision detection (y)

        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in blockHitList:
            if block.rect.y > self.rect.y:
                self.rect.bottom = block.rect.top
            elif block.rect.y < self.rect.y:
                self.rect.top = block.rect.bottom
            self.yv = 0

       # Knockback        
        self.attackedPlayer = self.attacked_player()

        self.do_knockback() 

        # Set direction
        
        if not self.jumping and self.knockback <= 0:
            if self.rect.x < self.player.rect.x:
                self.direction = "R"
            else:
                self.direction = "L"
                
        # If jump not on progress, try to jump

        if self.on_ground():
            self.canJump = True
            self.jumping = False
            if self.jumpDelay < 0:
                self.jumpDelay = 30
                self.canJump = False
        else:
            self.canJump = False

        if self.jumpDelay > 0:
            self.jumpDelay -= 1
        else:
            if self.knockback <= 0:
                if self.canJump and self.canRun and not self.jumping:
                    self.jump()

        if self.knockback > 0: self.knockback -= 1
        else:
            if self.jumping:
                if self.direction == "R":
                    self.xv = constants.BLOB_SPEED
                else:
                    self.xv = -constants.BLOB_SPEED
        
    def calc_gravity(self):

        ''' Calculates the effect of gravity on the blob '''

        if self.yv == 0:
            self.yv = 1
        else:
            self.yv += constants.BLOB_GRAVITY # Blobs have slightly less gravity than players

        # See if we hit the bottom of the screen

        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.yv >= 0:
            self.yv = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def on_ground(self):

        ''' Checks if the sprite is touching the ground '''

        # Move down 2 pixels, take a reading then move back up
        self.rect.y += 2
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y -= 2

        # Then check if we hit a platform
        if len(blockHitList) > 0:
            return True
        else:
            return False

    def dist_to(self, x, y):

        dx = x - self.rect.x
        dy = y - self.rect.y

        dist = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        return dist

    def jump(self):

        # Makes the blob jump if there is no obstacle in the way
        
        if self.can_jump():
            self.jumping = True
            self.yv = -constants.BLOB_JUMP_HEIGHT
            self.jumpDelay -= 1

    def touching_player(self):

        # Detects whether the blob is touching the player
        playerTouchingList = pygame.sprite.spritecollide(self, self.level.entityList, False)
        if len(playerTouchingList) > 0:
            # If touching players sword return true
            return True
        else:
            return False

    def can_jump(self):

        ''' Checks if there are any obstacles in the area the blob will land '''

        # Take record of old x,y to return to later
        
        oldX = self.rect.x
        oldY = self.rect.y
        
        # First move along 96px (Jump distance)
        if self.direction == "R":
            self.rect.x += 96
        else:
            self.rect.x -= 96

        # Iterate until touching an obstacle

        touchingObs = None
        while touchingObs == None:

            self.rect.y += 32
            if self.on_ground():

                obsHitList = pygame.sprite.spritecollide(self, self.level.obstacleList, False)

                if len(obsHitList) > 0:
                    touchingObs = False
                else:
                    touchingObs = True       
        
        # Then move back to original position
        self.rect.x = oldX
        self.rect.y = oldY

        return touchingObs

    def attacked_player(self):

        # Detectts whether the blob is attacking the player
        self.playerGroup = pygame.sprite.GroupSingle(sprite=self.player)
        playerTouchingList = pygame.sprite.spritecollide(self, self.playerGroup, False)
        if len(playerTouchingList) > 0:
            # If touching player return true
            return True
        else:
            return False

    def do_knockback(self):

        ''' Blobs also knockback after hitting the player '''

        # If the imp has just attacked the player:
        if self.player.impAttack and self.attackedPlayer:

            # Check direction
            if self.direction == "R":
                # Then set velocity to the opposite of the way it's facing
                self.xv = -15

            else:
                # And same again
                self.xv = 15

            # Float slightly into the air
            self.knockback = 80
            self.player.impAttack = False

            # Move out of the way to stop collision bugs
            self.rect.x += self.xv
            self.rect.y += self.yv

























        
