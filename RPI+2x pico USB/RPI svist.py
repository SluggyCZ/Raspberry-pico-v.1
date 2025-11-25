import serial
import threading
from flask import Flask

# Cesty uprav podle tvého RPi
PICO_BUTTON = "/dev/ttyACM0"
PICO_LED = "/dev/ttyACM1"

ser_button = serial.Serial(PICO_BUTTON, 115200, timeout=1)
ser_led = serial.Serial(PICO_LED, 115200, timeout=1)

led_state = "OFF"

app = Flask(__name__)

# ----------------------- LED CONTROL -----------------------
def toggle_led():
    global led_state

    if led_state == "OFF":
        ser_led.write(b"LED_ON\n")
        led_state = "ON"
    else:
        ser_led.write(b"LED_OFF\n")
        led_state = "OFF"

    print("LED je nyní:", led_state)
    return led_state


# ----------------------- WEB UI -----------------------
@app.route("/")
def index():
    html = f"""
    <html>
    <head><title>LED Toggler</title></head>
    <body style="font-family:Arial; text-align:center; margin-top:60px;">

        <h1>LED Toggle</h1>

        <button onclick="fetch('/toggle').then(()=>location.reload())"
        style="padding:20px; font-size:22px; background:#333; color:white; border-radius:10px;">
            Přepnout LED
        </button>

        <h2 style="margin-top:40px;">
            Stav LED: {led_state}
        </h2>
    </body>
    </html>
    """
    return html

@app.route("/toggle")
def toggle():
    return toggle_led()


# ----------------------- BUTTON LISTENER -----------------------
def listen_button():
    global led_state

    while True:
        line = ser_button.readline().decode().strip()

        if line == "BUTTON_PRESSED":
            print("Fyzicke tlacitko -> toggle")
            toggle_led()


threading.Thread(target=listen_button, daemon=True).start()

# ----------------------- START SERVERU -----------------------
app.run(host="0.0.0.0", port=5000)
