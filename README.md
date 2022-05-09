# Author: SCTMIC015

##Set Up information:

Set up follows much of the same procedure as before. Some of which is pasted below.

Setup assumes that you are using a UNIX-based OS with python3 and python3-venv installed.

To build the virtual environment and install necessary packages:

```
> make
```

Note: You can also put any packages you want to use in the requirements.txt file.

To activate the virtual environment:

```
> source ./venv/bin/activate
```

To run the skeleton code:

- To load the default object (ie "cube.obj")
```
> python ./src/main.py
```

- To select an object to load at startup 

```
> python ./src/main.py "objectname"
```
For Example to load suzanne as an object we would type python ./src/main.py "suzanne.obj"

## Key Presses
 
The appropriate Key presses to control the program

Task | Keys |
--- | --- | 
Colour | c Key - cycles through colours (White, Red, Green, Blue) |
Translate along Y axis | Up and Down Keys  |
Translate along X axis | Left and Right Keys |
Scale Up | + Key  |
Scale Down | - Key |
Rotate along X axis | x Key |
Rotate along Y axis | y Key |
Rotate along Z axis | Z key |
Reset Scene | r Key|
Add another object | a Key |
Quite program | q Key 