@echo off

echo "Create executable with PyInstaller"

pushd ..
    pyinstaller -n RobotArmSimulator src\robot_arm_simulator\__main__.py  --onefile --console
    rem --clean
popd
