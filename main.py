'''
THE LEGEND
By Sigton

Main:
The main program
'''

import pygame
from pygame import *

import constants, spritesheet, platforms, level, tools, imp, menu, blob
import player as p
from constants import PLAYER_SPEED # This seemed to stop some weird bug o.0

import sys

def main():

    '''
    MAIN PROGRAM
    '''

    # Init the mixer, then pygame itself

    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()

    # Set the display size

    global gameDisplay, clock

    gameDisplay = pygame.display.set_mode(constants.SIZE)

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Set the caption and icon
    pygame.display.set_caption("The Legend V1.0")
    icon = spritesheet.SpriteSheet("resources/images/icon.ico").get_image(0,0,32,32)
    pygame.display.set_icon(icon)

    '''
    Run the menu
    '''

    menu.mainMenu(gameDisplay, clock)

    # Create the player

    global player, activeSpriteList
    
    player = p.Player()

    activeSpriteList = pygame.sprite.Group()

    # Create the level list
    levelList = []
    levelList.append(level.Level_01(player))
    levelList.append(level.Level_02(player))
    levelList.append(level.Level_03(player))
    levelList.append(level.Level_04(player))
    levelList.append(level.Level_05(player))
    levelList.append(level.Level_06(player))

    # Set the current level
    currentLevelNo = 0
    currentLevel = levelList[currentLevelNo]

    player.level = currentLevel

    currentLevel.player = player

    for imp in currentLevel.impList:
        activeSpriteList.add(imp)

    player.rect.x = 150
    player.rect.y = 400
    activeSpriteList.add(player)

    # Variables to control the player

    run = 0
    jump = False
    attack = False
    shield = False
    fullscreen = 0

    # Loop until the user clicks the close button
    gameExit = False

    # -------- Main Program Loop --------
    while not gameExit:
        for event in pygame.event.get(): # User did something
            if event.type == QUIT: # If use clicked close
                gameExit = True

            elif event.type == KEYDOWN:
                if event.key == constants.K_ESCAPE: # Alternatively use the escape key
                    gameExit = True

                if event.key == K_LEFT or event.key == K_a:
                    run = -1
                if event.key == K_RIGHT or event.key == K_d:
                    run = 1
                if event.key == K_UP or event.key == K_w:
                    jump = True

                elif event.key == constants.K_FULLSCREEN:
                    fullscreen = 1 - fullscreen

                    if fullscreen == 1:
                        gameDisplay = pygame.display.set_mode((constants.SIZE), FULLSCREEN)
                    else:
                        gameDisplay = pygame.display.set_mode((constants.SIZE))

                elif event.key == K_SPACE:
                    if player.on_ground():
                        attack = True

                elif event.key == K_DOWN or event.key == K_s:
                    if player.on_ground():
                        shield = True

            elif event.type == KEYUP:
                if (event.key == K_LEFT or event.key == K_a) and player.xv < 0:
                    run = 0
                elif (event.key == K_RIGHT or event.key == K_d) and player.xv > 0:
                    run = 0
                elif event.key == K_UP or event.key == K_w:
                    jump = False
                    
        # Level progression
        if player.touching_checkpoint():
            currentLevel.reset_world()
            player.reset()
            
            currentLevelNo += 1
            currentLevel = levelList[currentLevelNo]
            
            player.level = currentLevel
            currentLevel.player = player
            
            for imp in currentLevel.impList:
                activeSpriteList.add(imp)

        # Player attacking, shielding, running and jumping

        if player.knockback > 0:
            player.knockback -= 1
            run = 0
        else:
            if abs(run) > 0:
                if run == 1:
                    player.go_right(PLAYER_SPEED)
                elif run == -1:
                    player.go_left(PLAYER_SPEED)
        
        if jump and not (attack or shield):
            player.jump(constants.PLAYER_JUMP_HEIGHT)

        if attack and player.attacking == 0 and player.shielding == 0:
            if player.on_ground():
                player.attack()
                attack = False

        if shield and player.shielding == 0 and player.attacking == 0:
            if player.on_ground():
                player.use_shield()
                shield = False

        if player.attacking > 0:
            run = 0
            player.attacking -= 1

        if player.shielding > 0:
            run = 0
            player.shielding -= 1

        # Update entities

        activeSpriteList.update()
        currentLevel.update()

        # Player attacking scripts

        for imp in currentLevel.impList:
            if imp.touching_player() and player.attacking > 0:
                currentLevel.impList.remove(imp)
                activeSpriteList.remove(imp)

        # If the player gets near the right side of the world shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            currentLevel.shift_world(-diff)

        # If the player gets near the left side of the world shift the world right (+x)
        if player.rect.x <= 200:
            diff = player.rect.x - 200
            player.rect.x = 200
            currentLevel.shift_world(-diff)

        '''
        All code to draw below this comment
        '''

        currentLevel.draw(gameDisplay)
        activeSpriteList.draw(gameDisplay)
        currentLevel.entityList.draw(gameDisplay)
        player.heartList.draw(gameDisplay)
        
        '''
        All code to draw above this comment
        '''

        # Limit to 60 fps
        clock.tick(60)

        # Then finally update the display
        pygame.display.flip()

    # and as not to leave the program hanging... (#SaveTheIDE's ;D)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
    
