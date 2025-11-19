from machine import Pin, UART
import time

uart = UART(1, baudrate=115200, tx=Pin(0), rx=Pin(1))
led = Pin(16, Pin.OUT)

while True:
    if uart.any():
        cmd = uart.readline().decode().strip()
        if cmd == "ON":
            led.value(1)
        elif cmd == "OFF":
            led.value(0)