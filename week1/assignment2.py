import sys
import colorsys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math


def draw_circle(x_offset, y_offset, r, color):
    glColor3d(color[0], color[1], color[2])
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        x = math.cos(i * 3.14159 / 180.0)
        y = math.sin(i * 3.14159 / 180.0)
        glVertex2d(x * r + x_offset, y * r + y_offset)
    glEnd()


def display():
    glClearColor(0, 0, 0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    for i in range(360):
        x = math.cos(i * 3.14159 / 180.0)
        y = math.sin(i * 3.14159 / 180.0)
        draw_circle(x, y, 0.5, colorsys.hsv_to_rgb(1 * i / 360, 1, 1))

    glFlush()  # 画面出力


if __name__ == "__main__":
    glutInit(sys.argv)  # ライブラリの初期化
    glutInitWindowSize(400, 400)  # ウィンドウサイズを指定
    glutCreateWindow(sys.argv[0])  # ウィンドウを作成
    glutDisplayFunc(display)  # 表示関数を指定
    glutMainLoop()  # イベント待ち
