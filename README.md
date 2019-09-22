# jpg2txt
## Converts Images of Stratigraphy to an Importable Format

## How to use it

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
| file      |  The location of the file. Can be relative or absolute          | 
| origin-x  |  The x-coordinate in pixels where the origin is                 |       
| origin-y  |  The y-coordinate in pixels where the origin is                 |          
| ref-x     |  The x-coordinate in pixels of the next interval on the x-axis  |    
| ref-y     |  The y-coordinate in pixels of the next interval on the x-axis  |     
| scale-x   |  The scale on the x-axis. In the example above, it is in meters |      
| scale-y   |  The scale on the y-axis. In the example above, it is in meters |        
| colors    |  Describes the different colors and how to categorize them      |    
| boundaries|  Describes the boundaries where the script will ignore          | 

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