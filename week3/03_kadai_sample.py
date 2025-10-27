import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random


# ティーポットデータのクラスの定義
class TeapotData:
    def __init__(self):
        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.shininess = None
        self.angle = None


# グローバル変数（プログラム中のどこからでもアクセスできる変数）には g_ を付けている
g_NumTeapots = 8
g_Teapots = [TeapotData() for i in range(g_NumTeapots)]

# float型の値は、数字の後ろにfを付ける。末尾のゼロは省略できる
g_TeapotSize = 1.0
g_InnerRadius = 6.0
g_OuterRadius = 7.5
g_HeightAmplitude = 0.8
g_HeightOffset = 0.2

g_EyeCenterX = 0.0
g_EyeCenterY = 9.0
g_EyeCenterZ = 30.0
g_EyeRadius = 8.0
g_EyeX = 0.0
g_EyeY = g_EyeCenterY
g_EyeZ = g_EyeCenterZ

g_AnimationIntervalMsec = 10

g_RotationDegree = 0.0
g_DeltaRotationDegree = 0.3

g_WindowWidth = 512
g_WindowHeight = 512


# 円筒を描画…引数は円の半径、高さ、円の分割数
# glutには円筒を描画するための関数が無いので、独自に準備
def displayCylinder(radius, height, nSlices):
    # 天頂面
    deltaTheta = 2 * math.pi / float(nSlices)

    glNormal3f(0, 1, 0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, height, 0)
    for i in range(nSlices + 1):
        theta = deltaTheta * i
        glVertex3f(radius * math.cos(theta), height, radius * math.sin(theta))
    glEnd()

    # 底面
    glNormal3f(0, -1, 0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(nSlices + 1):
        theta = deltaTheta * i
        glVertex3f(radius * math.cos(theta), 0, radius * math.sin(theta))
    glEnd()

    # 側面
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(nSlices + 1):
        theta = deltaTheta * i
        cosTheta = math.cos(theta)
        sinTheta = math.sin(theta)
        glNormal3f(cosTheta, 0, sinTheta)
        glVertex3f(radius * cosTheta, height, radius * sinTheta)
        glVertex3f(radius * cosTheta, 0, radius * sinTheta)
    glEnd()


# 表示部分をこの関数で記入
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 透視投影変換の設定
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, g_WindowWidth / float(g_WindowHeight), 1, 100.0)

    # モデル座標の操作へモード切り替え
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(g_EyeX, g_EyeY, g_EyeZ, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    ambientColor = [0.4, 0.2, 0.2, 1.0]
    diffuseColor = [1.0, 0.8, 0.8, 1.0]
    specularColor = [0.4, 0.3, 0.3, 1.0]
    shininess = 5.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambientColor)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuseColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess)

    glPushMatrix()
    glRotatef(g_RotationDegree, 0, 1, 0)

    # 屋根
    glPushMatrix()
    glTranslatef(0, g_HeightAmplitude + g_HeightOffset + 3.0, 0)
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(g_OuterRadius, 2.0, 32, 32)
    glPopMatrix()

    # 中心の柱
    glPushMatrix()
    glTranslatef(0, -1.0, 0)
    displayCylinder(0.5, g_HeightAmplitude + g_HeightOffset + 6.5, 32)
    glPopMatrix()

    # 土台
    glPushMatrix()
    glTranslatef(0, -2.0, 0)
    displayCylinder(g_OuterRadius, 0.7, 64)
    glPopMatrix()

    # 屋根の上のティーポット
    glPushMatrix()
    glTranslatef(0, g_HeightAmplitude + g_HeightOffset + 5.5, 0)
    glRotatef(g_RotationDegree, 0, 1, 0)  # 回転させている
    glutSolidTeapot(g_TeapotSize)
    glPopMatrix()

    deltaTheta = 360 / float(g_NumTeapots)

    # ティーポットと柱を1つずつ描画する
    "★下記のコードでは、常に同じ位置に描画されるので、全体が回転するように変更する"
    for i in range(g_NumTeapots):
        "★ティーポットの位置を決めるための角度。この角度を変化させることでティーポットが回転する。"
        thetaDegree = deltaTheta * i

        thetaRad = thetaDegree * math.pi / 180.0
        xPos = g_InnerRadius * math.sin(thetaRad)
        zPos = g_InnerRadius * math.cos(thetaRad)

        # ティーポットの高さ方向の値
        "★この値を少しずつ変化させることでティーポットが上下に移動する"
        bobbingAngle = math.radians(g_RotationDegree * 2.0 + thetaDegree)
        yPos = g_HeightOffset + g_HeightAmplitude * math.sin(bobbingAngle * 2)

        # ティーポットの色の指定
        glMaterialfv(GL_FRONT, GL_AMBIENT, g_Teapots[i].ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, g_Teapots[i].diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, g_Teapots[i].specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, g_Teapots[i].shininess)

        # ティーポットの描画
        glPushMatrix()
        glTranslatef(xPos, yPos, zPos)
        glRotatef(thetaDegree, 0, 1, 0)
        glRotatef(g_Teapots[i].angle, 0, 0, 1)
        glutSolidTeapot(1.2 * g_TeapotSize)
        glPopMatrix()

        # ティーポットを支える柱の色の指定
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambientColor)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuseColor)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, shininess)

        # ティーポットを支える柱の描画
        glPushMatrix()
        glTranslatef(xPos, -1.0, zPos)
        displayCylinder(0.3, yPos + 1.0, 32)
        glPopMatrix()

    glPopMatrix()

    glutSwapBuffers()  # バッファの入れ替え


# 一定時間ごとに呼び出される関数
def timer(value):
    global g_EyeX, g_EyeY, g_EyeZ
    # 回転角度の更新
    global g_RotationDegree
    g_RotationDegree += g_DeltaRotationDegree
    if g_RotationDegree >= 360.0:
        g_RotationDegree -= 360.0

    orbitAngle = math.radians(g_RotationDegree * 1)
    verticalAngle = math.radians(g_RotationDegree * 1.2)

    g_EyeX = g_EyeCenterX + g_EyeRadius * math.sin(orbitAngle)
    g_EyeZ = g_EyeCenterZ + g_EyeRadius * math.cos(orbitAngle)
    g_EyeY = g_EyeCenterY + 2.0 * math.sin(verticalAngle)

    glutPostRedisplay()

    glutTimerFunc(g_AnimationIntervalMsec, timer, value)


# ウィンドウサイズが変更されたときの処理
def reshape(w, h):
    if h > 0:
        # ビューポートをウィンドウサイズに変更
        glViewport(0, 0, w, h)
        global g_WindowWidth, g_WindowHeight
        g_WindowWidth = w
        g_WindowHeight = h


# 初期設定を行う関数
def init():
    glClearColor(1, 1, 1, 1)
    glClearDepth(100.0)

    lightAmbientColor0 = [0.2, 0.2, 0.2, 0.0]
    lightDiffuseColor0 = [0.4, 0.4, 0.4, 0.0]
    lightSpecularColor0 = [0.8, 0.8, 0.8, 0.0]
    lightPosition0 = [5.0, 5.0, 8.0, 0.0]

    lightAmbientColor1 = [0.2, 0.2, 0.2, 0.0]
    lightDiffuseColor1 = [0.4, 0.4, 0.4, 0.0]
    lightSpecularColor1 = [0.8, 0.8, 0.8, 0.0]
    lightPosition1 = [-5.0, 2.0, 3.0, 0.0]

    glEnable(GL_LIGHTING)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbientColor0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuseColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecularColor0)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition0)

    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, lightAmbientColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightDiffuseColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightSpecularColor1)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPosition1)

    random.seed(1)

    # 個々のティーポットの色を設定する処理 乱数で決めている
    for i in range(g_NumTeapots):
        g_Teapots[i].ambient = [
            0.2 * random.random(),
            0.2 * random.random(),
            0.2 * random.random(),
            1.0,
        ]
        g_Teapots[i].diffuse = [
            0.2 * random.random() + 0.8,
            0.2 * random.random() + 0.8,
            0.2 * random.random() + 0.8,
            1.0,
        ]
        g_Teapots[i].specular = [
            0.3 * random.random() + 0.2,
            0.3 * random.random() + 0.2,
            0.3 * random.random() + 0.2,
            1.0,
        ]
        g_Teapots[i].shininess = 2.0 + 30 * random.random()
        g_Teapots[i].angle = 15 * (2.0 * random.random() - 1.0)

    glEnable(GL_DEPTH_TEST)


if __name__ == "__main__":
    glutInit(sys.argv)  # ライブラリの初期化
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(g_WindowWidth, g_WindowHeight)  # ウィンドウサイズを指定
    glutCreateWindow(
        "Teapot Merry-Go-Round"
    )  # ウィンドウタイトルに表示する文字列を指定する場合
    glutDisplayFunc(display)  # 表示関数を指定
    glutReshapeFunc(reshape)  # ウィンドウサイズが変更されたときに実行される関数を指定
    timer(0)  # timer関数の実行
    init()  # 初期設定を行う
    glutMainLoop()  # イベント待ち
