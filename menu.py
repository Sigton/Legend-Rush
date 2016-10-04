'''
THE LEGEND
By Sigton

Menu:
This is the games main menu.
'''

import pygame
from pygame.locals import *

import constants, spritesheet

import sys

class Button(pygame.sprite.Sprite):

    '''
    A button class for the menu
    '''

    name = None

    def __init__(self, x, y, width, height):

        ''' Constructor '''

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the image

        self.spriteSheet = spritesheet.SpriteSheet("resources/images/buttons.png")

        self.regImg = self.spriteSheet.get_image(x,y,width,height)
        self.hoverImg = self.spriteSheet.get_image(x,y+height,width,height)
        self.pressImg = self.spriteSheet.get_image(x,y+(height*2),width,height)

        self.image = self.regImg

        self.rect = self.image.get_rect()

    def set_state(self, state):

        # Updates the costume of the button

        if state == 0:
            self.image = self.regImg
        if state == 1:
            self.image = self.hoverImg
        if state == 2:
            self.image = self.pressImg

class Image(pygame.sprite.Sprite):

    # This is to allow images to be classed as sprites

    def __init__(self, image):

        # Call the parents constructor

        pygame.sprite.Sprite.__init__(self)

        self.image = image

        self.rect = self.image.get_rect()

def mainMenu(display, clock):

    ''' Main Menu '''

    # Create groups for the sprites to go in

    buttons = pygame.sprite.Group()
    items = pygame.sprite.Group()

    # Create the background image

    backgroundImg = pygame.image.load("resources/images/title.png").convert()

    background = Image(backgroundImg)
    items.add(background)

    # Create the buttons

    playButton = Button(0,0,128,72)
    buttons.add(playButton)

    playButton.rect.centerx = constants.SCREEN_WIDTH/2
    playButton.rect.centery = constants.SCREEN_HEIGHT/2
    playButton.name = "play"

    optionsButton = Button(128,0,160,72)
    buttons.add(optionsButton)

    optionsButton.rect.centerx = constants.SCREEN_WIDTH/2
    optionsButton.rect.centery = constants.SCREEN_HEIGHT/2 + 160
    optionsButton.name = "options"

    charButton = Button(288,0,200,72)
    buttons.add(charButton)

    charButton.rect.centerx = constants.SCREEN_WIDTH/2
    charButton.rect.centery = constants.SCREEN_HEIGHT/2 + 80
    charButton.name = "char"

    # Play the music

    pygame.mixer.music.load('resources/sounds/Flight.mp3')

    pygame.mixer.music.play(-1)

    # Set run time vars

    done = False
    fullscreen = 0
    mousedown = False

    # Have a game loop for the menu

    while not done:

        for event in pygame.event.get():

            # Detect quits
            if event.type == QUIT or event.type == KEYDOWN and event.key == constants.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:

                if event.key == constants.K_FULLSCREEN:
                    fullscreen = 1 - fullscreen

                    if fullscreen == 1:
                        pygame.display.set_mode((constants.SIZE), FULLSCREEN)
                    else:
                        pygame.display.set_mode((constants.SIZE))

            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:
                    mousedown = True

            elif event.type == MOUSEBUTTONUP:

                if event.button == 1:
                    mousedown = False

        mousePos = pygame.mouse.get_pos()

        # Check the status of each button

        for button in buttons:

            if button.rect.collidepoint(mousePos):

                # First check the mouse is on the button

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

        items.draw(display)
        buttons.draw(display)

        '''
        Code to draw goes above this comment
        '''

        # Limit to 60 fps then update the display

        clock.tick(60)
        pygame.display.flip()
