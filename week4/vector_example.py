import numpy as np

# 2次元ベクトルの定義
p = np.array([1, 2])
q = np.array([3, 4])

# (例) ベクトルp と ベクトルq を出力する
print("p:", p)
print("q:", q)

# (1) p + q で表されるベクトルを出力する
print("p + q:", p + q)

# (2) -p で表されるベクトルを出力する
print("-p:", -p)

# (3) p - q で表されるベクトルを出力する
print("p - q:", p - q)

# (4) 3p + 2q で表されるベクトルを出力する
print("3p + 2q:", 3 * p + 2 * q)

# (5) p と q の内積を出力する
print("p ・ q:", np.dot(p, q))

# (6) p の大きさ（ノルム）を出力する
p_norm = np.linalg.norm(p)
print("p norm:", p_norm)

# (7) p を正規化したベクトルを出力する
print("p normalized:", p / p_norm)

# (8) p を90度回転させたベクトルを出力する
# ヒント： (x, y) で表されるベクトルを90度回転させると (-y, x) となる
print("p rotated 90 degree:", np.array([-p[1], p[0]]))
