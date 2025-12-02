@echo off

echo # Install RobotArmSimulator and its dependencies

pushd ..

echo =========================================================
echo ## Install requirements
echo =========================================================
python -m pip install --upgrade pip
rem pip install --upgrade setuptools wheel build pyinstaller

echo =========================================================
python --version
echo =========================================================

echo =========================================================
echo ## Uninstall RobotArmSimulator
echo =========================================================
pip show robotarmsimulator -q
if %ERRORLEVEL% equ 0 (
    pip uninstall -y robotarmsimulator
)

echo =========================================================
echo ## Install RobotArmSimulator
echo =========================================================
pip install -U ./

rem "build wheel"
rem python -m build .
rem pip install -U dist/robotarmsimulator-0.1.dev2+gf5822fd4b.d20251202-py3-none-any.whl

rem "install from git"
rem pip install RobotArmSimulator@git+https://github.com/HumanoidCommonNorms/RobotArmSimulator.git

echo =========================================================
echo ## pip list
echo =========================================================
pip list

echo =========================================================
echo ## Show RobotArmSimulator
echo =========================================================
pip show robotarmsimulator

popd
