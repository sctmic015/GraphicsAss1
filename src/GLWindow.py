import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

from Geometry import Geometry

# Notes on shaders
# Vertex shader -> Runs once per vertex and is responsible for position on screen and possibly some transformations
# Fragment shader -> Shape assembled and broken down to fragments/pixel. Resposible for calculating colour per pixels. Can be written as 
# strings but text files are better. 
# Notes om shaders. They do colour and positions seperately. It looks like we do it as one. vec4 so transformations can be done ith matrics

class Triangle:

    def __init__(self, shader):
        self.vertexLoc = glGetAttribLocation(shader, "position")
        #x, y, z, r, g, b    List of vertices. All the data we want to store at each point in a primitive. Here only positions - no colours or textures etc
        # openGL uses normalised device co-ordinates
        # x - left tp right - -1 to +1
        # y - bottom to top
        # z - depth - 0 -> flat on screen
        # np array data type built for c style data reading 
        # np array constructors used to pass to graphics card
        # must be 32 
        self.vertices = np.array([0.0, 0.5, 0.0,
                                  -0.5, -0.5, 0.0,
                                  0.5, -0.5, 0.0], dtype=np.float32)

        self.vertexCount = 3
        self.vbo = glGenBuffers(1)     # Vertex buffer object. One buffer for us. 
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) # Bind buffer so we know which one we are talking about
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW) # Shift buffer off to graphics card. # Static draw means set data once and use many times. Static draw for reading and writing multiple times. Both good though

        # enable attribute and describe how it is laid out in VBO. Not sure what vertex.loc is. 3 points in attribute
        # Data type floating point decimals 
        # False as do not need to normalise numbers
        # Stride is how many bytes we need to step to get to next position. Not sure why it is 0
        # Offset. How far we need to go to find type. Void pointer is special type of memory address. 
        # Allocating memory to graphcis card
        glEnableVertexAttribArray(self.vertexLoc)
        glVertexAttribPointer(self.vertexLoc, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    def cleanup(self):
        # Freeing vbo. , represents a list
        glDeleteBuffers(1, (self.vbo,))


class OpenGLWindow:

    def __init__(self):
        self.triangle = None
        self.clock = pg.time.Clock()

    # Shaders are like there own program in GPU
    def loadShaderProgram(self, vertex, fragment):
        # Opening vertex shader file in read. with as localises lifespan of resource so file closed after indented block
        with open(vertex, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment, 'r') as f:
            fragment_src = f.readlines()

        # Compile each of shader and pass in source code with flags
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))

        return shader

    def initGL(self, screen_width=640, screen_height=480):
        # Initialise
        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 2)

        # Creates new window. Tell pygamae using opengL and use double buffering system. 
        pg.display.set_mode((screen_width, screen_height), pg.OPENGL | pg.DOUBLEBUF)

        glEnable(GL_DEPTH_TEST)
        # Uncomment these two lines when perspective camera has been implemented
        #glEnable(GL_CULL_FACE)
        #glCullFace(GL_BACK)

        # Shows which colour we want to show on our screen
        glClearColor(0, 0, 0, 1)

        # Best way to declare vertex data. Ties in with VBO and associates with VBO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Note that this path is relative to your working directory when running the program
        # You will need change the filepath if you are running the script from inside ./src/
        # Call function and call resulting shader
        # Should have shader in use before declaring data

        self.shader = self.loadShaderProgram("./shaders/simple.vert", "./shaders/simple.frag")
        glUseProgram(self.shader)

        colorLoc = glGetUniformLocation(self.shader, "objectColor")
        glUniform3f(colorLoc, 1.0, 1.0, 1.0)

        # Uncomment this for triangle rendering
        self.triangle = Triangle(self.shader)

        # Uncomment this for model rendering
        #self.cube = Geometry('./resources/cube.obj')

        print("Setup complete!")


    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   # Colour buffer stores all pixels on screen. Colours stored in colour buffer bit thing
        glUseProgram(self.shader)  # You may not need this line

        #Uncomment this for triangle rendering
        # Draws the triangle
        # Was bound in youtube vid but not here
        # Using triangles 
        # Vertex 0 where we start from
        # Vertext count is number of points to draw
        glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertexCount)

        # Uncomment this for model rendering
        #glDrawArrays(GL_TRIANGLES, 0, self.cube.vertexCount)


        # Swap the front and back buffers on the window, effectively putting what we just "drew"
        # Onto the screen (whereas previously it only existed in memory)
        pg.display.flip()

        #
        # self.clock.tick(60)  # might need this

    def cleanup(self):
        # Deleting vao , represents list
        glDeleteVertexArrays(1, (self.vao,))
        # Uncomment for triangle rendering
        self.triangle.cleanup()
        # Uncomment for model rendering
        #self.cube.cleanup()
