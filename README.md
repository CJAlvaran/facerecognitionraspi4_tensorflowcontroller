# Raspberry Pi Smart Lock System Using Face Recognition, Anti-Spoofing Detection, and Firebase Realtime Database

# Overview

This project presents the development of a Raspberry Pi-based Smart Lock System that utilizes facial recognition, anti-spoofing detection, QR code registration, and Firebase Realtime Database integration to provide a secure and intelligent access control solution.

The system identifies authorized users through facial recognition while simultaneously verifying facial authenticity using a TensorFlow-based anti-spoofing model. Access is granted only when both identity verification and liveness detection are successful. Unauthorized access attempts trigger email notifications containing captured images of the detected individual.

The system also supports remote monitoring through Firebase Realtime Database and provides user registration through QR code verification.


# Project Overview

The Raspberry Pi Smart Lock System is an intelligent security solution designed to replace conventional lock-and-key mechanisms with biometric authentication.

The project combines:

* Face Recognition
* Anti-Spoofing Detection
* QR Code Registration
* Firebase Realtime Database
* Email Notification Services
* Servo Motor Door Control

The goal is to provide secure, automated, and remotely monitored access control.

---

# Features

## Face Recognition

* Detects and recognizes registered users.
* Uses facial encoding and matching techniques.
* Supports multiple authorized users.

## Anti-Spoofing Detection

* TensorFlow-based liveness detection.
* Prevents photo and screen spoofing attacks.
* Verifies that the detected face belongs to a real person.

## QR Code Registration

* Generates registration QR codes.
* Automates new user enrollment.
* Captures training images automatically.

## Firebase Realtime Database Integration

* Enables real-time door status synchronization.
* Supports cloud-based monitoring.
* Allows remote lock state updates.

## Email Alert System

* Sends security notifications for unknown users.
* Includes captured image attachments.
* Provides timestamps for incident tracking.

## Smart Lock Control

* Servo motor-based locking mechanism.
* Automatic unlock upon successful authentication.
* Manual override support.

---

# System Architecture

```text
Camera Module
      │
      ▼
Face Detection
      │
      ▼
Face Recognition
      │
      ▼
Anti-Spoofing Verification
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Known    Unknown
User      User
 │          │
 ▼          ▼
Unlock    Email Alert
Door         │
 │            ▼
 ▼       Firebase Log
Firebase
Update
```

---

# Hardware Requirements

| Component                | Quantity |
| ------------------------ | -------- |
| Raspberry Pi 4 Model B   | 1        |
| USB Webcam / Pi Camera   | 1        |
| Servo Motor (SG90/MG90S) | 1        |
| Push Buttons             | 2        |
| LEDs                     | 4        |
| Breadboard               | 1        |
| Jumper Wires             | Multiple |
| Power Supply             | 1        |

---

# GPIO Configuration

| Component       | GPIO Pin |
| --------------- | -------- |
| Servo Motor     | GPIO 17  |
| Register Button | GPIO 6   |
| Open Button     | GPIO 21  |
| White LED       | GPIO 16  |
| Red LED         | GPIO 26  |
| Green LED       | GPIO 11  |
| Orange LED      | GPIO 23  |

---

# Software Requirements

## Operating System

* Raspberry Pi OS Bullseye
* Raspberry Pi OS Bookworm

## Programming Language

* Python 3.9+

## Python Libraries

* OpenCV
* TensorFlow
* NumPy
* face_recognition
* firebase-admin
* pyzbar
* RPi.GPIO

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Third-Party Services

| Service                    | Purpose                          |
| -------------------------- | -------------------------------- |
| Firebase Realtime Database | Real-time cloud synchronization  |
| Gmail SMTP                 | Email notification service       |
| TensorFlow                 | Anti-spoofing inference          |
| OpenCV                     | Image acquisition and processing |
| face_recognition           | Facial recognition               |
| pyzbar                     | QR code decoding                 |

---

# Project Structure

```text
raspberrypi4-smartlock/
│
├── main.py
├── model_training.py
├── firebase_realtimedb.py
├── generate_qrcode.py
├── requirements.txt
├── README.md
│
├── dataset/
│   ├── real/
│   ├── userin/
│   ├── user_id_counter.txt
│   └── yolov8conn-tensormodel.keras
│
├── firebase/
│   └── service-account.json
│
└── docs/
```

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/yourusername/raspberrypi4-smartlock.git

cd raspberrypi4-smartlock
```

## Create Virtual Environment

```bash
python3 -m venv venv

source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Firebase Configuration

## Create Firebase Project

1. Open Firebase Console.
2. Create a new project.
3. Enable Realtime Database.

## Generate Service Account Key

1. Project Settings
2. Service Accounts
3. Generate New Private Key

Save the JSON credential file.

## Configure Firebase

```python
cred = credentials.Certificate(
    "firebase/service-account.json"
)

firebase_admin.initialize_app(
    cred,
    {
        "databaseURL":
        "https://your-project-default-rtdb.firebaseio.com/"
    }
)
```

---

# Gmail SMTP Configuration

The project uses Gmail SMTP services for sending security alerts.

## Enable Gmail App Password

1. Enable Two-Factor Authentication.
2. Navigate to Google Account → Security.
3. Open App Passwords.
4. Generate an App Password.

## Configure Application

```python
sender_email = "your-email@gmail.com"
receiver_email = "recipient@gmail.com"
gmail_app_password = "generated-app-password"
```

---

# Usage Guide

Start the application:

```bash
python3 main.py
```

The system will:

1. Initialize Firebase.
2. Load the TensorFlow model.
3. Load registered users.
4. Start camera monitoring.
5. Wait for authentication requests.

---

# User Registration Workflow

1. Press Register Button.
2. Generate QR Code.
3. Verify QR Code.
4. Enter Registration Mode.
5. Capture 75 Facial Images.
6. Save Images.
7. Train Recognition Model.
8. Register New User.

---

# Authentication Workflow

1. Detect face.
2. Generate encoding.
3. Compare against registered users.
4. Perform anti-spoofing verification.
5. Grant or deny access.

## Authorized User

* Unlock door.
* Turn on green LED.
* Save access image.
* Update Firebase.

## Unauthorized User

* Capture image.
* Send email alert.
* Deny access.

---

# Firebase Database Structure

```json
{
  "door_status": true
}
```

| Field       | Type    | Description         |
| ----------- | ------- | ------------------- |
| door_status | Boolean | Controls lock state |

---

# Security Considerations

The following files should not be committed to GitHub:

```gitignore
service-account.json
.env
*.jpg
*.jpeg
*.png
venv/
__pycache__/
```

Store all sensitive credentials using environment variables.

---

# Tested Environment

| Component          | Version       |
| ------------------ | ------------- |
| Raspberry Pi       | 4 Model B     |
| Python             | 3.9           |
| OpenCV             | 4.x           |
| TensorFlow         | 2.x           |
| Firebase Admin SDK | Latest Stable |
| face_recognition   | Latest Stable |

---

# Future Improvements

* Mobile Application Integration
* Web Dashboard
* Access Logs and Audit Trails
* RFID Backup Authentication
* Cloud Storage Integration
* Multi-User Access Management
* Remote Lock and Unlock Controls

---

# Authors

G13 Development Team

Capstone Project

Raspberry Pi Smart Lock with Face Recognition, Anti-Spoofing Detection, and Firebase Realtime Database Integration

---

# License

This project is intended for educational, academic, and research purposes.
