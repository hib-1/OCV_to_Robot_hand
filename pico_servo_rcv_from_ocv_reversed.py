# Combined LED and Servo control based on finger state input
# Date: 2025-08-10

from machine import Pin
from servo import Servo
import sys
import select

# Define GPIO pins for LEDs and Servos
led_pins = [15, 14, 13, 12, 11]   # LEDs for fingers 0–4
#servo_pins = [0, 1, 2, 3, 4]      # Servos for fingers 0–4
servo_pins = [4,3, 2, 1,0]      # Servos for fingers 0–4

# Initialize LED objects
leds = [Pin(pin_num, Pin.OUT) for pin_num in led_pins]

# Initialize Servo objects
servos = [Servo(pin=pin_num) for pin_num in servo_pins]

print("Pico is ready to receive finger states...")

def update_outputs(state_string):
    for i in range(5):
        if i < len(state_string):
            state = state_string[i]
            # Update LED
            leds[i].value(1 if state == '1' else 0)
            # Update Servo
            servos[i].move(180 if state == '1' else 0)
        else:
            leds[i].off()
            servos[i].move(0)

while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        data = sys.stdin.readline().strip()
        print("Received:", data)

        if len(data) == 5 and all(c in "01" for c in data):
            update_outputs(data)
