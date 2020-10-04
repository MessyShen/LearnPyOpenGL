'''
Siyuan Shen 2020.10
https://learnopengl-cn.github.io/02%20Lighting/03%20Materials/
'''

import numpy as np

import glfw
import glm
from OpenGL.GL import *
from ctypes import c_void_p
from utils.shader_program import ShaderProgram
from utils.camera_glm import Camera
from utils.objLoader import ObjLoader
from utils.glutils import load_texture

screenWidth = 1920
screenHeight = 1080

# camera
camera = Camera(glm.vec3(0.0, 0.0, 3.0))
lastX = screenWidth / 2.0
lastY = screenHeight / 2.0
firstMouse = True

# lighting
lightPos = glm.vec3(5.0, 1.0, 2.0)

# timing
deltaTime = 0.0
lastFrame = 0.0



def size_of(numpy_array):
    '''
    size of a numpy array
    '''
    return numpy_array.itemsize * numpy_array.size

def process_input(window):
    global deltaTime
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.ProcessKeyboard("FORWARD", deltaTime)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.ProcessKeyboard("LEFT", deltaTime)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.ProcessKeyboard("BACKWARD", deltaTime)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.ProcessKeyboard("RIGHT", deltaTime)





def main():
    global lastFrame, deltaTime
    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(screenWidth, screenHeight, "LearnOpenGL", None, None)

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # tell glfw to capture our mouse
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)

    lighting_shader_program = ShaderProgram("shaders/c05_materials.vs", 
                                            "shaders/c05_materials.fs")
    lighting_shader = lighting_shader_program.program_id

    lightcube_shader_program = ShaderProgram("shaders/c05_lightcube.vs", 
                                             "shaders/c05_lightcube.fs")
    lightcube_shader = lightcube_shader_program.program_id

    texture_floor_shader = ShaderProgram("shaders/c06_floor.vs", "shaders/c06_floor.fs")

    vertices = np.array([
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
         0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
        -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,

        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
         0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
        -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,

        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,
        -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,

         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,
         0.5,  0.5, -0.5,  1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
         0.5, -0.5,  0.5,  1.0,  0.0,  0.0,
         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,

        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
         0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
        -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,

        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
        -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 3,
        1, 2, 3
    ], dtype=np.int32)


    bar_indices, bar_buffer = ObjLoader.load_model("models/bar.obj")
    floor_indices, floor_buffer = ObjLoader.load_model("models/floor.obj")
    
    '''
    What is a VAO?
    when configuring vertex attribute, you only need to run those once.
    '''
    cubeVAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    # EBO = glGenBuffers(1)

    glBindVertexArray(cubeVAO)
    # copy vertex info mation to buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, size_of(bar_buffer), bar_buffer, GL_STATIC_DRAW)

    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, size_of(indices), indices, GL_STATIC_DRAW)

    # set vertex attribute pointer
    # the fifth param is STRIDE: 3*size of float
    f_size = bar_buffer.itemsize
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * f_size, c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * f_size, c_void_p(3 * f_size))
    glEnableVertexAttribArray(1)

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * f_size, c_void_p(5 * f_size))
    glEnableVertexAttribArray(2)

    # set cube vbo
    lightCubeVAO = glGenVertexArrays(1)
    lightCubeVBO = glGenBuffers(1)
    glBindVertexArray(lightCubeVAO)

    glBindBuffer(GL_ARRAY_BUFFER, lightCubeVBO)
    glBufferData(GL_ARRAY_BUFFER, size_of(vertices), vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * f_size, c_void_p(0))
    glEnableVertexAttribArray(0)


    # set floor
    floorVAO = glGenVertexArrays(1)
    floorVBO = glGenBuffers(1)
    glBindVertexArray(floorVAO)

    glBindBuffer(GL_ARRAY_BUFFER, floorVBO)
    glBufferData(GL_ARRAY_BUFFER, size_of(floor_buffer), floor_buffer, GL_STATIC_DRAW)
    f_size = bar_buffer.itemsize
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * f_size, c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * f_size, c_void_p(3 * f_size))
    glEnableVertexAttribArray(1)

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * f_size, c_void_p(5 * f_size))
    glEnableVertexAttribArray(2)
    
    floor_texture = load_texture("resources/textures/floor.jpg")

    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # polygon mode

    while not glfw.window_should_close(window):
        # per-frame time logit
        current_frame = glfw.get_time()
        deltaTime = current_frame - lastFrame
        lastFrame = current_frame

        process_input(window)

        glClearColor(0.9, 0.9, 0.9, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        lighting_shader_program.use()
        lighting_shader_program.setVec3("light.position", lightPos)
        lighting_shader_program.setVec3("viewPos", camera.Position)

        lightColor = glm.vec3()
        lightColor.x = glm.sin(glfw.get_time() * 2.0)
        lightColor.y = glm.sin(glfw.get_time() * 0.7)
        lightColor.z = glm.sin(glfw.get_time() * 1.3)
        lightColor = glm.vec3(0.9, 0.8, 0.1)
        diffuseColor = lightColor * glm.vec3(0.5)
        ambientColor = diffuseColor * glm.vec3(0.2)
        lighting_shader_program.setVec3("light.ambient", ambientColor)
        lighting_shader_program.setVec3("light.diffuse", diffuseColor)
        lighting_shader_program.setVec3("light.specular", glm.vec3(1.0, 1.0, 1.0))
        lighting_shader_program.setVec3("material.ambient", glm.vec3(1.0, 0.5, 3.1))
        lighting_shader_program.setVec3("material.diffuse", glm.vec3(1.0, 0.5, 3.1))
        lighting_shader_program.setVec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
        lighting_shader_program.setFloat("material.shininess", 8.0)

        projection = glm.perspective(glm.radians(camera.Zoom), float(screenWidth / screenHeight), 0.1, 100)
        view = camera.getViewMatrix()
        lighting_shader_program.setMat4("projection", projection)
        lighting_shader_program.setMat4("view", view)

        model = glm.mat4(1.0)
        lighting_shader_program.setMat4("model", model)

        # render the cube
        glBindVertexArray(cubeVAO)
        glDrawArrays(GL_TRIANGLES, 0, len(bar_indices))
        # glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        # glDrawArrays(GL_TRIANGLES, 0, 3)
        texture_floor_shader.use()
        texture_floor_shader.setMat4("projection", projection)
        texture_floor_shader.setMat4("view", view)
        texture_floor_shader.setMat4("model", model)
        glBindVertexArray(floorVAO)
        glBindTexture(GL_TEXTURE_2D, floor_texture)
        glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))


        # also draw the lamp object
        lightcube_shader_program.use()
        lightcube_shader_program.setMat4("projection", projection)
        lightcube_shader_program.setMat4("view", view)
        model = glm.mat4(1.0)
        model = glm.translate(model, lightPos)
        model = glm.scale(model, glm.vec3(0.2))
        lightcube_shader_program.setMat4("model", model)
        glBindVertexArray(lightCubeVAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)


        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def mouse_callback(window, xpos, ypos):
    global firstMouse, lastX, lastY
    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False
    
    x_offset = xpos - lastX
    y_offset = ypos - lastY

    lastX = xpos
    lastY = ypos

    camera.ProcessMouseMovement(x_offset, y_offset)

def scroll_callback(window, xoffset, yoffset):
    camera.ProcessMouseScroll(yoffset)


main()