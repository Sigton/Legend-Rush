'''
THE LEGEND
By Sigton

Imp:
Imp sprites for the player to battle
'''

import pygame
from pygame.locals import *

import constants, spritesheet, platforms, level
import player as p
import math

class Imp(pygame.sprite.Sprite):

    ''' Imp sprite to battle '''

    ''' Attributes '''

    # Set speed vector

    xv = 0

    direction = "R"

    # Arrays to hold the walking animations

    walkingFramesR = []
    walkingFramesL = []

    # Other sprites to interact with

    level = None
    player = None

    knockback = 0
    attackedPlayer = False

    def __init__(self):

        ''' Imp Constructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.spriteSheet = spritesheet.SpriteSheet("resources/images/Imp.png")

        # Load the images
        image = self.spriteSheet.get_image(0,0,37,70)
        self.walkingFramesR.append(image)
        self.imageR = image
        self.imageL = pygame.transform.flip(image, True, False)
        image = self.spriteSheet.get_image(37,0,37,70)
        self.walkingFramesR.append(image)
        image = self.spriteSheet.get_image(74,0,40,70)
        self.walkingFramesR.append(image)
        image = self.spriteSheet.get_image(114,0,41,70)
        self.walkingFramesR.append(image)
        image = self.spriteSheet.get_image(155,0,41,70)
        self.walkingFramesR.append(image)
        image = self.spriteSheet.get_image(196,0,41,70)
        self.walkingFramesR.append(image)
        image = self.spriteSheet.get_image(237,0,40,70)
        self.walkingFramesR.append(image)
        image = self.spriteSheet.get_image(277,0,46,70)
        self.walkingFramesR.append(image)
        image = self.spriteSheet.get_image(323,0,37,70)
        self.walkingFramesR.append(image)
        image = self.spriteSheet.get_image(360,0,37,70)

        for frame in self.walkingFramesR:
            image = pygame.transform.flip(frame, True, False)
            self.walkingFramesL.append(image)

        self.image = self.imageR

        self.rect = self.image.get_rect()

    def update(self):

        # Updates the imps status

        if self.knockback == 0:
            if self.rect.x < self.player.rect.x:
                self.direction = "R"
            else:
                self.direction = "L"

        if self.knockback > 0: self.knockback -= 1
        else:
            if self.dist_to(self.player.rect.x, self.player.rect.y) < constants.IMP_FOLLOW_DISTANCE and not self.on_edge():
                if self.direction == "R":
                    self.xv = constants.IMP_SPEED
                else:
                    self.xv = -constants.IMP_SPEED

        # If not next to player, move forward

        if not abs(self.player.rect.x - self.rect.x) <= 5:
            self.rect.x += self.xv
            self.xv *= constants.IMP_FRICTION
            if abs(self.xv) <= 0.5:
                self.xv = 0
        
            # Collision detection

            blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
            for block in blockHitList:
                if self.xv > 0:
                    self.rect.right = block.rect.left
                elif self.xv < 0:
                    self.rect.left = block.rect.right
                self.xv = 0

        else:
            self.xv = 0

        self.attackedPlayer = self.attacked_player()
        
        self.do_knockback()

        if abs(self.xv) > 0.5:
            if self.direction == "R":
                frame = (self.rect.x // 30) % len(self.walkingFramesR)
                self.image = self.walkingFramesR[frame]
            else:
                frame = (self.rect.x // 30) % len(self.walkingFramesL)
                self.image = self.walkingFramesL[frame]
        else:
            if self.direction == "R":
                self.image = self.imageR
            else:
                self.image = self.imageL

    def dist_to(self, x, y):

        # Gets the distance along a vector

        dx = x - self.rect.x
        dy = y - self.rect.y

        dist = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        return dist

    def touching_player(self):

        # Detects whether the imp is touching the player

        playerTouchingList = pygame.sprite.spritecollide(self, self.level.entityList, False)
        if len(playerTouchingList) > 0:
            # If touching players sword return true
            return True
        else:
            return False

    def attacked_player(self):

        # Detects whether the imp is attacking the player
        self.playerGroup = pygame.sprite.GroupSingle(sprite=self.player)
        playerTouchingList = pygame.sprite.spritecollide(self, self.playerGroup, False)
        if len(playerTouchingList) > 0:
            # If touching player return true
            return True
        else:
            return False

    def on_ground(self):

        ''' Checks if imp is on ground '''

        # Moves down 2 pixels and gets collision array

        self.rect.y += 2
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y -= 2

        # If something was hit then return true

        if len(blockHitList) > 0:
            return True
        else:
            return False

    def on_edge(self):

        ''' Checks if imp is on the edge of a platform '''

        # Moves along 32 pixels, then checks if on ground

        if self.direction == "R":

            # If imp is right-facing

            self.rect.x += 32
            onGround = self.on_ground()
            self.rect.x -= 32
            
            if onGround:

                # If there is a platform, then we are not on the edge so return false
                return False

            else:
                return True

        else:

            # If imp is facing left

            self.rect.x -= 32
            onGround = self.on_ground()
            self.rect.x += 32

            if onGround:

                # Same again
                return False

            else:
                return True

    def do_knockback(self):

        ''' The imp also knocks back after hitting the player '''

        # If the imp has just attacked the player:
        if self.player.impAttack and self.attackedPlayer:
            
            # Check direction
            if self.direction == "R":
                # Then set velocity to the opposite of the way its facing
                self.xv = -15

            else:
                # And same again
                self.xv = 15

            self.knockback = 50
            self.player.impAttack = False
            self.rect.x += self.xv
