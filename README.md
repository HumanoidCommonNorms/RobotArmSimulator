# ロボットアーム シミュレータ

ロボットアームの動作を3Dで可視化するシミュレータプログラムです。

## ロボット構成

- **第1軸**: 根元の回転モーター (Z軸周り)
- **第2軸**: 根元の上下モーター (Y軸周り)
- **第3軸**: 関節モーター (Y軸周り)
- **第4軸**: 関節モーター (Y軸周り)

### インストール

必要なライブラリをインストールしてください。

```bash
pip install numpy matplotlib
```

または 仮想環境venv を使用する場合:

```bash
# Pythonのバージョン3.11.0b4でテスト済み
#pyenv install 3.11.0b4
python -m venv venv_RobotArmSimulator
venv_RobotArmSimulator/Scripts/activate
python -m pip install --upgrade pip

# pyproject.tomlがあるディレクトリで以下を実行
pip install -U ./
# または GitHub から直接インストール
pip install RobotArmSimulator@git+https://github.com/HumanoidCommonNorms/RobotArmSimulator.git

# インストールされたパッケージの確認
pip list
```

## 使い方

```bash
cd src
python -m robot_arm_simulator -x 50 -y 30 -z 20

# オプションの例
options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -x X                  X軸, デフォルト: 0
  -y Y                  Y軸, デフォルト: 0
  -z Z                  Z軸, デフォルト: 0
  --link_len1, -l1 LINK_LEN1
                        リンク1の長さ, デフォルト: 100
  --link_len2, -l2 LINK_LEN2
                        リンク2の長さ, デフォルト: 80
  --link_len3, -l3 LINK_LEN3
                        リンク3の長さ, デフォルト: 20
```


## Authors and acknowledgment

We offer heartfelt thanks to the open-source community for the invaluable gifts they've shared with us. The hardware, libraries, and tools they've provided have breathed life into our journey of development. Each line of code and innovation has woven a tapestry of brilliance, lighting our path. In this symphony of ingenuity, we find ourselves humbled and inspired. These offerings infuse our project with boundless possibilities. As we create, they guide us like stars, reminding us that collaboration can turn dreams into reality. With deep appreciation, we honor the open-source universe that nurtures us on this journey of discovery and growth.
