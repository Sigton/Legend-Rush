'''
THE LEGEND
By Sigton

Player:
Playable player class.
'''

import pygame
from pygame.locals import *

import constants, spritesheet, platforms, level, tools, heart

class Player(pygame.sprite.Sprite):
    
    ''' Attributes '''

    # Set speed vector of player
    xv = 0
    yv = 0

    direction = "R"

    # Animation arrays
    walkingFramesL = []
    walkingFramesR = []

    # Sprites we can collide with
    level = None

    # Hearts
    heartList = None

    # Attacking attributes
    showSword = False
    attacking = 0
    sword = None

    # Shielding attributes
    showShield = False
    shielding = 0
    shield = None

    # Player's Health
    health = constants.PLAYER_HEALTH

    knockback = 0
    impAttack = False

    ''' Methods '''

    def __init__(self):
        ''' Constructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        spriteSheet = spritesheet.SpriteSheet("resources/images/player.png")

        # Load the static images

        self.standImgR = spriteSheet.get_image(0,0,27,62)
        self.jumpImgR = spriteSheet.get_image(113,0,30,69)
        self.fallImgR = spriteSheet.get_image(143,0,35,67)
        self.attackImgR = spriteSheet.get_image(178,0,33,62)

        self.standImgL = pygame.transform.flip(self.standImgR, True, False)
        self.jumpImgL = pygame.transform.flip(self.jumpImgR, True, False)
        self.fallImgL = pygame.transform.flip(self.fallImgR, True, False)
        self.attackImgL = pygame.transform.flip(self.attackImgR, True, False)

        # Load all the right-facing images into the list
        image = spriteSheet.get_image(0,0,27,62)
        self.walkingFramesR.append(image)
        image = spriteSheet.get_image(27,0,31,62)
        self.walkingFramesR.append(image)
        image = spriteSheet.get_image(58,0,27,62)
        self.walkingFramesR.append(image)
        image = spriteSheet.get_image(85,0,28,62)
        self.walkingFramesR.append(image)

        # Do the same, but flip them to left
        for frame in self.walkingFramesR:
            image = pygame.transform.flip(frame, True, False)
            self.walkingFramesL.append(image)

        # Set the starting image
        self.image = self.standImgR

        # Set a reference to the image rect
        self.rect = self.image.get_rect()

        # Load sounds
        self.jumpSound = pygame.mixer.Sound("resources/sounds/Jump Sound.wav")
        self.deathSound = pygame.mixer.Sound("resources/sounds/Death Sound.wav")
        self.attackSound = pygame.mixer.Sound("resources/sounds/Attack Sound.wav")
        self.jumpSound.set_volume(0.25)
        self.deathSound.set_volume(0.25)
        self.attackSound.set_volume(0.25)

        # Initiate the hearts
        self.heartList = pygame.sprite.Group()

        for n in range(int(constants.PLAYER_HEALTH/2)):
            newHeart = heart.Heart(n)
            newHeart.player = self
            self.heartList.add(newHeart)

    def update(self):
        ''' Move the player '''

        # Gravity
        self.calc_grav()

        # Momentum
        self.xv *= constants.PLAYER_FRICTION
        if abs(self.xv) <= 0.5:
            self.xv = 0
            
        # Move left/right

        self.rect.x += self.xv
        
        self.do_obs_hit()
                
        pos = self.rect.x + self.level.worldShift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walkingFramesR)
            self.image = self.walkingFramesR[frame]
        else:
            frame = (pos // 30) % len(self.walkingFramesL)
            self.image = self.walkingFramesL[frame]

        ''' Set costume '''

        if abs(self.xv) == 0:
            if self.attacking > 0:
                if self.direction == "R":
                    self.image = self.attackImgR
                else:
                    self.image = self.attackImgL
            else:
                if self.direction == "R":
                    self.image = self.standImgR
                else:
                    self.image = self.standImgL

        # See if we hit anything
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in blockHitList:
            # If we are moving right, set our right side to the left of the object we hit
            if self.xv > 0:
                self.rect.right = block.rect.left
            elif self.xv < 0:
                # Otherwise do the opposite
                self.rect.left = block.rect.right
                        
        # Move up/down
        self.rect.y += self.yv

        self.do_obs_hit() 
        
        # Check to see if we hit any platforms
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in blockHitList:

            # Reset our position based on the top/bottom of the object
            if self.yv > 0:
                self.rect.bottom = block.rect.top
            elif self.yv < 0:
                self.rect.top = block.rect.bottom

            # Stop vertical movement
            self.yv = 0
        
        ''' Set costume '''

        if len(blockHitList) == 0:
            if self.yv < 0:
                if self.direction == "R":
                    self.image = self.jumpImgR
                else:
                    self.image = self.jumpImgL
            else:
                if self.direction == "R":
                    self.image = self.fallImgR
                else:
                    self.image = self.fallImgL

        if self.attacking == 0 and self.showSword:
            self.level.entityList.remove(self.sword)
            self.sword = None
            self.showSword = False

        if self.shielding == 0 and self.showShield:
            self.level.entityList.remove(self.shield)
            self.shield = None
            self.showShield = False

        # Water physics

        self.water_physics()

        # Reset if we died

        if self.health <= 0:
            pygame.mixer.Sound.play(self.deathSound)
            self.reset()
            self.level.reset_world()

        # Update the hearts
        self.heartList.update()

    def calc_grav(self):
        ''' Calcualte the effect of gravity '''
        if self.yv == 0:
            self.yv = 1
        else:
            self.yv += constants.PLAYER_GRAVITY

        # See if we hit the ground

        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.yv >= 0:
            self.yv = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def on_ground(self):

        ''' Helper function to to check if we're on the ground '''

        # Moves down and takes record if there are any platforms below us

        self.rect.y += 2
        platformHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y -= 2

        # Then check if we hit a platform

        if len(platformHitList) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            # Then return if we are on the ground or not
            return True
        else:
            return False

    def jump(self, height):
        ''' Called when user hits jump button '''

        # If it is okay to jump, set our speed upwards
        if self.on_ground() and self.attacking == 0 and self.shielding == 0 and self.can_jump():
            self.yv = -height
            pygame.mixer.Sound.play(self.jumpSound)

    def attack(self):
        ''' Called when user hits the space-bar '''

        self.attacking = 15
        self.showSword = True
        self.sword = tools.Tool(self, "sword")
        self.level.entityList.add(self.sword)
        pygame.mixer.Sound.play(self.attackSound)

    def use_shield(self):
        ''' Called by user '''

        # Stops obstacles from doing damage and lessens knockback

        self.shielding = 20
        self.showShield = True
        self.shield = tools.Tool(self, "shield")
        self.level.entityList.add(self.shield)

    # Player-controlled movement
    def go_left(self,speed):
        ''' Called when user hits left key '''
        self.xv = -speed
        self.direction = "L"

    def go_right(self,speed):
        ''' Called when user hits right key '''
        self.xv = speed
        self.direction = "R"

    def reset(self):
        ''' Called when a death of level change occurs '''
        self.rect.x = 150
        self.rect.y = 400
        self.xv = 0
        self.yv = 0
        self.direction = "R"
        self.image = self.standImgR
        self.level.entityList.remove(self.sword)
        self.level.entityList.remove(self.shield)
        self.sword = None
        self.shield = None
        self.health = constants.PLAYER_HEALTH

    def hit_obstacle(self):

        ''' Obstacle collsiion detection '''

        obsHitList = pygame.sprite.spritecollide(self, self.level.obstacleList, False)

        # If touching an obstacle, return true

        if len(obsHitList) > 0:
            return True
        else:
            return False

    def hit_imp(self):

        ''' Detects when player has been attacked by an imp '''

        impHitList = pygame.sprite.spritecollide(self, self.level.impList, False)

        # If touching an imp, reset the world and player

        if len(impHitList) > 0:
            for imp in impHitList:
                if imp.rect.x < self.rect.x:
                    self.attackDir = "L"
                else:
                    self.attackDir = "R"
            return True
        else:
            return False

    def water_physics(self):
        ''' Deals with the physical properties of water '''

        # First check if the player is in water

        waterHitList = pygame.sprite.spritecollide(self, self.level.liquidList, False)
        if len(waterHitList) > 0:
            constants.PLAYER_SPEED = 2
            constants.PLAYER_JUMP_HEIGHT = 3
            constants.PLAYER_GRAVITY = 0.01
        else:
            constants.PLAYER_SPEED = 6
            constants.PLAYER_JUMP_HEIGHT = 10
            constants.PLAYER_GRAVITY = 0.35

    def touching_checkpoint(self):

        ''' Checks if the player is touching a checkpoint '''

        checkHitList = pygame.sprite.spritecollide(self, self.level.checkpointList, False)
        if len(checkHitList) > 0:
            return True
        else:
            return False

    def do_obs_hit(self):

        ''' Deals with hitting obstacles, imps, blobs etc '''

        # First of all, obstacles
        if self.hit_obstacle():
            
            if self.direction == "R":
                # If running to the right when hitting the obstacle, bounce to the left
                self.xv = -20

            else:
                # And vice-versa
                self.xv = 20
                
            self.yv = -5
            self.knockback = 20
            self.health -= 1

            # Move out of the way of the obstacle to stop collision errors
            self.rect.x += self.xv
            self.rect.y += self.yv

        # Then enemies

        # If just attacked by an Imp:
        if self.hit_imp():

            if self.attackDir == "R":
                # If running into the imp from the left, move the player back left
                self.xv = -20

            else:
                # And vice-versa
                self.xv = 20

            # Float slightly into the air
            self.yv = -5
            self.knockback = 30

            # If the shield is active imps do no damage, but still do knockback
            if self.shielding == 0:
                self.health -= 1
            self.impAttack = True

    def can_jump(self):

        ''' Tests to make sure the player can jump before jumping '''

        # Goes up one tile and makes sure there is nothing there

        self.rect.y -= 32
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y += 32

        if len(blockHitList) > 0:
            # If there is an object, the player can't jump so return false
            return False
        else:
            return True
