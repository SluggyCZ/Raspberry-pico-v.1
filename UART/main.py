from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

print("Pico chat připraven! Piš zprávy a stiskni Enter...")

while True:
    # Kontrola příchozích zpráv (non-blocking)
    if uart.any():
        data = uart.read().decode("utf-8").strip()
        if data:
            print("Druhé Pico říká:", data)

    # Kontrola vstupu od uživatele
    try:
        message = input()  # blokuje, dokud nenapíšeš
        if message:
            uart.write((message + "\n").encode('utf-8'))
    except KeyboardInterrupt:
        break
