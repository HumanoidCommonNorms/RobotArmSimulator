"""
ロボットアーム シミュレータ
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from robot_arm_simulator.config import RobotConfig

# 日本語フォントの設定
# plt.rcParams['font.family'] = 'MS Gothic'  # Windowsの場合
# plt.rcParams['font.family'] = 'Yu Gothic'  # 游ゴシック
plt.rcParams['font.family'] = 'Meiryo'     # メイリオ
# plt.rcParams['font.family'] = 'DejaVu Sans'  # 他のOSの場合


class ThreeAxisRobot:
    """
    3軸ロボットアームクラス

    パラメータ:
        link1_length: 第1リンク長 [mm] (省略時は設定ファイルから取得)
        link2_length: 第2リンク長 [mm] (省略時は設定ファイルから取得)
        link3_length: 第3リンク長 [mm] (省略時は設定ファイルから取得)
    """

    def __init__(self, link1_length=None, link2_length=None, link3_length=None):
        """コンストラクタ"""
        # 設定ファイルから値を取得(引数が指定されていない場合)
        if link1_length is None:
            link1_length = RobotConfig.LINK1_LENGTH
        if link2_length is None:
            link2_length = RobotConfig.LINK2_LENGTH
        if link3_length is None:
            link3_length = RobotConfig.LINK3_LENGTH

        self.link1 = link1_length
        self.link2 = link2_length
        self.link3 = link3_length

        # 角度制限を設定ファイルから取得 [rad]
        self.theta1_min, self.theta1_max = RobotConfig.get_theta1_range_rad()
        self.theta2_min, self.theta2_max = RobotConfig.get_theta2_range_rad()
        self.theta3_min, self.theta3_max = RobotConfig.get_theta3_range_rad()
        self.theta4_min, self.theta4_max = RobotConfig.get_theta4_range_rad()

    def forward_kinematics(self, theta1, theta2, theta3, theta4=0):
        """
        順運動学: 関節角度から各リンクの端点位置を計算

        パラメータ:
            theta1: 根元回転角度 [rad] (Z軸周り)
            theta2: 根元モーター角度 [rad] (Y軸周り)
            theta3: 関節モーター角度 [rad] (Y軸周り)
            theta4: Link3の角度 [rad] (Y軸周り)

        戻り値:
            positions: リンクの端点位置のリスト [(x, y, z), ...]
        """
        # 角度制限のチェック
        theta1 = np.clip(theta1, self.theta1_min, self.theta1_max)
        theta2 = np.clip(theta2, self.theta2_min, self.theta2_max)
        theta3 = np.clip(theta3, self.theta3_min, self.theta3_max)
        theta4 = np.clip(theta4, self.theta4_min, self.theta4_max)

        # 基点(原点)
        p0 = np.array([0, 0, 0])

        # 第1関節(Z軸回転のみ、高さ方向には動かない)
        # この時点では回転のみで、リンクはまだ伸びていない
        p1 = np.array([0, 0, 0])

        # 第2関節(Z軸回転 + Y軸回転後のリンク1端点)
        # Z軸回転とY軸回転の組み合わせ
        x1 = self.link1 * np.sin(theta2) * np.cos(theta1)
        y1 = self.link1 * np.sin(theta2) * np.sin(theta1)
        z1 = self.link1 * np.cos(theta2)
        p2 = np.array([x1, y1, z1])

        # 第3関節(リンク2端点)
        # theta2 + theta3 の合成角度でリンク2が伸びる
        total_angle2 = theta2 + theta3
        x2 = x1 + self.link2 * np.sin(total_angle2) * np.cos(theta1)
        y2 = y1 + self.link2 * np.sin(total_angle2) * np.sin(theta1)
        z2 = z1 + self.link2 * np.cos(total_angle2)
        p3 = np.array([x2, y2, z2])

        # 手先(リンク3端点) - theta4で独立して動く
        total_angle3 = theta2 + theta3 + theta4
        x3 = x2 + self.link3 * np.sin(total_angle3) * np.cos(theta1)
        y3 = y2 + self.link3 * np.sin(total_angle3) * np.sin(theta1)
        z3 = z2 + self.link3 * np.cos(total_angle3)
        p4 = np.array([x3, y3, z3])

        return [p0, p1, p2, p3, p4]

    def plot_robot(self, theta1, theta2, theta3, theta4=0, ax=None):
        """
        ロボットアームを3D描画

        パラメータ:
            theta1: 根元回転角度 [rad]
            theta2: 根元モーター角度 [rad]
            theta3: 関節モーター角度 [rad]
            theta4: Link3の角度 [rad]
            ax: matplotlib 3D軸(省略時は新規作成)

        戻り値:
            ax: 3D軸オブジェクト
        """
        if ax is None:
            fig = plt.figure(figsize=(10, 10))
            fig.canvas.manager.set_window_title('Robot Arm Simulator')
            ax = fig.add_subplot(111, projection='3d')

        # 順運動学で位置を計算
        positions = self.forward_kinematics(theta1, theta2, theta3, theta4)

        # リンクの色設定
        link_colors = [RobotConfig.LINK1_COLOR,
                       RobotConfig.LINK2_COLOR,
                       RobotConfig.LINK3_COLOR]
        link_labels = ['Link 1 [len:' + str(RobotConfig.LINK1_LENGTH) + ' mm]',
                       'Link 2 [len:' + str(RobotConfig.LINK2_LENGTH) + ' mm]',
                       'Link 3 [len:' + str(RobotConfig.LINK3_LENGTH) + ' mm]']

        # リンクを描画
        for i in range(len(positions) - 1):
            if i == 0:
                # 基点から第1関節(実際は同じ位置)
                continue
            xs = [positions[i][0], positions[i+1][0]]
            ys = [positions[i][1], positions[i+1][1]]
            zs = [positions[i][2], positions[i+1][2]]
            color = link_colors[i-1] if i-1 < len(link_colors) else 'blue'
            label = link_labels[i-1] if i-1 < len(link_labels) else None
            ax.plot(xs, ys, zs, '-', color=color, linewidth=3,
                    marker='o', markersize=8, label=label)

        # 基点を描画
        ax.scatter([0], [0], [0], color=RobotConfig.BASE_COLOR,
                   s=100, label='Base')

        # 手先位置を描画
        end_pos = positions[-1]
        ax.scatter([end_pos[0]], [end_pos[1]], [end_pos[2]],
                   color=RobotConfig.END_EFFECTOR_COLOR, s=100,
                   label='End Effector')

        # 軸の設定
        max_reach = self.link1 + self.link2 + self.link3
        ax.set_xlim([-max_reach, max_reach])
        ax.set_ylim([-max_reach, max_reach])
        ax.set_zlim([0, max_reach])

        ax.set_xlabel('X [mm]')
        ax.set_ylabel('Y [mm]')
        ax.set_zlabel('Z [mm]')
        ax.set_title(
            f'Robot Arm\n' +
            f'θ1={np.degrees(theta1):.1f}°, θ2={np.degrees(theta2):.1f}°, ' +
            f'θ3={np.degrees(theta3):.1f}°, θ4={np.degrees(theta4):.1f}°\n' +
            f'End Effector: ' +
            f'({end_pos[0]:.3f}, {end_pos[1]:.3f}, {end_pos[2]:.3f})')
        ax.legend(loc='upper left', bbox_to_anchor=(1.15, 1), borderaxespad=0)

        return ax


class RobotSimulator:
    """
    ロボットアームシミュレータ(アニメーション機能付き)
    """

    def __init__(self, robot):
        """
        コンストラクタ

        パラメータ:
            robot: ThreeAxisRobotインスタンス
        """
        self.robot = robot
        self.fig = None
        self.ax = None
        self.animation = None

    def animate_trajectory(self, trajectory, interval=50, save_path=None):
        """
        軌道をアニメーション表示

        パラメータ:
            trajectory: [(theta1, theta2, theta3), ...] の軌道リスト
            interval: フレーム間隔 [ms]
            save_path: 保存先パス(省略時は表示のみ)
        """
        self.fig = plt.figure(figsize=(10, 10))
        self.fig.canvas.manager.set_window_title('Robot Arm Simulator')
        self.ax = self.fig.add_subplot(111, projection='3d')

        def update(frame):
            """アニメーション更新関数"""
            self.ax.clear()
            if len(trajectory[frame]) == 4:
                theta1, theta2, theta3, theta4 = trajectory[frame]
            else:
                theta1, theta2, theta3 = trajectory[frame]
                theta4 = 0
            self.robot.plot_robot(theta1, theta2, theta3, theta4, self.ax)
            return self.ax,

        self.animation = FuncAnimation(
            self.fig, update, frames=len(trajectory),
            interval=interval, blit=False, repeat=True
        )

        if save_path:
            self.animation.save(save_path, writer='pillow', fps=20)
            print(f"Animation saved to: {save_path}")
        else:
            plt.show()

    def interactive_control(self,
                            init_theta1=0.0, init_theta2=0.0,
                            init_theta3=0.0, init_theta4=0.0):
        """
        インタラクティブな角度制御
        スライダーで各関節の角度を調整
        """
        from matplotlib.widgets import Slider, TextBox, Button

        # 図の作成
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.canvas.manager.set_window_title('Robot Arm Simulator')
        self.ax = self.fig.add_subplot(111, projection='3d')
        plt.subplots_adjust(left=0.1, right=0.85, bottom=0.30, top=0.88)

        # 初期状態を描画
        self.robot.plot_robot(init_theta1, init_theta2,
                              init_theta3, init_theta4, self.ax)

        # スライダーとテキストボックスの作成
        slider_width = 0.55
        slider_left = 0.15
        textbox_left = slider_left + slider_width + 0.07
        textbox_width = 0.08

        # θ1用
        ax_theta1 = plt.axes([slider_left, 0.18, slider_width, 0.03])
        ax_text1 = plt.axes([textbox_left, 0.18, textbox_width, 0.03])

        # θ2用
        ax_theta2 = plt.axes([slider_left, 0.13, slider_width, 0.03])
        ax_text2 = plt.axes([textbox_left, 0.13, textbox_width, 0.03])

        # θ3用
        ax_theta3 = plt.axes([slider_left, 0.08, slider_width, 0.03])
        ax_text3 = plt.axes([textbox_left, 0.08, textbox_width, 0.03])

        # θ4用
        ax_theta4 = plt.axes([slider_left, 0.03, slider_width, 0.03])
        ax_text4 = plt.axes([textbox_left, 0.03, textbox_width, 0.03])

        # リセットボタン用
        ax_reset = plt.axes(
            [textbox_left + textbox_width + 0.02, 0.18, 0.08, 0.03])

        slider_theta1 = Slider(ax_theta1, 'Base 回転',
                               RobotConfig.THETA1_MIN_DEG,
                               RobotConfig.THETA1_MAX_DEG,
                               valinit=np.degrees(init_theta1),
                               valstep=0.001)
        slider_theta2 = Slider(ax_theta2, 'Base',
                               RobotConfig.THETA2_MIN_DEG,
                               RobotConfig.THETA2_MAX_DEG,
                               valinit=np.degrees(init_theta2),
                               valstep=0.001)
        slider_theta3 = Slider(ax_theta3, 'リンク_1',
                               RobotConfig.THETA3_MIN_DEG,
                               RobotConfig.THETA3_MAX_DEG,
                               valinit=np.degrees(init_theta3),
                               valstep=0.001)
        slider_theta4 = Slider(ax_theta4, 'リンク_2',
                               RobotConfig.THETA4_MIN_DEG,
                               RobotConfig.THETA4_MAX_DEG,
                               valinit=np.degrees(init_theta4),
                               valstep=0.001)

        text_theta1 = TextBox(
            ax_text1, '', initial=f'{np.degrees(init_theta1):.3f}')
        text_theta2 = TextBox(
            ax_text2, '', initial=f'{np.degrees(init_theta2):.3f}')
        text_theta3 = TextBox(
            ax_text3, '', initial=f'{np.degrees(init_theta3):.3f}')
        text_theta4 = TextBox(
            ax_text4, '', initial=f'{np.degrees(init_theta4):.3f}')

        # リセットボタン
        reset_button = Button(ax_reset, 'リセット')

        def update(val):
            """スライダー更新時の処理"""
            self.ax.clear()
            theta1 = np.radians(slider_theta1.val)
            theta2 = np.radians(slider_theta2.val)
            theta3 = np.radians(slider_theta3.val)
            theta4 = np.radians(slider_theta4.val)
            self.robot.plot_robot(theta1, theta2, theta3, theta4, self.ax)

            # テキストボックスも更新
            text_theta1.set_val(f'{slider_theta1.val:.3f}')
            text_theta2.set_val(f'{slider_theta2.val:.3f}')
            text_theta3.set_val(f'{slider_theta3.val:.3f}')
            text_theta4.set_val(f'{slider_theta4.val:.3f}')

            self.fig.canvas.draw_idle()

        def update_from_text1(text):
            """テキストボックス1からの更新"""
            try:
                val = float(text)
                val = np.clip(val, RobotConfig.THETA1_MIN_DEG,
                              RobotConfig.THETA1_MAX_DEG)
                slider_theta1.set_val(val)
            except ValueError:
                pass

        def update_from_text2(text):
            """テキストボックス2からの更新"""
            try:
                val = float(text)
                val = np.clip(val, RobotConfig.THETA2_MIN_DEG,
                              RobotConfig.THETA2_MAX_DEG)
                slider_theta2.set_val(val)
            except ValueError:
                pass

        def update_from_text3(text):
            """テキストボックス3からの更新"""
            try:
                val = float(text)
                val = np.clip(val, RobotConfig.THETA3_MIN_DEG,
                              RobotConfig.THETA3_MAX_DEG)
                slider_theta3.set_val(val)
            except ValueError:
                pass

        def update_from_text4(text):
            """テキストボックス4からの更新"""
            try:
                val = float(text)
                val = np.clip(val, RobotConfig.THETA4_MIN_DEG,
                              RobotConfig.THETA4_MAX_DEG)
                slider_theta4.set_val(val)
            except ValueError:
                pass

        def reset(event):
            """リセットボタンが押されたときの処理"""
            slider_theta1.reset()
            slider_theta2.reset()
            slider_theta3.reset()
            slider_theta4.reset()

        slider_theta1.on_changed(update)
        slider_theta2.on_changed(update)
        slider_theta3.on_changed(update)
        slider_theta4.on_changed(update)

        text_theta1.on_submit(update_from_text1)
        text_theta2.on_submit(update_from_text2)
        text_theta3.on_submit(update_from_text3)
        text_theta4.on_submit(update_from_text4)

        reset_button.on_clicked(reset)

        plt.show()


def inverse_kinematics(px: int, py: int, pz: int, len_1: int, len_2: int):
    try:
        # XY平面上の距離
        dxy = np.sqrt(px*px + py*py)
        # 目標位置までの3D距離
        pow_reach = px*px + py*py + pz*pz
        arm_reach = np.sqrt(pow_reach)

        # ベース回転角（Z軸周り）
        theta0 = np.arctan2(py, px)
        # 余弦定理で肘関節の角度を計算
        cos_theta1 = (len_1*len_1 + len_2*len_2 - pow_reach) / (2*len_1*len_2)
        # 範囲チェック
        if arm_reach > (len_1+len_2):
            print("[ERROR] Target is out of reach! Len:", arm_reach)
            return (0, 0, 0)
        elif abs(cos_theta1) > 1.0:
            print("[ERROR] Target is out of reach! angle:", cos_theta1)
            return (0, 0, 0)
        else:
            theta2 = np.pi - np.arccos(cos_theta1)

            # 角度計算
            alpha = np.arctan2(pz, dxy)
            beta = np.arccos((len_1 + len_2*np.cos(theta2)) / arm_reach)
            theta1 = np.pi/2 - (alpha + beta)

            return (theta0, theta1, theta2)
    except Exception as e:
        print("[ERROR] Inverse Kinematics Error:", e)
        return (0, 0, 0)


if __name__ == "__main__":
    print("# robot_arm_simulator")
    # ロボットの作成(設定ファイルのパラメータを使用)
    robot = ThreeAxisRobot(
        RobotConfig.LINK1_LENGTH,
        RobotConfig.LINK2_LENGTH,
        RobotConfig.LINK3_LENGTH
    )
    # シミュレータの作成
    simulator = RobotSimulator(robot)

    # 逆運動学による計算
    inverse_kinematics_result = inverse_kinematics(
        RobotConfig.TARGET_POINT_X,
        RobotConfig.TARGET_POINT_Y,
        RobotConfig.TARGET_POINT_Z,
        RobotConfig.LINK1_LENGTH,
        RobotConfig.LINK2_LENGTH + RobotConfig.LINK3_LENGTH
    )

    # インタラクティブ制御の開始
    simulator.interactive_control(
        inverse_kinematics_result[0],
        inverse_kinematics_result[1],
        inverse_kinematics_result[2],
        0.0)
