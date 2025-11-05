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


def bezier_derivatives(control_points, t):
    if len(control_points) != 4:
        return None, None, None

    p0, p1, p2, p3 = control_points

    # 点 (B(t))
    B_x = (
        (1 - t) ** 3 * p0[0]
        + 3 * (1 - t) ** 2 * t * p1[0]
        + 3 * (1 - t) * t**2 * p2[0]
        + t**3 * p3[0]
    )
    B_y = (
        (1 - t) ** 3 * p0[1]
        + 3 * (1 - t) ** 2 * t * p1[1]
        + 3 * (1 - t) * t**2 * p2[1]
        + t**3 * p3[1]
    )
    B = np.array([B_x, B_y])

    # 1次導関数 (B'(t))
    B_prime_x = (
        3 * (1 - t) ** 2 * (p1[0] - p0[0])
        + 6 * (1 - t) * t * (p2[0] - p1[0])
        + 3 * t**2 * (p3[0] - p2[0])
    )
    B_prime_y = (
        3 * (1 - t) ** 2 * (p1[1] - p0[1])
        + 6 * (1 - t) * t * (p2[1] - p1[1])
        + 3 * t**2 * (p3[1] - p2[1])
    )
    B_prime = np.array([B_prime_x, B_prime_y])

    # 2次導関数 (B''(t))
    B_double_prime_x = 6 * (1 - t) * (p2[0] - 2 * p1[0] + p0[0]) + 6 * t * (
        p3[0] - 2 * p2[0] + p1[0]
    )
    B_double_prime_y = 6 * (1 - t) * (p2[1] - 2 * p1[1] + p0[1]) + 6 * t * (
        p3[1] - 2 * p2[1] + p1[1]
    )
    B_double_prime = np.array([B_double_prime_x, B_double_prime_y])

    return B, B_prime, B_double_prime


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

    # ベジェ曲線の描画
    num_curves = (len(g_ControlPoints) - 1) // 3
    for i in range(num_curves):
        start_index = i * 3
        control_points = g_ControlPoints[start_index : start_index + 4]
        if len(control_points) == 4:
            # 曲線の描画
            glColor3d(0.0, 0.0, 0.0)
            glLineWidth(2)
            glBegin(GL_LINE_STRIP)
            for j in range(101):
                t = j / 100.0
                point, _, _ = bezier_derivatives(control_points, t)
                if point is not None:
                    glVertex2dv(point)
            glEnd()

            # 法線の描画
            glColor3d(0.0, 0.0, 1.0)  # 法線は青色
            glLineWidth(1)
            for j in range(0, 101, 1):  # 曲線ごとに11個の法線を描画
                t = j / 100.0
                point, tangent, second_derivative = bezier_derivatives(
                    control_points, t
                )
                if (
                    point is not None
                    and tangent is not None
                    and second_derivative is not None
                ):
                    tangent_norm_sq = tangent[0] ** 2 + tangent[1] ** 2
                    if tangent_norm_sq > 1e-6:
                        # 曲率の計算
                        curvature_numerator = (
                            tangent[0] * second_derivative[1]
                            - tangent[1] * second_derivative[0]
                        )
                        curvature = curvature_numerator / (tangent_norm_sq**1.5)

                        # 法線ベクトル
                        normal = np.array([-tangent[1], tangent[0]])
                        normal_norm = np.linalg.norm(normal)
                        if normal_norm > 1e-6:
                            normal /= normal_norm

                        # 曲率に応じて法線の長さを変更
                        normal_length = 5000.0 * abs(curvature)  # スケールファクタ

                        p2 = point + normal * normal_length

                        glBegin(GL_LINES)
                        glVertex2dv(point)
                        glVertex2dv(p2)
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
