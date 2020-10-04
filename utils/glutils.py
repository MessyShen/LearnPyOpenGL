from OpenGL.GL import *
from ctypes import c_void_p

def set_position_attribute(location, size, stride, offset):
    glEnableVertexAttribArray(location)
    glVertexAttribPointer(location, size, GL_FLOAT, GL_FALSE, stride * 4, c_void_p(offset * 4))

def loadImage(imageName):
    """Load an image from a file using PIL.
    This is closer to what you really want to do than the
    original port's crammed-together stuff that set global
    state in the loading method.  Note the process of binding
    the texture to an ID then loading the texture into memory.
    This didn't seem clear to me somehow in the tutorial.
    """
    try:
        from PIL.Image import open
    except ImportError:
        from Image import open
    im = open(imageName)
    # im = im.convert("RGBA")
    try:
        ix, iy, image = im.size[0], im.size[1], im.tobytes("raw", "RGB", 0, -1)
    except SystemError:
        ix, iy, image = im.size[0], im.size[1], im.tobytes("raw", "RGB", 0, -1)
    # generate a texture ID
    ID=glGenTextures(1)
    # make it current
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # copy the texture into the current texture ID
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    print(ix,iy)
    glGenerateMipmap(GL_TEXTURE_2D)
    # return the ID for use
    return ID


def load_texture(path):
    from PIL import Image
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture