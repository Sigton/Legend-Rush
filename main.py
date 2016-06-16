'''
The Legend: Platformer
V4.0.7 Beta
By Sigton
'''

import pygame
from pygame.locals import *

import random, math, sys

'''
Global Constants
'''

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Player stats
global PLAYER_SPEED, PLAYER_JUMP_HEIGHT, PLAYER_GRAVITY

PLAYER_SPEED = 6
PLAYER_JUMP_HEIGHT = 10
PLAYER_GRAVITY = 0.35

IMP_FOLLOW_DISTANCE = 600

# Key Definitions

K_ESCAPE = 27
K_FULLSCREEN = 292
K_SPACE = 32

'''
Class to pull individual sprites form sprite sheets
'''

class SpriteSheet(object):

    # Points to sprite sheet image
    sprite_sheet = None

    def __init__(self, filename):
        ''' Constructor. Pass in file name of sprite sheet'''

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        ''' Grab a single image out of a larger spritesheet'''

        # Create a new blank image
        image = pygame.Surface([width,height]).convert()

        # Coy the sprite form the spritesheet
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))

        # Assuming white works for transparency
        image.set_colorkey(WHITE)

        # Return the image
        return image

'''
Managing tiles and platforms
'''

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

class Platform(pygame.sprite.Sprite):
    ''' A tile displayed on screen '''

    def __init__(self, spriteSheetData):
        ''' Platform constructor '''

        pygame.sprite.Sprite.__init__(self)

        spriteSheet = SpriteSheet("terrain.png")
        # Take the image from the spritesheet
        self.image = spriteSheet.get_image(spriteSheetData[0],
                                           spriteSheetData[1],
                                           spriteSheetData[2],
                                           spriteSheetData[3])

        self.rect = self.image.get_rect()

class AnimatedPlatform(pygame.sprite.Sprite):

    def __init__(self, spriteSheetData):
        ''' Constructor '''

        pygame.sprite.Sprite.__init__(self)

        spriteSheet = SpriteSheet("terrain.png")

        self.images = []

        # Take the image for each sprite from the spritesheet
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

class Level():
    ''' Generic level parent class'''

    # Lists of sprites

    platformList = None
    obstacleList = None
    liquidList = None
    impList = None

    # Background image
    background = None

    # How far the level has been scrolled
    worldShift = 0
    levelLimit = -1000

    def __init__(self, player):

        ''' Constructor '''
        
        self.platformList = pygame.sprite.Group()
        self.obstacleList = pygame.sprite.Group()
        self.liquidList = pygame.sprite.Group()
        self.impList = pygame.sprite.Group()
        self.entityList = pygame.sprite.Group()

        self.player = player

    def update(self):
        # Update everything on this level
        
        self.platformList.update()

    def draw(self, display):
        # Draw everything on this level

        # Draw the background
        # The background doesn't scroll as far as the sprites
        # to give a feeling of depth

        display.fill(BLUE)
        display.blit(self.background, (self.worldShift // 3,0))

        # Draw all the sprite lists
        self.platformList.draw(display)

    def shift_world(self, shift_x):
        ''' When the player moves left/right we need to scroll the level '''

        self.worldShift += shift_x
        # Make sure we don't scroll too far
        if self.worldShift >= 0:
            self.worldShift = 0
        elif self.worldShift <= -3860:
            self.worldShift = -3860
        else:
            # otherwise shift all sprites
            for platform in self.platformList:
                platform.rect.x += shift_x
            for liquid in self.liquidList:
                liquid.rect.x += shift_x
            for imp in self.impList:
                imp.rect.x += shift_x

    def reset_world(self):

        ''' Reset the scrolling '''

        # Move platforms back to their original position

        for platform in self.platformList:
            platform.rect.x -= self.worldShift
        for liquid in self.liquidList:
            liquid.rect.x -= self.worldShift
        for imp in self.impList:
            imp.rect.x -= self.worldShift
            
        # Then reset the shift
        
        self.worldShift = 0

    def create_platform(self, tile, x, y, output):
        newPlatform = [tile,x,y]
        output.append(newPlatform)

    def create_liquid(self, tileData, x, y):
        newPlatform = AnimatedPlatform(tileData)
        newPlatform.rect.x = x
        newPlatform.rect.y = y
        self.liquidList.add(newPlatform)

    def create_obstacle(self, tile, x, y):
        obs = Platform(tile)
        obs.rect.x = x
        obs.rect.y = y
        self.obstacleList.add(obs)
        self.platformList.add(obs)

    def create_imp(self, x, y):
        
        imp = Imp()

        imp.level = self
        imp.player = player
        
        imp.rect.x = x
        imp.rect.y = y

        self.impList.add(imp)

        return imp

# Create platformers for the level
class Level_01(Level):

    def __init__(self, player):
        ''' Create level 1 '''

        Level.__init__(self, player)

        self.background = pygame.image.load("background_01.png").convert()
        self.levelLimit = -2500

        # Create an array with the type of platform, and x,y location of the platform
        level = []

        # Create the ground
        
        pos = 0
        for n in range(146):
            if n > 10 and n < 15:
                Level.create_liquid(self,WATER,pos,536)
            else:
                Level.create_platform(self,GRASS,pos,536,level)
            
            pos += 32
        pos = 0
        for n in range(146):
            Level.create_platform(self,DIRT,pos,568,level)
            pos += 32

        # Create platforms

        Level.create_platform(self,GRASS,1120,408,level)
        Level.create_platform(self,GRASS,1152,408,level)
        Level.create_platform(self,GRASS,1184,408,level)

        Level.create_platform(self,GRASS,1280,344,level)
        Level.create_platform(self,GRASS,1312,344,level)
        Level.create_platform(self,GRASS,1344,344,level)

        Level.create_platform(self,GRASS,1920,504,level)
        Level.create_platform(self,GRASS,1952,504,level)
        Level.create_platform(self,GRASS,1984,504,level)
        Level.create_platform(self,GRASS,2016,504,level)
        Level.create_platform(self,GRASS,2048,504,level)
        Level.create_platform(self,GRASS,2080,504,level)
        Level.create_platform(self,GRASS,2112,504,level)
        
        # Go through the above defined platforms and "make them solid"

        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platformList.add(block)

        # Create obstacles

        Level.create_obstacle(self, SPIKE_1, 800, 504)
        Level.create_obstacle(self, SPIKE_1, 832, 504)
        Level.create_obstacle(self, SPIKE_1, 928, 504)
        Level.create_obstacle(self, SPIKE_1, 960, 504)

class Player(pygame.sprite.Sprite):

    ''' Attributes '''
    # Set speed vector of player
    xv = 0
    yv = 0

    # Animation arrays
    walkingFramesL = []
    walkingFramesR = []

    direction = "R"

    # Sprites we can collide with
    level = None

    # Attacking attributes
    showSword = False
    attacking = 0
    sword = None

    # Shielding attributes
    showShield = False
    shielding = 0
    shield = None

    ''' Methods '''
    
    def __init__(self):
        ''' Constructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        spriteSheet = SpriteSheet("player.png")

        # Load the static images

        self.standImgR = spriteSheet.get_image(0,0,30,70)
        self.jumpImgR = spriteSheet.get_image(126,0,33,77)
        self.fallImgR = spriteSheet.get_image(159,0,39,75)
        self.attackImgR = spriteSheet.get_image(198,0,37,70)

        self.standImgL = pygame.transform.flip(self.standImgR, True, False)
        self.jumpImgL = pygame.transform.flip(self.jumpImgR, True, False)
        self.fallImgL = pygame.transform.flip(self.fallImgR, True, False)
        self.attackImgL = pygame.transform.flip(self.attackImgR, True, False)

        # Load all the right-facing images into the list
        image = spriteSheet.get_image(0,0,30,70)
        self.walkingFramesR.append(image)
        image = spriteSheet.get_image(30,0,35,70)
        self.walkingFramesR.append(image)
        image = spriteSheet.get_image(65,0,30,70)
        self.walkingFramesR.append(image)
        image = spriteSheet.get_image(95,0,31,70)
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
        self.jumpSound = pygame.mixer.Sound("Jump Sound.wav")
        self.deathSound = pygame.mixer.Sound("Death Sound.wav")
        self.attackSound = pygame.mixer.Sound("Attack Sound.wav")
        self.jumpSound.set_volume(0.25)
        self.deathSound.set_volume(0.25)
        self.attackSound.set_volume(0.25)
        
    def update(self):
        ''' Move the player '''

        # Gravity
        self.calc_grav()

        # Move left/right
        
        self.rect.x += self.xv

        if self.hit_obstacle():
            pygame.mixer.Sound.play(self.deathSound)
            self.reset()
            self.level.reset_world()
        
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

        if self.hit_obstacle() or self.hit_imp():
            pygame.mixer.Sound.play(self.deathSound)
            self.reset()
            self.level.reset_world()

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

        if self.shielding == 0 and self.showShield:
            self.level.entityList.remove(self.shield)
            self.shield = None
            
        # Water Physics

        self.water_physics()
        
    def calc_grav(self):
        ''' Calculate the effect of gravity '''
        if self.yv == 0:
            self.yv = 1
        else:
            self.yv += PLAYER_GRAVITY

        # See if we hit the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.yv >= 0:
            self.yv = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def on_ground(self):

        ''' Helper function to check if we're on the ground '''

        # Moves down and takes record if there are any platforms below us
        
        self.rect.y += 2
        platformHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y -= 2

        # Then checks if we hit a platform

        if len(platformHitList) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            # Then return if we are on the ground or not
            return True
        else:
            return False

    def jump(self,height):
        ''' Called when user hits jump button '''

        # If it is ok to jump, set our speed upwards
        if self.on_ground() and self.attacking == 0:
            self.yv = -height
            pygame.mixer.Sound.play(self.jumpSound)

    def attack(self):
        ''' Called when user hits the space-bar '''
        
        self.attacking = 15
        self.showSword = True
        self.sword = Tool(self,"sword")
        self.level.entityList.add(self.sword)
        pygame.mixer.Sound.play(self.attackSound)

    def use_shield(self):
        ''' Called by user '''

        # Stops projectiles from doing damage
        
        self.shielding = 20
        self.showShield = True
        self.shield = Tool(self,"shield")
        self.level.entityList.add(self.shield)
        
    # Player-controlled movement
    def go_left(self,speed):
        ''' Called when user hits left arrow '''
        self.xv = -speed
        self.direction = "L"

    def go_right(self,speed):
        ''' Called when user hits right arrow '''
        self.xv = speed
        self.direction = "R"

    def stop(self):
        ''' Called when user lets off the keyboard '''
        self.xv = 0

    def reset(self):
        ''' Called when a death or level change occurs '''
        self.rect.x = 150
        self.rect.y = 400
        self.xv = 0
        self.yv = 0
        self.direction = "R"
        self.image = self.standImgR
        self.level.entityList.remove(self.sword)
        self.sword = None

    def hit_obstacle(self):
        
        ''' Obstacle collision detection detection '''

        obsHitList = pygame.sprite.spritecollide(self, self.level.obstacleList, False)

        # If touching an obstacle, reset the world and player
        
        if len(obsHitList) > 0:
            hitObs = True
        else:
            hitObs = False

        return hitObs

    def hit_imp(self):

        ''' Detects when the player has been attacked by am imp '''

        impHitList = pygame.sprite.spritecollide(self, self.level.impList, False)

        # If touching an imp, reset the world and player

        if len(impHitList) > 0:
            impAttack = True
        else:
            impAttack = False

        return impAttack

    def water_physics(self):
        ''' Deals with the physical properties of water '''

        global PLAYER_SPEED, PLAYER_JUMP_HEIGHT, PLAYER_GRAVITY

        # First check if the player is in water

        waterHitList = pygame.sprite.spritecollide(self, self.level.liquidList, False)
        if len(waterHitList) > 0:
            PLAYER_SPEED = 2
            PLAYER_JUMP_HEIGHT = 3
            PLAYER_GRAVITY = 0.01
        else:
            PLAYER_SPEED = 6
            PLAYER_JUMP_HEIGHT = 10
            PLAYER_GRAVITY = 0.35

class Tool(pygame.sprite.Sprite):

    ''' Sword item for player to hold when attacking '''

    player = None

    def __init__(self, player, tool):

        ''' Constructor '''

        # Call the parents constructor

        pygame.sprite.Sprite.__init__(self)

        # Load images in from the player sprite sheet

        self.spriteSheet = SpriteSheet("tools.png")

        # Then set the image

        self.imageSwordR = self.spriteSheet.get_image(0,0,45,18)
        self.imageSwordL = pygame.transform.flip(self.imageSwordR, True, False)

        self.imageShieldR = self.spriteSheet.get_image(47,0,25,43)
        self.imageShieldL = pygame.transform.flip(self.imageShieldR, True, False)

        if tool == "sword":
            self.imageR = self.imageSwordR
            self.imageL = self.imageSwordL
        elif tool == "shield":
            self.imageR = self.imageShieldR
            self.imageL = self.imageShieldL
    
        self.player = player

        if tool == "sword":
            self.xOff = 14
            self.yOff = 40

        elif tool == "shield":
            self.xOff = 8
            self.yOff = 24
        
        if self.player.direction == "R": 
            self.image = self.imageR
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.player.rect.x+self.xOff,self.player.rect.y+self.yOff)
        else:
            self.image = self.imageL
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.player.rect.x-self.xOff,self.player.rect.y+self.yOff)

    def update(self):

        # Makes sure it's pointing in the right direction

        if self.player.direction == "R":
            self.image = self.imageR
            self.rect.topleft = (self.player.rect.x+self.xOff,self.player.rect.y+self.yOff)
        else:
            self.image = self.imageL
            self.rect.topleft = (self.player.rect.x-self.xOff,self.player.rect.y+self.yOff)

class Imp(pygame.sprite.Sprite):

    ''' Imp Sprite to battle '''

    ''' Attributes '''

    # Set speed vector

    xv = 0
    yv = 0

    direction = "R"

    # Arrays to hold the walking animations

    walkingFramesR = []
    walkingFramesL = []

    # Other sprites to interact with

    level = None
    player = None

    def __init__(self):

        ''' Imp constructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.spriteSheet = SpriteSheet("Imp.png")

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

        if self.rect.x > self.player.rect.x:
            self.direction = "L"
        else:
            self.direction = "R"

        if self.dist_to(self.player.rect.x, self.player.rect.y) < IMP_FOLLOW_DISTANCE and not self.on_edge():
            if self.direction == "R":
                self.xv = 3
            else:
                self.xv = -3
        else:
            self.xv = 0

        # If not next to player, move forward
        
        if not abs(self.player.rect.x - self.rect.x) <= 5:
            self.rect.x += self.xv

            # Collision detection

            blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
            for block in blockHitList:
                if self.xv > 0:
                    self.rect.right = block.rect.left
                elif self.xv < 0:
                    self.rect.left = block.rect.right
                self.xv = 0

            # For imps obstacles are solid
            
            blockHitList = pygame.sprite.spritecollide(self, self.level.obstacleList, False)
            for block in blockHitList:
                if self.xv > 0:
                    self.rect.right = block.rect.left
                elif self.xv < 0:
                    self.rect.left = block.rect.right
                self.xv = 0
        else:
            self.xv = 0

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

        # Gets the ddistance along a vector
        
        dx = x - self.rect.x
        dy = y - self.rect.y

        dist = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        return dist

    def touching_player(self):

        # Detects whether the imp is touching the player

        playerTouchingList = pygame.sprite.spritecollide(self, self.level.entityList, False)
        if len(playerTouchingList) > 0:
            # If touching the players sword return true, otherwise return false
            return True
        else:
            return False

    def on_ground(self):

        ''' Checks if imp is on ground '''

        # Moves down 2 pixels and checks collision list

        self.rect.y += 2
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y -= 2

        # If we hit something return true

        if len(blockHitList) > 0:
            return True
        else:
            return False

    def on_edge(self):

        ''' Cechks if imp is on the edge of a platform '''

        # Moves along 32 pixels, then checks if on ground

        if self.direction == "R":

            # If imp is right-facing

            self.rect.x += 32
            onGround =  self.on_ground()
            self.rect.x -= 32

            if onGround:

                # If there is a platform, then we are not on the edge so return false
                return False

            else:
                return True
            
        else:

            # If imp is left facing

            self.rect.x -= 32
            onGround = self.on_ground()
            self.rect.x += 32

            if onGround:

                # Same again
                return False

            else:
                return True            
        
class Button(pygame.sprite.Sprite):

    ''' A button class for the menu '''

    name = None

    def __init__(self, x, y, width, height):

        ''' Constructor '''

        # Call the parents constructor

        pygame.sprite.Sprite.__init__(self)

        # Load the image

        self.spriteSheet = SpriteSheet("buttons.png")

        self.regImg = self.spriteSheet.get_image(x,y,width,height)
        self.hoverImg = self.spriteSheet.get_image(x,y+height,width,height)
        self.pressImg = self.spriteSheet.get_image(x,y+(height*2),width,height)

        self.image = self.regImg

        self.rect = self.image.get_rect()

    def set_state(self, state):

        # Updates the costume of the button
        
        if state == 0:
            self.image = self.regImg
            
        elif state == 1:
            self.image = self.hoverImg
            
        elif state == 2:
            self.image = self.pressImg
            
class Image(pygame.sprite.Sprite):

    # This is to allow images to be classed as sprites, cause I couldn't find another way to do that :P

    def __init__(self, image):

        # Call the parents constructor

        pygame.sprite.Sprite.__init__(self)

        self.image = image

        self.rect = self.image.get_rect()
        
def mainMenu():

    ''' MAIN MENU '''

    # Create groups for the sprites to go in

    buttons = pygame.sprite.Group()
    items = pygame.sprite.Group()

    # Create the background image

    backgroundImg = pygame.image.load("title.png").convert()

    background = Image(backgroundImg)
    items.add(background)

    # Create the buttons
    
    playButton = Button(0,0,128,72)
    buttons.add(playButton)

    playButton.rect.centerx = SCREEN_WIDTH/2
    playButton.rect.centery = SCREEN_HEIGHT/2
    playButton.name = "play"

    optionsButton = Button(128,0,160,72)
    buttons.add(optionsButton)

    optionsButton.rect.centerx = SCREEN_WIDTH/2
    optionsButton.rect.centery = SCREEN_HEIGHT/2 + 160
    optionsButton.name = "options"

    charButton = Button(288,0,200,72)
    buttons.add(charButton)

    charButton.rect.centerx = SCREEN_WIDTH/2
    charButton.rect.centery = SCREEN_HEIGHT/2 + 80
    charButton.name = "char"
    
    
    # Play the music

    pygame.mixer.music.load("Flight.mp3")
 
    pygame.mixer.music.play(-1)

    # Set run time vars

    done = False
    fullscreen = 0
    mousedown = False
    
    # Have a game loop for the menu

    while not done:

        for event in pygame.event.get():

            # Detect quits
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == K_FULLSCREEN:
                    fullscreen = 1 - fullscreen

                    if fullscreen == 1:
                        pygame.display.set_mode((size), FULLSCREEN)
                    else:
                        pygame.display.set_mode((size))

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    mousedown = True

            elif event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    mousedown = False

        mousePos = pygame.mouse.get_pos()

        # Check the status of each button

        for button in buttons:

            if button.rect.collidepoint(mousePos):

                # First check if the mouse is on the button
                
                if mousedown:

                    # Then if the mouse is being pressed
                    
                    button.set_state(2)
                    if button.name == "play":
                        done = True
                    
                else:
                    
                    button.set_state(1)
                
            else:
                
                button.set_state(0)

        '''
        Code to draw goes below this comment
        '''

        items.draw(gameDisplay)
        buttons.draw(gameDisplay)

        '''
        Code to draw goes above this comment
        '''

        # Limit to 60fps and then update the display

        clock.tick(60)
        pygame.display.flip()
                
def main():

    '''
    MAIN PROGRAM
    '''

    # Initialize the mixer, then pygame itself
    
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()

    # Set the display size

    global size, gameDisplay, clock
    
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    gameDisplay = pygame.display.set_mode(size)

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    pygame.display.set_caption("Legend Rush V4.1.2 Beta")

    '''
    Run the menu
    '''

    mainMenu()

    # Create the player

    global player
    
    player = Player()

    # Create the level list
    levelList = []
    levelList.append(Level_01(player))

    # Set the current level
    currentLevelNo = 0
    currentLevel = levelList[currentLevelNo]

    activeSpriteList = pygame.sprite.Group()
    player.level = currentLevel

    player.rect.x = 150
    player.rect.y = 400
    activeSpriteList.add(player)

    # Create imps

    imp = currentLevel.create_imp(1600, 466)
    activeSpriteList.add(imp)

    imp = currentLevel.create_imp(2016, 434)
    activeSpriteList.add(imp)

    # Vars to control the player

    jump = False
    attack = False
    shield = False
    fullscreen = 0
    
    # Loop until the user clicks the close button
    gameExit = False

    # -------- Main Program Loop --------
    while not gameExit:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                gameExit = True # Show that the game is done to exit the loop

            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE: # Alternatively use the escape key
                    gameExit = True

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_left(PLAYER_SPEED)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_right(PLAYER_SPEED)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    jump = True

                elif event.key == K_FULLSCREEN:
                    fullscreen = 1 - fullscreen

                    if fullscreen == 1:
                        pygame.display.set_mode((size), FULLSCREEN)
                    else:
                        pygame.display.set_mode((size))

                elif event.key == K_SPACE:
                    if player.on_ground():
                        attack = True
    
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if player.on_ground():
                        shield = True
                    
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.xv < 0:
                    player.stop()
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.xv > 0:
                    player.stop()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    jump = False

        # Player attacking, shielding and jumping

        if jump:
            player.jump(PLAYER_JUMP_HEIGHT)

        if attack and player.attacking == 0:
            if player.on_ground():
                player.attack()
                attack = False

        if shield and player.shielding == 0:
            if player.on_ground():
                player.use_shield()
                shield = False
                
        if player.attacking > 0:
            player.stop()
            player.attacking -= 1
    
        if player.shielding > 0:
            player.stop()
            player.shielding -= 1
            
        # Update entities
        activeSpriteList.update()
        currentLevel.entityList.update()
        
        # Player attacking scripts

        for imp in currentLevel.impList:
            if imp.touching_player() and player.attacking > 0:
                currentLevel.impList.remove(imp)
                activeSpriteList.remove(imp)
                
        # Update items in the level
        currentLevel.liquidList.update()

        # If the player gets near the right side shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            currentLevel.shift_world(-diff)

        # If the player gets near the left side shift the world right (+x)
        if player.rect.x <= 150:
            diff = player.rect.x - 150
            player.rect.x = 150
            currentLevel.shift_world(-diff)

        '''
        ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        '''
        
        currentLevel.draw(gameDisplay)
        activeSpriteList.draw(gameDisplay)
        currentLevel.entityList.draw(gameDisplay)
        currentLevel.liquidList.draw(gameDisplay)
    
        '''
        ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        '''

        # Limit to 60 FPS
        clock.tick(60)

        # Then finally update the screen
        pygame.display.flip()

    # and as not to leave the program hanging...
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
