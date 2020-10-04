import glm
import numpy as np
from OpenGL.GL import GL_TRUE

class Camera:
    def __init__(self, position=None, up=None, front=None,
                       yaw=-90.0, pitch=0.0):
        if position is None:
            self.Position = glm.vec3(0.0, 0.0, 0.0)
        else:
            self.Position = position
        
        if front is None:
            self.Front = glm.vec3(0.0, 0.0, -1.0)
        else:
            self.Front = front
        
        if up is None:
            self.WorldUp = glm.vec3(0.0, 1.0, 0.0)
        else:
            self.WorldUp = up
        
        self.Right = glm.vec3()
        self.Up = glm.vec3()

        self.Yaw   = yaw
        self.Pitch = pitch

        self.MovementSpeed = 2.5
        self.MouseSensitivity = 0.1
        self.Zoom = 45.0
        self.updateCameraVectors()

    def getViewMatrix(self):
        return glm.lookAt(self.Position, self.Position + self.Front, self.Up)

    def ProcessKeyboard(self, direction, deltaTime):
        velocity = self.MovementSpeed * deltaTime
        # print(direction, self.Position, velocity)
        if direction == "FORWARD":
            self.Position += self.Front * velocity
        if direction == "BACKWARD":
            self.Position -= self.Front * velocity
        if direction == "LEFT":
            self.Position -= self.Right * velocity
        if direction == "RIGHT":
            self.Position += self.Right * velocity

    def ProcessMouseMovement(self, xoffset, yoffset, constrainPicth=GL_TRUE):
        xoffset *= self.MouseSensitivity
        yoffset *= self.MouseSensitivity

        self.Yaw += xoffset
        self.Pitch += yoffset

        if constrainPicth == GL_TRUE:
            if self.Pitch > 89.0:
                self.Pitch = 89.0
            if self.Pitch < -89.0:
                self.Pitch = -89.0

        self.updateCameraVectors()

    def ProcessMouseScroll(self, yoffset):
        self.Zoom -= yoffset
        if self.Zoom < 1.0:
            self.Zoom = 1.0
        if self.Zoom > 45.0:
            self.Zoom = 45.0


    def updateCameraVectors(self):
        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.Yaw)) * glm.cos(glm.radians(self.Pitch))
        front.y = glm.sin(glm.radians(self.Pitch))
        front.z = glm.sin(glm.radians(self.Yaw)) * glm.cos(glm.radians(self.Pitch))
        self.Front = front
        self.Right = glm.normalize(glm.cross(self.Front, self.WorldUp))
        self.Up    = glm.normalize(glm.cross(self.Right, self.Front))
