import pyfirmata
import time

# Set your COM port here
PORT = 'COM7'
board = pyfirmata.Arduino(PORT)

# Define pins
green_led = board.get_pin('d:2:o')
red_led = board.get_pin('d:3:o')
buzzer = board.get_pin('d:4:o')
servo = board.get_pin('d:5:s')

def unlock_door():
    print("[ACCESS GRANTED] Unlocking door...")
    green_led.write(1)
    buzzer.write(1)
    servo.write(90)
    time.sleep(1)
    buzzer.write(0)
    print("Door unlocked.")

def lock_door():
    print("[LOCKING] Locking door...")
    green_led.write(0)
    servo.write(0)

def deny_access():
    print("[ACCESS DENIED] Unknown face.")
    red_led.write(1)
    for _ in range(3):
        buzzer.write(1)
        time.sleep(0.2)
        buzzer.write(0)
        time.sleep(0.2)
    red_led.write(0)
