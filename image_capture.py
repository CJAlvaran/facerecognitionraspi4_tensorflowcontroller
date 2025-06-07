import cv2
import os
from datetime import datetime

# Directory to save images
save_dir = "/home/crj/venv/dataset/real"
os.makedirs(save_dir, exist_ok=True)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Press 'r' to start capturing images.")
print("Press 'q' to quit.")

image_count = 0
capture_enabled = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting.")
        break

    # Display the frame
    cv2.imshow("Webcam", frame)

    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):  # Start capturing on 'r' key
        capture_enabled = True
        print("Capturing started...")

    if capture_enabled and image_count < 100:
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        image_path = os.path.join(save_dir, f"image_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        print(f"Saved: {image_path}")
        image_count += 1

    if image_count >= 100:
        print("Captured 100 images.")
        capture_enabled = False

    if key == ord('q'):  # Quit on 'q' key
        print("Exiting.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
