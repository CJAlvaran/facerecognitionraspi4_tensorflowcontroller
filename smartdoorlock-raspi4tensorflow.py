import cv2
from pyzbar.pyzbar import decode
import time
import RPi.GPIO as GPIO
import threading
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import tensorflow as tf
import numpy as np
import subprocess
import face_recognition
import firebase_admin
from firebase_admin import credentials, db

# Load TensorFlow anti-spoofing model
model = tf.keras.models.load_model('/home/crj/venv/dataset/yolov8conn-tensormodel.keras')

# Firebase setup
cred = credentials.Certificate('/home/crj/venv/raspberrypi4-smartlock-firebase-adminsdk-io2uo-57e7bf5425.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://raspberrypi4-smartlock-default-rtdb.firebaseio.com/'
})

# GPIO pin definitions
SERVO_PIN = 17
REGISTER_BUTTON_PIN = 6
OPEN_BUTTON_PIN = 21
WHITE_LED_PIN = 16
RED_LED_PIN = 26
GREEN_LED_PIN = 11
ORANGE_LED_PIN = 23

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Setup GPIO pins
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(REGISTER_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(OPEN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(WHITE_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(ORANGE_LED_PIN, GPIO.OUT)

# Setup PWM on the servo pin
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

# Helper functions for LEDs
def turn_on_led(led_pin):
    GPIO.output(WHITE_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(ORANGE_LED_PIN, GPIO.LOW)
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off_all_leds():
    GPIO.output(WHITE_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(ORANGE_LED_PIN, GPIO.LOW)

# Servo control
def set_servo_angle(angle):
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)

# Email setup
def send_email_with_image(image_path):
    sender_email = "raspberrysecurelock24@gmail.com"
    receiver_email = "randlemontilla0719@gmail.com"
    subject = "Unknown Person Detected!"
    body = f"""
    Dear User,

    This is an automated alert from your face recognition system.

    An unknown individual has been detected at your premises on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

    For your reference, a snapshot of the detected person is attached to this email.
    

    If you do not recognize this individual or need further assistance, please contact G13 Development Team at (+63)9705172899 or raspberrysecurelock24@gmail.com.

    Please take the necessary action.
    

    Best regards,  
    Your Face Recognition System
    G13 Dev Team
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read(), name=os.path.basename(image_path))
        msg.attach(img)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    gmail_app_password = 'bumc ohcq zaiu gvdl'

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, gmail_app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# TensorFlow preprocessing
def preprocess_face(face):
    face_resized = cv2.resize(face, (224, 224))
    face_normalized = face_resized / 255.0
    return np.expand_dims(face_normalized, axis=0)

# Initialize webcam
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Could not open video stream.")
    exit()

video_capture.set(3, 640)
video_capture.set(4, 480)
video_capture.set(cv2.CAP_PROP_FPS, 25)

# Load known faces
known_face_encodings = []
known_face_names = []
known_images_folder = "/home/crj/venv/dataset/real"
os.makedirs(known_images_folder, exist_ok=True)

for image_filename in os.listdir(known_images_folder):
    image_path = os.path.join(known_images_folder, image_filename)
    if image_path.endswith(('.jpg', '.jpeg', '.png')):
        name = os.path.splitext(image_filename)[0]
        known_image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(known_image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
            print(f"Loaded and encoded {name}")

# Persistent User ID Counter
USER_ID_FILE = "/home/crj/venv/dataset/user_id_counter.txt"

def get_next_user_id():
    if os.path.exists(USER_ID_FILE):
        with open(USER_ID_FILE, 'r') as file:
            last_user_id = int(file.read().strip())
    else:
        last_user_id = 0
    return last_user_id + 1

def save_user_id(user_id):
    with open(USER_ID_FILE, 'w') as file:
        file.write(str(user_id))

# Frame processing thread
frame_to_process = None
def capture_frames():
    global frame_to_process
    while True:
        ret, frame = video_capture.read()
        if ret:
            frame_to_process = frame

capture_thread = threading.Thread(target=capture_frames)
capture_thread.daemon = True
capture_thread.start()

# Register a new face
def register_new_face(frame):
    current_user_id = get_next_user_id()
    captured_images_count = 0
    user_id = f"userid_{str(current_user_id).zfill(2)}"

    turn_on_led(ORANGE_LED_PIN)
    turn_on_led(WHITE_LED_PIN)  # White LED should be on during capture
    print("Registering a new face...")

    # Capture 75 images for the new user
    while captured_images_count < 75:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        image_filename = f"{user_id}_{str(captured_images_count + 1).zfill(2)}_{timestamp}.jpg"
        image_path = os.path.join(known_images_folder, image_filename)
        cv2.imwrite(image_path, frame)
        print(f"Saved: {image_path}")
        captured_images_count += 1
        time.sleep(0.1)

    # Save the updated user id counter
    save_user_id(current_user_id)

    turn_off_all_leds()

    # Trigger model training after registration
    print("Training the model...")
    turn_on_led(WHITE_LED_PIN)  # Keep white LED on during training
    subprocess.call(["python3", "/home/crj/venv/model_training.py"])  # Trigger model training
    print("Model training complete!")
    turn_off_all_leds()

# QR Code and face detection loop
last_email_time = 0
email_interval = 60
capturing_images = False
captured_images_count = 0

# Function to handle changes in qr_status
# Function to handle changes in qr_status
def qr_status_listener(event):
    if event.data is True:
        print("QR Code Verified! Generating QR Code...")
        # Directly trigger the QR code generation script
        subprocess.Popen(["python3", "/home/crj/venv/generate_thruweb.py"])
    elif event.data is False:
        print("QR Code not verified or reset.")

# Attach the listener to qr_status in Firebase
try:
    db.reference('qr_status').listen(qr_status_listener)
except Exception as e:
    print(f"Error setting up listener for qr_status: {e}")


# Function to read door status from Firebase
def get_door_status():
    ref = db.reference('door_status')  # Path to your doorstatus in the database
    door_status = ref.get()
    return door_status

try:
    while True:
        if frame_to_process is not None:
            frame = frame_to_process.copy()

            # Check door status from Firebase
            door_status = get_door_status()

            if door_status == True:
                # Door is open, move servo to 180 and turn on green LED
                set_servo_angle(180)
                turn_off_all_leds()
                turn_on_led(GREEN_LED_PIN)
            elif door_status == False:
                # Door is closed, move servo to 0 and turn off LEDs
                set_servo_angle(0)
                turn_off_all_leds()

            # QR Code detection
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                if qr_data == "verifieduser":
                    print("QR Code verified user detected.")
                    turn_on_led(ORANGE_LED_PIN)
                    time.sleep(5)
                    turn_off_all_leds()

                    # Increment and save new user ID after QR verification
                    current_user_id = get_next_user_id()  # Get the next user ID
                    user_id = f"userid_{str(current_user_id).zfill(2)}"  # Format the user ID
                    save_user_id(current_user_id)  # Save the new user ID to the file

                    capturing_images = True
                    captured_images_count = 0
                    break
            if GPIO.input(REGISTER_BUTTON_PIN) == GPIO.LOW:  # Button is pressed
                turn_on_led(ORANGE_LED_PIN)  # Turn on orange LED
                subprocess.Popen(["python3", "/home/crj/venv/generate_qrcode.py"])
                time.sleep(1)  # Sleep for a short time to avoid multiple triggers
                turn_off_all_leds()
                
            if GPIO.input(OPEN_BUTTON_PIN) == GPIO.LOW:
                turn_off_all_leds()
                turn_on_led(GREEN_LED_PIN)
                set_servo_angle(180)
                time.sleep(5)
                set_servo_angle(0)
                turn_off_all_leds()
                

            # If we are capturing images after QR code scan
            if capturing_images:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                image_filename = f"{user_id}_{str(captured_images_count + 1).zfill(2)}_{timestamp}.jpg"
                image_path = os.path.join(known_images_folder, image_filename)
                cv2.imwrite(image_path, frame)  # Capture image
                print(f"Image saved: {image_path}")
                captured_images_count += 1

                if captured_images_count >= 75:
                    capturing_images = False
                    print("Registration complete!")
                    turn_off_all_leds()
                    
                    print("Training the model...")
                    turn_on_led(WHITE_LED_PIN)  # Keep white LED on during training
                    subprocess.call(["python3", "/home/crj/venv/model_training.py"])  # Trigger model training
                    print("Model training complete!")
                    turn_off_all_leds()

            # Face recognition part
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            if face_locations:
                # Select the first detected face
                first_face_location = face_locations[0]
                first_face_encoding = face_encodings[0]

                matches = face_recognition.compare_faces(known_face_encodings, first_face_encoding, tolerance=0.4)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Anti-spoofing using TensorFlow model
                top, right, bottom, left = first_face_location
                face_region = frame[top:bottom, left:right]
                processed_face = preprocess_face(face_region)
                prediction = model.predict(processed_face)
                print(f"Prediction: {prediction[0][0]}")  # Print the prediction value for debugging

                is_real = prediction[0][0] > 0.5  # Adjust threshold as needed

                if name != "Unknown":
                    color = (0, 255, 0)  # Green
                    label = f"{name} - Real"
                    set_servo_angle(180)
                    turn_off_all_leds()
                    turn_on_led(GREEN_LED_PIN)
                        # Save the image of the known person
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_filename = f"/home/crj/venv/dataset/userin/User-Door_In.jpg"  # Save in userin folder
                    cv2.imwrite(image_filename, frame)  # Save the image

                    with open('/home/crj/venv/name.txt', 'w') as f:
                        f.write(name)

                        # Transfer image to another script
                    subprocess.call(['python3', '/home/crj/venv/firebase_realtimedb.py', image_filename, name])

                else:
                    color = (0, 0, 255)  # Red
                    label = "Unknown - Real"
                    set_servo_angle(0)
                    turn_off_all_leds()
                    turn_on_led(RED_LED_PIN)
                        # Email sending for unknown face
                    current_time = time.time()
                    if current_time - last_email_time >= email_interval:
                        screenshot_filename = f"/home/crj/venv/dataset/unknown/unknown_{int(current_time)}.jpg"
                        cv2.imwrite(screenshot_filename, frame)
                        send_email_with_image(screenshot_filename)
                        last_email_time = current_time

                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            cv2.imshow("Face Recognition with Anti-Spoofing", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    cv2.destroyAllWindows()
    video_capture.release()