import os
import sys
import glm
import numpy as np
from OpenGL.GL import *
# this class is needed to create shader program and attach shaders to it.

class ShaderProgram(object):
    def __init__(self, vertpath="", fragpath=""):
        # paths to files should be set correctly
        # yep it will contain paths to shaders.
        self.vertpath = vertpath
        self.fragpath = fragpath
        vflag = os.path.exists(self.vertpath)
        fflag = os.path.exists(self.fragpath)
        if not vflag:
            print ("Vertex shader file (--> %s <--) doesn't exist!"%self.vertpath)
        if not fflag:
            print ("Fragment shader file (--> %s <--) doesn't exist!"%self.fragpath)
        if not (fflag and vflag):
            sys.exit(1)
        self.initProgram()

    def getShader(self, shader_source, shader_type):
        try:
            shader_id = glCreateShader(shader_type)
            glShaderSource(shader_id, shader_source)
            glCompileShader(shader_id)
            if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
                info = glGetShaderInfoLog(shader_id)
                raise RuntimeError('Shader compilation failed:\n %s'%info)
            return shader_id
        except:
            glDeleteShader(shader_id)
            raise

    def loadShader(self, path):
        source_file = open(path)
        shader_source = source_file.read()
        source_file.close()
        return shader_source

    def use(self):
        glUseProgram(self.program_id)
        return

    def initProgram(self):
        # create unique shader program id
        self.program_id = glCreateProgram()
        # load and compile individual shaders
        vertsource = self.loadShader(self.vertpath)
        fragsource = self.loadShader(self.fragpath)
        vert_id = self.getShader(vertsource, GL_VERTEX_SHADER)
        frag_id = self.getShader(fragsource, GL_FRAGMENT_SHADER)
        # if it's ok, attach them to shader program
        glAttachShader(self.program_id, vert_id)
        glAttachShader(self.program_id, frag_id)
        # link program means make program obj with created executables for different programmable processors for shaders,
        # that were attached.
        glLinkProgram(self.program_id)
        # if something went wrong
        if glGetProgramiv(self.program_id, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(self.program_id)
            glDeleteProgram(self.program_id)
            # they should be deleted anyway
            glDeleteShader(vert_id)
            glDeleteShader(frag_id)
            raise RuntimeError("Error in program linking: %s"%info)
        # shaders are attached, program is linked -> full shader program with compiled executables is ready,
        # no need in individual shaders ids, i suppose
        glDeleteShader(vert_id)
        glDeleteShader(frag_id)

    def attribLocation(self, name):
        return glGetAttribLocation(self.program_id, name)

    def uniformLocation(self, name):
        return glGetUniformLocation(self.program_id, name)


    def setBool(self, name, value):
        glUniform1i(glGetUniformLocation(self.program_id, name), int(value))

    def setVec3(self, name, value):
        glUniform3fv(glGetUniformLocation(self.program_id, name), 1, glm.value_ptr(value))

    def setFloat(self, name, value):
        glUniform1f(glGetUniformLocation(self.program_id, name), value)

    def setMat4(self, name, mat):
        glUniformMatrix4fv(glGetUniformLocation(self.program_id, name), 1, GL_FALSE, glm.value_ptr(mat))