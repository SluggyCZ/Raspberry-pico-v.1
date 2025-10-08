import board
import digitalio
import busio
import time

BUTTON_PIN = board.GP14
I2C_ADDR = 0x08  # libovolná adresa slave

# tlačítko
button = digitalio.DigitalInOut(BUTTON_PIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # aktivní LOW

# I2C
i2c = busio.I2C(scl=board.GP27, sda=board.GP26)

while not i2c.try_lock():
    pass

print("Master ready!")

while True:
    try:
        data = bytearray([0 if button.value else 1])
        i2c.writeto(I2C_ADDR, data)
    except OSError:
        pass  # pokud slave není ready
    time.sleep(0.05)