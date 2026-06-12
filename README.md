# Raspberry Pi Smart Lock System

## Overview

The Raspberry Pi Smart Lock System is an intelligent access control solution that integrates facial recognition, anti-spoofing detection, Firebase Realtime Database, QR code registration, and remote monitoring capabilities. The system is designed to improve security by providing multi-layer authentication and real-time notifications for unauthorized access attempts.

---

## Features

### Face Recognition

* Detects and identifies authorized users.
* Supports multiple registered users.
* Automatically grants access upon successful authentication.

### Anti-Spoofing Detection

* Utilizes a TensorFlow-based liveness detection model.
* Prevents unauthorized access through photographs or digital screen attacks.
* Enhances system security by validating real human presence.

### Firebase Realtime Database Integration

* Enables real-time communication between the smart lock and cloud services.
* Synchronizes door status information.
* Supports remote monitoring and control.

### QR Code Registration

* Generates registration QR codes for authorized enrollment.
* Simplifies user registration.
* Automates image collection for model training.

### Smart Lock Control

* Controls a servo motor-based locking mechanism.
* Supports automatic unlocking after successful authentication.
* Includes manual override functionality.

### Email Notification System

* Sends alerts when unknown individuals are detected.
* Attaches captured images for review.
* Provides timestamped security notifications.

### Status Indicators

| Indicator  | Description           |
| ---------- | --------------------- |
| White LED  | Processing / Training |
| Orange LED | Registration Mode     |
| Green LED  | Access Granted        |
| Red LED    | Access Denied         |

---

## System Architecture

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
      ├── Authorized User
      │       │
      │       ▼
      │   Unlock Door
      │
      └── Unknown User
              │
              ▼
         Email Alert
              │
              ▼
         Firebase Log
```

---

## Hardware Requirements

| Component                | Quantity |
| ------------------------ | -------- |
| Raspberry Pi 4 Model B   | 1        |
| USB Webcam or Pi Camera  | 1        |
| Servo Motor (SG90/MG90S) | 1        |
| Push Buttons             | 2        |
| LEDs                     | 4        |
| Breadboard               | 1        |
| Jumper Wires             | Multiple |
| Power Supply             | 1        |

---

## GPIO Configuration

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

## Software Requirements

### Operating System

* Raspberry Pi OS Bullseye
* Raspberry Pi OS Bookworm

### Programming Language

* Python 3.9 or later

### Libraries and Frameworks

* OpenCV
* TensorFlow
* NumPy
* face_recognition
* Firebase Admin SDK
* pyzbar
* RPi.GPIO

---

## Project Structure

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

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/raspberrypi4-smartlock.git

cd raspberrypi4-smartlock
```

### Create a Virtual Environment

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Firebase Configuration

### Step 1: Create a Firebase Project

Create a project using Firebase Console and enable Realtime Database.

### Step 2: Generate Service Account Credentials

Navigate to:

```text
Project Settings
    → Service Accounts
        → Generate New Private Key
```

Download the generated JSON file and place it inside the project.

### Step 3: Configure the Application

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

## User Registration Process

1. Press the registration button.
2. Generate a QR code.
3. Verify the QR code.
4. Enter registration mode.
5. Capture facial images.
6. Store images in the dataset directory.
7. Retrain the recognition model.
8. Add the user to the authorized database.

---

## Authentication Workflow

1. Detect face from camera feed.
2. Generate facial encoding.
3. Compare against registered users.
4. Perform anti-spoofing verification.
5. Grant or deny access.

### Authorized User

* Unlock door.
* Store entry record.
* Update Firebase database.

### Unknown User

* Capture image.
* Send email alert.
* Deny access.

---

## Security Considerations

The following files should never be uploaded to GitHub:

```gitignore
service-account.json
.env
*.jpg
*.png
venv/
__pycache__/
```

Sensitive information such as Firebase credentials and email passwords should be stored using environment variables.

---

## Tested Environment

| Component          | Version       |
| ------------------ | ------------- |
| Raspberry Pi       | 4 Model B     |
| Python             | 3.9           |
| OpenCV             | 4.x           |
| TensorFlow         | 2.x           |
| Firebase Admin SDK | Latest Stable |
| face_recognition   | Latest Stable |

---

## Future Improvements

* Mobile application integration
* Web-based administration dashboard
* Access history and audit logs
* Cloud image storage
* RFID backup authentication
* Multi-user management system
* Remote lock and unlock controls

---

## Authors

G13 Development Team

Capstone Project

Raspberry Pi Smart Lock with Face Recognition, Anti-Spoofing Detection, and Firebase Realtime Database Integration

---

## License

This project is intended for educational and research purposes.
