import numpy as np
import cv2
from cv2 import aruco
import time

width = 640
height = 480

url = 'http://10.10.214.170:8080/videofeed'
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(1)  # Change the camera index if needed
dictionary = aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

# Camera intrinsic parameters (to be adjusted based on your camera)
camera_matrix = np.array([[4.812065855545708359e+02,0.000000000000000000e+00,3.307193674896327025e+02], [0.000000000000000000e+00,4.809585518128358217e+02,2.530129398377878829e+02], [0.000000000000000000e+00,0.000000000000000000e+00,1.000000000000000000e+00]])
dist_coeffs = np.array([-4.043095739156457591e-02,7.325014105517174690e-01,-4.506008781255621543e-03,-2.693560294193073231e-04,-2.413315124184273852e+00])

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame,(width,height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(gray, dictionary)

    if np.all(ids is not None):
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)
        for id in ids:
            print(ids, rvecs, tvecs)
            time.sleep(2)
        
        for i in range(len(ids)):
            # aruco.drawAxis(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)
            aruco.drawDetectedMarkers(frame, corners)

    cv2.imshow('Aruco Markers', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()