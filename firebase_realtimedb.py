import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

with open('/home/crj/venv/name.txt', 'r') as f:
    knownname = f.read().strip()

# Initialize Firebase
cred = credentials.Certificate('/home/crj/venv/raspberrypi4-smartlock-firebase-adminsdk-io2uo-57e7bf5425.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://raspberrypi4-smartlock-default-rtdb.firebaseio.com'
})

# Email setup
def send_email_with_image(image_path, user_email):
    sender_email = "raspberrysecurelock24@gmail.com"
    subject = "Face Recognition Alert: Known User Detected"
    body = f"""
    Dear User,

    A known individual has been detected at your premises on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

    The snapshot of the detected person is attached to this email.

    If you have any concerns, please contact us at raspberrysecurelock24@gmail.com.

    Best regards,
    Your Face Recognition System
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read(), name=os.path.basename(image_path))
        msg.attach(img)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    gmail_app_password = 'bumc ohcq zaiu gvdl'  # Make sure to use your correct app password

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, gmail_app_password)
            server.sendmail(sender_email, user_email, msg.as_string())
        print(f"Email sent to {user_email} with image {os.path.basename(image_path)}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def upload_to_firebase(filename, user_email):
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Prepare the data to upload
    data = {
        'filename': knownname,
        'timestamp': timestamp
    }

    # Determine the next entry key
    ref = db.reference('user_files')
    
    # Fetch all existing entries
    all_entries = ref.get()

    # Find the next available key (e.g., entry1, entry2, entry3)
    if all_entries:
        next_entry_number = len(all_entries) + 1
    else:
        next_entry_number = 1

    # Create the key as entry1, entry2, etc.
    entry_key = f'entry{next_entry_number}'

    # Set the data under the custom key
    ref.child(entry_key).set(data)

    print(f"Uploaded {filename} to Firebase with key {entry_key} at {timestamp}")

    # Send email with the image attached
    send_email_with_image(filename, user_email)

# Example usage: upload the filename and send the email
filename = "/home/crj/venv/dataset/userin/User-Door_In.jpg"  # Replace with the actual image path
user_email = "randlemontilla0719@gmail.com"  # Replace with the user's email
upload_to_firebase(filename, user_email)

