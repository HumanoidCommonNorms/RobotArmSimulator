@echo off

echo "Install RobotArmSimulator and its dependencies"

pushd ..

echo =========================================================
echo "Install requirements"
echo =========================================================
python -m pip install --upgrade pip
rem pip install --upgrade setuptools wheel build pyinstaller

echo =========================================================
python --version
echo =========================================================


echo =========================================================
echo "Install RobotArmSimulator"
echo =========================================================
pip uninstall -y robot-arm_simulator
pip install -U ./

rem "build wheel"
rem python -m build .
rem cd dist
rem pip install -U [--.whl]

rem "install from git"
rem pip install RobotArmSimulator@git+https://github.com/HumanoidCommonNorms/RobotArmSimulator.git

echo =========================================================
echo "pip list"
echo =========================================================
pip list

echo =========================================================
echo "Show RobotArmSimulator"
echo =========================================================
pip show robot-arm_simulator

popd
