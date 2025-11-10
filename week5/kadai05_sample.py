import sys
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 制御点を格納する配列
g_ControlPoints = []

# ウィンドウサイズを保持する
g_WindowWidth = 512
g_WindowHeight = 512

# ノットベクトル
# この配列の値を変更することで基底関数が変化する。その結果として形が変わる。
# 下の例では、一定間隔で値が変化するので、「一様Bスプライン曲線」となる
g_NotVector = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 課題(2)では次のノットベクトルを変更する
# g_NotVector = [0, 0, 0, 0, 1, 1, 1, 1]


# 基底関数 N{i,n}(t)の値を計算する
def getBaseN(i, n, t) -> float:
    if n == 0:
        # n が 0 の時だけ t の値に応じて 0 または 1 を返す
        if g_NotVector[i] <= t < g_NotVector[i + 1]:
            return 1.0
        return 0.0
    else:
        # 係数を計算するときに、ノットが重なる（分母がゼロとなる）ときには、その項を無視する
        term1 = 0.0
        denominator1 = g_NotVector[i + n] - g_NotVector[i]
        if denominator1 != 0.0:
            term1 = ((t - g_NotVector[i]) / denominator1) * getBaseN(i, n - 1, t)

        term2 = 0.0
        denominator2 = g_NotVector[i + n + 1] - g_NotVector[i + 1]
        if denominator2 != 0.0:
            term2 = ((g_NotVector[i + n + 1] - t) / denominator2) * getBaseN(
                i + 1, n - 1, t
            )

        return term1 + term2


# 表示部分をこの関数で記入
def display():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)

    # 制御点の描画
    glPointSize(5)
    glColor3d(0.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    for point in g_ControlPoints:
        glVertex2dv(point)
    glEnd()

    # 制御点を結ぶ線分の描画
    glColor3d(1.0, 0.0, 0.0)
    glLineWidth(1)
    glBegin(GL_LINE_STRIP)
    for point in g_ControlPoints:
        glVertex2dv(point)
    glEnd()

    # ここにBスプライン曲線を描画するプログラムコードを入れる
    # ヒント1: 3次Bスプラインの場合は制御点を4つ入れるまでは何も描けない
    # ヒント2: パラメータtの値の取り得る範囲に注意
    if len(g_ControlPoints) >= 4:
        glColor3d(0.0, 0.0, 0.0)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)

        t_start = g_NotVector[3]
        t_end = g_NotVector[len(g_ControlPoints)]

        for t in np.arange(t_start, t_end, 0.01):
            point_on_curve = np.array([0.0, 0.0])
            for i in range(len(g_ControlPoints)):
                base_n = getBaseN(i, 3, t)
                point_on_curve += base_n * g_ControlPoints[i]
            glVertex2dv(point_on_curve)
        glEnd()

    glFlush()  # 画面出力


# ウィンドウのサイズが変更されたときの処理
def resize(w, h):
    if h > 0:
        glViewport(0, 0, w, h)
        g_WindowWidth = w
        g_WindowHeight = h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # ウィンドウ内の座標系設定
        # マウスクリックの座標と描画座標が一致するような正投影
        glOrtho(0, w, h, 0, -10, 10)
        glMatrixMode(GL_MODELVIEW)


# マウスクリックのイベント処理
def mouse(button, state, x, y):
    if state == GLUT_DOWN:
        # 左ボタンだったらクリックした位置に制御点を置く
        if button == GLUT_LEFT_BUTTON:
            # ノット数を増やせばいくらでも制御点を追加できるが、今回はノットベクトルが固定されているので
            # いくらでも追加できるわけではない
            if len(g_ControlPoints) < len(g_NotVector) - 4:
                g_ControlPoints.append(np.array([x, y]))

        # 右ボタンだったら末尾の制御点を削除
        if button == GLUT_RIGHT_BUTTON:
            if g_ControlPoints:
                g_ControlPoints.pop()
    glutPostRedisplay()


# キーが押されたときのイベント処理
def keyboard(key, x, y):
    if key == b"q":
        pass
    elif key == b"Q":
        pass
    elif key == b"\x1b":
        exit()  # b'\x1b'は ESC の ASCII コード

    glutPostRedisplay()


def init():
    # アンチエイリアスを有効にする
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)


if __name__ == "__main__":
    glutInit(sys.argv)  # ライブラリの初期化
    glutInitWindowSize(g_WindowWidth, g_WindowHeight)  # ウィンドウサイズを指定
    glutCreateWindow(sys.argv[0])  # ウィンドウを作成
    glutDisplayFunc(display)  # 表示関数を指定
    glutReshapeFunc(resize)  # ウィンドウサイズが変更されたときの関数を指定
    glutMouseFunc(mouse)  # マウス関数を指定
    glutKeyboardFunc(keyboard)  # キーボード関数を指定
    init()  # 初期設定を行う
    glutMainLoop()  # イベント待ち
