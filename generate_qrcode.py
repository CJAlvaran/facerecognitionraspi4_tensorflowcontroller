import cv2
import time
import RPi.GPIO as GPIO
import threading
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import qrcode
from datetime import datetime

# GPIO pin definitions
REGISTER_BUTTON_PIN = 6
ORANGE_LED_PIN = 23

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Setup GPIO pins
GPIO.setup(REGISTER_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ORANGE_LED_PIN, GPIO.OUT)

# Helper functions for LEDs
def turn_on_led(led_pin):
    GPIO.output(ORANGE_LED_PIN, GPIO.LOW)
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off_all_leds():
    GPIO.output(ORANGE_LED_PIN, GPIO.LOW)

# Email setup for sending QR code
def send_email_with_image(image_path, subject, body):
    sender_email = "raspberrysecurelock24@gmail.com"
    receiver_email = "randlemontilla0719@gmail.com"

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

# Generate QR code and send via email
def send_qr_code_email():
    qr_data = "verifieduser"
    qr = qrcode.make(qr_data)
    qr_image_path = "/home/crj/venv/verifieduser_qr.png"
    qr.save(qr_image_path)

    subject = "Verified User QR Code"
    body = f"""
    Dear User,

    Welcome to G13 Smart Lock System!
    
    We have generated a QR Code for new user registration, please make sure to save and secure this email to avoid unnecessary issues.

    To complete your registration, please scan the QR code attached to this email using your mobile device and scan the QR code in the application.

    Once scanned, the system will let you prepare for 5 seconds before starting the face capture, it may take up to 10 to 15 minutes to complete the registration process.

    If you encounter any issues, please contact our support team at (+63)9705172899 or raspberrysecurelock24@gmail.com.
    

    Thank you for joining us!

    Best regards,  
    Your Face Recognition System
    G13 Dev Team
    """

    send_email_with_image(qr_image_path, subject, body)
    print("QR Code sent via email.")

# QR Code detection loop
try:
    while True:
        # Check if the register button is pressed
        if GPIO.input(REGISTER_BUTTON_PIN) == GPIO.LOW:
            print("Button pressed, generating QR code...")
            turn_on_led(ORANGE_LED_PIN)
            send_qr_code_email()  # Send the email with the QR code
            time.sleep(1)  # Prevent rapid triggering
            turn_off_all_leds()

        time.sleep(0.1)  # Small delay to avoid high CPU usage
finally:
    GPIO.cleanup()
