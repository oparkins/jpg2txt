#!/usr/bin/env python3
"""
Helps convert a graph of different colors to text values and coordinates
"""

from tkinter import *      
import argparse
from PIL import Image
import json
import progressbar
import csv
import os

__author__ = "Owen Parkins"
__version__ = "0.1.0"


# https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python
def rgb2hex(r, g, b):
    """ Convert RGB colors to HEX """
    return "#{:02x}{:02x}{:02x}".format(r,g,b)


def CalculateSlope(point1, point2):
    if point1[0] - point2[0] == 0:
        return 0
    return (point1[1] - point2[1])/(point1[0] - point2[0])

def ApplyBoundaries_Top(config, img):
    lastBoundary = (0, 0)
    max_y = 0
    print("Applying Top Boundary")
    for boundary in progressbar.progressbar(config["boundaries"]["top"]):
        limit_x = int(boundary["x"])
        limit_y = int(boundary["y"])
        max_y = max(limit_y, max_y)
        for x in range(0, img.width):
            for y in range(0, img.height):
                # is the current point about the line between the current boundary and the last boundary
                if x > boundary["x"] or x < lastBoundary[0] or y > max_y:
                    continue
                slope = CalculateSlope((limit_x, limit_y), lastBoundary)
                if y < slope * (x - limit_x) + limit_y:
                    img.putpixel((x,y), (255,255,255))
        lastBoundary = (limit_x, limit_y)

def ApplyBoundaries_Bottom(config, img):
    lastBoundary = (0, img.height)
    min_y = 0
    print("Applying Bottom Boundary")
    for boundary in progressbar.progressbar(config["boundaries"]["bottom"]):
        limit_x = int(boundary["x"])
        limit_y = int(boundary["y"])
        min_y = max(limit_y, min_y)
        slope = CalculateSlope((limit_x, limit_y), lastBoundary)
        for x in range(0, img.width):
            for y in range(0, img.height):
                # is the current point about the line between the current boundary and the last boundary
                if x > boundary["x"] or x < lastBoundary[0] or y < min_y:
                    continue
                if y > slope * (x - limit_x) + limit_y:
                    img.putpixel((x,y), (255,255,255))
        lastBoundary = (limit_x, limit_y)


def ApplyBoundaries_Left(config, img):
    lastBoundary = (0, 0)
    max_x = 0
    print("Applying Left Boundary")
    for boundary in progressbar.progressbar(config["boundaries"]["left"]):
        limit_x = int(boundary["x"])
        limit_y = int(boundary["y"])
        max_x = max(limit_x, max_x )
        slope = CalculateSlope((limit_x, limit_y), lastBoundary)
        for x in range(0, img.width):
            for y in range(0, img.height):
                if x > max_x or y < lastBoundary[1] or y > limit_y: # Other boundaries can deal with it
                    continue
                # is the current point about the line between the current boundary and the last boundary
                if slope != 0:
                    result = (y - limit_y)/slope + limit_x
                else:
                    result = limit_x
                if x < result:
                    img.putpixel((x,y), (255,255,255))
        lastBoundary = (limit_x, limit_y)

def ApplyBoundaries_Right(config, img):
    lastBoundary = (0, 0)
    min_x = 0
    print("Applying Right Boundary")
    for boundary in progressbar.progressbar(config["boundaries"]["right"]):
        limit_x = int(boundary["x"])
        limit_y = int(boundary["y"])
        min_x = max(limit_x, min_x )
        slope = CalculateSlope((limit_x, limit_y), lastBoundary)
        for x in range(0, img.width):
            for y in range(0, img.height):
                if x < min_x or y < lastBoundary[1] or y > limit_y: # Other boundaries can deal with it
                    continue
                # is the current point about the line between the current boundary and the last boundary
                if slope != 0:
                    result = (y - limit_y)/slope + limit_x
                else:
                    result = limit_x
                if x < result:
                    img.putpixel((x,y), (255,255,255))
        lastBoundary = (limit_x, limit_y)

def ApplyBoundaries(config, img):
    """ Applies the boundries to the image """
    ApplyBoundaries_Top(config, img)
    ApplyBoundaries_Left(config, img)
    ApplyBoundaries_Right(config, img)
    ApplyBoundaries_Bottom(config, img)

def RemoveBlack(img):
    """ Will convert all black lines to the colors around them. May take multiple passes """
    completed = False 
    passNumber = 1
    while completed == False:
        completed = True
        print("Removing black lines - Pass " + str(passNumber))
        for x in progressbar.progressbar(range(0, img.width)):
            for y in range(0, img.height):
                # Skip the pixel if the color is black. If not, skip
                currentPixel = img.getpixel((x, y)) 
                if currentPixel != (0,0,0):
                    continue
                # if top is a legit color, use that
                if y - 1 > 0 and img.getpixel((x, y - 1)) != (255, 255, 255) and img.getpixel((x, y - 1)) != (0, 0, 0):
                    img.putpixel((x,y), img.getpixel((x, y - 1)))
                    completed = False 
                    continue

                # if bottom is a legit color, use that
                if y + 1 < img.height and img.getpixel((x, y + 1)) != (255, 255, 255) and img.getpixel((x, y + 1)) != (0, 0, 0):
                    img.putpixel((x,y), img.getpixel((x, y + 1)))
                    completed = False 
                    continue

                # if left is a legit color, use that
                if x - 1 > 0 and img.getpixel((x - 1, y)) != (255, 255, 255) and img.getpixel((x - 1, y)) != (0, 0, 0):
                    img.putpixel((x,y), img.getpixel((x - 1, y)))
                    completed = False 
                    continue

                # if right is a legit color, use that
                if x + 1 > 0 and img.getpixel((x + 1, y)) != (255, 255, 255) and img.getpixel((x + 1, y)) != (0, 0, 0):
                    img.putpixel((x,y), img.getpixel((x + 1, y)))
                    completed = False 
                    continue
        passNumber = passNumber + 1
    img.show()
def Convert(config):
    """ Converts the image to the stratigraphy descriptions """
    img = Image.open(config["file"])
    ApplyBoundaries(config, img)
    RemoveBlack(img)
    results = []
    x_scale = int(config["scale-x"]) / (int(config["ref-x"]) - int(config["origin-x"]))
    y_scale = int(config["scale-y"]) / (int(config["ref-y"]) - int(config["origin-y"]))
    print("Rows processed:")
    for x in progressbar.progressbar(range(0, img.width)):
        for y in range(0, img.height):
            # Skip the pixel if the color is white
            if img.getpixel((x, y)) == (255,255,255):
                continue
            for colorDescriptions in config["colors"]:
                for color in colorDescriptions["color"]:
                    pixel = img.getpixel((x, y))
                    if color == rgb2hex(pixel[0], pixel[1], pixel[2]):
                        x_meter = int((x - int(config["origin-x"])) * x_scale)
                        y_meter = int((y - int(config["origin-y"])) * y_scale)
                        results.append((x_meter, y_meter, colorDescriptions['id']))
    return results



def main(args):
    """ Main entry point of the app """
    with open(args.config, "r") as f:
        config = json.load(f)
    output = os.path.splitext(os.path.basename(config["file"]))[0]
    with open(output + ".csv", "w") as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(["x (meters)", "y (meters)", "id"])
        for row in Convert(config):
            csvWriter.writerow(list(row))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(description="Convert images stratigraphy descriptions")
    parser.add_argument("-f", dest="config", help="A configuration file to read")
    parser.add_argument("-g", dest="gui", action='store_true', help="Start the gui (not implemented)")
    main(parser.parse_args())