# /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filename: __main__.py
Author: TAILWAY
Date: 2025-02-20
Version: 1.0
Description: 主な処理の活用サンプル
License: MIT License
Contact: TAILWAY
"""

import argparse
import sys
import time
import logging
import robot_arm_simulator.robot_plot as RS
from robot_arm_simulator.__init__ import __version__

parser = argparse.ArgumentParser(
    prog='robotarm_simulator',
    add_help=True,
    description="ロボットアームシミュレータ"
)

parser.add_argument('--version', action='version',
                    version='%(prog)s : ' + __version__)
parser.add_argument('-x', type=int, help='X軸座標, デフォルト: 0', default=0)
parser.add_argument('-y', type=int, help='Y軸座標, デフォルト: 0', default=0)
parser.add_argument('-z', type=int, help='Z軸座標, デフォルト: 0', default=0)
parser.add_argument('--link_len1', '-l1', type=int,
                    help='リンク1の長さ, デフォルト: 100', default=100)
parser.add_argument('--link_len2', '-l2', type=int,
                    help='リンク2の長さ, デフォルト: 80', default=80)
parser.add_argument('--link_len3', '-l3', type=int,
                    help='リンク3の長さ, デフォルト: 20', default=20)

if __name__ == "__main__":
    result = 0
    _detail_formatting = "[%(levelname)s] %(asctime)s\t%(message)s"
    vi = None
    try:
        # ロギングの設定
        logging.basicConfig(level=logging.INFO, format=_detail_formatting)
        logger = logging.getLogger(parser.prog)
        # 引数の解析
        args = parser.parse_args()
        RS.RobotConfig.TARGET_POINT_X = args.x
        RS.RobotConfig.TARGET_POINT_Y = args.y
        RS.RobotConfig.TARGET_POINT_Z = args.z
        RS.RobotConfig.LINK1_LENGTH = args.link_len1
        RS.RobotConfig.LINK2_LENGTH = args.link_len2
        RS.RobotConfig.LINK3_LENGTH = args.link_len3
        # ロボットアームシミュレータ情報の表示
        logger.info("# robot_arm_simulator")
        logger.info("Link Lengths: ( "
                    f"{RS.RobotConfig.LINK1_LENGTH} / "
                    f"{RS.RobotConfig.LINK2_LENGTH} / "
                    f"{RS.RobotConfig.LINK3_LENGTH})")
        logger.info("Target Point: ( "
                    f"{RS.RobotConfig.TARGET_POINT_X}, "
                    f"{RS.RobotConfig.TARGET_POINT_Y}, "
                    f"{RS.RobotConfig.TARGET_POINT_Z})")

        # ロボットの作成(設定ファイルのパラメータを使用)
        robot = RS.ThreeAxisRobot(
            RS.RobotConfig.LINK1_LENGTH,
            RS.RobotConfig.LINK2_LENGTH,
            RS.RobotConfig.LINK3_LENGTH)

        # シミュレータの作成
        simulator = RS.RobotSimulator(robot)

        # 逆運動学による計算
        inverse_kinematics_result = RS.inverse_kinematics(
            RS.RobotConfig.TARGET_POINT_X,
            RS.RobotConfig.TARGET_POINT_Y,
            RS.RobotConfig.TARGET_POINT_Z,
            RS.RobotConfig.LINK1_LENGTH,
            RS.RobotConfig.LINK2_LENGTH + RS.RobotConfig.LINK3_LENGTH
        )
        # インタラクティブ制御の開始
        simulator.interactive_control(inverse_kinematics_result[0],
                                      inverse_kinematics_result[1],
                                      inverse_kinematics_result[2],
                                      0.0)
    except KeyboardInterrupt:
        logger.error("\nExiting by user request.")
        result = 0
    except Exception as e:
        import traceback
        traceback.print_exc()
        result = 1
    finally:
        if vi is not None:
            vi.closing()
        time.sleep(1)
        sys.exit(result)
