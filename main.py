from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy
import time

start_time = time.time()
new_time = time.time()
new_day = time.time()
year = 0
day = 0
sun_texture = 0
bumi_texture = 0
background_texture = 0
resetDay = 0
day_year = 0
moonKet = "Bulan Baru"

def read_textures():
    global sun_texture, bumi_texture, background_texture
    
    sun_texture = read_texture("sun.jpg")
    bumi_texture = read_texture("earth.jpg")

    background_texture = read_texture("gala.jpg")

def read_texture(filename):
    """
    Reads an image file and converts to an OpenGL-readable texture format
    """
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.uint8)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id


def init(): 
    glClearColor(0.5, 0.5, 0.5, 0.5)
    glShadeModel(GL_FLAT)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

def draw_custom_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 800)  # Adjust the coordinates based on your window size
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)  # Matikan pencahayaan sementara
    glColor3f(0.0, 1.0, 0.0)  # Set text color to green
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))
    glEnable(GL_LIGHTING)  # Hidupkan pencahayaan kembali


    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)    

def display():
    global year, day, sun_texture, bumi_texture, background_texture, resetDay, moonKet, new_time, new_day, day_year# Add these global declarations

    t = time.time() - start_time
    resetDay = time.time() - new_time
    day_year = time.time() - new_day
    year_period = 120.0  # 5 seconds for simulating one year
    year = (t / year_period)
    resetDay = int(365 * (resetDay / year_period))
    day_year = str(int(365 * (day_year / year_period)))
    day = 365 * year
    moon_sid = (365 / 27.3) * year
    dayLis = int(day)
    dayList = str(dayLis)
    
    if(resetDay >= 1 and resetDay <= 4):
        moonKet = "Bulan Sabit"
    elif(resetDay >= 5 and resetDay <= 8):
        moonKet = "Bulan Paruh"
    elif(resetDay >= 9 and resetDay <= 11):
        moonKet = "Bulan Cembung"
    elif(resetDay >= 12 and resetDay <= 14): 
        moonKet = "Bulan Purnama"
    elif(resetDay >= 15 and resetDay <= 17):
        moonKet = "Bulan Cembung"
    elif(resetDay >= 18 and resetDay <= 21):
        moonKet = "Bulan Paruh"
    elif(resetDay >= 22 and resetDay <= 25):
        moonKet = "Bulan Sabit"
    elif((resetDay >= 26 and resetDay <= 30) or resetDay == 0):
        moonKet = "Bulan Baru"

    if(resetDay == 30):
        new_time = time.time()

    if(day_year == "365"):
        new_day = time.time()


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Set light position


    # Draw background
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-10.0, -10.0, -5.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(10.0, -10.0, -5.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(10.0, 10.0, -5.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-10.0, 10.0, -5.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Set light position
    light_position = [0.0, 0.0, 0.0, 1.0]  # Directional light from the sun
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    # Render Text (Hello, World!)
    # glColor3f(1.0, 1.0, 1.0)  # Set text color to whit
    # Render additional text
    draw_custom_text(50, 750, "Rotasi Bulan Memutari Bumi dan Bumi Memutari")  # Adjust the position as needed
    draw_custom_text(50, 700, "Hari Ke : "+day_year)  # Adjust the position as needed
    draw_custom_text(50, 650, "Fase Bulan : "+moonKet)  # Adjust the position as needed

    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    # sun_texture = read_texture("sun.jpg")
    glBindTexture(GL_TEXTURE_2D, sun_texture)
    glColor4f(1.0, 1.0, 0, 1)
    qobj = gluNewQuadric()
    gluQuadricTexture(qobj, GL_TRUE)
    gluSphere(qobj, 1.0, 50, 50)
    glDisable(GL_TEXTURE_2D)

    glEnable(GL_LIGHTING)

    glPushMatrix()

    glRotatef(year * 360.0, 0.0, 1.0, 0.0)  # earth rotation around the sun
    glTranslatef(3.0, 0.0, 0.0)  # earth location

    glPushMatrix()  # push earth system

    glPushMatrix()
    glRotatef(day * 360.0, 0.0, 1.0, 0.0)  # earth spin
    glRotatef(90 - 23.4, 1.0, 0.0, 0.0)  # earth axis
    earth_ambient = [1.0, 1.0, 1.0, 1.0]
    earth_diffuse = [0.8, 0.8, 1.0, 1.0]
    earth_specular = [0.7, 0.7, 0.7, 1.0]
    earth_shininess = 30.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, earth_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, earth_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, earth_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, earth_shininess)
    glColor3f(0, 0, 1)  # blue

    glEnable(GL_TEXTURE_2D)
    # bumi_texture = read_texture("earth.jpg")
    glBindTexture(GL_TEXTURE_2D, bumi_texture)
    gluSphere(qobj, 0.3, 10, 8)
    # glutSolidSphere(0.3, 10, 8)  # earth
    glPopMatrix()

    glPushMatrix()
    moon_ambient = [0.8, 0.8, 0.8, 1.0]
    moon_diffuse = [0.6, 0.6, 1.0, 1.0]
    moon_specular = [0.5, 0.5, 0.5, 1.0]
    moon_shininess = 100.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, moon_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, moon_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, moon_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, moon_shininess)
    glRotatef(moon_sid * 360.0, 0.0, 1.0, 0.0)  # moon sidereal
    glTranslatef(1.0, 0.0, 0.0)  # distance moon to earth
    glRotatef(90, 1.0, 0.0, 0.0)
    glColor4f(0.4, 0.5, 0.6, 1)
    glutSolidSphere(0.1, 10, 8)  # moon
    glPopMatrix()

    glPopMatrix()  # pop earth system

    

    glPopMatrix()
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70.0, w / h, 1.0, 20.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1200, 800)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Sistem Solar Bumi Bulan Matahari")

init()
read_textures()
glutDisplayFunc(display)
glutIdleFunc(display)
glutReshapeFunc(reshape)


glutMainLoop()