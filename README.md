# jpg2txt
## Converts Images of Stratigraphy to an Importable Format

Takes an image and a configuration file (see below), and outputs a CSV file with the x,y, and material type of each pixel (or some dx/dy)

## How to use it
```
usage: jpg2txt.py [-h] [-f CONFIG] [-c COLUMNS] [-r ROWS] [-g] [-s]
                  [-ic IGNORECOLUMNS] [-mn]

Convert images stratigraphy descriptions

optional arguments:
  -h, --help         show this help message and exit
  -f CONFIG          A configuration file to read
  -c COLUMNS         Amount of columns to output
  -r ROWS            Amount of rows to output
  -g                 Start the gui (not implemented)
  -s                 Show the image after boundaries and black line removal
  -ic IGNORECOLUMNS  Ignore columns on the right side (useful for removing
                     stepping)
  -mn                Use Mark's numbering scheme (bottom xy is origin.)
```

Instead of using the boundaries, I recommend editing the image in a photo editor (like GIMP), and then running the application without any boundaries. This is especially true if using the `-mn` flag. If using the x,y coordinates with respect to the origin, then there shouldn't be a problem to use boundaries.

You can refine the grid that is outputted by using the `-c` and `-r` flags. This will limit the amount of rows and columns that are created, essentially creating some constant dx and dy during the processing.

## Example Configuration File
An explanation of the file is below
```
{
    "file": "/home/user/Documents/Something.png",
    "origin-x": 1808,
    "origin-y": 608,
    "ref-x": 2411,
    "ref-y": 150,
    "scale-x": 10000,
    "scale-y": 200,
    "colors" : [
        {
            "name": "silt",
            "id": 1,
            "color": [
                "#fff500",
                "#e3e300",
                "#ffff00"
            ]
        },
        {
            "name": "gravel",
            "id": 2,
            "color": [
                "#838281",
                "#787878"
            ]
        },
        {
            "name": "clay",
            "id": 3,
            "color": [
                "#e30000",
                "#da241e",
                "#c73100"
            ]
        },
        {
            "name": "very course sand/granules",
            "id": 4,
            "color": [
                "#e7781e",
                "#e37100"
            ]
        }
        ,
        {
            "name": "fine sand",
            "id": 5,
            "color": [
                "#00923f",
                "#008e00",
                "#008e47",
                "#007100"
            ]
        }
    ],
    "boundaries": {
        "left": [
            {
                "x": 642,
                "y": 0
            },
            {
                "x": 840,
                "y": 2191
            }
        ],
        "right" : [
        ],
        "top": [
            {
                "x": 1272,
                "y": 0
            },
            {
                "x": 1914,
                "y": 621
            },
            {
                "x": 2115,
                "y": 645
            },
            {
                "x": 7023,
                "y": 750
            }
        ],
        "bottom" : [

        ]
    } 
}
```

| attribute | description |
|-----------|-------------|
| file      |  The location of the file. Should be absolute                                                   | 
| origin-x  |  The x-coordinate in pixels where the origin is. Not needed if -mn is specified                 |       
| origin-y  |  The y-coordinate in pixels where the origin is.  Not needed if -mn is specified                |          
| ref-x     |  The x-coordinate in pixels of the next interval on the x-axis. Not needed if -mn is specified  |    
| ref-y     |  The y-coordinate in pixels of the next interval on the x-axis. Not needed if -mn is specified  |     
| scale-x   |  The scale on the x-axis. In the example above, it is in meters. Not needed if -mn is specified |      
| scale-y   |  The scale on the y-axis. In the example above, it is in meters. Not needed if -mn is specified |        
| colors    |  Describes the different colors and how to categorize them                                      |    
| boundaries|  Describes the boundaries where the script will ignore                                          | 

### ref-x and ref-y Description

The `ref-x` and `ref-y` are used to calculate the scale of the image. The equation used is:

```
x_scale = "scale-x" / ("ref-x" - "origin-x")
y_scale = "scale-y" / ("ref-y" - "origin-y")
```

This helps figure out in the units provided where the pixel would be located.

### Colors

The colors must be exact. If there are shadings or gradients, the program will not work. Clean up the image in GIMP if you have this problem.

The colors must not be black (#000000) or white (#FFFFFF). The program uses these colors in a special way.

### Boundaries

The program will actually replace all pixels outside the boundaries with a white pixel. This is to make the program less complex and more maintainable. It adds some processing time, but the intention is that the program is ran once.