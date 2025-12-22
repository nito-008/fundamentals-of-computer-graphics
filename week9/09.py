import sys
import math
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *


# 3次元ベクトルを作る
def vec3(x, y, z):
    return np.array([x, y, z], dtype=np.float64)


# 長さを計算する
def length(v):
    return np.linalg.norm(v)


# 長さを1に正規化する
def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0.0 else v


# 質点
class Point:
    def __init__(self):
        self.f = vec3(0, 0, 0)  # 質点に働く力のベクトル
        self.v = vec3(0, 0, 0)  # 速度ベクトル
        self.p = vec3(0, 0, 0)  # 位置
        self.bFixed = False  # 固定されているかどうか


# バネ
class Spring:
    def __init__(self, p0, p1):
        self.p0 = p0  # 質点0
        self.p1 = p1  # 質点1
        self.restLength = length(p0.p - p1.p)  # 自然長


POINT_NUM = 20


# 布の定義
class Cloth:
    def __init__(self):
        self.points = [[Point() for x in range(POINT_NUM)] for y in range(POINT_NUM)]
        self.springs: list[Spring] = []

        # 質点の定義
        for y in range(POINT_NUM):
            for x in range(POINT_NUM):
                self.points[x][y].bFixed = False
                self.points[x][y].p = vec3(x - POINT_NUM / 2, POINT_NUM / 2, -y)

        # バネの設定
        for y in range(POINT_NUM):
            for x in range(POINT_NUM):
                # 横方向のバネ
                if x < POINT_NUM - 1:
                    self.springs.append(
                        Spring(self.points[x][y], self.points[x + 1][y])
                    )

                # 縦方向のバネ
                if y < POINT_NUM - 1:
                    self.springs.append(
                        Spring(self.points[x][y], self.points[x][y + 1])
                    )

                # 右下方向のバネ
                if x < POINT_NUM - 1 and y < POINT_NUM - 1:
                    self.springs.append(
                        Spring(self.points[x][y], self.points[x + 1][y + 1])
                    )

                # 左下方向のバネ
                if x > 0 and y < POINT_NUM - 1:
                    self.springs.append(
                        Spring(self.points[x][y], self.points[x - 1][y + 1])
                    )

        # 固定点の指定
        self.points[0][0].bFixed = True
        self.points[POINT_NUM - 1][0].bFixed = True

    def update(self):
        for y in range(POINT_NUM):
            for x in range(POINT_NUM):
                self.points[x][y].f = vec3(0, 0, 0)

        for y in range(POINT_NUM):
            for x in range(POINT_NUM):
                if not self.points[x][y].bFixed:
                    self.points[x][y].f += g_Gravity * g_Mass

        for s in self.springs:
            p0 = s.p0
            p1 = s.p1
            v = p1.p - p0.p
            l = length(v)
            if l > 0:
                direction = v / l
                force_magnitude = g_Ks * (l - s.restLength)
                force = force_magnitude * direction
                p0.f += force
                p1.f -= force

        for y in range(POINT_NUM):
            for x in range(POINT_NUM):
                p = self.points[x][y]
                if not p.bFixed:
                    p.f -= g_Dk * p.v

                    acceleration = p.f / g_Mass
                    p.v += acceleration * g_dT
                    p.p += p.v * g_dT

    def draw(self):
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        for spring in self.springs:
            glVertex3dv(spring.p0.p)
            glVertex3dv(spring.p1.p)
        glEnd()

        glColor3f(1.0, 0.0, 0.0)
        glPointSize(4.0)
        glBegin(GL_POINTS)
        for y in range(POINT_NUM):
            for x in range(POINT_NUM):
                glVertex3dv(self.points[x][y].p)
        glEnd()


g_WindowID = 0  # ウィンドウ識別子

g_Cloth = Cloth()  # 布
g_RotateAngleH_deg = 0.0  # 画面水平方向の回転角度
g_RotateAngleV_deg = 0.0  # 画面垂直方向の回転角度
g_PreMousePositionX = 0  # マウスの前回の位置
g_PreMousePositionY = 0  # マウスの前回の位置
g_bRunning = True  # シミュレーションの実行中かどうか

g_Ks = 8.0  # バネ定数
g_Mass = 30.0  # 質点の質量
g_dT = 1.0  # 時間刻み幅
g_Dk = 0.1  # 空気抵抗係数
g_Gravity = vec3(0, -0.002, 0)  # 重力加速度


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_LIGHTING)
    glLoadIdentity()
    glTranslated(0, 0.0, -50)

    glRotated(g_RotateAngleV_deg, 1.0, 0.0, 0.0)
    glRotated(g_RotateAngleH_deg, 0.0, 1.0, 0.0)

    g_Cloth.draw()

    glutSwapBuffers()


# ウィンドウのサイズが変更されたときの処理
def resize(w, h):
    if h > 0:
        glViewport(0, 0, w, h)
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30.0, float(w) / float(h), 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)


def mouse(button, state, x, y):
    global g_PreMousePositionX, g_PreMousePositionY
    if button in [GLUT_LEFT_BUTTON, GLUT_RIGHT_BUTTON]:
        g_PreMousePositionX = x
        g_PreMousePositionY = y


def motion(x, y):
    global \
        g_RotateAngleH_deg, \
        g_RotateAngleV_deg, \
        g_PreMousePositionX, \
        g_PreMousePositionY
    g_RotateAngleH_deg += (x - g_PreMousePositionX) * 0.1
    g_RotateAngleV_deg += (y - g_PreMousePositionY) * 0.1
    g_PreMousePositionX = x
    g_PreMousePositionY = y
    glutPostRedisplay()


def timer(value):
    global g_bRunning
    if g_bRunning:
        g_Cloth.update()
    glutPostRedisplay()
    glutTimerFunc(10, timer, 0)


# キーが押されたときのイベント処理
def keyboard(key, x, y):
    global g_bRunning
    if key in [b"q", b"Q", b"\x1b"]:
        glutDestroyWindow(g_WindowID)
        return
    elif key == b"a":  # a キーでアニメーションのオン/オフ
        g_bRunning = not g_bRunning

    glutPostRedisplay()


def init():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


if __name__ == "__main__":
    glutInit(sys.argv)  # ライブラリの初期化
    glutInitWindowSize(600, 600)  # ウィンドウサイズを指定
    glutInitDisplayMode(
        GLUT_RGBA | GLUT_DEPTH | GLUT_DOUBLE
    )  # ディスプレイモードの設定
    g_WindowID = glutCreateWindow(sys.argv[0])  # ウィンドウを作成
    glutDisplayFunc(display)  # 表示関数を指定
    glutReshapeFunc(resize)  # ウィンドウサイズが変更されたときの関数を指定
    glutKeyboardFunc(keyboard)  # キーボード関数を指定
    glutMouseFunc(mouse)  # マウス関数を指定
    glutMotionFunc(motion)  # マウスの動きを指定
    timer(0)  # タイマー関数を指定
    init()  # 初期設定を行う関数を指定
    glutMainLoop()  # イベント待ち
