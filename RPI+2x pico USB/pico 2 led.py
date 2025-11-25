import machine
import sys

led = machine.Pin(15, machine.Pin.OUT)

while True:
    line = sys.stdin.readline().strip()

    if line == "LED_ON":
        led.value(1)

    if line == "LED_OFF":
        led.value(0)