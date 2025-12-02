@echo off

echo # Create executable with PyInstaller

pushd ..
    rmdir /s /q dist/*
    pyinstaller -n RobotArmSimulator src\robot_arm_simulator\__main__.py  --onefile --console
    rem --clean
    python -m build .
popd
