import machine
import time
import sys

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

last = 0

while True:
    state = button.value()

    if state == 1 and last == 0:
        print("BUTTON_PRESSED")

    last = state
    time.sleep(0.05)
