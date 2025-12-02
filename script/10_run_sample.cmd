@echo on

echo # Run sample script

pushd ..
    python -m robot_arm_simulator -x 0 -y 50 -z 0 -l1 100 -l2 80 -l3 40
popd
