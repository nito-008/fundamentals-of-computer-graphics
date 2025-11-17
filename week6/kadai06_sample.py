import numpy as np
import math

# 出力ファイル名
OUTPUT_FILENAME = "parametric_surface.obj"

# 定数
NUM_U = 50  # U方向の分割数
NUM_V = 50  # V方向の分割数

# 配列をnumpyで定義 (x, y, z座標)
x = np.zeros((NUM_U + 1, NUM_V + 1))
y = np.zeros((NUM_U + 1, NUM_V + 1))
z = np.zeros((NUM_U + 1, NUM_V + 1))


# u,v の値から3次元座標を返す関数
def function(u, v):
    # 平面の場合
    # x = u * 100
    # y = v * 100
    # z = 0

    # 波紋
    # x = u * 100
    # y = v * 100
    # z = math.sin(8 * math.pi * math.sqrt((u) ** 2 + (v - 0.5) ** 2)) / 10 * 100

    # ガウス関数
    # x = u * 100
    # y = v * 100
    # z = math.exp(-((u - 0.5) ** 2 + (v - 0.5) ** 2) / 0.1) / 2 * 100

    # 球
    x = math.cos(u * math.pi * 2) * math.cos((v * 2 - 1) * math.pi / 2)
    y = math.sin(u * math.pi * 2) * math.cos((v * 2 - 1) * math.pi / 2)
    z = math.sin((v * 2 - 1) * math.pi / 2)

    return x, y, z


# 配列に座標値を設定する
def setCoordinates():
    for i in range(NUM_U + 1):
        for j in range(NUM_V + 1):
            # u と v の値を 0.0 ～ 1.0 に正規化する
            u = 1.0 / NUM_U * i
            v = 1.0 / NUM_V * j

            # 座標値の設定
            x[i][j], y[i][j], z[i][j] = function(u, v)


# OBJ 形式でのファイル出力
def exportOBJ():
    try:
        # ファイルを開く
        with open(OUTPUT_FILENAME, "w") as fout:
            # 頂点情報の出力
            for i in range(NUM_U + 1):
                for j in range(NUM_V + 1):
                    # 各頂点の座標値を出力する
                    fout.write(f"v {x[i][j]} {y[i][j]} {z[i][j]}\n")

            # 面情報の出力
            ###
            # 課題：以下の部分を完成させて、面情報を出力するようにする
            ###
            for i in range(NUM_U):
                for j in range(NUM_V):
                    # OBJ形式では頂点番号は1から始まる
                    lb_index = i * (NUM_U + 1) + j + 2  # 左下の頂点番号
                    lt_index = i * (NUM_U + 1) + j + 1  # 左上の頂点番号
                    rb_index = (i + 1) * (NUM_U + 1) + j + 2  # 右下の頂点番号
                    rt_index = (i + 1) * (NUM_U + 1) + j + 1  # 右上の頂点番号

                    # 三角形を構成する頂点番号を出力
                    fout.write(f"f {lb_index} {rt_index} {lt_index}\n")
                    fout.write(f"f {lb_index} {rb_index} {rt_index}\n")

    except IOError as e:
        print(f"Error: {e}")
        exit(0)


# メイン処理
if __name__ == "__main__":
    setCoordinates()
    exportOBJ()
