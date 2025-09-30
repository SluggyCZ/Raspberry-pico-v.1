from machine import Pin, PWM
import utime, math

# LED piny GP2–GP6
led_pins = [2, 3, 4, 5, 6]
leds = []

for pin in led_pins:
    pwm = PWM(Pin(pin))
    pwm.freq(1000)
    pwm.duty_u16(0)
    leds.append(pwm)

# Tlačítko na GP7 (mezi pin a GND, s interním pull-up)
button = Pin(7, Pin.IN, Pin.PULL_UP)

mode = 1

# --- MODE 1: fade všech LED dohromady ---
def mode1():
    for i in range(0, 65535, 500):
        for led in leds:
            led.duty_u16(i)
        utime.sleep_ms(5)
    for i in range(65535, 0, -500):
        for led in leds:
            led.duty_u16(i)
        utime.sleep_ms(5)

# --- MODE 2: postupné přidávání LED (nahoru + dolů) ---
def mode2():
    # nahoru
    for idx in range(len(leds)):
        for i in range(0, 65535, 800):
            leds[idx].duty_u16(i)
            utime.sleep_ms(2)
    utime.sleep(0.5)
    # dolů
    for idx in reversed(range(len(leds))):
        for i in range(65535, -1, -800):
            leds[idx].duty_u16(i)
            utime.sleep_ms(2)
    utime.sleep(0.5)

# --- MODE 3: had se slabým dozníváním ---
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
        utime.sleep(delay)

# --- MODE 4: breathing (všechny najednou sinus) ---
def mode4():
    period_ms = 3000
    elapsed = utime.ticks_ms()
    phase = (elapsed % period_ms) / period_ms * 2 * math.pi
    brightness = int((math.sin(phase) + 1) / 2 * 65535)
    for led in leds:
        led.duty_u16(brightness)
    utime.sleep_ms(30)

# --- MODE 5: Knight Rider wave ---
def mode5():
    wave_width = 2
    delay = 0.1
    for center in range(-wave_width, len(leds) + wave_width):
        for i, led in enumerate(leds):
            dist = abs(i - center)
            if dist <= wave_width:
                led.duty_u16(int((1 - dist / wave_width) * 65535))
            else:
                led.duty_u16(0)
        utime.sleep(delay)
    for center in range(len(leds) + wave_width, -wave_width, -1):
        for i, led in enumerate(leds):
            dist = abs(i - center)
            if dist <= wave_width:
                led.duty_u16(int((1 - dist / wave_width) * 65535))
            else:
                led.duty_u16(0)
        utime.sleep(delay)

# --- hlavní loop ---
while True:
    if button.value() == 0:  # stisk
        mode += 1
        if mode > 5:
            mode = 1
        print("Přepínám na mód:", mode)
        utime.sleep(0.3)  # debounce

    if mode == 1:
        mode1()
    elif mode == 2:
        mode2()
    elif mode == 3:
        mode3()
    elif mode == 4:
        mode4()
    elif mode == 5:
        mode5()