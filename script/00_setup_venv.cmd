@echo off

echo "Setup Python virtual environment for Three-Axis Robot Arm Simulator"

set VENV_NAME=venv_RobotArmSimulator

pip install --upgrade pip
rem =========================================================
rem "Install pyenv-win for CMD"
rem =========================================================
rem pip install pyenv-win --target %USERPROFILE%/.pyenv --upgrade
rem =========================================================
rem "Install pyenv-win for PowerShell"
rem =========================================================
rem pip install pyenv-win --target $HOME//.pyenv

rem pyenv install --list
rem pyenv install 3.11.0b4
rem pyenv local 3.11.0b4


pushd ..
echo =========================================================
echo "Remove old venv"
echo =========================================================
rmdir /s /q %VENV_NAME%

echo =========================================================
echo "venv - Create and Activate : %VENV_NAME%"
echo =========================================================
python -m venv %VENV_NAME%
popd

..\%VENV_NAME%\Scripts\activate
