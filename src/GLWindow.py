import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr

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

# Hold position and angle for drawing a cube
class Cube:


    def __init__(self, position, eulers):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class Scene:
    def __init__(self):

        self.cubes = [
            Cube(
                position=[0, 0, -10],
                eulers=[0, 0, 0]
            ),
        ]
    def addCube(self):
        newCube = Cube(
                position=[-1.5, 0, -10],
                eulers=[0, 0, 0]
            )
        self.cubes.append(newCube)

class OpenGLWindow:

    def __init__(self):
        self.triangle = None
        self.clock = pg.time.Clock()
        self.scene = Scene()

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

    def initGL(self, screen_width=1080, screen_height=720, addSwitch=False):
        # Initialise
        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)      # Wonder what this does

        # Creates new window. Tell pygamae using opengL and use double buffering system. 
        pg.display.set_mode((screen_width, screen_height), pg.OPENGL | pg.DOUBLEBUF)

        glEnable(GL_DEPTH_TEST) # Checks if objects are drawing in front of each other properly
        # Uncomment these two lines when perspective camera has been implemented
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        # Shows which colour we want to show on our screen
        glClearColor(0, 0, 0, 1)

        # Best way to declare vertex data. Ties in with VBO and associates with VBO
        #self.vao = glGenVertexArrays(1)
        #glBindVertexArray(self.vao)

        # Note that this path is relative to your working directory when running the program
        # You will need change the filepath if you are running the script from inside ./src/
        # Call function and call resulting shader
        # Should have shader in use before declaring data

        self.shader = self.loadShaderProgram("./shaders/simple.vert", "./shaders/simple.frag")
        glUseProgram(self.shader)

        colorLoc = glGetUniformLocation(self.shader, "objectColor")
        glUniform3f(colorLoc, 1.0, 1.0, 1.0)

        # Uncomment this for triangle rendering
        #self.triangle = Triangle(self.shader)

        # Uncomment this for model rendering
        #self.cube = Geometry('./resources/cube.obj')
        self.wood_texture = Material("wood.jpeg")
        self.cube_load = Geometry("resources/suzanne.obj")

        #self.cube = Cube(
        #    position=[0, 0, -2],  # Positive z value behind camera, negative in front of camera
        #    eulers=[0, 0, 0]
        #)
        if (addSwitch == True):
            self.scene = Scene()
            self.scene.addCube()
        ## Perspective Projection matrix - Gives us our view
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640 / 480,    # fovy - field of view angle in the y think like half a view angle; aspect -> aspect ratio
            near=0.1, far=50, dtype=np.float32 # near closer than 0.1 not drawn and further than 10 not drawn
        )
        ## Sending in a 4 x 4 matrix with float values
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"), # Get location of projection uniform matrix
            1, GL_FALSE, projection_transform     # Number of matrices putting in and whether to transpose them. Lasr arguement matrix we send in
        )

        # Don't have to query projection matrix because used every frame or something like that
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

        print("Setup complete!")


    def render(self, rotate, scale, x, y, z):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   # Colour buffer stores all pixels on screen. Colours stored in colour buffer bit thing
        glUseProgram(self.shader)  # You may not need this line

        #Uncomment this for triangle rendering
        # Draws the triangle
        # Was bound in youtube vid but not here
        # Using triangles
        # Vertex 0 where we start from
        # Vertext count is number of points to draw
        #glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertexCount)

        # Uncomment this for model rendering
        #glDrawArrays(GL_TRIANGLES, 0, self.cube.vertexCount)


        count = 0
        for cube in self.scene.cubes:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)    # Gonna leave this here for now
            if count == 0:
                if (rotate >= 0 & rotate <=2):
                    cube.eulers[rotate] += 0.25
                    if cube.eulers[rotate] > 360:
                        cube.eulers[rotate] -= 360

                # refresh screen

                # Start with identity and multiply on progressively

                """    Eulers represent through rotations 
                    pitch: rotation around x axis
                    roll:rotation around z axis
                    yaw: rotation around y axis
                """

                # Rotate cube around axis I think
                model_transform = pyrr.matrix44.multiply(
                    m1=model_transform,
                    m2=pyrr.matrix44.create_from_eulers(
                        eulers=np.radians(cube.eulers), dtype=np.float32
                    )
                )
            elif count > 0:
                # translate
                model_transform = pyrr.matrix44.multiply(
                    m1=model_transform,
                    m2=pyrr.matrix44.create_from_translation(np.array([3, 0, 0]), dtype=np.float32)
                )

                if (rotate >= 0 & rotate <=2):
                    cube.eulers[rotate] += 0.25
                    if cube.eulers[rotate] > 360:
                        cube.eulers[rotate] -= 360

                model_transform = pyrr.matrix44.multiply(
                    m1=model_transform,
                    m2=pyrr.matrix44.create_from_eulers(
                        eulers=np.radians(cube.eulers), dtype=np.float32
                    )
                )

                model_transform = pyrr.matrix44.multiply(
                    m1=model_transform,
                    m2=pyrr.matrix44.create_from_translation(np.array([3, 0, 0]), dtype=np.float32)
                )

            # Send to position
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(cube.position), dtype=np.float32
                )
            )
            # Scale
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_scale(np.array([scale, scale, scale]), dtype=np.float32)
            )
            # translate
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(np.array([x, y, z]), dtype=np.float32)
            )

            # Send to position
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(cube.position), dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            self.wood_texture.use()

            glBindVertexArray(self.cube_load.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_load.vertexCount)
            # Swap the front and back buffers on the window, effectively putting what we just "drew"
            # Onto the screen (whereas previously it only existed in memory)
            count = count + 1
        pg.display.flip()

        #
        self.clock.tick(100)  # might need this

    def cleanup(self):
        # Deleting vao , represents list
        glDeleteVertexArrays(1, (self.vao,))
        # Uncomment for triangle rendering
        #self.triangle.cleanup()
        # Uncomment for model rendering
        self.cube.cleanup()


class Material:

    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(filepath).convert()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))