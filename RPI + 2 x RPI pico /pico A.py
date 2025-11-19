from machine import Pin, UART
import time

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
button = Pin(15, Pin.IN, Pin.PULL_UP)

last_state = 1

while True:
    state = button.value()
    if state != last_state:
        if state == 0:  # stisk
            uart.write("BUTTON_PRESS\n")
        last_state = state
    time.sleep(0.02)