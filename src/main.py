import pygame as pg
from GLWindow import *

def main():
	""" The main method where we create and setup our PyGame program """

	window = OpenGLWindow()
	window.initGL()
	running = True

	count = 0
	# Game loop runs for ever
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
		window.render() # Refresh screen
	
	window.cleanup()
	pg.quit


if __name__ == "__main__":
	main()

