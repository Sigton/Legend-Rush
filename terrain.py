'''
THE LEGEND
by Sigton

Terrain:
This generates/writes the level data
'''

import pygame
from pygame.locals import *

import json, os

class LevelData:

    ''' Class to write/load data to the level JSON files '''

    saveFile = None
    loadFile1 = None
    loadFile2 = None    

    tileColors = []
    typeColors = []

    # Set the color samples
    palette = os.path.join("level_data", "colorpalette.png")
    colorPalette = pygame.image.load(palette)
    pixAr = pygame.PixelArray(colorPalette)
    
    for pixel in pixAr:
        tileColors.append(pixel[0])

    palette = os.path.join("level_data", "typepalette.png")
    typePalette = pygame.image.load(palette)
    pixAr = pygame.PixelArray(typePalette)

    for pixel in pixAr:
        typeColors.append(pixel[0])

    def __init__(self, savefile, loadfile1, loadfile2):

        ''' Constructor '''

        self.saveFile = savefile
        self.loadFile1 = pygame.image.load(loadfile1)
        self.loadFile2 = pygame.image.load(loadfile2)

        levelData = []
        
    def load_data(self):

        ''' Loads data from the JSON file '''

        # Turn the JSON file into a python data structure
        with open(self.saveFile, 'r') as infile:
            data = json.load(infile)

        return data

    def write_data(self):

        ''' Writes data to the JSON file '''

        # A tuple of the different block types

        block_types = (
            "Solid",
            "Cosmetic",
            "Liquid",
            "Obstacle",
            "Checkpoint",
            "Enemy"
            )

        # Then turn the load file into a pixel array

        pixAr = pygame.PixelArray(self.loadFile1)
        pixAr2 = pygame.PixelArray(self.loadFile2)

        # And finally turn it into a complex data structure

        self.levelData = []
        
        x = 0
        for column in pixAr:
            y = 0
            for pixel in column:

                newTile = []
                tileData = {}

                newTile.append((x,y))
                
                if pixel in self.tileColors:
                    n = 0
                    for color in self.tileColors:
                        n += 1
                        if pixel == color:
                             tileData['tile'] = n
                    
                    if pixAr2[x][y] in self.typeColors:
                        n = 0
                        for color in self.typeColors:
                            
                            if pixAr2[x][y] == color:
                                tileData['type'] = block_types[n]
                                break
                            n += 1
                else:
                    tileData['tile'] = 0
                    tileData['type'] = None

                newTile.append(tileData)
                self.levelData.append(newTile)
                y += 1
            x += 1

        # Export it to the json file
        with open(self.saveFile, 'w') as outfile:
            json.dump(self.levelData, outfile, indent=4)
