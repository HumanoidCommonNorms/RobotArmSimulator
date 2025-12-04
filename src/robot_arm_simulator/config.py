"""
ロボットアーム 設定ファイル
各パラメータをここで一元管理
"""

import numpy as np


class RobotConfig:
    """ロボットアームの設定クラス"""
    # End-Effector 目標位置 [mm]
    TARGET_POINT_X = 0
    TARGET_POINT_Y = 50
    TARGET_POINT_Z = 0

    # リンク長設定 [mm]
    LINK1_LENGTH = 100
    LINK2_LENGTH = 80
    LINK3_LENGTH = 20

    # 第1軸(根元回転: Z軸周り)の角度制限 [度]
    THETA1_MIN_DEG = -180
    THETA1_MAX_DEG = 180

    # 第2軸(根元モーター: Y軸周り)の角度制限 [度]
    THETA2_MIN_DEG = -90
    THETA2_MAX_DEG = 180

    # 第3軸(関節モーター: Y軸周り)の角度制限 [度]
    THETA3_MIN_DEG = 0
    THETA3_MAX_DEG = 180

    # 第4軸(Link3の角度: Y軸周り)の角度制限 [度]
    THETA4_MIN_DEG = -90
    THETA4_MAX_DEG = 90

    # アームの色設定 (RGB or 色名)
    LINK1_COLOR = 'blue'        # 第1リンクの色
    LINK2_COLOR = 'green'       # 第2リンクの色
    LINK3_COLOR = 'orange'      # 第3リンクの色
    BASE_COLOR = 'red'          # 基点の色
    END_EFFECTOR_COLOR = 'purple'  # 手先の色

    @classmethod
    def get_theta1_range_rad(cls):
        """第1軸の角度範囲をラジアンで取得"""
        return np.radians(cls.THETA1_MIN_DEG), np.radians(cls.THETA1_MAX_DEG)

    @classmethod
    def get_theta2_range_rad(cls):
        """第2軸の角度範囲をラジアンで取得"""
        return np.radians(cls.THETA2_MIN_DEG), np.radians(cls.THETA2_MAX_DEG)

    @classmethod
    def get_theta3_range_rad(cls):
        """第3軸の角度範囲をラジアンで取得"""
        return np.radians(cls.THETA3_MIN_DEG), np.radians(cls.THETA3_MAX_DEG)

    @classmethod
    def get_theta4_range_rad(cls):
        """第4軸の角度範囲をラジアンで取得"""
        return np.radians(cls.THETA4_MIN_DEG), np.radians(cls.THETA4_MAX_DEG)

    @classmethod
    def get_link_lengths(cls):
        """リンク長のタプルを取得"""
        return (cls.LINK1_LENGTH, cls.LINK2_LENGTH, cls.LINK3_LENGTH)

    @classmethod
    def get_max_reach(cls):
        """最大到達距離を計算"""
        return cls.LINK1_LENGTH + cls.LINK2_LENGTH + cls.LINK3_LENGTH
