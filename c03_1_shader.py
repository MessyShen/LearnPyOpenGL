'''
Siyuan Shen 2020.10
https://learnopengl.com/Getting-started/Hello-Triangle
'''

import numpy as np

import glfw
from OpenGL.GL import *
from ctypes import c_void_p
from utils.shader_program import ShaderProgram

def size_of(numpy_array):
    '''
    size of a numpy array
    '''
    return numpy_array.itemsize * numpy_array.size


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def main():
    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(1280, 720, "LearnOpenGL", None, None)

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)


    my_shader_program = ShaderProgram("shaders/c03_triangle_vs.glsl", 
                                      "shaders/c03_triangle_fs.glsl")
    shader_program = my_shader_program.program_id
    success = glGetProgramiv(shader_program, GL_LINK_STATUS)

    vertices = np.array([
        0.5,  0.5, 0.0,  1.0, 0.0, 0.0, 
        0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
        -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,
        -0.5,  0.5, 0.0, 1.0, 0.0, 0.0
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 3,
        1, 2, 3
    ], dtype=np.int32)
    
    '''
    What is a VAO?
    when configuring vertex attribute, you only need to run those once.
    '''
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    # copy vertex info mation to buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, size_of(vertices), vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, size_of(indices), indices, GL_STATIC_DRAW)

    # set vertex attribute pointer
    # the fifth param is STRIDE: 3*size of float
    f_size = vertices.itemsize
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * f_size, c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * f_size, c_void_p(3 * f_size))
    glEnableVertexAttribArray(1)


    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # polygon mode

    while not glfw.window_should_close(window):
        process_input(window)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # we need a shader program
        glUseProgram(shader_program)
        glBindVertexArray(VAO)
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        # glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return

main()




