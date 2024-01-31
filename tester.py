import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def triangle():
    glBegin(GL_POLYGON)
    glVertex2f(-0.5, -0.5)
    glVertex2f(-0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glEnd()

def init():
    glClearColor(0.0, 0.0, 1.0, 1.0) # BG Color
    glColor3f(1.0, 0.0, 1.0) # object color

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_caption('Init func!')
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            init()
            triangle()
            pygame.display.flip()
            pygame.time.wait(10)

main()