from machine import Pin, PWM
import time

# LEDky na pinech GP2–GP6
led_pins = [2, 3, 4, 5, 6]
leds = [PWM(Pin(pin)) for pin in led_pins]

for led in leds:
    led.freq(1000)  # PWM frekvence

# Tlačítko (mezi GP7 a GND, interní pull-up)
button = Pin(7, Pin.IN, Pin.PULL_UP)

value = 1  # startovní mód

# ---------- Efekty ----------
def mode1():
    """Postupné rozsvícení a zhasnutí všech LED najednou"""
    for duty in range(0, 65535, 1000):
        for led in leds:
            led.duty_u16(duty)
        time.sleep(0.005)
    for duty in range(65535, 0, -1000):
        for led in leds:
            led.duty_u16(duty)
        time.sleep(0.005)

def mode2():
    """Postupné rozsvěcení LEDek s tím, že předchozí zůstávají svítit. Pak pomalé zhasnutí."""
    step = 1000
    # Rozsvícení
    for i in range(len(leds)):
        for duty in range(0, 65535, step):
            leds[i].duty_u16(duty)
            time.sleep(0.002)
    time.sleep(0.5)  # pauza když všechny svítí
    # Zhasnutí
    for i in reversed(range(len(leds))):
        for duty in range(65535, 0, -step):
            leds[i].duty_u16(duty)
            time.sleep(0.002)
    time.sleep(0.5)

def mode3():
    """Had s delší stopou a větším kontrastem."""
    length = len(leds)
    delay = 0.08  # zpomaleno

    for offset in range(length + 5):  # +5 aby ocas byl delší
        for i in range(length):
            distance = abs(i - offset)
            if distance == 0:
                duty = 65535   # hlavní LED (plný jas)
            elif distance == 1:
                duty = 12000   # blízká LED (slabší)
            elif distance == 2:
                duty = 4000    # ještě slabší
            else:
                duty = 0       # ostatní zhasnuté
            leds[i].duty_u16(duty)
        time.sleep(delay)

# ---------- Hlavní loop ----------
while True:
    # Obsluha tlačítka – přepínání hodnot
    if button.value() == 0:  # tlačítko stisknuté
        value += 1
        if value > 3:  # jen 3 módy
            value = 1
        print("Režim:", value)

        while button.value() == 0:  # počkej na uvolnění
            time.sleep(0.01)

    # Spouštění efektů podle režimu
    if value == 1:
        mode1()
    elif value == 2:
        mode2()
    elif value == 3:
        mode3()
