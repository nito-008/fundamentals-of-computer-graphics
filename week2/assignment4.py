from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, sys, time, random, colorsys

state = {"last": None, "t": 0.0}
lists = {"flower": None}
random.seed(42)


class F:
    def __init__(s):
        s.x = random.uniform(-0.95, 0.95)
        s.y = random.uniform(-0.95, 0.95)
        s.vx = random.uniform(-0.25, 0.25)
        s.vy = random.uniform(-0.25, 0.25)
        s.a = random.uniform(0, 360)
        s.va = random.uniform(-90, 90)
        s.s0 = random.uniform(0.12, 0.28)
        s.pfreq = random.uniform(0.2, 1.0)
        s.phase = random.uniform(0, 2 * math.pi)
        s.orb = random.uniform(0.0, 0.15)
        s.orbf = random.uniform(0.05, 0.25)
        s.k = random.choice([4, 5, 6, 7])


flowers = [F() for _ in range(5)]


def build_flower():
    fid = glGenLists(1)
    glNewList(fid, GL_COMPILE)
    glBegin(GL_TRIANGLE_FAN)
    glColor4f(1, 1, 1, 0.06)
    glVertex2f(0, 0)
    n = 720
    for i in range(n + 1):
        th = 2 * math.pi * i / n
        r = 0.82 * abs(math.cos(5 * th))
        x, y = r * math.cos(th), r * math.sin(th)
        h = (i % n) / n
        c = colorsys.hsv_to_rgb(h, 0.6, 1.0)
        glColor4f(c[0], c[1], c[2], 0.28)
        glVertex2f(x, y)
    glEnd()
    glBegin(GL_LINE_LOOP)
    glColor4f(1, 1, 1, 0.72)
    for i in range(n):
        th = 2 * math.pi * i / n
        r = 0.82 * abs(math.cos(5 * th))
        glVertex2f(r * math.cos(th), r * math.sin(th))
    glEnd()
    glEndList()
    lists["flower"] = fid


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for f in flowers:
        glPushMatrix()
        ox = f.orb * math.cos(state["t"] * 2 * math.pi * f.orbf + f.phase)
        oy = f.orb * math.sin(state["t"] * 2 * math.pi * f.orbf + f.phase * 0.7)
        glTranslatef(f.x + ox, f.y + oy, 0)
        glRotatef(f.a, 0, 0, 1)
        s = f.s0 * (1.0 + 0.18 * math.sin(state["t"] * 2 * math.pi * f.pfreq + f.phase))
        glScalef(s, s, 1)
        glCallList(lists["flower"])
        glPopMatrix()
    glutSwapBuffers()


def timer(_):
    now = time.perf_counter()
    dt = 0.016 if state["last"] is None else max(0.0, min(0.05, now - state["last"]))
    state["last"] = now
    state["t"] += dt
    for f in flowers:
        f.x += f.vx * dt
        f.y += f.vy * dt
        f.a = (f.a + f.va * dt) % 360
        r = f.s0
        if f.x < -1 + r:
            f.x = -1 + r
            f.vx *= -1
        if f.x > 1 - r:
            f.x = 1 - r
            f.vx *= -1
        if f.y < -1 + r:
            f.y = -1 + r
            f.vy *= -1
        if f.y > 1 - r:
            f.y = 1 - r
            f.vy *= -1
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)


def init():
    glClearColor(0.02, 0.03, 0.06, 1)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth(2.0)
    build_flower()


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(720, 720)
    glutCreateWindow(sys.argv[0])
    init()
    glutDisplayFunc(display)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()
