import RPi.GPIO as GPIO
import time

# Nastavení režimu číslování pinů
GPIO.setmode(GPIO.BCM)

# Nastavení GPIO 17 jako výstupu
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

print("Blikám LEDkou...")

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Zapni LED
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)   # Zhasni LED
        time.sleep(1)

except KeyboardInterrupt:
    print("\nKonec programu")

finally:
    GPIO.cleanup()  # Uvolni piny po ukončení

