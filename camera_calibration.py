import numpy as np
import cv2
import time
# Number of inner corners in the checkerboard
CHECKERBOARD_SIZE = (9, 6)

# Criteria for termination of the iterative process of corner refinement
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Arrays to store object points and image points from all images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
objp = np.zeros((CHECKERBOARD_SIZE[0] * CHECKERBOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD_SIZE[0], 0:CHECKERBOARD_SIZE[1]].T.reshape(-1, 2)

# Capture video from the default camera (0)
# url = 'http://10.10.214.170:8080/videofeed'
cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

for i in range(600):
    ret, frame = cap.read()
    init = time.time()
    if not ret:
        print("Error: Unable to capture frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD_SIZE, None)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)

        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners_refined)

        # Draw and display the corners
        frame = cv2.drawChessboardCorners(frame, CHECKERBOARD_SIZE, corners_refined, ret)
    
    cv2.imshow('frame', frame)
    # time.sleep(0.5)
    end = time.time()
    print(1. / (end-init))
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any open windows
cap.release()
cv2.destroyAllWindows()

# Calibrate camera
if len(objpoints) > 0 and len(imgpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Print the camera matrix and distortion coefficients
    print("Camera Matrix:")
    print(mtx)
    print("\nDistortion Coefficients:")
    print(dist)

    # Save calibration parameters
    np.savez("calibration_params.npz", mtx=mtx, dist=dist)
    file1 = "/cameraMatrix.txt"
    np.savetxt(file1, mtx, delimiter=',')
    file2 = "/cameraDistortion.txt"
    np.savetxt(file2, dist, delimiter=',')
else:
    print("Error: No corners detected for calibration.")
# import pygame.camera
# import pygame.image
# import requests
# import numpy as np
# import cv2

# # Initialize Pygame
# pygame.init()
# pygame.camera.init()

# # URL of the remote camera feed
# camera_url = "http://10.10.214.170:8080/videofeed"

# # Main loop
# running = True
# while running:
#     print('ho')
#     # Retrieve a frame from the camera feed
#     response = requests.get(camera_url)

#     if response.status_code == 200:
#         # Convert the raw image data to a Pygame surface
#         image = pygame.image.load_extended(response.content)

#         # Convert Pygame surface to OpenCV format
#         frame = pygame.surfarray.pixels3d(image)
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

#         # Display the frame
#         cv2.imshow("Remote Camera Feed", frame)

#     # Check for quit event
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Break the loop when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Clean up
# pygame.camera.quit()
# pygame.quit()
# cv2.destroyAllWindows()
