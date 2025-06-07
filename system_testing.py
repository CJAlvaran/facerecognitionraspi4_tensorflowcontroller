import RPi.GPIO as GPIO
import time

# Pin configuration
SERVO_PIN = 17
REGISTER_BUTTON_PIN = 6
OPEN_BUTTON_PIN = 21
WHITE_LED_PIN = 16
RED_LED_PIN = 26
GREEN_LED_PIN = 11
ORANGE_LED_PIN = 23

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([WHITE_LED_PIN, RED_LED_PIN, GREEN_LED_PIN, ORANGE_LED_PIN], GPIO.OUT)
GPIO.setup([REGISTER_BUTTON_PIN, OPEN_BUTTON_PIN], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Initialize servo
servo = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz for servo control
servo.start(0)

def test_leds():
    leds = [WHITE_LED_PIN, RED_LED_PIN, GREEN_LED_PIN, ORANGE_LED_PIN]
    for led in leds:
        GPIO.output(led, GPIO.HIGH)
        print(f"LED on PIN {led} ON")
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)
        print(f"LED on PIN {led} OFF")
        time.sleep(0.5)

def test_servo():
    print("Testing servo...")
    for angle in [0, 90, 180]:
        duty_cycle = 2 + (angle / 18)
        servo.ChangeDutyCycle(duty_cycle)
        print(f"Servo at {angle}°")
        time.sleep(1)
    servo.ChangeDutyCycle(0)  # Stop signal

def test_buttons():
    print("Press the buttons to test them.")
    try:
        while True:
            if not GPIO.input(REGISTER_BUTTON_PIN):
                print("Register button pressed!")
                time.sleep(0.3)
            if not GPIO.input(OPEN_BUTTON_PIN):
                print("Open button pressed!")
                time.sleep(0.3)
    except KeyboardInterrupt:
        print("Button test ended.")

try:
    test_leds()
    test_servo()
    test_buttons()
finally:
    servo.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete.")
