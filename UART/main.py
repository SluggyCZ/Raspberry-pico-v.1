from machine import UART, Pin
import time

# UART0: TX = GP0, RX = GP1
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

while True:
    # pošli zprávu
    uart.write("Ahoj z mého Pica!\n")
    
    # zkus přečíst příchozí data
    if uart.any():
        data = uart.read().decode("utf-8")
        print("Přijatá zpráva:", data)
    
    time.sleep(1)