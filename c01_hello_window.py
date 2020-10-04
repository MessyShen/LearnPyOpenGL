'''
Siyuan Shen 2020.10
https://learnopengl.com/Getting-started/Hello-Window
'''

import glfw
from OpenGL.GL import *

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

    if not window:
        print("init window fails")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    while not glfw.window_should_close(window):
        process_input(window)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return

if __name__ == '__main__':
    main()