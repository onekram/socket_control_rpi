import time
import cv2

def photo_maker():
    cap = cv2.VideoCapture("http://192.168.2.99:8080/?action=stream")  # Open the video stream from the camera
    cap.set(3, 320)  # Set the width of the image to 320 pixels
    cap.set(4, 320)  # Set the height of the image to 320 pixels
    i = 1

    while True:  # Infinite loop
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow("Image", frame)

        k = cv2.waitKey(1)  # Wait for a key press
        if k == ord('p'):  # If 'p' is pressed
            i += 1
            cv2.imwrite(f"camera/captured_frame_{i}.jpg", frame)  # Save the frame as an image
            print(f"Captured frame_{i}.jpg")  # Print confirmation

        if k == 27:  # If 'Esc' is pressed
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    photo_maker()
