import cv2
import numpy as np

def get_frame(cap):
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    camera_matrix = np.array([[1182.719, 0, 927.03],
                               [0, 1186.236, 609.52],
                               [0, 0, 1]], dtype=np.float32)
    dist_coeffs = np.array([-0.5, 0.3, 0, 0, 0], dtype=np.float32)

    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (frame_width, frame_height), 1, (frame_width, frame_height))
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return

    frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

    x, y, w, h = roi
    frame = frame[y:y+h, x:x+w]

    frame = cv2.resize(frame, (int(960 * 1.3), int(540 * 1.3)))

    return frame
