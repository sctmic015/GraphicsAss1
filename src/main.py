import pygame as pg
from GLWindow import *

def main():
	""" The main method where we create and setup our PyGame program """

	window = OpenGLWindow()
	window.initGL()
	running = True

	count = 0
	# Game loop runs for ever
	rotate = -1
	scale = 1
	x = 0
	y = 0
	z = 0
	while running:


		for event in pg.event.get(): # Grab all of the input events detected by PyGame
			if event.type == pg.QUIT:  # This event triggers when the window is closed
				running = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_q:  # This event triggers when the q key is pressed down
					running = False
				elif event.key == pg.K_c:
					if count % 3 == 0:
						colorLoc = glGetUniformLocation(window.shader, "objectColor")
						glUniform3f(colorLoc, 1, 0, 0)
						count = count + 1
					elif count % 3 == 1:
						colorLoc = glGetUniformLocation(window.shader, "objectColor")
						glUniform3f(colorLoc, 0, 1, 0)
						count = count + 1
					elif count % 3 == 2:
						colorLoc = glGetUniformLocation(window.shader, "objectColor")
						glUniform3f(colorLoc, 0, 0, 1)
						count = count + 1
				elif event.key == pg.K_z:
					rotate = 2
				elif event.key == pg.K_x:
					rotate = 1
				elif event.key == pg.K_y:
					rotate = 0
				elif event.key == pg.K_EQUALS:     # For some reason unkown to me the + is not registering
					scale = scale + 0.1
					print(scale)
				elif event.key == pg.K_MINUS:
					scale = scale - 0.1
					print(scale)
				elif event.key == pg.K_UP:
					y = y + 0.1
				elif event.key == pg.K_DOWN:
					y = y - 0.1
				elif event.key == pg.K_LEFT:
					x = x - 0.1
				elif event.key == pg.K_RIGHT:
					x = x + 0.1
				elif event.key == pg.K_a:
					window.initGL(addSwitch=True)
					rotate = -1
		window.render(rotate, scale, x, y, z) # Refresh screen
	
	window.cleanup()
	pg.quit


if __name__ == "__main__":
	main()

