#!/usr/bin/env python
import numpy as np
from config import RobotConfig

# ロボットアームの各関節角度を計算する逆運動学の例

# アームのリンク長さ（単位: mm）
L1 = RobotConfig.LINK1_LENGTH
L2 = RobotConfig.LINK2_LENGTH + RobotConfig.LINK3_LENGTH

# 目標位置 (単位: mm)
dx = RobotConfig.TARGET_POINT_X
dy = RobotConfig.TARGET_POINT_Y
dz = RobotConfig.TARGET_POINT_Z

# XY平面上の距離
dxy = np.sqrt(dx*dx + dy*dy)

# 目標位置までの3D距離
pow_reach = dx*dx + dy*dy + dz*dz
arm_reach = np.sqrt(pow_reach)

# ベース回転角（Z軸周り）
theta0 = np.arctan2(dy, dx)

# 余弦定理で肘関節の角度を計算
cos_theta1 = (L1*L1 + L2*L2 - pow_reach) / (2*L1*L2)
# 範囲チェック
if arm_reach > (L1+L2):
    print("[ERROR] Target is out of reach! Len:", arm_reach)
elif abs(cos_theta1) > 1.0:
    print("[ERROR] Target is out of reach! angle:", cos_theta1)
else:
    theta2 = np.pi - np.arccos(cos_theta1)

    # 角度計算
    alpha = np.arctan2(dz, dxy)
    beta = np.arccos((L1 + L2*np.cos(theta2)) / arm_reach)
    theta1 = np.pi/2 - (alpha + beta)

    print("  theta0 = ", np.degrees(theta0))
    print("  theta1 = ", np.degrees(theta1))
    print("  theta2 = ", np.degrees(theta2))
