# Aruco based pick and place with robotic arm (5 DOF)

This repository contains the inverse Kinematics solver in python and arduino code to control servo motor using a 16-Channel 12-bit PWM/Servo Driver.

IKSolver will communicate with Arduino through Serial communication for rotating joint angles.
It uses aruco marker to detect the object and give it to IK solver for pick and place.
