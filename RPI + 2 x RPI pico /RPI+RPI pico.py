from flask import Flask, render_template_string, request, redirect, url_for
import serial
import threading
import time

# UARTy
serA = serial.Serial("/dev/serial0", 115200, timeout=0.1)  # Pico A
serB = serial.Serial("/dev/ttyAMA3", 115200, timeout=0.1)  # Pico B (UART3)

led_state = False
button_state = False

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LED Control</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; background:#222; color:white; }
        button { font-size: 22px; padding: 15px 40px; margin: 20px; border:none; border-radius:10px; cursor:pointer; }
        .on { background-color: limegreen; }
        .off { background-color: crimson; }
    </style>
</head>
<body>
    <h1>💡 Ovládání LED</h1>
    <p>Tlačítko na Pico A: <strong>{{ 'STISKNUTO' if button_state else 'VOLNO' }}</strong></p>
    <p>LED stav: <strong>{{ 'ZAPNUTA' if led_state else 'VYPNUTA' }}</strong></p>
    <form action="/toggle" method="post">
        <button type="submit" class="{{ 'off' if led_state else 'on' }}">
            {{ 'Vypnout' if led_state else 'Zapnout' }}
        </button>
    </form>
</body>
</html>
"""

def send_led(state):
    global led_state
    led_state = state
    cmd = "ON\n" if state else "OFF\n"
    serB.write(cmd.encode())

def read_picoA():
    global button_state
    while True:
        if serA.in_waiting:
            msg = serA.readline().decode().strip()
            if msg == "BUTTON_PRESS":
                button_state = not button_state
                send_led(button_state)
        time.sleep(0.02)

threading.Thread(target=read_picoA, daemon=True).start()

@app.route("/")
def index():
    return render_template_string(HTML, led_state=led_state, button_state=button_state)

@app.route("/toggle", methods=["POST"])
def toggle():
    send_led(not led_state)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
